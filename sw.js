/* Service worker — caches static assets so the second visit is instant
   even on trash internet. Cache-first for everything in CACHE_FILES,
   stale-while-revalidate for /assets/*, network for HTML/JSON. */

const CACHE_NAME = 'econ-v2026-05-29-3-1780065075';
const CACHE_FILES = [
  // Fonts
  '/assets/fonts/fonts.css',
  '/assets/fonts/BebasNeue-Regular.woff2',
  '/assets/fonts/Syne-700.woff2',
  '/assets/fonts/JetBrainsMono-400.woff2',
  '/assets/fonts/Syne-400.woff2',
  '/assets/fonts/JetBrainsMono-300.woff2',
  '/assets/fonts/JetBrainsMono-500.woff2',
  '/assets/fonts/Syne-600.woff2',
  '/assets/fonts/Syne-800.woff2',
  // Cinema layer
  '/assets/cinema/cinema-v2.css',
  '/assets/cinema/cinema-v2.js',
  // Voice tour (intro is preloaded separately; cache the rest)
  '/assets/audio/jarvis/intro.mp3',
  '/assets/audio/jarvis/problem.mp3',
  '/assets/audio/jarvis/operations.mp3',
  '/assets/audio/jarvis/marketing.mp3',
  '/assets/audio/jarvis/financial.mp3',
  '/assets/audio/jarvis/fullstack.mp3',
  '/assets/audio/jarvis/founders.mp3',
  '/assets/audio/jarvis/qualify.mp3',
  '/assets/audio/jarvis/faq.mp3',
];

// On install — pre-fetch and cache the static set
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(c => c.addAll(CACHE_FILES.map(u => new Request(u, {cache:'reload'}))))
  );
  self.skipWaiting();
});

// On activate — purge old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

// On fetch — cache-first for static, network for everything else
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  // Only handle same-origin GETs
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;

  // cinema-v2 JS/CSS → network-first (so edits show immediately during dev)
  if (url.pathname.includes('cinema-v2')) {
    e.respondWith(
      fetch(e.request).then(fresh => {
        if (fresh && fresh.status === 200) {
          const clone = fresh.clone();
          caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
        }
        return fresh;
      }).catch(() => caches.match(e.request))
    );
    return;
  }
  // Other /assets/ (fonts, audio) → cache-first with background refresh
  if (url.pathname.startsWith('/assets/')) {
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) {
          fetch(e.request).then(fresh => {
            if (fresh && fresh.status === 200) {
              caches.open(CACHE_NAME).then(c => c.put(e.request, fresh));
            }
          }).catch(() => {});
          return cached;
        }
        return fetch(e.request).then(fresh => {
          if (fresh && fresh.status === 200) {
            const clone = fresh.clone();
            caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
          }
          return fresh;
        });
      })
    );
    return;
  }

  // HTML — network-first with cache fallback
  if (e.request.headers.get('accept')?.includes('text/html')) {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request))
    );
    return;
  }
});
