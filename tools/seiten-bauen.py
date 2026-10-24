#!/usr/bin/env python3
"""Erzeugt die statischen Seiten für buntwerkstudio.github.io (einmalig, Ergebnis wird committet)."""
import json, math, os, posixpath, random, tempfile

ZIEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://buntwerkstudio.github.io/'
KLANGFORM = 'https://klangform.netlify.app/'
WEGFORM = 'https://tracks-and-trails.netlify.app/'
STAND = '18.10.2026'
GEAENDERT = '2026-10-24'   # lastmod in sitemap.xml
# Wie SHOP.druckVerfuegbar in Klangform (js/config.js). False = gedruckte Teile ausverkauft, nur STL-Datei bestellbar.
DRUCK_VERFUEGBAR = False
HINWEIS_AUSVERKAUFT = '' if DRUCK_VERFUEGBAR else '<div class="kasten"><p><strong>Gerade ausverkauft:</strong> Fertig gedruckte Teile können wir im Moment nicht liefern. Die Druckdatei (STL) zum Selbstdrucken bekommst du weiter für 2 € per E-Mail.</p></div>'

# ---------------------------------------------------------------- Grafiken

# Logo E (19.10.2026): BS-Monogramm aus dem alten Logo in der dunklen Kachel, darunter die vier Farbbalken. Datei: img/logo.svg
LOGO = '<svg viewBox="0 0 320 320" aria-hidden="true"><rect width="320" height="320" rx="72" fill="#273134"/><path transform="translate(58 52) scale(.388)" fill="#f5f7f4" d="M369.5 1.1C341.8 5.3 320 16.7 300.1 37.3C295.1 42.5 295.2 43.6 300.6 49.3L304.1 53L308.9 45.8C311.5 41.8 317.3 35.1 321.7 30.9C339.4 14 360.9 7 386.1 9.8C398.3 11.1 406.1 13.4 417.4 19.1C443.4 32 467.1 60.8 481.6 96.9C485.3 106.2 486.1 107.5 488.4 107.8C489.9 108 491.2 107.6 491.5 106.8C491.8 106.1 491.6 83.3 491.2 56.2L490.5 6.9L484.5 12C480.8 15.2 478 16.8 477 16.4C467.3 12.6 440.9 5.4 426.5 2.8C414 0.5 379.7 -0.5 369.5 1.1ZM79.8 3.8C1.2 4 0 4 0 6C0 7.8 0.8 8 16.2 8.2L32.5 8.5L32.8 133.4C32.9 202.2 33.4 258.8 33.8 259.2C34.2 259.6 39.9 249.5 46.5 236.7C67.6 195.4 89.6 152.9 105.1 123.9L114 107.2L114 57.6L114 8L132.8 8C161.5 8 175.9 11.2 189.9 20.4C212.5 35.5 225.1 60.6 228.2 97.2C232 143 217.9 183.3 192 200.5C177.8 209.9 163 213 131.6 213C117.3 213 112 213.3 111.2 214.2C110.2 215.4 107.6 220.5 87 260.5C81.9 270.4 75.6 282.6 73 287.5C62.4 307.7 0 431.9 0 432.8C0 434.4 88 435.2 152.5 434.1C211.4 433.1 212.7 433.1 225 430.5C254.2 424.4 273.5 415.4 290.5 399.8C302.5 388.8 310.3 376.6 315.8 360.4C320.7 346.1 321.4 340.9 321.4 322.5C321.4 307.9 321.1 304.2 319.1 296.5C307.4 251.9 269.7 222.7 215.5 216.4C198.2 214.4 194.9 213.7 200.5 213.3C214.9 212.2 237.5 205.4 252.4 197.7C287.8 179.6 306 148.4 306 105.9C306 90.2 304.1 79.3 299.2 67.3C285.2 33 254.7 11.6 211.5 6C193 3.6 180.8 3.4 79.8 3.8ZM172 219.4C203 227.6 221.3 242.9 233.3 270.9C240.4 287.2 243 301.3 243 323C243 346.6 239.6 363.6 231.4 380.9C221.1 402.8 206.7 416.6 186 424.3C174.4 428.6 162.6 430 137.1 430L114 430L114 324.2C114 266 114.3 218 114.8 217.6C115.2 217.2 126.8 217 140.5 217.2C159.8 217.6 167 218.1 172 219.4ZM315.5 122C313.4 143.4 303.2 166.5 288.4 182.9C286 185.6 284 188.4 284 189.2C284 192.9 298.7 206.3 314.1 216.6C322 221.8 340.8 231.6 356.5 238.7C360.4 240.4 366.5 243.2 370.3 244.9C374 246.6 385.9 251.8 396.8 256.6C437.1 274.4 454.8 284.6 468.5 298.4C485.6 315.5 493.3 332.1 493.4 352C493.6 386.1 470 413.6 431.5 424.2C426.5 425.6 419.8 426.2 408 426.6C393.5 427.1 390.4 426.9 382 425C357.2 419.4 333.6 404 320.9 384.9L316.5 378.3L310 389.3C306 396.1 300.7 403.4 296.2 408.2L288.8 416L291.7 417.1C299.3 420.1 319.6 426.3 329 428.5C347.4 432.8 355.2 433.9 373.4 435.2C418 438.1 450.4 430.3 476.9 410.1C508.8 385.7 525.2 349.1 525.2 302.5C525.1 271.9 517.8 249.8 500.6 228.3C485.6 209.7 464.4 195.7 430 181.7C425.3 179.8 414.1 175.2 405 171.6C383.3 162.8 356.7 149.6 345.5 142.2C336.3 136.1 324.8 125.6 319.3 118.5L316.2 114.6L315.5 122Z"/><rect x="58" y="246" width="44" height="14" rx="7" fill="#3a6ea5"/><rect x="110" y="246" width="44" height="14" rx="7" fill="#4f6e45"/><rect x="162" y="246" width="44" height="14" rx="7" fill="#c9a23f"/><rect x="214" y="246" width="44" height="14" rx="7" fill="#b8312f"/></svg>'

