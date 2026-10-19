# Praksa: aplikacija za narudžbe

Praviš aplikaciju za narudžbe za klijenta Bistra d.o.o. Pripremljeno je samo okruženje, ostalo gradiš sam. Gledamo kod i kako objašnjavaš odluke.

**Faza A je cijeli zadatak.** Faze B i C su bonus.

## Redoslijed

Postavljanje → Korak 0 → A1 → A2 → bonus iz kontrolne liste, ako želiš → predaja i prezentacija.

Poslije svakog koraka pushaj i pošalji mentoru link na commit i sliku ekrana (za postavljanje samo sliku). Dok čekaš odgovor, radi dalje.

## Pomoć

- Pitanja o tome šta zadatak znači postavi mentoru, bilo kad.
- Za tehnički problem prvo pročitaj grešku i dokumentaciju, pa pretraži. Kad si probao bar dvije stvari i obje upisao pod *Probano*, pošalji podršci poruku u četiri reda:

  ```text
  Radim: …
  Greška: … (tačan tekst ili slika ekrana)
  Probano: …
  Očekujem: …
  ```

- AI koristi slobodno. Ne predaj kod koji ne razumiješ. Ako koristiš AI, na prezentaciji objašnjavaš i dio koda koji je on napisao.
- Commitaj kad nešto proradi (lista, unos, validacija…) i prije svakog pitanja podršci, pa pushaj na GitHub.

Podrška: ______________________________

## Postavljanje

