
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

const CELL = 1;
const GAP = 0.022;
const CUBIE = CELL - GAP;
const RADIUS = 0.03;
const PLATE = CUBIE - 2 * RADIUS;

export const LIGHT_DEFAULTS = {
  hemi: 3.5,
  key: 2.9,   keyPos: [-3, 5, 4],
  rim: 0.65,  rimPos: [4.5, 0.5, 2.5],
  back: 1.3,  backPos: [2.5, 1.5, -4],
};

export const MATERIAL_DEFAULTS = {
  roughness: 0.72,
  metalness: 0.02,
};

const AUTO_RY = 0.28;

const PEND_CENTER = 18;
const PEND_AMP = 20;
const PEND_PEAK = 0.09;
const PEND_RATE = PEND_PEAK / PEND_AMP;
const TRACK_GAIN = 0.004;
const RETURN_MAX = 0.6;
const VEL_LERP = 0.095;

function nearest(cur, target) {
  return target + 360 * Math.round((cur - target) / 360);
}

function newCanvas(size) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  return c;
}

const FACE_LAYOUT = {
  kanjiSize: 0.72,
  kanjiWidth: 0.86,
  kanjiCenterY: 0.40,
  romajiCenterY: 0.835,
  romajiWidth: 0.29,
  romajiSize: 0.11,
};

const FONT_KANJI = (px) => `500 ${px}px 'Zen Kaku Gothic New', sans-serif`;
const FONT_ROMAJI = (px) => `500 ${px}px 'Inter', sans-serif`;

function fitFont(ctx, text, font, startPx, maxW) {
  let px = startPx;
  ctx.font = font(px);
  const w = ctx.measureText(text).width;
  if (w > maxW) px *= maxW / w;
  return px;
}

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

