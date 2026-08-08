/* =========================================================================
   Orquestador de la página.
   - Inicializa el océano de fondo.
   - Pausa el mar cuando el hero no está visible (ahorro en móvil/desktop).
   - Sincroniza la grilla de caras con el panel de detalle.
   - Hidrata el cubo 3D (Three.js) si el módulo carga; si no, queda la grilla.
   (El fondo de la nav al scrollear DEJÓ de ser de este archivo, 2026-08-08:
   es CSS puro — opaco por defecto + scroll-driven como mejora—, porque el
   mecanismo por JS solo cubría la portada y las páginas de prosa quedaban
   sin fondo. Ver el bloque NAV de styles.css.)
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
// Estado de la vista explotada. Vive acá y no en cube.js porque quien decide
// qué se puede hacer en cada modo (seleccionar, explotar, alternar vista) es
// este orquestador; el cubo sólo ejecuta.
// setExploded es la ÚNICA vía de cambio: además del flag conmuta la clase
// .is-exploded del layout, de la que cuelga el CSS que esconde la ayuda y el
// toggle en modo explotado (visual solamente — la salida de teclado queda).
let exploded = false;
function setExploded(on) {
  exploded = on;
  const layout = document.querySelector('.cube__layout');
  if (layout) layout.classList.toggle('is-exploded', on);
}

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
  /* Explotado, las caras no se seleccionan — pero la GRILLA recortada sigue
     siendo focusable por teclado (es la capa semántica y no se le quita el
     foco a propósito). Si un foco de teclado llega acá con el cubo explotado,
     el gesto vale como «volver al cubo y elegir»: se rearma y se sigue. Es la
     salida coherente entre bloquear el teclado (peor) e ignorar el estado. */
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
   documento ya esté en caché cuando se decide entrar.

   ESTO NO SE FUE CON EL MAELSTROM, y no es un resto olvidado. Nació para que
   la animación de entrada no arrancara contra una petición de red, pero sin
   transición sirve igual o se nota más: ahora la navegación es un corte seco,
   y un corte contra una página que todavía está bajando es el blanco entre
   una y otra. Cuando vuelva la transición, vuelve además el motivo original.

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

/* ---- Control de la vista explotada ---------------------------------------
   El enlace «The idea underneath the cube →» de .cube__more se REEMPLAZA en modo
   3D por el botón Explode/Reassemble — decisión del autor: explotar el cubo
   es una invitación más fuerte que un enlace a leer, y /musubi/ sigue
   accesible por la nav y por el núcleo. El <a> QUEDA en el HTML como capa
   sin JS (y como destino en modo grilla, donde no hay cubo que explotar);
   acá sólo se alterna cuál de los dos se ve. Si la hidratación falla, el
   catch pasa a grilla y el enlace vuelve solo. */
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
    // Sin cubo todavía (el import resuelve), el botón no hace nada: mismo
    // criterio que el toggle, cuyos listeners también viven sin cubo.
    if (!cube || !cube.explode) return;
    if (!exploded) {
      setExploded(true);
      // La selección se limpia y el folio se cierra: un folio abierto de una
      // selección que ya no se puede cambiar es incoherente.
      clearSelection();
      cube.explode();
      // El núcleo lleva a /musubi/: precargarla ahora, igual que las caras.
      prefetchFace('musubi');
    } else {
      setExploded(false);
      cube.reassemble();
    }
    setMore('button');
  });
}
/* 'button' muestra el control de explotar (con el rótulo según el estado);
   'link' devuelve el enlace a /musubi/ (grilla y fallback sin cubo). */
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
  /* La grilla no tiene equivalente explotado: pasar a grilla REARMA el cubo
     al instante (sin animación — el escenario se oculta en el mismo gesto) y
     volver a 3D lo encuentra armado, igual que al cargar. El toggle queda
     usable en modo explotado a propósito: es la salida de accesibilidad, y
     esconder un control por el estado del canvas sería quitársela. */
  if (!is3d && exploded) {
    setExploded(false);
    if (cube && cube.reassemble) cube.reassemble(true);
  }
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
  // La ayuda dice lo del modo activo: en la grilla no hay nada que arrastrar,
  // así que «Drag to turn» ahí es una instrucción para un control que no
  // existe. El HTML trae el texto de GRILLA: sin JS la capa visible es la
  // grilla, y este código no corre para corregirlo. El de 3D lo pone el
  // arranque, que ya pasa por acá con setView('3d').
  const hint = document.querySelector('.cube__hint');
  if (hint) {
    hint.textContent = is3d
      ? 'Drag to turn. Click a face to select it.'
      : 'Click a face to select it.';
  }
  // El control de abajo acompaña al modo: botón de explotar en 3D, enlace a
  // /musubi/ en grilla (y en el fallback sin cubo, que pasa por acá).
  setMore(is3d ? 'button' : 'link');
}

