// WIBWUB Service Worker — auto-update on new version
const CACHE = 'wibwub-v625';
const FILES = [
  '/Wibwub-Dashboard/WIBWUB_Mobile.html',
  '/Wibwub-Dashboard/manifest.json',
  '/Wibwub-Dashboard/icon-180.png',
  '/Wibwub-Dashboard/icon-192.png',
  '/Wibwub-Dashboard/icon-512.png',
  '/Wibwub-Dashboard/logo-header.png',
];

// Install: cache all files, activate immediately
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(FILES))
  );
});

// Activate: delete old caches, take control now
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch: network first, cache fallback
// IMPORTANT: skip Firebase / Google API requests (POST + streaming — cannot cache)
self.addEventListener('fetch', e => {
  const url = e.request.url;

  // Skip non-GET and all Firebase/Google domains
  if (
    e.request.method !== 'GET' ||
    url.includes('firebaseio.com') ||
    url.includes('googleapis.com') ||
    url.includes('firebaseapp.com') ||
    url.includes('gstatic.com') ||
    url.includes('firebase') ||
    url.includes('identitytoolkit')
  ) return; // let browser handle directly, no service worker interference

  e.respondWith(
    fetch(e.request)
      .then(res => {
        if (res && res.status === 200 && res.type !== 'opaque') {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
