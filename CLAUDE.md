# CLAUDE.md — Kotodama Finance

Contexto permanente del proyecto. Sobrevive a la compactación y al reinicio de
sesión. Si algo de acá contradice lo que parece razonable a primera vista, gana
esto: cada punto está donde está porque ya se probó lo contrario y falló.

Complementa al `README.md`, que documenta el sitio para cualquiera. Este archivo
documenta **las decisiones y su porqué**, que es lo que se pierde al compactar.

---

# Compact instructions

Al compactar, preservar siempre:

1. **Las decisiones cerradas y su motivo** (sección siguiente). El motivo importa
   más que la decisión: sin él, alguien las "arregla" y reintroduce el bug.
2. **El estado de los cabos abiertos**, con lo que ya se midió de cada uno.
3. **El flujo de guardas antes de commitear**, y que ninguna se saltea.
4. **Los hallazgos de método**: qué métricas engañaron y por qué. Están al final.

Se puede descartar: el detalle de cómo se llegó a cada número, los intentos
fallidos ya corregidos, y las capturas intermedias.

---

## Estado

- Rama de trabajo: **`redesign-trust`**. `rebuild-static` está congelada.
- **`main` no se toca**: publica kotodamafinance.com y todavía sirve la landing
  vieja. Nada de esto está publicado.
- Tag `v1-dark` = versión navy+oro con el cubo Three.js, con registro visual en
  `docs/v1-dark/`.
- El sitio es estático: sin backend, sin frameworks, sin build step.
- Último cierre: **2026-08-03**, en `fd7ee89`. **Árbol limpio y todo pusheado**,
  con `check-structure`, `check-modes` y `check-pendulum` en verde.
  `check-ready` sigue en `2` por la redacción, que es lo esperado.
- La redacción va por la mitad: el hero, `/sugao/`, `/disclaimer/`, `/musubi/`
  y el `免責事項` ya tienen texto definitivo. Quedan **41 placeholders en 8
  páginas**, y **12 de ellos son `/method/`**.
- **No queda ningún pendiente técnico.** Los tres que había se cerraron el
  2026-08-04.

### AL RETOMAR, EMPEZAR ACÁ

**Levantar el servidor en `:8000` y correr `python tools/check-structure.py`
—tiene que dar verde—.** Si da rojo, eso es lo primero: algo cambió fuera de
sesión.

**Después no hay tarea mía esperando.** Lo único que queda es la redacción, que
se hace fuera de Code, y la revisión legal del `免責事項`, que es externa. El
resto está congelado por decisión del autor o depende de `/ja/`.

Si aparece trabajo, el candidato natural es **`/method/`**: concentra 12 de los
41 placeholders y es la última página que sigue siendo andamiaje puro. Al
redactarla hay que aplicar además las dos notas de fuentes provisorias.

---

## Decisiones cerradas — no rediscutir

### Los seis nombres de las caras
`肇 Hajime` · `素顔 Sugao` · `渡世 Tosei` · `家紋 Kamon` · `鳥居 Torii` ·
`絆 Kizuna`. **Cerrados por el autor.** No se traducen, no se reinterpretan, no
se proponen alternativas. Su kanji, romaji, gloss, dominio y estado vienen del
archivo de referencia y se copian literalmente.

### `[hidden] { display: none !important; }`
Está al principio de `styles.css` y **no se borra**. Varias clases del sitio
fijan `display` (`.btn`, `.status`, `.cube__stage`, `.cube__toggle`), y una
clase le gana por especificidad a la regla `[hidden]` del navegador: el elemento
seguía visible pese a estar marcado como oculto. Rompió el toggle del cubo una
vez y el botón de entrada otra. Se arregla para toda la clase de bug, no caso
por caso.

**Rompería `hidden="until-found"`** si algún día se usa. Para excluirlo:
`[hidden]:not([hidden="until-found"]) { display: none !important; }`.

### Romaji: Inter en el cubo, Cormorant en el resto
**No es una inconsistencia, son medios distintos.** En la grilla y las páginas
es texto del DOM a ~1.05rem, plano y de frente: Cormorant funciona y es la voz
de marca. En el cubo es una textura horneada a ~12px de altura de mayúscula, con
relieve grabado y escorzo — ahí Cormorant se deshace (medido a tamaño real: el
romaji de las caras laterales era ilegible). Inter tiene asta uniforme y x-height
alta, que es lo que aguanta ese tamaño.

Además va **confinado al cubie inferior central**: las juntas caen a 1/3 y 2/3 y
ocultan ~21px de la textura. Un kanji grande absorbe el corte; el romaji no —
una junta le borraría un asta entera.

### Péndulo en rx; herencia de dirección sólo en ry
`rx` no gira libre: oscila (centro 18°, amplitud 20°). Con rx libre el cubo daba
vueltas completas y el romaji aparecía invertido — un kanji dado vuelta se lee
como forma, texto latino dado vuelta se lee como error.

La **fase avanza siempre** y la velocidad objetivo sigue una posición ideal, sin
ramas, clamps ni reinicios. Una versión anterior reseteaba la fase al llegar al
límite y el péndulo quedaba con media excursión: reiniciar el movimiento en un
punto es exactamente lo que hay que evitar.

**La herencia de dirección quedó sólo en `ry`.** En `rx` manda la fase del
péndulo; un signo heredado del último tiro pelearía contra la oscilación.

Consecuencia asumida: `鳥居` y `絆` (arriba y abajo) no se muestran solas en
reposo. Se llega por arrastre o por la grilla.

### Encuadre de cámara por esfera envolvente
`d = R · margen / sin(fov/2)`, **con seno, no tangente**. La esfera envolvente
del cubo tiene radio `√3·(CELL + CUBIE/2) ≈ 2.58`: la diagonal del cuerpo mide
1.73 veces el lado, así que al girar el cubo "crece" mucho más allá de su cara.
Con una distancia fija se recortaba en toda rotación con un vértice cerca de la
vertical. Se recalcula en cada `resize`, así que es inmune a cambios de tamaño.
Es una **garantía**, no un ajuste: si la esfera entra, ninguna rotación se sale.

**Manda el semiángulo más chico**, `min(halfV, halfH)`, no la vertical siempre:
en un escenario apaisado gana la vertical, pero en uno más alto que ancho gana la
horizontal y la cámara tiene que alejarse más. Es la misma variable que queda sin
medir en móvil, donde el escenario cambia de proporción.

