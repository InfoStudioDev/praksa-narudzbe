"""Generiše početne podatke: data/seed.sql i data/csv/*.csv (schema.sql se piše ručno).

Pokretanje iz korijena repozitorija: python3 scripts/generisi_podatke.py data

Uvijek isti rezultat (fiksni seed). Imena su izmišljena; emailovi su na domeni example.com.
"""

import csv
import math
import random
import sys
from datetime import date, timedelta
from pathlib import Path

random.seed(20241)

START = date(2024, 1, 1)
END = date(2025, 12, 31)

KATEGORIJE = ["Voda", "Sokovi", "Kafa i čaj", "Grickalice", "Slatkiši", "Ugostiteljski potrošni"]

# (naziv, kategorija, jedinica, cijena na kraju perioda, tipična količina)
PROIZVODI = [
    ("Prirodna mineralna voda 0,5 l", "Voda", "kom", 0.85, 48),
    ("Gazirana mineralna voda 0,5 l", "Voda", "kom", 0.90, 48),
    ("Prirodna voda 1,5 l", "Voda", "kom", 1.20, 24),
    ("Gazirana voda 1,5 l", "Voda", "kom", 1.30, 24),
    ("Voda 0,25 l staklo", "Voda", "kom", 0.95, 48),
    ("Voda 5 l", "Voda", "kom", 2.40, 6),
    ("Sok od jabuke 1 l", "Sokovi", "kom", 2.60, 12),
    ("Sok od narandže 1 l", "Sokovi", "kom", 2.90, 12),
    ("Sok od breskve 0,2 l staklo", "Sokovi", "kom", 1.40, 24),
    ("Ledeni čaj breskva 0,5 l", "Sokovi", "kom", 1.60, 24),
    ("Ledeni čaj limun 0,5 l", "Sokovi", "kom", 1.60, 24),
    ("Limunada 0,33 l", "Sokovi", "kom", 1.50, 24),
    ("Gazirani sok cola 0,33 l", "Sokovi", "kom", 1.45, 24),
    ("Gazirani sok narandža 0,33 l", "Sokovi", "kom", 1.45, 24),
    ("Kafa mljevena 500 g", "Kafa i čaj", "kom", 11.50, 4),
    ("Kafa u zrnu 1 kg", "Kafa i čaj", "kom", 27.00, 2),
    ("Espresso kapsule 50 kom", "Kafa i čaj", "pak", 16.50, 3),
    ("Instant kafa 200 g", "Kafa i čaj", "kom", 9.80, 3),
    ("Čaj kamilica 20 kesica", "Kafa i čaj", "pak", 2.40, 6),
    ("Čaj nana 20 kesica", "Kafa i čaj", "pak", 2.40, 6),
    ("Crni čaj 20 kesica", "Kafa i čaj", "pak", 2.60, 6),
    ("Topla čokolada 25 kesica", "Kafa i čaj", "pak", 8.90, 3),
    ("Čips slani 150 g", "Grickalice", "kom", 2.70, 12),
    ("Čips paprika 150 g", "Grickalice", "kom", 2.70, 12),
    ("Kikiriki slani 200 g", "Grickalice", "kom", 3.10, 12),
    ("Kukuruzni flips 50 g", "Grickalice", "kom", 0.90, 30),
    ("Perece slane 200 g", "Grickalice", "kom", 1.90, 12),
    ("Krekeri 100 g", "Grickalice", "kom", 1.30, 18),
    ("Kokice 90 g", "Grickalice", "kom", 1.20, 18),
    ("Miješani orašasti plodovi 150 g", "Grickalice", "kom", 4.90, 8),
    ("Čokolada mliječna 100 g", "Slatkiši", "kom", 2.20, 20),
    ("Čokolada s lješnikom 100 g", "Slatkiši", "kom", 2.50, 20),
    ("Keks čokoladni 200 g", "Slatkiši", "kom", 2.10, 12),
    ("Napolitanke 250 g", "Slatkiši", "kom", 2.80, 12),
    ("Bombone voćne 100 g", "Slatkiši", "kom", 1.40, 20),
    ("Žvakaće gume 10 kom", "Slatkiši", "kom", 0.80, 30),
    ("Papirne salvete 100 kom", "Ugostiteljski potrošni", "pak", 1.60, 10),
    ("Šećer u kesicama 1000 kom", "Ugostiteljski potrošni", "pak", 14.00, 1),
    ("Slamke 200 kom", "Ugostiteljski potrošni", "pak", 3.20, 2),
    ("Papirne čaše 0,2 l 50 kom", "Ugostiteljski potrošni", "pak", 3.90, 4),
]
NEAKTIVAN = {"Voda 0,25 l staklo"}  # izbačen iz ponude sredinom 2025.
UKINUT_OD = date(2025, 6, 1)

