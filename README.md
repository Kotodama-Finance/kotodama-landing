# Kotodama Finance — página de entrada

Plataforma pública y gratuita de datos y análisis del sistema financiero
japonés. Este repo publica en GitHub Pages (kotodamafinance.com). La rama que
publica es `main`, y **se genera** — el sitio solo, sin estas notas—; ver
«Publicar» más abajo.

Sitio estático: sin backend, sin frameworks, sin build step. Se sirve tal cual.

## Estructura

```
index.html              home EN: todo el contenido y los enlaces, en el fuente
assets/css/styles.css   tokens en :root + estilos (compartido por todas las páginas)
assets/css/maelstrom.css la transición entre páginas, RESERVADA: no la carga nadie
assets/js/background.js océano WebGL de fondo
assets/js/cube.js       cubo de navegación (Three.js)
assets/js/main.js       orquestador: toggle, nav, visibilidad
assets/js/notes.js      buscador del archivo /notes/ (la segunda página con JS)
assets/fonts/           tipografías auto-hospedadas y subseteadas
assets/vendor/          Three.js vendoreado (sin CDN en runtime)
favicon.ico/.svg/-*.png iconos del sitio (generados, ver más abajo)
apple-touch-icon.png    icono para «añadir a inicio» en iOS
android-chrome-*.png    192/512 para Android/PWA — los enlaza el manifest
site.webmanifest        manifest mínimo (generado junto con los iconos)
sitemap.xml             generado por tools/make-sitemap.py
notes/search-index.json índice del buscador de /notes/ (generado por tools/make-notes.py)
robots.txt              todo abierto, incluidos los crawlers de IA
404.html                la sirve GitHub Pages ante cualquier ruta inexistente
og-image.png            tarjeta al compartir (generada)
tools/check-structure.py guarda estructural: verde siempre (ver más abajo)
tools/check-ready.py    guarda previa a publicar (hoy 2 esperado: capa 1 de seguros + andamiaje de notas en placeholders — historia en su docstring)
tools/make-favicon.py   genera los iconos a partir del subset de la marca
tools/make-sitemap.py   genera sitemap.xml Y el árbol de /sitemap/, de la misma lista (excluye los que declaran noindex, leído de la propia meta)
tools/make-notes.py     genera el feed de la portada, el listado de /notes/ y su índice — una pasada, tres salidas (mismo criterio noindex)
tools/make-og-image.py  genera og-image.png (sólo tipografía, sin navegador)
tools/make-deploy.py    genera el commit de publicación en main: el sitio solo
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
Hoy vive únicamente en `index.html`. Las páginas con JavaScript son DOS: la
portada (el cubo, con módulos y este mapa) y `/notes/` (su buscador,
`assets/js/notes.js` — script clásico, sin módulos, así que NO necesita
import map); **todas las demás** —las seis caras, las tres subpáginas de
Hajime, la sección de seguros, la nota de ejemplo, `/musubi/`, `/method/`,
`/sitemap/`, `/disclaimer/` y la 404— no cargan ningún script. Un import map **no se hereda
entre documentos**, así que una página nueva que quiera el cubo necesita **su
propia copia**, con la ruta corregida a su profundidad. El caso previsto es
`/ja/index.html`: un nivel abajo, o sea `../assets/vendor/three.module.js`.

## URLs

Esquema por **directorios**, no archivos sueltos. Cada página es un directorio
con su `index.html` adentro:

```
/                 index.html                 home EN
/musubi/          musubi/index.html          la idea que sostiene la plataforma
/sugao/           sugao/index.html           la persona detrás del proyecto
/method/          method/index.html          el método completo + las fuentes, una por una
/disclaimer/      disclaimer/index.html      el disclaimer completo (el único lugar)
/sitemap/         sitemap/index.html         el mapa del sitio (árbol generado; misma
                                             lista que sitemap.xml, para humanos)
/hajime/taichi/   hajime/taichi/index.html   línea macro de Hajime
/hajime/yorozu/   hajime/yorozu/index.html   línea sectorial de Hajime
/hajime/yugen/    hajime/yugen/index.html    línea de transparencia de Hajime
/hajime/yorozu/japan/seguros/                capa 1 de seguros japoneses (andamiaje,
                                             la primera ruta de CUATRO niveles;
                                             /hajime/yorozu/japan/ NO lleva página
                                             a propósito — da 404 y está bien)
/notes/           notes/index.html           el archivo de notas con buscador
                                             (noindex hasta la primera nota real)
/hajime/nota-ejemplo/                        nota-FIXTURE del generador: se borra
                                             con la primera nota real (noindex)
/ja/              (previsto)                 subárbol paralelo en japonés
```

**Los rótulos de vuelta siguen el ORIGEN, no un destino único**: las páginas que
se abren desde el cubo (las seis caras) vuelven al cubo — «Back to the Cube»,
con destino `/#cube-view`, el ancla del cubo mismo y no del título de la
sección—; las tres subpáginas de Hajime vuelven a `/hajime/` («Back to
Hajime»); las secciones de un sector vuelven a su subcara — la capa 1 de
seguros lleva «Back to Yorozu», destino `/hajime/yorozu/` (el criterio
extendido un nivel, 2026-08-07)—; y las demás (`/musubi/`, `/method/`,
`/sitemap/`, `/disclaimer/`, la 404) vuelven al inicio — «Back to the start»,
destino `/`. `/sitemap/` es el caso sin origen único —se llega desde el footer
de cualquier página— y usa el mismo rótulo que `/disclaimer/`, que ya era ese
caso.

`/method/` es el **desarrollo**; la sección `#method` de la portada queda como
**resumen** y la nav sigue apuntando ahí. **No hay `/sources/`**: la lista
taxativa de fuentes vive dentro de `/method/`, porque el criterio y su
aplicación no deben poder divergir.

GitHub Pages sirve `/musubi/` como `/musubi/index.html`, y redirige `/musubi`
(sin barra final) a `/musubi/` con un 301. Las URLs no llevan extensión.