### Los números del cubo se leen del código, y se tabulan en UN solo lugar

Constantes de geometría, luces, material, colores y física **viven en
`assets/js/cube.js` y en el `:root` de `styles.css`**. Ésa es la única fuente de
verdad. El README los tabula en «El cubo: parámetros vigentes» para poder
consultarlos sin leer el fuente; **ningún otro documento los repite**, por la
misma razón por la que el `免責事項` completo vive en un solo lugar: dos copias de
un número derivan, y la copia vieja se lee como si fuera la actual.

Ya pasó. **`docs/v1-dark/README.md` daba `hemi 2.2 · key 1.8 · rim 0.4 · back
0.8` y fondo de sección `#020509`**, que son los valores del tag y no los de hoy
(`hemi 3.5 · key 2.9 · rim 0.65 · back 1.3` sobre `--c-surface-cube` = `#05111d`;
las intensidades subieron justamente al aclarar ese fondo). Ahora ese archivo
dice en su encabezado que es histórico. **Al leer un `.md` con números del cubo,
la pregunta es siempre de cuándo son.**

### El import map vive en `index.html` y no se hereda

`cube.js` importa `three` como especificador desnudo; quien lo resuelve es el
import map de `index.html`. **No se comparte entre documentos**: una página nueva
que monte el cubo necesita su propia copia, con la ruta relativa corregida a su
profundidad (`/ja/index.html` necesitaría `../assets/vendor/three.module.js`).
Hoy es la única página publicable con JavaScript — las otras diez no cargan
ningún script—, así que agregar una página **no** obliga a tocarlo salvo que esa
página quiera el cubo. Detalle completo en el README, sección «El import map».

### `snap` es el movimiento; `parked` es el estado en que queda

Seleccionar una cara **detiene el cubo indefinidamente**, y eso es deliberado:
`snapTo()` pone `parked = true`, y mientras esté puesto la velocidad objetivo de
los dos ejes es 0. **No vuelve a arrancar solo** cuando termina el `hold`. El
único que lo revive es un arrastre nuevo, que es la misma acción que deshace la
selección y repliega el folio — o sea que el cubo se mueve exactamente cuando no
hay una cara elegida, y se queda quieto cuando sí.

Consecuencias que ya se aprovechan: con el cubo `parked` el render bajo demanda
no redibuja **ningún** cuadro, así que un cubo detenido no consume GPU; y el
ángulo objetivo pasa por `nearest()`, que elige el equivalente a ±180° del actual
para que no desenrolle vueltas enteras yendo al mismo lado.

### El lazy-init difiere CREAR el contexto, no dibujarlo

Hay **dos `IntersectionObserver` sobre `#cube`** y se confunden fácil, porque
miran el mismo elemento y hacen cosas distintas: el de `main.js` decide **cuándo
existe** el contexto WebGL, el de `cube.js` sólo pausa el loop cuando la sección
sale de pantalla.

Lo que se difiere no es el costo de dibujar —la geometría es trivial— sino el de
**crear el segundo contexto**: memoria de GPU, compilación de shaders y armado
del pipeline. Ese costo se paga una sola vez y **no lo evitan ni el render bajo
demanda ni la pausa por visibilidad**, porque para pausar un contexto primero hay
que crearlo.

Va con **`rootMargin: '0px'` a propósito**, que es lo contrario de lo habitual:
el hero mide `100vh`, así que la sección del cubo arranca ~20px debajo del fold y
cualquier margen de anticipación la haría intersectar ya en la carga — no se
diferiría nada. Con margen 0 el contexto se crea al scrollear, fuera del pico de
carga inicial. **Si alguien "mejora" esto agregando un `rootMargin` generoso,
desactiva la optimización entera sin que se note.**

### `素顔 Sugao` es la persona entera, en su propia página — no una sección de la portada
Sugao es **la persona detrás del proyecto, completa**: perfil profesional y
perfil personal. **Se publica ya**, en `/sugao/` y sólo ahí.

**Sin introducción**: la página arranca directo en el perfil profesional, que es
lo que contesta la pregunta que trae el lector. Una apertura genérica antes de
eso sólo demora la respuesta.

**Dónde NO va.** Hubo una sección `#operator` en la **portada** con nombre, rol,
trayectoria y `免責事項`, al modo de un `運営者情報`. Se eliminó entera y **no se
reintroduce**: la portada no lleva nada de esto. Quien quiera saber quién está
detrás entra a la cara, que para eso está en el cubo.

Decisiones dentro de la página:
- **Sin foto, y sin hueco reservado para una.** La credibilidad la carga el
  enlace a **LinkedIn**, que es verificable; un retrato no aporta nada
  comprobable y hay que mantenerlo.
- **El perfil profesional va en PROSA, no en formato CV.** Una lista de puestos y
  fechas se lee como currículum y no contesta la pregunta que trae el lector, que
  es qué habilita a esta persona a publicar esto.
- **Sin slots vacíos** para los perfiles que todavía no entran (IMDb,
  MyAnimeList, Steam, GitHub). Un hueco reservado para algo que no está se lee
  como página incompleta. Cuando existan, se agregan a `.profile-links`.
- **El `免責事項` NO va en `/sugao/`.** Ver la regla de abajo.

**Del archivo de referencia ya sólo queda en pie el `domain`**, «The human
behind», que es lo que muestra la tarjeta de la portada. Los otros dos los pisó
la redacción del autor y **el archivo de referencia quedó atrás**:

| Campo | Referencia | Vigente |
|---|---|---|
| `gloss` | «the true face» | **«The face behind the Cube»** |
| `status` | «Intro live · profiles deferred» | **«Live»** (`active`) |
| `domain` | «The human behind» | sin cambios |

O sea que para esta cara **la regla de copiar literal del archivo de referencia
ya no aplica**: manda lo redactado. Vale la pena tenerlo presente antes de
"restaurar" un campo desde la referencia creyendo que se corrige una deriva.

### El `免責事項`: el corto se repite, el completo vive una sola vez
Son **dos textos con dos reglas opuestas**, y confundirlas es lo que hay que
evitar:

- **El corto** —una línea: esto no es asesoramiento de inversión ni financiero—
  va en el **footer global**, o sea que **se repite en todas las páginas**. Esa
  repetición no es deriva: es su función. Una advertencia sólo sirve si está
  donde el lector está leyendo, no en una página a la que haya que llegar.
- **El completo** vive **UNA sola vez, en `/disclaimer/`**, y todo lo demás lo
  **enlaza**. Nunca se duplica. Dos copias de un texto legal derivan, y cuando
  derivan el sitio se contradice a sí mismo justo en lo único donde no puede
  permitírselo.

La prueba para saber cuál se está por escribir: si son más de una línea, va en
`/disclaimer/` y desde donde estabas se pone un enlace.

**EL TEXTO DE `/disclaimer/` ES UN BORRADOR SIN REVISAR.** Está redactado y
publicable como andamiaje, pero **no lo validó un profesional legal japonés**
(benrishi o abogado). No tratarlo como definitivo ni citarlo como si lo fuera:
declara ley aplicable japonesa y limitación de responsabilidad, que son
exactamente las cláusulas donde un texto sin revisar puede no sostener lo que
promete. **Antes de publicar a `main`, esto necesita revisión profesional.**

Y una cláusula tiene fecha de vencimiento propia: **«Language»** dice hoy que
prevalece el inglés hasta que se designe otra versión como autoritativa. Cuando
exista `/ja/` hay que revisarla, porque la prevalencia puede invertirse.

**Para la plantilla futura de notas financieras** (no existe todavía, no hay nada
que construir hoy): cada nota tiene que llevar **el corto al pie**, igual que
cualquier otra página. No el completo.

### `href="#"` es andamiaje, y hay guarda para que no sobreviva
**Hoy no queda ninguno**: el de LinkedIn en `/sugao/`, que era el único, lo
completó el autor con la URL real. La guarda queda igual, para el próximo.

Mientras un ancla lleve adentro su placeholder, es andamiaje declarado y
`check-ready` ya impide publicar. Lo que `check-structure` ataja es el caso
**silencioso**: que alguien redacte el rótulo, borre el `TODO` y se olvide de
pegar la URL — ahí el placeholder desaparece, todo se pone verde y el enlace
queda muerto. La guarda falla **exactamente** en ese momento y no antes.

### No templetizar: verificar
El nav y el footer están **duplicados** en todas las páginas. No hay build step
que los comparta, y las alternativas eran peores (inyectar por JS rompe la regla
de contenido en el HTML; Jekyll sería un build step y choca con `.nojekyll`).
La duplicación es aceptable **si está vigilada**: `check-ready.py` verifica que
los bloques sean idénticos carácter por carácter. Por eso el nav usa rutas
absolutas.

### El bloque de estado + botón es un folio que se despliega
**Esto REVIERTE una decisión anterior.** Antes el bloque de entrada reservaba
su altura desde el inicio con `min-height`, para que aparecer el estado y el
botón al seleccionar una cara no empujara el layout. Ahora el folio arranca con
**altura cero** y se **despliega animado** al seleccionar; se repliega al
arrastrar (deseleccionar).

Por qué se pudo revertir sin traer de vuelta el salto de layout: el folio está
**debajo** del cubo y de la grilla. Lo que se desplaza al abrirlo es el enlace
a Musubi y lo que sigue —nunca el cubo ni la cara que el usuario
acaba de tocar—, así que **nada se mueve bajo el cursor**. Reservar el espacio
dejaba un hueco vacío permanente para algo que la mayor parte del tiempo no
está; el folio sólo ocupa lugar cuando hay algo que mostrar.

Detalles que ya se probó que importan:
- **Animado, no instantáneo.** Un cambio de altura de golpe se lee como página
  rota; con transición se lee como despliegue. Es condición, no adorno.
- **Se anima `grid-template-rows` de `0fr` a `1fr`**, no `height` a `auto`
  (`auto` no interpola sin `interpolate-size`, sólo-Chromium) ni una altura fija
  en px (número mágico: el texto del estado no está redactado y el botón cambia
  de ancho con cada cara). `1fr` resuelve a la altura real del contenido. Su
  modo de fallo es el correcto: un motor que no interpole `fr` salta de 0 a la
  altura final, que es justo lo que se pide con `prefers-reduced-motion`.
- La separación superior va como **margen del primer hijo**, no `padding` del
  contenedor con overflow: con `border-box` el padding es un piso de altura que
  no colapsa y el folio plegado medía 16px en vez de 0.
- `inert` viaja con el estado plegado: no basta con invisible, tampoco tabulable
  ni leído por lector de pantalla.

`check-modes.py` lo verifica: plegado al cargar, desplegado al seleccionar,
replegado al arrastrar, transición declarada sobre `grid-template-rows`, y **el
cubo no se mueve** al abrirse (que es la propiedad que hace seguro el cambio).

### La transición entre páginas (maelstrom) está RESERVADA, fuera del lanzamiento

**Hoy el sitio NO tiene transición.** Entrar a una cara es una navegación normal
del navegador: **corte seco, sin fundido de ningún tipo.** Se apartó por
decisión del autor —no terminaba de funcionar— y **no se borró**.

Medido, no deducido: en una subpágina, `.face-page`, `main`, `body` y `html`
computan `animation: none` y `opacity: 1`. **La única excepción es el hero de la
portada**, que sube y aparece con `kf-rise` durante 1.3 s — y **eso no es un
resto de la transición**: corre en cualquier carga de la portada, incluida la
primera, y existía antes. Se queda a propósito: la portada es la que recibe, y
que tenga vida al cargar mientras las subpáginas entran secas es la asimetría
buscada. Está anotado junto a la regla, porque ahora que no hay transición es lo
único que se mueve al llegar y se lee fácil como un olvido.

**Dónde está**: `assets/css/maelstrom.css`, entero y calibrado, **no enlazado
desde ninguna página**. Ese archivo lleva en su encabezado cómo reactivarla, los
valores medidos y el bug conocido. En `styles.css` quedó un comentario en el
lugar de donde salió.

**Por qué en un archivo y no detrás de un flag.** Es una transición **entre
documentos**: `@view-transition` tiene que estar en la página que se va **y** en
la que llega. **Diez de las once páginas no cargan ningún JavaScript** —
verificado: `document.scripts.length` es 0 en una subpágina—, así que un
interruptor en runtime obligaría a meter JS en todas. No es una preferencia de
estilo: es que la otra opción choca con una regla del proyecto.