# Mjesečni sezonski faktori po kategoriji (jan..dec).
SEZONA_KAT = {
    "Voda": [0.70, 0.70, 0.85, 1.00, 1.20, 1.60, 1.90, 1.80, 1.20, 0.90, 0.75, 0.80],
    "Sokovi": [0.75, 0.75, 0.90, 1.00, 1.15, 1.50, 1.70, 1.60, 1.10, 0.90, 0.80, 1.00],
    "Kafa i čaj": [1.30, 1.20, 1.05, 0.95, 0.85, 0.75, 0.70, 0.75, 0.95, 1.10, 1.25, 1.35],
    "Grickalice": [0.90, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.10, 1.00, 0.95, 1.00, 1.40],
    "Slatkiši": [1.00, 1.10, 1.00, 1.05, 0.90, 0.80, 0.75, 0.80, 0.95, 1.00, 1.10, 1.50],
    "Ugostiteljski potrošni": [0.90, 0.90, 0.95, 1.00, 1.05, 1.15, 1.20, 1.15, 1.00, 0.95, 0.90, 1.00],
}
# Mjesečni faktori učestalosti narudžbi po vrsti kupca.
SEZONA_VRSTA = {
    "KAFIC": [0.85, 0.85, 0.95, 1.00, 1.10, 1.20, 1.25, 1.25, 1.05, 0.95, 0.90, 1.05],
    "RESTORAN": [0.85, 0.85, 0.95, 1.00, 1.05, 1.10, 1.15, 1.15, 1.00, 1.00, 1.00, 1.30],
    "PRODAVNICA": [0.90, 0.90, 1.00, 1.00, 1.05, 1.10, 1.15, 1.10, 1.00, 1.00, 1.00, 1.25],
    "HOTEL": [0.50, 0.50, 0.70, 0.90, 1.20, 1.70, 1.90, 1.90, 1.40, 0.90, 0.60, 0.90],
    "KANCELARIJA": [1.10, 1.05, 1.05, 1.00, 1.00, 0.85, 0.55, 0.55, 1.10, 1.10, 1.05, 0.80],
}
KATEGORIJE_PO_VRSTI = {
    "KAFIC": {"Voda": 3, "Sokovi": 3, "Kafa i čaj": 3, "Ugostiteljski potrošni": 1.5, "Grickalice": 0.5},
    "RESTORAN": {"Voda": 3, "Sokovi": 2.5, "Kafa i čaj": 2, "Ugostiteljski potrošni": 1.5},
    "PRODAVNICA": {"Voda": 2.5, "Sokovi": 2.5, "Grickalice": 3, "Slatkiši": 3, "Kafa i čaj": 1.5},
    "HOTEL": {"Voda": 3, "Sokovi": 2, "Kafa i čaj": 2.5, "Ugostiteljski potrošni": 1.5, "Slatkiši": 0.5},
    "KANCELARIJA": {"Kafa i čaj": 4, "Voda": 3, "Slatkiši": 1, "Ugostiteljski potrošni": 1},
}
NARUDZBI_SEDMICNO = {"KAFIC": 0.26, "RESTORAN": 0.23, "PRODAVNICA": 0.40, "HOTEL": 0.20, "KANCELARIJA": 0.10}
STAVKI = {"KAFIC": (2, 6), "RESTORAN": (2, 6), "PRODAVNICA": (3, 9), "HOTEL": (3, 8), "KANCELARIJA": (1, 4)}
RABATI = {"KAFIC": [0, 0, 0, 2], "RESTORAN": [0, 0, 2, 3], "PRODAVNICA": [0, 3, 5, 8],
          "HOTEL": [3, 5, 8, 10], "KANCELARIJA": [0, 0, 0, 3]}
