# Narudžbe: praksa

Zadatak i uputstvo za postavljanje od nule: [kit/zadatak.md](kit/zadatak.md).

```bash
npm install
cp .env.example .env.local
npm run baza
npm run dev
```

U `.env.local` upiši `DATABASE_URL`. `npm run baza` briše sve i učitava tabele, početne podatke i `migracije/`. `npm run dev` pokreće frontend (obično http://localhost:5173) i backend (port 3000).