Lo calibrado, para no rehacerlo a ojo: **rotación 46°** (era 14°), **escala
2.1** (era 1.3), **blur 4px** (era 16px), entrada desde **−38°** y 0.52, las dos
rotaciones en el **mismo sentido**. Y las **dos causas** de que la primera
versión se leyera como fundido y no como giro:

1. **El desenfoque tapaba el giro.** Una rotación se percibe por el ángulo de
   los BORDES, y 16px de blur son justo lo que los borra. Bajó a 4px.
2. **El fundido iba atado al giro**, así que la página estaba casi transparente
   antes de haber girado lo suficiente. Giro y fundido tienen que ser **dos
   animaciones con curvas distintas** sobre la misma capa. Juntarlas «para
   simplificar» reintroduce el problema.

**HAY UN BUG CONOCIDO Y ES EL PRIMER LUGAR DONDE MIRAR.** La variante táctil
**no hace lo que dice**: dentro de `@media (pointer: coarse)` se definen
`kf-maelstrom-out`/`in` —escala + fundido sin blur— pero **nunca se asignan**,
porque esas reglas sólo tocan `animation-duration`. El `animation-name` sigue
siendo `kf-maelstrom-spin-out`, que lleva `filter: blur(4px)`. O sea que **en un
teléfono corría la versión de escritorio con desenfoque**, apenas más rápida:
exactamente el costo que esa variante existía para evitar. Nunca se midió en un
dispositivo real, así que no se sabe cuánto de «no funcionaba bien» venía de
ahí. **Cualquier documento que diga «táctil sin blur» está describiendo la
intención, no lo que corría.**

**Lo que NO se fue con ella, y no son restos olvidados:**
- **La precarga (`rel=prefetch`) al seleccionar la cara.** Sirve igual sin
  transición, o se nota más: ahora el corte es seco, y un corte contra una
  página que todavía está bajando es el blanco entre una y otra.
- **El respaldo por `sessionStorage` del botón atrás.** Nunca tuvo que ver con
  la transición: restaura la **cara elegida** en el cubo. Verificado después de
  apartarla — `back_forward`, cara restaurada, folio abierto.

### Volver atrás restaura el cubo por dos caminos
Los dos hacen falta. **bfcache**: la página vuelve viva y entera sin ejecutar
nada; lo único que puede romperse es el contexto WebGL (el navegador libera la
GPU mientras está congelada), así que en `pageshow` con `persisted` se comprueba
`isContextLost()` y, si se perdió, se rehidrata. **Sin bfcache** (Chrome lo
descartó por memoria, o `Cache-Control: no-store` lo deshabilita —ojo, el
servidor de desarrollo manda `no-store`): la selección se restaura desde
`sessionStorage`, y **sólo** si la navegación fue `back_forward` — llegar a la
portada normalmente no debe elegir una cara en tu nombre.

### La capa de metadatos se genera y se vigila; nada se escribe a mano dos veces
`sitemap.xml` y `og-image.png` salen de scripts (`tools/make-sitemap.py`,
`tools/make-og-image.py`). El sitemap es la misma lista de URLs que ya existe
como directorios: se deriva en vez de copiarse, y `check-structure.py` verifica
que no le falte ninguna página. La imagen OG es **sólo tipografía** —llevaba el
cubo capturado del sitio y se sacó—, así que su script no necesita navegador, y
**lee los colores del `:root`** en vez de copiarlos: copiarlos haría que la
tarjeta derive de la paleta en silencio y que `:root` dejara de ser una entrada
real de la imagen.

- **`robots.txt` no bloquea crawlers de IA** — GPTBot, ClaudeBot, CCBot y demás.
  Es deliberado y está escrito en el archivo para que nadie los agregue "por las
  dudas": la descubribilidad por máquinas es objetivo del proyecto, la misma
  razón por la que el contenido va en el HTML.
- **Títulos y descriptions únicos por página, verificado.** Las seis subpáginas
  de las caras salieron del mismo molde y **compartían la description palabra
  por palabra**; eso hace que buscadores y crawlers las traten como duplicados y
  se queden con una. Ahora cada placeholder nombra su cara, y la guarda no deja
  que vuelvan a coincidir.
- **La 404 lleva `noindex` y queda fuera del sitemap**, y la guarda falla si una
  página con `noindex` aparece listada: son dos declaraciones que se contradicen.
  Usa rutas absolutas porque GitHub Pages la sirve ante URLs de cualquier
  profundidad.
- **`canonical`, `og:url` y `og:image` son ABSOLUTAS y autorreferentes**, con
  guarda. Quien arma la vista previa (LinkedIn, Slack, X) no es el navegador del
  lector y no resuelve rutas relativas: la tarjeta sale sin imagen. **El fallo no
  se ve en el sitio, se ve afuera**, que es por qué necesita guarda y no revisión
  visual. La 404 está exenta: no lleva ninguna de las tres, a propósito.
- **La og-image puede quedar vieja en silencio**: es un archivo, no una vista.
  `tools/og-image.lock.json` guarda el hash de sus ENTRADAS y la guarda avisa si
  alguna cambió. **La lista tiene que ser exacta en las dos direcciones**: una
  entrada de más avisa por cambios que no influyen —señal falsa, el mismo mal que
  partir `check-ready` vino a curar— y una de menos deja la imagen vieja en
  silencio. Hoy son: el script, el `:root` de styles.css, y las fuentes Inter y
  Zen Kaku. Salieron al sacar el cubo de la tarjeta: **cube.js** y **Cormorant**.
  Se hashea sólo el `:root` y no el CSS entero, que cambia por cosas ajenas.
- **Los archivos de texto del lock se hashean NORMALIZADOS; los binarios, por
  bytes.** `core.autocrlf=true` es el valor por defecto en Windows: git guarda
  LF y escribe CRLF al hacer checkout. Hasheando los bytes crudos del `.py`, la
  guarda avisaba «la og-image quedó vieja» con sólo **cambiar de rama y volver**
  —y también en cualquier **clon nuevo**—, sin que hubiera cambiado nada que
  mueva un píxel del PNG. Doblemente malo: es la señal falsa que esta guarda
  existe para no dar, y rompía justo el caso que motivó hashear contenido en vez
  de fechas, que era sobrevivir a un clon. Las fuentes siguen por bytes a
  propósito: son binarias, git no las convierte, y ahí el byte crudo sí es el
  contenido. Verificado en las dos direcciones: pasar el script a CRLF y a LF no
  avisa, y cambiar una línea de verdad sí.
