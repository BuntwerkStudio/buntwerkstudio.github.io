# Aufgaben

Status: `[ ]` offen, `[x]` erledigt. So wird die Liste abgearbeitet: `README.md`, Abschnitt „Aufgaben abarbeiten“.

## Phase A – Robert und Christopher

- [x] **A1 Amazon-Partner-ID** (18.10.2026): `affiliatesy0e-21` in `js/partner.js`.
- [x] **A2 Website im PartnerNet hinterlegen** (19.10.2026, geprüft: steht in der Liste neben Pinterest): partnernet.amazon.de → Konto → „Konto-Einstellungen“ → „Websites und mobile Apps bearbeiten“ → `https://buntwerkstudio.github.io` hinzufügen.
- [ ] **A3 Google Search Console:** search.google.com/search-console → „Property hinzufügen“ → URL-Präfix `https://buntwerkstudio.github.io/` → Bestätigung „HTML-Tag“ wählen und den Tag Claude schicken (dann B1).
- [ ] **A4 Zurückverlinken:** in den KDP-Büchern (Impressumsseite) und auf der Amazon-Autorenseite (author.amazon.de) auf https://buntwerkstudio.github.io/ verlinken.
- [ ] **A5 Eigene Domain (optional),** z. B. buntwerkstudio.de. Danach B2.
- [ ] **A6 Rechtstexte prüfen lassen,** zusammen mit Klangform und Wegform.
- [ ] **A7 Neue Adresse nach dem Umzug** an Claude geben (dann B3).

## Phase B – Aufgaben für Claude Code

- [ ] **B1 Bestätigungs-Tag der Search Console einbauen** (erst nach A3): Tag in `tools/seiten-bauen.py` in den Kopf von `index.html`, neu bauen, pushen. Danach Robert sagen: in der Search Console „Bestätigen“ klicken, unter „Sitemaps“ `sitemap.xml` einreichen.
- [ ] **B2 Eigene Domain einrichten** (erst nach A5): `CNAME`, Canonical-Adressen, `sitemap.xml`, `robots.txt`, Impressum, Datenschutz, Links in Klangform und Wegform.
- [ ] **B3 Neue Adresse überall eintragen** (erst nach A7): Website, Klangform und Wegform (Impressum, AGB, Datenschutz, Widerruf, Bestellbestätigungen in `js/kauf.js`, `ARBEITSWEISE.md`). Klangform/Wegform nur auf `entwicklung`, dann fragen, ob veröffentlicht werden soll.
- [x] **B4 Rücklink im Fuß von Klangform und Wegform** (19.10.2026 erledigt, liegt auf `entwicklung`, kommt mit der nächsten Veröffentlichung live; dazu die BuntwerkStudio-Kopfzeile oben) auf https://buntwerkstudio.github.io/ (auf `entwicklung`, mit der nächsten Veröffentlichung live).
- [ ] **B5 Neue Bücher** einbauen, sobald Robert Titel nennt: Umschlag und ASIN aus dem KDP-Bücherregal (Chrome), Eintrag in `BUCHLISTE`, neu bauen.
- [x] **B6 Schalter Hell/Dunkel in der Kopfzeile** (24.10.2026 erledigt, gleich wie Klangform B12 und Wegform B18: `js/thema.js` im Kopf jeder Seite aus `tools/seiten-bauen.py`, Stufen Automatisch → Hell → Dunkel, gemerkt im Browser. Liegt auf dem Branch `entwicklung`, kommt zusammen mit Klangform und Wegform auf `main`, wenn Robert „veröffentlichen“ sagt.)
- [x] **B7 Englische Seiten** (24.10.2026 erledigt, = Klangform B13 / Wegform B19: `tools/seiten-bauen.py` erzeugt `en/` mit Start, Klangform, Wegform, Bücher und Empfehlungen, 404 zweisprachig; Schalter „DE | EN“ in der Kopfzeile, `js/sprache.js` (Vorschlag nach Browsersprache, keine Umleitung, Wahl in localStorage `buntwerk-sprache`); hreflang de/en/x-default und Sitemap; Rechtstexte nur auf Deutsch verlinkt; Versand-Hinweis „within Germany only“; Amazon-Hinweis englisch und deutsch; Prüfung `python3 tools/sprache-pruefen.py`. Liegt auf dem Branch `entwicklung`, kommt mit „veröffentlichen“ auf `main`.)
- [ ] **B8 Empfehlungen: Aufbewahrungsboxen für Filament bei „Für Selbstdrucker“** (angelegt am 24.10.2026 von Robert, Gruppe am selben Tag von Robert auf „Für Selbstdrucker“ geändert). Link von Robert: https://link.amazon/B0d7ytyCQ
  1. Den Kurzlink in Chrome öffnen und die Produktseite auf amazon.de ansehen: ASIN (10 Zeichen, steht in der Adresse nach `/dp/`) und Produktname notieren. Ist es kein amazon.de-Artikel oder steht dort eine fremde Partner-Kennung (`tag=` in der Adresse), Robert fragen. Den Kurzlink selbst nicht auf die Seite schreiben.
  2. In `tools/seiten-bauen.py` in `GRUPPEN` bei „Für Selbstdrucker“ eine vierte Karte ergänzen: Titel „Aufbewahrungsbox für Filament“, ein kurzer Satz (z. B. „Hält dein Filament trocken und staubfrei, damit es sauber druckt.“), ohne Werbefloskeln. Genauso auf Englisch in `GRUPPEN_EN` bei der englischen Gruppe für Selbstdrucker (z. B. „Filament storage box“, „Keeps your filament dry and dust-free for clean prints.“), gleicher amazon.de-Link.
  3. Die anderen Karten verlinken auf eine Amazon-Suche (`amazon_suche`). Diese Karte verlinkt direkt auf den Artikel: `https://www.amazon.de/dp/<ASIN>` mit `data-amazon`, `rel="sponsored noopener"` und Sternchen (wie `partnerlink`), die Partner-Kennung hängt `js/partner.js` an. Dafür `GRUPPEN`/`gruppen_html()` so erweitern, dass ein Eintrag statt eines Suchbegriffs auch eine ASIN haben kann. Kein Produktbild und kein Preis von Amazon einbinden (Regel 1).
  4. Neu bauen (`python3 tools/seiten-bauen.py`), `sitemap.xml` (`lastmod` der Empfehlungsseite) prüfen, deutsch und englisch, hell, dunkel und 390 px ansehen, Link öffnen und prüfen, dass `tag=affiliatesy0e-21` angehängt ist.
  5. Auf dem Branch `entwicklung` committen (dort liegen schon B6 und B7), mit der nächsten Veröffentlichung nach `main`.
