#!/usr/bin/env python3
"""Build index.html (the full Ravish House bookstore) from data.json.

Keeps data.json as the single source of truth and inlines the catalog into
index.html so the site works both when served and when opened from file://.
Real cover images are used from covers/<id>-<n>.png when present; otherwise a
themed CSS placeholder cover is shown (via <img onerror>).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")
OUT = os.path.join(ROOT, "index.html")

# Per-series visual identity: gradient colors + motif emoji for placeholder covers.
THEME = {
    "love-by-the-numbers":   ("#0f4c5c", "#e9c46a", "📊"),
    "fathoms-of-the-heart":  ("#02182b", "#2a9d8f", "⚓"),
    "rind-and-the-reckless": ("#8a5a00", "#f4d58d", "🧀"),
    "below-zero-above-reason":("#1b3a5b", "#a8e0e6", "❄️"),
    "leave-no-trace":        ("#2d5016", "#9bc53d", "♻️"),
    "nothing-matters":       ("#161320", "#6c5b7b", "🌌"),
    "magma-rising":          ("#3b0d0c", "#ff6d00", "🌋"),
    "bunker-down":           ("#2b2b1f", "#c9a227", "☢️"),
    "between-the-flags":     ("#005f73", "#ffd166", "🛟"),
    "not-a-minute-late":     ("#1d2d44", "#b08968", "⏱️"),
    "sweetest-sting":        ("#7a5901", "#ffd60a", "🐝"),
    "cooking-the-books":     ("#14261a", "#4caf50", "📒"),
}


def enrich(catalog):
    for s in catalog["series"]:
        c1, c2, emoji = THEME.get(s["id"], ("#5a2a3a", "#d1a3b0", "❤️"))
        s["c1"], s["c2"], s["emoji"] = c1, c2, emoji
        for i, b in enumerate(s["books"], 1):
            b["cover"] = f"covers/{s['id']}-{i}.png"
            b["n"] = i
    return catalog


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ravish House — Love, in the unlikeliest places</title>
<style>
  :root{
    --ink:#241a15; --paper:#f7f1e6; --card:#fffdf8; --line:#e5d8c2;
    --accent:#8a2f3f; --accent2:#b0475a; --muted:#7c6f5e; --gold:#b08d3f;
    --shadow:0 8px 24px rgba(60,40,20,.16);
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{margin:0;background:var(--paper);color:var(--ink);
    font-family:"Iowan Old Style",Georgia,"Times New Roman",serif;line-height:1.55;}
  a{color:inherit;text-decoration:none;}
  img{max-width:100%;display:block;}

  header.site{position:sticky;top:0;z-index:50;background:rgba(247,241,230,.94);
    backdrop-filter:blur(6px);border-bottom:1px solid var(--line);}
  .bar{max-width:1160px;margin:0 auto;display:flex;align-items:center;gap:1rem;
    padding:.8rem 1.25rem;}
  .brand{cursor:pointer;display:flex;flex-direction:column;line-height:1.1;}
  .brand b{font-size:1.5rem;letter-spacing:.5px;}
  .brand span{font-size:.78rem;color:var(--accent);font-style:italic;}
  nav.top{margin-left:auto;display:flex;gap:1.2rem;align-items:center;}
  nav.top a{font-size:.95rem;color:var(--muted);cursor:pointer;}
  nav.top a:hover{color:var(--accent);}
  .cartbtn{background:var(--accent);color:#fff;border:none;border-radius:999px;
    padding:.5rem .95rem;font:inherit;font-size:.9rem;cursor:pointer;
    display:flex;align-items:center;gap:.4rem;}
  .cartbtn:hover{background:var(--accent2);}
  .cartbtn .badge{background:#fff;color:var(--accent);border-radius:999px;
    min-width:1.3rem;height:1.3rem;display:inline-flex;align-items:center;
    justify-content:center;font-size:.78rem;font-weight:bold;padding:0 .3rem;}

  .hero{max-width:1160px;margin:0 auto;padding:2.6rem 1.25rem 1rem;text-align:center;}
  .hero h1{font-size:2.5rem;margin:.2rem 0;}
  .hero p{color:var(--muted);max-width:680px;margin:.4rem auto 0;font-size:1.05rem;}
  .rule{width:80px;height:3px;background:var(--gold);margin:1.2rem auto;border-radius:2px;}

  main{max-width:1160px;margin:0 auto;padding:1rem 1.25rem 4rem;}
  .section-title{font-size:1.5rem;margin:1.6rem 0 1rem;display:flex;align-items:baseline;gap:.6rem;}
  .section-title small{color:var(--muted);font-size:.9rem;font-weight:normal;}

  .grid{display:grid;gap:1.4rem;}
  .series-grid{grid-template-columns:repeat(auto-fill,minmax(250px,1fr));}
  .book-grid{grid-template-columns:repeat(auto-fill,minmax(180px,1fr));}

  .series-card{background:var(--card);border:1px solid var(--line);border-radius:12px;
    overflow:hidden;box-shadow:var(--shadow);cursor:pointer;transition:transform .15s ease;
    display:flex;flex-direction:column;}
  .series-card:hover{transform:translateY(-4px);}
  .series-card .banner{height:150px;position:relative;display:flex;align-items:center;
    justify-content:center;font-size:3.4rem;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.35);}
  .series-card .body{padding:.9rem 1rem 1.1rem;}
  .series-card .theme{color:var(--accent);font-style:italic;font-size:.85rem;}
  .series-card h3{margin:.2rem 0 .3rem;font-size:1.25rem;}
  .series-card .by{color:var(--muted);font-size:.9rem;}
  .series-card .count{margin-top:.5rem;font-size:.82rem;color:var(--gold);font-weight:bold;
    text-transform:uppercase;letter-spacing:.5px;}

  /* Book cover (image or placeholder), classic 2:3 */
  .cover{position:relative;aspect-ratio:2/3;border-radius:8px;overflow:hidden;
    box-shadow:var(--shadow);background:#ddd;}
  .cover img{width:100%;height:100%;object-fit:cover;}
  .cover .ph{position:absolute;inset:0;display:flex;flex-direction:column;
    align-items:center;justify-content:space-between;padding:14% 10%;text-align:center;
    color:#fff;}
  .cover .ph .pub{font-size:.6rem;letter-spacing:2px;text-transform:uppercase;opacity:.8;}
  .cover .ph .emoji{font-size:2.6rem;filter:drop-shadow(0 2px 6px rgba(0,0,0,.4));}
  .cover .ph .t{font-size:1.02rem;font-weight:bold;line-height:1.15;
    text-shadow:0 2px 8px rgba(0,0,0,.45);}
  .cover .ph .a{font-size:.7rem;font-style:italic;opacity:.9;}

  .book{cursor:pointer;}
  .book .meta{margin-top:.55rem;}
  .book .bt{font-weight:bold;font-size:1rem;line-height:1.2;}
  .book .bp{color:var(--accent);font-weight:bold;margin-top:.15rem;}

  .btn{background:var(--accent);color:#fff;border:none;border-radius:8px;
    padding:.55rem .9rem;font:inherit;font-size:.9rem;cursor:pointer;width:100%;
    margin-top:.5rem;}
  .btn:hover{background:var(--accent2);}
  .btn.ghost{background:transparent;color:var(--accent);border:1px solid var(--accent);}

  /* Series page header */
  .series-hero{border-radius:14px;overflow:hidden;box-shadow:var(--shadow);
    margin:1.2rem 0 1.6rem;color:#fff;position:relative;}
  .series-hero .inner{padding:2rem 1.6rem;position:relative;z-index:1;}
  .series-hero .emoji{font-size:3rem;}
  .series-hero h2{font-size:2.1rem;margin:.3rem 0;}
  .series-hero .theme{font-style:italic;opacity:.95;}
  .series-hero .blurb{max-width:640px;margin-top:.7rem;opacity:.95;}
  .series-hero .author{margin-top:1rem;font-size:.95rem;opacity:.92;}
  .back{cursor:pointer;color:var(--muted);font-size:.9rem;display:inline-block;margin:.4rem 0;}
  .back:hover{color:var(--accent);}

  /* Modal */
  .modal-bg{position:fixed;inset:0;background:rgba(30,20,12,.55);z-index:100;
    display:none;align-items:center;justify-content:center;padding:1.25rem;}
  .modal-bg.show{display:flex;}
  .modal{background:var(--card);border-radius:14px;max-width:760px;width:100%;
    box-shadow:var(--shadow);max-height:90vh;overflow:auto;}
  .modal .row{display:flex;gap:1.4rem;padding:1.5rem;}
  .modal .row .mcover{flex:0 0 200px;max-width:200px;cursor:zoom-in;}
  .modal .mcap{font-size:.72rem;color:var(--muted);text-align:center;margin-top:.4rem;
    letter-spacing:.3px;}
  .modal .row .minfo{flex:1;min-width:0;}
  .modal h3{margin:.1rem 0 .2rem;font-size:1.6rem;}
  .modal .sub{color:var(--accent);font-style:italic;}
  .modal .tag{margin:.5rem 0 .2rem;font-style:italic;color:var(--gold);font-size:1.05rem;}
  .modal .desc{margin:.9rem 0;font-size:1.02rem;line-height:1.65;}
  .modal .price{font-size:1.4rem;color:var(--accent);font-weight:bold;}
  .x{float:right;font-size:1.4rem;cursor:pointer;color:var(--muted);padding:.6rem 1rem 0;}

  /* Fullscreen cover lightbox */
  .lightbox{position:fixed;inset:0;background:rgba(8,6,4,.97);z-index:300;display:none;
    align-items:center;justify-content:center;padding:1rem;cursor:zoom-out;}
  .lightbox.show{display:flex;}
  .lightbox img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;
    border-radius:8px;box-shadow:0 12px 48px rgba(0,0,0,.6);}
  .lightbox .lx{position:fixed;top:.5rem;right:.9rem;color:#fff;font-size:2.2rem;line-height:1;
    cursor:pointer;opacity:.9;text-shadow:0 2px 8px rgba(0,0,0,.6);}

  /* Cart drawer */
  .drawer-bg{position:fixed;inset:0;background:rgba(30,20,12,.45);z-index:110;display:none;}
  .drawer-bg.show{display:block;}
  .drawer{position:fixed;top:0;right:0;height:100%;width:min(420px,92vw);background:var(--card);
    z-index:120;box-shadow:-8px 0 30px rgba(0,0,0,.2);transform:translateX(100%);
    transition:transform .22s ease;display:flex;flex-direction:column;}
  .drawer.show{transform:translateX(0);}
  .drawer h3{margin:0;padding:1.1rem 1.25rem;border-bottom:1px solid var(--line);
    display:flex;justify-content:space-between;align-items:center;}
  .drawer .items{flex:1;overflow:auto;padding:.5rem 1.25rem;}
  .citem{display:flex;gap:.75rem;padding:.7rem 0;border-bottom:1px solid var(--line);align-items:center;}
  .citem .mini{width:44px;height:66px;border-radius:4px;flex:0 0 auto;box-shadow:var(--shadow);
    display:flex;align-items:center;justify-content:center;font-size:1.3rem;color:#fff;overflow:hidden;}
  .citem .mini img{width:100%;height:100%;object-fit:cover;}
  .citem .info{flex:1;font-size:.9rem;}
  .citem .rm{cursor:pointer;color:var(--muted);font-size:1.1rem;}
  .citem .rm:hover{color:var(--accent);}
  .drawer .foot{border-top:1px solid var(--line);padding:1.1rem 1.25rem;}
  .drawer .total{display:flex;justify-content:space-between;font-size:1.15rem;font-weight:bold;margin-bottom:.8rem;}
  .empty{color:var(--muted);text-align:center;padding:2rem 1rem;}

  .toast{position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%) translateY(200%);
    background:var(--ink);color:#fff;padding:.75rem 1.25rem;border-radius:999px;z-index:200;
    transition:transform .3s ease;font-size:.95rem;box-shadow:var(--shadow);}
  .toast.show{transform:translateX(-50%) translateY(0);}

  footer.site{border-top:1px solid var(--line);color:var(--muted);text-align:center;
    padding:2rem 1rem;font-size:.85rem;}
  .disclaimer{max-width:640px;margin:.6rem auto 0;font-size:.78rem;opacity:.8;}

  /* ---------- mobile ---------- */
  @media (max-width:640px){
    .bar{flex-wrap:wrap;gap:.5rem;padding:.65rem 1rem;}
    .brand b{font-size:1.3rem;}
    nav.top{gap:1rem;margin-left:auto;}
    .hero{padding:1.8rem 1rem .4rem;}
    .hero h1{font-size:1.95rem;}
    .hero p{font-size:1rem;}
    main{padding:1rem 1rem 3rem;}
    .section-title{font-size:1.3rem;}
    .book-grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:1.1rem;}
    .series-hero .inner{padding:1.4rem 1.15rem;}
    .series-hero h2{font-size:1.65rem;}
    .series-hero .emoji{font-size:2.4rem;}
    /* book modal becomes a full-screen, single-column reading sheet */
    .modal-bg{padding:0;align-items:stretch;}
    .modal{max-width:none;width:100%;border-radius:0;max-height:100vh;min-height:100vh;}
    .modal .row{flex-direction:column;gap:1rem;padding:1.15rem 1.15rem 2rem;}
    .modal .row .mcover{flex:0 0 auto;max-width:min(72vw,260px);margin:.2rem auto 0;}
    .modal h3{font-size:1.5rem;}
    .modal .desc{font-size:1.07rem;line-height:1.72;}
    .x{font-size:1.7rem;padding:.5rem .9rem 0;}
  }
</style>
</head>
<body>
<header class="site">
  <div class="bar">
    <div class="brand" onclick="go('#/')">
      <b>Ravish House</b><span>Love, in the unlikeliest places.</span>
    </div>
    <nav class="top">
      <a onclick="go('#/')">Home</a>
      <a onclick="go('#/'); setTimeout(()=>document.getElementById('catalog').scrollIntoView(),40)">Catalog</a>
      <button class="cartbtn" onclick="openCart()">🛒 Cart <span class="badge" id="cartCount">0</span></button>
    </nav>
  </div>
</header>

<div id="view"></div>

<footer class="site">
  &copy; 1987–2026 Ravish House. All passions reserved.
  <div class="disclaimer">
    Ravish House is a work of parody. All series, authors, titles, and books are
    fictional and satirical. Nothing here is for actual sale; the "checkout" is
    part of the joke.
  </div>
</footer>

<!-- Modal -->
<div class="modal-bg" id="modalBg" onclick="if(event.target===this)closeModal()">
  <div class="modal" id="modal"></div>
</div>

<!-- Cart -->
<div class="drawer-bg" id="drawerBg" onclick="closeCart()"></div>
<aside class="drawer" id="drawer">
  <h3>Your Cart <span class="x" onclick="closeCart()">&times;</span></h3>
  <div class="items" id="cartItems"></div>
  <div class="foot">
    <div class="total"><span>Total</span><span id="cartTotal">$0.00</span></div>
    <button class="btn" onclick="checkout()">Checkout</button>
    <button class="btn ghost" onclick="clearCart()" style="margin-top:.5rem;">Clear cart</button>
  </div>
</aside>

<div class="toast" id="toast"></div>

<!-- Fullscreen cover lightbox -->
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <span class="lx" onclick="closeLightbox()">&times;</span>
  <img id="lightboxImg" src="" alt="Cover">
</div>

<script id="catalog" type="application/json">__CATALOG_JSON__</script>
<script>
const CATALOG = JSON.parse(document.getElementById('catalog').textContent);
const SERIES = CATALOG.series;
const byId = Object.fromEntries(SERIES.map(s=>[s.id,s]));
const fmt = n => '$'+n.toFixed(2);

/* ---------- cover rendering (image with placeholder fallback) ---------- */
function coverHTML(s, b){
  const ph = `<div class="ph" style="background:linear-gradient(160deg,${s.c1},${s.c2})">
      <div class="pub">Ravish House</div>
      <div class="emoji">${s.emoji}</div>
      <div class="t">${esc(b.title)}</div>
      <div class="a">${esc(s.author)}</div>
    </div>`;
  return `<div class="cover">
     <img src="${b.cover}" alt="${esc(b.title)} cover" loading="lazy"
          onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
     <div style="display:none">${ph}</div>
   </div>`;
}
function miniHTML(s,b){
  return `<div class="mini" style="background:linear-gradient(160deg,${s.c1},${s.c2})">
    <img src="${b.cover}" alt="" onerror="this.replaceWith(document.createTextNode('${s.emoji}'))">
  </div>`;
}
function esc(t){return String(t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}

/* ---------- views ---------- */
function homeView(){
  const totalBooks = SERIES.reduce((a,s)=>a+s.books.length,0);
  const cards = SERIES.map(s=>`
    <div class="series-card" onclick="go('#/series/${s.id}')">
      <div class="banner" style="background:linear-gradient(160deg,${s.c1},${s.c2})">${s.emoji}</div>
      <div class="body">
        <div class="theme">${esc(s.theme)}</div>
        <h3>${esc(s.title)}</h3>
        <div class="by">by ${esc(s.author)}</div>
        <div class="count">${s.books.length} book${s.books.length>1?'s':''}</div>
      </div>
    </div>`).join('');
  return `
    <section class="hero">
      <h1>${esc(CATALOG.publisher.name)}</h1>
      <p>${esc(CATALOG.publisher.tagline)}</p>
      <div class="rule"></div>
      <p>${esc(CATALOG.publisher.about)}</p>
    </section>
    <main>
      <div class="section-title" id="catalog">Our Series <small>${SERIES.length} series · ${totalBooks} books</small></div>
      <div class="grid series-grid">${cards}</div>
    </main>`;
}

function seriesView(id){
  const s = byId[id];
  if(!s) return homeView();
  const books = s.books.map(b=>`
    <div class="book" onclick="openBook('${s.id}',${b.n})">
      ${coverHTML(s,b)}
      <div class="meta">
        <div class="bt">${esc(b.title)}</div>
        <div class="bp">${fmt(b.price)}</div>
      </div>
      <button class="btn" onclick="event.stopPropagation();addToCart('${s.id}',${b.n})">Add to Cart</button>
    </div>`).join('');
  return `
    <main>
      <div class="back" onclick="go('#/')">&larr; All series</div>
      <div class="series-hero">
        <div style="position:absolute;inset:0;background:linear-gradient(135deg,${s.c1},${s.c2})"></div>
        <div class="inner">
          <div class="emoji">${s.emoji}</div>
          <div class="theme">${esc(s.theme)}</div>
          <h2>${esc(s.title)}</h2>
          <div class="blurb">${esc(s.blurb)}</div>
          <div class="author"><strong>${esc(s.author)}</strong> — ${esc(s.authorBio)}</div>
        </div>
      </div>
      <div class="section-title">Books in this series <small>${s.books.length} title${s.books.length>1?'s':''}</small></div>
      <div class="grid book-grid">${books}</div>
    </main>`;
}

/* ---------- book modal ---------- */
function openBook(sid,n){
  const s=byId[sid], b=s.books[n-1];
  document.getElementById('modal').innerHTML = `
    <span class="x" onclick="closeModal()">&times;</span>
    <div class="row">
      <div class="mcover" onclick="openLightbox('${b.cover}')" title="View larger">
        ${coverHTML(s,b)}<div class="mcap">Tap to enlarge</div>
      </div>
      <div class="minfo">
        <div class="sub">${esc(s.title)} · ${esc(s.theme)}</div>
        <h3>${esc(b.title)}</h3>
        <div class="by" style="color:var(--muted)">by ${esc(s.author)}</div>
        ${b.tagline?`<div class="tag">${esc(b.tagline)}</div>`:''}
        <div class="desc">${esc(b.description)}</div>
        <div class="price">${fmt(b.price)}</div>
        <button class="btn" onclick="addToCart('${sid}',${n});closeModal()">Add to Cart</button>
      </div>
    </div>`;
  document.getElementById('modalBg').classList.add('show');
}
function closeModal(){document.getElementById('modalBg').classList.remove('show');}

/* ---------- fullscreen cover lightbox ---------- */
function openLightbox(src){
  const lb=document.getElementById('lightbox'), im=document.getElementById('lightboxImg');
  im.onerror=closeLightbox;           // no real cover image -> just skip
  im.src=src; lb.classList.add('show');
}
function closeLightbox(){document.getElementById('lightbox').classList.remove('show');}

/* ---------- cart ---------- */
let cart = load();
function load(){try{return JSON.parse(localStorage.getItem('rh_cart')||'[]')}catch(e){return[]}}
function save(){localStorage.setItem('rh_cart',JSON.stringify(cart));renderCart();}
function key(sid,n){return sid+'-'+n;}
function addToCart(sid,n){
  const k=key(sid,n); const ex=cart.find(i=>i.k===k);
  if(ex) ex.q++; else cart.push({k,sid,n,q:1});
  save(); toast('Added to cart 💕');
}
function removeItem(k){cart=cart.filter(i=>i.k!==k);save();}
function clearCart(){cart=[];save();}
function cartTotal(){return cart.reduce((a,i)=>{const b=byId[i.sid].books[i.n-1];return a+b.price*i.q;},0);}
function renderCart(){
  document.getElementById('cartCount').textContent = cart.reduce((a,i)=>a+i.q,0);
  document.getElementById('cartTotal').textContent = fmt(cartTotal());
  const el=document.getElementById('cartItems');
  if(!cart.length){el.innerHTML='<div class="empty">Your cart is empty.<br>So much improbable love awaits.</div>';return;}
  el.innerHTML = cart.map(i=>{
    const s=byId[i.sid], b=s.books[i.n-1];
    return `<div class="citem">
      ${miniHTML(s,b)}
      <div class="info"><strong>${esc(b.title)}</strong><br>
        <span style="color:var(--muted)">${esc(s.title)}</span><br>
        ${fmt(b.price)} × ${i.q}</div>
      <div class="rm" onclick="removeItem('${i.k}')" title="Remove">&times;</div>
    </div>`;
  }).join('');
}
function openCart(){document.getElementById('drawer').classList.add('show');document.getElementById('drawerBg').classList.add('show');}
function closeCart(){document.getElementById('drawer').classList.remove('show');document.getElementById('drawerBg').classList.remove('show');}
function checkout(){
  if(!cart.length){toast('Add a book first! 📚');return;}
  const n=cart.reduce((a,i)=>a+i.q,0), t=fmt(cartTotal());
  cart=[];save();closeCart();
  toast(`💌 Order placed! ${n} book${n>1?'s':''} · ${t}. Your improbable passions are on the way.`);
}

/* ---------- toast + routing ---------- */
let toastT;
function toast(msg){const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');
  clearTimeout(toastT);toastT=setTimeout(()=>el.classList.remove('show'),2600);}
function go(hash){location.hash=hash;}
function render(){
  const h=location.hash||'#/';
  const m=h.match(/^#\/series\/(.+)$/);
  document.getElementById('view').innerHTML = m?seriesView(decodeURIComponent(m[1])):homeView();
  window.scrollTo(0,0);
}
window.addEventListener('hashchange',render);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeLightbox();closeModal();closeCart();}});
render();renderCart();
</script>
</body>
</html>
"""


def main():
    with open(DATA) as f:
        catalog = json.load(f)
    catalog = enrich(catalog)
    html = TEMPLATE.replace("__CATALOG_JSON__", json.dumps(catalog))
    with open(OUT, "w") as f:
        f.write(html)
    nbooks = sum(len(s["books"]) for s in catalog["series"])
    print(f"Wrote {OUT}: {len(catalog['series'])} series, {nbooks} books.")


if __name__ == "__main__":
    main()