DAN_U_SEDMICI = [1.25, 1.15, 1.05, 1.05, 1.00, 0.50, 0.0]  # pon..ned

GRADOVI = [("Sarajevo", 30), ("Tuzla", 10), ("Zenica", 9), ("Mostar", 9), ("Banja Luka", 8),
           ("Bihać", 6), ("Travnik", 5), ("Konjic", 4), ("Goražde", 3), ("Visoko", 4),
           ("Brčko", 4), ("Livno", 3), ("Gradačac", 3), ("Cazin", 2)]
RIJECI = ["Lipa", "Javor", "Breza", "Hrast", "Jela", "Izvor", "Most", "Kamen", "Zora", "Sunce",
          "Luka", "Polje", "Dolina", "Rijeka", "Sjever", "Centar", "Kutak", "Ugao", "Trg", "Park",
          "Bašta", "Ruža", "Neven", "Jasen", "Grab", "Topola", "Vrba", "Kesten", "Smreka", "Bistrik",
          "Mjesec", "Zvijezda", "Kruna", "Sidro", "Jedro", "Talas", "Oblak", "Duga", "Planina", "Brijeg",
          "Vidik", "Zlatica", "Biser", "Mozaik", "Kocka", "Ključ", "Kapija", "Avlija", "Čaršija", "Mlin",
          "Vrelo", "Lastavica", "Golub", "Bor", "Sedef", "Kalem", "Tulipan", "Jorgovan", "Visibaba", "Maslačak"]
PREFIKS = {"KAFIC": "Kafić", "RESTORAN": "Restoran", "PRODAVNICA": "Market", "HOTEL": "Hotel",
           "KANCELARIJA": "Biro"}
BROJ_PO_VRSTI = [("KAFIC", 20), ("RESTORAN", 10), ("PRODAVNICA", 15), ("HOTEL", 5), ("KANCELARIJA", 10)]

# Poskupljenja: od datuma, po kategoriji, faktor (cijena prije = cijena poslije / faktor).
POSKUPLJENJA = [(date(2025, 3, 1), "Kafa i čaj", 1.12), (date(2025, 1, 1), None, 1.05)]

ASCII = str.maketrans("čćđšžČĆĐŠŽ", "ccdszCCDSZ")


def tezinski(parovi):
    ukupno = sum(t for _, t in parovi)
    r = random.uniform(0, ukupno)
    for v, t in parovi:
        r -= t
        if r <= 0:
            return v
    return parovi[-1][0]


def cijena_na_dan(lista_cijena, kategorija, dan):
    c = lista_cijena
    for od, kat, faktor in POSKUPLJENJA:
        if dan < od and (kat is None or kat == kategorija):
            c = c / faktor
    return round(c, 2)


def poisson(lam):
    l, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= random.random()
        if p <= l:
            return k
        k += 1