`/musubi/` se llamaba `/naming/`. **No quedó redirección**: GitHub Pages sirve
archivos estáticos y no tiene reglas de reescritura, así que la ruta vieja
responde con la 404 del sitio. Fue aceptable porque el renombre ocurrió antes
de la publicación (la landing vieja sólo tenía la portada, así que `/naming/`
nunca estuvo publicada). **Desde la publicación (2026-08-06) la regla cambia**:
renombrar una ruta ya publicada exige dejar en su lugar un `index.html` con
`<link rel="canonical">` a la nueva y un `<meta http-equiv="refresh">`, que es
lo más parecido a un 301 que permite Pages.

El archivo `.nojekyll` desactiva el procesamiento con Jekyll: el sitio ya es
estático y no lo necesita. Además evita un problema silencioso — Jekyll ignora
todo path que empiece con `_`, así que sin ese archivo un directorio así
simplemente no se publicaría.

### El disclaimer: dos textos, dos reglas opuestas

Es la única duplicación deliberada de texto del sitio, y conviene entender por
qué antes de "arreglarla". (El rótulo japonés `免責事項` que encabezaba el corto
y el `<title>`/eyebrow de `/disclaimer/` **se retiró de la versión inglesa**:
era la traducción de «disclaimer», o sea japonés ornamental. Los glifos siguen
en el subset porque será el título real de la página legal de `/ja/`.)

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
| `tools/check-ready.py` | antes de publicar a `main` | instantánea | hoy `2` esperado — capa 1 de seguros en placeholders (2026-08-07); `0` cuando llegue su texto |

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
  metadatos únicos, URLs absolutas, cobertura del subset japonés, **el árbol de
  /sitemap/ al día** (idéntico al que `make-sitemap.py` generaría hoy),
  **ningún `href="#"` que haya perdido su placeholder**, **ningún placeholder
  nuevo** respecto de `tools/placeholders-baseline.json`, y **nada de
  castellano en lo que se publica**. Sale `0` si está bien, `1` si algo se
  rompió.

  **La guarda de castellano no busca en el repo, aísla la superficie
  publicable** —texto visible, `<title>`, atributos que ve un usuario o un
  crawler, strings de `main.js`/`cube.js`, el sitemap y el robots— y mira sólo
  ahí. Los comentarios de HTML/CSS/JS, `tools/`, los `.md` y `_ref/` quedan
  fuera a propósito: están en castellano por decisión y no se publican.

  **NO ES COMPLETA, y conviene saberlo**: detecta diacríticos y una lista de
  palabras función. Castellano sin acentos y sin esas palabras se le escapa —
  se le escapó `«no se pudo hidratar; se mantiene la grilla»`, que apareció
  revisando a mano los `console.*`. Cubre la reincidencia de lo conocido; **al
  agregar una página hay que leer su superficie además de correr esto.**
- **`check-ready.py`** — ¿puede publicarse? Sale `0` listo, **`2` falta trabajo
  previsto** (esperado, no es una regresión) y `1` si hay algo roto de verdad.

  El `2` cubre **una sola cosa: los placeholders sin redactar**. Hubo una
  segunda —la revisión legal del `免責事項`, detectada por una marca de borrador
  en el HTML— y **se retiró** cuando el autor decidió publicar el descargo sin
  revisión de un profesional legal japonés. El motivo y el marco legal que lo
  sostiene están en `CLAUDE.md`.

  De esa guarda conviene conservar la lección aunque la guarda ya no exista:
  **una marca así tiene que ser un token SIN ESPACIOS**. La primera versión usaba
  una frase, y una frase se parte en el salto de línea de un comentario HTML y
  deja de encontrarse — daba «revisado» con el borrador intacto, que es el falso
  verde exacto que la guarda venía a impedir.

Al redactar un placeholder el conteo baja: eso **no** falla, pero hay que fijar
el piso nuevo con `python tools/check-structure.py --actualizar-baseline`.

**Si un cambio rompe algo y no se puede arreglar en el momento**, revertir al
último commit verde en vez de dejar el árbol roto, y decir qué se revirtió y
por qué.

**Tags**: sólo en hitos, no cada tanto. Anotados, no ligeros — un hito lleva
fecha, autor y mensaje. **Y una vez empujado, un tag no se mueve**: es un
registro fechado del estado en ese commit, así que un mensaje que quedó viejo es
historia y no deriva. Reescribirlo lo convertiría en una copia peor de los
documentos vivos, y `--force` sobre un tag ya publicado rompe los clones ajenos.

| Tag | Qué marca |
|---|---|
| `v1-dark` | la versión navy + oro con el cubo en Three.js |
| `v1-content-complete` | **el sitio terminado de contenido**: cero placeholders, `check-ready` en 0 |
| `v1-published` | **la publicación** (2026-08-06) — en el commit FUENTE `6dc8214` de `redesign-trust` (el que pasó las guardas), no en `main`; el commit de `main` (`824fada`) lleva el hash cruzado |

`v1-content-complete` **es el punto al que hay que volver si algo se rompe en la
migración de DNS**, que es lo próximo que pasa. Por eso apunta al último estado
verificado en verde y no al commit donde se redactó el último placeholder
(`2115a4e`): ahí el contenido ya estaba completo, pero `check-structure` estaba
en rojo — la guarda del baseline se rompía justo al llegar a cero, y se arregló
en el commit siguiente. Un punto de restauración tiene que estar verde.

## Antes de publicar

Antes de publicar a `main` —que **ya no es un merge**: `main` se genera con
`tools/make-deploy.py`, ver «Publicar» más abajo—, correr:

```
python tools/check-ready.py
```

Tiene que terminar con `LISTO PARA PUBLICAR` y código de salida 0. Comprueba:

1. **Que no queden placeholders de redacción**, en **dos** familias. La obvia
   son los elementos con `class="todo"`. La otra son los `TODO` de `<title>` y
   de cualquier `content="…"`, que **no llevan clase porque no son elementos**.
   Un placeholder en producción es texto en castellano dirigido al autor
   apareciendo en un sitio en inglés.

   **Acá había un `grep -c 'class="todo"'` como equivalencia, y era falso**: se
   come la segunda familia entera. Durante un tiempo la guarda tampoco la
   contaba, y el sitio podía dar «LISTO PARA PUBLICAR» con seis descriptions que
   decían *«TODO: descripción de esta cara.»*. Si aparece otra clase de
   placeholder que no sea un elemento con clase, va agregada en
   `placeholders()`, no en un `grep` de este README.
