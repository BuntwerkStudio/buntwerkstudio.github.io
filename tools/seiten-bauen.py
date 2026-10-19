#!/usr/bin/env python3
"""Erzeugt die statischen Seiten für buntwerkstudio.github.io (einmalig, Ergebnis wird committet)."""
import json, math, os, random, tempfile

ZIEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://buntwerkstudio.github.io/'
KLANGFORM = 'https://klangform.netlify.app/'
WEGFORM = 'https://tracks-and-trails.netlify.app/'
STAND = '18.10.2026'
# Wie SHOP.druckVerfuegbar in Klangform (js/config.js). False = gedruckte Teile ausverkauft, nur STL-Datei bestellbar.
DRUCK_VERFUEGBAR = False
HINWEIS_AUSVERKAUFT = '' if DRUCK_VERFUEGBAR else '<div class="kasten"><p><strong>Gerade ausverkauft:</strong> Fertig gedruckte Teile können wir im Moment nicht liefern. Die Druckdatei (STL) zum Selbstdrucken bekommst du weiter für 2 € per E-Mail.</p></div>'

# ---------------------------------------------------------------- Grafiken

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#273134"/>'
        '<rect x="6" y="13" width="3" height="6" rx="1.5" fill="#3a6ea5"/>'
        '<rect x="11" y="8" width="3" height="16" rx="1.5" fill="#4f6e45"/>'
        '<rect x="16" y="5" width="3" height="22" rx="1.5" fill="#c9a23f"/>'
        '<rect x="21" y="10" width="3" height="12" rx="1.5" fill="#b8312f"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E"
           "%3Crect width=%2232%22 height=%2232%22 rx=%228%22 fill=%22%23273134%22/%3E"
           "%3Crect x=%226%22 y=%2213%22 width=%223%22 height=%226%22 rx=%221.5%22 fill=%22%233a6ea5%22/%3E"
           "%3Crect x=%2211%22 y=%228%22 width=%223%22 height=%2216%22 rx=%221.5%22 fill=%22%234f6e45%22/%3E"
           "%3Crect x=%2216%22 y=%225%22 width=%223%22 height=%2222%22 rx=%221.5%22 fill=%22%23c9a23f%22/%3E"
           "%3Crect x=%2221%22 y=%2210%22 width=%223%22 height=%2212%22 rx=%221.5%22 fill=%22%23b8312f%22/%3E%3C/svg%3E")

random.seed(7)
WELLE = [0.18, 0.32, 0.55, 0.78, 0.62, 0.9, 1.0, 0.7, 0.85, 0.52, 0.66, 0.4, 0.58, 0.3, 0.22, 0.36, 0.16]


def anhaenger(x, y, breite, hoehe, farbe, drehung=0, schatten=True):
    """Schallwellen-Schlüsselanhänger Form „Balken“ (Draufsicht)."""
    n = len(WELLE)
    oese = hoehe * 0.42
    teile = []
    innen_x = x + oese * 1.25
    schritt = (breite - oese * 1.5) / n
    bw = schritt * 0.62
    for i, w in enumerate(WELLE):
        h = max(hoehe * 0.16, hoehe * w)
        bx = innen_x + i * schritt
        teile.append(f'<rect x="{bx:.1f}" y="{y + (hoehe - h) / 2:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="{bw / 2:.1f}"/>')
    # Steg durch die Mitte und Öse
    steg = f'<rect x="{x + oese * .6:.1f}" y="{y + hoehe / 2 - hoehe * .08:.1f}" width="{breite - oese * .6:.1f}" height="{hoehe * .16:.1f}" rx="{hoehe * .08:.1f}"/>'
    ring = (f'<circle cx="{x + oese * .55:.1f}" cy="{y + hoehe / 2:.1f}" r="{oese * .55:.1f}"/>')
    loch = f'<circle cx="{x + oese * .55:.1f}" cy="{y + hoehe / 2:.1f}" r="{oese * .26:.1f}" fill="#273134"/>'
    filt = ' filter="url(#schatten)"' if schatten else ''
    cx, cy = x + breite / 2, y + hoehe / 2
    return (f'<g transform="rotate({drehung} {cx:.0f} {cy:.0f})"{filt}><g fill="{farbe}">{ring}{steg}{"".join(teile)}</g>{loch}</g>')


