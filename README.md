# Kotodama Finance — página de entrada

Plataforma pública y gratuita de datos y análisis del sistema financiero
japonés. Este repo publica en GitHub Pages (kotodamafinance.com).

Sitio estático: sin backend, sin frameworks, sin build step. Se sirve tal cual.

## Estructura

```
index.html              home EN: todo el contenido y los enlaces, en el fuente
assets/css/styles.css   tokens en :root + estilos (compartido por todas las páginas)
assets/js/background.js océano WebGL de fondo
assets/js/cube.js       cubo de navegación (Three.js)
assets/js/main.js       orquestador: toggle, nav, visibilidad
assets/fonts/           tipografías auto-hospedadas y subseteadas
assets/vendor/          Three.js vendoreado (sin CDN en runtime)
tools/check-ready.py    guarda previa a publicar (ver más abajo)
docs/v1-dark/           registro visual de versiones etiquetadas
```

Para desarrollo alcanza con cualquier servidor estático desde la raíz del repo.
Los módulos ES necesitan HTTP, no funcionan por `file://`.

## URLs

Esquema por **directorios**, no archivos sueltos. Cada página es un directorio
con su `index.html` adentro:

```
/            index.html          home EN
/naming/     naming/index.html   subpágina
/ja/         (previsto)          subárbol paralelo en japonés
```

GitHub Pages sirve `/naming/` como `/naming/index.html`, y redirige `/naming`
(sin barra final) a `/naming/` con un 301. Las URLs no llevan extensión.

El archivo `.nojekyll` desactiva el procesamiento con Jekyll: el sitio ya es
estático y no lo necesita. Además evita un problema silencioso — Jekyll ignora
todo path que empiece con `_`, así que sin ese archivo un directorio así
simplemente no se publicaría.

## Antes de publicar

Antes de cualquier merge a `main`, correr:

```
python tools/check-ready.py
```

Tiene que terminar con `LISTO PARA PUBLICAR` y código de salida 0. Comprueba:

1. **Que no queden placeholders de redacción.** Equivale a
   `grep -c 'class="todo"' index.html` sobre todos los HTML publicables, y tiene
   que dar **0**. Un placeholder en producción es texto en castellano dirigido
   al autor apareciendo en un sitio en inglés.
2. **Que el subset japonés cubra todos los glifos del sitio** (ver abajo).

## Tipografías: el subset es un paso obligatorio

Las tipografías están auto-hospedadas y subseteadas. El subset de **Zen Kaku
Gothic New** contiene exactamente los glifos japoneses que aparecen en el sitio,
y nada más — por eso pesa ~13 KB en vez de 2,3 MB.

**Cada vez que se agrega texto japonés nuevo hay que regenerar el subset.** Si
no, ese carácter se renderiza con una fuente del sistema: no desaparece, sólo
desentona, y es fácil que pase inadvertido.

Regenerar (requiere `pip install fonttools brotli`) con las TTF de origen del
repo `google/fonts` (`ofl/zenkakugothicnew`). `$JA` es la cadena completa de
glifos japoneses del sitio, que está listada en el comentario de `@font-face`
en `assets/css/styles.css`:

```
JA="肇素顔渡世家紋鳥居絆言霊産河川立方体一次資料追跡可能公開日本銀行財務省金融庁取引所内閣府総語免責事項　"

pyftsubset ZenKakuGothicNew-Regular.ttf \
  --output-file=assets/fonts/zen-kaku-gothic-new-400-subset.woff2 \
  --flavor=woff2 --text="$JA" --unicodes=U+0020-007F,U+3000

pyftsubset ZenKakuGothicNew-Medium.ttf \
  --output-file=assets/fonts/zen-kaku-gothic-new-500-subset.woff2 \
  --flavor=woff2 --text="$JA" --unicodes=U+0020-007F,U+3000
```

El latín básico va incluido para tramos mixtos como «e-Stat / 総務省».

**Verificar contra la tabla `cmap` de la fuente**, que es la única fuente de
verdad sobre qué glifos contiene:

```
python tools/check-ready.py
```

**No usar `document.fonts.check()` para esto.** Informa si la fuente está
cargada, no si contiene el glifo: devuelve `true` para caracteres que la fuente
no puede dibujar. Ya dio un falso positivo con 免責事項.

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