2. **Que el subset japonés cubra todos los glifos del sitio** (ver abajo).
3. **Que el nav y el footer no hayan derivado** entre todas las páginas.

Hoy sale **2** y **es lo esperado** — desde el 2026-08-07 el andamiaje de la
capa 1 de seguros (`/hajime/yorozu/japan/seguros/`) tiene 25 placeholders a
propósito, esperando el texto del autor. El significado del código 2 alterna
entre esperado y regresión según si hay andamiaje deliberado en pie — ya
cambió CUATRO veces, y la historia completa vive en el docstring de
`check-ready.py`, que es el que hay que leer antes de interpretar una
corrida. La referencia estable: **el baseline de `check-structure` dice el
techo acordado** (hoy 25, todos en esa página); placeholders POR ENCIMA del
baseline son regresión — castellano dirigido al autor que se coló—, y `1`
sigue siendo estructura rota, siempre.

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

**Y el quinto elemento, desde la rama de deploy (2026-08-06): la guarda del
propio `make-deploy.py`**, que corre sola al generar `main` y es todo-o-nada
—si algo falla, no se commitea nada—. Verifica que el árbol publicado esté
**completo** (cada URL del sitemap con su página; cada referencia de los HTML,
el CSS y los JS resuelta adentro del árbol — sobre los bytes YA transformados:
lo verificado es lo publicado), que **no lleve notas** (por tipo —cero
`.md`/`.py`/`.json`— además de por lista), la **identidad en dos clases**
(cada blob no transformado, idéntico al del commit fuente; cada
`.html`/`.css`/`.js` publicado, igual a la transformación recomputada de su
blob fuente), que **la transformación no haya tocado nada más que
comentarios** (la guarda de contenido: cero comentarios en el artefacto por
`html.parser`, mismo stream de eventos, mismo texto visible, el chrome
idéntico entre páginas del artefacto, la meta de Search Console/import
map/gc-pixel/noindex vivos, tokens de CSS/JS intactos), y que **nadie haya
editado `main` a mano** desde el último deploy. El procedimiento completo del
día, en «Publicar», acá abajo.

**Desde el 2026-08-08 el deploy TRANSFORMA: elimina los comentarios de los
HTML, CSS y JS publicados** (los comentarios son notas de trabajo y no viajan
al dominio; el fuente no se toca — la decisión completa, en `CLAUDE.md`).
Consecuencia con regla propia: **lo servido ya NO es byte-idéntico al
fuente** — cualquier comparación de bytes servidos va contra el árbol de
`main`, no contra `redesign-trust`, y cualquier diagnóstico sobre el dominio
tiene que reproducir la transformación antes de concluir.

### Una trampa de CSS que ya mordió dos veces

Varias clases del sitio fijan `display` (`.btn`, `.status`, `.cube__stage`,
`.cube__toggle`). Una clase **le gana por especificidad** a la regla `[hidden]`
del navegador, así que un elemento marcado como oculto seguía viéndose. Hay una
regla `[hidden] { display: none !important; }` al principio de `styles.css` que
lo resuelve para toda la clase de bug. No borrarla.

## Publicar: `main` se genera, no se mergea

`main` publica **SOLO el sitio**. Las notas de trabajo —`CLAUDE.md`, este
README, `tools/`, `docs/`, los JSON de estado y `maelstrom.css`— viven en la
rama de desarrollo y **no llegan al dominio**: GitHub Pages publica la rama
entera, y un merge habría servido `kotodamafinance.com/CLAUDE.md`. La decisión
completa, con sus alternativas descartadas, está en `CLAUDE.md`; la lista
autoritativa de exclusión, en `NO_PUBLICABLES` de `tools/make-deploy.py`.

**`main` es una rama-artefacto, como `maintenance`: NADIE la edita a mano.**
Todo cambio va desarrollo → guardas → `make-deploy`. Si alguien commitea en
`main` directo, el próximo deploy lo detecta —compara el árbol de la punta
contra lo que regeneraría desde la `Fuente:` que ese commit declara— y frena
antes de pisar.

**La primera publicación salió el 2026-08-06** con este procedimiento, tal
como está escrito abajo: deploy `824fada` desde el fuente `6dc8214` (tag
`v1-published`), verificado en el dominio — rutas nuevas en 200, notas en
404, CNAME y HTTPS intactos, pixel disparando. Los seis pasos alcanzaron sin
improvisar nada.

### El día de publicar

Desde `redesign-trust`, con el árbol limpio:

1. **Las cuatro guardas en verde** (ver «Flujo de trabajo»; `check-ready`
   en `0`).
2. **Generar y verificar.** Corre la guarda del deploy y, si todo pasa, arma
   el commit en `main` **local** (con `--solo-verificar` sólo lista qué entra
   y qué queda afuera, sin commitear):

   ```bash
   python tools/make-deploy.py
   ```

3. **Verificar el artefacto en navegador, UNA vez** — la única corrida contra
   el árbol real de `main`. Materializarlo en un worktree:

   ```bash
   git worktree add _dev/main-check main
   ```

   Detener el servidor de desarrollo, servir **ese** árbol
   (`python -m http.server 8000 --directory _dev/main-check`) y correr
   `python tools/check-modes.py`. Al terminar, parar ese servidor y limpiar:

   ```bash
   git worktree remove _dev/main-check
   ```

4. **Push:**

   ```bash
   git push origin main
   ```

5. **El tag de publicación, en el commit FUENTE de `redesign-trust`** —el que
   pasó por las guardas—, no en `main`; el mensaje del commit de `main` ya
   lleva el hash cruzado (`Fuente:`). El nombre lo elige el autor en el
   momento (los hitos anteriores fueron `v1-dark` y `v1-content-complete`):

   ```bash
   git tag -a <nombre-del-tag> -m "Publicación del sitio" <hash-fuente>
   ```

   ```bash
   git push origin <nombre-del-tag>
   ```