def relief(cx, cy, r, sechs=True):
    """Wegform-Relief in Höhenstufen (Draufsicht) mit roter Route."""
    def umriss(rr):
        pts = []
        for k in range(6):
            a = math.radians(60 * k + 30)
            pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
        return ' '.join(pts)

    def blob(mx, my, rr, phase, wellig=0.18, n=64):
        pts = []
        for k in range(n):
            a = 2 * math.pi * k / n
            f = 1 + wellig * math.sin(3 * a + phase) + wellig * .6 * math.sin(5 * a + phase * 1.7)
            pts.append(f'{mx + rr * f * math.cos(a):.1f},{my + rr * .82 * f * math.sin(a):.1f}')
        return ' '.join(pts)

    stufen = [('#5f7f4f', 1.0), ('#7d9a5d', .74), ('#c8b48a', .52), ('#9a9a92', .33), ('#f1f0ea', .16)]
    teile = [f'<clipPath id="sechs"><polygon points="{umriss(r)}"/></clipPath>']
    teile.append(f'<polygon points="{umriss(r)}" fill="#4f6e45" filter="url(#schatten)"/>')
    g = ['<g clip-path="url(#sechs)">']
    for i, (farbe, f) in enumerate(stufen):
        g.append(f'<polygon points="{blob(cx + r * .08, cy - r * .05, r * f * 1.05, i * .9 + .4)}" fill="{farbe}"/>')
    # zweiter Gipfel
    g.append(f'<polygon points="{blob(cx - r * .48, cy + r * .38, r * .3, 2.1)}" fill="#7d9a5d"/>')
    g.append(f'<polygon points="{blob(cx - r * .48, cy + r * .38, r * .16, 3.1)}" fill="#c8b48a"/>')
    g.append('</g>')
    teile += g
    route = [(-.82, .55), (-.62, .5), (-.5, .3), (-.3, .26), (-.18, .05), (-.02, .1), (.08, -.04),
             (.2, -.2), (.34, -.12), (.44, -.3), (.62, -.36), (.78, -.52)]
    d = 'M' + ' L'.join(f'{cx + px * r:.1f},{cy + py * r:.1f}' for px, py in route)
    teile.append(f'<path d="{d}" fill="none" stroke="#c0392b" stroke-width="{r * .045:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    teile.append(f'<polygon points="{umriss(r)}" fill="none" stroke="#2e4229" stroke-width="2"/>')
    return ''.join(teile)


def buch(x, y, b, h, farbe, drehung=0):
    cx, cy = x + b / 2, y + h / 2
    return (f'<g transform="rotate({drehung} {cx:.0f} {cy:.0f})" filter="url(#schatten)">'
            f'<rect x="{x}" y="{y}" width="{b}" height="{h}" rx="4" fill="{farbe}"/>'
            f'<rect x="{x}" y="{y}" width="{b * .08:.1f}" height="{h}" rx="2" fill="#000" opacity=".22"/>'
            f'<rect x="{x + b * .22:.1f}" y="{y + h * .16:.1f}" width="{b * .62:.1f}" height="{h * .05:.1f}" rx="2" fill="#f5f7f4" opacity=".9"/>'
            f'<rect x="{x + b * .22:.1f}" y="{y + h * .25:.1f}" width="{b * .4:.1f}" height="{h * .035:.1f}" rx="2" fill="#f5f7f4" opacity=".6"/>'
            f'<g transform="translate({x + b * .2:.1f} {y + h * .55:.1f}) scale({b / 150:.3f})" fill="#c9a23f">'
            + ''.join(f'<rect x="{i * 9}" y="{30 - 30 * w}" width="5" height="{60 * w:.1f}" rx="2.5"/>' for i, w in enumerate(WELLE[2:13])) +
            '</g></g>')


DEFS = ('<defs><filter id="schatten" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="9" stdDeviation="8" flood-color="#000" flood-opacity=".45"/></filter></defs>')


def svg(inhalt, box='0 0 500 400', titel=''):
    t = f'<title>{titel}</title>' if titel else ''
    return f'<svg viewBox="{box}" role="img" xmlns="http://www.w3.org/2000/svg">{t}{DEFS}{inhalt}</svg>'


HELD_BILD = svg(relief(205, 190, 128) + anhaenger(268, 268, 190, 62, '#c9a23f', -8) + buch(372, 60, 92, 136, '#3a6ea5', 7),
                titel='3D-gedrucktes Wanderrelief, Schallwellen-Anhänger und Buch auf einem Druckbett')
KLANG_BILD = svg(anhaenger(95, 80, 280, 90, '#c9a23f', -6) + anhaenger(45, 235, 210, 66, '#3a6ea5', 4) + anhaenger(285, 250, 160, 52, '#ecebe6', -10),
                 titel='Schlüsselanhänger in Form einer Schallwelle')
WEG_BILD = svg(relief(250, 205, 165), titel='Relief einer Wanderroute in Höhenstufen mit roter Route')
BUCH_BILD = svg(buch(110, 70, 130, 190, '#b8312f', -6) + buch(260, 80, 130, 190, '#3a6ea5', 5), titel='Bücher von BuntwerkStudio')

# ---------------------------------------------------------------- Rahmen

MENUE = [('index.html', 'Start'), ('schallwelle-anhaenger.html', 'Klangform'), ('wanderroute-3d-relief.html', 'Wegform'),
         ('buecher.html', 'Bücher'), ('empfehlungen.html', 'Empfehlungen')]


def kopf(datei):
    links = ''.join(f'<a href="{d if d != "index.html" else "./"}"{" aria-current=\"page\"" if d == datei else ""}>{n}</a>' for d, n in MENUE)
    return (f'<header class="huelle kopfzeile"><a class="wortmarke" href="./" aria-label="BuntwerkStudio – Startseite">{LOGO}'
            f'<span>Buntwerk<b>Studio</b></span></a><nav class="menue" aria-label="Hauptmenü">{links}</nav></header>')


FUSS = f'''<footer class="fuss"><div class="huelle">
  <div class="fuss-raster">
    <div><a class="wortmarke" href="./">{LOGO}<span>Buntwerk<b>Studio</b></span></a>
      <p>3D-gedruckte Erinnerungsstücke und Bücher aus Ostbevern im Münsterland.</p></div>
    <div><h2>3D-Druck</h2><ul>
      <li><a href="schallwelle-anhaenger.html">Klangform: Schallwelle</a></li>
      <li><a href="wanderroute-3d-relief.html">Wegform: Wanderroute</a></li>
      <li><a href="{KLANGFORM}" rel="noopener">Klangform gestalten</a></li>
      <li><a href="{WEGFORM}" rel="noopener">Wegform gestalten</a></li></ul></div>
    <div><h2>Mehr</h2><ul>
      <li><a href="buecher.html">Bücher</a></li>
      <li><a href="empfehlungen.html">Empfehlungen</a></li>
      <li><a href="mailto:buntwerkstudio@gmail.com">E-Mail schreiben</a></li></ul></div>
    <div><h2>Rechtliches</h2><ul>
      <li><a href="impressum.html">Impressum</a></li>
      <li><a href="datenschutz.html">Datenschutz</a></li>
      <li><a href="datenschutz.html#partnerprogramm">Hinweis zu Partnerlinks</a></li></ul></div>
  </div>
  <p class="klein">Als Amazon-Partner verdienen wir an qualifizierten Verkäufen. Mit * markierte Links sind Partnerlinks: Kaufst du darüber ein, erhalten wir eine kleine Provision. Für dich ändert sich der Preis nicht.</p>
  <p class="klein">© 2026 BuntwerkStudio · Inhaber Robert Maximilian Maahs · Kleinunternehmer nach § 19 UStG</p>
</div></footer>'''


def seite(datei, titel, beschreibung, inhalt, ld=None, index=True, og_typ='website'):
    url = BASIS + ('' if datei == 'index.html' else datei)
    robots = 'index, follow, max-image-preview:large' if index else 'noindex, follow'
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>' for x in (ld or []))
    html = f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; form-action 'none'; base-uri 'self'">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{titel}</title>
  <meta name="description" content="{beschreibung}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_typ}">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="BuntwerkStudio">
  <meta property="og:title" content="{titel}">
  <meta property="og:description" content="{beschreibung}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASIS}img/vorschau.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#273134">
  <link rel="icon" href="{FAVICON}">
  <link rel="preload" href="fonts/fredoka-600.woff" as="font" type="font/woff" crossorigin>
  <link rel="stylesheet" href="css/style.css">
  {lds}
</head>
<body>
{kopf(datei)}
{inhalt}
{FUSS}
<script src="js/partner.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(ZIEL, datei), 'w', encoding='utf-8') as f:
        f.write(html)


def kruemel(*teile):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASIS + ('' if d == 'index.html' else d)} for i, (d, n) in enumerate(teile)]}


def fragen_ld(paare):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f, "acceptedAnswer": {"@type": "Answer", "text": a}} for f, a in paare]}


def fragen_html(paare):
    return '<div class="fragen">' + ''.join(f'<details><summary>{f}</summary><p>{a}</p></details>' for f, a in paare) + '</div>'


def amazon_suche(begriff):
    from urllib.parse import quote_plus
    return f'https://www.amazon.de/s?k={quote_plus(begriff)}'


def partnerlink(href, text, klasse='zweit'):
    return f'<a class="{klasse}" href="{href}" data-amazon rel="sponsored noopener" target="_blank">{text}*</a>'


ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": BASIS + "#organisation", "name": "BuntwerkStudio",
       "url": BASIS, "logo": BASIS + "img/logo.png", "email": "buntwerkstudio@gmail.com",
       "founder": {"@type": "Person", "name": "Robert Maximilian Maahs"},
       "address": {"@type": "PostalAddress", "streetAddress": "Zum Fuchsbau 7", "postalCode": "48346", "addressLocality": "Ostbevern",
                   "addressRegion": "Nordrhein-Westfalen", "addressCountry": "DE"},
       "brand": [{"@type": "Brand", "name": "Klangform"}, {"@type": "Brand", "name": "Wegform"}],
       "sameAs": [KLANGFORM, WEGFORM]}

# ---------------------------------------------------------------- Startseite

def collage(namen):
    teile = ''.join(f'<img src="img/buch-{n}.webp" alt="" width="302" height="390" class="dreh{i}">' for i, (n, d) in enumerate(namen))
    return f'<div class="bett collage" aria-hidden="true">{teile}</div>'




START = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">3D-Druck aus dem Münsterland</p>
    <h1>Erinnerungen, die man anfassen kann</h1>
    <p class="einleitung">Wir drucken deine Stimme als Schallwelle und deine Wanderung als Relief mit echtem Gelände. Du gestaltest im Browser, wir drucken in Ostbevern und Ascheberg.</p>
    <div class="knoepfe">
      <a class="haupt" href="schallwelle-anhaenger.html">Schallwelle als Anhänger <span class="pfeil" aria-hidden="true">→</span></a>
      <a class="zweit" href="wanderroute-3d-relief.html">Wanderroute als Relief</a>
    </div>
    <div class="streifen" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  </div>
  <div class="bett">{HELD_BILD}</div>
