// Provjera okruženja: aplikacija se pokreće i baza odgovara.
// Ovo nije početak aplikacije. Kad provjera prođe, zamijeni ovu stranicu svojim radom.
import { Suspense } from "react";
import { connection } from "next/server";
import { Client } from "pg";

const TABELE = ["kupci", "proizvodi", "narudzbe", "stavke_narudzbe"];

async function ProvjeraBaze() {
  await connection();

  if (!process.env.DATABASE_URL) {
    return <p>Baza: nema DATABASE_URL. Kopiraj .env.example u .env.local.</p>;
  }

  const client = new Client({ connectionString: process.env.DATABASE_URL });
  try {
    await client.connect();
    const brojevi = await Promise.all(
      TABELE.map(async (tabela) => {
        const r = await client.query(`select count(*)::int as n from ${tabela}`);
        return `${tabela}: ${r.rows[0].n}`;
      }),
    );
    return <p>Baza odgovara. {brojevi.join(", ")}.</p>;
  } catch (e) {
    return <p>Baza ne odgovara: {e instanceof Error ? e.message : String(e)}</p>;
  } finally {
    await client.end().catch(() => {});
  }
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
