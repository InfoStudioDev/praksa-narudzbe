# Praksa: aplikacija za narudžbe

Praviš aplikaciju za narudžbe za klijenta Bistra d.o.o. Pored koda gledamo kako istražuješ, rješavaš probleme i objašnjavaš odluke. Unaprijed je pripremljeno samo okruženje. Sve ostalo gradiš samostalno.

**Faza A je cijeli zadatak.** Kad je završiš, zadatak je gotov. Faze B i C su bonus.

## Redoslijed

| Korak | Kad završiš, pošalji podršci |
| --- | --- |
| Postavljanje | sliku ekrana: „Aplikacija radi. Baza odgovara: …“ |
| Korak 0 | upit za deset najvećih kupaca i njegov rezultat |
| A1 | link na commit i sliku liste, unosa i četiri odbijena unosa |
| A2 | link na commit i sliku promjene statusa i novog polja |
| Predaja i prezentacija | link na svoj repozitorij |
| Bonus B i C | link na commit i slike, za svaku fazu posebno |

## Pomoć

- Pitanja o tome šta zadatak znači postavi bilo kad.
- Za tehnički problem prvo pročitaj grešku i dokumentaciju, pa pretraži. Ako ne ide, pošalji poruku u četiri reda:

  ```text
  Radim: …
  Greška: … (tačan tekst ili slika ekrana)
  Probano: …
  Očekujem: …
  ```

- AI koristi slobodno. Ne predaj kod koji ne razumiješ. Na prezentaciji objašnjavaš i dio koda koji je napisao AI.
- Commitaj kad nešto proradi (lista, unos, validacija…) i prije svakog pitanja podršci, pa pushaj na GitHub.

Podrška: ______________________________

## Postavljanje