</section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Unsere zwei Werkstätten</p>
    <h2>Zwei Konfiguratoren, ein Studio</h2>
    <p>Beide laufen komplett in deinem Browser. Deine Aufnahme und deine Route verlassen dein Gerät nicht. Du siehst sofort eine Vorschau und den Preis.</p></div>
  <div class="karten">
    <article class="karte karte-oben gold">
      <div class="bett">{KLANG_BILD}</div>
      <div class="karte-text">
        <p class="marke">Klangform</p>
        <h3>Deine Stimme als Schlüsselanhänger, Schmuck oder Aufsteller</h3>
        <p>Nimm ein „Ich liebe dich“, ein Lachen oder einen Herzschlag auf. Daraus wird ein massives Teil in der Form deiner Schallwelle. Ab <span class="preis">6 €</span>.{'' if DRUCK_VERFUEGBAR else ' Gedruckte Teile sind gerade ausverkauft, die Druckdatei gibt es für 2 €.'}</p>
        <div class="knoepfe">
          <a class="haupt" href="{KLANGFORM}" rel="noopener">Klangform gestalten <span class="pfeil" aria-hidden="true">→</span></a>
          <a class="zweit" href="schallwelle-anhaenger.html">Mehr erfahren</a>
        </div>
      </div>
    </article>
    <article class="karte karte-oben gruen">
      <div class="bett">{WEG_BILD}</div>
      <div class="karte-text">
        <p class="marke">Wegform</p>
        <h3>Deine Wanderung als 3D-Relief mit echtem Gelände</h3>
        <p>Lade deine GPX- oder FIT-Datei von Garmin, Strava oder Komoot hoch. Wir drucken Berge, Täler und deine Route, auf Wunsch mit Höhenstufen in mehreren Farben.</p>
        <div class="knoepfe">
          <a class="haupt" href="{WEGFORM}" rel="noopener">Wegform gestalten <span class="pfeil" aria-hidden="true">→</span></a>
          <a class="zweit" href="wanderroute-3d-relief.html">Mehr erfahren</a>
        </div>
      </div>
    </article>
  </div>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">So einfach geht es</p><h2>In drei Schritten zu deinem Stück</h2></div>
  <ol class="ablauf">
    <li><h3>Gestalten</h3><p>Ton aufnehmen oder Route hochladen, dann Produkt, Form, Größe und Farbe wählen.</p></li>
    <li><h3>Bestellen</h3><p>Du schickst die Bestellung ab und bekommst von uns eine Bestätigung mit PayPal-Link oder Rechnung.</p></li>
    <li><h3>Auspacken</h3><p>Wir drucken dein Teil und verschicken es. Bei Klangform innerhalb von 7 Tagen nach Zahlungseingang.</p></li>
  </ol>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Geschenkideen</p><h2>Für wen?</h2>
    <p>Persönliche Geschenke, die es nur einmal gibt.</p></div>
  <ul class="chips">
    <li>Jahrestag und Valentinstag</li><li>Hochzeit: das Ja-Wort</li><li>Geburt: erster Herzschlag</li>
    <li>Oma und Opa: Stimme der Enkel</li><li>Wanderer und Bergsteiger</li><li>Läufer: Marathonstrecke</li>
    <li>Radfahrer: Alpenpass</li><li>Weihnachten</li><li>Erinnerung an einen geliebten Menschen</li>
  </ul>
</div></section>

<section class="abschnitt"><div class="huelle karten">
  <div>
    <p class="marke">Bücher</p><h2>Malbücher für Klein und Groß</h2>
    <p class="leise">Robert und Christopher haben Mal- und Skizzenbücher für Kinder ab 4 Jahren und Mandala-Malbücher mit Affirmationen gestaltet. Alle als Taschenbuch bei Amazon.</p>
    <div class="knoepfe"><a class="zweit" href="buecher.html">Zu den Büchern <span class="pfeil" aria-hidden="true">→</span></a></div>
  </div>
  @@COLLAGE@@
