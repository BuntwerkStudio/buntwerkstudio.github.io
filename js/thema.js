// Hell/Dunkel-Schalter in der BuntwerkStudio-Kopfzeile (Website, Klangform B12, Wegform B18).
// Gleiche Datei in allen drei Repositories. Normales Skript (kein Modul) im <head>, damit data-theme
// vor dem ersten Zeichnen gesetzt ist und nichts aufblitzt. Kein fremder Server.
// Stufen: auto (wie das Gerät, Standard) → light → dark → auto. Gemerkt in localStorage „buntwerk-thema“.
(function () {
  var SCHLUESSEL = 'buntwerk-thema';
  var STUFEN = ['auto', 'light', 'dark'];
  var TEXT = { auto: 'Automatisch (wie dein Gerät)', light: 'Hell', dark: 'Dunkel' };
  var root = document.documentElement;

  var ohneSpeicher = null; // ohne localStorage gilt die Wahl nur bis zum Neuladen
  function lesen() {
    if (ohneSpeicher) return ohneSpeicher;
    try { var t = localStorage.getItem(SCHLUESSEL); return t === 'light' || t === 'dark' ? t : 'auto'; } catch (e) { return 'auto'; }
  }
  function schreiben(t) {
    try { if (t === 'auto') localStorage.removeItem(SCHLUESSEL); else localStorage.setItem(SCHLUESSEL, t); ohneSpeicher = null; } catch (e) { ohneSpeicher = t; }
  }
  function setzen(t) {
    if (t === 'auto') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', t);
  }
  // Tatsächlich sichtbares Thema (für Teile, die ihre Farben nicht aus CSS-Variablen holen)
  function sichtbar() {
    var t = lesen();
    if (t !== 'auto') return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function melden() {
    try { window.dispatchEvent(new CustomEvent('buntwerk-thema', { detail: { wahl: lesen(), sichtbar: sichtbar() } })); } catch (e) { /* alte Browser */ }
  }

  setzen(lesen());

  var SVG = {
    auto: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor"/></svg>',
    light: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4.2" fill="currentColor"/><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></g></svg>',
    dark: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.5 14.6A8.6 8.6 0 0 1 9.4 3.5a8.6 8.6 0 1 0 11.1 11.1z" fill="currentColor"/></svg>',
  };

  function knopfZeigen(k) {
    var t = lesen();
    var naechste = STUFEN[(STUFEN.indexOf(t) + 1) % STUFEN.length];
    k.innerHTML = SVG[t];
    k.setAttribute('aria-label', 'Darstellung: ' + TEXT[t] + '. Klicken für: ' + TEXT[naechste]);
    k.title = 'Darstellung: ' + TEXT[t];
    k.setAttribute('data-wahl', t);
  }

  function einbauen() {
    var zeile = document.querySelector('.buntwerk-kopf .kopfzeile, header.kopfzeile');
    if (!zeile || zeile.querySelector('.thema-knopf')) return;
    var k = document.createElement('button');
    k.type = 'button';
    k.className = 'thema-knopf';
    knopfZeigen(k);
    k.addEventListener('click', function () {
      var t = STUFEN[(STUFEN.indexOf(lesen()) + 1) % STUFEN.length];
      schreiben(t);
      setzen(t);
      knopfZeigen(k);
      melden();
    });
    zeile.appendChild(k);
  }

  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var neu = function () { if (lesen() === 'auto') melden(); };
    if (mq.addEventListener) mq.addEventListener('change', neu); else if (mq.addListener) mq.addListener(neu);
  }
  // Wahl in einem anderen Tab geändert
  window.addEventListener('storage', function (e) {
    if (e.key !== SCHLUESSEL) return;
    setzen(lesen());
    var k = document.querySelector('.thema-knopf');
    if (k) knopfZeigen(k);
    melden();
  });

  window.buntwerkThema = { wahl: lesen, sichtbar: sichtbar };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', einbauen); else einbauen();
})();
