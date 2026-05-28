// WIBWUB Service Worker — auto-update on new version
const CACHE = 'wibwub-v40';
const FILES = [
  '/Wibwub-Dashboard/WIBWUB_Mobile.html',
  '/Wibwub-Dashboard/manifest.json',
  '/Wibwub-Dashboard/icon-180.png',
  '/Wibwub-Dashboard/icon-192.png',
  '/Wibwub-Dashboard/icon-512.png',
  '/Wibwub-Dashboard/logo-header.png',
];

// Install: cache all files, activate immediately (don't wait)
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(FILES))
  );
});

// Activate: delete old caches, take control of all open pages now
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch: network first Ã¢ÂÂ if offline fallback to cache
self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
