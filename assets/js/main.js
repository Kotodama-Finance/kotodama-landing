/* =========================================================================
   Orquestador de la página.
   - Inicializa el océano de fondo.
   - Nav: fondo al scrollear.
   - Pausa el mar cuando el hero no está visible (ahorro en móvil/desktop).
   - Sincroniza la grilla de caras con el panel de detalle.
   - Hidrata el cubo 3D (Three.js) si el módulo carga; si no, queda la grilla.
   ========================================================================= */

import { initSea } from './background.js';

// Marca de JS activo: habilita el panel de detalle de una sola cara.
// Sin JS (crawlers incluidos) se ven las seis caras y todo el contenido.
document.documentElement.classList.add('js');

const reduce = window.matchMedia
  && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---- Fondo océano ------------------------------------------------------- */
const seaCanvas = document.getElementById('sea');
const sea = initSea(seaCanvas, reduce);

/* ---- Nav: fondo al scrollear -------------------------------------------- */
const nav = document.getElementById('nav');
function onScroll() {
  nav.classList.toggle('is-scrolled', window.scrollY > 60);
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ---- Pausar el mar cuando el hero sale de vista -------------------------- */
if (sea && sea.setHeroVisible) {
  const hero = document.getElementById('top');
  if (hero && 'IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((e) => sea.setHeroVisible(e.isIntersecting));
    }, { threshold: 0.02 }).observe(hero);
  }
}

/* ---- Caras: sincronía grilla ⇄ detalle ---------------------------------- */
// Declarado antes de setActiveFace: esta lo referencia y se llama en la carga.
let cube = null;
const FACE_KEYS = ['hajime', 'sugao', 'tosei', 'kamon', 'torii', 'kizuna'];
const cards = Array.from(document.querySelectorAll('.face-card'));
const details = new Map(
  FACE_KEYS.map((k) => [k, document.getElementById('face-' + k)])
);

let activeFace = 'hajime';

/** Marca una cara como activa (resalta la card y muestra su detalle). */
function setActiveFace(key) {
  if (!FACE_KEYS.includes(key)) return;
  activeFace = key;
  cards.forEach((c) => c.classList.toggle('is-active', c.dataset.face === key));
  details.forEach((el, k) => { if (el) el.classList.toggle('is-shown', k === key); });
  // aviso al cubo 3D si está montado
  if (cube && cube.snapTo) cube.snapTo(key);
}

cards.forEach((card) => {
  // el click resalta y muestra el detalle; el href ancla al bloque (baseline)
  card.addEventListener('click', () => setActiveFace(card.dataset.face));
  // Teclado: al tabular hasta una cara, el cubo hace snap a esa cara, así lo
  // que se ve y lo que tiene el foco coinciden.
  card.addEventListener('focus', () => setActiveFace(card.dataset.face));
});
setActiveFace('hajime');

/* ---- Toggle 3D / grilla (aparece solo si el cubo hidrata) --------------- */
const toggle = document.querySelector('.cube__toggle');
const stage = document.getElementById('cube-stage');
const grid = document.querySelector('.face-grid');

function setView(view) {
  const is3d = view === '3d';
  // Vistas excluyentes: en modo cubo se ve el cubo, en modo grilla la grilla.
  if (stage) stage.hidden = !is3d;
  // En 3D la grilla no se elimina del DOM ni va a display:none: se oculta
  // visualmente (clip) pero sigue siendo focusable por teclado y legible por
  // crawlers. Es la capa semántica; el canvas va aria-hidden.
  if (grid) grid.classList.toggle('is-sr', is3d);
  // En modo grilla el cubo se oculta: pausamos su loop para no gastar GPU.
  if (cube && cube.setEnabled) cube.setEnabled(is3d);
  if (toggle) {
    toggle.querySelectorAll('button').forEach((b) => {
      b.setAttribute('aria-selected', String(b.dataset.view === view));
    });
  }
}

/* ---- Hidratar el cubo 3D (Three.js) ------------------------------------- */
async function hydrateCube() {
  if (!stage) return;
  try {
    const mod = await import('./cube.js');
    cube = mod.initCube(stage, {
      faces: FACE_KEYS,
      reduce,
      onSelect: (key) => setActiveFace(key),
    });
    if (!cube) return;
    // el cubo cargó: mostramos el escenario y el toggle
    stage.hidden = false;
    if (toggle) {
      toggle.hidden = false;
      toggle.querySelectorAll('button').forEach((b) => {
        b.addEventListener('click', () => setView(b.dataset.view));
      });
    }
    setView('3d');
    // No forzamos snap al cargar: se conserva la vista 3/4 inicial del cubo.
  } catch (err) {
    // Sin cubo: la grilla semántica queda como navegación. No es un fallo fatal.
    console.warn('[cube] no se pudo hidratar; se mantiene la grilla.', err);
  }
}
hydrateCube();