FAVICON = '/img/logo.svg'

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
MENUE_EN = [('en/index.html', 'Home'), ('en/sound-wave-keychain.html', 'Klangform'), ('en/hiking-route-3d-relief.html', 'Wegform'),
            ('en/books.html', 'Books'), ('en/recommendations.html', 'Recommendations')]

# Englische Seiten (Aufgabe B7 = Klangform B13 = Wegform B19, entschieden 24.10.2026): nur die Website, eigene Adressen unter /en/.
# Rechtstexte gibt es nur auf Deutsch; der Schalter führt dort zur englischen Startseite.
EN = {'index.html': 'en/index.html', 'schallwelle-anhaenger.html': 'en/sound-wave-keychain.html',
      'wanderroute-3d-relief.html': 'en/hiking-route-3d-relief.html', 'buecher.html': 'en/books.html', 'empfehlungen.html': 'en/recommendations.html'}
DE = {v: k for k, v in EN.items()}


def englisch(datei):
    return datei.startswith('en/')


def adresse(datei):
    """Öffentliche Adresse einer Seite (Startseiten ohne index.html)."""
    return BASIS + (datei[:-len('index.html')] if datei.endswith('index.html') else datei)


def rel(von, nach):
    """Relativer Link von Seite „von“ zu Seite „nach“ (beide relativ zum Repository)."""
    p = posixpath.relpath(nach, posixpath.dirname(von) or '.')
    if p == 'index.html' or p.endswith('/index.html'):
        p = p[:-len('index.html')] or './'
    return p


def sprachschalter(datei):
    """„DE | EN“ in der Kopfzeile, führt zur gleichen Seite in der anderen Sprache (js/sprache.js merkt die Wahl)."""
    en = englisch(datei)
    ziel = {'de': DE.get(datei, 'index.html') if en else datei, 'en': datei if en else EN.get(datei, 'en/index.html')}
    teile = [f'<a href="{rel(datei, ziel[s])}" lang="{s}" hreflang="{s}" data-sprache="{s}" title="{t}"'
             f'{" aria-current=\"true\"" if (s == "en") == en else ""}>{s.upper()}</a>'
             for s, t in (('de', 'Deutsch'), ('en', 'English'))]
    return f'<nav class="sprache" aria-label="Sprache / Language">{teile[0]}<span aria-hidden="true">|</span>{teile[1]}</nav>'


def kopf(datei):
    en = englisch(datei)
    links = ''.join(f'<a href="{rel(datei, d)}"{" aria-current=\"page\"" if d == datei else ""}>{n}</a>' for d, n in (MENUE_EN if en else MENUE))
    start = rel(datei, 'en/index.html' if en else 'index.html')
    return (f'<header class="huelle kopfzeile"><a class="wortmarke" href="{start}" aria-label="BuntwerkStudio – {"Home" if en else "Startseite"}">{LOGO}'
            f'<span>Buntwerk<b>Studio</b></span></a><nav class="menue" aria-label="{"Main menu" if en else "Hauptmenü"}">{links}</nav>{sprachschalter(datei)}</header>')


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

FUSS_EN = f'''<footer class="fuss"><div class="huelle">
  <div class="fuss-raster">
    <div><a class="wortmarke" href="./">{LOGO}<span>Buntwerk<b>Studio</b></span></a>
      <p>3D-printed keepsakes and books from Ostbevern, Germany.</p></div>
    <div><h2>3D printing</h2><ul>
      <li><a href="sound-wave-keychain.html">Klangform: sound wave</a></li>
      <li><a href="hiking-route-3d-relief.html">Wegform: hiking route</a></li>
      <li><a href="{KLANGFORM}" rel="noopener" hreflang="de">Design with Klangform (German)</a></li>
      <li><a href="{WEGFORM}" rel="noopener" hreflang="de">Design with Wegform (German)</a></li></ul></div>
    <div><h2>More</h2><ul>
      <li><a href="books.html">Books</a></li>
      <li><a href="recommendations.html">Recommendations</a></li>
      <li><a href="mailto:buntwerkstudio@gmail.com">Send us an email</a></li></ul></div>
    <div><h2>Legal</h2><ul>
      <li><a href="../impressum.html" hreflang="de">Legal notice (German)</a></li>
      <li><a href="../datenschutz.html" hreflang="de">Privacy policy (German)</a></li>
      <li><a href="../datenschutz.html#partnerprogramm" hreflang="de">Affiliate links (German)</a></li></ul></div>
  </div>
  <p class="klein">As an Amazon Associate we earn from qualifying purchases. Links marked with * are affiliate links: if you buy through them, we receive a small commission. The price stays the same for you.</p>
  <p class="klein" lang="de">Als Amazon-Partner verdienen wir an qualifizierten Verkäufen.</p>
  <p class="klein">The German versions of our legal texts are binding. © 2026 BuntwerkStudio · Owner Robert Maximilian Maahs · Small business under § 19 UStG (no VAT charged)</p>
</div></footer>'''


