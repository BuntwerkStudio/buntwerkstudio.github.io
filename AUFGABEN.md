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
- [ ] **B4 Rücklink im Fuß von Klangform und Wegform** auf https://buntwerkstudio.github.io/ (auf `entwicklung`, mit der nächsten Veröffentlichung live).
- [ ] **B5 Neue Bücher** einbauen, sobald Robert Titel nennt: Umschlag und ASIN aus dem KDP-Bücherregal (Chrome), Eintrag in `BUCHLISTE`, neu bauen.
