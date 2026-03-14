# Lektionar-Register

Durchsuchbares Schriftstellenregister für die deutschen Messlektionare (Bände I–VIII).

## Demo

👉 [Live-Version auf GitHub Pages](https://mtedaldi.github.io/lektionar-register)

*(Link nach Aktivierung von GitHub Pages eintragen)*

## Features

- Bandübergreifende Suche nach Bibelstellen
- Perikopen-Überlappungssuche (z. B. `Joh 3,16` findet `Joh 3,14–21`)
- Unterstützt Lektionar 1982 ff. (EÜ 1980) und 2018 ff. (EÜ 2016, in Vorbereitung)
- Intelligenter Parser für Lektionar-Notation (`Gen 1,1.26–28.31a`, `Gen 2,7-9; 3,1-7` usw.)
- Biblische Sortierreihenfolge
- CSV-Export der gefilterten Ergebnisse
- Offline-fähig – einzelne HTML-Datei, keine externen Abhängigkeiten, kein Server nötig

## Verwendung

Die Datei `index.html` im Browser öffnen – keine Installation, kein Login, kein Tracking.

Oder direkt online über die GitHub-Pages-URL oben.

## Projektstand

| Datensatz | Status |
|---|---|
| 1982 ff. (EÜ 1980) | ✅ Vollständig (4557 Einträge) |
| 2018 ff. (EÜ 2016) | ⏳ In Vorbereitung – Kontakt mit DLI läuft |

## Dateistruktur

```
lektionar-register/
├── index.html           # Die Anwendung (standalone, offline-fähig)
├── README.md
├── LICENSE
└── tools/
    ├── lektionar_scraper.py   # Scrapt 1982-Daten von dli-daten.de
    └── embed_fonts.sh         # Bettet Schriften lokal ein (Datenschutz)
```

## Werkzeuge

### lektionar_scraper.py

Scrapt das Schriftstellenverzeichnis von [dli-daten.de](https://dli-daten.de) und speichert es als CSV.

```bash
pip3 install requests
python3 tools/lektionar_scraper.py
# → lektionar_1982.csv
```

### embed_fonts.sh

Ersetzt die Google-Fonts-Anfrage durch lokal eingebettete Schriften (DSGVO/DSG-konform).

```bash
chmod +x tools/embed_fonts.sh
./tools/embed_fonts.sh index.html
# → index_offline.html
```

## Daten und Urheberrecht

Die eingebetteten Daten des Lektionars 1982 ff. wurden mit dem enthaltenen Scraper von
[dli-daten.de](https://dli-daten.de) bezogen und sind **© Deutsches Liturgisches Institut, Trier**.

Dieses Projekt ist nicht-kommerziell und dient ausschliesslich der liturgischen Praxis.
Eine Klärung der Nutzungsrechte mit dem DLI ist in Vorbereitung.

Wer die Daten selbst beziehen möchte, kann dies mit `tools/lektionar_scraper.py` direkt
von der Originalquelle tun.

## Lizenz

**Code:** MIT License – siehe [LICENSE](LICENSE)

**Daten:** © Deutsches Liturgisches Institut, Trier – nicht unter der MIT-Lizenz

## Mitwirken

Fehler, Verbesserungsvorschläge oder Ergänzungen gerne als Issue oder Pull Request.

## Entstehung

Dieses Tool wurde in Zusammenarbeit mit [Claude](https://claude.ai) (Anthropic) entwickelt.
Die Idee, die fachlichen Anforderungen, das Testen und alle inhaltlichen Entscheidungen
stammen vom Autor – Claude hat den Code geschrieben und technische Lösungsvorschläge
erarbeitet.

Der Entwicklungsprozess war iterativ: Anforderung → Umsetzung → Test → Feedback →
nächste Iteration. Wer sich für diesen Ansatz interessiert: der Entstehungsprozess ist
im Wesentlichen in der Konversationsgeschichte dokumentiert.

KI-gestützte Entwicklung wird hier bewusst transparent gemacht.