</div></section>
</main>'''

START = START.replace('@@COLLAGE@@', collage([('dino-skizzenbuch', -7), ('feen-skizzenbuch', 3), ('reichtum-wohlstand', 9)]))
seite('index.html', 'BuntwerkStudio – Schallwelle und Wanderroute als 3D-Druck',
      'Personalisierte 3D-Druck-Geschenke aus dem Münsterland: deine Stimme als Schallwellen-Anhänger (Klangform) und deine Wanderroute als 3D-Relief (Wegform). Dazu Malbücher für Kinder und Erwachsene.',
      START, ld=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "BuntwerkStudio", "url": BASIS, "inLanguage": "de-DE",
                       "publisher": {"@id": BASIS + "#organisation"}}])

# ---------------------------------------------------------------- Klangform

K_FRAGEN = [
    ('Was kann ich aufnehmen?', 'Alles, was einen Klang hat: einen Namen, ein „Ich liebe dich“, ein Lachen, einen Herzschlag aus dem Ultraschall-Video, eine Sprachnachricht oder ein paar Sekunden aus eurem Lied. 2 bis 5 Sekunden sind ideal.'),
    ('Kann ich eine Sprachnachricht oder ein Video verwenden?', 'Ja. Du kannst statt einer Aufnahme eine Audio- oder Videodatei hochladen, zum Beispiel eine gespeicherte Sprachnachricht oder ein Video vom Ultraschall. Danach wählst du den Ausschnitt.'),
    ('Wird meine Aufnahme hochgeladen?', 'Nein. Die Aufnahme wird nur in deinem Browser ausgewertet. Aus ihr entsteht eine Reihe von Zahlen für die Form. Aus diesen Zahlen lässt sich der Ton nicht wiederherstellen.'),
    ('Was kostet ein Schallwellen-Anhänger?', 'Ein Schlüsselanhänger kostet je nach Größe 7 bis 9 €, ein Kettenanhänger 7 €, Christbaumschmuck ab 6 €. Der Versand in Deutschland kostet 2,95 €. Alle Preise sind Endpreise.'),
    ('Wie lange dauert die Lieferung?', 'Wir drucken dein Teil und verschicken es innerhalb von 7 Tagen nach Zahlungseingang.' + ('' if DRUCK_VERFUEGBAR else ' Gerade sind gedruckte Teile ausverkauft. Die Druckdatei kommt nach Zahlungseingang per E-Mail.')),
    ('Ist eine Kette oder ein Band dabei?', 'Nein. Kettenanhänger kommen ohne Kette, Lesezeichen und Christbaumschmuck ohne Band. Passende Ketten, Bänder und Schlüsselringe findest du auf unserer Seite mit Empfehlungen.'),
    ('Kann ich selbst drucken?', 'Ja. Du kannst statt des gedruckten Teils die STL-Datei für 2 € bestellen und sie auf deinem eigenen 3D-Drucker drucken.'),
]

PRODUKTE_K = [
    ('Schlüsselanhänger', 'Klein, Mittel, Groß', '7 € bis 9 €', 'Mit 5-mm-Öse für den Schlüsselring. 9 Formen von Balken bis Herz.'),
    ('Kettenanhänger', 'eine Größe', '7 €', 'Klein und leicht, mit 3-mm-Öse. Ohne Kette.'),
    ('Lesezeichen', '15 cm', '7 €', 'Plakette mit Schallwelle, auf Wunsch mit Name.'),
    ('Christbaumschmuck', 'Klein, Mittel', '6 € bis 8 €', 'Stern, Scheibe oder Herz zum Aufhängen.'),
    ('Untersetzer', '9,5 cm', '8 €', 'Für Tassen und Gläser.'),
    ('Tischaufsteller', '10, 14, 18 cm breit', '9,90 € bis 15,90 €', 'Skyline mit Steckfuß, auf Wunsch mit Name im Sockel.'),
    ('Ohrringe', 'ein Paar', 'bald', 'Sehr leicht, ohne Haken. Gerade noch nicht bestellbar.'),
    ('STL-Datei', '–', '2 €', 'Zum Selbstdrucken, kommt per E-Mail.'),
]

KLANG = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Klangform</p>
    <h1>Schallwelle als Schlüsselanhänger, Kette und Aufsteller</h1>
    <p class="einleitung">Nimm deine Stimme, ein Lachen oder einen Herzschlag auf. Daraus drucken wir ein Teil in der Form deiner Schallwelle. Ab 6 €, gedruckt im Münsterland.</p>
    <div class="knoepfe">
      <a class="haupt" href="{KLANGFORM}" rel="noopener">Jetzt Schallwelle gestalten <span class="pfeil" aria-hidden="true">→</span></a>
      <a class="zweit" href="#preise">Preise ansehen</a>
    </div>
    {HINWEIS_AUSVERKAUFT}
  </div>
  <div class="bett">{KLANG_BILD}<p class="unterschrift">Schlüsselanhänger, Form Balken. Jede Welle ist einzigartig.</p></div>
</section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">So funktioniert es</p><h2>Vom Ton zum Anhänger in zwei Minuten</h2></div>
  <ol class="ablauf">
    <li><h3>Ton aufnehmen</h3><p>Direkt im Browser aufnehmen oder eine Audio- oder Videodatei wählen. 2 bis 5 Sekunden reichen.</p></li>
    <li><h3>Form wählen</h3><p>Balken, Welle, Rund, Ring, Plakette, Herz, Stern, Scheibe, Unendlich oder Skyline. Dazu Größe und Farbe.</p></li>
    <li><h3>Bestellen</h3><p>Du bekommst einen Bestellcode und schickst die Bestellung ab. Wir drucken und verschicken.</p></li>
  </ol>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Anlässe</p><h2>Ein Geschenk, das nach dir klingt</h2>
    <p>Ein Schallwellen-Anhänger hält einen Moment fest, den man sonst nur hören kann.</p></div>
  <ul class="chips">
    <li>„Ich liebe dich“ zum Jahrestag</li><li>Das Ja-Wort zur Hochzeit</li><li>Herzschlag vom Ultraschall</li>
    <li>Der Name des Kindes</li><li>Das erste „Mama“ oder „Papa“</li><li>Lachen der Enkel für Oma und Opa</li>
    <li>Sprachnachricht eines geliebten Menschen</li><li>Ausschnitt aus eurem Lied</li><li>Christbaumschmuck mit Kinderstimme</li>
  </ul>
</div></section>

<section class="abschnitt" id="preise"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Produkte und Preise</p><h2>Was wir aus deiner Schallwelle drucken</h2>
    <p>Alle Teile sind massiv, aus einem Stück und in einer Farbe gedruckt, ohne Kleinteile. Endpreise, als Kleinunternehmer berechnen wir keine Umsatzsteuer. Versand in Deutschland 2,95 €.</p></div>
  <div class="tabelle-huelle"><table>
    <thead><tr><th scope="col">Produkt</th><th scope="col">Größe</th><th scope="col">Preis</th><th scope="col">Details</th></tr></thead>
    <tbody>{''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td class="preis">{c}</td><td>{d}</td></tr>' for a, b, c, d in PRODUKTE_K)}</tbody>
  </table></div>
  {HINWEIS_AUSVERKAUFT}
  <div class="knoepfe"><a class="haupt" href="{KLANGFORM}" rel="noopener">Zu Klangform <span class="pfeil" aria-hidden="true">→</span></a></div>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Datenschutz</p><h2>Deine Aufnahme bleibt bei dir</h2>
    <p>Klangform braucht keinen Server für deine Aufnahme. Dein Browser rechnet die Schallwelle aus. In die Bestellung kommen nur die Zahlen für die Form, nie der Ton selbst. Keine Cookies, kein Tracking.</p></div>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Fragen</p><h2>Häufige Fragen zum Schallwellen-Anhänger</h2></div>
  {fragen_html(K_FRAGEN)}
</div></section>
</main>'''

seite('schallwelle-anhaenger.html', 'Schallwelle als Schlüsselanhänger – personalisiert, 3D-gedruckt | Klangform',
      'Deine Stimme als Schallwellen-Schlüsselanhänger, Kettenanhänger, Lesezeichen oder Aufsteller. Aufnahme im Browser, 3D-gedruckt im Münsterland, ab 6 €.',
      KLANG, ld=[kruemel(('index.html', 'Start'), ('schallwelle-anhaenger.html', 'Klangform')),
                 {"@context": "https://schema.org", "@type": "Product", "name": "Klangform Schallwellen-Anhänger",
                  "description": "Personalisierter 3D-gedruckter Schlüsselanhänger, Kettenanhänger, Lesezeichen, Christbaumschmuck, Untersetzer oder Tischaufsteller in der Form der eigenen Schallwelle.",
                  "image": BASIS + "img/vorschau.png", "brand": {"@type": "Brand", "name": "Klangform"}, "category": "Personalisierte Geschenke",
                  "material": "PLA", "manufacturer": {"@id": BASIS + "#organisation"},
                  "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": "6.00", "highPrice": "15.90", "offerCount": "7",
                             "availability": "https://schema.org/InStock" if DRUCK_VERFUEGBAR else "https://schema.org/OutOfStock", "url": KLANGFORM,
                             "seller": {"@id": BASIS + "#organisation"}}},
                 fragen_ld(K_FRAGEN)])

# ---------------------------------------------------------------- Wegform

W_FRAGEN = [
    ('Welche Dateien kann ich hochladen?', 'GPX- und FIT-Dateien. Die bekommst du aus Garmin Connect, Strava, Komoot, Wahoo, Suunto, Polar und den meisten anderen Apps für Uhren und Fahrradcomputer.'),
    ('Woher kommt das Gelände?', 'Aus weltweiten Höhendaten (AWS Terrain Tiles). Dein Relief zeigt Berge und Täler rund um deine Route, nicht nur die Linie.'),
    ('Was ist der Unterschied zwischen Basis und Premium?', 'Basis: Gelände in einer Farbe, die Route als eigenes rotes Teil zum Einstecken. Premium: Gelände in 2 bis 4 Höhenstufen von Grün bis Weiß, wahlweise als Schneekappe, Herbst oder Wald.'),
    ('Wie groß ist das Relief?', 'Rund, eckig oder sechseckig mit 60, 100 oder 150 mm. Dazu gibt es eine Grundplatte mit Titel, Datum, Zeit, Kilometern, Höhenmetern und auf Wunsch dem Höhenprofil.'),
    ('Verlässt meine Route mein Gerät?', 'Deine Datei bleibt in deinem Browser. In die Bestellung kommt nur eine vereinfachte Route im Bestellcode, damit wir das Modell drucken können.'),
    ('Gibt es auch einen Anhänger?', 'Ja. Der Anhänger (50 mm) zeigt deine Route, hat oben eine Öse und auf der Rückseite Name und Zeit.'),
]

