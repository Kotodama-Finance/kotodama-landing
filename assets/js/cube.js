/* =========================================================================
   Cubo de navegación en Three.js.

   Por qué Three.js y no CSS 3D: el cubo CSS sufría z-fighting y bleed-through
   (se veían kanji de caras traseras, el núcleo asomaba por las juntas) porque
   CSS 3D no tiene z-buffer. Acá la oclusión la resuelve el depth buffer del GPU
   sobre geometría real: 26 cubies sólidos y opacos que llenan el volumen 3x3x3.

   Paleta: navy + oro, nada más; no entra un tercer color por ninguna vía.
   Cómo se reparte ese oro entre las luces se decide —y se explica— en el bloque
   de luces, que es donde vive el código que lo aplica.

   Kanji: NO va en el cubie central. Se extiende sobre los 9 cubies de la cara
   (una textura por cara; cada quad mapea su sub-rect por UV, recortado por la
   junta, así el trazo alinea entre cubies y se corta solo en las juntas).
   Efecto grabado por normalMap (sin desplazar geometría). Dos variantes:
     - 'inlay'    (default): surco relleno en oro, estilo 象嵌.
     - 'engraved'          : grabado puro, solo profundidad, sin oro.
   Se alterna con ?kanji=engraved en la URL.

   Física portada del objeto CUBE de la referencia. Los signos de rotación en X
   se invierten respecto de CSS porque CSS usa Y-abajo y Three.js Y-arriba.

   VISTA EXPLOTADA (rama cube-exploded): los 26 cubies se separan hacia un
   radio común formando un caparazón esférico —plasma globe, esta versión sin
   las corrientes— con el núcleo de vidrio dorado en el centro (産霊 · 河川 ·
   言霊 orbitándolo). Reversible en el mismo contexto. Ver los bloques
   marcados «Vista explotada» y «Núcleo».
   ========================================================================= */

import * as THREE from 'three';
import { RoundedBoxGeometry } from '../vendor/RoundedBoxGeometry.js';

const FACE_DEFS = {
  hajime: { kanji: '肇',   romaji: 'Hajime', normal: [0, 0, 1],  target: { rx: 0,   ry: 0 } },
  sugao:  { kanji: '素顔', romaji: 'Sugao',  normal: [1, 0, 0],  target: { rx: 0,   ry: -90 } },
  tosei:  { kanji: '渡世', romaji: 'Tosei',  normal: [0, 0, -1], target: { rx: 0,   ry: 180 } },
  kamon:  { kanji: '家紋', romaji: 'Kamon',  normal: [-1, 0, 0], target: { rx: 0,   ry: 90 } },
  torii:  { kanji: '鳥居', romaji: 'Torii',  normal: [0, 1, 0],  target: { rx: 90,  ry: 0 } },
  kizuna: { kanji: '絆',   romaji: 'Kizuna', normal: [0, -1, 0], target: { rx: -90, ry: 0 } },
};

const DEG = Math.PI / 180;

/* --- Geometría de las juntas -------------------------------------------------
   Junta fina de Rubik real. El gap y el radio del bisel se suman en el vacío
   que se abre donde concurren cuatro esquinas redondeadas, así que los dos van
   chicos: la cara se lee como unidad y la junta sigue visible. */
const CELL = 1;
const GAP = 0.022;                 // separación entre cubies
const CUBIE = CELL - GAP;          // 0.978
const RADIUS = 0.03;               // bisel: chico, para no abrir rombos
const PLATE = CUBIE - 2 * RADIUS;  // zona plana de la cara del cubie

/* Esquema de iluminación. Los COLORES salen de los tokens; acá solo van
   intensidades y posiciones, que son forma, no paleta.
   Medido: dentro de la familia navy el color base del cubie no separa del
   fondo (todas las variantes caen en ~4 unidades sRGB). Lo que separa es la
   luz: el rango entre cara iluminada y cara en sombra, y el contraluz, que
   dibuja el borde de la silueta.
   Se puede sobrescribir por cara vía initCube(stage, { lighting: {...} }). */
export const LIGHT_DEFAULTS = {
  // Luz difusa y pareja, como la de las fotos del cubo físico en _ref/.
  // Lo que importa no es la relación key/hemi sino la del ambiente contra el
  // TOTAL direccional (key+rim+back): con tres direccionales, bajar sólo la key
  // deja el reparto casi igual. Acá el ambiente domina y el resultado es un
  // degradé suave, sin el highlight duro que leía metálico.
  // Subidas al aclarar el fondo de sección (#020509 -> #05111d): la separación
  // del cubo contra su fondo se sostiene con LUZ, no oscureciendo la página.
  // El reparto entre ellas no cambia, así que el carácter difuso se conserva.
  hemi: 3.5,                        // ambiente: la fuente principal
  key: 2.9,   keyPos: [-3, 5, 4],   // clave suave, arriba-izquierda (como las fotos)
  rim: 0.65,  rimPos: [4.5, 0.5, 2.5],   // relleno frontal derecho, tinte oro
  back: 1.3,  backPos: [2.5, 1.5, -4],   // relleno trasero (no es un rim: ver abajo)
};

/* Material del cubie. roughness alto = degradé suave en el bisel; roughness
   bajo concentra el reflejo en un punto y lee metálico/pulido. metalness sin
   environment map además oscurece, así que se mantiene bajo.
   Sobrescribible con initCube(stage, { material: {...} }). */
export const MATERIAL_DEFAULTS = {
  roughness: 0.72,      // plástico mate: degradé suave en el bisel, sin punto de brillo
  metalness: 0.02,
};

/* Velocidad de autorrotación (grados por tick de ~30fps) */
const AUTO_RY = 0.28;

/* rx no gira libre: oscila como un péndulo alrededor de la vista 3/4.
   Con rx corriendo libre el cubo daba vueltas completas y el romaji aparecía
   invertido o de costado. Un kanji dado vuelta se lee como forma; texto latino
   dado vuelta se lee como error. Acotarlo mantiene el texto siempre cerca de la
   vertical sin perder el movimiento en dos ejes, que es lo que da vida.
   Consecuencia asumida: 鳥居 y 絆 (arriba y abajo) no se muestran solas en
   reposo; se llega por arrastre o por la grilla.
   La amplitud sale de integrar la velocidad: rx = centro + (PICO/RITMO)*sin(fase),
   así que RITMO = PICO/AMPLITUD da justo la amplitud buscada. */
