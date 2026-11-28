// Untermenü in der Kopfzeile (Aufgabe 2026-11-27_website_menue-gestalten, 28.11.2026).
// Das Menü ist ein <details>: Auf- und Zuklappen per Klick, Tippen, Enter und Leertaste kann der Browser selbst,
// auch ohne JavaScript. Hier kommen nur dazu: aria-expanded, Esc schließt, Klick daneben schließt.
(function () {
  var menues = document.querySelectorAll('.menue details.untermenue');
  if (!menues.length) return;
  function zu(d) { if (d.open) d.open = false; }
  Array.prototype.forEach.call(menues, function (d) {
    var knopf = d.querySelector('summary');
    d.addEventListener('toggle', function () {
      knopf.setAttribute('aria-expanded', d.open ? 'true' : 'false');
    });
    d.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.key === 'Esc') && d.open) { zu(d); knopf.focus(); }
    });
    d.addEventListener('focusout', function (e) {
      if (e.relatedTarget && !d.contains(e.relatedTarget)) zu(d);
    });
  });
  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(menues, function (d) { if (!d.contains(e.target)) zu(d); });
  });
})();