6. **Después del push, comprobar EN EL DOMINIO que las notas no estén** — es
   la propiedad que motivó todo esto: `kotodamafinance.com/CLAUDE.md`,
   `/README.md` y `/tools/check-ready.py` tienen que dar **404**, y la
   portada tiene que cargar entera (cubo incluido). **Y que los comentarios
   tampoco**: el ver-código de la portada servida sin ningún `<!--` (salvo
   dentro de `<script>`/`<style>`, donde no hay), con la meta de Search
   Console intacta.

### Rollback: volver a un estado bueno ya publicado

Para el día del apuro: son **dos comandos**, y no hace falta checkout, revert
ni acordarse de nada más. `make-deploy` puede publicar desde CUALQUIER commit
sin tocar el árbol de trabajo — lee los blobs directo de la base de objetos:

```bash
python tools/make-deploy.py --fuente <commit-bueno>
```

```bash
git push origin main
```

- **¿Cuál es el commit bueno?** El fuente del último deploy sano. Cada commit
  de `main` lo declara en su mensaje —`git log main`, la línea
  `Fuente: <hash>`— y los tags de publicación apuntan a esos mismos commits
  en `redesign-trust`. `v1-content-complete` es el punto de restauración de
  la migración de DNS.
- **La historia no se reescribe**: el rollback es un commit NUEVO encima de
  `main`, sin force-push. Pages publica en un par de minutos.
- **Los avisos del rollback son esperables, no errores**: si el commit bueno
  es anterior a la creación de algo que hoy existe (un favicon, una entrada
  de la lista de exclusión), el script lo dice y sigue — el sitio de ese día
  se publica como era. Lo que sí frena siempre: `CNAME`/`.nojekyll`/
  `index.html`/`404.html` ausentes, notas de trabajo en el árbol, o
  referencias rotas. (Probado contra `v1-content-complete`.)
- Si lo que hace falta es **bajar el sitio**, eso no es un rollback: es la
  rama `maintenance` (sección siguiente).

## La rama `maintenance`: bajar el sitio para una obra grande

Un cartel para cuando haya que dejar el sitio fuera de línea a propósito. **No
reemplaza nada**: vive en una rama aparte y se activa cambiando de qué rama
publica GitHub Pages, así que ni el sitio ni `main` se tocan en ningún momento.

**Cubre el sitio entero con dos archivos.** `index.html` responde la raíz;
cualquier otra ruta —`/sugao/`, `/method/`, un enlace viejo— no existe en esa
rama, así que Pages sirve `404.html`, que es **el mismo archivo**. No hace falta
replicar las carpetas del sitio. La guarda comprueba que los dos sean el mismo blob:
si se separan, la portada diría una cosa y el resto otra.

### Activar

En GitHub: **Settings → Pages → Build and deployment → Branch**, elegir
`maintenance` / `(root)` y guardar. Tarda un par de minutos en reconstruir. Eso
es todo: la rama ya está en `origin`.

Si se regeneró desde la última vez, empujarla antes —`make-maintenance.py` sólo
escribe la rama local—:

```bash
git push origin maintenance
```

### Volver

Misma pantalla, elegir de nuevo la rama que publicaba —hoy **`main`**— y
guardar. No hay nada que revertir en el repo: la rama de mantenimiento queda
donde estaba, lista para la próxima.

> **El CNAME es lo único que puede romper el dominio.** La rama lo lleva,
> copiado del sitio, y **tiene que seguir llevándolo**: cuando Pages publica una
> rama sin `CNAME`, da de baja el dominio propio de la configuración. Volver a
> ponerlo obliga a reaprovisionar el certificado HTTPS, que puede tardar horas —
> justo cuando el sitio ya está caído. Por eso la rama tiene cuatro archivos y
> no dos, y por eso la guarda compara el CNAME contra el del sitio en vez de
> darlo por sentado. El cuarto es `.nojekyll`, para que Pages suba los archivos
> en vez de correr un build de Jekyll que no hace falta y puede fallar.

### La rama se GENERA, no se edita

```bash
python tools/make-maintenance.py              # construye en _dev/maintenance/
python tools/make-maintenance.py --publicar    # además, actualiza la rama
```

El script escribe la rama con plumbing: **no hace checkout ni mueve `HEAD`**, así
que se puede correr con el árbol de trabajo en cualquier estado. Editar los
archivos de la rama a mano no sirve — la próxima corrida los pisa. El texto, el
diseño y la paleta viven en el script; la paleta la **lee del `:root`** de
`styles.css`, como `make-og-image.py`.

**Y el HTML sale SIN comentarios (2026-08-08)**: el generador lo pasa por el
mismo `transformar()` de `make-deploy.py` — «cero comentarios en lo servido»
rige también en esta rama. Los comentarios viven en la plantilla del script,
que es el fuente.

Es un cartel, no una página: **una sola petición HTTP**. El CSS, el favicon y
las fuentes van embebidos, no hay JavaScript y no hay WebGL. Con archivos
aparte el titular aparecería primero en una fuente del sistema y saltaría al
llegar la buena, que en una página de cinco líneas es lo único que se ve.

### Verificarla antes de activarla

```bash
python tools/check-maintenance.py
```

**No entra en el flujo de cuatro guardas de cada commit**, a propósito: mira una
rama que no cambia entre commits, así que ahí sólo sería ruido. Se corre al
tocar la rama y **antes de activarla**, que es cuando importa. Comprueba los dos
archivos idénticos, el CNAME, que no haya ninguna referencia externa —en esa
rama cualquier `<link>` o `<script>` es un 404 seguro—, el `noindex`, que el
mailto sea el mismo del sitio, que no viaje ningún comentario (ni `<!--` ni
`/*` en el CSS inline, que el stripper deja crudo a propósito), y la cobertura
de las fuentes embebidas contra su `cmap`.

No compara bytes contra el generador y no es por comodidad: **el codificador
woff2 no es determinista** —tres corridas del mismo comando, tres `sha1`
distintos, también con `PYTHONHASHSEED=0`—, así que esa guarda habría estado en
rojo desde el primer día. Compara el HTML con los base64 elididos, que sí es
estable, y las fuentes por su `cmap`.

### El japonés: Zen Kaku va embebido, y el camino hasta ahí importa

