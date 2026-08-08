
import { initSea } from './background.js';

document.documentElement.classList.add('js');

const reduce = window.matchMedia
  && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const seaCanvas = document.getElementById('sea');
const sea = initSea(seaCanvas, reduce);

if (sea && sea.setHeroVisible) {
  const hero = document.getElementById('top');
  if (hero && 'IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((e) => sea.setHeroVisible(e.isIntersecting));
    }, { threshold: 0.02 }).observe(hero);
  }
}

let cube = null;
let exploded = false;
function setExploded(on) {
  exploded = on;
  const layout = document.querySelector('.cube__layout');
  if (layout) layout.classList.toggle('is-exploded', on);
}

const FACES = {
  hajime: { romaji: 'Hajime', state: 'light',  status: 'First analysis on the way' },
  sugao:  { romaji: 'Sugao',  state: 'active', status: 'Live' },
  tosei:  { romaji: 'Tosei',  state: 'soon',   status: 'Coming soon' },
  kamon:  { romaji: 'Kamon',  state: 'soon',   status: 'Coming soon' },
  torii:  { romaji: 'Torii',  state: 'soon',   status: 'Coming soon' },
  kizuna: { romaji: 'Kizuna', state: 'soon',   status: 'Coming soon' },
};
const FACE_KEYS = Object.keys(FACES);

const cards = Array.from(document.querySelectorAll('.face-card'));
const elStatus = document.getElementById('cube-status');
const elStatusText = document.getElementById('cube-status-text');
const elOpen = document.getElementById('cube-open');
const elFolio = document.getElementById('cube-folio');

const CLAVE_CARA = 'kf:face';

let activeFace = null;

function setFolio(open) {
  if (!elFolio) return;
  elFolio.classList.toggle('is-open', open);
  if (open) elFolio.removeAttribute('inert');
  else elFolio.setAttribute('inert', '');
}

function setActiveFace(key) {
  const face = FACES[key];
  if (!face) return;
  if (exploded) {
    setExploded(false);
    if (cube && cube.reassemble) cube.reassemble();
    setMore('button');
  }
  activeFace = key;
  cards.forEach((c) => c.classList.toggle('is-active', c.dataset.face === key));

  if (elStatus) {
    elStatus.dataset.state = face.state;
    elStatus.querySelector('.dot').dataset.state = face.state;
    elStatusText.textContent = face.status;
  }
  if (elOpen) {
    elOpen.href = '/' + key + '/';
    elOpen.textContent = 'Open ' + face.romaji + ' →';
  }
  setFolio(true);
  prefetchFace(key);
  try { sessionStorage.setItem(CLAVE_CARA, key); } catch (e) {   }
  if (cube && cube.snapTo) cube.snapTo(key);
}

function clearSelection() {
  activeFace = null;
  cards.forEach((c) => c.classList.remove('is-active'));
  setFolio(false);
  try { sessionStorage.removeItem(CLAVE_CARA); } catch (e) {   }
}

const prefetched = new Set();
function prefetchFace(key) {
  if (prefetched.has(key)) return;
  const con = navigator.connection;
  if (con && (con.saveData || /(^|-)2g$/.test(con.effectiveType || ''))) return;
  prefetched.add(key);
  const l = document.createElement('link');
  l.rel = 'prefetch';
  l.as = 'document';
  l.href = '/' + key + '/';
  document.head.appendChild(l);
}

cards.forEach((card) => {
  card.addEventListener('click', (e) => {
    e.preventDefault();
    setActiveFace(card.dataset.face);
    if (elOpen) elOpen.focus();
  });
  card.addEventListener('focus', () => setActiveFace(card.dataset.face));
});

const toggle = document.querySelector('.cube__toggle');
const stage = document.getElementById('cube-stage');
const grid = document.querySelector('.face-grid');