function buildNormalMap(size, kanji, romaji, strength) {
  const mask = newCanvas(size);
  paintFace(mask.getContext('2d'), size, kanji, romaji, '#000', '#fff');
  const blurCv = newCanvas(size);
  const bctx = blurCv.getContext('2d');
  bctx.filter = `blur(${Math.round(size * 0.012)}px)`;
  bctx.drawImage(mask, 0, 0);
  bctx.filter = 'none';

  const src = bctx.getImageData(0, 0, size, size).data;
  const h = new Float32Array(size * size);
  for (let i = 0, n = size * size; i < n; i++) h[i] = src[i * 4] / 255;

  const out = bctx.createImageData(size, size);
  const o = out.data;
  const at = (x, y) => h[Math.min(size - 1, Math.max(0, y)) * size + Math.min(size - 1, Math.max(0, x))];
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const dx = -(at(x + 1, y) - at(x - 1, y));
      const dy = -(at(x, y + 1) - at(x, y - 1));
      let nx = -dx * strength;
      let ny = dy * strength;
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

function makeFaceMaps(kanji, romaji, { navy, gold, inlay }) {
  const CS = 768;
  const NS = 384;

  const color = newCanvas(CS);
  paintFace(color.getContext('2d'), CS, kanji, romaji, navy, inlay ? gold : navy);

  const { normalCanvas } = buildNormalMap(NS, kanji, romaji, 2.6);

  const colorTex = new THREE.CanvasTexture(color);
  colorTex.colorSpace = THREE.SRGBColorSpace;
  colorTex.anisotropy = 8;

  const normalTex = new THREE.CanvasTexture(normalCanvas);
  normalTex.anisotropy = 4;

  return { colorTex, normalTex };
}

function buildFaceQuad(material, r, c) {
  const du = PLATE / (3 * CELL);
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

export function initCube(stage, opts) {
  const {
    reduce = false,
    onSelect = () => {},
    onDragStart = () => {},
    onCoreOpen = () => {},
  } = opts || {};

  const coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;

  const params = new URLSearchParams(location.search);
  const inlay = params.get('kanji') !== 'engraved';

  const EXPLODE_R = (() => {
    const v = parseFloat(params.get('explodeR'));
    return Number.isFinite(v) && v > 1.4 ? v : 5.5;
  })();
  const CENTER_F = (() => {
    const v = parseFloat(params.get('centerF'));
    return Number.isFinite(v) && v > 0.4 && v <= 1 ? v : 0.85;
  })();
  const CORE_R = (() => {
    const v = parseFloat(params.get('coreR'));
    return Number.isFinite(v) && v > 0.3 ? v : 0.7;
  })();
  const EXPLODE_MS = 1100;
  const X = { t: 0, target: 0, last: 0 };
  const easeInOut = (u) => (u < 0.5 ? 4 * u * u * u : 1 - ((-2 * u + 2) ** 3) / 2);

  const cs = getComputedStyle(document.documentElement);
  const tok = (n) => {
    const v = cs.getPropertyValue(n).trim();
    if (!v) throw new Error(`[cube] falta el token CSS ${n} en :root`);
    return v;
  };
  const bodyHex = tok('--c-cube-body');
  const goldHex = tok('--c-gold');
  const goldSoftHex = tok('--c-gold-soft');
  const goldInkHex = tok('--c-gold-ink');
  const navyDeepHex = tok('--c-navy');
  const keyLightHex = tok('--c-cube-key-light');

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(24, 1, 0.1, 100);
  camera.lookAt(0, 0, 0);

  const HALF_SIDE = CELL + CUBIE / 2;
  const CUBE_RADIUS = Math.sqrt(3) * HALF_SIDE;
  const FIT_MARGIN = 1.06;

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
  renderer.setClearColor(0x000000, 0);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, coarse ? 1.5 : 2));
  renderer.domElement.setAttribute('aria-hidden', 'true');
  stage.insertBefore(renderer.domElement, stage.firstChild);

  const LI = Object.assign({}, LIGHT_DEFAULTS, opts && opts.lighting);

  const hemi = new THREE.HemisphereLight(
    new THREE.Color(keyLightHex), new THREE.Color(navyDeepHex), LI.hemi
  );
  scene.add(hemi);

  const key = new THREE.DirectionalLight(new THREE.Color(keyLightHex), LI.key);
  key.position.set(...LI.keyPos);
  scene.add(key);

  const rim = new THREE.DirectionalLight(new THREE.Color(goldSoftHex), LI.rim);
  rim.position.set(...LI.rimPos);
  scene.add(rim);

  const back = new THREE.DirectionalLight(new THREE.Color(goldSoftHex), LI.back);
  back.position.set(...LI.backPos);
  scene.add(back);

  const group = new THREE.Group();
  group.rotation.order = 'YXZ';
  scene.add(group);

  const geo = new RoundedBoxGeometry(CUBIE, CUBIE, CUBIE, 3, RADIUS);
  const MT = Object.assign({}, MATERIAL_DEFAULTS, opts && opts.material);
  const bodyMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(bodyHex), roughness: MT.roughness, metalness: MT.metalness,
  });

  const cubies = [];
  const cubieAt = {};
  for (let x = -1; x <= 1; x++)
    for (let y = -1; y <= 1; y++)
      for (let z = -1; z <= 1; z++) {
        if (x === 0 && y === 0 && z === 0) continue;
        const m = new THREE.Mesh(geo, bodyMat);
        m.position.set(x * CELL, y * CELL, z * CELL);
        m.userData.home = m.position.clone();
        m.userData.dir = m.position.clone().normalize();
        const clase2 = Math.round(m.userData.home.lengthSq() / (CELL * CELL));
        m.userData.rFactor = clase2 === 1 ? CENTER_F : 1;
        group.add(m);
        cubies.push(m);
        cubieAt[`${x},${y},${z}`] = m;
      }

  const faceMats = [];
  Object.values(FACE_DEFS).forEach((def) => {
    const [nx, ny, nz] = def.normal;
    const maps = makeFaceMaps(def.kanji, def.romaji, { navy: bodyHex, gold: goldHex, inlay });
    const mat = new THREE.MeshStandardMaterial({
      map: maps.colorTex,
      normalMap: maps.normalTex,
      normalScale: new THREE.Vector2(1.3, 1.3),
      roughness: MT.roughness,
      metalness: MT.metalness,
    });
    faceMats.push({ mat, maps, kanji: def.kanji, romaji: def.romaji });

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
  const coreGroup = new THREE.Group();
  coreGroup.visible = false;
  scene.add(coreGroup);
  const core = new THREE.Mesh(new THREE.SphereGeometry(CORE_R, 48, 32), coreMat);
  coreGroup.add(core);

  const WORD_TURN_S = (() => {
    const v = parseFloat(params.get('wordSpin'));
    return Number.isFinite(v) && v >= 4 && v <= 120 ? v : 24;
  })();
  const WORD_SPIN = -(2 * Math.PI) / (WORD_TURN_S * 1000);
  const WORD_FIXED = 0.6;
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
    ctx.font = `500 ${Math.round(H * 0.19)}px 'Zen Kaku Gothic New', sans-serif`;
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
  const wordTilt = new THREE.Group();
  wordTilt.rotation.set(0.10, 0, 0.14);
  wordTilt.add(wordShell);
  coreGroup.add(wordTilt);

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

  const C = {
    rx: 18, ry: -26,
    trx: 0, try: 0,
    velRx: 0, velRy: 0,
    snapping: false, dragging: false, moved: false,
    holdUntil: 0,
    pendPhase: 0,
    parked: false,
    signRy: 1,
  };

  function applyRotation() {
    group.rotation.x = C.rx * DEG;
    group.rotation.y = C.ry * DEG;
  }
  applyRotation();

  const tmpV = new THREE.Vector3();
  function applyExplode(ts) {
    const k = easeInOut(X.t);
    cubies.forEach((m) => {
      tmpV.copy(m.userData.dir).multiplyScalar(EXPLODE_R * m.userData.rFactor);
      m.position.lerpVectors(m.userData.home, tmpV, k);
    });
    const pulsing = X.t === 1 && !reduce;
    const pulse = pulsing ? 1 + 0.015 * Math.sin(ts * 0.0014) : 1;
    coreGroup.scale.setScalar((0.4 + 0.6 * k) * pulse);
    coreGroup.visible = k > 0.02;
    coreMat.emissiveIntensity = pulsing
      ? 0.16 + 0.1 * (0.5 + 0.5 * Math.sin(ts * 0.0014))
      : 0.16;
    wordShell.rotation.y = reduce ? WORD_FIXED : ts * WORD_SPIN;
    wordMat.opacity = Math.max(0, (k - 0.55) / 0.45);
    applyCamera();
  }

  function snapTo(key) {
    const def = FACE_DEFS[key];
    if (!def) return;
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
  function pickCore(clientX, clientY) {
    if (!coreGroup.visible) return false;
    const r = renderer.domElement.getBoundingClientRect();
    ndc.x = ((clientX - r.left) / r.width) * 2 - 1;
    ndc.y = -((clientY - r.top) / r.height) * 2 + 1;
    raycaster.setFromCamera(ndc, camera);
    return raycaster.intersectObject(core, false).length > 0;
  }

  const el = renderer.domElement;
  function onDown(e) {
    C.dragging = true; C.snapping = false; C.moved = false;
    C.parked = false;
    C.velRx = 0; C.velRy = 0;
    onDragStart();
    stage.classList.add('is-dragging');
    try { el.setPointerCapture(e.pointerId); } catch (err) {}
  }
  function onMove(e) {
    if (!C.dragging) {
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
        if (X.t === 1 && pickCore(e.clientX, e.clientY)) onCoreOpen();
      } else {
        const key = pickFace(e.clientX, e.clientY);
        if (key) { onSelect(key); snapTo(key); }
      }
    } else {
      if (Math.abs(C.velRy) > 0.01) C.signRy = Math.sign(C.velRy);
    }
  }
  el.addEventListener('pointerdown', onDown);
  el.addEventListener('pointermove', onMove);
  el.addEventListener('pointerup', onUp);
  el.addEventListener('pointerleave', onUp);

  let lastRx = null, lastRy = null;

  function resize() {
    const w = stage.clientWidth || 1;
    const h = Math.max(stage.clientHeight || 1, 1);
    renderer.setSize(w, h, true);
    camera.aspect = w / h;
    frameCamera();
    lastRx = null;
    renderer.render(scene, camera);
  }
  const ro = new ResizeObserver(resize);
  ro.observe(stage);
  resize();

  let enabled = true;
  let visible = true;
  const sectionCube = document.getElementById('cube');
  if (sectionCube && 'IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((e) => { visible = e.isIntersecting; });
    }, { threshold: 0.02 }).observe(sectionCube);
  }

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
        const idle = C.parked || now() < C.holdUntil;
        const tRy = idle ? 0 : AUTO_RY * C.signRy;

        let tRx = 0;
        if (!idle) {
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
    explode() {
      C.parked = false;
      C.snapping = false;
      X.target = 1;
      if (reduce) X.t = 1;
      lastRx = null;
    },
    reassemble(instant) {
      X.target = 0;
      if (reduce || instant) X.t = 0;
      el.style.cursor = '';
      lastRx = null;
    },
    isExploded() { return X.target === 1; },
    setEnabled(v) {
      enabled = !!v;
      if (enabled) { lastRx = null; resize(); }
    },
    render() { renderer.render(scene, camera); },
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
    isContextLost() { return renderer.getContext().isContextLost(); },
    setRotation(rx, ry) { C.rx = rx; C.ry = ry; C.snapping = false; applyRotation(); },
    dispose() {
      ro.disconnect();
      renderer.dispose();
      el.remove();
    },
  };
}
