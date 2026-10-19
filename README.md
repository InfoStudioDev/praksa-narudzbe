# Narudžbe: praksa

Ovdje je samo okruženje: podaci za bazu i prazna Next.js aplikacija koja provjerava da li sve radi. Aplikaciju gradiš ti.

Zadatak: [kit/zadatak.md](kit/zadatak.md).

Podrška: ______________________________

## 1. Instaliraj alate

| Alat | Za šta | Link |
| --- | --- | --- |
| Git | verzije koda | [git-scm.com/downloads](https://git-scm.com/downloads) |
| Node.js, LTS verzija | pokretanje aplikacije | [nodejs.org/en/download](https://nodejs.org/en/download) |
| Editor | pisanje koda | [VS Code](https://code.visualstudio.com/) ili [Cursor](https://cursor.com/) |
| GitHub nalog | tvoj repozitorij | [github.com/signup](https://github.com/signup) |

Terminal: na macOS-u *Terminal*, na Windowsu *PowerShell*, ili [terminal u VS Code-u](https://code.visualstudio.com/docs/terminal/getting-started). Na macOS-u `git --version` prvi put ponudi instalaciju alata; prihvati.

Provjeri u terminalu:

```bash
git --version
node --version     # v24 ili novija
```

Na Windowsu: ako PowerShell javi `running scripts is disabled`, pokreni `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ili koristi Command Prompt.

## 2. Preuzmi repozitorij

Napravi svoju kopiju na GitHubu (*Use this template* ili *Fork*), pa je kloniraj:

```bash
git clone <link na tvoj repozitorij>
cd <ime tvog repozitorija>
npm install
```

## 3. Napravi bazu

Baza je PostgreSQL na [Neonu](https://neon.com), besplatni plan, bez instalacije.

1. Napravi nalog na Neonu i novi projekat (region u Evropi, npr. Frankfurt).
2. U konzoli klikni **Connect**, isključi **Connection pooling** (host bez `-pooler`) i kopiraj connection string ([uputstvo](https://neon.com/docs/connect/connect-from-any-app)).
3. Napravi `.env.local`:

   ```bash
   cp .env.example .env.local       # Windows: copy .env.example .env.local
   ```

4. U `.env.local` zamijeni vrijednost `DATABASE_URL` svojim stringom. Na kraju stringa neka bude `?sslmode=verify-full` (Neon daje `?sslmode=require&channel_binding=require`; zamijeni to).

## 4. Napuni bazu

```bash
npm run baza
```

Skripta napravi tabele iz `data/schema.sql` i učita `data/seed.sql`. Na kraju piše `Baza je spremna.`

SQL nad bazom pokrećeš u Neon konzoli: **SQL Editor** ([uputstvo](https://neon.com/docs/get-started/query-with-neon-sql-editor)).

## 5. Pokreni aplikaciju

```bash
npm run dev
```

Otvori <http://localhost:3000>. Vidjet ćeš:

> Aplikacija radi.
>
> Baza odgovara: kupci 60, proizvodi 40, narudzbe 2068, stavke_narudzbe 10095.

Ako to vidiš, okruženje je spremno. `app/page.tsx` je samo provjera. Zamijeni je svojim radom.

## Kad nešto ne radi

| Poruka | Šta uraditi |
| --- | --- |
| `nema DATABASE_URL` | Nema `.env.local` (korak 3). Napravi ga i ponovo pokreni naredbu. |
| `password authentication failed` ili `getaddrinfo ENOTFOUND` | Connection string nije tačno prepisan. Kopiraj ga ponovo iz Neona. Provjeri i internet. |
| `relation "kupci" does not exist` | Baza je prazna. Pokreni `npm run baza`. |
| `Tabele postoje, ali su prazne` ili brojevi su 0 | Učitavanje je prekinuto. Pokreni `npm run baza -- --ispocetka`. |
| `timeout expired` | Mreža možda blokira port 5432. Probaj s druge mreže, npr. hotspot s mobitela. |
| `SECURITY WARNING: The SSL modes 'prefer', 'require'...` | U `.env.local` zamijeni `sslmode=require` sa `sslmode=verify-full`. |
| Prvi upit nakon pauze traje duže | Neon uspava bazu nakon par minuta bez rada. Normalno je. |
| Vraćanje početnih podataka | `npm run baza -- --ispocetka`. Briše tabele iz šeme i unesene podatke. |

Ako i dalje ne radi, pošalji podršci tačnu poruku greške i šta nije pomoglo.

Connection string je lozinka. Ne ide u git, u browser ni u poruke. Bazi se pristupa samo sa servera (Server Components, Server Actions).

## Šta je u repozitoriju

```text
app/page.tsx           provjera okruženja (zamijeni je)
data/schema.sql        tabele
data/seed.sql          početni podaci
data/csv/              isti podaci kao CSV, za analizu i prognozu
scripts/baza.mjs       puni bazu (npm run baza)
kit/zadatak.md         zadatak
```
