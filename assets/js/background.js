/* =========================================================================
   Fondo: océano WebGL.
   Shader y parámetros = versión de PRODUCCIÓN (fbm de 5 octavas), calibrada y
   aprobada. NO tocar el GLSL ni los valores SPEED/BREATH.

   ---------------------------------------------------------------------------
   PALETA DEL MAR: VIVE EN EL GLSL, NO EN :root
   ---------------------------------------------------------------------------
   Es la única excepción al sistema de tokens del proyecto. Los colores del
   océano son constantes dentro del fragment shader, porque forman parte del
   código calibrado a mano que está cerrado. Cambiar el color del mar exige
   editar el shader acá abajo; tocar :root no tiene ningún efecto sobre él.

   Las constantes son tres, en la función main() (~línea 107), y se mezclan
   según la altura de ola H:
     deep  = vec3(0.001, 0.009, 0.024)   ~#000206   senos, la parte más honda
     mid   = vec3(0.024, 0.075, 0.130)   ~#061321   cuerpo del agua
     crest = vec3(0.075, 0.150, 0.215)   ~#132637   crestas iluminadas
   Más un realce vertical aditivo: col += uv.y * vec3(0.010, 0.020, 0.030),
   que aclara levemente hacia el horizonte.

   Los valores van directo a gl_FragColor sin corrección de gamma, así que se
   leen como sRGB. Quedan dentro de la familia navy de la marca (mid es casi
   idéntico al fondo de sección), pero NO están sincronizados con los tokens:
   si la paleta cambia en :root, estos hay que actualizarlos a mano.
   ---------------------------------------------------------------------------

   Estrategia de rendimiento:
   - Desktop: resolución completa (DPR hasta 2), sin cap de FPS.
   - Móvil (pointer:coarse): media resolución (DPR*0.5) + cap de 25 fps.
   - prefers-reduced-motion: se dibuja UN solo frame estático (atmósfera del
     shader, sin movimiento) y se detiene el loop.
   - Sin WebGL: se oculta el canvas y se muestra el fallback CSS (.sea-fallback).
   ========================================================================= */

const VERT = 'attribute vec2 p; void main(){ gl_Position=vec4(p,0.0,1.0); }';

// Fragment shader — copiado 1:1 de index.html en producción (5 octavas).
const FRAG = `
precision highp float;
uniform vec2 u_res; uniform float u_time;
uniform float u_speed;   // travel speed of the waves
uniform float u_breath;  // breathing of the swell (independent)

vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;}
vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}
vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);}
vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}
float snoise(vec3 v){
  const vec2 C=vec2(1.0/6.0,1.0/3.0); const vec4 D=vec4(0.0,0.5,1.0,2.0);
  vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx);
  vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.0-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy);
  vec3 x1=x0-i1+C.xxx; vec3 x2=x0-i2+C.yyy; vec3 x3=x0-D.yyy;
  i=mod289(i);
  vec4 pp=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));
  float n_=0.142857142857; vec3 ns=n_*D.wyz-D.xzx;
  vec4 j=pp-49.0*floor(pp*ns.z*ns.z);
  vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.0*x_);
  vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.0-abs(x)-abs(y);
  vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw);
  vec4 s0=floor(b0)*2.0+1.0; vec4 s1=floor(b1)*2.0+1.0; vec4 sh=-step(h,vec4(0.0));
  vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
  vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w);
  vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
  p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;
  vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0); m=m*m;
  return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
}

float fbm(vec3 p){
  float s=0.0,a=0.55;
  for(int i=0;i<5;i++){ s+=a*snoise(p); p*=2.02; a*=0.5; }
  return s;
}

vec2 anis(vec2 p){
  vec2 q = vec2(p.x+p.y, p.y-p.x)*0.7071;
  q.x *= 0.45;
  q.y *= 1.55;
  return q;
}

float ocean(vec2 uvp, float t){
  vec2 V = normalize(vec2(1.0,-1.0));
  vec2 base = uvp + V * (u_time * u_speed);
  float swell = fbm(vec3(base*0.7, u_time*u_breath)) * 2.0;
  vec2 slope = vec2(
    fbm(vec3(base*0.7+vec2(0.15,0.0), u_time*u_breath)) - swell/2.0,
    fbm(vec3(base*0.7+vec2(0.0,0.15), u_time*u_breath)) - swell/2.0
  );
  vec2 wp = anis(base*1.6 + slope*0.6);
  float wn = fbm(vec3(wp, u_time*u_breath*1.3));
  float crest = wn>0.0 ? pow(wn, 0.7) : -pow(-wn, 1.5);
  float waves = crest * 2.1;
  vec2 cp = anis(base*3.8 + slope*0.4);
  float ripple = fbm(vec3(cp, u_time*u_breath*1.8));
  ripple = ripple>0.0 ? pow(ripple,0.8) : -pow(-ripple,1.3);
  float chop = ripple * 0.30;
  return swell + waves + chop;
}

float oceanSmooth(vec2 uvp, float t){
  vec2 V = normalize(vec2(1.0,-1.0));
  vec2 base = uvp + V * (u_time * u_speed);
  float swell = fbm(vec3(base*0.7, u_time*u_breath)) * 2.0;
  vec2 slope = vec2(
    fbm(vec3(base*0.7+vec2(0.15,0.0), u_time*u_breath)) - swell/2.0,
    fbm(vec3(base*0.7+vec2(0.0,0.15), u_time*u_breath)) - swell/2.0
  );
  vec2 wp = anis(base*1.6 + slope*0.6);
  float wn = fbm(vec3(wp, u_time*u_breath*1.3));
  float crest = wn>0.0 ? pow(wn, 0.7) : -pow(-wn, 1.5);
  float waves = crest * 2.1;
  return swell + waves;
}

void main(){
  vec2 uv = gl_FragCoord.xy/u_res.xy;
  float aspect = u_res.x/u_res.y;
  vec2 p = vec2(uv.x*aspect, uv.y);
  float t = u_time * 0.09;
  float persp = mix(1.5, 3.2, uv.y);
  vec2 sp = p*persp;
  float H = ocean(sp, t);
  float e = 0.008*persp;
  float hx = oceanSmooth(sp+vec2(e,0.0), t) - oceanSmooth(sp-vec2(e,0.0), t);
  float hy = oceanSmooth(sp+vec2(0.0,e), t) - oceanSmooth(sp-vec2(0.0,e), t);
  vec3 n = normalize(vec3(-hx*5.2, -hy*5.2, 0.13));
  vec3 deep  = vec3(0.001,0.009,0.024);
  vec3 mid   = vec3(0.024,0.075,0.130);
  vec3 crest = vec3(0.075,0.150,0.215);
  vec3 col = mix(deep, mid, smoothstep(-0.7,0.8,H));
  col = mix(col, crest, smoothstep(0.20,0.95,H)*0.85);
  col += uv.y*vec3(0.010,0.020,0.030);
  vec3 L = normalize(vec3(-0.35,0.65,0.6));
  float shade = dot(n, L) * 0.5 + 0.5;
  col *= mix(0.62, 1.20, smoothstep(0.12, 0.94, shade));
  gl_FragColor = vec4(col,1.0);
}`;

