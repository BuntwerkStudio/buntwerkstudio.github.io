#!/usr/bin/env python3
"""Prüft die zweisprachige Website (Aufgabe B7): python3 tools/sprache-pruefen.py (nach tools/seiten-bauen.py).
1. Englische Seiten: lang="en", kein deutscher Rest (Umlaute, ß, „) außerhalb von Stellen mit lang="de" und außerhalb von Skripten.
2. Jede Seite hat den Schalter „DE | EN“, gepaarte Seiten verweisen per hreflang aufeinander, die Sitemap kennt alle.
3. Alle lokalen Links, Bilder, Skripte und Stile zeigen auf vorhandene Dateien."""
import glob, os, re, sys

ZIEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://buntwerkstudio.github.io/'
fehler = []


def lesen(p):
    with open(os.path.join(ZIEL, p), encoding='utf-8') as f:
        return f.read()


def ohne_deutsch(html):
    html = re.sub(r'<script\b.*?</script>', '', html, flags=re.S)
    # Elemente mit lang="de" (auch verschachtelt gleicher Art: von innen nach außen entfernen)
    alt = None
    while alt != html:
        alt = html
        html = re.sub(r'<(\w+)\b[^>]*\blang="de"[^>]*>(?:(?!<\1\b).)*?</\1>', '', html, flags=re.S)
    return re.sub(r'\b(href|src)="[^"]*"', '', html)   # Adressen dürfen deutsch sein (amazon.de-Suchen, Dateinamen)


seiten = sorted(p.replace(os.sep, '/') for p in glob.glob('*.html', root_dir=ZIEL) + glob.glob('en/*.html', root_dir=ZIEL))
englisch = [p for p in seiten if p.startswith('en/')]
if len(englisch) < 5:
    fehler.append(f'zu wenige englische Seiten: {englisch}')
karte = lesen('sitemap.xml')

for p in seiten:
    html = lesen(p)
    en = p.startswith('en/')
    if p != '404.html' and 'class="sprache"' not in html:
        fehler.append(f'{p}: Sprachschalter fehlt')
    if f'<html lang="{"en" if en else "de"}">' not in html:
        fehler.append(f'{p}: falsches lang')
    if en:
        rest = ohne_deutsch(html)
        for m in re.finditer(r'[äöüÄÖÜß„]', rest):
            fehler.append(f'{p}: deutscher Rest „{rest[max(0, m.start() - 40):m.end() + 20].strip()}“')
            break
        if 'hreflang="de"' not in html or 'hreflang="x-default"' not in html:
            fehler.append(f'{p}: hreflang fehlt')
    if p not in ('404.html',) and (BASIS + (p[:-10] if p.endswith('index.html') else p)) not in karte:
        fehler.append(f'{p}: fehlt in sitemap.xml')
    # lokale Ziele
    for ziel in re.findall(r'\b(?:href|src)="([^"#?]+)', html):
        if re.match(r'(https?:|mailto:|data:)', ziel):
            continue
        pfad = ziel.lstrip('/') if ziel.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(p), ziel)).replace(os.sep, '/')
        if pfad.endswith('/') or pfad in ('', '.'):
            pfad = (pfad.rstrip('/') + '/index.html').lstrip('./') if pfad not in ('', '.') else 'index.html'
        if not os.path.exists(os.path.join(ZIEL, pfad)):
            fehler.append(f'{p}: Link „{ziel}“ zeigt ins Leere')

# Gepaarte Seiten verweisen aufeinander
for p in englisch:
    html = lesen(p)
    de = re.search(r'hreflang="de" href="([^"]+)"', html).group(1)
    deutsch = de.replace(BASIS, '') or 'index.html'
    if f'hreflang="en" href="{BASIS}{p[:-10] if p.endswith("index.html") else p}"' not in lesen(deutsch):
        fehler.append(f'{deutsch}: verweist nicht per hreflang auf {p}')

print('\n'.join(fehler) if fehler else f'Sprach-Prüfung bestanden ({len(seiten)} Seiten, davon {len(englisch)} englisch).')
sys.exit(1 if fehler else 0)