EXPORT = [
    ('Garmin Connect', 'Aktivität öffnen, oben rechts auf das Zahnrad, dann „Als GPX exportieren“ oder „Original exportieren“ (FIT).'),
    ('Strava', 'Aktivität am Computer öffnen, links auf die drei Punkte, dann „GPX exportieren“.'),
    ('Komoot', 'Tour am Computer öffnen, auf die drei Punkte, dann „Download“ bzw. „GPX-Datei herunterladen“.'),
    ('Andere Uhren und Apps', 'Suche im Menü der Aktivität nach „Exportieren“, „GPX“ oder „Datei herunterladen“.'),
]

WEG = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Wegform</p>
    <h1>Deine Wanderroute als 3D-Relief</h1>
    <p class="einleitung">Lade deine GPX- oder FIT-Datei hoch. Wir drucken das echte Gelände rund um deine Tour, mit deiner Route in Rot. Für die Gipfeltour, den Marathon oder den Alpenpass.</p>
    <div class="knoepfe">
      <a class="haupt" href="{WEGFORM}" rel="noopener">Jetzt Relief gestalten <span class="pfeil" aria-hidden="true">→</span></a>
      <a class="zweit" href="#gpx">GPX-Datei finden</a>
    </div>
  </div>
  <div class="bett">{WEG_BILD}<p class="unterschrift">Premium-Relief, sechseckig, mit Höhenstufen und Route.</p></div>
</section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">So funktioniert es</p><h2>Von der Tour zum Modell</h2></div>
  <ol class="ablauf">
    <li><h3>Route hochladen</h3><p>GPX oder FIT von deiner Uhr, deinem Radcomputer oder deiner App. Die Datei bleibt in deinem Browser.</p></li>
    <li><h3>Gestalten</h3><p>Produkt, Form, Größe, Farben und Ausschnitt wählen. Die 3D-Vorschau zeigt dir sofort das Ergebnis.</p></li>
    <li><h3>Bestellen</h3><p>Du schickst den Bestellcode ab. Wir drucken dein Relief mit 0,2 mm Schichthöhe und verschicken es.</p></li>
  </ol>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Produkte</p><h2>Relief, Grundplatte und Anhänger</h2></div>
  <div class="karten drei">
    <article class="karte karte-oben gruen"><div class="karte-text"><h3>Relief</h3>
      <p>Echtes Gelände in 60, 100 oder 150 mm, rund, eckig oder sechseckig.</p>
      <ul class="liste"><li>Basis: Gelände einfarbig, Route zum Einstecken</li><li>Premium: 2 bis 4 Höhenstufen</li><li>Farbschemen Natur, Wald, Alpin, Schneekappe, Herbst</li></ul></div></article>
    <article class="karte karte-oben gold"><div class="karte-text"><h3>Grundplatte</h3>
      <p>Der Rahmen für dein Relief, mit erhabener Schrift auf dem Rand.</p>
      <ul class="liste"><li>Titel, Datum und Zeit</li><li>Kilometer und Höhenmeter</li><li>Auf Wunsch mit Höhenprofil</li></ul></div></article>
    <article class="karte karte-oben rot"><div class="karte-text"><h3>Anhänger</h3>
      <p>Deine Route zum Mitnehmen, 50 mm, mit Öse.</p>
      <ul class="liste"><li>Rund, eckig oder sechseckig</li><li>Name und Zeit auf der Rückseite</li><li>Für Schlüssel, Rucksack oder Medaillenhalter</li></ul></div></article>
  </div>
  <p class="leise">Die Preise siehst du direkt im Konfigurator, bevor du bestellst.</p>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Ideen</p><h2>Welche Tour soll es sein?</h2></div>
  <ul class="chips">
    <li>Gipfel in den Alpen</li><li>Alpenüberquerung E5</li><li>Jakobsweg-Etappe</li><li>Erster Marathon</li>
    <li>Ultratrail</li><li>Rennrad über den Pass</li><li>Hochzeitswanderung</li><li>Hausrunde im Münsterland</li>
    <li>Geschenk für den Wanderverein</li>
  </ul>
</div></section>

<section class="abschnitt" id="gpx"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Anleitung</p><h2>So bekommst du deine GPX-Datei</h2>
    <p>Fast jede Sport-App kann deine Aktivität als Datei speichern. So geht es bei den bekanntesten:</p></div>
  <div class="tabelle-huelle"><table>
    <thead><tr><th scope="col">App</th><th scope="col">So geht es</th></tr></thead>
    <tbody>{''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in EXPORT)}</tbody>
  </table></div>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Fragen</p><h2>Häufige Fragen zum 3D-Relief</h2></div>
  {fragen_html(W_FRAGEN)}
  <p class="partner-hinweis">* Partnerlink: Als Amazon-Partner verdienen wir an qualifizierten Verkäufen. Für dich ändert sich der Preis nicht.</p>
