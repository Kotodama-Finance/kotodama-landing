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
docs/mediciones/        mediciones con fecha y condiciones (luz, rendimiento)
```

Para desarrollo alcanza con cualquier servidor estático desde la raíz del repo.
Los módulos ES necesitan HTTP, no funcionan por `file://`.

## El import map

`cube.js` importa Three.js con el especificador desnudo `three`. Un navegador no
sabe resolver eso solo: quien lo traduce es el **import map**, que vive en
`index.html` justo antes del `<script type="module">` que arranca `main.js`.

```html
<script type="importmap">
{ "imports": { "three": "./assets/vendor/three.module.js" } }
</script>
<script type="module" src="./assets/js/main.js"></script>
```

Es lo que hace posible tener Three.js vendoreado sin bundler: el especificador
queda igual que si viniera de un CDN, y el mapa lo apunta al archivo local.

Tres cosas que no se ven mirando el HTML:

- **La ruta se resuelve contra el documento que lleva el mapa**, no contra el
  módulo que hace el `import`. Por eso los bancos de prueba de `_dev/` llevan el
  mismo mapa con `../assets/vendor/three.module.js`: están un nivel más abajo.
- **El mapa tiene que ir antes del primer módulo que lo use**, y sólo puede haber
  uno por documento. Declarado después, no se aplica: la resolución de `three`
  falla, el `await import('./cube.js')` de `hydrateCube()` lanza, y el `catch`
  de `main.js` deja la grilla como navegación con un `console.warn`. **El sitio
  no se rompe, sólo se queda sin cubo** — que es el modo de fallo buscado, pero
  también es silencioso, así que conviene mirar la consola.
- **`RoundedBoxGeometry` no pasa por el mapa.** `cube.js` la importa por ruta
  relativa (`../vendor/RoundedBoxGeometry.js`), así que no aparece ahí y no hay
  que agregarla.

**Al agregar una página, el mapa sólo hace falta si esa página monta el cubo.**
Hoy vive únicamente en `index.html`, que es la única página publicable con
JavaScript: las otras diez —las seis caras, `/musubi/`, `/method/`, `/sugao/`,
`/disclaimer/` y la 404— no cargan ningún script. Un import map **no se hereda
entre documentos**, así que una página nueva que quiera el cubo necesita **su
propia copia**, con la ruta corregida a su profundidad. El caso previsto es
`/ja/index.html`: un nivel abajo, o sea `../assets/vendor/three.module.js`.

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
| **Corto** (una línea) | footer global | **se repite** en todas las páginas |
| **Completo** | `/disclaimer/` | **una sola vez**, todo lo demás lo enlaza |

Repetir el corto no es deriva: es su función. Una advertencia sólo sirve si está
donde el lector está leyendo, no en una página a la que haya que llegar. Como
vive en el footer, que es idéntico en todas las páginas, **se redacta una vez** y
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

- **`check-structure.py`** — nav y footer idénticos en todas las páginas,
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
3. **Que el nav y el footer no hayan derivado** entre todas las páginas.

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

## El cubo: parámetros vigentes

**Todo lo de acá está leído de `assets/js/cube.js` y del `:root` de
`assets/css/styles.css`. Si algo no coincide, manda el código y esta tabla está
vieja.** Las capturas de `docs/v1-dark/` y las mediciones de `docs/mediciones/`
son registros con fecha, no la definición: valen para el momento en que se
tomaron y varias de sus cifras ya no son las de hoy.

### Geometría

Son **26 cubies redondeados, todos idénticos**, que llenan el volumen **3×3×3**.
No hay cubie central: el núcleo está vacío porque no se ve nunca, y el cubo se
lee sólido porque los 26 son opacos y el depth buffer resuelve la oclusión —que
es la razón de haber pasado de CSS 3D a Three.js.

| Constante | Valor | Qué es |
|---|---|---|
| `CELL` | `1` | paso de la grilla: la unidad de todo lo demás |
| `GAP` | `0.022` | separación entre cubies |
| `CUBIE` | `0.978` | arista del cubie, derivada: `CELL - GAP` |
| `RADIUS` | `0.03` | radio del bisel |
| `PLATE` | `0.918` | zona plana de la cara, derivada: `CUBIE - 2·RADIUS` |

`GAP` y `RADIUS` van los dos chicos, y por la misma razón: **se suman en el vacío
que se abre donde concurren cuatro esquinas redondeadas.** Si crecen, ese hueco
deja de leerse como junta y se abre en rombo. La malla es
`RoundedBoxGeometry(CUBIE, CUBIE, CUBIE, 3, RADIUS)` — 3 segmentos de bisel.