1. Instaliraj [Git](https://git-scm.com/downloads), [Node.js](https://nodejs.org/en/download) (LTS, v24 ili novija) i editor, npr. [VS Code](https://code.visualstudio.com/). Terminal: na macOS-u *Terminal*, na Windowsu *PowerShell*, ili [terminal u VS Code-u](https://code.visualstudio.com/docs/terminal/getting-started). Git prije prvog commita traži ime i email ([uputstvo](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)):

   ```bash
   git config --global user.name "Ime Prezime"
   git config --global user.email "adresa@primjer.ba"
   ```

2. Napravi [GitHub nalog](https://github.com/signup). Na stranici ovog repozitorija klikni **Use this template** → **Create a new repository** ([uputstvo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)). Repozitorij može biti javni ili privatni, s mentorom dodanim kao saradnikom ([uputstvo](https://docs.github.com/en/account-and-profile/how-tos/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository)). Za push, i za kloniranje privatnog repozitorija, GitHub traži prijavu: VS Code te sam pita da se prijaviš ([uputstvo](https://code.visualstudio.com/docs/sourcecontrol/github)), a izvan njega instaliraj [GitHub CLI](https://cli.github.com/) i pokreni `gh auth login` ([uputstvo](https://cli.github.com/manual/gh_auth_login)). Preuzmi repozitorij na računar i instaliraj pakete:

   ```bash
   git clone https://github.com/<tvoj-nalog>/<ime-repozitorija>.git
   cd <ime-repozitorija>
   npm install
   ```

3. Napravi bazu. Treba ti PostgreSQL. Aplikacija i `npm run baza` rade s bilo kojom opcijom iz tabele; razlikuje se samo connection string. Najjednostavniji je Neon: nema instalacije, a SQL pokrećeš u browseru.

   | Opcija | Connection string | SQL pokrećeš u |
   | --- | --- | --- |
   | [Neon](https://neon.com/docs/connect/connect-from-any-app), besplatno u oblaku (preporuka) | Nalog, projekat u Evropi. **Connect**, isključi **Connection pooling**, kopiraj string. Na kraju stavi `?sslmode=verify-full` umjesto onoga što Neon daje. | SQL Editoru u konzoli |
   | [Supabase](https://supabase.com/docs/guides/database/connecting-to-postgres), besplatno u oblaku | Nalog, projekat u Evropi. **Connect** → **Session pooler**, kopiraj string i upiši lozinku baze. Na kraju dodaj `?sslmode=no-verify`. | SQL Editoru u konzoli |
   | [Lokalni PostgreSQL](https://www.postgresql.org/download/), instalacija na računar | `postgresql://postgres:LOZINKA@127.0.0.1:5432/postgres`, s korisnikom i lozinkom iz instalacije | pgAdminu ili psql-u |
   | [PGlite](https://pglite.dev/docs/pglite-socket), PostgreSQL u memoriji, bez naloga | U drugom terminalu pokreni `npx -y -p @electric-sql/pglite-socket@0.2.13 pglite-server -m 10` i ostavi ga upaljen. String: `postgresql://postgres:postgres@127.0.0.1:5432/postgres`. Kad ga ugasiš, podaci nestanu, pa opet `npm run baza`. | psql-u ili drugom PostgreSQL klijentu, koji instaliraš posebno |

4. Kopiraj `.env.example` u `.env.local` (`cp .env.example .env.local`, na Windowsu `copy`). U `.env.local` upiši svoj string kao `DATABASE_URL`.
5. Napuni bazu i pokreni aplikaciju:

   ```bash
   npm run baza     # tabele i početni podaci; svako pokretanje briše sve i učitava ispočetka
   npm run dev
   ```

   `npm run baza` ispiše „Baza je spremna.“ Na <http://localhost:3000> treba pisati „Aplikacija radi.“ i „Baza odgovara: kupci 60, proizvodi 40, narudzbe 2068, stavke_narudzbe 10095.“ `app/page.tsx` je samo ta provjera; zamijeni je svojim radom.

**Česti problemi**

| Poruka | Šta uraditi |
| --- | --- |
| `nema DATABASE_URL` | Nema `.env.local` (korak 4). |
| `relation "kupci" does not exist` | Pokreni `npm run baza`. |
| `ECONNREFUSED` | Lokalna baza ili PGlite nije pokrenut. |

- `npm install` ispiše upozorenja (`npm warn`, `vulnerabilities`). To je normalno. Problem je samo `npm error`.
- `npm run dev` i PGlite rade dok ih ne zaustaviš: **Ctrl+C** u terminalu.
- Finder na macOS-u ne prikazuje `.env.local`. Skrivene fajlove pokaže **Cmd+Shift+.**; u editoru se fajl vidi normalno.
- Lozinka sa `@`, `#`, `/` ili `?` kvari connection string. Postavi lozinku od slova i brojeva.

## Korak 0: osnove

Ako ove alate koristiš prvi put, prođi ova poglavlja. Linkovi za faze B i C su kod tih faza.

| Tema | Poglavlja | Možeš dalje kad znaš |
| --- | --- | --- |
| HTML i CSS | MDN: [HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website/Creating_the_content), [CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website/Styling_the_content) | napraviti stranicu s formom |
| JavaScript | MDN: [Functions](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Functions), [Arrays](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Arrays), [Objects](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Object_basics), [Promises i async/await](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS/Promises) | napisati funkciju koja filtrira i sabira niz objekata; objasniti šta radi `await` |
| TypeScript | [TS for JS Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html), [Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) | dodati tipove funkciji i objektu |
| React | [Quick Start](https://react.dev/learn), [Thinking in React](https://react.dev/learn/thinking-in-react), [State](https://react.dev/learn/state-a-components-memory) | napraviti komponentu s formom i stanjem |
| Next.js | Learn: [Getting Started](https://nextjs.org/learn/dashboard-app/getting-started), [Fetching Data](https://nextjs.org/learn/dashboard-app/fetching-data), [Mutating Data](https://nextjs.org/learn/dashboard-app/mutating-data), [Improving Accessibility](https://nextjs.org/learn/dashboard-app/improving-accessibility) | pročitati podatke iz baze i sačuvati formu na serveru |
| SQL | PostgreSQL: [poglavlje 2.4–2.7](https://www.postgresql.org/docs/current/tutorial-sql.html), [Joins](https://www.postgresql.org/docs/current/tutorial-join.html), [Foreign Keys](https://www.postgresql.org/docs/current/tutorial-fk.html) | napisati `SELECT` s `JOIN` i `GROUP BY` |
| Git | Pro Git: [Recording Changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository), [Branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell); GitHub: [Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world) | napraviti branch, commit i push |

Next.js kurs radi u posebnom folderu, ne u ovom repozitoriju: ima svoj starter i svoju bazu.

Provjera: napiši upit koji vraća deset kupaca s najvećim prometom u zadnjoj godini podataka (naziv, broj narudžbi, promet; promet računaj po pravilima iz poglavlja 2). Pokreni ga nad svojom bazom, sačuvaj kao `sql/korak0.sql` u repozitoriju, pa commitaj i pushaj. To je tvoj prvi push.

## 1. Klijent

Bistra d.o.o. je izmišljena firma: distributer pića, kafe i grickalica sa šezdesetak kupaca (kafići, restorani, prodavnice, hoteli i firme).

Danas narudžbe stižu telefonom, porukom i mailom. Komercijalista ih prepisuje u Excel, a skladište dobije odštampanu listu. Zato:

- ima grešaka u količinama i cijenama, i niko ne zna koja je verzija tačna;
- kad kupac pita gdje mu je roba, odgovor traže tri osobe;
- vlasnik ne vidi koji kupci i proizvodi donose novac, ni šta je u padu;
- nabavka nagađa: ljeti nestane vode, zimi višak stoji u skladištu.

Bistra traži jedno mjesto za narudžbe (unos, pregled, status), pregled poslovanja i prognozu potražnje za nabavku.

| Ko koristi | Šta radi |
| --- | --- |
| Komercijalista | unosi i ispravlja narudžbe |
| Skladište | priprema robu i mijenja status |
| Vlasnik | prati poslovanje |
| Nabavka | gleda prognozu i planira narudžbe kod dobavljača |

Tok narudžbe:

| Status | Može preći u | Izmjena i brisanje |
| --- | --- | --- |
| `KREIRANA` | `U_OBRADI`, `OTKAZANA` | da |
| `U_OBRADI` | `POSLATA`, `OTKAZANA` | ne |
| `POSLATA` | `ISPORUCENA` | ne |
| `ISPORUCENA`, `OTKAZANA` | (kraj) | ne |

## 2. Podaci

U `data/` su šema (`schema.sql`) i podaci (`seed.sql`, isto u `csv/`). Podaci su generisani i pokrivaju dvije godine poslovanja. Zadnji datum u podacima je „danas“ za analizu i prognozu. Imena su izmišljena.

```text
kupci ─< narudzbe ─< stavke_narudzbe >─ proizvodi >─ kategorije
```

| Tabela | Šta je | Važne kolone |
| --- | --- | --- |
| `kupci` | kupci | `sifra`, `naziv`, `vrsta`, `grad` |
| `kategorije` | grupe proizvoda | `naziv` |
| `proizvodi` | cjenovnik | `sifra`, `naziv`, `kategorija_id`, `cijena`, `aktivan` |
| `narudzbe` | zaglavlje narudžbe | `broj`, `kupac_id`, `datum`, `datum_isporuke`, `status` |
| `stavke_narudzbe` | proizvodi u narudžbi | `narudzba_id`, `proizvod_id`, `kolicina`, `cijena_po_komadu`, `rabat_posto` |

Pravila:

- `proizvodi.cijena` je trenutna cijena. `stavke_narudzbe.cijena_po_komadu` je cijena u trenutku narudžbe. Nisu uvijek iste.
- Iznos stavke = `kolicina × cijena_po_komadu × (1 − rabat_posto / 100)`.
- Otkazane narudžbe ne ulaze u promet.
- Neaktivan proizvod se ne nudi u novim narudžbama, ali ostaje u starim.

Promjenu šeme radi kao migraciju: SQL fajl u svom repozitoriju, pokrenut tamo gdje pokrećeš SQL (Postavljanje, korak 3). `npm run baza` vraća originalnu šemu, pa migracije nakon toga pokreni ponovo.

## 3. Faze

### Faza A: narudžbe

**A1. Lista i unos.** Napravi:

1. listu narudžbi u MUI X Data Gridu: broj, kupac, datum, status, broj stavki, iznos; sortiranje i filter po statusu;
2. detalje narudžbe sa stavkama;
3. unos nove narudžbe: kupac, datum i jedna ili više stavki (proizvod, količina, cijena po komadu, rabat; cijena se predlaže iz cjenovnika).

Pravila unosa, u formi i na serveru:

- kupac je obavezan i narudžba ima bar jednu stavku;
- broj narudžbe (`broj`) je obavezan i jedinstven; odluči kako ga dodjeljuješ;
- proizvod je obavezan i aktivan, a isti proizvod se javlja samo jednom po narudžbi;
- količina je cijeli broj veći od nule, cijena nula ili veća, rabat od 0 do 100.

**Gotovo kad:** lista, detalji i unos rade; nova narudžba ostaje i nakon osvježavanja stranice; server odbija sva četiri neispravna unosa (bez kupca, bez stavki, s količinom 0, s negativnom cijenom) i kad isključiš provjeru u formi, s porukom koje polje nije ispravno i zašto; znaš pokazati put jednog zahtjeva od forme do baze i nazad.

**A2. Status, izmjena, novo polje.** Napravi:

1. promjenu statusa po tabeli iz poglavlja 1;
2. izmjenu i brisanje narudžbe, samo dok je `KREIRANA`;
3. jedno novo polje, npr. način plaćanja, tako da se vidi u formi, sačuva u bazi i prikaže u listi; uz to ide migracija.

**Gotovo kad:** server odbija svaki prelaz i svaku izmjenu koje tabela ne dozvoljava; novo polje radi od forme do baze, uz migraciju.

**Predaja.** Link na tvoj repozitorij. U njegovom README-u: kako pokrenuti aplikaciju i šta još ne radi.

### Faza B: analitika (bonus)

Vlasnik hoće pregled poslovanja. Napravi stranicu s tri do četiri grafika ([MUI X Charts](https://mui.com/x/react-charts/quickstart/)) i odgovori na pitanja:

- Kako se kreće promet po mjesecima? Ima li sezone i rasta?
- Koji kupci i proizvodi donose najviše? Ko je prestao naručivati?
- Kako se vrste kupaca i kategorije razlikuju kroz godinu?
- Šta se desilo s cijenama i kako je to uticalo na promet?
- Koje narudžbe stoje u `U_OBRADI` ili `POSLATA` više od 7 dana od datuma narudžbe? Isporuka traje do 3 radna dana.

Upite piši u SQL-u i drži ih u repozitoriju.

**Gotovo kad:** grafici rade nad bazom, a u `ANALIZA.md` su tri do pet nalaza. Svaki nalaz ima broj iz podataka i jednu rečenicu preporuke za Bistru.

### Faza C: prognoza i asistent (bonus)

**C1. Prognoza potražnje.** Nabavka pita koliko čega naručiti za osam sedmica nakon zadnjeg datuma u podacima.

- Napravi sedmične serije količina po proizvodu ili kategoriji, samo iz početnih podataka.
- Prvo napravi jednostavnu osnovu (baseline), npr. ista sedmica prošle godine ili prosjek zadnjih sedmica.
- Onda model: [Chronos-2](https://github.com/amazon-science/chronos-forecasting) (alternative: [TimesFM](https://github.com/google-research/timesfm), [statsforecast](https://nixtlaverse.nixtla.io/statsforecast/docs/getting-started/getting_started_short.html)). Sakrij zadnjih 12 sedmica, prognoziraj ih i izmjeri grešku (npr. MAE) za model i za osnovu.
- Ovaj dio može biti u Pythonu, s [pandas](https://pandas.pydata.org/docs/getting_started/index.html) i [Jupyterom](https://jupyter.org/install). Rezultat ide u bazu ili CSV koji aplikacija čita.

**Gotovo kad:** aplikacija prikazuje stvarne vrijednosti, prognozu za sakrivenih 12 sedmica i prognozu za narednih osam; greška modela i osnove je izmjerena i znaš objasniti zašto je jedna manja.

**C2. Asistent nad podacima.** Korisnik pita, npr. „Koji kafići u Mostaru su najviše naručivali ljeti?“ ili „Šta da naručimo za sljedeći mjesec?“, a asistent odgovara iz podataka.

- Koristi [Vercel AI SDK](https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling) i model lokalno preko [Ollame](https://ai-sdk.dev/providers/community-providers/ollama), s [modelom koji podržava alate](https://ollama.com/search?c=tools). Alternative s API ključem: [Anthropic API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), [OpenAI API](https://developers.openai.com/api/docs/guides/function-calling). Ključ ide u `.env.local`, nikad u kod.
- Asistent ne piše proizvoljan SQL. Napiši mu tri do pet alata samo za čitanje (tool calling), npr. promet po kupcu, top proizvodi, prognoza. Smije ih pozvati više zaredom.

**Gotovo kad:** asistent odgovara iz podataka preko tvojih alata; vidi se koje je alate pozvao; na prezentaciji pokažeš dva pitanja na koja griješi i objasniš zašto.

## 4. Tehnologije

Ovo koristimo za faze A i B. Ako izabereš alternativu, na prezentaciji objasni zašto.

| Područje | Koristimo | Alternative |
| --- | --- | --- |
| Framework | [Next.js](https://nextjs.org/docs/app/getting-started) (App Router) | [React Router](https://reactrouter.com/start/framework/installation), [TanStack Start](https://tanstack.com/start/latest/docs/framework/react/overview) |
| UI | [MUI](https://mui.com/material-ui/getting-started/installation/) | [Mantine](https://mantine.dev/getting-started/), [shadcn/ui](https://ui.shadcn.com/docs) |
| Tabela | [MUI X Data Grid](https://mui.com/x/react-data-grid/quickstart/), besplatni paket `@mui/x-data-grid` | [AG Grid](https://www.ag-grid.com/react-data-grid/getting-started/), [TanStack Table](https://tanstack.com/table/latest/docs/overview) |
| Grafici | [MUI X Charts](https://mui.com/x/react-charts/quickstart/) | [Recharts](https://recharts.github.io/en-US/guide/getting-started/), [Apache ECharts](https://echarts.apache.org/handbook/en/get-started/) |
| Forme i validacija | [React Hook Form](https://react-hook-form.com/get-started) + [Zod](https://zod.dev/) | [TanStack Form](https://tanstack.com/form/latest/docs/overview), [Valibot](https://valibot.dev/guides/introduction/) |
| Pisanje u bazu | [Server Actions](https://nextjs.org/docs/app/getting-started/mutating-data) | [Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers) |
| Baza | [PostgreSQL](https://www.postgresql.org/docs/current/), bilo koja opcija iz Postavljanja (korak 3), bez objašnjenja | — |
| Pristup bazi | SQL s [node-postgres](https://node-postgres.com/) ili [Drizzle](https://orm.drizzle.team/docs/overview) | [Prisma](https://www.prisma.io/docs), [Kysely](https://kysely.dev/docs/intro) |
| Testovi | [Vitest](https://vitest.dev/guide/), [Playwright](https://playwright.dev/docs/intro) | [Jest](https://jestjs.io/docs/getting-started), [Cypress](https://docs.cypress.io/app/get-started/why-cypress) |

Firma koristi i Express, TypeORM, Oracle, Keycloak, nginx i Turborepo. Za ovaj zadatak nisu potrebni.

## 5. Prezentacija i kontrolna lista

Prezentacija je uživo ili preko video poziva, s mentorom. Aplikaciju pokrećeš na svom računaru i dijeliš ekran. Slajdovi nisu obavezni. Kontrolna lista je dnevni red: idemo redom, kolonu *Ti* popunjavaš ti, kolonu *Mentor* mentor.

| Predaja | Ti | Mentor |
| --- | :---: | :---: |
| Repozitorij je dostupan mentoru; README kaže kako pokrenuti aplikaciju i šta još ne radi | ☐ | ☐ |
| Aplikacija se pokreće po tom README-u na drugom računaru ili kad repozitorij kloniraš u novi prazan folder | ☐ | ☐ |
| A1: ispunjeno sve pod *Gotovo kad* | ☐ | ☐ |
| A2: ispunjeno sve pod *Gotovo kad* | ☐ | ☐ |
| U repozitoriju nema lozinki ni API ključeva | ☐ | ☐ |

| Prezentacija | Ti | Mentor |
| --- | :---: | :---: |
| Glavni tok pokazan uživo | ☐ | ☐ |
| Objašnjen put jednog zahtjeva od forme do baze | ☐ | ☐ |
| Objašnjen dio koda koji je napisao AI (ako si koristio AI) | ☐ | ☐ |
| Objašnjena jedna odluka i alternativa koja nije izabrana | ☐ | ☐ |
| Pokazan jedan problem: kako je nađen i riješen | ☐ | ☐ |
| Rečeno šta bi bilo sljedeće | ☐ | ☐ |

| Bonus | Ti | Mentor |
| --- | :---: | :---: |
| Faza B: ispunjeno sve pod *Gotovo kad* | ☐ | ☐ |
| Faza C1: ispunjeno sve pod *Gotovo kad* | ☐ | ☐ |
| Faza C2: ispunjeno sve pod *Gotovo kad* | ☐ | ☐ |
| Testovi: Vitest za pravila unosa, Playwright za unos narudžbe od početka do kraja | ☐ | ☐ |
| Skica arhitekture u README-u (šta radi browser, šta server, šta baza) ili kratak video ili GIF glavnog toka | ☐ | ☐ |
| CI: GitHub Actions pokreće lint, build i testove na svaki push | ☐ | ☐ |