def main(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    kategorije = [{"id": i + 1, "naziv": n} for i, n in enumerate(KATEGORIJE)]
    kat_id = {k["naziv"]: k["id"] for k in kategorije}
    kat_skr = {"Voda": "VOD", "Sokovi": "SOK", "Kafa i čaj": "KAF", "Grickalice": "GRI",
               "Slatkiši": "SLA", "Ugostiteljski potrošni": "POT"}

    proizvodi, brojac = [], {}
    for i, (naziv, kat, jm, cijena, kol) in enumerate(PROIZVODI):
        brojac[kat] = brojac.get(kat, 0) + 1
        proizvodi.append({"id": i + 1, "sifra": f"{kat_skr[kat]}-{brojac[kat]:03d}", "naziv": naziv,
                          "kategorija_id": kat_id[kat], "jedinica_mjere": jm, "cijena": f"{cijena:.2f}",
                          "aktivan": "false" if naziv in NEAKTIVAN else "true",
                          "_kat": kat, "_kol": kol, "_cijena": cijena})

    rijeci = RIJECI[:]
    random.shuffle(rijeci)
    kupci, k = [], 0
    for vrsta, broj in BROJ_PO_VRSTI:
        for _ in range(broj):
            k += 1
            rijec = rijeci.pop()
            naziv = f"{PREFIKS[vrsta]} {rijec}"
            kreiran = START - timedelta(days=random.randint(30, 900))
            kraj = None
            if random.random() < 0.13:  # novi kupci tokom perioda
                kreiran = START + timedelta(days=random.randint(120, 600))
            elif random.random() < 0.08:  # kupci koji su prestali naručivati
                kraj = START + timedelta(days=random.randint(300, 620))
            prefs = {}
            for kat, t in KATEGORIJE_PO_VRSTI[vrsta].items():
                for p in proizvodi:
                    if p["_kat"] == kat:
                        prefs[p["id"]] = t * random.choice([0.2, 0.5, 1, 1, 1.5, 2.5])
            kupci.append({"id": k, "sifra": f"K{k:04d}", "naziv": naziv, "vrsta": vrsta,
                          "grad": tezinski(GRADOVI),
                          "email": "" if random.random() < 0.2 else
                          f"{rijec.lower().translate(ASCII)}.{PREFIKS[vrsta].lower().translate(ASCII)}@example.com",
                          "kreiran": kreiran.isoformat(),
                          "_od": max(kreiran, START), "_do": kraj, "_vel": random.lognormvariate(0, 0.45),
                          "_rabat": random.choice(RABATI[vrsta]), "_prefs": prefs})

    narudzbe, stavke = [], []
    dan, sid, po_godini = START, 0, {}
    while dan <= END:
        trend = 1 + 0.12 * ((dan - START).days / 365)
        praznik = 0.0 if (dan.month, dan.day) in {(1, 1), (1, 2), (5, 1)} else 1.0
        for kupac in kupci:
            if dan < kupac["_od"] or (kupac["_do"] and dan > kupac["_do"]):
                continue
            vrsta = kupac["vrsta"]
            p = (NARUDZBI_SEDMICNO[vrsta] / 6) * SEZONA_VRSTA[vrsta][dan.month - 1] \
                * DAN_U_SEDMICI[dan.weekday()] * trend * praznik * min(kupac["_vel"], 2.0)
            if random.random() >= p:
                continue
            nid = len(narudzbe) + 1
            po_godini[dan.year] = po_godini.get(dan.year, 0) + 1
            lo, hi = STAVKI[vrsta]
            broj_stavki = random.randint(lo, hi)
            kandidati = []
            for pid, t in kupac["_prefs"].items():
                pr = proizvodi[pid - 1]
                if pr["naziv"] in NEAKTIVAN and dan >= UKINUT_OD:
                    continue
                kandidati.append((pid, t * SEZONA_KAT[pr["_kat"]][dan.month - 1]))
            izabrani = set()
            while len(izabrani) < min(broj_stavki, len(kandidati)):
                izabrani.add(tezinski([c for c in kandidati if c[0] not in izabrani]))
            for pid in sorted(izabrani):
                pr = proizvodi[pid - 1]
                sez = SEZONA_KAT[pr["_kat"]][dan.month - 1]
                kol = max(1, poisson(pr["_kol"] * kupac["_vel"] * (0.6 + 0.4 * sez)))
                sid += 1
                stavke.append({"id": sid, "narudzba_id": nid, "proizvod_id": pid, "kolicina": kol,
                               "cijena_po_komadu": f"{cijena_na_dan(pr['_cijena'], pr['_kat'], dan):.2f}",
                               "rabat_posto": f"{kupac['_rabat']:.2f}"})
            starost = (END - dan).days
            if random.random() < 0.04:
                status, isporuka = "OTKAZANA", ""
            elif starost > 10:
                status = "ISPORUCENA"
                isporuka = dan + timedelta(days=random.choice([1, 1, 2, 2, 3]))
                if isporuka.weekday() == 6:
                    isporuka += timedelta(days=1)
                isporuka = isporuka.isoformat()
            else:
                status = tezinski([("KREIRANA", 3 if starost < 3 else 0.5), ("U_OBRADI", 3),
                                   ("POSLATA", 2), ("ISPORUCENA", 1 if starost > 4 else 0)])
                isporuka = (dan + timedelta(days=2)).isoformat() if status == "ISPORUCENA" else ""
            napomena = ""
            if random.random() < 0.05:
                napomena = random.choice(["Dostava prije 9h.", "Pozvati prije dostave.",
                                          "Ulaz iz dvorišta.", "Hitno.", "Račun na email."])
            narudzbe.append({"id": nid, "broj": f"N-{dan.year}-{po_godini[dan.year]:05d}", "kupac_id": kupac["id"],
                             "datum": dan.isoformat(), "datum_isporuke": isporuka, "status": status,
                             "napomena": napomena,
                             "kreirana": f"{dan.isoformat()} {random.randint(7, 15):02d}:{random.randint(0, 59):02d}:00"
                                         f"{'+02' if 4 <= dan.month <= 10 else '+01'}"})
        dan += timedelta(days=1)

    # Nekoliko starih narudžbi koje su "zapele" u obradi: stvarni problem za analizu.
    stare = [n for n in narudzbe if n["status"] == "ISPORUCENA" and n["datum"] < "2025-09-01"]
    for n in random.sample(stare, 4):
        n["status"], n["datum_isporuke"] = "U_OBRADI", ""

    tabele = [
        ("kategorije", ["id", "naziv"], kategorije),
        ("proizvodi", ["id", "sifra", "naziv", "kategorija_id", "jedinica_mjere", "cijena", "aktivan"], proizvodi),
        ("kupci", ["id", "sifra", "naziv", "vrsta", "grad", "email", "kreiran"], kupci),
        ("narudzbe", ["id", "broj", "kupac_id", "datum", "datum_isporuke", "status", "napomena", "kreirana"], narudzbe),
        ("stavke_narudzbe", ["id", "narudzba_id", "proizvod_id", "kolicina", "cijena_po_komadu", "rabat_posto"], stavke),
    ]
    brojevi = {"id", "kategorija_id", "kupac_id", "narudzba_id", "proizvod_id", "kolicina",
               "cijena", "cijena_po_komadu", "rabat_posto", "aktivan"}

    def sql_vrijednost(kolona, v):
        if v == "" or v is None:
            return "null"
        if kolona in brojevi:
            return str(v)
        return "'" + str(v).replace("'", "''") + "'"

    csv_dir = out_dir / "csv"
    csv_dir.mkdir(exist_ok=True)
    with open(out_dir / "seed.sql", "w", encoding="utf-8") as f:
        f.write("-- Narudžbe: početni podaci. Generisani; sva imena su izmišljena.\n")
        f.write("-- Učitaj nakon schema.sql.\n\nset client_encoding = 'UTF8';\n\nbegin;\n")
        for ime, kolone, redovi in tabele:
            for i in range(0, len(redovi), 500):
                dio = redovi[i:i + 500]
                f.write(f"\ninsert into {ime} ({', '.join(kolone)}) values\n")
                f.write(",\n".join("(" + ", ".join(sql_vrijednost(c, r[c]) for c in kolone) + ")" for r in dio))
                f.write(";\n")
            f.write(f"select setval(pg_get_serial_sequence('{ime}', 'id'), (select max(id) from {ime}));\n")
        f.write("\ncommit;\n")
    for ime, kolone, redovi in tabele:
        with open(csv_dir / f"{ime}.csv", "w", encoding="utf-8", newline="") as c:
            w = csv.writer(c)
            w.writerow(kolone)
            for r in redovi:
                w.writerow([r[k] for k in kolone])

    print({ime: len(redovi) for ime, _, redovi in tabele})


if __name__ == "__main__":
    main(Path(sys.argv[1]))