def seite(datei, titel, beschreibung, inhalt, ld=None, index=True, og_typ='website'):
    en = englisch(datei)
    pre = '../' if en else ''
    url = adresse(datei)
    robots = 'index, follow, max-image-preview:large' if index else 'noindex, follow'
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>' for x in (ld or []))
    paar = DE.get(datei) if en else EN.get(datei)
    alternativ = '' if not paar else ''.join(
        f'<link rel="alternate" hreflang="{h}" href="{adresse(d)}">{chr(10)}  '
        for h, d in (('de', paar if en else datei), ('en', datei if en else paar), ('x-default', paar if en else datei)))
    html = f'''<!doctype html>
<html lang="{'en' if en else 'de'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; form-action 'none'; base-uri 'self'">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{titel}</title>
  <meta name="description" content="{beschreibung}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  {alternativ}<meta property="og:type" content="{og_typ}">
  <meta property="og:locale" content="{'en_GB' if en else 'de_DE'}">
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
  <link rel="preload" href="{pre}fonts/fredoka-600.woff" as="font" type="font/woff" crossorigin>
  <script src="{pre}js/thema.js"></script>
  <link rel="stylesheet" href="{pre}css/style.css">
  {lds}
</head>
<body>
{kopf(datei)}
{inhalt}
{FUSS_EN if en else FUSS}
<script src="{pre}js/partner.js" defer></script>
<script src="{pre}js/sprache.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.dirname(os.path.join(ZIEL, datei)), exist_ok=True)
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
    dict(asin='B0G2HKSN16', en_unter='An advent calendar to colour in for children, with 24 pictures and numbers', en_text='24 pictures to colour in, one for each day until Christmas. With big numbers so children can find the days themselves.', datei='adventsmalbuch', titel='Adventsmalbuch',
         unter='Ein Adventskalender zum Ausmalen für Kinder mit 24 Bildern und Zahlen',
         text='24 Bilder zum Ausmalen, eins für jeden Tag bis Weihnachten. Mit großen Zahlen, damit Kinder die Tage selbst finden.',
         gruppe='Kinder', farbe='#b8312f', motiv='stern', jahr='2025-11-15'),
    dict(asin='B0DC131TPW', en_unter='30 animals in 10 languages', en_text='30 animals to colour in. Each animal has its name in 10 languages. Colour and learn words along the way.', datei='tiermalbuch', titel='Mein buntes Tiermalbuch',
         unter='30 Tiere in 10 Sprachen',
         text='30 Tiere zum Ausmalen. Zu jedem Tier steht der Name in 10 Sprachen. Malen und nebenbei Wörter lernen.',
         gruppe='Kinder', farbe='#3a6ea5', motiv='tier', jahr='2024-08-02'),
    dict(asin='B0FDQDGMPS', en_unter='100 pages to draw on, for children aged 4 and up', en_text='Blank sketchbook with a funny dinosaur on the cover. 100 empty pages for their own pictures.', datei='dino-skizzenbuch', titel='Dino-Skizzenbuch',
         unter='100 Seiten zum Zeichnen für Kinder ab 4 Jahren',
         text='Blanko-Skizzenbuch mit lustigem Dinosaurier auf dem Umschlag. 100 leere Seiten für eigene Bilder.',
         gruppe='Kinder', farbe='#4f6e45', motiv='dino', jahr='2025-06-19'),
    dict(asin='B0FF39FCHH', en_unter='Blank drawing book for children aged 4 and up', en_text='Empty pages to draw on, with a little fairy at the edge of the page.', datei='feen-skizzenbuch', titel='Feen-Skizzenbuch',
         unter='Blanko-Zeichenbuch für Kinder ab 4 Jahren',
         text='Leere Seiten zum Zeichnen, begleitet von einer kleinen Fee am Seitenrand.',
         gruppe='Kinder', farbe='#8a5aa8', motiv='fee', jahr='2025-06-22'),
    dict(asin='B0FRXY1SQY', en_unter='Mandalas and affirmations to colour in', en_text='Mandalas to colour in, each with an affirmation. For quiet moments and to switch off.', datei='heilung-selbstliebe', titel='Heilung & Selbstliebe',
         unter='Mandalas für ein höheres Selbst – Mandalas und Affirmationen zum Ausmalen',
         text='Mandalas zum Ausmalen, jeweils mit einer Affirmation. Für ruhige Minuten und zum Abschalten.',
         gruppe='Erwachsene', farbe='#2f7d7a', motiv='mandala', jahr='2025-09-20'),
    dict(asin='B0G1KV25LM', en_unter='Mandalas and affirmations to colour in', en_text='Mandalas with affirmations about abundance and wealth. Colouring as a small daily break.', datei='reichtum-wohlstand', titel='Reichtum, Wohlstand und Manifestation',
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


def buchkarte(b, en=False):
    if en:
        return (f'<article class="buch">'
                f'<img src="../{b["bild"]}" alt="Cover of “{b["titel"]}”" width="{b["bw"]}" height="{b["bh"]}" loading="lazy">'
                f'<p class="kennung">{"Children" if b["gruppe"] == "Kinder" else "Adults"} · Paperback in German</p>'
                f'<h3 lang="de">{b["titel"]}</h3><p>{b["en_unter"]}</p><p>{b["en_text"]}</p>'
                f'<div class="knoepfe"><a class="haupt" href="https://www.amazon.de/dp/{b["asin"]}" data-amazon rel="sponsored noopener" target="_blank">View on Amazon.de*</a></div>'
                f'</article>')
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
      <div class="knoepfe"><a class="haupt" href="/">Zur Startseite</a><a class="zweit" href="{KLANGFORM}" rel="noopener">Klangform</a><a class="zweit" href="{WEGFORM}" rel="noopener">Wegform</a></div>
      <div lang="en"><h2>Page not found</h2><p>This page does not exist. <a href="/en/">Go to the English home page</a>.</p></div></div>
      <div class="bett">{WEG_BILD}</div></main>''', index=False)

