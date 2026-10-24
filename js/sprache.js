// Sprachwechsel „DE | EN“ in der BuntwerkStudio-Kopfzeile (Website, Aufgabe B7 = Klangform B13 = Wegform B19).
// Der Schalter selbst ist ein normaler Link zur gleichen Seite in der anderen Sprache (tools/seiten-bauen.py).
// Dieses Skript merkt die Wahl in localStorage „buntwerk-sprache“ und schlägt beim ersten Besuch die Sprache
// des Browsers vor, wenn sie nicht zur Seite passt. Es leitet nie automatisch um. Kein fremder Server.
(function () {
  var SCHLUESSEL = 'buntwerk-sprache';
  var seite = (document.documentElement.getAttribute('lang') || 'de').slice(0, 2) === 'en' ? 'en' : 'de';
  var TEXT = {
    en: { satz: 'This page is also available in English.', link: 'Read in English', zu: 'Close' },
    de: { satz: 'Diese Seite gibt es auch auf Deutsch.', link: 'Auf Deutsch lesen', zu: 'Schließen' },
  };

  function lesen() {
    try { var s = localStorage.getItem(SCHLUESSEL); return s === 'de' || s === 'en' ? s : null; } catch (e) { return null; }
  }
  function schreiben(s) {
    try { localStorage.setItem(SCHLUESSEL, s); } catch (e) { /* ohne Speicher gilt die Wahl nur für diesen Besuch */ }
  }
  function browser() {
    var l = (navigator.languages && navigator.languages[0]) || navigator.language || 'de';
    return /^de\b/i.test(l) ? 'de' : 'en';
  }

  function vorschlagen(schalter, sprache) {
    var ziel = schalter.querySelector('a[data-sprache="' + sprache + '"]');
    var kopf = schalter.closest('header');
    if (!ziel || !kopf || document.querySelector('.sprach-hinweis')) return;
    var t = TEXT[sprache];
    var huelle = document.createElement('div');
    huelle.className = 'huelle';
    var box = document.createElement('div');
    box.className = 'sprach-hinweis';
    box.setAttribute('role', 'note');
    box.setAttribute('lang', sprache);
    var p = document.createElement('p');
    p.textContent = t.satz;
    var a = document.createElement('a');
    a.className = 'zweit';
    a.href = ziel.getAttribute('href');
    a.hreflang = sprache;
    a.textContent = t.link;
    a.addEventListener('click', function () { schreiben(sprache); });
    var zu = document.createElement('button');
    zu.type = 'button';
    zu.className = 'sprach-zu';
    zu.setAttribute('aria-label', t.zu);
    zu.textContent = '×';
    zu.addEventListener('click', function () { schreiben(seite); huelle.remove(); });
    box.appendChild(p); box.appendChild(a); box.appendChild(zu);
    huelle.appendChild(box);
    kopf.parentNode.insertBefore(huelle, kopf.nextSibling);
  }

  function einbauen() {
    var schalter = document.querySelector('.sprache');
    if (!schalter) return;
    Array.prototype.forEach.call(schalter.querySelectorAll('a[data-sprache]'), function (a) {
      a.addEventListener('click', function () { schreiben(a.getAttribute('data-sprache')); });
    });
    var wunsch = lesen() || browser();
    if (wunsch !== seite) vorschlagen(schalter, wunsch);
  }

  window.buntwerkSprache = { wahl: lesen, seite: seite };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', einbauen); else einbauen();
})();
