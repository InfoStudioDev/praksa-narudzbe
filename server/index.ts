// Backend: Hono na Node.js, port 3000. Frontend ga zove preko /api (vidi vite.config.ts).
// GET /api/provjera je samo provjera okruženja, a GET /api/kupci/:id primjer rute. Svoje rute dodaj pored njih.
import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { HTTPException } from "hono/http-exception";
import { z } from "zod";
import { pool } from "./db";

const app = new Hono();

function opisGreske(e: unknown) {
  if (e instanceof AggregateError) return e.errors.map((x) => String(x?.message ?? x)).join("; ");
  return e instanceof Error ? e.message || e.name : String(e);
}

// Greške iz Zoda kao { "stavke.0.kolicina": "poruka" }: isti ključevi koje forma koristi u setError.
// Greška koja nije vezana za jedno polje (npr. .refine na cijelom objektu) ide pod "root".
function poljaIzZoda(greska: z.ZodError) {
  const polja: Record<string, string> = {};
  for (const issue of greska.issues) polja[issue.path.join(".") || "root"] ??= issue.message;
  return polja;
}

app.get("/api/provjera", async (c) => {
  if (!process.env.DATABASE_URL) {
    return c.json({ poruka: "Baza: nema DATABASE_URL. Kopiraj .env.example u .env.local." });
  }
  try {
    const r = await pool.query(`
      select (select count(*) from kupci)           as kupci,
             (select count(*) from proizvodi)       as proizvodi,
             (select count(*) from narudzbe)        as narudzbe,
             (select count(*) from stavke_narudzbe) as stavke_narudzbe`);
    const brojevi = Object.entries(r.rows[0]).map(([tabela, n]) => `${tabela} ${n}`);
    return c.json({ poruka: `Baza odgovara: ${brojevi.join(", ")}.` });
  } catch (e) {
    return c.json({ poruka: `Baza ne odgovara: ${opisGreske(e)}` });
  }
});

// Primjer: jedan kupac po id-u. Neispravan zahtjev vraća 400 s porukom za svako polje.
// Vrijednost od korisnika ide u upit samo kao parametar ($1), nikad lijepljenjem u tekst upita.
const KupacParametri = z.object({
  id: z.coerce
    .number({ error: "Id mora biti broj." })
    .int({ error: "Id mora biti cijeli broj." })
    .positive({ error: "Id mora biti veći od nule." })
    .max(2147483647, { error: "Id je prevelik." }),
});

app.get("/api/kupci/:id", async (c) => {
  const ulaz = KupacParametri.safeParse({ id: c.req.param("id") });
  if (!ulaz.success) {
    return c.json({ poruka: "Neispravan zahtjev.", polja: poljaIzZoda(ulaz.error) }, 400);
  }
  const r = await pool.query(
    "select id, sifra, naziv, vrsta, grad, email, kreiran from kupci where id = $1",
    [ulaz.data.id],
  );
  if (r.rows.length === 0) return c.json({ poruka: "Kupac ne postoji." }, 404);
  return c.json(r.rows[0]);
});

// Neočekivana greška (npr. iz baze) vraća JSON s porukom, ne običan tekst "Internal Server Error".
app.onError((e, c) => {
  if (e instanceof HTTPException) return e.getResponse();
  console.error(e);
  return c.json({ poruka: `Greška na serveru: ${opisGreske(e)}` }, 500);
});

// Samo na ovom računaru (127.0.0.1), da backend nije otvoren na mreži.
serve({ fetch: app.fetch, port: 3000, hostname: "127.0.0.1" }, (info) => {
  console.log(`Backend radi na http://localhost:${info.port}`);
});