# ---------------------------------------------------------------- Englische Seiten (B7)
# Kurz und klar, Leser mit „you“. Die Konfiguratoren Klangform und Wegform gibt es nur auf Deutsch (Entscheidung 24.10.2026).
# tools/sprache-pruefen.py prüft, dass die englischen Seiten außerhalb von lang="de" keine Umlaute enthalten.

NUR_DEUTSCH = '<p class="leise">The configurators are in German.</p>'
VERSAND_EN = 'We ship printed models within Germany only. Print files are available worldwide.'
AUSVERKAUFT_EN = '' if DRUCK_VERFUEGBAR else '<div class="kasten"><p><strong>Currently sold out:</strong> we cannot deliver printed parts at the moment. You can still get the print file (STL) for €2 by email.</p></div>'
MUENSTERLAND = '<span lang="de">Münsterland</span>'
AUTOREN_EN = '<span lang="de">Robert Maximilian Maahs</span> and <span lang="de">Christopher Müller</span>'

HELD_EN = svg(relief(205, 190, 128) + anhaenger(268, 268, 190, 62, '#c9a23f', -8) + buch(372, 60, 92, 136, '#3a6ea5', 7),
              titel='3D-printed hiking relief, sound wave keychain and book on a print bed')
KLANG_EN = svg(anhaenger(95, 80, 280, 90, '#c9a23f', -6) + anhaenger(45, 235, 210, 66, '#3a6ea5', 4) + anhaenger(285, 250, 160, 52, '#ecebe6', -10),
               titel='Keychains in the shape of a sound wave')
WEG_EN = svg(relief(250, 205, 165), titel='Relief of a hiking route with colour bands by height and a red route')
COLLAGE_EN = collage([('dino-skizzenbuch', -7), ('feen-skizzenbuch', 3), ('reichtum-wohlstand', 9)]).replace('src="img/', 'src="../img/')

ORG_EN = {**ORG, "description": "3D-printed personalised keepsakes and books from Ostbevern, Germany."}

START_EN = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">3D printing from Germany</p>
    <h1>Memories you can hold in your hand</h1>
    <p class="einleitung">We print your voice as a sound wave and your hike as a relief with real terrain. You design it in your browser, we print it in Ostbevern and Ascheberg in the {MUENSTERLAND} region.</p>
    <div class="knoepfe">
      <a class="haupt" href="sound-wave-keychain.html">Sound wave keychain <span class="pfeil" aria-hidden="true">→</span></a>
      <a class="zweit" href="hiking-route-3d-relief.html">Hiking route as a relief</a>
    </div>
    <p class="leise">{VERSAND_EN}</p>
    <div class="streifen" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  </div>
  <div class="bett">{HELD_EN}</div>
</section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Our two workshops</p>
    <h2>Two configurators, one studio</h2>
    <p>Both run entirely in your browser. Your recording and your route stay on your device. You see a preview and the price right away. The configurators are in German.</p></div>
  <div class="karten">
    <article class="karte karte-oben gold">
      <div class="bett">{KLANG_EN}</div>
      <div class="karte-text">
        <p class="marke">Klangform</p>
        <h3>Your voice as a keychain, pendant or desk display</h3>
        <p>Record an “I love you”, a laugh or a heartbeat. We turn it into a solid piece in the shape of your sound wave. From <span class="preis">€6</span>.{'' if DRUCK_VERFUEGBAR else ' Printed parts are sold out right now; the print file costs €2.'}</p>
        <div class="knoepfe">
          <a class="haupt" href="{KLANGFORM}" rel="noopener" hreflang="de">Design with Klangform <span class="pfeil" aria-hidden="true">→</span></a>
          <a class="zweit" href="sound-wave-keychain.html">Learn more</a>
        </div>
        {NUR_DEUTSCH}
      </div>
    </article>
    <article class="karte karte-oben gruen">
      <div class="bett">{WEG_EN}</div>
      <div class="karte-text">
        <p class="marke">Wegform</p>
        <h3>Your hike as a 3D relief with real terrain</h3>
        <p>Upload your GPX or FIT file from Garmin, Strava or Komoot. We print the mountains, valleys and your route, with colour bands by height if you like.</p>
        <div class="knoepfe">
          <a class="haupt" href="{WEGFORM}" rel="noopener" hreflang="de">Design with Wegform <span class="pfeil" aria-hidden="true">→</span></a>
          <a class="zweit" href="hiking-route-3d-relief.html">Learn more</a>
        </div>
        {NUR_DEUTSCH}
      </div>
    </article>
  </div>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">How it works</p><h2>Three steps to your piece</h2></div>
  <ol class="ablauf">
    <li><h3>Design</h3><p>Record a sound or upload a route, then choose the product, shape, size and colour.</p></li>
    <li><h3>Order</h3><p>You pay with PayPal. Print files are ready to download right after payment.</p></li>
    <li><h3>Unpack</h3><p>We print your piece and ship it within Germany. For Klangform within 7 days of payment.</p></li>
  </ol>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Gift ideas</p><h2>Who is it for?</h2>
    <p>Personal gifts that exist only once.</p></div>
  <ul class="chips">
    <li>Anniversary and Valentine’s Day</li><li>Wedding: the “I do”</li><li>Birth: the first heartbeat</li>
    <li>Grandparents: the grandchildren’s voices</li><li>Hikers and climbers</li><li>Runners: the marathon course</li>
    <li>Cyclists: an alpine pass</li><li>Christmas</li><li>In memory of a loved one</li>
  </ul>
