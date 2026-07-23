# Kotodama Finance — página de entrada

Plataforma pública y gratuita de datos y análisis del sistema financiero
japonés. Este repo publica en GitHub Pages (kotodamafinance.com).

Sitio estático: sin backend, sin frameworks, sin build step. Se sirve tal cual.

## Estructura

```
index.html              todo el contenido y los enlaces, en el fuente
assets/css/styles.css   tokens en :root + estilos
assets/js/background.js océano WebGL de fondo
assets/js/cube.js       cubo de navegación (Three.js)
assets/js/main.js       orquestador: toggle, nav, visibilidad
assets/fonts/           tipografías auto-hospedadas y subseteadas
assets/vendor/          Three.js vendoreado (sin CDN en runtime)
```

Para desarrollo alcanza con cualquier servidor estático desde la raíz del repo.
Los módulos ES necesitan HTTP, no funcionan por `file://`.

## Decisiones

- **El contenido va en el HTML, no inyectado por JS.** La descubribilidad por
  buscadores y por crawlers de IA es un objetivo explícito del proyecto, y esos
  crawlers en general no ejecutan JavaScript. El cubo 3D se hidrata por JS, pero
  el texto, los enlaces y las seis caras están en el fuente.

- **La grilla de seis es la capa semántica.** Es la navegación de teclado y lo
  que leen los crawlers. En vista 3D se oculta visualmente con el patrón clip —
  nunca con `display:none` — y se revela al recibir foco. El canvas del cubo va
  `aria-hidden`.

- **Ningún color literal fuera de `:root`.** Incluye los que consume el JS, que
  se leen con `getPropertyValue` sin fallback: si falta un token, el cubo falla
  con el nombre del token en vez de disfrazarlo con un hex de repuesto.

- **La paleta del mar es la excepción: vive en el GLSL, no en `:root`.** Los
  colores del océano (`deep`, `mid`, `crest`) son constantes dentro del fragment
  shader de `assets/js/background.js`, que es código calibrado a mano y cerrado;
  cambiar el color del mar requiere editar el shader, no los tokens, y esos
  valores no se sincronizan solos si cambia la paleta.

- **El cubo va en Three.js, no en CSS 3D.** CSS 3D no tiene z-buffer: el cubo
  anterior sufría z-fighting y bleed-through (se veían los kanji de las caras
  traseras). Con geometría real la oclusión la resuelve el depth buffer.

- **Tipografías auto-hospedadas y subseteadas**, sin terceros. El subset japonés
  cubre exactamente los glifos que aparecen en la página: si cambia un nombre de
  cara o cualquier texto japonés hay que regenerarlo. Glifos y comando de
  regeneración están documentados en `assets/css/styles.css`.

- **`prefers-reduced-motion`** se respeta: el mar dibuja un único cuadro fijo y
  el cubo queda estático pero arrastrable. El degradado atmosférico vive en el
  `background` del `body`, siempre presente, para que nunca quede un hueco si el
  contexto WebGL no arranca.
