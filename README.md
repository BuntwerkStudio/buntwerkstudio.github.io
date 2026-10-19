# BuntwerkStudio

Website von BuntwerkStudio: https://buntwerkstudio.github.io/

| Seite | Inhalt | Wichtigste Suchbegriffe |
|---|---|---|
| `index.html` | Startseite, Überblick | 3D-Druck Geschenk personalisiert, Münsterland |
| `schallwelle-anhaenger.html` | Klangform: Preise, Anlässe, Fragen | Schallwelle Schlüsselanhänger, Stimme als Anhänger, Herzschlag, Sprachnachricht |
| `wanderroute-3d-relief.html` | Wegform: Produkte, GPX-Anleitung, Fragen | Wanderroute als 3D-Relief, GPX 3D drucken, Geschenk Wanderer, Marathon |
| `buecher.html` | 6 Taschenbücher bei Amazon | Malbuch Kinder, Adventsmalbuch, Mandala Affirmationen |
| `empfehlungen.html` | Zubehör als Amazon-Partnerlinks | Kette, Schlüsselring, NFC-Sticker, Filament |
| `impressum.html`, `datenschutz.html` | Rechtliches | – |

## Aufgaben abarbeiten (Anleitung für Claude Code)

Dieser Abschnitt ist in allen drei Repositories gleich (Klangform, Wegform, Website). Er gilt, sobald Robert oder Christopher „Aufgaben“ sagt, z. B. „Arbeite die Aufgaben ab“, „Mach die Aufgaben“, „Neue Aufgabe: …“. Die Aufgabenliste steht in `AUFGABEN.md`.

### Schritt 1: Vorbereiten

1. `ARBEITSWEISE.md` und `CLAUDE.md` lesen. Dort stehen die festen Regeln.
2. Klangform und Wegform: auf den Branch `entwicklung` wechseln und den neuesten Stand holen (`git checkout entwicklung && git pull`). Website: Branch `main`.
3. `AUFGABEN.md` ganz lesen.

### Schritt 2: Auswählen und sortieren

1. Alle offenen Aufgaben (`- [ ]`) sammeln.
2. Aufteilen:
   - **Für Claude Code:** alles, was im Repository, im Browser (Chrome) oder in der Testumgebung erledigt werden kann.
   - **Für Robert/Christopher:** Probedrucke, Entscheidungen, Zugangsdaten, Zahlungen, Behörden. Diese nicht selbst machen. Am Ende als nummerierte Liste mit Klickpfaden nennen.
   - **Blockiert:** Aufgaben mit „erst nach …“, deren Voraussetzung noch offen ist. Überspringen, Grund notieren.
3. Reihenfolge der Aufgaben für Claude Code:
   1. Fehler auf der Live-Seite und alles zu Zahlung, Bestellung und Recht
   2. Aufgaben, von denen andere abhängen
   3. Aufgaben, die beide Tools betreffen: einmal bauen, in Klangform und Wegform gleich einsetzen
   4. neue Funktionen
   5. Texte, Design, Aufräumen
   Innerhalb einer Stufe gilt die Reihenfolge in `AUFGABEN.md`.
4. Aufgaben, die dieselben Dateien ändern, direkt nacheinander erledigen. Dann muss nur einmal gelesen und geprüft werden.

### Schritt 3: Plan zeigen

1. Eine Aufgabenliste (Task-Liste) anlegen: eine Zeile je Aufgabe, als Letztes „Alles prüfen“.
2. Dem Nutzer in 3 bis 6 Zeilen sagen, was jetzt erledigt wird, was übersprungen wird und warum. Dann sofort anfangen, ohne auf ein „Ok“ zu warten.
3. Rückfragen nur bei echten Entscheidungen, zum Beispiel Preis, Rechtstext, Geld, etwas nicht Umkehrbares. Alle Fragen in einer Nachricht sammeln. Antwortet niemand, die vernünftigste Annahme nehmen, sie in `AUFGABEN.md` notieren und weiterarbeiten. Nicht Umkehrbares wird dann nicht gemacht.

### Schritt 4: Umsetzen (je Aufgabe)

1. Erst die betroffenen Dateien lesen, dann in wenigen großen Schritten ändern.
2. Gemeinsame Dateien (Liste in `ARBEITSWEISE.md`, Abschnitt 5) in Klangform und Wegform gleich ändern und mit `cmp` vergleichen.
3. Ändert sich ein Ablauf, Preis oder eine Regel: `CLAUDE.md`, `ARBEITSWEISE.md` und `README.md` im selben Commit anpassen.
4. Bestellcodes, die Kunden schon haben, müssen gültig bleiben. Ändert sich die Geometrie, die Code-Version erhöhen.

### Schritt 5: Prüfen (je Aufgabe)