</div></section>

<section class="abschnitt"><div class="huelle karten">
  <div>
    <p class="marke">Books</p><h2>Colouring books for young and old</h2>
    <p class="leise">{AUTOREN_EN} have made colouring books and sketchbooks for children aged 4 and up and mandala colouring books with affirmations. All are paperbacks in German, sold on Amazon.de.</p>
    <div class="knoepfe"><a class="zweit" href="books.html">See the books <span class="pfeil" aria-hidden="true">→</span></a></div>
  </div>
  {COLLAGE_EN}
</div></section>
</main>'''

seite('en/index.html', 'BuntwerkStudio – sound waves and hiking routes as 3D prints',
      'Personalised 3D-printed gifts from Germany: your voice as a sound wave keychain (Klangform) and your hiking route as a 3D relief (Wegform). Plus colouring books for children and adults.',
      START_EN, ld=[ORG_EN, {"@context": "https://schema.org", "@type": "WebSite", "name": "BuntwerkStudio", "url": BASIS + 'en/', "inLanguage": "en",
                             "publisher": {"@id": BASIS + "#organisation"}}])

K_FRAGEN_EN = [
    ('What can I record?', 'Anything with a sound: a name, an “I love you”, a laugh, a heartbeat from an ultrasound video, a voice message or a few seconds of your song. 2 to 5 seconds work best.'),
    ('Can I use a voice message or a video?', 'Yes. Instead of recording, you can upload an audio or video file, for example a saved voice message or an ultrasound video. Then you choose the part you want.'),
    ('Is my recording uploaded?', 'No. The recording is only analysed in your browser. It becomes a row of numbers for the shape. The sound cannot be restored from these numbers.'),
    ('How much does a sound wave keychain cost?', 'A keychain costs €7 to €9 depending on the size, a pendant €7, a Christmas ornament from €6. Shipping within Germany costs €2.95. All prices are final prices.'),
    ('Do you ship outside Germany?', VERSAND_EN),
    ('How long does delivery take?', 'We print your piece and ship it within 7 days of payment.' + ('' if DRUCK_VERFUEGBAR else ' Printed parts are sold out right now. The print file comes by email after payment.')),
    ('Is a chain or ribbon included?', 'No. Pendants come without a chain, bookmarks and Christmas ornaments without a ribbon. You find matching chains, ribbons and key rings on our recommendations page.'),
    ('Can I print it myself?', 'Yes. Instead of the printed part you can order the STL file for €2 and print it on your own 3D printer.'),
]
PRODUKTE_K_EN = [
    ('Keychain', 'Small, medium, large', '€7 to €9', 'With a 5 mm hole for the key ring. 9 shapes from bars to heart.'),
    ('Pendant', 'one size', '€7', 'Small and light, with a 3 mm hole. Without chain.'),
    ('Bookmark', '15 cm', '€7', 'Plate with sound wave, with a name if you like.'),
    ('Christmas ornament', 'Small, medium', '€6 to €8', 'Star, disc or heart to hang up.'),
    ('Coaster', '9.5 cm', '€8', 'For cups and glasses.'),
    ('Desk display', '10, 14, 18 cm wide', '€9.90 to €15.90', 'Skyline with a stand, with a name in the base if you like.'),
    ('Earrings', 'one pair', 'soon', 'Very light, without hooks. Not available yet.'),
    ('STL file', '–', '€2', 'To print yourself, sent by email.'),
]

KLANG_EN_SEITE = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Klangform</p>
    <h1>Sound wave as a keychain, pendant and desk display</h1>
    <p class="einleitung">Record your voice, a laugh or a heartbeat. We print a piece in the shape of your sound wave. From €6, printed in Germany.</p>
    <div class="knoepfe">
      <a class="haupt" href="{KLANGFORM}" rel="noopener" hreflang="de">Design your sound wave <span class="pfeil" aria-hidden="true">→</span></a>
      <a class="zweit" href="#prices">See prices</a>
    </div>
    {NUR_DEUTSCH}
    {AUSVERKAUFT_EN}
  </div>
  <div class="bett">{KLANG_EN}<p class="unterschrift">Keychain, bar shape. Every wave is unique.</p></div>
</section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">How it works</p><h2>From sound to keychain in two minutes</h2></div>
  <ol class="ablauf">
    <li><h3>Record</h3><p>Record directly in your browser or choose an audio or video file. 2 to 5 seconds are enough.</p></li>
    <li><h3>Choose a shape</h3><p>Bars, wave, round, ring, plate, heart, star, disc, infinity or skyline. Then size and colour.</p></li>
    <li><h3>Order</h3><p>You pay with PayPal. We print and ship your piece within Germany.</p></li>
  </ol>
  {NUR_DEUTSCH}
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Occasions</p><h2>A gift that sounds like you</h2>
    <p>A sound wave keychain holds on to a moment you could otherwise only hear.</p></div>
  <ul class="chips">
    <li>“I love you” for an anniversary</li><li>The “I do” at the wedding</li><li>A heartbeat from the ultrasound</li>
    <li>Your child’s name</li><li>The first “Mama” or “Papa”</li><li>Grandchildren laughing, for grandparents</li>
    <li>A voice message from a loved one</li><li>A clip from your song</li><li>Christmas ornament with a child’s voice</li>
  </ul>
</div></section>

<section class="abschnitt" id="prices"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Products and prices</p><h2>What we print from your sound wave</h2>
    <p>All pieces are solid, made in one part and one colour, with no small parts. Final prices; as a small business we do not charge VAT. Shipping within Germany €2.95. {VERSAND_EN}</p></div>
  <div class="tabelle-huelle"><table>
    <thead><tr><th scope="col">Product</th><th scope="col">Size</th><th scope="col">Price</th><th scope="col">Details</th></tr></thead>
    <tbody>{''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td class="preis">{c}</td><td>{d}</td></tr>' for a, b, c, d in PRODUKTE_K_EN)}</tbody>
  </table></div>
  {AUSVERKAUFT_EN}
  <div class="knoepfe"><a class="haupt" href="{KLANGFORM}" rel="noopener" hreflang="de">Go to Klangform <span class="pfeil" aria-hidden="true">→</span></a></div>
  {NUR_DEUTSCH}
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Privacy</p><h2>Your recording stays with you</h2>
    <p>Klangform needs no server for your recording. Your browser calculates the sound wave. Only the numbers for the shape go into the order, never the sound itself. No cookies, no tracking.</p></div>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Questions</p><h2>Frequently asked questions about the sound wave keychain</h2></div>
  {fragen_html(K_FRAGEN_EN)}
</div></section>
</main>'''

