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

/* ---- Caras: grilla, estado y botón de entrada ---------------------------- */
// Declarado antes de setActiveFace: esta lo referencia y se llama en la carga.
let cube = null;

/* El estado de cada cara venía del panel lateral, que se quitó. No puede
   desaparecer de la vista 3D: alguien navegando en modo cubo entraría a una
   cara sin saber que está vacía. Ahora viaja con el botón de entrada.

   POR QUÉ SUGAO LLEVA EL PUNTO LLENO Y HAJIME NO. Se lee al revés de lo que
   uno espera: Hajime es la cara del análisis, o sea el proyecto. Pero los
   estados dicen lo que HAY, no lo que importa — Hajime no tiene todavía una
   línea publicada y Sugao está entera. Es lo que el lead del cubo ya promete
   («One is live today»), y con el reparto anterior la grilla lo desmentía.
   No hay estado nuevo: los tres siguen siendo los mismos, cambia quién ocupa
   cada uno. Si alguien lo "arregla" devolviéndole el punto lleno a Hajime,
   vuelve a haber dos caras leyéndose como la más fuerte y ninguna de las dos
   es la publicada. */
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

/* Cara seleccionada, para restaurarla al volver atrás cuando el bfcache no
   aplica. Declarada acá arriba a propósito: setActiveFace la usa y se llama en
   la restauración, así que si estuviera más abajo entraría en zona muerta. */
const CLAVE_CARA = 'kf:face';

let activeFace = null;

/* Despliega o repliega el folio (estado + botón).
   La animación es puro CSS: acá sólo se conmuta la clase. `inert` viaja con
   ella para que plegado no sea sólo invisible — sin tabulación ni lectura por
   lector de pantalla. No se usa `hidden` porque display:none no se anima: el
   folio colapsaría de golpe, que es justo lo que se quería evitar. */
function setFolio(open) {
  if (!elFolio) return;
  elFolio.classList.toggle('is-open', open);
  if (open) elFolio.removeAttribute('inert');
  else elFolio.setAttribute('inert', '');
}

/** Selecciona una cara: resalta su tarjeta y despliega estado + botón. */
function setActiveFace(key) {
  const face = FACES[key];
  if (!face) return;
  activeFace = key;
  cards.forEach((c) => c.classList.toggle('is-active', c.dataset.face === key));

  if (elStatus) {
    elStatus.dataset.state = face.state;
    elStatus.querySelector('.dot').dataset.state = face.state;
    elStatusText.textContent = face.status;
  }
  if (elOpen) {
    // El botón navega SIEMPRE, incluso en las caras "coming soon": su
    // subpágina existe y ahí el placeholder lo dice de frente.
    elOpen.href = '/' + key + '/';
    elOpen.textContent = 'Open ' + face.romaji + ' →';
  }
  setFolio(true);
  prefetchFace(key);
  try { sessionStorage.setItem(CLAVE_CARA, key); } catch (e) { /* modo privado */ }
  if (cube && cube.snapTo) cube.snapTo(key);
}

/** Arrastrar revive el cubo: se deshace la selección y el folio se repliega. */
function clearSelection() {
  activeFace = null;
  cards.forEach((c) => c.classList.remove('is-active'));
  setFolio(false);
  try { sessionStorage.removeItem(CLAVE_CARA); } catch (e) { /* modo privado */ }
}

/* ---- Precarga de la cara seleccionada ------------------------------------
   Se precarga al SELECCIONAR, no al pulsar el botón: entre una cosa y la otra
   hay un gesto entero, que es exactamente el tiempo que hace falta para que el
   documento ya esté en caché cuando se decide entrar. Sin eso, la transición
   de entrada arranca contra una petición de red y se ve el parpadeo.

   rel=prefetch y no prerender a propósito: prefetch baja el documento y para;
   prerender además ejecutaría su JS. Ninguna subpágina lo necesita, y en la
   portada sería crear un contexto WebGL de más por cada cara que se toca. */
const prefetched = new Set();
function prefetchFace(key) {
  if (prefetched.has(key)) return;
  const con = navigator.connection;
  // Respetar «ahorro de datos» y las conexiones muy lentas: ahí precargar algo
  // que quizá no se visite es exactamente lo que no hay que hacer.
  if (con && (con.saveData || /(^|-)2g$/.test(con.effectiveType || ''))) return;
  prefetched.add(key);
  const l = document.createElement('link');
  l.rel = 'prefetch';
  l.as = 'document';
  l.href = '/' + key + '/';
  document.head.appendChild(l);
}