// Valores calibrados de producción — no tocar.
const SPEED = 0.040;
const BREATH = 0.050;

/* Instante del frame estático que se dibuja con prefers-reduced-motion.
   NO puede ser t=0: ahí el campo de ruido está en su estado más plano y el mar
   sale sin forma. A t=12s el swell ya viajó y tiene relieve.
   Ajustable: initSea(canvas, reduce, stillTime) toma cualquier otro instante. */
const STILL_TIME = 12.0;

function compile(gl, type, src) {
  const s = gl.createShader(type);
  gl.shaderSource(s, src);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) console.error(gl.getShaderInfoLog(s));
  return s;
}

/**
 * Inicializa el océano de fondo.
 * @param {HTMLCanvasElement} canvas  #sea
 * @param {boolean} reduce            prefers-reduced-motion activo
 * @param {number} [stillTime]        instante del frame estático (reduced-motion)
 */
export function initSea(canvas, reduce, stillTime = STILL_TIME) {
  // Si el contexto no arranca, ocultamos el canvas y queda el degradado de piso
  // que vive en el background del body. Nunca hay un hueco.
  // En reduced-motion dibujamos un único frame: preserveDrawingBuffer evita que
  // el canvas se vacíe tras el primer composite.
  const attrs = reduce ? { preserveDrawingBuffer: true } : undefined;
  const gl = canvas.getContext('webgl', attrs) || canvas.getContext('experimental-webgl', attrs);
  if (!gl) { canvas.style.display = 'none'; return null; }

  const coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
  const resScale = coarse ? 0.5 : 1;         // móvil: media resolución
  const minFrame = coarse ? 40 : 0;          // móvil: cap ~25 fps

  const prog = gl.createProgram();
  gl.attachShader(prog, compile(gl, gl.VERTEX_SHADER, VERT));
  gl.attachShader(prog, compile(gl, gl.FRAGMENT_SHADER, FRAG));
  gl.linkProgram(prog);
  gl.useProgram(prog);

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const lp = gl.getAttribLocation(prog, 'p');
  gl.enableVertexAttribArray(lp);
  gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);

  const uR = gl.getUniformLocation(prog, 'u_res');
  const uT = gl.getUniformLocation(prog, 'u_time');
  const uSpeed = gl.getUniformLocation(prog, 'u_speed');
  const uBreath = gl.getUniformLocation(prog, 'u_breath');

  function resize() {
    const d = Math.min(window.devicePixelRatio || 1, 2) * resScale;
    canvas.width = (window.innerWidth * d) | 0;
    canvas.height = (window.innerHeight * d) | 0;
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  window.addEventListener('resize', resize);
  resize();

  function drawAt(timeSec) {
    gl.uniform2f(uR, canvas.width, canvas.height);
    gl.uniform1f(uT, timeSec);
    gl.uniform1f(uSpeed, SPEED);
    gl.uniform1f(uBreath, BREATH);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }

  // reduced-motion: un frame estático (mar con forma, sin movimiento), sin loop.
  if (reduce) {
    const still = () => drawAt(stillTime);
    still();
    // redibujar el frame estático si cambia el tamaño (sin animar)
    window.addEventListener('resize', still);
    return { drawAt, setHeroVisible() {} };
  }

  // Loop animado. Se pausa cuando el hero no está visible (lo maneja main.js
  // vía el flag heroVisible) o con la pestaña oculta.
  const state = { heroVisible: true };
  const s0 = performance.now();
  let last = 0;
  (function frame(now) {
    requestAnimationFrame(frame);
    if (state.heroVisible === false || document.hidden) return;
    if (minFrame && now - last < minFrame) return;
    last = now;
    drawAt((now - s0) * 0.001);
  })(s0);

  // handle para que main.js pause/reanude según visibilidad
  return {
    setHeroVisible(v) { state.heroVisible = v; },
    drawAt,
  };
}