seite('en/sound-wave-keychain.html', 'Sound wave keychain – personalised and 3D-printed | Klangform',
      'Your voice as a sound wave keychain, pendant, bookmark or desk display. Recorded in your browser, 3D-printed in Germany, from €6.',
      KLANG_EN_SEITE, ld=[kruemel(('en/index.html', 'Home'), ('en/sound-wave-keychain.html', 'Klangform')),
                          {"@context": "https://schema.org", "@type": "Product", "name": "Klangform sound wave keychain",
                           "description": "Personalised 3D-printed keychain, pendant, bookmark, Christmas ornament, coaster or desk display in the shape of your own sound wave.",
                           "image": BASIS + "img/vorschau.png", "brand": {"@type": "Brand", "name": "Klangform"}, "category": "Personalised gifts",
                           "material": "PLA", "manufacturer": {"@id": BASIS + "#organisation"},
                           "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": "6.00", "highPrice": "15.90", "offerCount": "7",
                                      "availability": "https://schema.org/InStock" if DRUCK_VERFUEGBAR else "https://schema.org/OutOfStock", "url": KLANGFORM,
                                      "seller": {"@id": BASIS + "#organisation"}}},
                          fragen_ld(K_FRAGEN_EN)])

W_FRAGEN_EN = [
    ('Which files can I upload?', 'GPX and FIT files. You get them from Garmin Connect, Strava, Komoot, Wahoo, Suunto, Polar and most other apps for watches and bike computers.'),
    ('Where does the terrain come from?', 'From worldwide elevation data (AWS Terrain Tiles). Your relief shows the mountains and valleys around your route, not just the line.'),
    ('What is the difference between Basic, Premium and Real?', 'Basic: terrain in one colour, the route as a separate red part to plug in. Premium: terrain in 2 to 4 colour bands by height, from green to white. Real: terrain in real colours, with water, forest, meadow and rock.'),
    ('How big is the relief?', 'Round, square or hexagonal, 60, 100 or 150 mm. There is a base plate with title, date, time, kilometres, metres of climbing and, if you like, the elevation profile.'),
    ('Does my route leave my device?', 'Your file stays in your browser. Only a simplified route goes into the order code, so that we can print the model.'),
    ('Do you ship outside Germany?', VERSAND_EN),
    ('Is there a pendant too?', 'Yes. The pendant (50 mm) shows your route, has a hole at the top and the name and time on the back.'),
]
EXPORT_EN = [
    ('Garmin Connect', 'Open the activity, click the gear icon at the top right, then “Export to GPX” or “Export Original” (FIT).'),
    ('Strava', 'Open the activity on a computer, click the three dots on the left, then “Export GPX”.'),
    ('Komoot', 'Open the tour on a computer, click the three dots, then “Download” or “Download GPX file”.'),
    ('Other watches and apps', 'Look in the activity menu for “Export”, “GPX” or “Download file”.'),
]

