# Narudžbe: praksa

Ovdje je samo okruženje: baza s podacima i prazna Next.js aplikacija koja provjerava da sve radi. Aplikaciju gradiš ti.

Zadatak: [kit/zadatak.md](kit/zadatak.md) (isto i kao [PDF](kit/zadatak.pdf)).

Podrška: ______________________________

## 1. Instaliraj alate

| Alat | Za šta | Link |
| --- | --- | --- |
| Git | verzije koda | [git-scm.com/downloads](https://git-scm.com/downloads) |
| Node.js, LTS verzija | pokretanje aplikacije | [nodejs.org/en/download](https://nodejs.org/en/download) |
| Docker Desktop | baza (PostgreSQL) | [docs.docker.com/get-started/get-docker](https://docs.docker.com/get-started/get-docker/) |
| Editor | pisanje koda | [VS Code](https://code.visualstudio.com/) ili [Cursor](https://cursor.com/) |

Na Windowsu Docker Desktop traži WSL 2. Instalacija te vodi kroz to.

Provjeri u terminalu:

```bash
git --version
node --version     # v24 ili novije
docker --version
```

## 2. Preuzmi repozitorij

Napravi svoju kopiju na GitHubu (*Use this template* ili *Fork*) i kloniraj nju:

```bash
git clone <link na tvoj repozitorij>
cd praksa-narudzbe
npm install
```

## 3. Pokreni bazu

Pokreni Docker Desktop, pa:

```bash
docker compose up -d
```

Prvi put Docker preuzme PostgreSQL i učita `data/schema.sql` i `data/seed.sql`. Provjeri sa `docker compose ps`: servis `baza` treba biti pokrenut.

## 4. Poveži aplikaciju s bazom

```bash
cp .env.example .env.local       # Windows: copy .env.example .env.local
```

## 5. Pokreni aplikaciju

```bash
npm run dev
```

Otvori <http://localhost:3000>. Treba pisati:

> Aplikacija radi.
> Baza odgovara. kupci: 60, proizvodi: 40, narudzbe: 2068, stavke_narudzbe: 10095.

Ako to vidiš, okruženje je spremno. `app/page.tsx` je samo provjera. Zamijeni je svojim radom.

## Kad nešto ne radi

| Poruka | Šta uraditi |
| --- | --- |
| `nema DATABASE_URL` | Nema `.env.local` (korak 4). Napravi ga i ponovo pokreni `npm run dev`. |
| `ECONNREFUSED ...:5432` | Baza nije pokrenuta. Pokreni Docker Desktop, pa `docker compose up -d`. |
| `port is already allocated` | Port 5432 je zauzet, možda već imaš PostgreSQL. U `docker-compose.yml` promijeni `"5432:5432"` u `"5433:5432"`, a u `.env.local` port u 5433. |
| `password authentication failed` | Uporedi `.env.local` sa `docker-compose.yml`. |
| Hoćeš početne podatke ispočetka | `docker compose down -v`, pa `docker compose up -d`. Briše sve što je uneseno. |

Ako i dalje ne radi, javi se podršci. Pošalji šta je pokušano i tačnu poruku greške.

## Bez Dockera

Možeš koristiti lokalno instaliran [PostgreSQL](https://www.postgresql.org/download/) ili [Supabase](https://supabase.com/docs). Pokreni `data/schema.sql`, pa `data/seed.sql` (najlakše preko `psql`), a u `.env.local` stavi svoj connection string.

Baza se poziva samo sa servera (Server Components, Server Actions), nikad iz browsera. Ako na Supabaseu koristiš njihov API ili javni ključ, prvo uključi [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) na tabelama.

## Šta je u repozitoriju

```text
app/page.tsx           provjera okruženja (zamijeni je)
data/schema.sql        tabele
data/seed.sql          početni podaci
data/csv/              isti podaci kao CSV, za analizu i prognozu
docker-compose.yml     PostgreSQL za lokalni rad
kit/zadatak.md, .pdf   zadatak
```