- **La tarjeta se juzga a ~500 px, no a 1200**: es el ancho al que se ve en un
  feed. Ahí el nombre de la marca quedaba en ~10 px y era lo primero que se
  perdía; ahora va al doble de cuerpo y en blanco. Y la bajada usa **Inter, no
  Cormorant**, por lo mismo que el romaji del cubo: a ese tamaño las astas finas
  de una serif de display desaparecen. `--prueba` deja la versión reducida.
- **hreflang: sólo el patrón anotado en el README**, sin implementar, hasta que
  exista `/ja/`.

### Los placeholders de metadatos también se cuentan
Los `TODO` de `<title>` y de `content="…"` **no llevan `class="todo"`**, porque
no son elementos. Durante un tiempo no se contaron, y el sitio podía dar «LISTO
PARA PUBLICAR» con seis descriptions que decían *«TODO: descripción de esta
cara.»* — exactamente el fallo que la guarda existe para evitar. `placeholders()`
ahora cuenta las dos familias. Si aparece otra clase de placeholder que no sea
un elemento con clase, hay que agregarla ahí.

### El shader del mar es código cerrado
El GLSL de `assets/js/background.js` está calibrado a mano y **no se toca**. Su
paleta (`deep`, `mid`, `crest`) vive en constantes del fragment shader, **fuera
de `:root`** — es la única excepción a "ningún color literal fuera de `:root`".
Cambiar el color del mar exige editar el shader, y esos valores no se sincronizan
solos si cambia la paleta.

### En la versión inglesa no va japonés ornamental
La prueba es simple: **si el japonés sólo traduce la palabra inglesa que tiene
al lado, es textura y se saca.** Si es un nombre conceptual propio, se queda.

- **Se sacaron**: `The Cube · 立方体`, `Method · 一次資料`, y los kanji que
  encabezaban las tres tarjetas del método (`一次資料` / `追跡可能` / `公開`),
  cada uno traduciendo su propio título inglés.
- **Se quedan**: `素顔`, `免責事項`, los seis nombres de las caras, los tres
  términos del núcleo, y **los nombres reales de los organismos** en la lista de
  fuentes (`日本銀行` junto a Bank of Japan). Esos no decoran: son el nombre por
  el que se llega a la fuente.

**La versión japonesa se escribirá como ORIGINAL, no como traducción de ésta**:
ahí «The Cube» será katakana, no `立方体`. Por eso lo que se sacó no se tiró —
los glifos siguen en el subset a propósito. Ver la advertencia en el
`@font-face` de `styles.css` antes de regenerarlo.

### `/musubi/` explica la IDEA, no los nombres

**Esto reemplaza una premisa anterior.** La página nació como «el sistema de
nombres»: siete bloques sobre por qué hay nombres japoneses, cómo se deriva cada
uno, y una tabla con las seis caras y su razón. Se redactó entero de nuevo, en
**cuatro bloques** que explican la idea de la que sale la plataforma — el agua
(`Kasen`, `Okeanos`), el nombrar (`Kotodama`), el vínculo (`Musubi`) y quién es
el lector (`Odysseus`, `Aeolus`).

- **La tabla de las seis caras salió a propósito, no se perdió.** Cada cara dice
  lo suyo en su propia página; la tabla obligaba a mantener sincronizadas dos
  listas de la misma cosa.
- **La página no explica los nombres de las caras, y no hay que reponer eso.**
  Es la consecuencia buscada del punto anterior.
- **Los seis nombres del marco van en `<i class="name">`**, cursiva y a color
  de texto pleno. `<i>` y no `<em>` porque `<em>` es énfasis y un lector de
  pantalla lo entonaría; cada nombre se marca **una sola vez**, donde se lo
  presenta. Y no van en oro: el oro es de los subtítulos y los enlaces.
- **Usa `.face-page`, como las otras nueve subpáginas.** Antes usaba `.naming*`,
  que ya no existe: se borró con la tabla. De paso ganó el `<h1>` que le
  faltaba — era la única subpágina que no tenía, sólo un `<h2>`.
- **Dos frases del bloque 3 son las mismas que cierran el lead del cubo en la
  portada**, a propósito del autor. Son dos copias del mismo texto y **no hay
  guarda que las compare**: si se redacta una, hay que mirar la otra. Está
  anotado en el HTML de los dos lados.

### `/method/` es el desarrollo; la sección de la portada es el resumen
La sección `#method` de la portada **queda** —los tres pilares y los cuatro
pasos— y la nav «Method» **sigue apuntando ahí**, no a la subpágina. A
`/method/` se llega por un enlace al pie de esa sección.

**La lista taxativa de fuentes vive dentro de `/method/`, no en un `/sources/`
aparte.** Separarlas obligaría a mantener sincronizados el criterio y su
aplicación, que es exactamente lo que no debe poder divergir. La portada muestra
**cinco de ejemplo**, japonesas y globales, para que se vea que el alcance no es
sólo Japón.

### No redactar contenido
Sólo **andamiaje con placeholders `TODO`**, en castellano a propósito para que no
puedan confundirse con copy real (el sitio está en inglés). El texto final y la
versión japonesa son un pase aparte del autor. Tampoco se inventan explicaciones
del sistema filosófico ni las razones de los nombres.

### Otras reglas vigentes
- **Ningún color literal fuera de `:root`**, incluidos los que consume el JS
  (`cube.js` los lee con `getPropertyValue`, **sin fallback**: si falta un token
  falla con su nombre en vez de disfrazarlo con un hex de repuesto).
- **El contenido va en el HTML**, no inyectado por JS: la descubribilidad por
  crawlers de IA es objetivo del proyecto y esos crawlers no ejecutan JS.
- **La grilla de seis es la capa semántica**: nav de teclado y lo que leen los
  crawlers. En vista 3D se oculta con el patrón clip, **nunca** `display:none`.
  Al recibir foco se corre **al costado** del escenario, no encima: taparlo
  escondía justo lo que el usuario de teclado necesita ver.
