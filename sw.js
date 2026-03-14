/* 오프라인용 껍데기만 캐시 — 데이터는 항상 네트워크 */
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open("v1").then((c) => c.addAll(["./index.html", "./manifest.json"]).catch(() => {})));
  self.skipWaiting();
});
self.addEventListener("fetch", (e) => {
  if (e.request.mode === "navigate") {
    e.respondWith(fetch(e.request).catch(() => caches.match("./index.html")));
  }
});
