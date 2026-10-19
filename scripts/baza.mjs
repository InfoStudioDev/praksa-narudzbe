// Napuni bazu iz DATABASE_URL (.env.local): izvrši data/schema.sql i data/seed.sql.
// Šema prvo briše postojeće tabele, pa svako pokretanje vraća početno stanje.
import { readFileSync } from "node:fs";
import pg from "pg";

if (!process.env.DATABASE_URL) {
  console.error("Nema DATABASE_URL. Kopiraj .env.example u .env.local i upiši svoj connection string.");
  process.exit(1);
}

const client = new pg.Client({ connectionString: process.env.DATABASE_URL, connectionTimeoutMillis: 10000 });
try {
  await client.connect();
  await client.query(readFileSync("data/schema.sql", "utf8"));
  await client.query(readFileSync("data/seed.sql", "utf8"));
  console.log("Baza je spremna.");
} catch (e) {
  const poruka = e instanceof AggregateError ? e.errors.map((x) => x.message).join("; ") : e.message || e.name;
  console.error(`Greška: ${poruka}`);
  process.exitCode = 1;
} finally {
  await client.end().catch(() => {});
}