const PEND_CENTER = 18;    // grados: la vista 3/4 inicial
const PEND_AMP = 20;       // grados de excursión a cada lado
const PEND_PEAK = 0.09;    // velocidad máxima, la misma que tenía la deriva libre
const PEND_RATE = PEND_PEAK / PEND_AMP;   // radianes de fase por tick
/* Cuánto tira rx hacia la posición ideal del péndulo. Cerca del ideal es casi
   nulo (queda un péndulo puro); lejos —el usuario arrastró a rx=180— satura en
   el techo y trae el cubo de vuelta en ~8 s. */
const TRACK_GAIN = 0.004;    // por grado de desvío
const RETURN_MAX = 0.6;      // techo de velocidad, grados por tick (~18°/s)
/* Lerp de VELOCIDAD: converge en ~1s a 30fps -> sin saltos de velocidad. */
const VEL_LERP = 0.095;

function nearest(cur, target) {
  return target + 360 * Math.round((cur - target) / 360);
}

function newCanvas(size) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  return c;
}

/* Reparto de la cara -------------------------------------------------------
   Las juntas caen a 1/3 y 2/3 de la cara y ocultan una franja de ~21px de la
   textura (de 768). Un kanji grande la absorbe: el corte se lee como parte del
   objeto. El romaji NO: es texto latino chico, de trazo fino, y una junta le
   borraría un asta entera o un travesaño y lo volvería ilegible.
   Por eso el romaji va CONFINADO al cubie inferior central — su ancho es menor
   a un tercio de la cara, así que ninguna junta lo cruza — y el kanji se achica
   y sube para dejarle lugar. */
const FACE_LAYOUT = {
  kanjiSize: 0.72,       // alto máximo del kanji, en fracción de la cara
  kanjiWidth: 0.86,      // ancho máximo
  kanjiCenterY: 0.40,
  romajiCenterY: 0.835,  // centro de la fila inferior de cubies
  romajiWidth: 0.29,     // < 1/3: entra en el cubie central sin tocar juntas
  romajiSize: 0.11,
};

const FONT_KANJI = (px) => `500 ${px}px 'Zen Kaku Gothic New', sans-serif`;
/* Inter y no Cormorant, aunque el romaji vaya en Cormorant en el resto del
   sitio. Medido a tamaño real (cubo de 720px): en Cormorant itálica el romaji
   de las caras escorzadas se deshacía. Es una serif de display, de astas finas
   y modulación fuerte; grabada y a ~12px de altura de mayúscula, el halo del
   relieve se come el trazo. Inter tiene asta uniforme y x-height alta, que es
   exactamente lo que aguanta ese tamaño. */
const FONT_ROMAJI = (px) => `500 ${px}px 'Inter', sans-serif`;

/* Achica el cuerpo hasta que el texto entre en maxW. */
function fitFont(ctx, text, font, startPx, maxW) {
  let px = startPx;
  ctx.font = font(px);
  const w = ctx.measureText(text).width;
  if (w > maxW) px *= maxW / w;
  return px;
}

/* Pinta el contenido de una cara. La usan TANTO el mapa de color (navy + oro)
   COMO la máscara del grabado (negro + blanco): así el relieve calza exacto con
   el trazo, sin poder desincronizarse.
   OJO: en la máscara, negro y blanco no son colores de paleta y nunca se ven.
   Codifican un campo de alturas (0 = plano, 1 = trazo) del que se derivan las
   normales del grabado. Por eso no salen de un token. */
function paintFace(ctx, S, kanji, romaji, bg, fg) {
  const L = FACE_LAYOUT;
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, S, S);
  ctx.fillStyle = fg;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  const kpx = fitFont(ctx, kanji, FONT_KANJI, S * L.kanjiSize, S * L.kanjiWidth);
  ctx.font = FONT_KANJI(kpx);
  ctx.fillText(kanji, S / 2, S * L.kanjiCenterY + kpx * 0.04);

  const rpx = fitFont(ctx, romaji, FONT_ROMAJI, S * L.romajiSize, S * L.romajiWidth);
  ctx.font = FONT_ROMAJI(rpx);
  ctx.fillText(romaji, S / 2, S * L.romajiCenterY);
}

/* Normal map de un surco: se difumina la máscara y se derivan normales.
   El trazo baja (grabado), de ahí el signo negativo en el gradiente. */
function buildNormalMap(size, kanji, romaji, strength) {
  const mask = newCanvas(size);
  paintFace(mask.getContext('2d'), size, kanji, romaji, '#000', '#fff');
  const blurCv = newCanvas(size);
  const bctx = blurCv.getContext('2d');
  bctx.filter = `blur(${Math.round(size * 0.012)}px)`;
  bctx.drawImage(mask, 0, 0);
  bctx.filter = 'none';

  const src = bctx.getImageData(0, 0, size, size).data;
  // altura en un Float32Array plano: más rápido que leer el ImageData por pixel
  const h = new Float32Array(size * size);
  for (let i = 0, n = size * size; i < n; i++) h[i] = src[i * 4] / 255;

  const out = bctx.createImageData(size, size);
  const o = out.data;
  const at = (x, y) => h[Math.min(size - 1, Math.max(0, y)) * size + Math.min(size - 1, Math.max(0, x))];
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      // grabado: la altura DISMINUYE donde hay trazo -> -h
      const dx = -(at(x + 1, y) - at(x - 1, y));
      const dy = -(at(x, y + 1) - at(x, y - 1));
      let nx = -dx * strength;
      let ny = dy * strength;   // canvas Y va hacia abajo; Three espera verde arriba
      const nz = 1;
      const len = Math.hypot(nx, ny, nz);
      nx /= len; ny /= len;
      const i = (y * size + x) * 4;
      o[i] = (nx * 0.5 + 0.5) * 255;
      o[i + 1] = (ny * 0.5 + 0.5) * 255;
      o[i + 2] = (nz / len * 0.5 + 0.5) * 255;
      o[i + 3] = 255;
    }
  }
  const cv = newCanvas(size);
  cv.getContext('2d').putImageData(out, 0, 0);
  return { normalCanvas: cv, maskCanvas: mask };
}

/* Mapas de una cara: color (navy, con el trazo en oro si es incrustado) y
   normal (el surco del grabado). */
