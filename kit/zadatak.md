# Praksa: aplikacija za narudžbe

## O zadatku

Praviš aplikaciju za narudžbe: lista narudžbi, detalji, unos nove narudžbe i izmjena postojeće. Podaci su izmišljeni: distributer pića i grickalica i njegovi kupci (kafići, restorani, prodavnice, hoteli i firme).

Cilj je da se upoznaš s tehnologijama, relacionim bazama i osnovnim funkcionalnostima: lista, detalji, unos, izmjena, brisanje i provjera podataka. Od toga se sastoji velik dio poslovnih sistema. Drugi cilj je da naučiš koristiti MUI kako treba, da aplikacija izgleda profesionalno.

Zadatak ima tri faze:

1. Osnovna aplikacija za prikaz i rad s narudžbama.
2. Analitika: grafici i pregledi nad podacima.
3. Pametni algoritmi i modeli mašinskog učenja: prognoza prodaje i asistent koji odgovara iz podataka.

Prva faza je ključna, a druge dvije su opcionalne. Zadatak je ciljano široko definisan i ne moraš uraditi sve. Ako kroz njega savladaš i samo osnove relacionih baza, i to je super.

Ako imaš pitanje o zadatku ili zapneš, slobodno se javi mentoru na mail, pa ćemo organizovati poseban call. Pomaže ako prije toga pushaš kod i napišeš šta radiš, koja se greška javlja i šta je već probano.

Slobodno koristi AI da ti objasni stvari i tehnologije i pomogne u učenju. Bitno je samo da razumiješ sve što on uradi i shvataš pozadinu.

## Tehnologije

- Frontend: React i MUI, pokreće ga Vite.
- Backend: Node.js, TypeScript i Hono.
- Baza: PostgreSQL, backend joj pristupa preko paketa `pg`.

Frontend šalje zahtjeve na `/api/...`, a backend čita i piše u bazu i vraća JSON. Za tabelu koristi MUI X Data Grid (besplatni paket `@mui/x-data-grid`), za grafike MUI X Charts, a za forme React Hook Form i Zod. Osnovni paketi za prvu fazu su već instalirani.

Veza s bazom je u `server/db.ts`: `pool` za upite i `transakcija()` za više upita koji moraju proći svi ili nijedan. Primjer rute je `GET /api/kupci/:id` u `server/index.ts`: provjerava ulaz Zodom i vraća poruku za svako neispravno polje. Vrijednosti od korisnika u SQL šalji samo kao parametre (`$1`), a narudžbu sa stavkama čuvaj u jednoj transakciji.

Ako s nečim radiš prvi put, počni ovdje:

