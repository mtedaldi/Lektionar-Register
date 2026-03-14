#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# Lektionar-Scraper – dli-daten.de (Lektionar 1982 ff.)
# Abhängigkeiten: requests (pip3 install requests)
# Alles andere: Python-Standardbibliothek
#
# Aufruf:
#   python3 lektionar_scraper.py
#
# Ergebnis:
#   lektionar_1982.csv  (UTF-8 mit BOM, Semikolon-getrennt, Excel-kompatibel)
# ═══════════════════════════════════════════════════════════════════════════

import requests
import csv
import time
from html.parser import HTMLParser

BASE_URL = "https://dli-daten.de/dli/dlb/schriftstellen"
OUTPUT   = "lektionar_1982.csv"

BUECHER = [
    ("Gen","Gen"),("Ex","Ex"),("Lev","Lev"),("Num","Num"),("Dtn","Dtn"),
    ("Jos","Jos"),("Ri","Ri"),("Rut","Rut"),
    ("1 Sam","1+Sam"),("2 Sam","2+Sam"),("1 Kön","1+Koen"),("2 Kön","2+Koen"),
    ("1 Chr","1+Chr"),("2 Chr","2+Chr"),
    ("Esra","Esra"),("Neh","Neh"),("Tob","Tob"),("Jdt","Jdt"),("Est","Est"),
    ("1 Makk","1+Makk"),("2 Makk","2+Makk"),
    ("Ijob","Ijob"),("Ps","Ps"),("Spr","Spr"),("Koh","Koh"),("Hld","Hld"),
    ("Weish","Weish"),("Sir","Sir"),
    ("Jes","Jes"),("Jer","Jer"),("Klgl","Klgl"),("Bar","Bar"),("Ez","Ez"),("Dan","Dan"),
    ("Hos","Hos"),("Joël","Joel"),("Am","Am"),("Obd","Obd"),("Jona","Jona"),
    ("Mi","Mi"),("Nah","Nah"),("Hab","Hab"),("Zef","Zef"),("Hag","Hag"),
    ("Sach","Sach"),("Mal","Mal"),
    ("Mt","Mt"),("Mk","Mk"),("Lk","Lk"),("Joh","Joh"),("Apg","Apg"),
    ("Röm","Roem"),("1 Kor","1+Kor"),("2 Kor","2+Kor"),("Gal","Gal"),
    ("Eph","Eph"),("Phil","Phil"),("Kol","Kol"),
    ("1 Thess","1+Thess"),("2 Thess","2+Thess"),
    ("1 Tim","1+Tim"),("2 Tim","2+Tim"),("Tit","Tit"),("Phlm","Phlm"),
    ("Hebr","Hebr"),("Jak","Jak"),
    ("1 Petr","1+Petr"),("2 Petr","2+Petr"),
    ("1 Joh","1+Joh"),("2 Joh","2+Joh"),("3 Joh","3+Joh"),("Jud","Jud"),("Offb","Offb"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; LektionarScraper/1.0)"}

class TabellenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_td = False
        self.aktuelle_zeile = None
        self.aktueller_text = []
        self.zeilen = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
        elif tag == "tr" and self.in_table:
            self.aktuelle_zeile = []
        elif tag == "td" and self.aktuelle_zeile is not None:
            self.in_td = True
            self.aktueller_text = []

    def handle_endtag(self, tag):
        if tag == "td" and self.in_td:
            self.in_td = False
            self.aktuelle_zeile.append("".join(self.aktueller_text).strip())
        elif tag == "tr" and self.aktuelle_zeile is not None:
            if len(self.aktuelle_zeile) >= 5:
                self.zeilen.append(self.aktuelle_zeile)
            self.aktuelle_zeile = None
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data):
        if self.in_td:
            self.aktueller_text.append(data)


def hol_buch(buch_anzeige, buch_url):
    url = f"{BASE_URL}?auswahl={buch_url}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = "utf-8"
    except Exception as e:
        print(f"FEHLER: {e}")
        return []

    parser = TabellenParser()
    parser.feed(r.text)

    if not parser.zeilen:
        print("WARNUNG: keine Tabellenzeilen", end=" ")
        return []

    ergebnis = []
    letzter_vers = ""
    letztes_formular = ""

    for z in parser.zeilen:
        vers     = z[0].strip()
        formular = z[1].strip()
        lesejahr = z[2].strip()
        band     = z[3].strip()
        seite    = z[4].strip()

        # Carry-forward
        if vers:     letzter_vers = vers
        else:        vers = letzter_vers
        if formular: letztes_formular = formular
        else:        formular = letztes_formular

        # Ungültige Zeilen überspringen
        if not band or not seite: continue
        if "lektionar" in band.lower(): continue

        ergebnis.append({
            "schriftstelle": f"{buch_anzeige} {vers}" if vers else "",
            "messformular":  formular,
            "lesejahr":      lesejahr,
            "band":          band,
            "seite":         seite,
        })

    return ergebnis


def main():
    print("Lektionar-Scraper – dli-daten.de (1982 ff.)\n")
    alle = []

    for i, (buch_anzeige, buch_url) in enumerate(BUECHER, 1):
        print(f"  [{i:2d}/{len(BUECHER)}] {buch_anzeige:<10} ... ", end="", flush=True)
        zeilen = hol_buch(buch_anzeige, buch_url)
        alle.extend(zeilen)
        print(f"{len(zeilen)} Einträge")
        time.sleep(0.4)

    with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f,
            fieldnames=["schriftstelle","messformular","lesejahr","band","seite"],
            delimiter=";")
        writer.writeheader()
        writer.writerows(alle)

    print(f"\nFertig! {len(alle)} Einträge → {OUTPUT}")

if __name__ == "__main__":
    main()