**Hoy el cartel lleva Zen Kaku embebido**: los siete glifos —保守作業中 y 言霊—
salen de un micro-subset de 1,46 KB (1,94 KB en base64) incrustado en el HTML.
Verificado con `CSS.getPlatformFontsForNode`: los cinco del titular y los dos
del logo se dibujan con **Zen Kaku Gothic New Medium**, una sola cara.

Se embebe porque **ésta es la página que se muestra cuando algo salió mal**, y
ahí que se vea distinta en cada máquina es lo peor que puede pasar. La pila del
sistema funcionaba —medido: los cinco glifos en Yu Gothic Medium—, pero costaba
consistencia y dejaba afuera Linux pelado sin fuentes CJK, donde el titular era
tofu.

Los tres glifos que faltaban —守 (U+5B88), 作 (U+4F5C), 中 (U+4E2D)— se
agregaron al subset **del sitio**, aunque ninguna página los use, porque este
generador sólo puede leer archivos del repo: si leyera la TTF de origen, que a
propósito no está versionada, la rama dejaría de poder regenerarse en otra
máquina. Cuestan 0,3 KB y la fórmula de derivación los preserva sola.

**Lo que conviene no perder es por qué NO se copió el `woff2` y ya.** Era la
opción obvia y es la peor, porque **no falla como uno espera**. Medido con
`CSS.getPlatformFontsForNode`:

| Pila declarada | Qué dibuja de verdad |
|---|---|
| `'Zen Kaku', sans-serif` | 2 glifos Zen Kaku + **3 Microsoft YaHei** |
| `'Hiragino', 'Yu Gothic', sans-serif` | 5 glifos Yu Gothic Medium |
| `sans-serif` **con** `lang="ja"` | 5 glifos Noto Sans JP |
| `sans-serif` **sin** `lang` | 5 glifos Microsoft YaHei |

El fallback de fuentes es **por glifo**, así que el titular se dibuja entero y
parece correcto: no hay tofu que delate nada. Lo que habría salido es un titular
en dos tipografías, **una de ellas china**, en la rama que ninguna guarda del
sitio mira.

Dos cosas quedan de ahí aunque el problema ya esté resuelto. La primera:
**`lang="ja"` decide si el navegador cae en una fuente japonesa o en una china**
(última fila de la tabla), así que sigue puesto en los dos `<span>` japoneses y
no es decoración semántica — es la red por si el `@font-face` no cargara. La
segunda: `JA_EMBEBIDO` en el generador **no adivina**. Si falta un glifo aborta
nombrándolo, justamente porque la versión rota se ve bien.

Y el subset de esta rama **no tiene el problema de desactualizarse** que sí tiene
el del sitio: su texto es fijo y no va a crecer. El del sitio se agranda cada vez
que se escribe una página; un conjunto de entrada cerrado no deriva. Ésa fue la
razón para no dejarlo en la pila del sistema: el argumento de «un subset propio
genera deuda» no aplicaba.

### El costo asumido del `noindex`

La página lleva `noindex` porque no se quiere el estado de mantenimiento en el
índice de nadie. El costo: un `noindex` sostenido hace que un buscador deje caer
las URLs, y volver a indexarlas lleva tiempo. Se aceptó mientras el sitio no
estaba publicado; **desde la publicación (2026-08-06) el sitio está
indexándose, así que el costo es real**: si esta rama tiene que quedar arriba,
que sea lo menos posible — lo canónico ahí es un 503, y GitHub Pages no puede
servirlo.

## Tipografías: el subset es un paso obligatorio

Las tipografías están auto-hospedadas y subseteadas. El subset de **Zen Kaku
Gothic New** contiene exactamente los glifos japoneses que aparecen en el sitio
(más los reservados para `/ja/`), y nada más — decenas de KB en vez de los
2,3 MB de la TTF completa. El número exacto se lee del archivo, no de acá:
un tamaño escrito en un `.md` caduca con la próxima regeneración, y éste ya
caducó una vez (decía «~13 KB» cuando el subset llevaba meses en ~30).

**Cada vez que se agrega texto japonés nuevo hay que regenerar el subset.** Si
no, ese carácter se renderiza con una fuente del sistema: no desaparece, sólo
desentona, y es fácil que pase inadvertido.

Regenerar (requiere `pip install fonttools brotli`) con las TTF de origen del
repo `google/fonts` (`ofl/zenkakugothicnew`). **Esas TTF no están en este repo
ni tienen por qué estar**: pesan ~2,2 MB cada una, no se sirven, y sólo hacen
falta el día que se regenera. Hay que bajarlas en ese momento — y de un subset
**no** se pueden sacar glifos que no tiene, así que no hay atajo.

**La fórmula de derivación y los comandos exactos viven en UN solo lugar: el
comentario de `@font-face` en `assets/css/styles.css`**, junto al código que
sirve los archivos. Este README no los repite, y es una corrección: acá había
una segunda copia y derivó en tres puntos a la vez — decía que la cadena `$JA`
«está listada» en ese comentario (dejó de listarse, deliberadamente), daba la
fórmula sin el tercer término (el japonés del cartel de mantenimiento, que la
versión vigente sí incluye) y daba otro comando (`--unicodes=<conjunto>` a
secas, cuando el que reproduce el archivo servido va con `--text` más los
rangos fijos). Dos copias de un método derivan igual que dos copias de un
número, y la copia vieja se lee como si fuera la vigente.

Lo que sí es de acá: el conjunto **se deriva, no se transcribe** (la unión con
el subset actual preserva los glifos reservados para `/ja/`, que regenerar
desde el texto de hoy borraría), y la extracción del HTML usa **la misma
función que la guarda** (`texto_visible` + `JAPONES` en `tools/_guardas.py`),
para que no haya dos criterios de qué es «japonés del sitio».

**Verificar en las dos direcciones después de regenerar**: que todo el japonés
del HTML quede cubierto, y que **no se haya caído ningún código del subset
anterior**. Lo segundo es lo que atrapa el borrado silencioso de los reservados.

El latín básico va incluido para tramos mixtos como «e-Stat / 総務省».

### Los dos comandos no son iguales, y no hay que unificarlos

