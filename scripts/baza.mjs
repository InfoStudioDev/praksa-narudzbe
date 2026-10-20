// Napuni bazu iz DATABASE_URL (.env.local): izvrši data/schema.sql, data/seed.sql
// i tvoje migracije/*.sql, redom po imenu fajla.
// Šema prvo briše postojeće tabele, pa svako pokretanje vraća početno stanje.
import { existsSync, readdirSync, readFileSync } from "node:fs";
import pg from "pg";

if (!process.env.DATABASE_URL) {
  console.error("Nema DATABASE_URL. Kopiraj .env.example u .env.local i upiši svoj connection string.");
  process.exit(1);
}

const migracije = existsSync("migracije")
  ? readdirSync("migracije").filter((f) => f.endsWith(".sql")).sort().map((f) => `migracije/${f}`)
  : [];

const client = new pg.Client({ connectionString: process.env.DATABASE_URL, connectionTimeoutMillis: 10000 });
let fajl;
try {
  await client.connect();
  for (fajl of ["data/schema.sql", "data/seed.sql", ...migracije]) {
    await client.query(readFileSync(fajl, "utf8"));
  }
  if (migracije.length) console.log(`Migracije: ${migracije.join(", ")}`);
  console.log("Baza je spremna.");
} catch (e) {
  const poruka = e instanceof AggregateError ? e.errors.map((x) => x.message).join("; ") : e.message || e.name;
  console.error(fajl ? `Greška u ${fajl}: ${poruka}` : `Greška: ${poruka}`);
  process.exitCode = 1;
} finally {
  await client.end().catch(() => {});
}
