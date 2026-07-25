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
tools/make-og-image.py  genera og-image.png (sólo tipografía, sin navegador)
docs/v1-dark/           registro visual de versiones etiquetadas
```

Para desarrollo alcanza con cualquier servidor estático desde la raíz del repo.
Los módulos ES necesitan HTTP, no funcionan por `file://`.

## URLs

Esquema por **directorios**, no archivos sueltos. Cada página es un directorio
con su `index.html` adentro:

```
/            index.html              home EN
/musubi/     musubi/index.html       el núcleo del cubo
/sugao/      sugao/index.html        la persona detrás del proyecto
/method/     method/index.html       el método completo + las fuentes, una por una
/disclaimer/ disclaimer/index.html   免責事項 completo (el único lugar)
/ja/         (previsto)              subárbol paralelo en japonés
```

`/method/` es el **desarrollo**; la sección `#method` de la portada queda como
**resumen** y la nav sigue apuntando ahí. **No hay `/sources/`**: la lista
taxativa de fuentes vive dentro de `/method/`, porque el criterio y su
aplicación no deben poder divergir.

GitHub Pages sirve `/musubi/` como `/musubi/index.html`, y redirige `/musubi`
(sin barra final) a `/musubi/` con un 301. Las URLs no llevan extensión.

`/musubi/` se llamaba `/naming/`. **No quedó redirección**: GitHub Pages sirve
archivos estáticos y no tiene reglas de reescritura, así que la ruta vieja
responde con la 404 del sitio. Es aceptable porque nada de esto está publicado
todavía; si alguna vez se renombra una ruta **ya publicada**, hay que dejar en
su lugar un `index.html` con `<link rel="canonical">` a la nueva y un
`<meta http-equiv="refresh">`, que es lo más parecido a un 301 que permite
Pages.

El archivo `.nojekyll` desactiva el procesamiento con Jekyll: el sitio ya es
estático y no lo necesita. Además evita un problema silencioso — Jekyll ignora
todo path que empiece con `_`, así que sin ese archivo un directorio así
simplemente no se publicaría.

### El `免責事項`: dos textos, dos reglas opuestas

Es la única duplicación deliberada de texto del sitio, y conviene entender por
qué antes de "arreglarla":

| | Dónde vive | Regla |
|---|---|---|
| **Corto** (una línea) | footer global | **se repite** en las diez páginas |
| **Completo** | `/disclaimer/` | **una sola vez**, todo lo demás lo enlaza |

Repetir el corto no es deriva: es su función. Una advertencia sólo sirve si está
donde el lector está leyendo, no en una página a la que haya que llegar. Como
vive en el footer, que es idéntico en las diez páginas, **se redacta una vez** y
se propaga con el mismo script con que se insertó.

El completo, en cambio, no se duplica nunca. Dos copias de un texto legal
derivan, y un sitio que se contradice en su propio descargo pierde exactamente
lo que el descargo da. La prueba práctica: **si son más de una línea, va en
`/disclaimer/`** y desde donde estabas se pone un enlace.

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

- **`check-structure.py`** — nav y footer idénticos en las diez páginas,
  metadatos únicos, URLs absolutas, cobertura del subset japonés, **ningún
  `href="#"` que haya perdido su placeholder** y **ningún placeholder nuevo**
  respecto de `tools/placeholders-baseline.json`. Sale `0` si está bien, `1` si
  algo se rompió.
- **`check-ready.py`** — ¿puede publicarse? Sale `0` listo, **`2` falta trabajo
  previsto** (esperado, no es una regresión) y `1` si hay algo roto de verdad.

  El `2` cubre dos cosas: los placeholders sin redactar y **la revisión legal
  del `免責事項`**. `/disclaimer/` declara ley aplicable japonesa y limitación
  de responsabilidad, y el texto todavía **no lo validó un profesional**. La
  guarda lo detecta por una marca de una sola palabra dentro del propio HTML,
  que se saca a mano después de la revisión. Es un token sin espacios a
  propósito: una marca con espacios se parte en el salto de línea de un
  comentario y deja de encontrarse — pasó en la primera versión, que daba
  «revisado» con el borrador intacto.

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
3. **Que el nav y el footer no hayan derivado** entre las diez páginas.

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
| `sitemap.xml` | lista las 9 páginas indexables | `python tools/make-sitemap.py` |
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
apuntarían a la nada. Tampoco lleva `canonical` ni Open Graph: un canonical en
una página `noindex` no dice nada, y una tarjeta linda al compartirla haría
pasar un enlace roto por contenido.

### Las URLs de metadatos son absolutas, y hay guarda

`canonical`, `og:url` y `og:image` son **absolutas** en las diez páginas
indexables, y `canonical`/`og:url` apuntan cada una **a sí misma**.