### Encuadre de cámara

`PerspectiveCamera(fov 24, near 0.1, far 100)`, con la distancia **calculada en
cada `resize()`**, nunca fija:

```
CUBE_RADIUS = √3 · (CELL + CUBIE/2) ≈ 2.579     // esfera envolvente
FIT_MARGIN  = 1.06
camera.z    = CUBE_RADIUS · FIT_MARGIN / sin(min(halfV, halfH))
```

Dos detalles que importan: es **seno, no tangente** (la esfera envolvente, no la
cara), y **manda el semiángulo más chico de los dos**. En un escenario apaisado
gana la vertical y `camera.z ≈ 13.2`; en uno más alto que ancho gana la
horizontal y la cámara se aleja más. Ésa es la variable que queda sin medir en
móvil, donde el escenario cambia de proporción.

`setPixelRatio(min(devicePixelRatio, 2))`, y **1.5 en punteros gruesos**, donde
además se apaga el antialias.

### Luces y material — VIGENTES

Las intensidades y posiciones están en `LIGHT_DEFAULTS`; los colores salen de los
tokens, nunca literales.

| Luz | Intensidad | Posición | Color |
|---|---|---|---|
| `hemi` | **3.5** | — | cielo `--c-cube-key-light`, suelo `--c-navy` |
| `key` | **2.9** | `[-3, 5, 4]` | `--c-cube-key-light` |
| `rim` | **0.65** | `[4.5, 0.5, 2.5]` | `--c-gold-soft` |
| `back` | **1.3** | `[2.5, 1.5, -4]` | `--c-gold-soft` |

Material del cubie: **`roughness 0.72`, `metalness 0.02`**. Mate a propósito:
roughness bajo concentra el reflejo en un punto y lee metálico, y metalness sin
environment map oscurece en vez de brillar.

El ambiente domina sobre el total direccional, que es lo que da el degradé suave.
La clave y el hemisférico son **neutros** —tintarlos de oro le come el canal azul
al navy y lo desatura a gris—; el oro entra por `rim` y `back`, y por el trazo
incrustado.

> **El juego `hemi 2.2 · key 1.8 · rim 0.4 · back 0.8` es HISTÓRICO**: es el del
> tag `v1-dark`, y está documentado en `docs/v1-dark/README.md`. **No es el
> actual.** Las intensidades subieron al aclarar el fondo de sección de `#020509`
> a `#05111d`, porque la separación del cubo contra su fondo se sostiene con
> **luz** y no oscureciendo la página. El reparto entre las cuatro no cambió, así
> que el carácter difuso se conserva.

### Colores — VIGENTES

| Token | Valor | Dónde |
|---|---|---|
| `--c-cube-body` | `#040d18` | cuerpo del cubie |
| `--c-surface-cube` | `#05111d` | fondo de la sección del cubo |
| `--c-gold` | `#c8a85a` | el trazo incrustado |
| `--c-gold-soft` | `#e7d6a6` | `rim` y `back` |
| `--c-cube-key-light` | `#ffffff` | `key` y el cielo del hemisférico |

**`#020509` ya no es el fondo de nada.** Aparece en `docs/v1-dark/README.md` y en
un comentario de `styles.css` como el valor anterior: era un casi negro que hacía
leer la página como tres páginas pegadas, y se reemplazó por una rampa suave
entre secciones. Cualquier documento que lo dé como fondo actual está desactualizado.

El cuerpo del cubie es el navy de marca sin deriva, y eso está medido: dentro de
la familia navy a esa profundidad **todas las variantes caen dentro de ~4 unidades
sRGB**, o sea que el color base no es una palanca perceptible. Lo que separa el
cubo del fondo es la luz. Ver `docs/mediciones/luz-arco.md`.

### Física: el péndulo

| Constante | Valor | Qué es |
|---|---|---|
| `PEND_CENTER` | `18` | grados: el centro, la vista 3/4 |
| `PEND_AMP` | `20` | grados de excursión a cada lado |
| `PEND_PEAK` | `0.09` | velocidad máxima, grados por tick |
| `PEND_RATE` | `0.0045` | radianes de fase por tick, derivada: `PEND_PEAK / PEND_AMP` |
| `TRACK_GAIN` | `0.004` | corrección hacia la posición ideal, por grado de desvío |
| `RETURN_MAX` | `0.6` | techo de velocidad (~18°/s): vuelve desde rx=180 en ~8 s |
| `VEL_LERP` | `0.095` | lerp de velocidad: converge en ~1 s |
| `AUTO_RY` | `0.28` | autorrotación en Y, grados por tick |