- **URLs por directorios** (`/musubi/`, `/hajime/`…), sin extensión.
- **Cada texto japonés nuevo obliga a regenerar el subset** de Zen Kaku. Ver
  README. **`document.fonts.check()` no sirve** para verificarlo: informa si la
  fuente está cargada, no si contiene el glifo.

---

## Flujo obligatorio antes de cada commit

Correr las guardas. **Si alguna falla, no commitear**: arreglar, o revertir al
último commit verde y avisar qué se revirtió y por qué. El objetivo es que todo
commit sea un punto de restauración seguro por construcción, no por suerte.

| Guarda | Cuándo | Costo | Se espera |
|---|---|---|---|
| `python tools/check-structure.py` | siempre | instantánea | **verde** |
| `python tools/check-modes.py` | siempre | ~40 s | **verde** |
| `python tools/check-pendulum.py` | antes de push, o al tocar la física | ~2–4 min | **verde** |
| `python tools/check-ready.py` | antes de publicar a `main` | instantánea | rojo hasta la redacción |

Las dos que usan navegador necesitan el sitio servido en `:8000`.

**Por qué `check-ready` no va en cada commit.** Está en rojo por diseño mientras
queden placeholders, y **una guarda siempre en rojo deja de ser señal**: uno se
entrena a ignorarla y el día que se rompa algo de verdad no lo ve. Por eso se
partió en dos, con códigos de salida distintos:

- `check-structure.py` — nav y footer idénticos, cobertura del subset, y **sin
  placeholders nuevos contra `tools/placeholders-baseline.json`**. Sale `0`/`1`.
  Ésta es la que tiene que estar verde siempre, así que su rojo significa algo.
- `check-ready.py` — ¿puede ir a `main`? Sale `0` listo, **`2` falta redacción
  (esperado, no es regresión)**, `1` algo roto de verdad.

Cuando se redacta un placeholder el conteo baja: la guarda lo informa y **no**
falla, pero hay que fijar el piso nuevo con
`python tools/check-structure.py --actualizar-baseline`.

**Tags**: sólo en hitos. El próximo natural es cuando el andamiaje esté completo,
antes del pase de redacción.

---

## Cabos abiertos (lista viva)

**Estado al cierre de la sesión del 2026-08-03.** El andamiaje está completo
—once páginas, el cubo, la transición, la capa de metadatos y las guardas—,
**empezó la redacción**, y el registro técnico ya no tiene huecos.

### Hecho en esta sesión (2026-08-03): documentar desde el código

Sesión de documentación: **no se tocó ni una línea de comportamiento**. Se
cerraron los huecos del registro técnico leyendo el fuente, no los papeles.

- **README**: dos secciones nuevas, «El import map» y «El cubo: parámetros
  vigentes» (geometría, constantes, encuadre, luces, colores, péndulo,
  `snap`/`parked`, lazy-init), más el índice de `docs/mediciones/`.
- **`docs/mediciones/rendimiento.md`**, nuevo: la única medición de rendimiento
  que existe, de escritorio, fechada y con condiciones.
- **Divergencias resueltas contra el código**: `docs/v1-dark/README.md` daba como
  actuales unas luces y un fondo que son del tag, y quedó marcado como histórico
  punto por punto; `luz-arco.md` sí coincidía y quedó confirmado.
- **`cube.js`**: el encabezado decía «las luces van tintadas en oro» y era falso
  **desde el primer commit** (verificado con `git log -L` y `git log -S`: `hemi`
  y `key` nunca fueron doradas). Se sacó de ahí y el reparto real vive ahora en
  el bloque de luces, junto al código que lo aplica.

**La regla que dejó la sesión**: los números del cubo se leen del código y se
tabulan en un solo lugar. Ver la decisión cerrada correspondiente.

### Ya redactado: texto definitivo, versión de lanzamiento en inglés

- **El hero de la portada.** Titular y bajada nuevos.
- **`/sugao/` entera**: perfil profesional y personal, con LinkedIn (URL real) y
  LibraryThing. Sin introducción, sin foto y sin slots vacíos.
- **`/disclaimer/` completo** —ocho cláusulas— y **la línea corta del `免責事項`
  en el footer de las once páginas**.

La versión japonesa es un pase aparte y **se escribe como original, no
traduciendo de acá**.

### Andamiaje agregado en la sesión del 2026-07-25

- **`/method/`**, subpágina nueva, con placeholders. La sección `#method` de la
  portada **queda como resumen** y la nav sigue apuntando a ese ancla; a la
  subpágina se llega por «Read the full method →» al pie. La lista taxativa de
  fuentes vive **dentro** de `/method/`; no hay `/sources/`.
- **Cinco fuentes de ejemplo** en la portada: BOJ, FSA, EDINET, BIS y Damodaran
  Online, japonesas y globales.
- **Rótulos japoneses ornamentales retirados de la versión EN** (`立方体`,
  `一次資料`, `追跡可能`, `公開`). **Los glifos siguen en el subset** para
  `/ja/`, con una advertencia en el `@font-face` para que nadie los borre al
  regenerarlo.

### El único frente activo: la redacción

**41 placeholders `TODO`** en **8 páginas**, y **se escriben fuera de Code** —
son decisiones de contenido del autor, no tareas de implementación.

| Página | Placeholders |
|---|---|
| `/method/` | 12 |
| `/hajime/` `/tosei/` `/kamon/` `/torii/` `/kizuna/` | 5 c/u |
| `404.html` · portada | 2 c/u |
| `/musubi/` · `/sugao/` · `/disclaimer/` | **0 — no les falta nada** |

**`/method/` es la última página que sigue siendo andamiaje puro.** Las cinco
caras tienen 5 cada una y son todas del mismo molde: las dos `description`, el
lead y dos párrafos de cuerpo.

**Al redactar `/method/`, aplicar también las dos notas de fuentes provisorias**
que hoy están en la portada, ya corregidas por el autor y anotadas en el
comentario del propio HTML: BIS → «Cross-border banking exposure»; Damodaran →
«Valuation datasets by sector and region».

### Los tres estados dicen QUÉ HAY, no qué importa — decisión cerrada

`5de4566`. **Sugao lleva `active` con el estado «Live»; Hajime bajó a `light` y
conserva «First analysis on the way».** Las otras cuatro no se tocaron.

