const CACHE_NAME = 'rockabilly-radar-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/events.json'
];

// Installieren – Cache aufbauen
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache geöffnet');
        return cache.addAll(urlsToCache);
      })
  );
});

// Aktivieren – Alten Cache aufräumen
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch – Netzwerk-Anfragen abfangen
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Wenn im Cache gefunden, zurückgeben
        if (response) {
          return response;
        }
        // Sonst aus dem Netzwerk laden
        return fetch(event.request).then(
          response => {
            // Prüfen ob Antwort gültig
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Antwort in den Cache legen
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
  );
});

