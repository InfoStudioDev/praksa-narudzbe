# Praksa: aplikacija za narudžbe

Praviš aplikaciju za narudžbe za klijenta Bistra d.o.o. Pripremljeno je samo okruženje, ostalo gradiš sam. Gledamo kod i kako objašnjavaš odluke.

Kako radiš:

1. Postavi okruženje (poglavlje 4).
2. Prođi kontrolnu listu (poglavlje 7) redom, red po red. Svaki red je jedan mali zadatak s rezultatom koji se vidi.
3. Kad red radi, označi ga, commitaj i pushaj, pa pređi na sljedeći.
4. Kad završiš grupu redova (npr. *Korak 1: unos*), pošalji mentoru link na zadnji commit i sliku ekrana. Dok čekaš odgovor, radi dalje.

**Korak 1 je cijeli zadatak.** Koraci 2 i 3 su bonus.

## 1. Pozadina: zašto i za koga

Bistra d.o.o. je izmišljena firma: distributer pića, kafe i grickalica sa šezdesetak kupaca (kafići, restorani, prodavnice, hoteli i firme).

Danas narudžbe stižu telefonom, porukom i mailom. Komercijalista ih prepisuje u Excel, a skladište dobije odštampanu listu. Zato:

- ima grešaka u količinama i cijenama, i niko ne zna koja je verzija tačna;
- kad kupac pita gdje mu je roba, odgovor traže tri osobe;
- vlasnik ne vidi koji kupci i proizvodi donose novac, ni šta je u padu;
- nabavka nagađa: ljeti nestane vode, zimi višak stoji u skladištu.

Bistra traži jedno mjesto za narudžbe, pregled poslovanja i prognozu potražnje za nabavku.

| Ko koristi | Šta radi |
| --- | --- |
| Komercijalista | unosi i ispravlja narudžbe |
| Skladište | priprema robu i mijenja status |
| Vlasnik | prati poslovanje |
| Nabavka | gleda prognozu i planira narudžbe kod dobavljača |

## 2. Šta se očekuje: tri koraka

| Korak | Šta praviš | Za koga |
| --- | --- | --- |
| 1. Narudžbe (CRUD) | lista, detalji, unos, izmjena, brisanje i status narudžbi | komercijalista, skladište |
| 2. Analitika | grafici i nalazi o poslovanju | vlasnik |
| 3. Inteligencija | prognoza potražnje i asistent koji odgovara iz podataka | nabavka, vlasnik |

Tačni zadaci su u kontrolnoj listi (poglavlje 7). Ovdje su pravila i pozadina.

### Korak 1: narudžbe (CRUD)

Pravila unosa provjerava server, ne samo forma. Neispravan unos ne smije završiti u bazi ni kad isključiš provjeru u formi.

- Kupac je obavezan i narudžba ima bar jednu stavku.
- Broj narudžbe se dodjeljuje sam, u formatu iz podataka (`N-2025-00001`: godina i redni broj), i jedinstven je.
- Proizvod je obavezan i aktivan. Isti proizvod je samo jednom u narudžbi.
- Količina je cijeli broj veći od nule, cijena nula ili veća, rabat od 0 do 100.
- Izmjena i brisanje su dozvoljeni samo dok je narudžba `KREIRANA`. Status se mijenja po tabeli iz poglavlja 5.

### Korak 2: analitika (bonus)

Vlasnik hoće pregled poslovanja: stranicu s graficima nad bazom i kratak pisani izvještaj. Upite piši u SQL-u i drži ih u repozitoriju. Pitanja:

- Kako se kreće promet po mjesecima? Ima li sezone i rasta?
- Koji kupci i proizvodi donose najviše? Ko je prestao naručivati?
- Kako se vrste kupaca i kategorije razlikuju kroz godinu?
- Šta se desilo s cijenama i kako je to uticalo na promet?
- Koje narudžbe stoje u `U_OBRADI` ili `POSLATA` više od 7 dana od datuma narudžbe? Isporuka traje do 3 radna dana.