Se lee al revés de lo que uno espera, y por eso conviene el motivo escrito:
Hajime es la cara del análisis, o sea el proyecto, así que el instinto es
dejarle el marcador más fuerte. Pero **Hajime no tiene todavía una línea
publicada y Sugao está entera.** El lead del cubo ya promete «One is live
today», y con el reparto anterior la grilla lo desmentía: el punto lleno estaba
en la cara vacía. Si alguien lo "arregla" devolviéndoselo a Hajime, vuelve a
haber dos caras leyéndose como la más fuerte y ninguna es la publicada.

**No se agregó un cuarto estado, y el porqué importa más que el resultado.** Se
evaluó un `live` propio y no había con qué distinguirlo:

- **La animación no sirve.** `prefers-reduced-motion: reduce` apaga todo con
  `animation: none !important`, así que dos puntos que sólo difieran por el
  pulso quedan idénticos justo para quien más necesita la señal.
- **Un color nuevo tampoco**: la paleta es navy + oro, y el vocabulario ya está
  agotado — lleno en oro, hueco en oro, hueco en gris.

Con tres estados y tres grados de «cuánto hay», alcanzaba con **cambiar quién
ocupa cada uno**. El sistema queda intacto.

Sigue abierta una decisión adyacente que ya estaba anotada: el `domain` de la
tarjeta («The human behind») sale del archivo de referencia, así que cambiarlo
es otra cosa.

### Cerrado en la sesión del 2026-08-04: los metadatos alcanzaron al hero

`bf70085`. El `<head>` de la portada y la tarjeta social seguían describiendo el
hero anterior. **Es el modo de fallo de fábrica de estas dos cosas**: no se ven
al mirar la página, así que sobreviven al reemplazo del texto que describen.

- `<title>` y `description`/`og:description` **derivados del hero**, con la
  dependencia anotada en el propio `<head>`.
- `LINEA` de `make-og-image.py` es ahora **el titular del hero, literal**;
  imagen regenerada y lock resellado. Verificada a 500 px.
- **`og:image:alt` describía «El cubo de seis caras», y la tarjeta no lleva el
  cubo desde que pasó a ser sólo tipografía.** Además estaba **en castellano**,
  la única cadena así fuera de los `TODO`, y viaja en cada enlace compartido.

Ese último deja un hueco que conviene tener presente: **`og-image.lock.json`
vigila las ENTRADAS de la imagen, no el TEXTO que la describe.** El alt puede
quedar mintiendo sin que ninguna guarda se entere, porque no es una entrada de
la composición. Hoy no hay guarda para eso y no está claro que valga una: la
única regla comprobable sería prohibir la cadena vieja, que caza este caso y
ningún otro.

El piso está fijado en `tools/placeholders-baseline.json`: **bajarlo es progreso,
subirlo es un bug**. Al redactar, correr
`python tools/check-structure.py --actualizar-baseline` para fijar el piso nuevo.
Incluye los `TODO` de `<title>` y `content="…"`, que no llevan `class="todo"`.

Y lo de siempre: **cada texto japonés nuevo obliga a regenerar el subset** de Zen
Kaku, verificando contra la tabla `cmap`. Ya frenó una vez, con el 迷 de la 404.

### Congelados por decisión del autor — no proponerlos

- **Móvil.** Sin medir en dispositivo real (degradación del cubo, el FOV
  horizontal que manda con el escenario más alto que ancho, el maelstrom táctil).
  Se retoma cuando el autor lo diga.

  **Hay una sola medición de rendimiento y es de escritorio**:
  `docs/mediciones/rendimiento.md` (julio de 2026, RTX 4060 Laptop a 165 Hz).
  Ahí sobra margen — la página completa mide lo mismo que no dibujar nada— y el
  único término que aparece es el shader del mar, que evalúa ruido por píxel a
  pantalla completa. **Ese resultado no dice nada de móvil**: el costo escala con
  los píxeles y una GPU de teléfono no tiene ese margen. La media resolución y
  el cap de 25 fps son **precaución, no medición**.

  Y el tercer ejemplo que estaba acá —«el maelstrom táctil sin blur»— **había
  que sacarlo, porque nunca fue cierto**: esa variante definía sus keyframes
  pero no los asignaba, así que en táctil corría la versión con desenfoque. Es
  el aviso más útil de todo este párrafo: una precaución que se documenta y no
  se verifica es indistinguible de una que no existe. La transición está hoy
  reservada; el detalle, en `assets/css/maelstrom.css`.
- **Vista explotada del cubo.** Va **después** del pase de redacción; se discutió
  fuera de estas sesiones y el brief todavía no está escrito. Lo que sí está
  decidido, para que el brief lo dé por sentado: al abrirse, el **núcleo** del
  cubo muestra los **tres conceptos** del centro conceptual del proyecto en
  kanji —**産霊 · 河川 · 言霊** (Musubi · Kasen · Kotodama)— y al hacer clic
  lleva a **`/musubi/`**. **No hacen falta glifos nuevos** en el subset, pero
  ojo con el motivo, porque el que estaba escrito acá dejó de ser cierto: los
  tres ya NO viven en el HTML de `/musubi/` —esa página se redactó y ahora
  nombra a Kasen y Kotodama en romaji, no en kanji—. Siguen cubiertos porque
  están en la **marca de agua de la portada** (`.about__watermark`) y porque
  `言` y `霊` son además el logo del nav. Si algún día se toca esa marca de
  agua, esta suposición se cae. No hay nada visual que construir hoy.
- **Remolino ukiyo-e para la transición.** Ocho iteraciones fallidas entre Design
  y Claude: **el ruido procedural produce textura, no dibujo** — granulado, no la
  línea de una ola grabada. Requiere ilustrador humano o un enfoque distinto.
  **No reintentar con los mismos medios.** Y hoy la pregunta ni se plantea: la
  transición entera está **reservada y fuera del lanzamiento**, así que no hay
  nada que ilustrar hasta que se decida retomarla.

### Ideas anotadas, sin probar

