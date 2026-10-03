// WIBWUB Service Worker — auto-update on new version
const CACHE = 'wibwub-v1387';
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

  // IMPORTANT: force bypass of the browser's HTTP disk cache on every fetch.
  // Without {cache:'no-store'} here, a plain fetch(e.request) still honors
  // normal HTTP caching rules (e.g. GitHub Pages' Cache-Control: max-age),
  // so even "network-first" can silently return a stale disk-cached response
  // instead of hitting the network — and a user's hard-refresh (Cmd+Shift+R)
  // does NOT force this internal fetch() to bypass cache, because the browser's
  // hard-reload signal doesn't propagate through the service worker's fetch
  // interception. This was the root cause of dashboards looking "stuck" on old
  // data even after every device did a manual hard refresh.
  const freshRequest = new Request(e.request, { cache: 'no-store' });
  e.respondWith(
    fetch(freshRequest)
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