function makeFaceMaps(kanji, romaji, { navy, gold, inlay }) {
  const CS = 768;    // color: alto, el trazo tiene que quedar nítido
  const NS = 384;    // normal: alcanza y es mucho más barato de calcular

  const color = newCanvas(CS);
  // Sin incrustación: el trazo no lleva oro, sólo queda el relieve del grabado.
  paintFace(color.getContext('2d'), CS, kanji, romaji, navy, inlay ? gold : navy);

  const { normalCanvas } = buildNormalMap(NS, kanji, romaji, 2.6);

  const colorTex = new THREE.CanvasTexture(color);
  colorTex.colorSpace = THREE.SRGBColorSpace;
  colorTex.anisotropy = 8;

  const normalTex = new THREE.CanvasTexture(normalCanvas);
  normalTex.anisotropy = 4;

  return { colorTex, normalTex };
}

/* Quad de una cara: uno por cubie, mapeando su sub-rect de la textura de la
   cara. El recorte por la junta hace que el trazo alinee entre cubies y se
   interrumpa solo en la junta.
   DESDE LA VISTA EXPLOTADA cada quad es HIJO de su cubie, no de un grupo
   aparte por cara: la explosión mueve los 26 cubies, y las caras tienen que
   viajar CON ellos o quedarían flotando donde estaba el cubo. La posición
   local dentro del cubie es n·(CUBIE/2 + 0.006) — la misma transformación de
   mundo que tenía el grupo (d − CELL = CUBIE/2 + 0.006), así que el render
   armado es idéntico al de antes del cambio. */
function buildFaceQuad(material, r, c) {
  const du = PLATE / (3 * CELL);   // fracción de textura que cubre un quad
  const geo = new THREE.PlaneGeometry(PLATE, PLATE);
  const uc = (c + 0.5) / 3;
  const vc = 1 - (r + 0.5) / 3;
  const u0 = uc - du / 2;
  const v0 = vc - du / 2;
  const uv = geo.attributes.uv;
  for (let i = 0; i < uv.count; i++) {
    uv.setXY(i, u0 + uv.getX(i) * du, v0 + uv.getY(i) * du);
  }
  uv.needsUpdate = true;
  return new THREE.Mesh(geo, material);
}

/**
 * Monta el cubo dentro del elemento `stage`.
 * @param {HTMLElement} stage
 * @param {{reduce:boolean, onSelect:(key:string)=>void}} opts
 */
