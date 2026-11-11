// 4K Pursuit service worker: works offline, always tries the network first for the page and the plan.
const CACHE='ip4k-__VER__';
const SHELL=['./','index.html','plan.json','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png','icons/maskable-512.png','icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const req=e.request; if(req.method!=='GET') return;
  const url=new URL(req.url);
  const fresh=req.mode==='navigate'||url.pathname.endsWith('/plan.json')||url.pathname.endsWith('/index.html');
  if(url.origin===location.origin&&fresh){
    e.respondWith(fetch(req).then(r=>{const cp=r.clone();caches.open(CACHE).then(c=>c.put(req.mode==='navigate'?'index.html':req,cp));return r}).catch(()=>caches.match(req.mode==='navigate'?'index.html':req).then(r=>r||caches.match('./'))));
    return;
  }
  if(url.origin===location.origin||/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)){
    e.respondWith(caches.match(req).then(hit=>{const net=fetch(req).then(r=>{if(r.ok||r.type==='opaque'){const cp=r.clone();caches.open(CACHE).then(c=>c.put(req,cp))}return r}).catch(()=>hit);return hit||net}));
  }
});
