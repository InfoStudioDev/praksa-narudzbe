# Praksa: aplikacija za narudžbe

Pored koda gledamo kako istražuješ, rješavaš probleme i objašnjavaš odluke. Unaprijed je pripremljeno samo okruženje (vidi `README.md`). Sve ostalo gradiš samostalno.

**Kako se radi**

- Vodi `DNEVNIK.md` u svom repozitoriju. Za svaku veću stvar kratko zapiši: šta treba, šta čitaš i probaš, šta nije radilo, šta biraš i zašto.
- AI koristi slobodno, za objašnjenje koda, greške ili pojma. Ne predaj kod koji ne razumiješ. Ako je AI napisao veći dio nečega, navedi to u dnevniku.
- Kad zapneš, prvo pročitaj poruku greške i dokumentaciju, pa pretraži. Ako ne ide, pošalji podršci tačnu poruku greške i šta nije pomoglo.
- Commitaj često, s jasnim porukama.

Podrška: ______________________________

Faze idu od lakše ka težoj. Faza A je obavezna. B i C su dodatne i teže; računa se svaka završena.

## Korak 0: osnove

Ako ove alate koristiš prvi put, kreni odavde. Linkovi vode na zvaničnu dokumentaciju.

| Tema | Šta proći | Možeš dalje kad znaš |
| --- | --- | --- |
| HTML i CSS | [MDN: Your first website](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website) | napraviti jednostavnu stranicu s formom |
| JavaScript | [MDN: JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting) | napisati funkciju koja filtrira i sabira niz objekata |
| TypeScript | [TypeScript za JavaScript programere](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html) | dodati tipove funkciji i objektu |
| React | [react.dev/learn](https://react.dev/learn) | napraviti komponentu s formom i stanjem |
| Next.js | [Next.js Learn: Dashboard App](https://nextjs.org/learn/dashboard-app) | objasniti razliku između server i client komponente |
| SQL i relacije | PostgreSQL: [poglavlje 2](https://www.postgresql.org/docs/current/tutorial-sql.html), [strani ključevi](https://www.postgresql.org/docs/current/tutorial-fk.html), [ograničenja](https://www.postgresql.org/docs/current/ddl-constraints.html) | napisati `SELECT` s `JOIN` i `GROUP BY` (kako pokrenuti SQL: `README.md`) |
| Git | [Pro Git, poglavlja 1–3](https://git-scm.com/book/en/v2), [GitHub: Git basics](https://docs.github.com/en/get-started/git-basics) | napraviti branch, commit i push |

Relacije na našim podacima: tabela čuva jednu vrstu stvari (kupac, proizvod, narudžba). Primarni ključ `id` jednoznačno označava red. Strani ključ, npr. `narudzbe.kupac_id`, pokazuje na red u drugoj tabeli. Jedna narudžba ima više stavki (1:N). Narudžbe i proizvodi su u vezi N:M preko stavki. `JOIN` spaja tabele po tim ključevima.

Provjera: napiši upit koji vraća deset kupaca s najvećim prometom u 2025. godini (naziv, broj narudžbi, promet; promet računaj po pravilima iz poglavlja 2). Kad ga znaš napisati i objasniti, kreni na fazu A.

## 1. Zašto ova aplikacija

Klijent je distributer pića, kafe i grickalica. Snabdijeva šezdesetak kupaca: kafiće, restorane, prodavnice, hotele i firme.

Danas narudžbe stižu telefonom, porukom i mailom. Komercijalista ih prepisuje u Excel, a skladište dobije odštampanu listu. Posljedice:

- greške u količinama i cijenama, i niko ne zna koja je verzija tačna;
- kupac pita gdje mu je roba, a odgovor traže tri osobe;
- vlasnik ne vidi koji kupci i proizvodi donose novac, ni šta je u padu;
- nabavka nagađa koliko robe naručiti. Ljeti nestane vode, zimi višak stoji u skladištu.

Klijent traži:

1. jedno mjesto za narudžbe: unos, pregled i status;
2. pregled poslovanja: promet, kupci, proizvodi, sezona;
3. prognozu potražnje za nabavku i asistenta koji odgovara na pitanja o podacima.

| Ko koristi | Šta radi |
| --- | --- |
| Komercijalista | unosi i ispravlja narudžbe |
| Skladište | priprema robu i mijenja status |
| Vlasnik | prati poslovanje |
| Nabavka | gleda prognozu i planira narudžbe kod dobavljača |

Tok narudžbe: `KREIRANA` → `U_OBRADI` → `POSLATA` → `ISPORUCENA`. Dok nije poslata, narudžba može biti `OTKAZANA`.

## 2. Podaci

U `data/` su šema (`schema.sql`) i podaci (`seed.sql`, isto u `csv/`). Podaci su generisani i pokrivaju dvije godine poslovanja. Završavaju 31. 12. 2025; za analizu i prognozu to je „danas“. Imena su izmišljena.

```text
kupci ─< narudzbe ─< stavke_narudzbe >─ proizvodi >─ kategorije
```

| Tabela | Šta je | Važne kolone |
| --- | --- | --- |
| `kupci` | kupci distributera | `sifra`, `naziv`, `vrsta`, `grad` |
| `kategorije` | grupe proizvoda | `naziv` |
| `proizvodi` | cjenovnik | `sifra`, `naziv`, `kategorija_id`, `cijena`, `aktivan` |
| `narudzbe` | zaglavlje narudžbe | `broj`, `kupac_id`, `datum`, `datum_isporuke`, `status` |
| `stavke_narudzbe` | proizvodi u narudžbi | `narudzba_id`, `proizvod_id`, `kolicina`, `cijena_po_komadu`, `rabat_posto` |

Pravila:

- `proizvodi.cijena` je trenutna cijena. `stavke_narudzbe.cijena_po_komadu` je cijena u trenutku narudžbe. Nisu uvijek iste.
- Iznos stavke = `kolicina × cijena_po_komadu × (1 − rabat_posto / 100)`.
- Otkazane narudžbe ne ulaze u promet.
- Neaktivan proizvod se ne nudi u novim narudžbama, ali ostaje u starim.

Podaci nisu savršeni. Ako nađeš nešto čudno, zapiši i predloži šta bi klijent trebao uraditi. Ako mijenjaš šemu, napiši migraciju (SQL fajl) i obrazloži je u dnevniku.

## 3. Faze

### Faza A: narudžbe (obavezno)

Radi redom. A1 i A2 se računaju posebno.

**A1. Lista i unos.** Napravi:

1. listu narudžbi u MUI X Data Gridu (ili alternativi iz poglavlja 4): broj, kupac, datum, status, broj stavki, iznos; sortiranje i filter po statusu;
2. detalje narudžbe sa stavkama;
3. unos nove narudžbe: kupac, datum i jedna ili više stavki (proizvod, količina, cijena po komadu, rabat; cijena se predlaže iz cjenovnika).

Pravila unosa, u formi i na serveru:

- kupac je obavezan i narudžba ima bar jednu stavku;
- proizvod je obavezan i aktivan, a isti proizvod se javlja samo jednom po narudžbi;
- količina je cijeli broj veći od nule, cijena nula ili veća, rabat od 0 do 100.

Probaj ispravan unos, unos bez kupca, bez stavki, s količinom 0 i s negativnom cijenom. Neispravan unos ne smije završiti u bazi ni kad privremeno isključiš provjeru u formi. Ako se narudžba ne sačuva, korisnik vidi jasnu poruku.

**Gotovo kad:** nova narudžba ostaje i nakon osvježavanja stranice; sva četiri neispravna unosa server odbija; znaš pokazati put jednog zahtjeva od forme do baze i nazad.

**A2. Status, izmjena, novo polje.** Napravi:

1. promjenu statusa po toku iz poglavlja 1; nedozvoljen prelaz se odbija;
2. izmjenu i brisanje: narudžbu u statusu `KREIRANA` možeš izmijeniti ili obrisati, a u statusu `U_OBRADI` samo otkazati;
3. jedno novo polje, npr. način plaćanja, tako da se vidi u formi, sačuva u bazi i prikaže u listi. Uz to ide migracija.

**Gotovo kad:** status ide samo dozvoljenim putem; poslata narudžba se ne može izmijeniti ni obrisati; novo polje radi od forme do baze.

### Faza B: analitika

Vlasnik hoće pregled poslovanja. Napravi stranicu s tri do četiri grafika (MUI X Charts ili alternativa iz poglavlja 4) i odgovori na pitanja:

- Kako se kreće promet po mjesecima? Ima li sezone i rasta?
- Koji kupci i proizvodi donose najviše? Ko je prestao naručivati?
- Kako se vrste kupaca i kategorije razlikuju kroz godinu?
- Šta se desilo s cijenama i kako je to uticalo na promet?
- Ima li narudžbi koje predugo stoje u istom statusu?

Upite piši u SQL-u i drži ih u repozitoriju. Ne računaj sve u browseru.

**Gotovo kad:** grafici rade nad bazom, a u `ANALIZA.md` su tri do pet nalaza. Svaki nalaz ima broj iz podataka i jednu rečenicu preporuke za klijenta.

### Faza C: prognoza i asistent

**C1. Prognoza potražnje.** Nabavka pita koliko čega naručiti za sljedećih osam sedmica.

- Napravi sedmične serije količina po proizvodu ili kategoriji, samo iz početnih podataka. Pazi na nepotpune sedmice i proizvode koji se više ne prodaju.
- Prvo napravi jednostavnu osnovu (baseline), npr. ista sedmica prošle godine ili prosjek zadnjih sedmica.
- Onda model: Chronos-2 ili TimesFM. Sakrij zadnjih 12 sedmica, prognoziraj ih i izmjeri grešku (npr. MAE) za model i za osnovu.
- Prikaži prognozu u aplikaciji uz stvarne vrijednosti.

Ovaj dio može biti u [Pythonu](https://www.python.org/downloads/). Rezultat ide u bazu ili CSV koji aplikacija čita.

**C2. Asistent nad podacima.** Korisnik pita, npr. „Koji kafići u Mostaru su najviše naručivali ljeti?“ ili „Šta da naručimo za sljedeći mjesec?“, a asistent odgovara iz podataka.

- Asistent ne piše proizvoljan SQL. Napiši mu nekoliko alata samo za čitanje (tool calling): promet po kupcu, top proizvodi, prognoza i slično.
- Prikaži koje je alate pozvao.
- API ključ je u `.env.local`, nikad u kodu ni u repozitoriju. Bez ključa možeš koristiti Ollama lokalno.
- Zapiši bar dva pitanja na koja asistent odgovara pogrešno i zašto.

**Gotovo kad:** prognoza je bolja od osnove ili znaš objasniti zašto nije; asistent odgovara iz podataka i vidi se koje je alate koristio.

## 4. Tehnologije

Ovo koristimo. Ako izabereš alternativu, u dnevniku napiši zašto.

| Područje | Koristimo | Alternative |
| --- | --- | --- |
| Framework | [Next.js](https://nextjs.org/docs/app/getting-started) (App Router) | [React Router](https://reactrouter.com/start/framework/installation), [TanStack Start](https://tanstack.com/start/latest/docs/framework/react/overview) |
| UI | [MUI](https://mui.com/material-ui/getting-started/installation/) | [Mantine](https://mantine.dev/getting-started/), [shadcn/ui](https://ui.shadcn.com/docs) |
| Tabela | [MUI X Data Grid](https://mui.com/x/react-data-grid/quickstart/), paket `@mui/x-data-grid` | [AG Grid](https://www.ag-grid.com/react-data-grid/getting-started/), [TanStack Table](https://tanstack.com/table/latest/docs/overview) |
| Grafici | [MUI X Charts](https://mui.com/x/react-charts/quickstart/) | [Recharts](https://recharts.github.io/en-US/guide/getting-started/), [Apache ECharts](https://echarts.apache.org/handbook/en/get-started/) |
| Forme i validacija | [React Hook Form](https://react-hook-form.com/get-started) + [Zod](https://zod.dev/) | [TanStack Form](https://tanstack.com/form/latest/docs/overview), [Valibot](https://valibot.dev/guides/introduction/) |
| Pisanje u bazu | [Server Actions](https://nextjs.org/docs/app/getting-started/mutating-data) | [Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers) |
| Baza | [PostgreSQL](https://www.postgresql.org/docs/current/) | [Supabase](https://supabase.com/docs), [Neon](https://neon.com/docs/introduction), [SQLite](https://www.sqlite.org/docs.html), [Oracle Free](https://www.oracle.com/database/free/) |
| Pristup bazi | čisti SQL ili [Drizzle](https://orm.drizzle.team/docs/overview) | [Prisma](https://www.prisma.io/docs), [Kysely](https://kysely.dev/docs/intro), [TypeORM](https://typeorm.io/) |
| Prognoza | [Chronos-2](https://github.com/amazon-science/chronos-forecasting) | [TimesFM](https://github.com/google-research/timesfm), [statsforecast](https://nixtlaverse.nixtla.io/statsforecast/docs/getting-started/getting_started_short.html), [Prophet](https://facebook.github.io/prophet/docs/quick_start.html) |
| Analiza | [pandas](https://pandas.pydata.org/docs/getting_started/index.html), [Jupyter](https://jupyter.org/install) | SQL direktno nad bazom |
| LLM | [Vercel AI SDK](https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling) | [Anthropic API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), [OpenAI API](https://developers.openai.com/api/docs/guides/function-calling), [Ollama](https://docs.ollama.com/capabilities/tool-calling) (lokalno) |
| Testovi | [Vitest](https://vitest.dev/guide/), [Playwright](https://playwright.dev/docs/intro) | [Jest](https://jestjs.io/docs/getting-started), [Cypress](https://docs.cypress.io/app/get-started/why-cypress) |

Napomene:

- Data Grid: dovoljna je besplatna verzija (`@mui/x-data-grid`). Pro i Premium ne trebaju. Pazi da verzija odgovara verziji MUI-ja.
- TimesFM 3.0 ima težine pod nekomercijalnom licencom (2.5 je Apache-2.0). Za učenje je u redu, ali to zapiši. Chronos-2 je Apache-2.0.
- Next.js je postavljen s podrazumijevanim postavkama, uključujući Cache Components. Pročitaj u dokumentaciji šta to znači za čitanje iz baze; `app/page.tsx` je jedan primjer.
- Firma koristi i Express, TypeORM, Oracle, Keycloak, Docker, nginx i Turborepo. Za ovaj zadatak nisu potrebni.

## 5. Bonusi

- Testovi: Vitest za pravila unosa, Playwright za unos narudžbe od početka do kraja.
- Skica arhitekture u README-u: šta radi browser, šta server, šta baza.
- Kratak video ili GIF glavnog toka.
- CI: GitHub Actions pokreće lint, build i testove na svaki push.
- Docker i za aplikaciju.
- Izvoz u Excel, pretraga, paginacija na serveru.
- Nešto drugo što bi klijentu pomoglo. Objasni zašto.

## 6. Kontrolna lista

Popunjavamo je zajedno, na predaji i na prezentaciji. Kolona *Ti* je tvoja, kolona *Pregled* je za osobu koja pregleda.

| Predaja | Ti | Pregled |
| --- | :---: | :---: |
| Repozitorij je dostupan; README objašnjava pokretanje od nule | ☐ | ☐ |
| Aplikacija se pokreće po README-u na drugom računaru | ☐ | ☐ |
| `DNEVNIK.md`: za veće odluke piše šta je čitano i probano, šta nije radilo, zašto je izabrano i gdje je pomogao AI | ☐ | ☐ |
| A1: lista, detalji i unos rade; nova narudžba ostaje nakon osvježavanja | ☐ | ☐ |
| A1: četiri neispravna unosa server odbija; neuspjelo čuvanje daje jasnu poruku | ☐ | ☐ |
| A2: status ide samo dozvoljenim putem; izmjena i brisanje po pravilima | ☐ | ☐ |
| A2: novo polje dodano, s migracijom | ☐ | ☐ |
| U repozitoriju nema lozinki ni API ključeva | ☐ | ☐ |
| Zapisano šta još ne radi | ☐ | ☐ |

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
| CI ili Docker za aplikaciju | ☐ | ☐ |
