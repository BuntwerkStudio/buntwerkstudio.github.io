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

## Was ihr selbst tun müsst

1. **Amazon-Partner-ID eintragen:** In `js/partner.js` bei `AMAZON_TAG` eure Tracking-ID eintragen (z. B. `'buntwerk-21'`), oder Claude die ID schicken.
2. **Website im PartnerNet hinterlegen:** partnernet.amazon.de → Konto → „Konto-Einstellungen“ → „Websites und mobile Apps bearbeiten“ → `https://buntwerkstudio.github.io` hinzufügen. Amazon prüft das Konto erst nach den ersten 3 Verkäufen innerhalb von 180 Tagen.
3. **Google Search Console:** search.google.com/search-console → „Property hinzufügen“ → URL-Präfix `https://buntwerkstudio.github.io/` → Bestätigung per HTML-Tag (Claude baut den Tag ein) → danach „Sitemaps“ → `sitemap.xml` einreichen. Gleiches bei Bing Webmaster Tools (Import aus Google geht mit einem Klick).
4. **Zurückverlinken:** In Klangform und Wegform im Fuß einen Link auf https://buntwerkstudio.github.io/ setzen, in den KDP-Büchern (Impressumsseite) und auf der Amazon-Autorenseite (author.amazon.de) ebenfalls. Links von euren eigenen Seiten helfen Google, die Seite schnell zu finden.
5. **Neue Bücher:** Neue Titel aus dem KDP-Bücherregal Claude nennen. Claude holt Umschlag und ASIN und baut sie ein.
6. **Eigene Domain (optional, empfohlen):** z. B. buntwerkstudio.de. In GitHub unter Settings → Pages → „Custom domain“ eintragen, beim Domain-Anbieter die DNS-Einträge von GitHub setzen. Dann Impressum, Datenschutz und Canonical-Adressen anpassen lassen.
7. **Rechtstexte prüfen lassen**, zusammen mit Klangform und Wegform (siehe `RECHTLICHES.md` in Klangform).

## Ändern

Texte, Bücher und Empfehlungen stehen in `tools/seiten-bauen.py`. Nach einer Änderung `python3 tools/seiten-bauen.py` ausführen und alles committen.
