# Narudžbe: praksa

Ovdje je samo okruženje: baza s podacima i prazna Next.js aplikacija koja provjerava da li sve radi. Aplikaciju gradiš ti.

Zadatak: [kit/zadatak.md](kit/zadatak.md) (i kao [PDF](kit/zadatak.pdf)).

Podrška: ______________________________

## 1. Instaliraj alate

| Alat | Za šta | Link |
| --- | --- | --- |
| Git | verzije koda | [git-scm.com/downloads](https://git-scm.com/downloads) |
| Node.js, LTS verzija | pokretanje aplikacije | [nodejs.org/en/download](https://nodejs.org/en/download) |
| Docker Desktop | baza (PostgreSQL) | [docs.docker.com/get-started/get-docker](https://docs.docker.com/get-started/get-docker/) |
| Editor | pisanje koda | [VS Code](https://code.visualstudio.com/) ili [Cursor](https://cursor.com/) |
| GitHub nalog | tvoj repozitorij | [github.com/signup](https://github.com/signup) |

Na Windowsu Docker Desktop traži WSL 2. Instalacija te vodi kroz to. Ako PowerShell javi `running scripts is disabled`, pokreni `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ili koristi Command Prompt.

Provjeri u terminalu:

```bash
git --version
node --version     # v24 ili novija
docker --version
```

## 2. Preuzmi repozitorij

Napravi svoju kopiju na GitHubu (*Use this template* ili *Fork*), pa je kloniraj:

```bash
git clone <link na tvoj repozitorij>
cd <ime tvog repozitorija>
npm install
```

## 3. Pokreni bazu

Pokreni Docker Desktop, pa:

```bash
docker compose up -d --wait
```

Prvi put Docker preuzme PostgreSQL i učita `data/schema.sql` i `data/seed.sql`. Naredba završi kad je baza spremna. Provjeri: `docker compose ps`. U koloni STATUS za `baza` treba pisati `(healthy)`.

SQL nad bazom pokrećeš iz terminala:

```bash
docker compose exec baza psql -U praksa -d narudzbe
```

Upiši npr. `select count(*) from narudzbe;`. Izlaz: `\q`. Više u dokumentaciji za [psql](https://www.postgresql.org/docs/current/app-psql.html). Može i iz editora (npr. ekstenzija za PostgreSQL).

## 4. Poveži aplikaciju s bazom

```bash
cp .env.example .env.local       # Windows: copy .env.example .env.local
```

## 5. Pokreni aplikaciju

```bash
npm run dev
```

Otvori <http://localhost:3000>. Vidjet ćeš:

> Aplikacija radi.
> Baza odgovara: kupci 60, proizvodi 40, narudzbe 2068, stavke_narudzbe 10095.

Ako to vidiš, okruženje je spremno. `app/page.tsx` je samo provjera. Zamijeni je svojim radom.

## Kad nešto ne radi

| Poruka | Šta uraditi |
| --- | --- |
| `nema DATABASE_URL` | Nema `.env.local` (korak 4). Napravi ga i ponovo pokreni `npm run dev`. |
| `ECONNREFUSED ...:5432` | Baza nije pokrenuta. Pokreni Docker Desktop, pa `docker compose up -d --wait`. |
| `port is already allocated`, `address already in use` ili `role "praksa" does not exist` | Port 5432 je zauzet, vjerovatno već imaš PostgreSQL. U `docker-compose.yml` promijeni `"127.0.0.1:5432:5432"` u `"127.0.0.1:5433:5432"`, a u `.env.local` `:5432` u `:5433`. |
| `relation "kupci" does not exist` ili `the database system is starting up` | Baza se još puni ili je ostao stari volume. Sačekaj pa osvježi. Ako ostane, `docker compose down -v`, pa `docker compose up -d --wait`. |
| `password authentication failed` | Korisnik i lozinka u `.env.local` moraju biti isti kao u `docker-compose.yml`. |
| Vraćanje početnih podataka | `docker compose down -v`, pa `docker compose up -d --wait`. Briše sve unesene podatke. |

Ako i dalje ne radi, pošalji podršci tačnu poruku greške i šta nije pomoglo.

## Bez Dockera

Možeš koristiti lokalno instaliran [PostgreSQL](https://www.postgresql.org/download/) ili [Supabase](https://supabase.com/docs). Pokreni `data/schema.sql`, pa `data/seed.sql` (najlakše preko `psql`), a u `.env.local` stavi svoj connection string.

Bazi se pristupa samo sa servera (Server Components, Server Actions), nikad iz browsera. Na Supabaseu uzmi connection string za *Session pooler* i uključi [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) na svim tabelama.

## Šta je u repozitoriju

```text
app/page.tsx           provjera okruženja (zamijeni je)
data/schema.sql        tabele
data/seed.sql          početni podaci
data/csv/              isti podaci kao CSV, za analizu i prognozu
docker-compose.yml     PostgreSQL za lokalni rad
kit/zadatak.md, .pdf   zadatak
```