1. Instaliraj [Git](https://git-scm.com/downloads), [Node.js](https://nodejs.org/en/download) (LTS, v24 ili novija) i editor, npr. [VS Code](https://code.visualstudio.com/). Terminal: na macOS-u *Terminal*, na Windowsu *PowerShell*, ili [terminal u VS Code-u](https://code.visualstudio.com/docs/terminal/getting-started).
2. Napravi [GitHub nalog](https://github.com/signup). Na stranici ovog repozitorija klikni **Use this template** → **Create a new repository** ([uputstvo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)). Kloniraj svoj novi repozitorij i u njemu pokreni:

   ```bash
   npm install
   ```

3. Napravi bazu na [Neonu](https://neon.com) (besplatni plan, bez instalacije): nalog, novi projekat, region u Evropi. U konzoli klikni **Connect**, isključi **Connection pooling** i kopiraj connection string ([uputstvo](https://neon.com/docs/connect/connect-from-any-app)).
4. Kopiraj `.env.example` u `.env.local` (`cp .env.example .env.local`, na Windowsu `copy`). U `.env.local` upiši svoj string kao `DATABASE_URL` i na kraju stavi `?sslmode=verify-full` umjesto onoga što Neon daje.
5. Napuni bazu i pokreni aplikaciju:

   ```bash
   npm run baza     # tabele i početni podaci; svako pokretanje briše sve i učitava ispočetka
   npm run dev
   ```

   Na <http://localhost:3000> treba pisati „Aplikacija radi.“ i „Baza odgovara: kupci 60, proizvodi 40, narudzbe 2068, stavke_narudzbe 10095.“ `app/page.tsx` je samo ta provjera; zamijeni je svojim radom.

SQL nad bazom pokrećeš u Neon konzoli, u **SQL Editoru** ([uputstvo](https://neon.com/docs/get-started/query-with-neon-sql-editor)).

| Poruka | Šta uraditi |
| --- | --- |
| `nema DATABASE_URL` | Nema `.env.local` (korak 4). |
| `relation "kupci" does not exist` | Pokreni `npm run baza`. |

**Za osobu koja pomaže kod kuće**

- Git prije prvog commita traži ime i email: `git config --global user.name "Ime Prezime"` i `git config --global user.email "adresa@primjer.ba"` ([uputstvo](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)).
- `npm install` ispiše upozorenja (`npm warn`, `vulnerabilities`). To je normalno. Problem je samo `npm error`.
- `npm run dev` radi dok ga ne zaustaviš: **Ctrl+C** u terminalu.
- Finder na macOS-u ne prikazuje `.env.local`. Skrivene fajlove pokaže **Cmd+Shift+.**; u editoru se fajl vidi normalno.

## Korak 0: osnove

Ako ove alate koristiš prvi put, prođi ova poglavlja. Za fazu A trebaju samo ona. Linkovi za faze B i C su kod tih faza.

| Tema | Poglavlja | Možeš dalje kad znaš |
| --- | --- | --- |
| HTML i CSS | MDN: [HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website/Creating_the_content), [CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website/Styling_the_content) | napraviti stranicu s formom |
| JavaScript | MDN: [Variables](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Variables), [Functions](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Functions), [Arrays](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Arrays), [Objects](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Object_basics) | napisati funkciju koja filtrira i sabira niz objekata |
| TypeScript | [TS for JS Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html), [Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) | dodati tipove funkciji i objektu |
| React | [Quick Start](https://react.dev/learn), [Thinking in React](https://react.dev/learn/thinking-in-react), [State](https://react.dev/learn/state-a-components-memory) | napraviti komponentu s formom i stanjem |
| Next.js | Learn: [Getting Started](https://nextjs.org/learn/dashboard-app/getting-started), [Fetching Data](https://nextjs.org/learn/dashboard-app/fetching-data), [Mutating Data](https://nextjs.org/learn/dashboard-app/mutating-data), [Improving Accessibility](https://nextjs.org/learn/dashboard-app/improving-accessibility) | pročitati podatke iz baze i sačuvati formu na serveru |
| SQL | PostgreSQL: [poglavlje 2.4–2.7](https://www.postgresql.org/docs/current/tutorial-sql.html), [Joins](https://www.postgresql.org/docs/current/tutorial-join.html), [Foreign Keys](https://www.postgresql.org/docs/current/tutorial-fk.html) | napisati `SELECT` s `JOIN` i `GROUP BY` |
| Git | Pro Git: [Recording Changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository), [Branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell); GitHub: [Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world) | napraviti branch, commit i push |

Relacije na našim podacima: tabela čuva jednu vrstu stvari (kupac, proizvod, narudžba). Primarni ključ `id` jednoznačno označava red. Strani ključ, npr. `narudzbe.kupac_id`, pokazuje na red u drugoj tabeli. Jedna narudžba ima više stavki (1:N). Narudžbe i proizvodi su u vezi N:M preko stavki. `JOIN` spaja tabele po tim ključevima.

Provjera: napiši upit koji vraća deset kupaca s najvećim prometom u zadnjoj godini podataka (naziv, broj narudžbi, promet; promet računaj po pravilima iz poglavlja 2).

## 1. Klijent

Bistra d.o.o. je distributer pića, kafe i grickalica. Snabdijeva šezdesetak kupaca: kafiće, restorane, prodavnice, hotele i firme.

Danas narudžbe stižu telefonom, porukom i mailom. Komercijalista ih prepisuje u Excel, a skladište dobije odštampanu listu. Posljedice:

- greške u količinama i cijenama, i niko ne zna koja je verzija tačna;
- kupac pita gdje mu je roba, a odgovor traže tri osobe;
- vlasnik ne vidi koji kupci i proizvodi donose novac, ni šta je u padu;
- nabavka nagađa koliko robe naručiti. Ljeti nestane vode, zimi višak stoji u skladištu.

Bistra traži: jedno mjesto za narudžbe (unos, pregled, status), pregled poslovanja i prognozu potražnje za nabavku.

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

U podacima ima narudžbi koje predugo stoje u jednom statusu. Ako ih nađeš, pokaži ih na prezentaciji.

Promjenu šeme radi kao migraciju: SQL fajl u svom repozitoriju, pokrenut u SQL Editoru. `npm run baza` vraća originalnu šemu, pa migracije nakon toga pokreni ponovo.

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

Probaj ispravan unos, unos bez kupca, bez stavki, s količinom 0 i s negativnom cijenom. Neispravan unos ne smije završiti u bazi ni kad privremeno isključiš provjeru u formi. Kad unos ne prođe, poruka kaže koje polje nije ispravno i zašto.

**Gotovo kad:** nova narudžba ostaje i nakon osvježavanja stranice; sva četiri neispravna unosa server odbija; znaš pokazati put jednog zahtjeva od forme do baze i nazad.

**A2. Status, izmjena, novo polje.** Napravi:

1. promjenu statusa po tabeli iz poglavlja 1;
2. izmjenu i brisanje narudžbe, samo dok je `KREIRANA`;
3. jedno novo polje, npr. način plaćanja, tako da se vidi u formi, sačuva u bazi i prikaže u listi; uz to ide migracija.

**Gotovo kad:** server odbija svaki prelaz i svaku izmjenu koje tabela ne dozvoljava; novo polje radi od forme do baze.

**Predaja.** Link na tvoj repozitorij. U njegovom README-u: kako pokrenuti aplikaciju i šta još ne radi.

### Faza B: analitika (bonus)

Vlasnik hoće pregled poslovanja. Napravi stranicu s tri do četiri grafika ([MUI X Charts](https://mui.com/x/react-charts/quickstart/)) i odgovori na pitanja:

- Kako se kreće promet po mjesecima? Ima li sezone i rasta?
- Koji kupci i proizvodi donose najviše? Ko je prestao naručivati?
- Kako se vrste kupaca i kategorije razlikuju kroz godinu?
- Šta se desilo s cijenama i kako je to uticalo na promet?
- Koje narudžbe stoje u `U_OBRADI` ili `POSLATA` više od 7 dana od datuma narudžbe?

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
- Asistent ne piše proizvoljan SQL. Napiši mu nekoliko alata samo za čitanje (tool calling): promet po kupcu, top proizvodi, prognoza i slično. Smije ih pozvati više zaredom.

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
| Baza | [PostgreSQL](https://www.postgresql.org/docs/current/) na [Neonu](https://neon.com/docs/introduction) | [Supabase](https://supabase.com/docs), [lokalni PostgreSQL](https://www.postgresql.org/download/) |
| Pristup bazi | SQL s [node-postgres](https://node-postgres.com/) ili [Drizzle](https://orm.drizzle.team/docs/overview) | [Prisma](https://www.prisma.io/docs), [Kysely](https://kysely.dev/docs/intro) |
| Testovi | [Vitest](https://vitest.dev/guide/), [Playwright](https://playwright.dev/docs/intro) | [Jest](https://jestjs.io/docs/getting-started), [Cypress](https://docs.cypress.io/app/get-started/why-cypress) |

Firma koristi i Express, TypeORM, Oracle, Keycloak, nginx i Turborepo. Za ovaj zadatak nisu potrebni.

## 5. Bonus

Uz faze B i C, bonus je i:

- testovi: Vitest za pravila unosa, Playwright za unos narudžbe od početka do kraja;
- skica arhitekture u README-u: šta radi browser, šta server, šta baza;
- kratak video ili GIF glavnog toka;
- CI: GitHub Actions pokreće lint, build i testove na svaki push.

## 6. Prezentacija i kontrolna lista

Prezentacija je uživo ili preko video poziva. Prisutni su ti, osoba koja pregleda i podrška. Aplikaciju pokrećeš na svom računaru i dijeliš ekran. Kontrolna lista je dnevni red: idemo redom, kolonu *Ti* popunjavaš ti, kolonu *Pregled* osoba koja pregleda.

| Predaja | Ti | Pregled |
| --- | :---: | :---: |
| Repozitorij je dostupan; README kaže kako pokrenuti aplikaciju i šta još ne radi | ☐ | ☐ |
| Aplikacija se pokreće po tom README-u na drugom računaru | ☐ | ☐ |
| A1: lista, detalji i unos rade; nova narudžba ostaje nakon osvježavanja | ☐ | ☐ |
| A1: četiri neispravna unosa server odbija, s porukom koje polje i zašto | ☐ | ☐ |
| A2: server dozvoljava samo prelaze i izmjene iz tabele | ☐ | ☐ |
| A2: novo polje dodano, s migracijom | ☐ | ☐ |
| U repozitoriju nema lozinki ni API ključeva | ☐ | ☐ |

| Prezentacija | Ti | Pregled |
| --- | :---: | :---: |
| Glavni tok pokazan uživo | ☐ | ☐ |
| Objašnjen put jednog zahtjeva od forme do baze | ☐ | ☐ |
| Objašnjen dio koda koji je napisao AI | ☐ | ☐ |
| Objašnjena jedna odluka i alternativa koja nije izabrana | ☐ | ☐ |
| Pokazan jedan problem: kako je nađen i riješen | ☐ | ☐ |
| Rečeno šta bi bilo sljedeće | ☐ | ☐ |

| Bonus | Ti | Pregled |
| --- | :---: | :---: |
| Faza B: grafici i `ANALIZA.md` s nalazima | ☐ | ☐ |
| Faza C1: prognoza izmjerena u odnosu na osnovu | ☐ | ☐ |
| Faza C2: asistent s alatima | ☐ | ☐ |
| Testovi | ☐ | ☐ |
| Skica arhitekture ili video | ☐ | ☐ |
| CI (GitHub Actions) | ☐ | ☐ |