El japonés de arriba va **sin** `--layout-features`; el latino de abajo va
**con** `--layout-features='*'`. Parece una inconsistencia y no lo es: está
medido en las dos direcciones, y **cada uno reproduce su archivo commiteado sólo
con su propia forma**.

La medición que fijó la regla (fechada por sus propios números: el subset
japonés tenía entonces 163 glifos; hoy es más grande y la regla se re-verifica
en cada regeneración comparando features contra el archivo anterior):

| | sin el flag | con el flag |
|---|---|---|
| **Zen Kaku** | 163 glifos · 13,2 KB — **reproduce** | 258 glifos · 16,0 KB · suma `aalt fwid ordn sups` |
| **Inter / Cormorant** | −35 %, se pierden 374 y 503 glifos | **reproduce** |

Ponerle el flag al japonés o quitárselo al latino produce, en cada caso, un
archivo distinto del que se sirve. La regla no es «usar el flag»: es **que el
comando escrito reproduzca el archivo commiteado**, y eso se comprueba
regenerando y comparando glifos y features, no de memoria.

```
pyftsubset Inter[opsz,wght].ttf \
  --output-file=assets/fonts/inter-latin.woff2 --flavor=woff2 \
  --layout-features='*' \
  --unicodes=U+0020-007F,U+00A0-00FF,U+016B,U+2010-2027,U+2030-2044,U+2190-2193,U+2212

pyftsubset CormorantGaramond[wght].ttf \
  --output-file=assets/fonts/cormorant-garamond-latin.woff2 --flavor=woff2 \
  --layout-features='*' \
  --unicodes=U+0020-007F,U+00A0-00FF,U+016B,U+2010-2027,U+2030-2044,U+2190-2193,U+2212

pyftsubset CormorantGaramond-Italic[wght].ttf \
  --output-file=assets/fonts/cormorant-garamond-latin-italic.woff2 --flavor=woff2 \
  --layout-features='*' \
  --unicodes=U+0020-007F,U+00A0-00FF,U+016B,U+2010-2027,U+2030-2044,U+2190-2193,U+2212
```

**Inter y Cormorant son variables y hay que conservar los ejes**: Inter lleva
`[opsz, wght]` y `make-og-image.py` fija el peso por eje, así que perderlos
cambiaría la tarjeta sin que nada avise. `pyftsubset` los conserva; verificarlo
igual después de regenerar.

### Optimización disponible, sin hacer: ~79 KB en las fuentes latinas

Los subsets latinos llevan features de OpenType que **el sitio no usa**: `smcp`,
`onum`, `dlig`, `ss01`…, y con ellas 374 glifos de Inter y 503 de Cormorant.
Verificado: **cero** `font-feature-settings`, **cero** `font-variant`, **cero**
`small-caps` en todo el CSS y el HTML.

Quitarlas —regenerando **sin** `--layout-features='*'`— baja las tres fuentes de
**198 KB a 119 KB**, o sea **~79 KB por carga**:

| | hoy | sin features |
|---|---|---|
| `inter-latin.woff2` | 93,0 KB | 60,5 KB |
| `cormorant-garamond-latin.woff2` | 60,5 KB | 28,7 KB |
| `cormorant-garamond-latin-italic.woff2` | 45,1 KB | 30,0 KB |

**No se hizo, y la razón importa más que el número**: esas features son
exactamente lo que alguien usa después sin acordarse de que se sacaron, y con
el sitio ya publicado (2026-08-06) el fallo silencioso sería en producción.
`liga`, `kern` y `calt` no están en juego — sobreviven al subset por defecto y
son las que el navegador aplica solo.

**La condición para revisarlo**: si algún día el CSS usa `font-feature-settings`,
`font-variant` o `small-caps`, esta optimización deja de estar disponible **y**
hay que regenerar comprobando que la feature concreta sobreviva.

**Los paréntesis de ancho completo son la trampa de esta lista.** `U+FF08` y
`U+FF09` son japoneses y **no** entran por `U+0020-007F`: ese rango trae `(` y
`)` de ASCII, que son otros caracteres y se ven mal junto a un kanji. Al pasar
el footer a `日本語（近日公開）` faltaban **tres** glifos, no uno — `近` y los
dos paréntesis—, y son los paréntesis los que no se ven venir.

**Más seguro que reescribir `$JA` a mano**: derivar el conjunto nuevo del viejo.
Se lee la `cmap` del subset actual, se le suman los códigos que falten y se
subsetea a esa unión. Retranscribir cincuenta y pico de kanji para agregar uno
es la forma más fácil de perder otro — y perderlo es silencioso.

**Y la `og-image` va a protestar después de regenerar**: el subset de peso 500
es una de sus entradas, así que la guarda avisa aunque la tarjeta sólo use 言霊
y el PNG salga byte a byte idéntico (verificado). Se arregla con
`python tools/make-og-image.py`. No sacar la fuente del lock por esto: un cambio
de fuente **sí** puede mover la tarjeta, y el costo de la falsa alarma es un
comando.

**Verificar contra la tabla `cmap` de la fuente**, que es la única fuente de
verdad sobre qué glifos contiene:

```
python tools/check-ready.py
```

**No usar `document.fonts.check()` para esto.** Informa si la fuente está
cargada, no si contiene el glifo: devuelve `true` para caracteres que la fuente
no puede dibujar. Ya dio un falso positivo con 免責事項.

### El subset LATINO también se queda corto, y ahí no hay guarda

La verificación automática cubre el subset japonés. **El latino no lo mira
nadie**, y tiene el mismo problema: `Yūgen` en `/hajime/` trae **ū (U+016B)**,
que no entraba en ninguno de los rangos declarados. Un carácter latino en una
fuente latina se da por sentado, y ahí está la trampa. **Al escribir romaji con
macrón —ō, ū— verificar contra la `cmap` antes de publicar**, igual que con el
japonés.

Y ahí salió la divergencia que corrige la sección «Los dos comandos no son
iguales»: **el comando latino que estaba escrito no reproducía los archivos
commiteados**, porque le faltaba `--layout-features='*'`. El japonés sí
reproducía el suyo — y le habría roto el flag. Por eso son distintos.

## Iconos (favicon)