- **Unabare de fondo en la og:image.** Usar un frame estático del mar,
  oscurecido, detrás de la tipografía. La tarjeta actual es legible pero
  **genérica**; el mar es lo que la haría reconocible como este proyecto y no
  como cualquier sitio financiero serio.
  *(«Unabare» es como el autor llama al shader del mar; el nombre no aparece en
  el código, donde es `background.js` / `#sea`.)*

  Lo que ya está resuelto para intentarlo: `initSea(canvas, reduce, stillTime)`
  dibuja **un solo frame** con `preserveDrawingBuffer: true`, que es justo lo que
  hace falta para poder leer los píxeles del canvas. `STILL_TIME = 12.0` es el
  instante elegido, y el tercer parámetro permite probar otros.

  **El costo a sopesar antes de empezar**: hoy `make-og-image.py` no necesita
  navegador ni servidor, que fue una ventaja explícita de sacar el cubo. Meter el
  mar la devuelve, y además reintroduce `background.js` como entrada de
  `og-image.lock.json`. No es un impedimento, pero es un intercambio, no una
  mejora gratis. Y el texto tiene que seguir leyéndose **a 500 px**: el mar es
  oscuro y de bajo contraste, así que probablemente haga falta oscurecerlo más de
  lo que parece necesario a tamaño completo.

### Depende de que exista `/ja/`

- **hreflang y versión japonesa**: patrón documentado en el README, sin
  implementar. Incluye `<html lang="ja">`, canonical de cada página a sí misma, y
  extender `make-sitemap.py` con `xhtml:link`.

### Cerrados en esta sesión — no reabrir

- ~~Luz a lo largo del arco del péndulo~~ — no había problema. La métrica decía
  «70% del perímetro con ΔL bajo» y era cierto, pero no significaba lo que
  parecía: el cuerpo del cubie (lum ~11.5) es **más oscuro que el fondo** (15.3),
  así que todo perímetro sin iluminar falla por construcción — y un objeto más
  oscuro que su fondo se lee como silueta. Lo que desaparece es ΔL ≈ 0, no ΔL
  chico y consistente. Cerrado por inspección visual, todo en
  `docs/mediciones/luz-arco.md`. **La pregunta era perceptual y binaria: si
  alguien sospecha que el cubo se pierde, se saca una captura, no un barrido.**
- ~~`favicon.ico` 404~~ — hay `.ico` (16/32/48), `.svg` y `apple-touch-icon`,
  generados por `tools/make-favicon.py`. Consola limpia.
- ~~Animación maelstrom~~ — implementada y calibrada dos veces, y después
  **apartada del lanzamiento** por decisión del autor. Reservada en
  `assets/css/maelstrom.css`; ver la decisión cerrada arriba. **Reabrirla es
  post-lanzamiento**, y ahí el punto de partida es el bug de la variante
  táctil, no una recalibración.
- ~~Capa de metadatos~~ — sitemap generado, robots abierto a los crawlers de IA,
  Open Graph completo, 404, y títulos/descriptions únicos verificados por guarda.

---

## Hallazgos de método (para no repetirlos)

Estas equivocaciones ya costaron tiempo. Todas fueron **métricas mal elegidas**
que produjeron conclusiones equivocadas:

- **Ratios de contraste WCAG entre dos navies casi negros**: pasar de 2.27× a
  4.20× eran 3 unidades sRGB sobre 255, invisibles. Medir en **unidades sRGB
  absolutas**, no en ratios.
- **"Brillo de la cara más oscura"**: castiga a los esquemas con más rango, que
  son los buenos. Usar **% de píxeles a menos de 3 unidades del fondo**.
- **Calibrar en una sola pose**: un esquema ganó por maximizar el rango en una
  pose fija, que es justo lo que produce luz inestable al girar. Medir en **2–3
  poses rotadas** y reportar la variación.
- **`document.fonts.check()`** da falsos positivos de cobertura de glifos.
  Verificar contra la tabla `cmap` de la fuente.
- **Leer un canvas WebGL fuera de su frame** devuelve vacío: da falsos negativos.
  Renderizar y leer en el mismo turno, o usar la captura compositada.
- **`Page.captureScreenshot` se cuelga durante una transición entre documentos.**
  El pedido queda esperando y revienta por timeout: no es que salga mal la
  captura, es que no vuelve. Para filmar una view transition hay que usar
  **`Page.startScreencast`**, que empuja cuadros como eventos en vez de
  responder pedidos. Y como los eventos llegan mezclados con las respuestas,
  conviene un hilo lector que consuma todo el socket: interrumpir un `recv()`
  por timeout para sondear deja media trama leída y cuelga lo que sigue.
  Para ver el detalle, `Animation.setPlaybackRate` ralentiza sin tocar el CSS,
  así que lo filmado sigue siendo la animación publicada.
- **En headless el loop del cubo corre a ~7–15 ticks/s, no a 30.** Las pruebas
  de física tienen que esperar **por ticks, no por reloj**.
- **Y las transiciones CSS tampoco siguen el reloj de pared en headless.** Misma
  trampa que la anterior, en otra forma, y muerde a cualquier medición de estado
  animado. Midiendo el folio 1,6 s después del clic dio **5 px de 97**: seguía a
  mitad del despliegue. Con `deviceScaleFactor=2` y dos contextos WebGL el
  compositor se atrasa muchísimo. **Esperar a que la propiedad se estabilice**
  —dos lecturas iguales seguidas— en vez de dormir un rato y dar por hecho que
  terminó. Lo delató que la captura mostraba el folio abierto y la medición
  decía que estaba cerrado: **cuando la captura y la métrica se contradicen, la
  sospechosa es la métrica.**
- **Un test roto se disfraza de bug de la página.** Si el JS de una guarda lanza,
  tiene que reventar el script, no devolver `undefined` en silencio.
- **Una variante que sólo se LEE no está verificada.** No es una métrica mal
  elegida: es la ausencia de métrica, disfrazada de código presente. La variante
  táctil del maelstrom definía sus keyframes sin blur y **nunca los asignaba**
  —sólo cambiaba `animation-duration`—, así que en teléfono corría la versión
  cara. **El CSS no protesta**: un `@keyframes` que nadie usa es legal y
  silencioso. Por eso la variante «existía» —se la podía leer, citar y
  documentar— y sobrevivió a dos calibraciones y a tres documentos que la daban
  por hecha. El mismo silencio dejó a `kf-fade` definido y sin usar.
  La prueba no es releer el bloque: es medir la propiedad efectiva en el modo
  que se quiere probar. Y el corolario incómodo: **una precaución documentada y
  nunca verificada es indistinguible de una que no existe** — la lista de
  precauciones de móvil tenía tres ítems y uno era falso.