Pose inicial: **`rx 18, ry -26`**. El loop es `requestAnimationFrame` con un
piso de **32 ms por tick** (~30 fps), que es el ritmo con el que calzan esos
valores de damping. El porqué de cada decisión —la fase que siempre avanza, la
herencia de dirección sólo en `ry`— está en `CLAUDE.md`.

### `snap` y el estado `parked`

Son dos cosas distintas y conviene no confundirlas: **el snap es el movimiento,
`parked` es el estado en que queda.**

`snapTo(key)` pone `parked = true` y lleva la rotación al objetivo de la cara con
un lerp de **0.12** por tick, hasta que las dos componentes quedan a menos de
**0.2°**; ahí clava los valores exactos y arranca un `hold` de **2600 ms**. El
ángulo objetivo pasa por `nearest()`, que elige el equivalente a ±180° del actual:
sin eso el cubo desenrollaría vueltas enteras para llegar al mismo lado. Bajo
`prefers-reduced-motion` no hay lerp: salta al objetivo y listo.

**`parked` es la razón por la que el cubo se queda quieto indefinidamente al
seleccionar una cara**, y no vuelve a arrancar solo pasado el hold. Mientras esté
puesto, la velocidad objetivo de los dos ejes es 0. **Sólo un drag nuevo lo
revive**: `pointerdown` lo apaga y deshace la selección, que es la misma acción
que repliega el folio.

Un `pointerup` cuenta como click limpio si `|dx| + |dy|` nunca pasó de **3 px**
acumulados: entonces se hace raycast contra los cubies, se selecciona la cara y
se hace el snap. Si hubo arrastre, en cambio, la autorrotación hereda el **signo**
del tiro (sólo en Y). El arrastre convierte a **0.45° por píxel**.

**Render bajo demanda**: el loop sólo redibuja si `rx` o `ry` se movieron más de
**0.002°**. Con el cubo `parked` eso es nunca, así que un cubo detenido no
consume GPU. Lo mismo hace `setEnabled(false)` en modo grilla, que pausa el loop
entero; al volver, invalida la caché y fuerza un cuadro.

### Lazy-init del contexto WebGL

**Hay dos `IntersectionObserver` sobre `#cube`, y hacen cosas distintas.** Se
confunden fácil porque miran el mismo elemento.

1. **`main.js` — crear el contexto.** `hydrateCubeWhenNear()` no importa
   `cube.js` hasta que la sección toca el viewport; ahí se desconecta y no vuelve
   a correr. Lo que se difiere **no es dibujar** —la geometría es trivial— sino
   **crear el segundo contexto WebGL**: memoria de GPU, compilación de shaders y
   armado del pipeline. Ese costo se paga una vez y **no lo evitan ni el render
   bajo demanda ni la pausa por visibilidad**, porque para pausar un contexto
   primero hay que crearlo.

   Va con **`rootMargin: '0px'` a propósito**, que es lo contrario de lo
   habitual: el hero mide `100vh`, así que la sección del cubo arranca ~20 px
   debajo del fold y cualquier margen de anticipación la haría intersectar **ya
   en la carga**, con lo cual no se diferiría nada. Con margen 0 el contexto se
   crea al scrollear, fuera del pico inicial —donde ya están la compilación del
   shader del mar y las fuentes—, y el margen de maniobra lo da el padding de la
   sección.

   Si el navegador no tiene `IntersectionObserver`, hidrata directo. Y si la
   hidratación falla, no es fatal: queda la grilla semántica.

2. **`cube.js` — pausar el loop.** El segundo observer, con `threshold 0.02`,
   sólo mantiene la bandera `visible`. El loop no hace nada si el cubo está fuera
   de pantalla, en modo grilla, o si la pestaña está oculta.

### Mediciones

Van en `docs/mediciones/`, **fechadas y con sus condiciones**, porque una
medición sin condiciones no se puede repetir ni comparar:

| Archivo | Qué mide | Estado |
|---|---|---|
| `luz-arco.md` | contraste del cubo contra su fondo a lo largo del arco del péndulo | cerrado: no había problema, y explica por qué la métrica engañaba |
| `rendimiento.md` | tiempo por cuadro de la página completa (escritorio, julio 2026) | en escritorio sobra margen; **móvil sin medir en dispositivo real** |

## Metadatos y descubribilidad

Que el sitio sea legible por máquinas es un **objetivo** del proyecto, no un
extra: es la misma razón por la que todo el contenido va en el HTML.

| Archivo | Qué hace | Se mantiene |
|---|---|---|
| `sitemap.xml` | lista todas las páginas indexables | `python tools/make-sitemap.py` |
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

`canonical`, `og:url` y `og:image` son **absolutas** en todas las páginas
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
