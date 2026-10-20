// Veza s bazom za cijeli backend: jedan pool konekcija i pomoćna funkcija za transakcije.
import pg from "pg";

// date (1082) ostaje tekst "2025-12-31". Inače pg napravi Date u lokalnoj ponoći,
// a JSON ispiše prethodni dan ("2025-12-30T23:00:00.000Z").
pg.types.setTypeParser(1082, (v) => v);
// numeric (1700) i bigint (20, npr. count(*)) pg vraća kao tekst. Ovdje postaju brojevi.
pg.types.setTypeParser(1700, (v) => parseFloat(v));
pg.types.setTypeParser(20, (v) => parseInt(v, 10));

export const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL, connectionTimeoutMillis: 5000 });

// Baza (npr. Neon kad se uspava) zatvori konekciju koja miruje. Bez ovoga backend padne.
pool.on("error", (e) => console.error("Baza:", e.message));

// Upiti u fn su jedna transakcija: ili prođu svi, ili nijedan. U fn koristi client.query, ne pool.query.
// Primjer: await transakcija(async (client) => { await client.query(...); await client.query(...); });
export async function transakcija<T>(fn: (client: pg.PoolClient) => Promise<T>): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query("begin");
    const rezultat = await fn(client);
    await client.query("commit");
    return rezultat;
  } catch (e) {
    await client.query("rollback").catch(() => {});
    throw e;
  } finally {
    client.release();
  }
}