No es un detalle de estilo. Quien arma la vista previa —LinkedIn, Slack, X,
WhatsApp— **no es el navegador del lector** y no tiene contra qué resolver una
ruta relativa: con `og:image="/og-image.png"` la tarjeta sale sin imagen. Y el
fallo no se ve en el sitio, que anda perfecto; se ve afuera, donde nadie mira.
Un `canonical` que apunta a otra página es peor que no tenerlo: le dice al
buscador que ésta no es la versión buena.

`check-structure.py` lo verifica en cada commit, justamente porque es un fallo
silencioso.

### La imagen OG puede quedar vieja sin que nada avise

Es un archivo, no una vista: no se «re-renderiza» solo. Si cambia algo de lo que
la determina, el PNG sigue mostrando la versión anterior.

Mismo problema que el sitemap, distinta solución: el sitemap se regenera barato y
se compara la **salida**; acá se comparan las **entradas**.
`tools/og-image.lock.json` guarda un hash de cada una y `check-structure.py`
avisa si alguna cambió.

**La lista tiene que ser exacta en las dos direcciones.** Una entrada de más
produce avisos por cambios que ya no influyen —señal falsa, que es lo que hace
que una guarda se deje de mirar—; una de menos deja la imagen vieja en silencio,
que es el fallo que esto viene a tapar. Vigentes:

| Entrada | Por qué |
|---|---|
| `tools/make-og-image.py` | define la composición entera |
| el `:root` de `styles.css` | de ahí lee los colores |
| `inter-latin.woff2` | el nombre y la bajada |
| `zen-kaku-…-500-subset.woff2` | el 言霊 |

Salieron de la lista cuando la tarjeta dejó de llevar el cubo: **`cube.js`**, que
ya no aparece en la imagen, y **Cormorant**, que ya no se usa.

Se hashea **sólo el `:root`** y no `styles.css` entero: el CSS cambia todo el
tiempo por cosas que no tocan la tarjeta. Verificado en las dos direcciones:
cambiar `--c-gold` avisa **y regenerar produce un PNG distinto**; cambiar la luz
del cubo o la opacidad del footer no avisa.

Y los archivos de **texto se hashean normalizando los saltos de línea**; las
fuentes, por bytes crudos. En Windows `core.autocrlf=true` hace que git guarde LF
y escriba CRLF al hacer checkout, así que hashear los bytes del `.py` hacía
saltar la guarda con sólo cambiar de rama, o al **clonar el repo de nuevo** —
justo el caso que motivó comparar contenido en vez de fechas. Las fuentes son
binarias, git no las toca, y ahí el byte crudo sí es el contenido.

```
python tools/make-og-image.py            # regenera y vuelve a sellar
python tools/make-og-image.py --sellar   # acepta la imagen actual sin regenerar
```

El `--sellar` es para cuando la imagen la pone el autor a mano en vez del script.

**La imagen OG es 1200×630** (relación 1.91:1), que es la medida canónica: la
que piden Facebook, LinkedIn, Slack, Discord y X. Debajo de 600×315 varias
plataformas degradan a miniatura cuadrada.

Es **sólo tipografía**: 言霊 en oro, el nombre de la marca y la bajada. No lleva
el cubo. Por eso el script **no necesita navegador ni servidor** —sólo las
fuentes— y la tarjeta se lee como institucional.

**La medida que manda no es 1200 px sino ~500**, que es el ancho al que se ve en
un feed de escritorio: un 42%. Lo que no se lea ahí no está sirviendo, por bien
que se vea a tamaño completo. Para juzgarla así:

```
python tools/make-og-image.py --prueba
```

deja además `_dev/og-image-500px.png`. Dos consecuencias de haber mirado a ese
tamaño: el nombre de la marca está al doble de cuerpo y en blanco (a 23 px en
azul grisáceo quedaba en ~10 px de feed, y era lo primero que se perdía), y la
bajada va en **Inter y no en Cormorant** — es una serif de display con astas
finas, el mismo problema que obligó a pasar el romaji del cubo a Inter. Cormorant
sigue siendo la voz de marca en el sitio, donde el texto se ve a tamaño real.

**El script lee los colores del `:root` de `styles.css`**, no los copia. Es la
diferencia con `make-favicon.py`, que sí los copia porque un icono de 16 px no
puede depender de parsear un CSS. Copiarlos acá tendría dos costos: la tarjeta
derivaría de la paleta sin que nadie lo note, y `:root` dejaría de ser una
entrada real de la imagen — con lo cual la guarda de abajo avisaría por cambios
que no la afectan, o no avisaría por los que sí.

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
4. **`/musubi/` puede querer otro rótulo en japonés.** En inglés la nav dice
   «Musubi», que es el romaji. La versión japonesa podría preferir escribirlo en
   kanji —**産霊** o **結び**—, que no son intercambiables: 産霊 es el término del
   núcleo que ya aparece en la página, y 結び es la palabra corriente para «nudo,
   atadura». Es una decisión del autor, no una traducción mecánica; queda
   anotada, sin implementar.

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