WEG_EN_SEITE = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Wegform</p>
    <h1>Your hiking route as a 3D relief</h1>
    <p class="einleitung">Upload your GPX or FIT file. We print the real terrain around your tour, with your route in red. For the summit hike, the marathon or the alpine pass.</p>
    <div class="knoepfe">
      <a class="haupt" href="{WEGFORM}" rel="noopener" hreflang="de">Design your relief <span class="pfeil" aria-hidden="true">→</span></a>
      <a class="zweit" href="#gpx">Find your GPX file</a>
    </div>
    {NUR_DEUTSCH}
  </div>
  <div class="bett">{WEG_EN}<p class="unterschrift">Premium relief, hexagonal, with colour bands by height and the route.</p></div>
</section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">How it works</p><h2>From your tour to a model</h2></div>
  <ol class="ablauf">
    <li><h3>Upload your route</h3><p>GPX or FIT from your watch, bike computer or app. The file stays in your browser.</p></li>
    <li><h3>Design</h3><p>Choose the product, shape, size, colours and section. The 3D preview shows you the result right away.</p></li>
    <li><h3>Order</h3><p>You pay with PayPal. Print files are ready to download straight away. Printed reliefs are printed with 0.2 mm layers and shipped within Germany.</p></li>
  </ol>
  {NUR_DEUTSCH}
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Products</p><h2>Relief, base plate and pendant</h2></div>
  <div class="karten drei">
    <article class="karte karte-oben gruen"><div class="karte-text"><h3>Relief</h3>
      <p>Real terrain in 60, 100 or 150 mm, round, square or hexagonal.</p>
      <ul class="liste"><li>Basic: terrain in one colour, route to plug in</li><li>Premium: 2 to 4 colour bands by height</li><li>Real: water, forest, meadow and rock in real colours</li></ul></div></article>
    <article class="karte karte-oben gold"><div class="karte-text"><h3>Base plate</h3>
      <p>The frame for your relief, with raised lettering on the edge.</p>
      <ul class="liste"><li>Title, date and time</li><li>Kilometres and metres of climbing</li><li>Elevation profile if you like</li></ul></div></article>
    <article class="karte karte-oben rot"><div class="karte-text"><h3>Pendant</h3>
      <p>Your route to take with you, 50 mm, with a hole.</p>
      <ul class="liste"><li>Round, square or hexagonal</li><li>Name and time on the back</li><li>For keys, backpack or medal hanger</li></ul></div></article>
  </div>
  <p class="leise">You see the prices in the configurator before you order. {VERSAND_EN}</p>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Ideas</p><h2>Which tour will it be?</h2></div>
  <ul class="chips">
    <li>A summit in the Alps</li><li>Crossing the Alps on the E5</li><li>A stage of the Camino de Santiago</li><li>Your first marathon</li>
    <li>Ultra trail</li><li>Road bike over a pass</li><li>Wedding hike</li><li>Your local loop</li>
    <li>A gift for the hiking club</li>
  </ul>
</div></section>

<section class="abschnitt" id="gpx"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">How to</p><h2>How to get your GPX file</h2>
    <p>Almost every sports app can save your activity as a file. This is how it works in the best-known ones:</p></div>
  <div class="tabelle-huelle"><table>
    <thead><tr><th scope="col">App</th><th scope="col">How it works</th></tr></thead>
    <tbody>{''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in EXPORT_EN)}</tbody>
  </table></div>
</div></section>

<section class="abschnitt"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">Questions</p><h2>Frequently asked questions about the 3D relief</h2></div>
  {fragen_html(W_FRAGEN_EN)}
</div></section>
</main>'''

seite('en/hiking-route-3d-relief.html', 'Hiking route as a 3D relief – print your GPX in 3D | Wegform',
      'Your hike, bike ride or marathon as a 3D-printed relief with real terrain. Upload GPX or FIT, design, order. With base plate and elevation profile.',
      WEG_EN_SEITE, ld=[kruemel(('en/index.html', 'Home'), ('en/hiking-route-3d-relief.html', 'Wegform')), fragen_ld(W_FRAGEN_EN)])

BUECHER_EN = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Books</p>
    <h1>Colouring books and sketchbooks</h1>
    <p class="einleitung">By {AUTOREN_EN}: colouring books and sketchbooks for children aged 4 and up and mandala colouring books with affirmations for adults. All are paperbacks in German, sold on Amazon.de.</p>
    <div class="knoepfe"><a class="haupt" href="#children">For children</a><a class="zweit" href="#adults">For adults</a></div>
  </div>
  {COLLAGE.replace('src="img/', 'src="../img/')}
</section>

<section class="abschnitt" id="children"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">For children</p><h2>Colour, draw, learn words</h2>
    <p>Gift ideas for children aged 4 and up: for Advent, for kindergarten or for long car journeys.</p></div>
  <div class="buecher">{''.join(buchkarte(b, True) for b in kinder)}</div>
</div></section>

<section class="abschnitt" id="adults"><div class="huelle">
  <div class="kopf-abschnitt"><p class="marke">For adults</p><h2>Mandalas with affirmations</h2>
    <p>Colouring to relax. Each mandala has a sentence to take with you through the day.</p></div>
  <div class="buecher">{''.join(buchkarte(b, True) for b in gross)}</div>
  <p class="partner-hinweis">* Affiliate link: as an Amazon Associate we earn from qualifying purchases. The price stays the same for you. You see the current price on Amazon.de.</p>
</div></section>
</main>'''