El juego completo **se genera**, no se edita a mano — ocho archivos:
`favicon.ico` (16/32/48 px), `favicon.svg`, `favicon-16x16.png` y
`favicon-32x32.png` (sueltos, sin `<link>`), `apple-touch-icon.png` (180),
`android-chrome-192x192.png` y `-512x512.png` (sin `<link>`: los referencia
`site.webmanifest`), y el propio `site.webmanifest`:

```
python tools/make-favicon.py            # regenera los ocho
python tools/make-favicon.py --strip    # además, la tira de comparación en _dev/
```

Salen del **mismo subset de la marca** (Zen Kaku peso 500), así que el icono es
literalmente la misma letra 言 que el logo del nav, en oro sobre navy **sólido**
— transparente, el kanji dorado desaparece sobre la barra clara de un navegador
en modo claro. El SVG lleva el glifo como `<path>` y no como `<text>`: un
favicon no carga webfonts.

**El 16px lleva un tratamiento propio, y salió de medir**: con el render normal
los trazos de 言 se embarraban (el punto se fundía con el primer trazo). Lleva
más relleno, un enfoque tras la reducción y un tope por canal al oro para que
el enfoque no lave el trazo a blanco. El detalle y los números están en el
docstring de `dibujar_kanji` en el script.

Los colores (`--c-navy`, `--c-gold`) están **copiados** en el script, porque un
icono se renderiza aislado y no ve el CSS. Es la misma excepción que el shader
del mar: si cambia la paleta, hay que volver a correr el script.

El `favicon.ico` existe aunque haya `<link>`: el navegador pide `/favicon.ico`
igual, y sin el archivo cada carga deja un 404 en la consola.

Las cuatro etiquetas `<link>` (ico, svg, apple-touch, manifest) están
duplicadas en todas las páginas, y `check-structure` verifica que el bloque
sea idéntico carácter por carácter — el mismo trato que el nav y el footer.

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
cada `resize()`**, nunca fija. **Anisotrópico desde 2026-08-04** — reemplaza a
la esfera envolvente completa:

```
S           = CELL + CUBIE/2 ≈ 1.489            // media arista del cuerpo 3×3
CUBE_RADIUS = √3 · S ≈ 2.579                    // sólo la horizontal lo usa
FIT_MARGIN  = 1.06
d_vertical   = FIT_MARGIN · S · (√2 / tan(halfV) + 1)
d_horizontal = FIT_MARGIN · CUBE_RADIUS / sin(halfH)
camera.z     = max(d_vertical, d_horizontal)
```

**La clave es que el cubo no tiene roll**: rota sólo en `rx` y `ry`
(`rotation.z` es siempre 0, order `'YXZ'`), y como `ry` no cambia la coordenada
vertical, la altura máxima alcanzable es **√2·S** —una arista arriba, `rx≈45°`—
y el vértice arriba (√3·S) **es inalcanzable**. La esfera completa pagaba ~8 %
de distancia por esa pose imposible; a 720×620 la cámara pasó de `z≈13.15` a
`z≈12.08` y el cubo dibujado creció de 442 a 483 px de alto.

Tres detalles que importan:

- **La vertical va con tangente y la horizontal con seno, y no es un error.**
  La regla «con seno, no tangente» era de la esfera; la vertical ahora acota un
  punto concreto (la arista más alta, que queda a radio S del eje y su peor
  azimut la acerca S a la cámara — de ahí el «+ 1»), y para un punto la
  tangente es exacta. La horizontal sigue siendo un radio de revolución (`ry`
  gira libre), y ahí el seno sigue siendo el correcto.
- **La garantía cubre TODAS las rotaciones alcanzables** — péndulo, snap
  (`rx=±90`) y arrastre manual, que no está acotado. **No asume la amplitud del
  péndulo**: cambiar `PEND_AMP` no la invalida. Lo único que la invalida es
  introducir roll; ese día vuelve la esfera, `√3·S / sin(min(halfV, halfH))`.
- **Manda la condición más exigente de las dos.** En apaisado la vertical; en
  un escenario más alto que ancho, la horizontal — que sigue siendo la variable
  sin medir en móvil.

Verificado con barrido de 360 poses (`rx` −8…180 más −90, el snap de Kizuna,
× `ry` cada 15°): ninguna recorta, margen mínimo **17 px** exactamente en el
peor caso teórico (`rx` 44–45°). Detalle en `docs/mediciones/encuadre.md`;
el guión, en `docs/mediciones/barrido-encuadre.py`.

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

   Va con **`rootMargin: '0px 0px -1px 0px'`** — margen NEGATIVO abajo, y el
   signo es la parte que importa. El hero mide **exactamente** `100vh`, así que
   la sección del cubo **toca el fold ya en la carga**, y para el observer dos
   rects que comparten el borde **intersecan**: con margen `0px` el contexto se
   creaba en la carga y el diferimiento no difería nada (medido: el canvas
   existía antes de scrollear; la versión anterior de este párrafo decía «~20 px
   debajo del fold» y ya no era cierto). El `-1px` encoge el viewport observado
   lo justo para que tocar el borde no cuente, y el contexto se crea recién al
   scrollear, fuera del pico inicial —donde ya están la compilación del shader
   del mar y las fuentes—. Un `rootMargin` positivo «generoso» desactiva la
   optimización entera.

   **El LAYOUT del modo 3D no espera a la hidratación**: `main.js` lo reserva en
   la carga (`setView('3d')` — escenario vacío con su alto de CSS, toggle
   visible, grilla recortada, ayuda de 3D) para que la altura de la página sea
   estable desde el primer layout. Sin la reserva, el escenario aparecía recién
   al resolver el import y metía ~406 px de alto arriba de `#about`, `#method` y
   `#footer` **después** de que el ancla aterrizara: los destinos de la nav
   quedaban corridos exactamente eso. `check-modes` verifica la estabilidad.
   Si la hidratación falla, el `catch` revierte a la grilla y esconde el toggle.

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
| `encuadre.md` | el encuadre anisotrópico: barrido de 360 poses sin recorte y el efecto en la portada | cerrado: margen mínimo 17 px en el peor caso teórico (rx≈45°) |

## Metadatos y descubribilidad

