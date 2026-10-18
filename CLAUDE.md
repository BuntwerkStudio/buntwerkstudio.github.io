# Projekt: BuntwerkStudio-Website

Startseite von BuntwerkStudio (Inhaber Robert Maximilian Maahs, Zum Fuchsbau 7, 48346 Ostbevern, buntwerkstudio@gmail.com, Kleinunternehmer nach § 19 UStG). Verlinkt die beiden 3D-Druck-Konfiguratoren Klangform und Wegform und die Bücher bei Amazon. Robert und Christopher sind keine Webentwickler: Schritte, die sie selbst ausführen müssen, als nummerierte Liste mit genauen Klickpfaden.

## Aufbau

- Statische Seite auf GitHub Pages, Adresse https://buntwerkstudio.github.io/ (Repository `BuntwerkStudio/buntwerkstudio.github.io`, öffentlich). Jeder Push auf `main` ist sofort online.
- Alle HTML-Seiten werden von `tools/seiten-bauen.py` erzeugt: `python3 tools/seiten-bauen.py`. Texte, Bücher (`BUCHLISTE`), Empfehlungen (`GRUPPEN`), Links (`KLANGFORM`, `WEGFORM`) dort ändern, nicht in den HTML-Dateien, und danach neu bauen.
- `css/style.css`: Design von Klangform/Wegform (gleiche Farben, Schrift, Knöpfe, Druckbett). `fonts/`: Fredoka 600 (OFL), lokal.
- `js/partner.js`: Amazon-Partner-Kennung `AMAZON_TAG`. Alle Links mit `data-amazon` bekommen sie angehängt.
- `img/buch-*.webp`: echte Umschläge von Amazon (302×390, lokal im Repository, vom Inhaber freigegeben 18.10.2026). Fehlt eins, zeichnet `tools/seiten-bauen.py` einen Ersatz-Umschlag als SVG. Neues Buch: Eintrag in `BUCHLISTE`, Umschlag als `img/buch-<datei>.webp` ablegen.
- `img/vorschau.png` (1200×630, Social Media), `img/logo.png`, `robots.txt`, `sitemap.xml`, `404.html`, `.nojekyll`.

## Feste Regeln

1. Keine externen Server, CDNs, Schriften, Bilder oder Widgets laden. Amazon-Bilder nur als Kopie im Repository, nie direkt von Amazon einbinden, keine Amazon-Widgets. Dann bleibt die Seite ohne Cookie-Banner. Jeder neue Dienst muss vorher in `datenschutz.html`.
2. Jeder Amazon-Link: `data-amazon`, `rel="sponsored noopener"`, Sternchen `*` am Linktext. Der Hinweis „Als Amazon-Partner verdienen wir an qualifizierten Verkäufen.“ bleibt im Fuß jeder Seite.
3. Preise nur aus der Konfiguration von Klangform (`js/config.js`) übernehmen. Wegform-Preise sind noch Platzhalter und werden nicht genannt.
4. Texte auf Deutsch, Leser mit „du“, kurze klare Sätze ohne Werbefloskeln.
5. Klangform und Wegform werden hier nur verlinkt, ihre Repositories nicht ändern.
6. Nach Änderungen an Produkten: Seiten neu bauen, `sitemap.xml` (`lastmod`) prüfen.

## Prüfen

`python3 -m http.server 8000`, dann `http://localhost:8000` öffnen, hell, dunkel und Handybreite ansehen.