export function initCube(stage, opts) {
  const {
    reduce = false,
    onSelect = () => {},
    onDragStart = () => {},
    onCoreOpen = () => {},
  } = opts || {};

  const coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;

  // Variante del kanji: incrustado en oro (default) o grabado puro.
  const params = new URLSearchParams(location.search);
  const inlay = params.get('kanji') !== 'engraved';

  /* ---- Vista explotada: estado -------------------------------------------
     Los 26 cubies viajan hacia afuera con un modelo INTERPOLADO entre dos
     extremos que ya se probaron y fallan cada uno a su manera:
     · RADIAL RECTO: cada cubie aleja su posición original en proporción —
       las esquinas (√3) siguen más lejos que los centros de cara (1) y el
       resultado es un cubo grande y hueco, no un globo;
     · RADIO COMÚN: todos sobre la misma esfera — pero los centros de cara,
       que parten más cerca del centro, viajan DE MÁS, y con la expansión
       grande (5.0) sobresalen y rompen la lectura de globo (lo vio el autor
       en vivo; a 2.6-4.2 el efecto no saltaba).
     EXPLODE_MIX (abajo) mezcla los dos. Cada cubie CONSERVA su orientación
     (nada rota sobre sí mismo), que es lo que mantiene las caras legibles.
     `?explodeR=` permite comparar radios sin tocar el código (calibración
     visual del autor); 5.0 es el que ELIGIÓ mirando la grilla de combos:
     a 5.0 las caras se agrupan menos que a 4.2, y prefiere errar del lado
     del globo, no del cubo. */
  const EXPLODE_R = (() => {
    const v = parseFloat(params.get('explodeR'));
    return Number.isFinite(v) && v > 1.4 ? v : 5.0;
  })();
  /* Mezcla radial↔común (`?explodeMix=`, 0 a 1), normalizada por la ESQUINA:
     a cualquier mix las esquinas terminan en EXPLODE_R, y el factor sólo
     decide cuánto se meten hacia adentro aristas y centros — la silueta del
     globo no cambia al calibrar. 0 = radial recto, 1 = radio común. 0.65
     elegido sobre el barrido capturado: a 0.5 todavía se lee grilla cúbica,
     a 0.8 el centro de cara superior ya se despega del arco. */
  const EXPLODE_MIX = (() => {
    const v = parseFloat(params.get('explodeMix'));
    return Number.isFinite(v) && v >= 0 && v <= 1 ? v : 0.65;
  })();
  /* Radio del núcleo, también calibrable (`?coreR=`). 0.5 elegido por el
     autor en la misma pasada que el 5.0 — los dos se calibran JUNTOS porque
     se refuerzan: caparazón bien abierto y núcleo chico es el punto donde se
     lee como plasma globe, no una bola grande adentro de una cáscara. */
  const CORE_R = (() => {
    const v = parseFloat(params.get('coreR'));
    return Number.isFinite(v) && v > 0.3 ? v : 0.5;
  })();
  const EXPLODE_MS = 1100;
  const X = { t: 0, target: 0, last: 0 };
  const easeInOut = (u) => (u < 0.5 ? 4 * u * u * u : 1 - ((-2 * u + 2) ** 3) / 2);

  /* Colores: SIEMPRE desde los tokens de :root. Sin fallback hardcodeado —
     un hex de repuesto hace que un token faltante parezca funcionar (fue lo que
     ocultó el azul pizarra). Si falta, esto revienta con el nombre del token y
     el catch de hydrateCube deja la grilla como navegación. */
  const cs = getComputedStyle(document.documentElement);
  const tok = (n) => {
    const v = cs.getPropertyValue(n).trim();
    if (!v) throw new Error(`[cube] falta el token CSS ${n} en :root`);
    return v;
  };
  const bodyHex = tok('--c-cube-body');       // cuerpo del cubie
  const goldHex = tok('--c-gold');
  const goldSoftHex = tok('--c-gold-soft');
  const goldInkHex = tok('--c-gold-ink');     // tinta de los kanji del núcleo
  const navyDeepHex = tok('--c-navy');
  const keyLightHex = tok('--c-cube-key-light');

  /* ---- Escena, cámara, renderer ---- */
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(24, 1, 0.1, 100);
  camera.lookAt(0, 0, 0);

  /* Encuadre calculado, no una distancia fija — y ANISOTRÓPICO, no esférico.
     ESTO REEMPLAZA al encuadre por esfera envolvente completa.

     El cubo rota SOLO en dos ejes: rx (péndulo / arrastre / snap) y ry (giro
     libre). rotation.z es siempre 0 —order 'YXZ' y nadie lo toca—, y eso acota
     la altura alcanzable: como ry no cambia la coordenada vertical, la media
     altura máxima del cuerpo es √2·S —una ARISTA arriba, rx≈45°—, y el vértice
     arriba (√3·S) es INALCANZABLE: necesitaría roll. La versión anterior
     encuadraba la esfera completa (√3·S ≈ 2.58) y pagaba ~8% de distancia por
     una pose que no existe.

     Las dos condiciones, por función soporte del cuerpo barrido (el peor punto
     real, no una esfera que lo contiene):

       vertical:   d ≥ M · (√2·S / tan(halfV) + S)
                   El punto más alto (arista a rx≈45°) queda a radio S del eje
                   de ry, y su peor azimut lo acerca S hacia la cámara: de ahí
                   el «+ S». VA CON TANGENTE A PROPÓSITO: la regla «con seno,
                   no tangente» era de la ESFERA (la recta tangente a la
                   esfera); para un punto concreto la tangente es exacta.
                   Quien la «corrija» a seno aleja la cámara sin ganar nada.

       horizontal: d ≥ M · √3·S / sin(halfH)
                   ry gira libre, así que el radio horizontal máximo sí es el
                   de la esfera (√3·S, con la diagonal horizontal a rx≈45°), y
                   para un radio de revolución la fórmula del seno es la
                   correcta — acá no cambió nada.

     Manda la mayor de las dos, recalculado en cada resize. La garantía sigue
     siendo geométrica y cubre TODAS las rotaciones alcanzables: el péndulo, el
     snap (rx=±90) y el arrastre manual, que no está acotado. NO asume la
     amplitud del péndulo — cambiar PEND_AMP/PEND_CENTER no invalida el
     encuadre. Lo ÚNICO que lo invalida es introducir roll (rotation.z ≠ 0):
     ese día vuelve la esfera, d = M·√3·S/sin(min(halfV, halfH)).

     Verificado con barrido de poses (rx −8..180 × ry 0..345, y las dos de
     snap): ninguna pose recorta; el margen mínimo queda en el peor caso
     teórico (rx≈45°). Los números, en docs/mediciones/encuadre.md. */
  const HALF_SIDE = CELL + CUBIE / 2;
  const CUBE_RADIUS = Math.sqrt(3) * HALF_SIDE;   // sólo la horizontal lo usa
  const FIT_MARGIN = 1.06;

  /* La vista explotada tiene su propia distancia, y ahí la fórmula de la
     ESFERA es exacta —no una cota floja—: el caparazón explotado ES una
     esfera (radio común + media diagonal del cubie), invariante ante
     cualquier rotación, así que el razonamiento anisotrópico de arriba no
     aplica. La cámara interpola entre las dos distancias con la misma curva
     de la explosión. */
  let distAssembled = 10;
  let distExploded = 12;

  function applyCamera() {
    const k = easeInOut(X.t);
    camera.position.z = distAssembled + (distExploded - distAssembled) * k;
  }

  function frameCamera() {
    const halfV = (camera.fov / 2) * DEG;
    const halfH = Math.atan(Math.tan(halfV) * camera.aspect);
    const dv = FIT_MARGIN * HALF_SIDE * (Math.SQRT2 / Math.tan(halfV) + 1);
    const dh = (CUBE_RADIUS * FIT_MARGIN) / Math.sin(halfH);
    distAssembled = Math.max(dv, dh);
    const rOut = EXPLODE_R + Math.sqrt(3) * (CUBIE / 2) + 0.15;
    distExploded = (FIT_MARGIN * rOut) / Math.sin(Math.min(halfV, halfH));
    applyCamera();
    camera.updateProjectionMatrix();
  }

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: !coarse });
  renderer.setClearColor(0x000000, 0);   // alfa 0: transparente, no es un color
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, coarse ? 1.5 : 2));
  renderer.domElement.setAttribute('aria-hidden', 'true');
  stage.insertBefore(renderer.domElement, stage.firstChild);

  /* ---- Luces ----
     REPARTO DE COLOR, que es lo único que hay que recordar de acá:
       hemi y key -> NEUTRAS  (--c-cube-key-light)
       rim y back -> ORO      (--c-gold-soft)
     Las intensidades y posiciones están en LIGHT_DEFAULTS, arriba.

     Las dos principales van neutras a propósito: tintarlas de oro le come el
     canal azul al navy y lo desatura a gris. La luz blanca sube el brillo
     conservando el hue navy, que es lo que se quiere del cuerpo.

     El oro entra por dos vías, y la principal NO es una luz: es el material del
     trazo incrustado. Las dos secundarias son estos rellenos tintados, que
     aportan calidez sin lavar el cuerpo — y ojo con el nombre, ninguno de los
     dos dibuja un contorno; ver sus comentarios más abajo.

     No volver a describir esto en el encabezado del archivo. Hubo ahí una
     versión que decía «las luces van tintadas en oro», y era falsa desde el
     primer commit: hemi y key nunca fueron doradas. */
  const LI = Object.assign({}, LIGHT_DEFAULTS, opts && opts.lighting);

  const hemi = new THREE.HemisphereLight(
    new THREE.Color(keyLightHex), new THREE.Color(navyDeepHex), LI.hemi
  );
  scene.add(hemi);

  const key = new THREE.DirectionalLight(new THREE.Color(keyLightHex), LI.key);
  key.position.set(...LI.keyPos);       // arriba-izquierda, como en las fotos
  scene.add(key);

  // Relleno desde la derecha: sin él, en la vista 3/4 la cara derecha cae a
  // negro. Tinte oro = calidez de marca.
  const rim = new THREE.DirectionalLight(new THREE.Color(goldSoftHex), LI.rim);
  rim.position.set(...LI.rimPos);
  scene.add(rim);

  // Cuarta luz, desde atrás-derecha. Medido: con RADIUS en 0.03 casi no queda
  // curva donde aterrice luz rasante, así que NO produce un rim de contorno;
  // funciona como relleno de la cara que apunte en esa dirección. Por eso su
  // efecto depende mucho de la pose.
  const back = new THREE.DirectionalLight(new THREE.Color(goldSoftHex), LI.back);
  back.position.set(...LI.backPos);
  scene.add(back);

  /* ---- 26 cubies redondeados, TODOS idénticos ---- */
  const group = new THREE.Group();
  group.rotation.order = 'YXZ';         // replica el orden rotateX·rotateY de CSS
  scene.add(group);

  const geo = new RoundedBoxGeometry(CUBIE, CUBIE, CUBIE, 3, RADIUS);
  const MT = Object.assign({}, MATERIAL_DEFAULTS, opts && opts.material);
  const bodyMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(bodyHex), roughness: MT.roughness, metalness: MT.metalness,
  });

  const cubies = [];
  const cubieAt = {};   // "x,y,z" de grilla -> mesh; lo usan los quads de cara
  for (let x = -1; x <= 1; x++)
    for (let y = -1; y <= 1; y++)
      for (let z = -1; z <= 1; z++) {
        if (x === 0 && y === 0 && z === 0) continue;   // el centro es del núcleo
        const m = new THREE.Mesh(geo, bodyMat);
        m.position.set(x * CELL, y * CELL, z * CELL);
        // Datos de la explosión: posición armada, dirección radial unitaria,
        // y el factor de radio de la mezcla radial↔común (ver EXPLODE_MIX):
        // propio = |home| relativo a la esquina (1/√3 centros, √2/√3 aristas,
        // 1 esquinas); a mix 0 cada cual conserva su proporción, a mix 1
        // todos igualan a la esquina.
        m.userData.home = m.position.clone();
        m.userData.dir = m.position.clone().normalize();
        const propio = m.userData.home.length() / (Math.sqrt(3) * CELL);
        m.userData.rFactor = propio + (1 - propio) * EXPLODE_MIX;
        group.add(m);
        cubies.push(m);
        cubieAt[`${x},${y},${z}`] = m;
      }

  /* ---- Kanji abarcando la cara entera ---- */
  const faceMats = [];
  Object.values(FACE_DEFS).forEach((def) => {
    const [nx, ny, nz] = def.normal;
    const maps = makeFaceMaps(def.kanji, def.romaji, { navy: bodyHex, gold: goldHex, inlay });
    const mat = new THREE.MeshStandardMaterial({
      map: maps.colorTex,
      normalMap: maps.normalTex,
      normalScale: new THREE.Vector2(1.3, 1.3),
      // metalness alto oscurecería el oro: sin environment map un metal no
      // tiene difusa y sólo refleja el entorno (inexistente acá). Se mantiene
      // bajo para que el oro rinda su color real.
      roughness: MT.roughness,
      metalness: MT.metalness,
    });
    faceMats.push({ mat, maps, kanji: def.kanji, romaji: def.romaji });

    /* Cada quad va como hijo de SU cubie (ver buildFaceQuad): la rotación de
       la placa se aplica al quad y la posición local es la normal por
       CUBIE/2 + 0.006 — la misma transformación de mundo que tenía el grupo
       por cara. El dueño se deriva de la geometría: rotar el offset local
       (c−1, 1−r, 0) de la placa y sumarle la normal da la celda de grilla. */
    const rotE = new THREE.Euler();
    if (nz === -1) rotE.y = Math.PI;
    else if (nx === 1) rotE.y = Math.PI / 2;
    else if (nx === -1) rotE.y = -Math.PI / 2;
    else if (ny === 1) rotE.x = -Math.PI / 2;
    else if (ny === -1) rotE.x = Math.PI / 2;
    const rotQ = new THREE.Quaternion().setFromEuler(rotE);
    const v = new THREE.Vector3();
    for (let r = 0; r < 3; r++)
      for (let c = 0; c < 3; c++) {
        const quad = buildFaceQuad(mat, r, c);
        v.set(c - 1, 1 - r, 0).applyQuaternion(rotQ);
        const owner = cubieAt[
          `${Math.round(v.x + nx)},${Math.round(v.y + ny)},${Math.round(v.z + nz)}`
        ];
        quad.quaternion.copy(rotQ);
        quad.position.set(nx, ny, nz).multiplyScalar(CUBIE / 2 + 0.006);
        owner.add(quad);
      }
  });

  /* ---- Núcleo: esfera de vidrio dorada, sólo visible explotado ------------
     MeshPhysicalMaterial con transmission REAL: el vendor es r160 (leído de
     REVISION en three.module.js — el «r128» que circulaba en papeles quedó
     viejo), así que hay pase de transmisión completo con ior y thickness: a
     través del vidrio se ve el caparazón de atrás, refractado. El tinte va en
     `color`, que en un material transmisivo colorea la luz transmitida.
     Vive en la ESCENA, no en el grupo: el péndulo hace girar el caparazón
     alrededor de un núcleo quieto, que es lo que deja verlo desde ángulos
     distintos. El pulso (emissive + escala) corre sólo explotado y sin
     reduced-motion, en el tick — no hay keyframes CSS que puedan quedar
     declarados sin asignar. */
  const coreMat = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color(goldHex),
    metalness: 0.0,
    roughness: 0.12,
    transmission: 0.82,
    thickness: 1.3,
    ior: 1.5,
    clearcoat: 1.0,
    clearcoatRoughness: 0.18,
    emissive: new THREE.Color(goldHex),
    emissiveIntensity: 0.16,
  });
  /* Grupo del núcleo: la esfera de vidrio y el cascarón de palabras escalan y
     aparecen JUNTOS (applyExplode escala el grupo). Vive en la ESCENA, no en
     `group`: el péndulo gira el caparazón alrededor de un núcleo quieto. */
  const coreGroup = new THREE.Group();
  coreGroup.visible = false;
  scene.add(coreGroup);
  const core = new THREE.Mesh(new THREE.SphereGeometry(CORE_R, 48, 32), coreMat);
  coreGroup.add(core);

  /* Los tres conceptos del centro — 産霊 · 河川 · 言霊 — EN LA SUPERFICIE:
     textura equirrectangular sobre un cascarón apenas mayor que la esfera.
     ESTO REVIERTE la primera versión (sprites orbitando), a pedido del autor.
     La objeción que motivó los sprites —una textura clavada a la esfera se va
     de vista media órbita con el péndulo— se resuelve de otro modo: el
     péndulo NO gira el núcleo (está en la escena); quien gira es el CASCARÓN
     DE PALABRAS, sobre su propio eje, lento y continuo. Las palabras quedan
     pegadas a la superficie y aun así desfilan: se leen todas, por turnos.
     EN ORO LUMINOSO (--c-gold-ink): más claro y más saturado que la esfera,
     el trazo resalta brillando. TRES alternativas ya se probaron y
     descartaron — no volver a ninguna: --c-gold sobre la esfera dorada
     perdía el trazo (medido en la v1); el NAVY daba contraste pero el autor
     lo descartó (sobre el oro se ve sucio y mete el color del fondo en la
     única pieza enteramente dorada); y el BRONCE OSCURO fue interpretación
     equivocada de «dorado duro» — daba más delta que la serie luminosa,
     pero el autor quería un oro que resalte brillando, no hundiéndose. El
     techo del lado luminoso: si el trazo llega a blanco deja de ser oro
     (las series medidas viven junto al token, en :root). Glifos del subset
     vía canvas, verificados contra cmap; fonts.ready los rehornea abajo. */
  const WORD_SPIN = 0.00018;   // rad/ms: vuelta entera en ~35 s, un frente cada ~12
  const WORD_FIXED = 0.6;      // reduce: ángulo quieto con una palabra de frente
  const CORE_WORDS = ['産霊', '河川', '言霊'];
  function bakeWordsTexture() {
    const W = 2048;
    const H = 1024;
    const cv = document.createElement('canvas');
    cv.width = W; cv.height = H;
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = goldInkHex;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    // 0.19, bajado de 0.24 a pedido del autor: proporcionalmente MÁS chicos
    // que el arrastre del cambio de radio (coreR 0.72→0.5 ya los achica solo).
    ctx.font = `500 ${Math.round(H * 0.19)}px 'Zen Kaku Gothic New', sans-serif`;
    // Sobre el ecuador (donde la proyección equirrectangular no deforma), con
    // corrimientos verticales chicos para que no desfilen en fila perfecta.
    const dy = [-0.055, 0.03, -0.01];
    CORE_WORDS.forEach((word, i) => {
      ctx.fillText(word, W * ((i + 0.5) / 3), H * (0.5 + dy[i]));
    });
    const tex = new THREE.CanvasTexture(cv);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 8;
    return tex;
  }
  const wordMat = new THREE.MeshBasicMaterial({
    map: bakeWordsTexture(),
    transparent: true,
    opacity: 0,
    depthWrite: false,
  });
  const wordShell = new THREE.Mesh(
    new THREE.SphereGeometry(CORE_R * 1.012, 48, 32), wordMat
  );
  // Eje del giro apenas inclinado: un desfile perfectamente horizontal se lee
  // mecánico. La inclinación es del PADRE; el hijo gira sobre su Y local.
  const wordTilt = new THREE.Group();
  wordTilt.rotation.set(0.10, 0, 0.14);
  wordTilt.add(wordShell);
  coreGroup.add(wordTilt);

  // Si la fuente Zen no estaba lista, rehacer los mapas de cada cara — y las
  // texturas de las palabras del núcleo, que usan la misma fuente.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(() => {
      faceMats.forEach((f) => {
        const m = makeFaceMaps(f.kanji, f.romaji, { navy: bodyHex, gold: goldHex, inlay });
        f.mat.map = m.colorTex;
        f.mat.normalMap = m.normalTex;
        f.mat.needsUpdate = true;
      });
      wordMat.map = bakeWordsTexture();
      wordMat.needsUpdate = true;
    });
  }

  /* ---- Estado de rotación ---- */
  const C = {
    rx: 18, ry: -26,          // vista 3/4 inicial
    trx: 0, try: 0,
    velRx: 0, velRy: 0,
    snapping: false, dragging: false, moved: false,
    holdUntil: 0,
    pendPhase: 0,
    // parked: al SELECCIONAR una cara el cubo se detiene y se queda quieto
    // indefinidamente. Solo un drag nuevo lo revive.
    parked: false,
    /* Dirección heredada del último drag. Sólo en Y: en X manda la fase del
       péndulo, no el sentido del último tiro. Heredar un signo en rx pelearía
       contra la oscilación en vez de sumarse a ella. */
    signRy: 1,
  };

  function applyRotation() {
    group.rotation.x = C.rx * DEG;
    group.rotation.y = C.ry * DEG;
  }
  applyRotation();

  /* Aplica el estado de explosión con curva: posiciones de los 26 cubies
     (lerp entre su casa y su punto sobre la esfera de radio común), núcleo
     (aparece creciendo desde el hueco central: a t chico su escala lo deja
     dentro de la cavidad del cubie ausente), palabras y cámara. */
  const tmpV = new THREE.Vector3();
  function applyExplode(ts) {
    const k = easeInOut(X.t);
    cubies.forEach((m) => {
      tmpV.copy(m.userData.dir).multiplyScalar(EXPLODE_R * m.userData.rFactor);
      m.position.lerpVectors(m.userData.home, tmpV, k);
    });
    /* Pulso del núcleo: los valores de la v1, A PROPÓSITO — esto REVIERTE un
       boost que se probó, se MIDIÓ y se descartó. Subir la emisiva a
       0.10→0.55 con ±3% de escala hacía el pulso claramente visible (el
       vaivén pasó de 34 a 73,9 unidades sRGB, senoidal limpio), pero a ese
       costo la esfera dejaba de leerse como vidrio. El autor eligió el
       vidrio: QUE EL PULSO NO SE PERCIBA ESTÁ BIEN, y no se compensa por
       otra vía (ni escala, ni color, ni keyframes). Con reduce, quieto. */
    const pulsing = X.t === 1 && !reduce;
    const pulse = pulsing ? 1 + 0.015 * Math.sin(ts * 0.0014) : 1;
    coreGroup.scale.setScalar((0.4 + 0.6 * k) * pulse);
    coreGroup.visible = k > 0.02;
    coreMat.emissiveIntensity = pulsing
      ? 0.16 + 0.1 * (0.5 + 0.5 * Math.sin(ts * 0.0014))
      : 0.16;
    // El cascarón de palabras gira sobre su eje, independiente del péndulo.
    wordShell.rotation.y = reduce ? WORD_FIXED : ts * WORD_SPIN;
    wordMat.opacity = Math.max(0, (k - 0.55) / 0.45);
    applyCamera();
  }

  function snapTo(key) {
    const def = FACE_DEFS[key];
    if (!def) return;
    // Seleccionar una cara detiene el cubo: hace el snap y se queda ahí.
    C.parked = true;
    if (reduce) {
      C.rx = nearest(C.rx, def.target.rx);
      C.ry = nearest(C.ry, def.target.ry);
      C.trx = C.rx; C.try = C.ry;
      C.snapping = false;
      applyRotation();
      return;
    }
    C.trx = nearest(C.rx, def.target.rx);
    C.try = nearest(C.ry, def.target.ry);
    C.snapping = true;
  }

  /* ---- Raycast: click en una cara la selecciona ---- */
  const raycaster = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  function faceKeyFromNormal(n) {
    const ax = Math.abs(n.x), ay = Math.abs(n.y), az = Math.abs(n.z);
    let sel;
    if (ax >= ay && ax >= az) sel = [Math.sign(n.x), 0, 0];
    else if (ay >= ax && ay >= az) sel = [0, Math.sign(n.y), 0];
    else sel = [0, 0, Math.sign(n.z)];
    return Object.keys(FACE_DEFS).find((k) => {
      const nn = FACE_DEFS[k].normal;
      return nn[0] === sel[0] && nn[1] === sel[1] && nn[2] === sel[2];
    });
  }
  function pickFace(clientX, clientY) {
    const r = renderer.domElement.getBoundingClientRect();
    ndc.x = ((clientX - r.left) / r.width) * 2 - 1;
    ndc.y = -((clientY - r.top) / r.height) * 2 + 1;
    raycaster.setFromCamera(ndc, camera);
    const hits = raycaster.intersectObjects(cubies, false);
    if (!hits.length || !hits[0].face) return null;
    return faceKeyFromNormal(hits[0].face.normal);
  }
  /* Explotado, el ÚNICO clicable es el núcleo (lleva a /musubi/ vía
     onCoreOpen). Las caras dejan de ser seleccionables — lo decide onUp. */
  function pickCore(clientX, clientY) {
    if (!coreGroup.visible) return false;
    const r = renderer.domElement.getBoundingClientRect();
    ndc.x = ((clientX - r.left) / r.width) * 2 - 1;
    ndc.y = -((clientY - r.top) / r.height) * 2 + 1;
    raycaster.setFromCamera(ndc, camera);
    return raycaster.intersectObject(core, false).length > 0;
  }

  /* ---- Drag (Pointer Events, sin librería de controles) ---- */
  const el = renderer.domElement;
  function onDown(e) {
    C.dragging = true; C.snapping = false; C.moved = false;
    C.parked = false;                 // arrastrar revive el cubo
    C.velRx = 0; C.velRy = 0;
    onDragStart();                    // y deshace la selección: el botón se va
    stage.classList.add('is-dragging');
    try { el.setPointerCapture(e.pointerId); } catch (err) {}
  }
  function onMove(e) {
    if (!C.dragging) {
      // Explotado, el cursor avisa que el núcleo es clicable. '' devuelve el
      // cursor al que diga el CSS del escenario.
      if (X.t === 1) {
        el.style.cursor = pickCore(e.clientX, e.clientY) ? 'pointer' : '';
      }
      return;
    }
    const dx = e.movementX || 0, dy = e.movementY || 0;
    if (Math.abs(dx) + Math.abs(dy) > 3) C.moved = true;
    C.ry += dx * 0.45;
    C.rx += dy * 0.45;
    if (!reduce) { C.velRy = dx * 0.45; C.velRx = dy * 0.45; }
  }
  function onUp(e) {
    if (!C.dragging) return;
    C.dragging = false;
    stage.classList.remove('is-dragging');
    C.holdUntil = 0;
    const wasClick = !C.moved;
    setTimeout(() => { C.moved = false; }, 40);
    if (wasClick) {
      if (X.target === 1 || X.t > 0.02) {
        // Modo explotado (o en transición): las caras NO se seleccionan.
        // El único clic que hace algo es el del núcleo, ya explotado del todo.
        if (X.t === 1 && pickCore(e.clientX, e.clientY)) onCoreOpen();
      } else {
        // Click limpio: selecciona la cara; snapTo deja el cubo detenido (parked).
        const key = pickFace(e.clientX, e.clientY);
        if (key) { onSelect(key); snapTo(key); }
      }
    } else {
      // Soltó arrastrando: la autorrotación hereda el sentido del tiro.
      if (Math.abs(C.velRy) > 0.01) C.signRy = Math.sign(C.velRy);
    }
  }
  el.addEventListener('pointerdown', onDown);
  el.addEventListener('pointermove', onMove);
  el.addEventListener('pointerup', onUp);
  el.addEventListener('pointerleave', onUp);

  /* ---- Tamaño ----
     lastRx/lastRy son la caché del render bajo demanda (ver el loop). Se
     declaran acá arriba porque resize() tiene que invalidarlas. */
  let lastRx = null, lastRy = null;

  function resize() {
    const w = stage.clientWidth || 1;
    const h = Math.max(stage.clientHeight || 1, 1);
    renderer.setSize(w, h, true);
    camera.aspect = w / h;
    frameCamera();
    // setSize reasigna y limpia el drawing buffer: sin esto, si el ángulo no
    // cambia nadie redibuja y el canvas queda vacío hasta la próxima
    // interacción. Es lo que hacía que el cubo no apareciera hasta el click.
    lastRx = null;
    // Y redibujamos ya, sin esperar al próximo tick, que puede estar pausado
    // por visibilidad. (La escena ya está construida cuando corre el resize.)
    renderer.render(scene, camera);
  }
  const ro = new ResizeObserver(resize);
  ro.observe(stage);
  resize();

  /* ---- Visibilidad ---- */
  let enabled = true;      // false en modo grilla: el loop se pausa
  let visible = true;      // false cuando la sección sale del viewport
  const sectionCube = document.getElementById('cube');
  if (sectionCube && 'IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((e) => { visible = e.isIntersecting; });
    }, { threshold: 0.02 }).observe(sectionCube);
  }

  /* ---- Loop: física a ~30 fps (para que los valores de damping calcen) ----
     El movimiento libre es UNA sola velocidad angular que se interpola hacia su
     objetivo (0 durante el hold, autorrotación después). No hay rama separada
     de inercia vs autorrotación, así que no hay salto de velocidad en ningún
     frame: al soltar, el tiro decae de forma continua hasta la autorrotación. */
  const now = () => performance.now();
  let last = 0;
  function tick(ts) {
    requestAnimationFrame(tick);
    if (!enabled || !visible || document.hidden) return;
    if (ts - last < 32) return;
    last = ts;

    if (!C.dragging) {
      if (C.snapping) {
        C.rx += (C.trx - C.rx) * 0.12;
        C.ry += (C.try - C.ry) * 0.12;
        C.velRx = 0; C.velRy = 0;
        if (Math.abs(C.trx - C.rx) < 0.2 && Math.abs(C.try - C.ry) < 0.2) {
          C.rx = C.trx; C.ry = C.try; C.snapping = false;
          C.holdUntil = now() + 2600;
        }
      } else if (!reduce) {
        // parked (cara seleccionada) => objetivo 0: se detiene y espera.
        // Si no, hold => 0 y después autorrotación EN EL SENTIDO heredado.
        const idle = C.parked || now() < C.holdUntil;
        const tRy = idle ? 0 : AUTO_RY * C.signRy;

        /* Objetivo de velocidad en X. Nunca se asigna rx a mano: sólo se mueve
           su VELOCIDAD objetivo, y velRx la persigue con el mismo lerp que el
           resto. Por eso no puede haber escalón, ni siquiera volviendo desde
           una rotación extrema. */
        let tRx = 0;
        if (!idle) {
          /* La fase avanza SIEMPRE y describe un péndulo ideal. La velocidad
             objetivo es la de ese péndulo (feed) más una corrección que arrastra
             rx hacia la posición ideal. Sin ramas ni clamps.

             La versión anterior recortaba rx en el límite y reseteaba la fase a
             π, que es velocidad máxima negativa: el MEDIO de una bajada, no un
             extremo, donde la velocidad es cero. El resultado era un péndulo que
             oscilaba entre el límite y el centro — media excursión (medido: 25°
             de 40). Siguiendo la posición ideal el problema no existe, porque no
             hay ningún punto donde se reinicie el movimiento.

             La corrección también resuelve el retorno desde una rotación
             extrema: a rx=180 vale -162*ganancia, o sea el techo, y se apaga
             sola a medida que rx se acerca. */
          C.pendPhase += PEND_RATE;
          const ideal = PEND_CENTER + PEND_AMP * Math.sin(C.pendPhase);
          const feed = PEND_PEAK * Math.cos(C.pendPhase);
          const corr = (ideal - C.rx) * TRACK_GAIN;
          tRx = Math.max(-RETURN_MAX, Math.min(RETURN_MAX, feed + corr));
        }
        C.velRx += (tRx - C.velRx) * VEL_LERP;
        C.velRy += (tRy - C.velRy) * VEL_LERP;
        C.rx += C.velRx;
        C.ry += C.velRy;
      }
    }

    /* Animación de la explosión: t avanza hacia el objetivo por RELOJ, no por
       tick — en headless los ticks caen a ~7-15/s y una animación por tick
       duraría cualquier cosa. El paso se acota para que volver de una pestaña
       oculta no salte media transición de golpe. */
    let explodeMoved = false;
    if (X.t !== X.target) {
      const dt = Math.min(100, ts - (X.last || ts));
      const step = dt / EXPLODE_MS;
      X.t = X.target > X.t
        ? Math.min(X.target, X.t + step)
        : Math.max(X.target, X.t - step);
      explodeMoved = true;
    }
    X.last = ts;

    /* Render bajo demanda: quieto (parked) no redibuja, ahorra GPU y batería.
       Explotado sin reduce se redibuja siempre: el pulso del núcleo y las
       palabras en órbita son movimiento propio, sin cambio de rx/ry. Con
       reduce, explotado queda quieto de verdad y vuelve el bajo demanda. */
    const selfMotion = X.t > 0 && !reduce;
    if (explodeMoved || selfMotion || lastRx === null
        || Math.abs(C.rx - lastRx) > 0.002 || Math.abs(C.ry - lastRy) > 0.002) {
      lastRx = C.rx; lastRy = C.ry;
      applyRotation();
      applyExplode(ts);
      renderer.render(scene, camera);
    }
  }
  requestAnimationFrame(tick);

  return {
    snapTo,
    /* Vista explotada. Reversible por diseño: mismo contexto WebGL, misma
       escena — sólo cambian posiciones, escala del núcleo y cámara. explode()
       despierta el cubo (parked fuera) porque quieto se ve muerto; la
       selección la limpia main.js ANTES de llamar. Con reduce no hay
       transición: t salta al estado final, como el resto de las animaciones
       del sitio. */
    explode() {
      C.parked = false;
      C.snapping = false;
      X.target = 1;
      if (reduce) X.t = 1;
      lastRx = null;   // fuerza el próximo redibujo aunque rx/ry no cambien
    },
    reassemble(instant) {
      X.target = 0;
      if (reduce || instant) X.t = 0;
      el.style.cursor = '';
      lastRx = null;
    },
    isExploded() { return X.target === 1; },
    /* Pausa/reanuda el loop. En modo grilla el cubo se oculta y no debe seguir
       consumiendo GPU. */
    setEnabled(v) {
      enabled = !!v;
      if (enabled) { lastRx = null; resize(); }   // fuerza un redibujo al volver
    },
    /* Fuerza un cuadro. El loop se apoya en rAF, que no corre con la pestaña
       oculta; esto permite dibujar bajo demanda. */
    render() { renderer.render(scene, camera); },
    /* Retocar luz y material sin reconstruir texturas (que es lo caro).
       Pensado para comparar esquemas lado a lado. */
    setLighting(p) {
      if (p.hemi != null) hemi.intensity = p.hemi;
      if (p.key != null) key.intensity = p.key;
      if (p.rim != null) rim.intensity = p.rim;
      if (p.back != null) back.intensity = p.back;
    },
    setMaterial(p) {
      [bodyMat, ...faceMats.map((f) => f.mat)].forEach((m) => {
        if (p.roughness != null) m.roughness = p.roughness;
        if (p.metalness != null) m.metalness = p.metalness;
        m.needsUpdate = true;
      });
    },
    getRotation() { return { rx: C.rx, ry: C.ry, velRx: C.velRx, velRy: C.velRy }; },
    /* ¿el contexto sigue vivo? Al volver por el botón atrás la página puede
       venir del bfcache, y mientras estuvo congelada el navegador tiene
       permitido liberar la GPU. El canvas queda ahí, pero en negro. */
    isContextLost() { return renderer.getContext().isContextLost(); },
    setRotation(rx, ry) { C.rx = rx; C.ry = ry; C.snapping = false; applyRotation(); },
    dispose() {
      ro.disconnect();
      renderer.dispose();
      el.remove();
    },
  };
}