/* ---- Reservar el layout 3D ANTES de hidratar ----------------------------
   Sin esto, las anclas aterrizaban ~400px corridas. La cadena, medida: al
   navegar de una subpágina a /#about, el scroll suave ATRAVIESA la sección del
   cubo; eso dispara el lazy-init, y cuando el import de Three.js resuelve, el
   escenario (620px) reemplaza a la grilla (~215px) insertando ~406px de alto
   ARRIBA del destino — con el scroll ya aterrizado. scroll-margin-top no puede
   arreglar eso: el destino se movió después del aterrizaje.

   La reserva pone el layout 3D (escenario vacío con su alto de CSS, grilla
   recortada, ayuda de 3D) en cuanto corre el módulo, así que la altura de la
   página queda estable desde el primer layout y el ancla aterriza donde va a
   quedarse. Lo que se difiere sigue siendo lo caro —crear el contexto WebGL—,
   no la geometría de la página.

   Si la hidratación falla, el catch de hydrateCube revierte a la grilla: el
   fallback sin cubo sigue siendo el mismo de siempre. Sin JS este código no
   corre y la capa visible es la grilla, como antes.

   EL TOGGLE ENTRA EN LA RESERVA, y no es un detalle: mostrarlo recién al
   hidratar metía ~59px (su alto + margen) DESPUÉS del aterrizaje del ancla —
   la misma clase de corrimiento que la reserva existe para evitar, en chico.
   Sus listeners funcionan sin cubo (setView guarda cada uso de `cube`), y la
   elección hecha ANTES de que el import resuelva se respeta: la hidratación
   re-aplica el modo vigente en vez de forzar 3D (ver hydrateCube).
   Condicionado a `stage`: sin escenario en el DOM no hay layout 3D que
   reservar, y recortar la grilla sola dejaría la sección vacía. */
if (stage) {
  if (toggle) {
    toggle.hidden = false;
    toggle.querySelectorAll('button').forEach((b) => {
      b.addEventListener('click', () => setView(b.dataset.view));
    });
  }
  setView('3d');
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
      // Único elemento clicable en modo explotado: el núcleo lleva a Musubi.
      onCoreOpen: () => { window.location.assign('/musubi/'); },
    });
    // Un cubo recién creado arranca ARMADO. Importa en la rehidratación tras
    // perder el contexto (bfcache): si la página volvió con exploded=true, el
    // flag describiría un estado que el cubo nuevo no tiene.
    setExploded(false);
    // initCube hoy no devuelve null (o devuelve el cubo o lanza), pero si
    // alguna versión futura lo hiciera, con la reserva puesta un return
    // silencioso dejaría el escenario visible y VACÍO para siempre — sin
    // pasar por el catch y sin reintento (el observer ya se desconectó).
    // Null se trata como fallo: mismo camino que el catch.
    if (!cube) throw new Error('initCube returned null');
    // Se RE-APLICA el modo VIGENTE, no '3d' incondicional: el toggle está
    // vivo desde la reserva, así que el usuario pudo elegir la grilla
    // mientras el import resolvía — y un setView('3d') fijo acá le pisaba
    // la elección devolviéndolo a 3D solo. stage.hidden es el modo: la
    // reserva lo puso en false y sólo el toggle lo cambia. En 3D esto
    // enciende el loop del cubo recién creado (setEnabled); en grilla lo
    // deja creado y apagado, listo para cuando vuelva.
    setView(stage.hidden ? 'grid' : '3d');
    // No forzamos snap al cargar: se conserva la vista 3/4 inicial del cubo.
    // La excepción es volver atrás: si hay una cara restaurada, el cubo tiene
    // que aparecer mirándola, no en la pose de bienvenida.
    if (activeFace && cube.snapTo) cube.snapTo(activeFace);
  } catch (err) {
    // Sin cubo: la grilla semántica queda como navegación. No es un fallo fatal.
    // Deshace la reserva de layout 3D hecha en la carga: escenario oculto,
    // grilla visible, ayuda de grilla, y el toggle se esconde — sin cubo no
    // hay dos vistas entre las que alternar.
    setView('grid');
    if (toggle) toggle.hidden = true;
    // EL MENSAJE VA EN INGLÉS aunque el comentario esté en castellano, y la
    // distinción es la que vale para todo el archivo: un comentario no se
    // ejecuta, un console.warn SÍ — es salida que el programa produce en
    // runtime, dirigida a quien esté mirando la consola. Es interfaz, aunque
    // sea técnica, y esta interfaz está en inglés como el resto del sitio.
    console.warn('[cube] could not hydrate; falling back to the grid.', err);
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
    // rootMargin NEGATIVO abajo (-1px), y el signo es la parte que importa: el
    // hero mide EXACTAMENTE 100vh, así que la sección del cubo TOCA el fold ya
    // en la carga — y dos rects que se tocan INTERSECAN para el observer,
    // aunque compartan sólo el borde. Con margen 0 el contexto WebGL se creaba
    // en la carga y el lazy-init no difería nada (medido: el canvas existía
    // antes de scrollear). El -1px encoge el viewport observado justo lo
    // suficiente para que «tocar el borde» no cuente, y el contexto se crea
    // recién al scrollear, fuera del pico de carga inicial (shader del mar +
    // fuentes). Un rootMargin POSITIVO «generoso» desactiva la optimización
    // entera: la sección intersectaría en la carga.
  }, { rootMargin: '0px 0px -1px 0px' });
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
    console.warn('[cube] context lost after bfcache restore; rehydrating.');
    cube.dispose();
    cube = null;
    hydrateCube();
  } else if (cube.render) {
    cube.render();                        // un cuadro por si el buffer se vació
  }
});
