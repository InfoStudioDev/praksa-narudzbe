// Backend: Hono na Node.js, port 3000. Frontend ga zove preko /api (vidi vite.config.ts).
// GET /api/provjera je samo provjera okruženja; svoje rute dodaj pored nje.
import { serve } from "@hono/node-server";
import { Hono } from "hono";
import pg from "pg";

const app = new Hono();

function opisGreske(e: unknown) {
  if (e instanceof AggregateError) return e.errors.map((x) => String(x?.message ?? x)).join("; ");
  return e instanceof Error ? e.message || e.name : String(e);
}

app.get("/api/provjera", async (c) => {
  if (!process.env.DATABASE_URL) {
    return c.json({ poruka: "Baza: nema DATABASE_URL. Kopiraj .env.example u .env.local." });
  }
  const client = new pg.Client({ connectionString: process.env.DATABASE_URL, connectionTimeoutMillis: 5000 });
  try {
    await client.connect();
    const r = await client.query(`
      select (select count(*) from kupci)::int           as kupci,
             (select count(*) from proizvodi)::int       as proizvodi,
             (select count(*) from narudzbe)::int        as narudzbe,
             (select count(*) from stavke_narudzbe)::int as stavke_narudzbe`);
    const brojevi = Object.entries(r.rows[0]).map(([tabela, n]) => `${tabela} ${n}`);
    return c.json({ poruka: `Baza odgovara: ${brojevi.join(", ")}.` });
  } catch (e) {
    return c.json({ poruka: `Baza ne odgovara: ${opisGreske(e)}` });
  } finally {
    await client.end().catch(() => {});
  }
});

// Samo na ovom računaru (127.0.0.1), da backend nije otvoren na mreži.
serve({ fetch: app.fetch, port: 3000, hostname: "127.0.0.1" }, (info) => {
  console.log(`Backend radi na http://localhost:${info.port}`);
});
