#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# embed_fonts.sh – Google Fonts herunterladen und in lektionar.html einbetten
#
# Voraussetzungen: curl, base64, python3 (alle auf Debian vorinstalliert)
#
# Aufruf:
#   chmod +x embed_fonts.sh
#   ./embed_fonts.sh lektionar.html
#
# Ergebnis:
#   lektionar_offline.html  (identisch, aber ohne Google-Fonts-Anfragen)
# ═══════════════════════════════════════════════════════════════════════════

INPUT="${1:-lektionar.html}"
OUTPUT="${INPUT%.html}_offline.html"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
TMPDIR=$(mktemp -d)

echo "Lade Font-CSS von Google..."
CSS=$(curl -s \
  "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" \
  -H "User-Agent: $UA")

if [ -z "$CSS" ]; then
  echo "FEHLER: Font-CSS konnte nicht geladen werden"
  exit 1
fi

# Font-URLs extrahieren
URLS=$(echo "$CSS" | grep -oP 'https://[^)]+\.woff2')
echo "Gefundene Font-Dateien:"
echo "$URLS" | while read url; do echo "  $url"; done

# Jeden Font herunterladen und als Base64 kodieren
echo ""
echo "Lade Fonts herunter..."

# Python übernimmt das Einbetten (einfacher als bash)
python3 - "$CSS" "$INPUT" "$OUTPUT" "$TMPDIR" << 'PYEOF'
import sys, re, os, urllib.request, base64

css_text = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]
tmpdir = sys.argv[4]

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"

# Alle woff2-URLs aus CSS extrahieren
urls = re.findall(r'(https://[^)]+\.woff2)', css_text)
print(f"  {len(urls)} Font-Dateien gefunden")

# Jeden Font downloaden und in CSS ersetzen
for url in urls:
    print(f"  Lade: {url[:60]}...")
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    data = urllib.request.urlopen(req).read()
    b64 = base64.b64encode(data).decode('ascii')
    data_uri = f"data:font/woff2;base64,{b64}"
    css_text = css_text.replace(url, data_uri)
    print(f"    → {len(data)//1024} KB eingebettet")

# @import in HTML durch eingebettetes CSS ersetzen
with open(input_file, encoding='utf-8') as f:
    html = f.read()

# Google Fonts @import ersetzen durch eingebettetes CSS
old_import = "@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');"
assert old_import in html, "FEHLER: @import nicht in HTML gefunden!"

html = html.replace(old_import, css_text)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nFertig!")
print(f"  Eingabe:  {input_file} ({os.path.getsize(input_file)//1024} KB)")
print(f"  Ausgabe:  {output_file} ({os.path.getsize(output_file)//1024} KB)")
print(f"  Keine externen Font-Anfragen mehr.")
PYEOF

# Temp aufräumen
rm -rf "$TMPDIR"