</div></section>
</main>'''

seite('wanderroute-3d-relief.html', 'Wanderroute als 3D-Relief – GPX in 3D drucken | Wegform',
      'Deine Wanderung, Radtour oder dein Marathon als 3D-gedrucktes Relief mit echtem Gelände. GPX oder FIT hochladen, gestalten, bestellen. Mit Grundplatte und Höhenprofil.',
      WEG, ld=[kruemel(('index.html', 'Start'), ('wanderroute-3d-relief.html', 'Wegform')), fragen_ld(W_FRAGEN)])

# ---------------------------------------------------------------- Bücher

# Stand KDP-Bücherregal 18.10.2026, alle als Taschenbuch live
BUCHLISTE = [
    dict(asin='B0G2HKSN16', datei='adventsmalbuch', titel='Adventsmalbuch',
         unter='Ein Adventskalender zum Ausmalen für Kinder mit 24 Bildern und Zahlen',
         text='24 Bilder zum Ausmalen, eins für jeden Tag bis Weihnachten. Mit großen Zahlen, damit Kinder die Tage selbst finden.',
         gruppe='Kinder', farbe='#b8312f', motiv='stern', jahr='2025-11-15'),
    dict(asin='B0DC131TPW', datei='tiermalbuch', titel='Mein buntes Tiermalbuch',
         unter='30 Tiere in 10 Sprachen',
         text='30 Tiere zum Ausmalen. Zu jedem Tier steht der Name in 10 Sprachen. Malen und nebenbei Wörter lernen.',
         gruppe='Kinder', farbe='#3a6ea5', motiv='tier', jahr='2024-08-02'),
    dict(asin='B0FDQDGMPS', datei='dino-skizzenbuch', titel='Dino-Skizzenbuch',
         unter='100 Seiten zum Zeichnen für Kinder ab 4 Jahren',
         text='Blanko-Skizzenbuch mit lustigem Dinosaurier auf dem Umschlag. 100 leere Seiten für eigene Bilder.',
         gruppe='Kinder', farbe='#4f6e45', motiv='dino', jahr='2025-06-19'),
    dict(asin='B0FF39FCHH', datei='feen-skizzenbuch', titel='Feen-Skizzenbuch',
         unter='Blanko-Zeichenbuch für Kinder ab 4 Jahren',
         text='Leere Seiten zum Zeichnen, begleitet von einer kleinen Fee am Seitenrand.',
         gruppe='Kinder', farbe='#8a5aa8', motiv='fee', jahr='2025-06-22'),
    dict(asin='B0FRXY1SQY', datei='heilung-selbstliebe', titel='Heilung & Selbstliebe',
         unter='Mandalas für ein höheres Selbst – Mandalas und Affirmationen zum Ausmalen',
         text='Mandalas zum Ausmalen, jeweils mit einer Affirmation. Für ruhige Minuten und zum Abschalten.',
         gruppe='Erwachsene', farbe='#2f7d7a', motiv='mandala', jahr='2025-09-20'),
    dict(asin='B0G1KV25LM', datei='reichtum-wohlstand', titel='Reichtum, Wohlstand und Manifestation',
         unter='Mandalas und Affirmationen zum Ausmalen',
         text='Mandalas mit Affirmationen rund um Fülle und Wohlstand. Ausmalen als kleine tägliche Auszeit.',
         gruppe='Erwachsene', farbe='#c9a23f', motiv='mandala', jahr='2025-11-09'),
]
AUTOR = 'Robert Maximilian Maahs'
AUTOREN = ['Robert Maximilian Maahs', 'Christopher Müller']


def umschlag_svg(b):
    """Gestalteter Umschlag (eigene Grafik, kein Amazon-Bild). Später durch echte Umschläge ersetzbar."""
    f = b['farbe']
    m = b['motiv']
    cx, cy = 200, 330
    if m == 'mandala':
        teile = []
        for ring, (r, n) in enumerate([(130, 16), (100, 12), (70, 10), (42, 8)]):
            for k in range(n):
                a = 2 * math.pi * k / n
                teile.append(f'<ellipse cx="{cx + r * .55 * math.cos(a):.1f}" cy="{cy + r * .55 * math.sin(a):.1f}" rx="{r * .42:.1f}" ry="{r * .16:.1f}" '
                             f'transform="rotate({math.degrees(a):.1f} {cx + r * .55 * math.cos(a):.1f} {cy + r * .55 * math.sin(a):.1f})" fill="none" stroke="#fff" stroke-width="2.4" opacity="{.9 - ring * .12:.2f}"/>')
        teile.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="#fff"/>')
        motiv = ''.join(teile)
    elif m == 'stern':
        motiv = ''
        for i in range(24):
            x = 70 + (i % 6) * 52
            y = 210 + (i // 6) * 64
            motiv += f'<rect x="{x - 20}" y="{y - 22}" width="40" height="44" rx="8" fill="#fff" opacity=".92"/><text x="{x}" y="{y + 8}" text-anchor="middle" font-size="20" font-weight="700" fill="{f}">{i + 1}</text>'
    elif m == 'tier':
        motiv = (f'<circle cx="200" cy="330" r="92" fill="#fff"/><circle cx="135" cy="255" r="34" fill="#fff"/><circle cx="265" cy="255" r="34" fill="#fff"/>'
                 f'<circle cx="168" cy="318" r="11" fill="{f}"/><circle cx="232" cy="318" r="11" fill="{f}"/><ellipse cx="200" cy="358" rx="20" ry="14" fill="{f}"/>')
    elif m == 'dino':
        motiv = ('<path d="M70 420 C80 330 150 300 200 300 C240 300 250 250 250 220 C250 190 300 180 320 205 C340 230 320 260 290 262 '
                 'C280 300 300 340 300 420 Z" fill="#fff"/>'
                 '<path d="M150 300 l15 -28 l15 28 M190 298 l15 -30 l15 30 M228 290 l12 -26 l12 26" fill="#fff"/>'
                 f'<circle cx="300" cy="215" r="7" fill="{f}"/>')
    else:  # fee
        motiv = ('<ellipse cx="160" cy="300" rx="55" ry="85" fill="#fff" opacity=".75" transform="rotate(-25 160 300)"/>'
                 '<ellipse cx="240" cy="300" rx="55" ry="85" fill="#fff" opacity=".75" transform="rotate(25 240 300)"/>'
                 '<circle cx="200" cy="270" r="26" fill="#fff"/><path d="M200 296 L170 420 L230 420 Z" fill="#fff"/>'
                 '<path d="M300 200 l8 18 l20 2 l-15 13 l5 20 l-18 -11 l-18 11 l5 -20 l-15 -13 l20 -2 Z" fill="#fff"/>')
    titel = b['titel']
    zeilen, zeile = [], ''
    for w in titel.split():
        if len(zeile + ' ' + w) > 16 and zeile:
            zeilen.append(zeile)
            zeile = w
        else:
            zeile = (zeile + ' ' + w).strip()
    zeilen.append(zeile)
    zeilen = [z.replace('&', '&amp;') for z in zeilen]
    text = ''.join(f'<text x="200" y="{78 + i * 38}" text-anchor="middle" font-size="32" font-weight="700" fill="#fff">{z}</text>' for i, z in enumerate(zeilen))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="400" height="600" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">'
            f'<rect width="400" height="600" fill="{f}"/><rect width="22" height="600" fill="#000" opacity=".18"/>'
            f'{text}{motiv}<text x="200" y="560" text-anchor="middle" font-size="17" fill="#fff" opacity=".85">{AUTOR}</text></svg>')


# Echte Umschläge: img/buch-<datei>.webp (von Amazon, 302×390). Fehlt eine Datei, wird ein gezeichneter Umschlag erzeugt.
for b in BUCHLISTE:
    if os.path.exists(os.path.join(ZIEL, 'img', f"buch-{b['datei']}.webp")):
        b['bild'], b['bw'], b['bh'] = f"img/buch-{b['datei']}.webp", 302, 390
    else:
        with open(os.path.join(ZIEL, 'img', f"buch-{b['datei']}.svg"), 'w', encoding='utf-8') as fh:
            fh.write(umschlag_svg(b))
        b['bild'], b['bw'], b['bh'] = f"img/buch-{b['datei']}.svg", 400, 600


def buchkarte(b):
    return (f'<article class="buch">'
            f'<img src="{b["bild"]}" alt="Umschlag von „{b["titel"]}“" width="{b["bw"]}" height="{b["bh"]}" loading="lazy">'
            f'<p class="kennung">{b["gruppe"]} · Taschenbuch</p>'
            f'<h3>{b["titel"]}</h3><p>{b["unter"]}</p><p>{b["text"]}</p>'
            f'<div class="knoepfe"><a class="haupt" href="https://www.amazon.de/dp/{b["asin"]}" data-amazon rel="sponsored noopener" target="_blank">Bei Amazon ansehen*</a></div>'
            f'</article>')


def buch_ld(b):
    return {"@type": "Book", "name": f'{b["titel"]}: {b["unter"]}', "author": [{"@type": "Person", "name": n} for n in AUTOREN],
            "bookFormat": "https://schema.org/Paperback", "inLanguage": "de", "datePublished": b['jahr'],
            "url": f'https://www.amazon.de/dp/{b["asin"]}', "image": BASIS + b['bild'],
            "publisher": {"@id": BASIS + "#organisation"}}


COLLAGE = collage([('tiermalbuch', -7), ('adventsmalbuch', 3), ('heilung-selbstliebe', 9)])

kinder = [b for b in BUCHLISTE if b['gruppe'] == 'Kinder']
gross = [b for b in BUCHLISTE if b['gruppe'] == 'Erwachsene']

BUECHER = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Bücher</p>
    <h1>Malbücher und Skizzenbücher</h1>
    <p class="einleitung">Von Robert Maximilian Maahs und Christopher Müller: Malbücher und Skizzenbücher für Kinder ab 4 Jahren und Mandala-Malbücher mit Affirmationen für Erwachsene. Alle als Taschenbuch bei Amazon.</p>
    <div class="knoepfe"><a class="haupt" href="#kinder">Für Kinder</a><a class="zweit" href="#erwachsene">Für Erwachsene</a></div>
  </div>
  {COLLAGE}
</section>

<section class="abschnitt" id="kinder"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Für Kinder</p><h2>Ausmalen, zeichnen, Wörter lernen</h2>
    <p>Geschenkideen für Kinder ab 4 Jahren: zum Advent, für den Kindergarten oder für lange Autofahrten.</p></div>
  <div class="buecher">{''.join(buchkarte(b) for b in kinder)}</div>
</div></section>

<section class="abschnitt" id="erwachsene"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Für Erwachsene</p><h2>Mandalas mit Affirmationen</h2>
    <p>Ausmalen zum Entspannen. Jedes Mandala hat einen Satz, der dich durch den Tag begleitet.</p></div>
  <div class="buecher">{''.join(buchkarte(b) for b in gross)}</div>
  <p class="partner-hinweis">* Partnerlink: Als Amazon-Partner verdienen wir an qualifizierten Verkäufen. Für dich ändert sich der Preis nicht. Den aktuellen Preis siehst du bei Amazon.</p>
</div></section>
</main>'''

