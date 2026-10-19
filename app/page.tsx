// Provjera okruženja: aplikacija se pokreće i baza odgovara.
// Kad provjera prođe, zamijeni ovu stranicu svojom aplikacijom.
import { Suspense } from "react";
import { connection } from "next/server";
import { Client } from "pg";

function opisGreske(e: unknown) {
  if (e instanceof AggregateError) return e.errors.map((x) => String(x?.message ?? x)).join("; ");
  return e instanceof Error ? e.message || e.name : String(e);
}

async function stanjeBaze(): Promise<string> {
  if (!process.env.DATABASE_URL) {
    return "Baza: nema DATABASE_URL. Kopiraj .env.example u .env.local.";
  }

  const client = new Client({
    connectionString: process.env.DATABASE_URL,
    connectionTimeoutMillis: 5000,
  });
  try {
    await client.connect();
    const r = await client.query(`
      select (select count(*) from kupci)::int           as kupci,
             (select count(*) from proizvodi)::int       as proizvodi,
             (select count(*) from narudzbe)::int        as narudzbe,
             (select count(*) from stavke_narudzbe)::int as stavke_narudzbe`);
    const brojevi = Object.entries(r.rows[0]).map(([tabela, n]) => `${tabela} ${n}`);
    return `Baza odgovara: ${brojevi.join(", ")}.`;
  } catch (e) {
    return `Baza ne odgovara: ${opisGreske(e)}`;
  } finally {
    await client.end().catch(() => {});
  }
}

async function ProvjeraBaze() {
  await connection();
  return <p>{await stanjeBaze()}</p>;
}

export default function Page() {
  return (
    <main style={{ padding: 32, fontFamily: "sans-serif", lineHeight: 1.6 }}>
      <h1>Aplikacija radi.</h1>
      <Suspense fallback={<p>Provjeravam bazu...</p>}>
        <ProvjeraBaze />
      </Suspense>
    </main>
  );
}