const moreP = document.querySelector('.cube__more');
const moreLink = moreP ? moreP.querySelector('a') : null;
let moreBtn = null;
if (moreP && moreLink) {
  moreBtn = document.createElement('button');
  moreBtn.type = 'button';
  moreBtn.className = 'cube__more-action';
  moreBtn.hidden = true;
  moreBtn.textContent = 'Explode the Cube';
  moreP.appendChild(moreBtn);
  moreBtn.addEventListener('click', () => {
    if (!cube || !cube.explode) return;
    if (!exploded) {
      setExploded(true);
      clearSelection();
      cube.explode();
      prefetchFace('musubi');
    } else {
      setExploded(false);
      cube.reassemble();
    }
    setMore('button');
  });
}
function setMore(mode) {
  if (!moreLink || !moreBtn) return;
  moreLink.hidden = mode === 'button';
  moreBtn.hidden = mode !== 'button';
  if (mode === 'button') {
    moreBtn.textContent = exploded ? 'Reassemble the Cube' : 'Explode the Cube';
  }
}

function setView(view) {
  const is3d = view === '3d';
  if (!is3d && exploded) {
    setExploded(false);
    if (cube && cube.reassemble) cube.reassemble(true);
  }
  if (stage) stage.hidden = !is3d;
  if (grid) grid.classList.toggle('is-sr', is3d);
  if (cube && cube.setEnabled) cube.setEnabled(is3d);
  if (toggle) {
    toggle.querySelectorAll('button').forEach((b) => {
      b.setAttribute('aria-selected', String(b.dataset.view === view));
    });
  }
  const hint = document.querySelector('.cube__hint');
  if (hint) {
    hint.textContent = is3d
      ? 'Drag to turn. Click a face to select it.'
      : 'Click a face to select it.';
  }
  setMore(is3d ? 'button' : 'link');
}

if (stage) {
  if (toggle) {
    toggle.hidden = false;
    toggle.querySelectorAll('button').forEach((b) => {
      b.addEventListener('click', () => setView(b.dataset.view));
    });
  }
  setView('3d');
}

async function hydrateCube() {
  if (!stage) return;
  try {
    const mod = await import('./cube.js');
    cube = mod.initCube(stage, {
      faces: FACE_KEYS,
      reduce,
      onSelect: (key) => setActiveFace(key),
      onDragStart: () => clearSelection(),
      onCoreOpen: () => { window.location.assign('/musubi/'); },
    });
    setExploded(false);
    if (!cube) throw new Error('initCube returned null');
    setView(stage.hidden ? 'grid' : '3d');
    if (activeFace && cube.snapTo) cube.snapTo(activeFace);
  } catch (err) {
    setView('grid');
    if (toggle) toggle.hidden = true;
    console.warn('[cube] could not hydrate; falling back to the grid.', err);
  }
}

function hydrateCubeWhenNear() {
  if (!stage) return;
  const section = document.getElementById('cube');
  if (!section || !('IntersectionObserver' in window)) { hydrateCube(); return; }
  const io = new IntersectionObserver((entries) => {
    if (!entries.some((e) => e.isIntersecting)) return;
    io.disconnect();
    hydrateCube();
  }, { rootMargin: '0px 0px -1px 0px' });
  io.observe(section);
}
hydrateCubeWhenNear();

function esVueltaAtras() {
  const e = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
  return !!e && e.type === 'back_forward';
}

function restoreSelection() {
  if (!elFolio || !esVueltaAtras()) return;
  let key = null;
  try { key = sessionStorage.getItem(CLAVE_CARA); } catch (e) {   }
  if (!key || !FACES[key]) return;
  elFolio.classList.add('no-anim');
  setActiveFace(key);
  requestAnimationFrame(() => requestAnimationFrame(() => {
    elFolio.classList.remove('no-anim');
  }));
}
restoreSelection();

window.addEventListener('pageshow', (e) => {
  if (!e.persisted) return;
  if (!cube) return;
  if (cube.isContextLost && cube.isContextLost()) {
    console.warn('[cube] context lost after bfcache restore; rehydrating.');
    cube.dispose();
    cube = null;
    hydrateCube();
  } else if (cube.render) {
    cube.render();
  }
});