seite('buecher.html', 'Malbücher für Kinder und Mandala-Malbücher | BuntwerkStudio',
      'Malbücher und Skizzenbücher für Kinder ab 4 Jahren (Adventsmalbuch, Tiermalbuch in 10 Sprachen, Dino- und Feen-Skizzenbuch) und Mandala-Malbücher mit Affirmationen. Als Taschenbuch bei Amazon.',
      BUECHER, ld=[kruemel(('index.html', 'Start'), ('buecher.html', 'Bücher')),
                   {"@context": "https://schema.org", "@type": "ItemList", "name": "Bücher von BuntwerkStudio",
                    "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": buch_ld(b)} for i, b in enumerate(BUCHLISTE)]}])
# ---------------------------------------------------------------- Empfehlungen

GRUPPEN = [
    ('Zu deinem Klangform-Stück', 'gold', 'Kettenanhänger, Lesezeichen und Christbaumschmuck liefern wir ohne Kette und Band. Das hier passt dazu:', [
        ('Halskette für Anhänger', 'Dünne Kette mit kleinem Verschluss. Unsere Öse hat 3,2 mm.', 'Halskette Edelstahl dünn Damen'),
        ('Schlüsselringe', 'Für die 5-mm-Öse am Schlüsselanhänger.', 'Schlüsselringe 25mm Edelstahl'),
        ('Satinband', 'Für Lesezeichen und Christbaumschmuck.', 'Satinband 3mm'),
        ('Ohrhaken', 'Für die Ohrringe, aus hautverträglichem Material.', 'Ohrhaken Titan hypoallergen'),
    ]),
    ('Zu deinem Wegform-Relief', 'gruen', 'Damit dein Relief noch mehr erzählt:', [
        ('Wandregal oder Bilderleiste', 'Zum Aufstellen von Relief und Grundplatte.', 'Bilderleiste Holz 60cm'),
        ('Medaillenhalter', 'Für Läufer: Medaille und Wegform-Anhänger an einem Platz.', 'Medaillenhalter Laufen'),
    ]),
    ('Für Selbstdrucker', 'blau', 'Du hast die STL-Datei gekauft und druckst selbst? Damit drucken wir:', [
        ('PLA-Filament 1,75 mm', 'Für alle Klangform-Teile reicht PLA, 100 % Füllung, 0,2 mm Schichthöhe.', 'PLA Filament 1,75mm 1kg'),
        ('Düse 0,4 mm', 'Unsere Teile sind für eine 0,4-mm-Düse ausgelegt.', 'Düse 0,4mm 3D Drucker'),
        ('Haftmittel fürs Druckbett', 'Damit flache Teile sauber liegen bleiben.', 'Druckbett Haftspray 3D Druck'),
    ]),
]


def gruppen_html():
    out = []
    for titel, farbe, text, eintraege in GRUPPEN:
        karten = ''.join(f'<article class="karte karte-oben {farbe}"><div class="karte-text"><h3>{n}</h3><p>{b}</p>'
                         f'<div class="knoepfe">{partnerlink(amazon_suche(s), "Bei Amazon ansehen")}</div></div></article>'
                         for n, b, s in eintraege)
        out.append(f'<section class="abschnitt"><div class="huelle"><div class="kopf-abschnitt"><h2>{titel}</h2><p>{text}</p></div>'
                   f'<div class="karten drei">{karten}</div></div></section>')
    return ''.join(out)


EMPF = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Empfehlungen</p>
    <h1>Was zu unseren Stücken passt</h1>
    <p class="einleitung">Zubehör, das wir selbst nutzen oder das zu unseren Drucken passt. Die Links führen zu einer Suche bei Amazon, damit du selbst vergleichen kannst.</p>
    <p class="partner-hinweis">Alle mit * markierten Links sind Partnerlinks. Als Amazon-Partner verdienen wir an qualifizierten Verkäufen. Kaufst du darüber ein, erhalten wir eine kleine Provision. Für dich ändert sich der Preis nicht. Mehr dazu in der <a href="datenschutz.html#partnerprogramm">Datenschutzerklärung</a>.</p>
  </div>
  <div class="bett">{KLANG_BILD}</div>
</section>
{gruppen_html()}
</main>'''

seite('empfehlungen.html', 'Zubehör für Schallwellen-Anhänger und 3D-Relief | BuntwerkStudio',
      'Ketten, Schlüsselringe, Bänder, Bilderleisten und Filament: Zubehör, das zu den 3D-Drucken von Klangform und Wegform passt.',
      EMPF, ld=[kruemel(('index.html', 'Start'), ('empfehlungen.html', 'Empfehlungen'))])

# ---------------------------------------------------------------- Impressum

IMPRESSUM = f'''<main class="textseite">
  <h1>Impressum</h1>
  <h2>Angaben nach § 5 Digitale-Dienste-Gesetz</h2>
  <p>BuntwerkStudio<br>Inhaber: Robert Maximilian Maahs<br>Zum Fuchsbau 7<br>48346 Ostbevern<br>Deutschland</p>

  <h2>Kontakt</h2>
  <p>E-Mail: <a href="mailto:buntwerkstudio@gmail.com">buntwerkstudio@gmail.com</a><br>
  Kontaktformular: <a href="{KLANGFORM}kontakt.html" rel="noopener">Nachricht schreiben</a></p>

  <h2>Umsatzsteuer</h2>
  <p>Kleinunternehmer nach § 19 Umsatzsteuergesetz. Es wird keine Umsatzsteuer berechnet und daher auch keine ausgewiesen.</p>

  <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 Medienstaatsvertrag</h2>
  <p>Robert Maximilian Maahs, Anschrift wie oben.</p>

  <h2>Verbraucherstreitbeilegung</h2>
  <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>

  <h2>Verkauf und Vertragspartner</h2>
  <p>Auf dieser Seite wird nichts verkauft. Bestellungen laufen über <a href="{KLANGFORM}" rel="noopener">Klangform</a> und <a href="{WEGFORM}" rel="noopener">Wegform</a>. Dort findest du AGB, Kundeninformationen, Widerrufsbelehrung und die Widerrufsfunktion. Bücher kaufst du bei Amazon; Vertragspartner ist dann Amazon.</p>

  <h2>Partnerlinks</h2>
  <p>Als Amazon-Partner verdienen wir an qualifizierten Verkäufen. Links mit * sind Partnerlinks. Kaufst du darüber ein, erhalten wir eine Provision. Der Preis ändert sich für dich nicht.</p>

  <h2>Haftung für Links</h2>
  <p>Für die Inhalte fremder Seiten, auf die wir verlinken, sind deren Betreiber verantwortlich. Wir haben die verlinkten Seiten beim Setzen der Links geprüft. Erfahren wir von Rechtsverstößen, entfernen wir den Link.</p>

  <h2>Schrift</h2>
  <p>Fredoka (SIL Open Font License), lokal eingebunden.</p>
