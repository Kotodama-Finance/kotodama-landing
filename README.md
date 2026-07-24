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
favicon.ico/.svg        iconos del sitio (generados, ver más abajo)
apple-touch-icon.png    icono para «añadir a inicio» en iOS
sitemap.xml             generado por tools/make-sitemap.py
robots.txt              todo abierto, incluidos los crawlers de IA
404.html                la sirve GitHub Pages ante cualquier ruta inexistente
og-image.png            tarjeta al compartir (generada)
tools/check-structure.py guarda estructural: verde siempre (ver más abajo)
tools/check-ready.py    guarda previa a publicar (roja hasta la redacción)
tools/make-favicon.py   genera los iconos a partir del subset de la marca
tools/make-sitemap.py   genera el sitemap a partir de los HTML publicables
tools/make-og-image.py  genera og-image.png capturando el cubo real
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

## Flujo de trabajo (obligatorio)

**Antes de cada commit** corré las guardas. Si alguna falla, no commitees:
arreglá, o revertí al último commit verde. El objetivo es que todo commit del
historial sea un punto de restauración seguro por construcción, no por suerte.

| Guarda | Cuándo | Costo | Se espera |
|---|---|---|---|
| `tools/check-structure.py` | siempre | instantánea, sin navegador | **verde** |
| `tools/check-modes.py` | siempre | ~40 s | **verde** |
| `tools/check-pendulum.py` | antes de push, o al tocar la física del cubo | ~2–4 min | **verde** |
| `tools/check-ready.py` | antes de publicar a `main` | instantánea | rojo hasta la redacción |

`check-pendulum.py` es la única demasiado lenta para cada commit: mide dos
períodos de una oscilación real en un navegador, y encima el loop corre a un
ritmo variable en headless (~7–15 ticks/s), así que no se puede acortar sin
perder lo que verifica.

Las dos que usan navegador necesitan el sitio servido en `:8000`.

**`check-ready.py` no va en cada commit**, y no es un descuido: mientras queden
placeholders está en rojo por diseño, y una guarda que siempre está en rojo se
deja de mirar — el día que se rompa algo de verdad, pasa inadvertido. Por eso la
verificación estructural vive aparte, en `check-structure.py`, que **sí** tiene
que estar en verde siempre:

- **`check-structure.py`** — nav y footer idénticos en las ocho páginas,
  cobertura del subset japonés, y **ningún placeholder nuevo** respecto de
  `tools/placeholders-baseline.json`. Sale `0` si está bien, `1` si algo se
  rompió.
- **`check-ready.py`** — ¿puede publicarse? Sale `0` listo, **`2` falta
  redacción** (esperado, no es una regresión) y `1` si hay algo roto de verdad.

Al redactar un placeholder el conteo baja: eso **no** falla, pero hay que fijar
el piso nuevo con `python tools/check-structure.py --actualizar-baseline`.

**Si un cambio rompe algo y no se puede arreglar en el momento**, revertir al
último commit verde en vez de dejar el árbol roto, y decir qué se revirtió y
por qué.

**Tags**: sólo en hitos, no cada tanto. El próximo natural es cuando el
andamiaje esté completo, antes del pase de redacción.

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
3. **Que el nav y el footer no hayan derivado** entre las ocho páginas.

Hoy sale **2** (faltan placeholders), que es lo esperado hasta el pase de
redacción; **1** sería una regresión de verdad.

Y con el sitio servido, la guarda de comportamiento del cubo:

```
python tools/check-modes.py
```

Verifica en un navegador real que en modo cubo la grilla esté **recortada** (no
en flujo, pero tampoco en `display:none`: es la capa semántica), que en modo
grilla el escenario compute `display:none`, y el ciclo de selección completo
—carga sin nada seleccionado, clic, arrastre, otro clic—. Existe porque esas
dos cosas se rompieron dos veces, las dos por un cambio de layout que pisó una
regla de CSS, y las dos se detectaron mirando la página en vez de por una
prueba. `check-ready.py` no puede cubrirlo: son estilos computados y eventos.

### Una trampa de CSS que ya mordió dos veces

Varias clases del sitio fijan `display` (`.btn`, `.status`, `.cube__stage`,
`.cube__toggle`). Una clase **le gana por especificidad** a la regla `[hidden]`
del navegador, así que un elemento marcado como oculto seguía viéndose. Hay una
regla `[hidden] { display: none !important; }` al principio de `styles.css` que
lo resuelve para toda la clase de bug. No borrarla.

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

## Iconos (favicon)

Los tres iconos —`favicon.ico` (16/32/48 px), `favicon.svg` y
`apple-touch-icon.png`— **se generan**, no se editan a mano:

```
python tools/make-favicon.py            # regenera los tres
python tools/make-favicon.py --strip    # además, la tira de comparación en _dev/
```

Salen del **mismo subset de la marca** (Zen Kaku peso 500), así que el icono es
literalmente la misma letra 言 que el logo del nav, en oro sobre navy. El SVG
lleva el glifo como `<path>` y no como `<text>`: un favicon no carga webfonts.

Los colores (`--c-navy`, `--c-gold`) están **copiados** en el script, porque un
icono se renderiza aislado y no ve el CSS. Es la misma excepción que el shader
del mar: si cambia la paleta, hay que volver a correr el script.