Que el sitio sea legible por máquinas es un **objetivo** del proyecto, no un
extra: es la misma razón por la que todo el contenido va en el HTML.

| Archivo | Qué hace | Se mantiene |
|---|---|---|
| `sitemap.xml` | lista todas las páginas indexables | `python tools/make-sitemap.py` |
| `/sitemap/` | la misma lista, para humanos — la página del mapa del sitio | el mismo comando (regenera su árbol) |
| `robots.txt` | abre todo y apunta al sitemap | a mano (casi nunca cambia) |
| `og-image.png` | la tarjeta al compartir un enlace | `python tools/make-og-image.py` |
| `404.html` | GitHub Pages la sirve ante cualquier ruta inexistente | a mano |
| feed de notas (portada) + listado de `/notes/` + `notes/search-index.json` | las tres salidas del sistema de notas, de la misma lista | `python tools/make-notes.py` (una pasada; hoy vacíos: cero notas publicables) |

**El sitemap se genera, no se escribe.** Es una lista duplicada —las mismas URLs
que ya están en el sistema de archivos— y la duplicación acá no hace falta ni
vigilarla: se deriva. Al agregar una página, correr el script. Si alguien se
olvida, `check-structure.py` lo caza, porque verifica que toda página publicable
esté listada.

**La página `/sitemap/` es la misma lista, para humanos** (2026-08-07 — nació
como bloque en el footer de todas las páginas y el autor lo revirtió el mismo
día: demasiado footer; el footer conserva sólo el enlace «Site map» en su
línea de abajo, vigilado por la identidad del footer). La misma corrida de
`make-sitemap.py` escribe el árbol entre los marcadores de esa página: dos
secciones con jerarquía visual (The Site primero: Home, Musubi, Method, Site
map, Disclaimer; The Cube después: las seis caras en el orden de la grilla,
con las subpáginas anidadas en el orden de las tarjetas de su padre, sin tope
de profundidad). Todo se deriva: las
URLs son el mismo conjunto que el sitemap (la 404 y las `noindex` quedan
afuera), los nombres salen del `face-page__romaji` con que cada página se
presenta en su h1, y lo único no derivable —el orden de las páginas de nivel
superior que no son caras— vive en `ORDEN_SITIO` (`tools/_guardas.py`) con
guarda: una página sin lugar ABORTA la generación nombrándola, sin escribir
nada. Las **notas** no entran al mapa — las resume la página de archivo `/notes/`,
que se sumará a `ORDEN_SITIO` al estrenarse—: cada nota se declara con
`<meta name="kotodama-type" content="note">` en su propio HTML, desde la
primera. **El sistema de notas ya existe completo y sin deployar**
(2026-08-07: contrato de metadatos, `make-notes.py` con sus tres salidas, y
el buscador de `/notes/`) — el detalle y el pase de estreno, en CLAUDE.md.
Que el árbol no quede **viejo** lo vigila la sección «Mapa del sitio
en el footer» de `check-structure.py`, comparando contra lo que el generador
escribiría hoy; los tres artefactos de notas tienen su sección gemela
(«Notas»), comparada contra `make-notes.py` por la misma vía.

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

**El lock vigila las entradas de la imagen, no el texto que la describe.** Son
dos cosas distintas y el hueco ya mordió: `og:image:alt` siguió diciendo «El
cubo de seis caras» mucho después de que la tarjeta dejara de llevar el cubo —y
encima en castellano, en un sitio en inglés—, porque un alt no es una entrada de
la composición y ninguna guarda lo mira. Al cambiar **qué muestra** la tarjeta,
el alt de las diez páginas se cambia a mano.

Y la bajada, `LINEA`, es **el titular del hero literal**, no un texto aparte: si
se redacta el hero, hay que regenerar. La primera versión de este README no lo
decía y la tarjeta sobrevivió un reemplazo de hero entero anunciando la frase
vieja.

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
  contexto WebGL no arranca. También queda sin efecto el folio de entrada, que
  aparece de una.

- **Entrar a una cara es una navegación normal: corte seco, sin fundido.** Hubo
  una transición entre documentos —el «maelstrom», hecha sólo con
  `@view-transition`— y **está reservada, no borrada**: vive entera en
  `assets/css/maelstrom.css`, que **no se carga desde ninguna página**. Se
  apartó antes del lanzamiento por decisión del autor.

  No puede ir detrás de un flag: es una transición **entre documentos**, así que
  la regla tiene que estar en las dos páginas, y **todas menos la portada no
  cargan ningún JavaScript**. Por eso se apartó en un archivo. El encabezado de ese
  archivo explica cómo reactivarla, qué valores ya están calibrados y un bug
  conocido de la variante táctil.

  **Que siga apartada lo vigila `check-modes`**, en la portada y en una
  subpágina. No lee el archivo: le pregunta al navegador qué reglas están en
  efecto, así que ve por igual un `<link>` a `maelstrom.css`, un `@import`, las
  reglas pegadas de vuelta en `styles.css`, un `<style>` inline y una hoja
  adoptada por JS. **Al reactivarla hay que sacar esa comprobación**, que va a
  dar rojo — y eso es lo que se busca: que volver no pueda pasar en silencio.

  **Si aparece corriendo, sospechar primero de una copia vieja de `styles.css`
  en el navegador.** El maelstrom vivía dentro de `styles.css` hasta `af7c726`,
  así que cualquier copia anterior trae las seis reglas. **El fingerprint es el
  conteo de `view-transition` en el texto que baja: 9 el viejo, 0 el vigente.**
  No usar el tamaño como referencia: el del vigente cambia con cada edición del
  CSS y con el final de línea (CRLF del checkout contra LF del blob), y ya
  caducó una vez a las horas de tabulado. Un `Ctrl+Shift+R` no descarta la
  copia vieja —no toca los *Local Overrides* de DevTools—; el detalle y la
  comprobación que separa el DOM de la red, en `CLAUDE.md`.

- **El bloque de estado + botón bajo el cubo es un folio que se despliega.**
  Arranca con altura cero y se abre animado al seleccionar una cara; se cierra al
  arrastrar. No empuja nada visible porque está debajo del cubo. Verlo en detalle
  en `CLAUDE.md`.