</main>'''
seite('impressum.html', 'Impressum – BuntwerkStudio', 'Impressum von BuntwerkStudio, Inhaber Robert Maximilian Maahs, Ostbevern.', IMPRESSUM, index=True)

# ---------------------------------------------------------------- Datenschutz

DATENSCHUTZ = f'''<main class="textseite">
  <h1>Datenschutz</h1>
  <p class="leise">Diese Erklärung gilt für buntwerkstudio.github.io. Stand: {STAND}.</p>

  <h2>1. Verantwortlich</h2>
  <p>BuntwerkStudio<br>Inhaber: Robert Maximilian Maahs<br>Zum Fuchsbau 7<br>48346 Ostbevern<br>Deutschland<br>E-Mail: <a href="mailto:buntwerkstudio@gmail.com">buntwerkstudio@gmail.com</a></p>

  <h2>2. Kurz gesagt</h2>
  <p>Diese Seite setzt keine Cookies, nutzt keine Analyse- oder Werbedienste und lädt keine Inhalte von anderen Servern. Schrift, Bilder und Programmcode liegen alle auf dieser Seite. Daten an andere gehen erst, wenn du auf einen Link zu einer anderen Seite klickst.</p>

  <h2>3. Hosting bei GitHub Pages</h2>
  <p>Die Seite liegt bei GitHub Pages, einem Dienst von GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Wenn du die Seite aufrufst, verarbeitet GitHub technisch notwendige Daten: deine IP-Adresse, Datum und Uhrzeit, die aufgerufene Adresse, die vorher besuchte Seite (Referrer) und Angaben zu deinem Browser. GitHub speichert diese Daten zur Sicherheit des Dienstes und löscht sie nach eigenen Angaben nach kurzer Zeit.</p>
  <p>Rechtsgrundlage ist unser berechtigtes Interesse an einer sicheren und erreichbaren Seite (Art. 6 Abs. 1 lit. f DSGVO). Die Daten können in den USA verarbeitet werden. GitHub gehört zu Microsoft; Microsoft und seine US-Tochtergesellschaften sind nach dem EU-U.S. Data Privacy Framework zertifiziert. Mehr dazu: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub-Datenschutzerklärung</a>.</p>

  <h2 id="partnerprogramm">4. Amazon-Partnerprogramm</h2>
  <p>Wir nehmen am Partnerprogramm von Amazon Europe Core S.à r.l., 38 avenue John F. Kennedy, L-1855 Luxemburg, teil. Als Amazon-Partner verdienen wir an qualifizierten Verkäufen. Links zu Amazon mit * sind Partnerlinks und enthalten unsere Partner-Kennung.</p>
  <p>Auf dieser Seite selbst werden keine Inhalte von Amazon geladen und keine Cookies gesetzt. Erst wenn du auf einen Partnerlink klickst, öffnet sich die Seite von Amazon. Amazon erfährt dann, dass du über unsere Seite kommst, und setzt auf seiner eigenen Seite Cookies, um einen Kauf unserer Kennung zuzuordnen. Wir erfahren nicht, wer du bist; wir sehen nur Klicks und Verkäufe ohne Namen. Dafür ist Amazon verantwortlich. Es gilt die <a href="https://www.amazon.de/gp/help/customer/display.html?nodeId=201909010" rel="noopener">Datenschutzerklärung von Amazon</a>. Amazon kann Daten auch in den USA verarbeiten.</p>
  <p>Rechtsgrundlage für die Partnerkennung in unseren Links ist unser berechtigtes Interesse an einer Provision für Empfehlungen (Art. 6 Abs. 1 lit. f DSGVO). Die Cookies auf der Seite von Amazon setzt Amazon nach seinen eigenen Regeln und Einwilligungen.</p>

  <h2>5. Links zu Klangform und Wegform</h2>
  <p>Klangform und Wegform sind unsere eigenen Seiten bei Netlify. Klickst du auf einen Link dorthin, gelten die Datenschutzerklärungen von <a href="{KLANGFORM}datenschutz.html" rel="noopener">Klangform</a> und <a href="{WEGFORM}datenschutz.html" rel="noopener">Wegform</a>.</p>

  <h2>6. E-Mail</h2>
  <p>Schreibst du uns eine E-Mail, verarbeiten wir deine E-Mail-Adresse, deinen Namen und deine Nachricht, um dir zu antworten (Art. 6 Abs. 1 lit. b DSGVO bei Fragen zu einer Bestellung, sonst lit. f). Unser Postfach liegt bei Google (Gmail, Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland). Nachrichten werden deshalb auf Servern von Google gespeichert, auch in den USA möglich. Google ist nach dem EU-U.S. Data Privacy Framework zertifiziert. Wir löschen Nachrichten, wenn sie erledigt sind, es sei denn, wir müssen sie aus Handels- oder Steuerrecht aufbewahren.</p>

  <h2>7. Keine automatisierten Entscheidungen</h2>
  <p>Wir treffen keine Entscheidungen über dich, die nur automatisch erfolgen (Art. 22 DSGVO).</p>

  <h2>8. Deine Rechte</h2>
  <p>Du hast das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18) und Datenübertragbarkeit (Art. 20). Schreib dafür an <a href="mailto:buntwerkstudio@gmail.com">buntwerkstudio@gmail.com</a>.</p>
  <p><strong>Widerspruchsrecht (Art. 21 DSGVO):</strong> Soweit wir Daten auf Grundlage unseres berechtigten Interesses verarbeiten, kannst du dieser Verarbeitung aus Gründen, die sich aus deiner besonderen Situation ergeben, jederzeit widersprechen.</p>
  <p>Du kannst dich bei einer Datenschutz-Aufsichtsbehörde beschweren, zum Beispiel bei der Landesbeauftragten für Datenschutz und Informationsfreiheit Nordrhein-Westfalen, Kavalleriestraße 2–4, 40213 Düsseldorf.</p>
</main>'''
seite('datenschutz.html', 'Datenschutz – BuntwerkStudio', 'Datenschutzerklärung von BuntwerkStudio: keine Cookies, kein Tracking, Hosting bei GitHub Pages, Amazon-Partnerprogramm.', DATENSCHUTZ)

# ---------------------------------------------------------------- 404

seite('404.html', 'Seite nicht gefunden – BuntwerkStudio', 'Diese Seite gibt es nicht.',
      f'''<main class="huelle held"><div><p class="marke">Fehler 404</p><h1>Diese Seite gibt es nicht</h1>
      <p class="einleitung">Vielleicht hilft dir einer dieser Wege weiter.</p>
      <div class="knoepfe"><a class="haupt" href="./">Zur Startseite</a><a class="zweit" href="{KLANGFORM}" rel="noopener">Klangform</a><a class="zweit" href="{WEGFORM}" rel="noopener">Wegform</a></div></div>
      <div class="bett">{WEG_BILD}</div></main>''', index=False)

# ---------------------------------------------------------------- robots, sitemap

with open(os.path.join(ZIEL, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\n\nSitemap: {BASIS}sitemap.xml\n')

sm = [('', '1.0'), ('schallwelle-anhaenger.html', '0.9'), ('wanderroute-3d-relief.html', '0.9'),
      ('buecher.html', '0.7'), ('empfehlungen.html', '0.5'), ('impressum.html', '0.2'), ('datenschutz.html', '0.2')]
with open(os.path.join(ZIEL, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p, prio in sm:
        f.write(f'  <url><loc>{BASIS}{p}</loc><lastmod>2026-10-18</lastmod><priority>{prio}</priority></url>\n')
    f.write('</urlset>\n')

# Bild für die Vorschau (SVG) – wird in PNG umgewandelt
with open(os.path.join(tempfile.gettempdir(), 'held.svg'), 'w') as f:
    f.write(HELD_BILD.replace('<svg ', '<svg width="1000" height="800" ', 1))
print('fertig')