El `favicon.ico` existe aunque haya `<link>`: el navegador pide `/favicon.ico`
igual, y sin el archivo cada carga deja un 404 en la consola.

## Metadatos y descubribilidad

Que el sitio sea legible por máquinas es un **objetivo** del proyecto, no un
extra: es la misma razón por la que todo el contenido va en el HTML.

| Archivo | Qué hace | Se mantiene |
|---|---|---|
| `sitemap.xml` | lista las 8 páginas indexables | `python tools/make-sitemap.py` |
| `robots.txt` | abre todo y apunta al sitemap | a mano (casi nunca cambia) |
| `og-image.png` | la tarjeta al compartir un enlace | `python tools/make-og-image.py` |
| `404.html` | GitHub Pages la sirve ante cualquier ruta inexistente | a mano |

**El sitemap se genera, no se escribe.** Es una lista duplicada —las mismas URLs
que ya están en el sistema de archivos— y la duplicación acá no hace falta ni
vigilarla: se deriva. Al agregar una página, correr el script. Si alguien se
olvida, `check-structure.py` lo caza, porque verifica que toda página publicable
esté listada.

No lleva `<lastmod>`: sólo sirve si es exacto, para que fuera exacto habría que
sacarlo de git en cada regeneración, y entonces el sitemap cambiaría en cada
commit ensuciando el historial. `<changefreq>` y `<priority>` los ignora Google
desde hace años.

**`robots.txt` no bloquea a los crawlers de IA** (GPTBot, ClaudeBot, CCBot,
PerplexityBot, Google-Extended). No están nombrados porque `User-agent: *` ya
los cubre; el archivo lo dice por escrito para que nadie los agregue «por las
dudas» copiando un robots.txt ajeno.

**La 404 queda fuera del sitemap** y lleva `noindex`: pedir que se indexe la
página de error es lo contrario de lo que hace falta. Usa rutas absolutas porque
GitHub Pages la sirve ante URLs de cualquier profundidad
(`/tosei/algo/inexistente/`), y con rutas relativas el CSS y los enlaces
apuntarían a la nada.

**La imagen OG es 1200×630** (relación 1.91:1), que es la medida canónica: la
que piden Facebook, LinkedIn, Slack, Discord y X. Debajo de 600×315 varias
plataformas degradan a miniatura cuadrada. El cubo **se captura del sitio de
verdad** —por eso el script necesita el servidor en `:8000`, a diferencia de
`make-favicon.py`— porque redibujarlo a mano crearía una copia que deriva del
original en cuanto cambie cualquier parámetro de luz o material.

### hreflang: el patrón para cuando exista `/ja/`

**Todavía no está implementado** — no hay versión japonesa. Cuando la haya, el
patrón es éste, y tiene una regla que se incumple seguido:

**Las declaraciones tienen que ser recíprocas y cada página se declara a sí
misma.** Si `/hajime/` apunta a `/ja/hajime/` pero la japonesa no apunta de
vuelta, Google descarta el par entero. Y si una página no se lista a sí misma,
tampoco vale.

En el `<head>` de **las dos** versiones de cada página, el mismo bloque idéntico:

```html
<link rel="alternate" hreflang="en" href="https://kotodamafinance.com/hajime/">
<link rel="alternate" hreflang="ja" href="https://kotodamafinance.com/ja/hajime/">
<link rel="alternate" hreflang="x-default" href="https://kotodamafinance.com/hajime/">
```

`x-default` apunta a la inglesa: es la que ve quien no coincide con ningún
idioma declarado. Y en Open Graph, `<meta property="og:locale" content="en_US">`
con `og:locale:alternate` = `ja_JP` (invertidos en la versión japonesa).

Tres cosas más para ese día:

1. **`<html lang="ja">`** en las páginas japonesas — hoy las ocho dicen `en`.
2. **El `canonical` de cada página apunta a sí misma**, nunca de la japonesa a
   la inglesa: son contenidos distintos, no duplicados.
3. **El sitemap puede llevar los alternates** con `xmlns:xhtml` y un
   `<xhtml:link>` por idioma dentro de cada `<url>`. `make-sitemap.py` habrá que
   extenderlo; hoy emite sólo `<loc>`.

Y lo de siempre: **cada texto japonés nuevo obliga a regenerar el subset**, que
para una versión japonesa entera significa rehacerlo con el corpus completo —
ahí ya no alcanza con listar los kanji a mano.

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
  contexto WebGL no arranca. También queda sin efecto el folio de entrada (que
  aparece de una) y la transición entre páginas (que ni se declara).

- **Entrar a una cara atraviesa una transición entre documentos** (el
  «maelstrom»), hecha sólo con `@view-transition` — sin SPA ni router. La página
  gira, escala y se desenfoca; la nueva entra girada y se acomoda. Es progresiva:
  un navegador sin soporte navega normal. En pantallas táctiles es más liviana
  (sin desenfoque). Bajo `prefers-reduced-motion` no se declara.

- **El bloque de estado + botón bajo el cubo es un folio que se despliega.**
  Arranca con altura cero y se abre animado al seleccionar una cara; se cierra al
  arrastrar. No empuja nada visible porque está debajo del cubo. Verlo en detalle
  en `CLAUDE.md`.
