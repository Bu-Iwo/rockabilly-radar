/*
  ROCKABILLY RADAR – Offline-Speicher (Service Worker)
  Diese Datei muss nicht angepasst werden.

  Wie es funktioniert:
  - Die App-Dateien und alle Termine werden auf dem Handy zwischengespeichert, damit die App auch ohne Netz startet.
  - Ist eine Internetverbindung da, holt die App immer zuerst die neueste Version von GitHub.
    Neue Termine erscheinen also, sobald du die Dateien hochgeladen hast und die App das nächste Mal geöffnet wird.
  - Kartenbilder (OpenStreetMap) werden nicht gespeichert. Ohne Netz zeigt die App die vereinfachte Europakarte.
*/

var CACHE = 'rr-v1';
var DATEIEN = [
  './', 'index.html', 'europe.js', 'events.js',
  'events-country-1.js', 'events-country-2.js', 'events-country-3.js', 'pruefung.js', 'uebersetzung-en.js',
  'manifest.json', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png'
];
var SCHRIFTEN = ['fonts.googleapis.com', 'fonts.gstatic.com'];
var WARTEZEIT = 4000;

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return Promise.all(DATEIEN.map(function (d) {
        return cache.add(new Request(d, { cache: 'reload' })).catch(function () { /* einzelne Datei fehlt: weiter */ });
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (namen) {
      return Promise.all(namen.filter(function (n) { return n !== CACHE; }).map(function (n) { return caches.delete(n); }));
    }).then(function () { return self.clients.claim(); })
  );
});

/* Zuerst Netz (frische Termine), bei Ausfall oder langsamer Verbindung der gespeicherte Stand */
function netzZuerst(request, istSeite) {
  return new Promise(function (resolve) {
    var fertig = false;
    function ausCache() {
      return caches.match(request, { ignoreSearch: true }).then(function (r) {
        return r || (istSeite ? caches.match('index.html') : null);
      });
    }
    var timer = setTimeout(function () {
      ausCache().then(function (r) { if (r && !fertig) { fertig = true; resolve(r); } });
    }, WARTEZEIT);
    fetch(request.url, { cache: 'no-cache', credentials: 'same-origin' }).then(function (antwort) {
      clearTimeout(timer);
      if (antwort && antwort.ok) {
        var kopie = antwort.clone();
        caches.open(CACHE).then(function (c) { c.put(request.url, kopie); });
      }
      if (!fertig) { fertig = true; resolve(antwort); }
    }).catch(function () {
      clearTimeout(timer);
      ausCache().then(function (r) {
        if (!fertig) { fertig = true; resolve(r || Response.error()); }
      });
    });
  });
}

/* Schriften: gespeicherte Version sofort, im Hintergrund erneuern */
function schriften(request) {
  return caches.open(CACHE).then(function (cache) {
    return cache.match(request).then(function (gespeichert) {
      var holen = fetch(request).then(function (antwort) {
        if (antwort && (antwort.ok || antwort.type === 'opaque')) { cache.put(request, antwort.clone()); }
        return antwort;
      }).catch(function () { return gespeichert; });
      return gespeichert || holen;
    });
  });
}

self.addEventListener('fetch', function (event) {
  var request = event.request;
  if (request.method !== 'GET') { return; }
  var url = new URL(request.url);
  if (url.origin === self.location.origin) {
    event.respondWith(netzZuerst(request, request.mode === 'navigate'));
  } else if (SCHRIFTEN.indexOf(url.hostname) !== -1) {
    event.respondWith(schriften(request));
  }
  /* alles andere (Karte, Buchungsseiten) läuft ganz normal übers Netz */
});