cards.forEach((card) => {
  // el click resalta y prepara el botón; el href sigue siendo la ruta real
  card.addEventListener('click', (e) => {
    // con JS, seleccionar no navega: navega el botón
    e.preventDefault();
    setActiveFace(card.dataset.face);
    if (elOpen) elOpen.focus();
  });
  // Teclado: al tabular hasta una cara, el cubo hace snap y aparece el botón.
  card.addEventListener('focus', () => setActiveFace(card.dataset.face));
});

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
      onDragStart: () => clearSelection(),
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
    // La excepción es volver atrás: si hay una cara restaurada, el cubo tiene
    // que aparecer mirándola, no en la pose de bienvenida.
    if (activeFace && cube.snapTo) cube.snapTo(activeFace);
  } catch (err) {
    // Sin cubo: la grilla semántica queda como navegación. No es un fallo fatal.
    console.warn('[cube] no se pudo hidratar; se mantiene la grilla.', err);
  }
}

/* Lazy-init: el cubo no crea su contexto WebGL hasta que su sección se acerca
   al viewport. Lo que se difiere NO es el costo de dibujar (geometría trivial)
   sino el de CREAR el segundo contexto: memoria de GPU, compilación de shaders
   y armado del pipeline. Ese costo se paga una sola vez al inicializar y no lo
   evitan ni el render bajo demanda ni la pausa por visibilidad, porque para
   pausar un contexto primero hay que crearlo.
   En todas las plataformas: en desktop no cuesta nada y es lo correcto igual. */
function hydrateCubeWhenNear() {
  if (!stage) return;
  const section = document.getElementById('cube');
  if (!section || !('IntersectionObserver' in window)) { hydrateCube(); return; }
  const io = new IntersectionObserver((entries) => {
    if (!entries.some((e) => e.isIntersecting)) return;
    io.disconnect();
    hydrateCube();
    // Sin rootMargin a propósito: el hero mide 100vh, así que la sección del
    // cubo arranca apenas ~20px debajo del fold. Cualquier margen de anticipación
    // la haría intersectar ya en la carga y no se diferiría nada. Con margen 0
    // el contexto se crea recién al scrollear, fuera del pico de carga inicial
    // (compilación del shader del mar + fuentes). El margen de maniobra lo da el
    // padding de la sección: el cubo queda bastante más abajo del borde.
  }, { rootMargin: '0px' });
  io.observe(section);
}
hydrateCubeWhenNear();

/* ---- Volver atrás -------------------------------------------------------
   Dos caminos, y hacen falta los dos:

   1. bfcache. La página vuelve viva y entera —cubo, pose, folio desplegado—
      sin ejecutar nada. Es el caso bueno y no hay que restaurar nada. Lo único
      que puede haberse roto es el contexto WebGL: mientras la página está
      congelada el navegador tiene permiso para liberar la GPU, y entonces el
      canvas vuelve en negro. Por eso se comprueba en `pageshow`.

   2. Sin bfcache (el navegador no lo tiene, o Chrome lo descartó por presión
      de memoria). La página se reconstruye desde cero y la selección se
      perdería. Ahí entra sessionStorage.

   Sólo se restaura si la navegación fue back/forward. En una carga normal no
   hay nada seleccionado, y eso es deliberado: llegar a la portada no debe
   elegir una cara en tu nombre. */
function esVueltaAtras() {
  const e = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
  return !!e && e.type === 'back_forward';
}

function restoreSelection() {
  if (!elFolio || !esVueltaAtras()) return;
  let key = null;
  try { key = sessionStorage.getItem(CLAVE_CARA); } catch (e) { /* modo privado */ }
  if (!key || !FACES[key]) return;
  // Sin animación: volver atrás devuelve la página como estaba. Reproducir el
  // despliegue haría parecer que la elección la acaba de hacer el navegador.
  elFolio.classList.add('no-anim');
  setActiveFace(key);
  // dos cuadros: uno para que el layout aplique el estado final, otro para
  // devolver la transición sin que la reanimación arranque sola.
  requestAnimationFrame(() => requestAnimationFrame(() => {
    elFolio.classList.remove('no-anim');
  }));
}
restoreSelection();

window.addEventListener('pageshow', (e) => {
  if (!e.persisted) return;               // carga normal: no vino del bfcache
  if (!cube) return;
  if (cube.isContextLost && cube.isContextLost()) {
    // El canvas volvió sin GPU. Se tira y se rehidrata: es la única salida y
    // cuesta lo mismo que la primera vez.
    console.warn('[cube] contexto perdido al volver del bfcache; rehidratando.');
    cube.dispose();
    cube = null;
    hydrateCube();
  } else if (cube.render) {
    cube.render();                        // un cuadro por si el buffer se vació
  }
});
