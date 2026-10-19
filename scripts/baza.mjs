// Napuni bazu: izvrši data/schema.sql i data/seed.sql nad bazom iz DATABASE_URL (.env.local).
// npm run baza                 napravi tabele i učitaj početne podatke
// npm run baza -- --ispocetka  obriši tabele iz šeme i učitaj sve ponovo
import { readFileSync } from "node:fs";
import pg from "pg";

const ispocetka = process.argv.includes("--ispocetka");

if (!process.env.DATABASE_URL) {
  console.error("Nema DATABASE_URL. Kopiraj .env.example u .env.local i upiši svoj connection string.");
  process.exit(1);
}

const client = new pg.Client({ connectionString: process.env.DATABASE_URL, connectionTimeoutMillis: 10000 });
try {
  await client.connect();
  const { rows } = await client.query("select to_regclass('public.narudzbe') is not null as postoji");
  if (rows[0].postoji && !ispocetka) {
    console.log("Tabele već postoje. Za početne podatke ispočetka: npm run baza -- --ispocetka");
  } else {
    if (ispocetka) {
      await client.query("drop table if exists stavke_narudzbe, narudzbe, proizvodi, kategorije, kupci cascade");
    }
    await client.query(readFileSync("data/schema.sql", "utf8"));
    await client.query(readFileSync("data/seed.sql", "utf8"));
    console.log("Baza je spremna.");
  }
} catch (e) {
  const poruka = e instanceof AggregateError ? e.errors.map((x) => x.message).join("; ") : e.message || e.name;
  console.error(`Greška: ${poruka}`);
  process.exitCode = 1;
} finally {
  await client.end().catch(() => {});
}