seite('en/books.html', 'Colouring books for children and mandala colouring books | BuntwerkStudio',
      'Colouring books and sketchbooks for children aged 4 and up and mandala colouring books with affirmations, in German. Paperbacks on Amazon.de.',
      BUECHER_EN, ld=[kruemel(('en/index.html', 'Home'), ('en/books.html', 'Books')),
                      {"@context": "https://schema.org", "@type": "ItemList", "name": "Books by BuntwerkStudio",
                       "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": buch_ld(b)} for i, b in enumerate(BUCHLISTE)]}])

# Suchbegriffe bleiben deutsch (amazon.de, Partner-ID gilt nur dort)
GRUPPEN_EN = [
    ('For your Klangform piece', 'gold', 'We deliver pendants, bookmarks and Christmas ornaments without chain or ribbon. These go well with them:', [
        ('Necklace for pendants', 'Thin chain with a small clasp. Our hole is 3.2 mm.', 'Halskette Edelstahl dünn Damen'),
        ('Key rings', 'For the 5 mm hole on the keychain.', 'Schlüsselringe 25mm Edelstahl'),
        ('Satin ribbon', 'For bookmarks and Christmas ornaments.', 'Satinband 3mm'),
        ('Earring hooks', 'For the earrings, made of skin-friendly material.', 'Ohrhaken Titan hypoallergen'),
    ]),
    ('For your Wegform relief', 'gruen', 'So that your relief tells even more:', [
        ('Wall shelf or picture ledge', 'To display the relief and base plate.', 'Bilderleiste Holz 60cm'),
        ('Medal hanger', 'For runners: medal and Wegform pendant in one place.', 'Medaillenhalter Laufen'),
    ]),
    ('For self-printers', 'blau', 'You bought the STL file and print it yourself? This is what we print with:', [
        ('PLA filament 1.75 mm', 'PLA is enough for all Klangform parts, 100 % infill, 0.2 mm layer height.', 'PLA Filament 1,75mm 1kg'),
        ('0.4 mm nozzle', 'Our parts are designed for a 0.4 mm nozzle.', 'Düse 0,4mm 3D Drucker'),
        ('Bed adhesive', 'So that flat parts stay flat on the print bed.', 'Druckbett Haftspray 3D Druck'),
    ]),
]


def gruppen_html_en():
    out = []
    for titel, farbe, text, eintraege in GRUPPEN_EN:
        karten = ''.join(f'<article class="karte karte-oben {farbe}"><div class="karte-text"><h3>{n}</h3><p>{b}</p>'
                         f'<div class="knoepfe">{partnerlink(amazon_suche(s), "View on Amazon.de")}</div></div></article>'
                         for n, b, s in eintraege)
        out.append(f'<section class="abschnitt"><div class="huelle"><div class="kopf-abschnitt"><h2>{titel}</h2><p>{text}</p></div>'
                   f'<div class="karten drei">{karten}</div></div></section>')
    return ''.join(out)


EMPF_EN = f'''<main>
<section class="huelle held">
  <div>
    <p class="marke">Recommendations</p>
    <h1>What goes with our pieces</h1>
    <p class="einleitung">Accessories we use ourselves or that go with our prints. The links lead to a search on Amazon.de, so you can compare for yourself.</p>
    <p class="partner-hinweis">All links marked with * are affiliate links. As an Amazon Associate we earn from qualifying purchases. If you buy through them, we receive a small commission. The price stays the same for you. More in our <a href="../datenschutz.html#partnerprogramm" hreflang="de">privacy policy (German)</a>.</p>
  </div>
  <div class="bett">{KLANG_EN}</div>
</section>
{gruppen_html_en()}
</main>'''

seite('en/recommendations.html', 'Accessories for sound wave keychains and 3D reliefs | BuntwerkStudio',
      'Chains, key rings, ribbons, picture ledges and filament: accessories that go with the 3D prints from Klangform and Wegform.',
      EMPF_EN, ld=[kruemel(('en/index.html', 'Home'), ('en/recommendations.html', 'Recommendations'))])

# ---------------------------------------------------------------- robots, sitemap

with open(os.path.join(ZIEL, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\n\nSitemap: {BASIS}sitemap.xml\n')

sm = [('index.html', '1.0'), ('schallwelle-anhaenger.html', '0.9'), ('wanderroute-3d-relief.html', '0.9'),
      ('buecher.html', '0.7'), ('empfehlungen.html', '0.5'), ('impressum.html', '0.2'), ('datenschutz.html', '0.2')]
sm += [(EN[d], prio) for d, prio in sm if d in EN]
with open(os.path.join(ZIEL, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
    for p, prio in sm:
        paar = EN.get(p) or DE.get(p)
        alt = '' if not paar else ''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{adresse(d)}"/>'
                                          for h, d in (('de', DE.get(p, p)), ('en', EN.get(p, p)), ('x-default', DE.get(p, p))))
        f.write(f'  <url><loc>{adresse(p)}</loc><lastmod>{GEAENDERT}</lastmod><priority>{prio}</priority>{alt}</url>\n')
    f.write('</urlset>\n')

# Bild für die Vorschau (SVG) – wird in PNG umgewandelt
with open(os.path.join(tempfile.gettempdir(), 'held.svg'), 'w') as f:
    f.write(HELD_BILD.replace('<svg ', '<svg width="1000" height="800" ', 1))
print('fertig')
