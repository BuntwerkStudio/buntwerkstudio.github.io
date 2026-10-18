// Amazon-Partner-Kennung (Tracking-ID aus PartnerNet), z. B. 'buntwerk-21'.
// Hier eintragen, dann tragen alle Amazon-Links auf der Seite die Kennung.
const AMAZON_TAG = '';

if (AMAZON_TAG) {
  document.querySelectorAll('a[data-amazon]').forEach((a) => {
    try {
      const url = new URL(a.href);
      url.searchParams.set('tag', AMAZON_TAG);
      a.href = url.toString();
    } catch (e) { /* Link unverändert lassen */ }
  });
}