### Korak 3: inteligencija (bonus)

**Prognoza.** Nabavka pita koliko čega naručiti za osam sedmica nakon zadnjeg datuma u podacima. Model: [Chronos-2](https://github.com/amazon-science/chronos-forecasting) (alternative: [TimesFM](https://github.com/google-research/timesfm), [statsforecast](https://nixtlaverse.nixtla.io/statsforecast/docs/getting-started/getting_started_short.html)). Ovaj dio može biti u Pythonu, s [pandas](https://pandas.pydata.org/docs/getting_started/index.html) i [Jupyterom](https://jupyter.org/install). Rezultat ide u bazu ili CSV koji aplikacija čita.

**Asistent.** Korisnik pita, npr. „Koji kafići u Mostaru su najviše naručivali ljeti?“, a asistent odgovara iz podataka. Koristi [Vercel AI SDK](https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling) i model lokalno preko [Ollame](https://ai-sdk.dev/providers/community-providers/ollama), s [modelom koji podržava alate](https://ollama.com/search?c=tools). Alternative s API ključem: [Anthropic API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), [OpenAI API](https://developers.openai.com/api/docs/guides/function-calling). Ključ ide u `.env.local`, nikad u kod. Asistent ne piše proizvoljan SQL: dobija tri do pet alata samo za čitanje (tool calling).

## 3. Tehnologije

### Glavni dijelovi

Aplikacija ima tri dijela: frontend u browseru (React i MUI), backend na serveru (Node.js, TypeScript i Hono) i bazu (PostgreSQL). Frontend šalje zahtjeve na `/api/...`, a backend čita i piše u bazu i vraća JSON.

| Dio | Uloga u aplikaciji | Počni ovdje | Ako ništa drugo, uradi ovo |
| --- | --- | --- | --- |
| React | ekrani i forme | [Quick Start](https://react.dev/learn), [Thinking in React](https://react.dev/learn/thinking-in-react), [State](https://react.dev/learn/state-a-components-memory) | [Quick Start](https://react.dev/learn) i [Tutorial: Tic-Tac-Toe](https://react.dev/learn/tutorial-tic-tac-toe) |
| MUI | gotove komponente: dugmad, forme, tabela, grafici | [Installation](https://mui.com/material-ui/getting-started/installation/), [Usage](https://mui.com/material-ui/getting-started/usage/), [Templates](https://mui.com/material-ui/getting-started/templates/), [Data Grid](https://mui.com/x/react-data-grid/quickstart/), [Charts](https://mui.com/x/react-charts/quickstart/) | instaliraj MUI i Data Grid i prikaži tri ručno upisane narudžbe u tabeli |
| Node.js, TypeScript i Hono | backend: rute `/api/...`, validacija, SQL | [TS for JS Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html), [Hono na Node.js-u](https://hono.dev/docs/getting-started/nodejs), [Hono validacija](https://hono.dev/docs/guides/validation) | dodaj u `server/index.ts` rutu `GET /api/kupci` koja vraća prvih deset kupaca iz baze kao JSON |
| PostgreSQL i SQL | podaci; upite pišeš sam | [Tutorial 2.4–2.7](https://www.postgresql.org/docs/current/tutorial-sql.html), [Joins](https://www.postgresql.org/docs/current/tutorial-join.html), [Foreign Keys](https://www.postgresql.org/docs/current/tutorial-fk.html) | [SQLBolt](https://sqlbolt.com/) (interaktivne lekcije u browseru), pa [PostgreSQL Exercises](https://pgexercises.com/) |

React pretpostavlja JavaScript. Ako ti treba, MDN: [Functions](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Functions), [Arrays](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Arrays), [Objects](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Object_basics), [Promises i async/await](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS/Promises). Za Git: Pro Git [Recording Changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository) i GitHub [Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world).

### Šta koristimo i alternative

Ako izabereš alternativu, na prezentaciji objasni zašto.

| Područje | Koristimo | Alternative |
| --- | --- | --- |
| UI komponente | [MUI](https://mui.com/material-ui/getting-started/installation/) (Material UI) | [Mantine](https://mantine.dev/getting-started/), [shadcn/ui](https://ui.shadcn.com/docs) |
| Tabela | [MUI X Data Grid](https://mui.com/x/react-data-grid/quickstart/), besplatni paket `@mui/x-data-grid` | [AG Grid](https://www.ag-grid.com/react-data-grid/getting-started/), [TanStack Table](https://tanstack.com/table/latest/docs/overview) |
| Grafici | [MUI X Charts](https://mui.com/x/react-charts/quickstart/) | [Recharts](https://recharts.github.io/en-US/guide/getting-started/), [Apache ECharts](https://echarts.apache.org/handbook/en/get-started/) |
| Forme i validacija | [React Hook Form](https://react-hook-form.com/get-started) + [Zod](https://zod.dev/), isti Zod i na serveru | [TanStack Form](https://tanstack.com/form/latest/docs/overview), [Valibot](https://valibot.dev/guides/introduction/) |
| Frontend | [React](https://react.dev/) + [Vite](https://vite.dev/guide/) | — |
| Backend | [Hono](https://hono.dev/docs/) na Node.js-u, TypeScript | [Express](https://expressjs.com/en/starter/installing.html), [Fastify](https://fastify.dev/docs/latest/Guides/Getting-Started/) |
| Baza | [PostgreSQL](https://www.postgresql.org/docs/current/): Neon, lokalni ili PGlite (poglavlje 4) | — |
| Pristup bazi | SQL s [node-postgres](https://node-postgres.com/) ili [Drizzle](https://orm.drizzle.team/docs/overview) | [Kysely](https://kysely.dev/docs/intro), [Prisma](https://www.prisma.io/docs) |
| Testovi | [Vitest](https://vitest.dev/guide/), [Playwright](https://playwright.dev/docs/intro) | [Jest](https://jestjs.io/docs/getting-started), [Cypress](https://docs.cypress.io/app/get-started/why-cypress) |

Firma koristi i Express, TypeORM, Oracle, Keycloak, nginx i Turborepo. Za ovaj zadatak nisu potrebni.

## 4. Postavljanje

1. Instaliraj [Git](https://git-scm.com/downloads), [Node.js](https://nodejs.org/en/download) (LTS, v24 ili novija) i [VS Code](https://code.visualstudio.com/). Komande pokrećeš u [terminalu u VS Code-u](https://code.visualstudio.com/docs/terminal/getting-started). Git prije prvog commita traži ime i email ([uputstvo](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)):

   ```bash
   git config --global user.name "Ime Prezime"
   git config --global user.email "adresa@primjer.ba"
   ```

2. Napravi [GitHub nalog](https://github.com/signup). Na stranici ovog repozitorija klikni **Use this template** → **Create a new repository** ([uputstvo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)). Repozitorij može biti javni ili privatni, s mentorom dodanim kao saradnikom ([uputstvo](https://docs.github.com/en/account-and-profile/how-tos/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository)). Za push, i za kloniranje privatnog repozitorija, GitHub traži prijavu: u VS Code-u **Sign in with GitHub** ([uputstvo](https://code.visualstudio.com/docs/sourcecontrol/github)). Preuzmi repozitorij i instaliraj pakete:

   ```bash
   git clone https://github.com/<tvoj-nalog>/<ime-repozitorija>.git
   cd <ime-repozitorija>
   npm install
   ```

3. Napravi bazu. Aplikacija i `npm run baza` rade s bilo kojom opcijom iz tabele; razlikuje se samo connection string. Najjednostavniji je Neon: nema instalacije, a SQL pokrećeš u browseru.

   | Opcija | Connection string | SQL pokrećeš u |
   | --- | --- | --- |
   | [Neon](https://neon.com/docs/connect/connect-from-any-app), besplatno u oblaku (preporuka) | Nalog, projekat u Evropi. **Connect**, isključi **Connection pooling**, kopiraj string tačno kako ga Neon daje. | SQL Editoru u konzoli |
   | [Lokalni PostgreSQL](https://www.postgresql.org/download/), instalacija na računar | `postgresql://postgres:LOZINKA@127.0.0.1:5432/postgres`, s korisnikom i lozinkom iz instalacije | pgAdminu ili psql-u |
   | [PGlite](https://pglite.dev/docs/pglite-socket), PostgreSQL u memoriji, bez naloga | U drugom terminalu pokreni `npx -y -p @electric-sql/pglite-socket@0.2.13 pglite-server -m 10` i ostavi ga upaljen. String: `postgresql://postgres:postgres@127.0.0.1:5432/postgres`. Kad ga ugasiš, podaci nestanu, pa opet `npm run baza`. | psql-u ili drugom PostgreSQL klijentu, koji instaliraš posebno |

4. Kopiraj `.env.example` u `.env.local` (`cp .env.example .env.local`). U `.env.local` upiši svoj string kao `DATABASE_URL`.
5. Napuni bazu i pokreni aplikaciju:

   ```bash
   npm run baza     # tabele i početni podaci; svako pokretanje briše sve i učitava ispočetka
   npm run dev      # backend [api] na portu 3000 i frontend [web] na portu 5173
   ```

   `npm run baza` ispiše „Baza je spremna.“ Na <http://localhost:5173> treba pisati „Aplikacija radi.“ i „Baza odgovara: kupci 60, proizvodi 40, narudzbe 2068, stavke_narudzbe 10095.“ `src/App.tsx` (frontend) i `server/index.ts` (backend) su samo ta provjera; zamijeni ih svojim radom.

**Česti problemi**

| Poruka | Šta uraditi |
| --- | --- |
| `.env.local not found` ili `nema DATABASE_URL` | Nema `.env.local` (korak 4). Poslije izmjene `.env.local` zaustavi i ponovo pokreni `npm run dev`. |
| `relation "kupci" does not exist` | Pokreni `npm run baza`. |
| `ECONNREFUSED` | Lokalna baza ili PGlite nije pokrenut. |
| `Backend ne odgovara` | Backend se nije pokrenuo. Pogledaj redove `[api]` u terminalu. |

- `npm run dev` i PGlite rade dok ih ne zaustaviš: **Ctrl+C** u terminalu.
- Uz Neonov string `npm run baza` i `npm run dev` ispišu `SECURITY WARNING` o SSL modu. To je samo upozorenje drajvera; sve radi.

## 5. Podaci

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

Tok narudžbe:

| Status | Može preći u | Izmjena i brisanje |
| --- | --- | --- |
| `KREIRANA` | `U_OBRADI`, `OTKAZANA` | da |
| `U_OBRADI` | `POSLATA`, `OTKAZANA` | ne |
| `POSLATA` | `ISPORUCENA` | ne |
| `ISPORUCENA`, `OTKAZANA` | (kraj) | ne |

Promjenu šeme radi kao migraciju: SQL fajl u folderu `sql/` tvog repozitorija, pokrenut tamo gdje pokrećeš SQL (poglavlje 4, korak 3). `npm run baza` vraća originalnu šemu, pa migracije nakon toga pokreni ponovo.

## 6. Pomoć

- Pitanja o tome šta zadatak znači postavi mentoru, bilo kad.
- Za tehnički problem prvo pročitaj grešku i dokumentaciju, pa pretraži. Kad si probao bar dvije stvari i obje upisao pod *Probano*, pošalji podršci poruku u četiri reda:

  ```text
  Radim: …
  Greška: … (tačan tekst ili slika ekrana)
  Probano: …
  Očekujem: …
  ```

- Prije pitanja podršci commitaj i pushaj, da se vidi tvoj kod.
- AI koristi slobodno. Ne predaj kod koji ne razumiješ. Ako koristiš AI, na prezentaciji objašnjavaš i dio koda koji je on napisao.

Podrška: ______________________________

## 7. Kontrolna lista

Radi redom. Kad red radi, označi kolonu *Ti*. Kolonu *Mentor* popunjava mentor na prezentaciji. Prezentacija je uživo ili preko video poziva: aplikaciju pokrećeš na svom računaru i dijeliš ekran. Slajdovi nisu obavezni.

| Pokretanje | Ti | Mentor |
| --- | :---: | :---: |
| 1. `npm run baza` ispiše „Baza je spremna.“ | ☐ | ☐ |
| 2. Na <http://localhost:5173> piše „Baza odgovara: kupci 60, proizvodi 40, narudzbe 2068, stavke_narudzbe 10095.“ | ☐ | ☐ |
| 3. `sql/prvi-upit.sql` vraća deset kupaca s najvećim prometom u zadnjoj godini podataka (naziv, broj narudžbi, promet po pravilima iz poglavlja 5) i pushan je na GitHub | ☐ | ☐ |

| Korak 1: lista i detalji | Ti | Mentor |
| --- | :---: | :---: |
| 4. `GET /api/narudzbe` vraća narudžbe kao JSON: broj, kupac, datum, status, broj stavki, iznos | ☐ | ☐ |
| 5. Lista narudžbi u MUI X Data Gridu prikazuje te kolone | ☐ | ☐ |
| 6. Klik na naslov kolone sortira listu | ☐ | ☐ |
| 7. Filter po statusu prikazuje samo narudžbe tog statusa | ☐ | ☐ |
| 8. Klik na narudžbu otvara detalje: stavke (proizvod, količina, cijena po komadu, rabat, iznos) i ukupan iznos | ☐ | ☐ |

| Korak 1: unos | Ti | Mentor |
| --- | :---: | :---: |
| 9. Forma za novu narudžbu ima kupca, datum i stavke; stavka se može dodati i ukloniti | ☐ | ☐ |
| 10. Kad izabereš proizvod, cijena po komadu se popuni iz cjenovnika; neaktivni proizvodi se ne nude | ☐ | ☐ |
| 11. Sačuvana narudžba dobije novi broj i vidi se u listi i nakon osvježavanja stranice | ☐ | ☐ |
| 12. Server odbija narudžbu bez kupca; poruka kaže koje polje nije ispravno i zašto | ☐ | ☐ |
| 13. Server odbija narudžbu bez stavki, s istom vrstom poruke | ☐ | ☐ |
| 14. Server odbija količinu 0 i količinu koja nije cijeli broj | ☐ | ☐ |
| 15. Server odbija negativnu cijenu i rabat izvan 0–100 | ☐ | ☐ |
| 16. Server odbija isti proizvod dvaput u narudžbi i neaktivan proizvod | ☐ | ☐ |
| 17. Redovi 12–16 rade i kad zahtjev pošalješ direktno na `/api`, bez forme | ☐ | ☐ |

| Korak 1: izmjena, brisanje, status | Ti | Mentor |
| --- | :---: | :---: |
| 18. U narudžbi `KREIRANA` promijeniš količinu stavke; nova količina i novi iznos ostaju i nakon osvježavanja | ☐ | ☐ |
| 19. U narudžbi `KREIRANA` dodaš i obrišeš stavku | ☐ | ☐ |
| 20. Narudžbu `KREIRANA` obrišeš | ☐ | ☐ |
| 21. Server odbija izmjenu i brisanje narudžbe koja nije `KREIRANA` | ☐ | ☐ |
| 22. Status se mijenja po tabeli iz poglavlja 5 | ☐ | ☐ |
| 23. Server odbija prelaz koji tabela ne dozvoljava, npr. `ISPORUCENA` → `KREIRANA` | ☐ | ☐ |

| Korak 1: novo polje i predaja | Ti | Mentor |
| --- | :---: | :---: |
| 24. Migracija u `sql/` dodaje u `narudzbe` kolonu `nacin_placanja` (gotovina, kartica, virman) | ☐ | ☐ |
| 25. Način plaćanja se bira u formi, sačuva u bazi i prikaže u listi | ☐ | ☐ |
| 26. Znaš pokazati put jednog zahtjeva od forme do baze i nazad | ☐ | ☐ |
| 27. README tvog repozitorija kaže kako pokrenuti aplikaciju i šta još ne radi | ☐ | ☐ |
| 28. Repozitorij kloniran u novi prazan folder pokreće se po tom README-u | ☐ | ☐ |
| 29. U repozitoriju nema lozinki ni API ključeva | ☐ | ☐ |

| Korak 2: analitika (bonus) | Ti | Mentor |
| --- | :---: | :---: |
| 30. Grafik prometa po mjesecima ([MUI X Charts](https://mui.com/x/react-charts/quickstart/)) | ☐ | ☐ |
| 31. Top deset kupaca i top deset proizvoda po prometu | ☐ | ☐ |
| 32. Grafik prometa po vrsti kupca i po kategoriji, po mjesecima | ☐ | ☐ |
| 33. Lista narudžbi koje stoje u `U_OBRADI` ili `POSLATA` više od 7 dana od datuma narudžbe | ☐ | ☐ |
| 34. `ANALIZA.md` ima tri do pet nalaza; svaki ima broj iz podataka i jednu rečenicu preporuke za Bistru; jedan nalaz je o cijenama | ☐ | ☐ |

| Korak 3: inteligencija (bonus) | Ti | Mentor |
| --- | :---: | :---: |
| 35. Sedmične količine po kategoriji, samo iz početnih podataka | ☐ | ☐ |
| 36. Osnova (ista sedmica prošle godine) i model prognoziraju sakrivenih zadnjih 12 sedmica; greška (MAE) izmjerena za oba | ☐ | ☐ |
| 37. Aplikacija prikazuje stvarne vrijednosti, prognozu za sakrivenih 12 sedmica i prognozu za narednih osam | ☐ | ☐ |
| 38. Znaš objasniti zašto je greška jednog od njih manja | ☐ | ☐ |
| 39. Asistent ima tri do pet alata samo za čitanje, npr. promet po kupcu, top proizvodi, prognoza | ☐ | ☐ |
| 40. Asistent odgovara iz podataka i vidi se koje je alate pozvao | ☐ | ☐ |
| 41. Pokažeš dva pitanja na koja asistent griješi i objasniš zašto | ☐ | ☐ |

| Prezentacija | Ti | Mentor |
| --- | :---: | :---: |
| 42. Glavni tok pokazan uživo | ☐ | ☐ |
| 43. Objašnjen dio koda koji je napisao AI (ako si koristio AI) | ☐ | ☐ |
| 44. Objašnjena jedna odluka i alternativa koja nije izabrana | ☐ | ☐ |
| 45. Pokazan jedan problem: kako je nađen i riješen | ☐ | ☐ |
| 46. Rečeno šta bi bilo sljedeće | ☐ | ☐ |

| Dodatni bonus | Ti | Mentor |
| --- | :---: | :---: |
| 47. Testovi: Vitest za pravila unosa, Playwright za unos narudžbe od početka do kraja | ☐ | ☐ |
| 48. Skica arhitekture u README-u (šta radi browser, šta server, šta baza) ili kratak video ili GIF glavnog toka | ☐ | ☐ |
| 49. CI: GitHub Actions pokreće build i testove na svaki push | ☐ | ☐ |
