# Narudžbe: praksa

Zadatak i uputstvo za postavljanje od nule: [kit/zadatak.md](kit/zadatak.md).

Pokretanje (Node.js 24+, PostgreSQL connection string):

```bash
npm install
cp .env.example .env.local   # upiši DATABASE_URL
npm run baza                 # tabele i početni podaci; svaki put briše sve i učitava ispočetka
npm run dev                  # http://localhost:3000
```

`data/`: šema, početni podaci i CSV. `scripts/`: punjenje baze i generator podataka.