1. Alle Tests: `for t in tests/*.test.mjs; do node "$t" || echo "FEHLER: $t"; done`. Wegform: `tests/geometrie.test.mjs` dauert etwa 6 Minuten, nicht abbrechen; `tests/gelaende.test.mjs` braucht Internet; fehlt es, die Aufgabe als „ungeprüft ohne Netz“ melden.
2. Ändert sich die Seite: Testumgebung starten (`node tests/zahlung-vorschau.mjs`, Wegform `PREIS=4 node tests/zahlung-vorschau.mjs`, `DRUCK=1` für Gedrucktes; Website `python3 -m http.server 8000`) und mit Playwright durchklicken. Bildschirmfotos hell, dunkel und bei 390 px Breite ansehen.
3. Fehler sofort reparieren und erneut prüfen. Nach 3 erfolglosen Versuchen: Änderung zurücknehmen, die Aufgabe als blockiert markieren und den Grund notieren, mit der nächsten Aufgabe weitermachen.

### Schritt 6: Abhaken und sichern (je Aufgabe)

1. In `AUFGABEN.md`: `- [ ]` → `- [x]`, dahinter Datum und ein Satz zum Ergebnis.
2. Ein Commit je Aufgabe mit deutscher Nachricht, die mit der Aufgabennummer anfängt (z. B. `B3: …`). Werkstatt-Code geändert: `[werkstatt]` in die Nachricht.
3. Klangform und Wegform: nur auf `entwicklung` pushen. Das kostet keine Netlify-Credits. Website: auf `main` pushen, das kostet nichts.

### Schritt 7: Abschluss

1. Alle Tests in allen geänderten Repositories noch einmal laufen lassen.
2. Kurze Rückmeldung an den Nutzer:
   1. erledigt (je Aufgabe ein Satz)
   2. für Robert/Christopher (nummerierte Schritte mit genauen Klickpfaden)
   3. blockiert oder offen, mit Grund
3. Fragen, ob veröffentlicht werden soll. Klangform und Wegform kommen **nur** auf `main`, wenn Robert oder Christopher deutlich „veröffentlichen“, „live stellen“ oder „push auf main“ sagt. Dann einmal für alles: `entwicklung` in `main` mergen, pushen, in Netlify auf „Published“ prüfen, kurz live testen. Vorher sagen, ob der Build Credits kostet (15 je Projekt; reine Doku-Änderungen kosten nichts).

### Neue Aufgaben aufnehmen

Sagt jemand „Neue Aufgabe: …“:

1. In `AUFGABEN.md` eintragen, in der passenden Phase mit nächster freier Nummer: A = Robert/Christopher, B = Claude Code, C = später.
2. Bei größeren Aufgaben einen Auftragstext darunter schreiben (wie bei den bestehenden Aufgaben).
3. Betrifft die Aufgabe beide Tools, in beiden `AUFGABEN.md` eintragen.
4. Danach abarbeiten wie oben, außer der Nutzer sagt „nur notieren“.

### Auftrag zum Kopieren

Diesen Text in Claude Code (claude.ai/code) einfügen:

```
Arbeite die Aufgaben ab. Lies zuerst ARBEITSWEISE.md, CLAUDE.md und in der README.md den Abschnitt „Aufgaben abarbeiten“ und halte dich genau an die Schritte 1 bis 7. Repositories: BuntwerkStudio/Klangform, BuntwerkStudio/tracks-and-trails, BuntwerkStudio/buntwerkstudio.github.io. Nichts auf main von Klangform oder Wegform pushen, bis ich „veröffentlichen“ sage.
```

## Was ihr selbst tun müsst

Die gleichen Punkte stehen mit Status in `AUFGABEN.md`.

1. **Amazon-Partner-ID:** erledigt (18.10.2026, `affiliatesy0e-21` in `js/partner.js`).
2. **Website im PartnerNet hinterlegen:** erledigt (19.10.2026). partnernet.amazon.de → Konto → „Konto-Einstellungen“ → „Websites und mobile Apps bearbeiten“ → `https://buntwerkstudio.github.io` hinzufügen. Amazon prüft das Konto erst nach den ersten 3 Verkäufen innerhalb von 180 Tagen.
3. **Google Search Console:** search.google.com/search-console → „Property hinzufügen“ → URL-Präfix `https://buntwerkstudio.github.io/` → Bestätigung per HTML-Tag (Claude baut den Tag ein) → danach „Sitemaps“ → `sitemap.xml` einreichen. Gleiches bei Bing Webmaster Tools (Import aus Google geht mit einem Klick).
4. **Zurückverlinken:** In Klangform und Wegform im Fuß einen Link auf https://buntwerkstudio.github.io/ setzen, in den KDP-Büchern (Impressumsseite) und auf der Amazon-Autorenseite (author.amazon.de) ebenfalls. Links von euren eigenen Seiten helfen Google, die Seite schnell zu finden.
5. **Neue Bücher:** Neue Titel aus dem KDP-Bücherregal Claude nennen. Claude holt Umschlag und ASIN und baut sie ein.
6. **Eigene Domain (optional, empfohlen):** z. B. buntwerkstudio.de. In GitHub unter Settings → Pages → „Custom domain“ eintragen, beim Domain-Anbieter die DNS-Einträge von GitHub setzen. Dann Impressum, Datenschutz und Canonical-Adressen anpassen lassen.
7. **Rechtstexte prüfen lassen**, zusammen mit Klangform und Wegform (siehe `RECHTLICHES.md` in Klangform).

## Ändern

Texte, Bücher und Empfehlungen stehen in `tools/seiten-bauen.py`. Nach einer Änderung `python3 tools/seiten-bauen.py` ausführen und alles committen.