- React: [Quick Start](https://react.dev/learn) i [Tutorial (Tic-Tac-Toe)](https://react.dev/learn/tutorial-tic-tac-toe)
- SQL: [SQLBolt](https://sqlbolt.com/), kratke interaktivne lekcije u pregledniku, i [zvanični PostgreSQL tutorijal](https://www.postgresql.org/docs/current/tutorial.html)
- Git i GitHub: [Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world)
- MUI: [Getting started](https://mui.com/material-ui/getting-started/) i [Data Grid](https://mui.com/x/react-data-grid/quickstart/)
- Forme: [React Hook Form](https://react-hook-form.com/get-started), za stavke [useFieldArray](https://react-hook-form.com/docs/usefieldarray), a za MUI polja [Controller](https://react-hook-form.com/docs/usecontroller/controller)

Za ostalo (JavaScript, TypeScript, Hono, Zod) potraži dokumentaciju ili pitaj AI kad ti zatreba.

### Izgled aplikacije

Aplikacija treba izgledati profesionalno. Za to ti ne treba puno svog CSS-a, nego ono što MUI već ima:

- jedna tema za cijelu aplikaciju (`ThemeProvider` i `CssBaseline`);
- osnovni raspored s trakom na vrhu ili menijem sa strane, npr. iz [MUI templates](https://mui.com/material-ui/getting-started/templates/): pakete koje template uvozi instaliraj, a plaćene (Pro, Premium) izbaci;
- Data Grid za listu narudžbi, sa sortiranjem i filterom, i status kao `Chip`;
- `Dialog` ili `Drawer` za unos i izmjenu, i `Autocomplete` za izbor kupca i proizvoda;
- poruka o grešci ispod polja i `Snackbar` kad se narudžba sačuva.

## Postavljanje

1. Instaliraj [Git](https://git-scm.com/downloads), [Node.js](https://nodejs.org/en/download) (LTS, verzija 24 ili novija) i [VS Code](https://code.visualstudio.com/). Komande pokrećeš u terminalu u VS Code-u. Na Windowsu za terminal postavi Git Bash, koji dolazi s Gitom: Ctrl+Shift+P → **Terminal: Select Default Profile** → **Git Bash**, pa otvori novi terminal. Tako komande rade isto kao na macOS-u i Linuxu. Prije prvog commita Git traži ime i email:

   ```bash
   git config --global user.name "Ime Prezime"
   git config --global user.email "adresa@primjer.ba"
   ```

2. Napravi GitHub nalog ako ga nemaš. Na stranici ovog repozitorija klikni **Use this template** → **Create a new repository**. Repozitorij može biti javan; ako je privatan, dodaj mentora kao saradnika (pitaj ga za GitHub korisničko ime). U VS Code-u se prijavi preko **Sign in with GitHub**, pa preuzmi repozitorij i instaliraj pakete:

   ```bash
   git clone https://github.com/<tvoj-nalog>/<ime-repozitorija>.git
   cd <ime-repozitorija>
   npm install
   ```

   Onda taj folder otvori u VS Code-u (File → Open Folder). Ne stavljaj ga u folder koji sinhronizuje OneDrive.

3. Napravi besplatnu bazu na [Neonu](https://neon.com/): otvori nalog i napravi projekat u Evropi. Klikni **Connect**, isključi **Connection pooling** i kopiraj connection string tačno kako ga Neon daje. Svoje SQL upite pokrećeš u Neonovom SQL Editoru. Ako već imaš PostgreSQL na računaru, možeš koristiti njega (`postgresql://postgres:LOZINKA@127.0.0.1:5432/postgres`), a upite pokretati u pgAdminu ili psql-u.

4. Kopiraj `.env.example` u `.env.local` (`cp .env.example .env.local`), pa u VS Code-u u `.env.local` upiši svoj connection string kao `DATABASE_URL`.

5. Napuni bazu i pokreni aplikaciju:

   ```bash
   npm run baza
   npm run dev
   ```

   `npm run baza` briše sve i učitava tabele, početne podatke i tvoje migracije, pa ispiše „Baza je spremna.“ `npm run dev` pokreće backend (port 3000) i frontend. Otvori adresu koju ispiše `[web]`, obično <http://localhost:5173>. Tamo piše „Aplikacija radi.“ i „Baza odgovara: kupci 60, proizvodi 40, narudzbe 2068, stavke_narudzbe 10095.“ `src/App.tsx` je samo ta provjera i njega zamjenjuješ svojom aplikacijom. Svoje rute dodaješ u `server/index.ts`.

Ako nešto ne radi:

- `npm.ps1 cannot be loaded` ili `running scripts is disabled`: terminal je PowerShell. Prebaci na Git Bash (korak 1).
- `.env.local not found` ili `nema DATABASE_URL`: nema `.env.local` (korak 4). Nakon svake izmjene `.env.local` zaustavi `npm run dev` (Ctrl+C) i pokreni ga ponovo.
- `ENOTFOUND HOST`: u `.env.local` je ostao primjer. Upiši svoj connection string.
- `relation "kupci" does not exist`: pokreni `npm run baza`.
- `ECONNREFUSED 127.0.0.1:5432`: lokalna baza nije pokrenuta.
- `EADDRINUSE` i port `3000`: aplikacija već radi u drugom terminalu. Zaustavi je tamo (Ctrl+C).
- `Backend ne odgovara` ili `ECONNREFUSED 127.0.0.1:3000`: backend se nije pokrenuo. Pogledaj redove `[api]` u terminalu.
- Uz Neon se ispiše `SECURITY WARNING` o SSL-u. To je samo upozorenje i sve radi.

Ako ti se u postavljanju javi greška ili zapneš, slobodno se javi mentoru na mail, s tačnom porukom greške, pa ćemo to riješiti zajedno.

## Podaci

U `data/` su šema (`schema.sql`) i početni podaci (`seed.sql`) za dvije godine poslovanja.

```text
kupci ─< narudzbe ─< stavke_narudzbe >─ proizvodi >─ kategorije
```

| Tabela | Važne kolone |
| --- | --- |
| `kupci` | `sifra`, `naziv`, `vrsta`, `grad` |
| `kategorije` | `naziv` |
| `proizvodi` | `sifra`, `naziv`, `kategorija_id`, `cijena`, `aktivan` |
| `narudzbe` | `broj`, `kupac_id`, `datum`, `datum_isporuke`, `status` |
| `stavke_narudzbe` | `narudzba_id`, `proizvod_id`, `kolicina`, `cijena_po_komadu`, `rabat_posto` |

- Iznos stavke je `kolicina × cijena_po_komadu × (1 − rabat_posto / 100)`.
- `proizvodi.cijena` je današnja cijena, a `cijena_po_komadu` cijena u trenutku narudžbe.
- Otkazane narudžbe ne ulaze u promet.
- Zadnji datum u podacima uzmi kao današnji.

Nova narudžba ima kupca i bar jednu stavku. Broj joj dodjeljuje server: `N-`, godina iz datuma narudžbe i sljedeći redni broj u toj godini, s pet cifara (npr. `N-2025-00001`). Broj se ne mijenja ni kad se narudžba kasnije izmijeni. U stavci je aktivan proizvod, svaki proizvod samo jednom; količina je cijeli broj veći od nule, cijena nula ili više, a rabat od 0 do 100. Ova pravila provjerava server, ne samo forma.

Status narudžbe ide ovim redom:

| Status | Može preći u |
| --- | --- |
| `KREIRANA` | `U_OBRADI`, `OTKAZANA` |
| `U_OBRADI` | `POSLATA`, `OTKAZANA` |
| `POSLATA` | `ISPORUCENA` |
| `ISPORUCENA`, `OTKAZANA` | (kraj) |

Kupac, datum i stavke mogu se mijenjati, a narudžba brisati, samo dok je `KREIRANA`. Status se mijenja po tabeli.

Promjenu šeme, npr. novu kolonu ili tabelu, napiši kao SQL fajl u folderu `migracije/`. `npm run baza` nakon početnih podataka pokrene i te fajlove, redom po imenu, i ispiše koje je pokrenuo.

## Kontrolna lista

Radi redom po kontrolnoj listi. Kad nešto proradi, označi to u `kit/zadatak.md` u svom repozitoriju (`- [ ]` postaje `- [x]`), commitaj i pushaj.

### Početak

- [ ] `npm run baza` ispiše „Baza je spremna.“, a <http://localhost:5173> pokaže broj redova u tabelama.
- [ ] SQLBolt, lekcije 1–17.
- [ ] `sql/prvi-upit.sql` vraća deset kupaca s najvećim prometom u zadnjoj godini podataka: naziv, broj narudžbi i promet, bez otkazanih narudžbi.
- [ ] React Quick Start i Tutorial (Tic-Tac-Toe), u posebnom folderu, ne u ovom repozitoriju.
- [ ] `GET /api/kupci` vraća prvih deset kupaca iz baze kao JSON.

### Faza 1: narudžbe

- [ ] Aplikacija ima MUI temu, traku na vrhu ili meni sa strane i naslov Narudžbe.
- [ ] `GET /api/narudzbe` vraća narudžbe: broj, kupac, datum, status i iznos.
- [ ] Stranica Narudžbe ih prikazuje u Data Gridu. Sortiranje radi i može se filtrirati po statusu.
- [ ] Klik na narudžbu otvara detalje: stavke (proizvod, količina, cijena, rabat, iznos) i ukupan iznos.
- [ ] `GET /api/kupci` sada vraća sve kupce, a `GET /api/proizvodi` aktivne proizvode s cijenom.
- [ ] Forma za novu narudžbu ima kupca, datum i stavke. Stavka se dodaje i uklanja, a cijena se popuni iz cjenovnika i može se promijeniti.
- [ ] Sačuvana narudžba ima broj koji je dao server i status `KREIRANA`, i vidi se u listi i nakon osvježavanja stranice.
- [ ] Server odbija neispravnu narudžbu i kad je poslana bez forme (F12, `fetch` u konzoli): bez kupca, bez stavki, količina `0` ili `1.5`, cijena `-1`, rabat `120`, isti proizvod dvaput. Vraća status 400 i poruku za polje koje nije ispravno.
- [ ] Server odbija i proizvod koji je neaktivan ili ne postoji. Server to provjerava upitom u bazu.
- [ ] Kad server odbije narudžbu, forma prikaže njegovu poruku uz polje na koje se odnosi. Provjeri to tako što u SQL editoru proizvodu koji je već u formi postaviš `aktivan = false`, pa sačuvaš.
- [ ] Narudžbu sa statusom `KREIRANA` obrišeš.
- [ ] U detaljima se status bira s padajuće liste koja nudi samo dozvoljene prelaze.
- [ ] Nedozvoljen prelaz (npr. `ISPORUCENA` → `KREIRANA`), poslan preko `fetch` u konzoli, server odbija (status 400).
- [ ] Narudžbu sa statusom `KREIRANA` otvoriš u istoj formi kao novu, promijeniš kupca, datum i stavke i sačuvaš. Server izmjenu provjerava po istim pravilima kao novu narudžbu. Izmjena ostaje i nakon osvježavanja.
- [ ] Kod narudžbe koja nije `KREIRANA` server odbija izmjenu kupca, datuma i stavki, i brisanje (status 400).
- [ ] `migracije/001-nacin-placanja.sql` dodaje u `narudzbe` kolonu `nacin_placanja` (`GOTOVINA`, `KARTICA` ili `VIRMAN`). Postojeće narudžbe dobiju `VIRMAN`, a `npm run baza` prolazi bez greške.
- [ ] Način plaćanja se bira u formi i vidi u listi.

### Faza 2: analitika (opcionalno)

Upite piši u SQL-u i drži ih u repozitoriju.

- [ ] Grafik prometa po mjesecima ([MUI X Charts](https://mui.com/x/react-charts/quickstart/)).
- [ ] Tabela s top deset kupaca i top deset proizvoda po prometu.
- [ ] Grafik prometa po vrsti kupca i po kategoriji, po mjesecima.
- [ ] Lista narudžbi koje stoje u `U_OBRADI` ili `POSLATA` više od 7 dana od datuma narudžbe.
- [ ] `ANALIZA.md` s tri do pet nalaza, svaki s brojem iz podataka.

### Faza 3: pametni algoritmi (opcionalno)

Sve ovdje je besplatno. Prognoza se radi u Pythonu s modelom [Chronos-2](https://github.com/amazon-science/chronos-forecasting), koji radi i bez grafičke kartice. Python i pakete najlakše postaviš preko [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv init --python 3.13 prognoza
cd prognoza
uv add chronos-forecasting pandas "psycopg[binary]" python-dotenv
uv run main.py
```

Model se sam preuzme pri prvom pokretanju (oko pola GB). Connection string skripta čita sa `load_dotenv("../.env.local")` (paket python-dotenv). Na Windowsu s ARM procesorom (npr. Snapdragon) poslije `cd prognoza` pokreni i `uv python pin cpython-3.13-windows-x86_64-none`, jer PyTorch za taj procesor nema gotov paket.

Za asistenta treba besplatan Gemini API ključ iz [Google AI Studija](https://aistudio.google.com/apikey), s dnevnim ograničenjem broja upita. Paketi su `ai` i `@ai-sdk/google`. Ključ upiši u `.env.local` kao `GOOGLE_GENERATIVE_AI_API_KEY` i koristi ga samo na backendu, nikad u frontendu.

- [ ] Python skripta čita iz baze sedmične količine po kategoriji. Sedmice bez prodaje imaju 0, inače ih model ne prihvata.
- [ ] Zadnjih 12 sedmica sakriješ i prognoziraš ih jednostavno: ista sedmica prošle godine. Izmjeriš grešku (MAE).
- [ ] Istih 12 sedmica prognoziraš s Chronos-2, izmjeriš grešku i uporediš je s jednostavnom prognozom.
- [ ] Prognoza za narednih osam sedmica, sa srednjom vrijednošću i rasponom (p10 do p90), upisana je u tabelu `prognoze`. `npm run baza` briše i nju, pa skriptu nakon toga pokreneš ponovo.
- [ ] Grafik u aplikaciji prikazuje stvarne količine i prognozu s rasponom, kao u primjeru [Line with forecast](https://mui.com/x/react-charts/line-demo/#line-with-forecast).
- [ ] Asistent odgovara na pitanja iz podataka, npr. „Koji kafići u Mostaru su najviše naručivali ljeti?“ Koristi [Vercel AI SDK](https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling) s [Gemini modelom](https://ai-sdk.dev/providers/ai-sdk-providers/google-generative-ai). Asistent ne piše SQL sam, nego koristi tri do pet alata koji samo čitaju podatke, npr. promet po kupcu ili prognozu. Vidi se koje je alate pozvao.

### Završna prezentacija

- [ ] README kaže kako pokrenuti aplikaciju i šta još ne radi.
- [ ] U repozitoriju nema lozinki ni API ključeva.

Na prezentaciji pokreneš aplikaciju na svom računaru i pokažeš je. Objasni put jednog zahtjeva od forme do baze i nazad, jedan problem i kako je riješen, i šta bi bilo sljedeće. Ako je dio koda napisao AI, objasni i njega. Slajdovi nisu potrebni.
