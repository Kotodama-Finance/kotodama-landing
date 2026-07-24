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

### `/sugao/` y el registro del operador
- **Portada `#operator`**: registro factual denso (nombre, rol, contacto,
  `免責事項`). La señal de confianza tiene que estar donde nace la duda.
- **`/sugao/`**: desarrollo de largo aliento, y después los perfiles diferidos.
  **No repite** los datos duros: los enlaza.
- **El `免責事項` vive en un solo lugar.** Texto legal duplicado es la peor
  clase de deriva.

No se duplica prosa: cambia el **registro**, no el contenido. Y el `id` de la
portada es `operator`, no `sugao`, para que el nombre Sugao designe una sola
cosa (la cara y su subpágina).

### No templetizar: verificar
El nav y el footer están **duplicados** en las ocho páginas. No hay build step
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
al sistema de nombres y lo que sigue —nunca el cubo ni la cara que el usuario
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

### La transición entre páginas (maelstrom) es CSS puro
Entrar a una cara usa **`@view-transition { navigation: auto }`** —transición
entre documentos, sin SPA ni router—, dentro de
`@media (prefers-reduced-motion: no-preference)` para que bajo reduced-motion no
haya nada que desactivar: la regla ni se declara. Hoy es sólo `transform` +
`filter: blur` + `opacity` sobre `::view-transition-old/new(root)`: la página
que se va gira/escala/desenfoca, la que llega entra girada desde el otro lado y
se acomoda, las dos en el **mismo sentido** para que se lea un solo remolino.

- `mix-blend-mode: normal` pisa el `plus-lighter` que el navegador pone por
  defecto: como las capas además se mueven y escalan, sumarlas daba un fogonazo
  claro donde se solapan.
- **Táctil** (`pointer: coarse`): escala + fundido, **sin blur** — el desenfoque
  a pantalla completa es lo caro y lo que peor escala en GPU de teléfono.
- Precarga (`rel=prefetch`) **al seleccionar la cara, no al pulsar el botón**:
  el gesto entre una cosa y otra es el tiempo que hace falta para que el
  documento ya esté en caché. Respeta `saveData` y 2G.
- **`feTurbulence` no se usa todavía**: es el escalón caro y la versión barata
  alcanza. Si hiciera falta más remolino, el próximo paso es darle
  `view-transition-name` propio a la nav para que quede quieta.

### Volver atrás restaura el cubo por dos caminos
Los dos hacen falta. **bfcache**: la página vuelve viva y entera sin ejecutar
nada; lo único que puede romperse es el contexto WebGL (el navegador libera la
GPU mientras está congelada), así que en `pageshow` con `persisted` se comprueba
`isContextLost()` y, si se perdió, se rehidrata. **Sin bfcache** (Chrome lo
descartó por memoria, o `Cache-Control: no-store` lo deshabilita —ojo, el
servidor de desarrollo manda `no-store`): la selección se restaura desde
`sessionStorage`, y **sólo** si la navegación fue `back_forward` — llegar a la
portada normalmente no debe elegir una cara en tu nombre.

### El shader del mar es código cerrado
El GLSL de `assets/js/background.js` está calibrado a mano y **no se toca**. Su
paleta (`deep`, `mid`, `crest`) vive en constantes del fragment shader, **fuera
de `:root`** — es la única excepción a "ningún color literal fuera de `:root`".
Cambiar el color del mar exige editar el shader, y esos valores no se sincronizan
solos si cambia la paleta.

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
- **URLs por directorios** (`/naming/`, `/hajime/`…), sin extensión.
- **Cada texto japonés nuevo obliga a regenerar el subset** de Zen Kaku. Ver
  README. **`document.fonts.check()` no sirve** para verificarlo: informa si la
  fuente está cargada, no si contiene el glifo.

---

## Flujo obligatorio antes de cada commit

Correr las guardas. **Si alguna falla, no commitear**: arreglar, o revertir al
último commit verde y avisar qué se revirtió y por qué. El objetivo es que todo
commit sea un punto de restauración seguro por construcción, no por suerte.

| Guarda | Cuándo | Costo |
|---|---|---|
| `python tools/check-ready.py` | siempre | instantánea |
| `python tools/check-modes.py` | siempre | ~40 s |
| `python tools/check-pendulum.py` | antes de push, o al tocar la física | ~2–4 min |

Las dos que usan navegador necesitan el sitio servido en `:8000`.

**Tags**: sólo en hitos. El próximo natural es cuando el andamiaje esté completo,
antes del pase de redacción.

---

## Cabos abiertos (lista viva)

- ~~Luz a lo largo del arco del péndulo~~ — **CERRADO**, no reabrir. No había
  problema. La métrica decía «70% del perímetro con ΔL bajo» y era cierto, pero
  no significaba lo que parecía: el cuerpo del cubie (lum ~11.5) es **más oscuro
  que el fondo** (15.3), así que todo perímetro sin iluminar falla por
  construcción — y un objeto más oscuro que su fondo se ve perfecto, se lee como
  silueta. Lo que desaparece es ΔL ≈ 0, no ΔL chico y consistente. Cerrado por
  inspección visual con una hoja de contactos de 8 poses cubriendo el arco real.
  Todo en `docs/mediciones/luz-arco.md`. **La pregunta era perceptual y binaria:
  si alguien sospecha que el cubo se pierde, se saca una captura, no un barrido.**

- **Móvil sin medir en dispositivo real.** Incluye: degradación del cubo, y que
  con escenario más alto que ancho manda el FOV horizontal, la cámara se aleja y
  queda aire vertical desperdiciado. El shader ya va a media resolución y 25 fps.
  El maelstrom táctil (escala + fundido, sin blur) tampoco se vio en un teléfono.
- ~~`favicon.ico` 404~~ — **CERRADO**. Hay `favicon.ico` (16/32/48), `favicon.svg`
  y `apple-touch-icon.png`, generados por `tools/make-favicon.py` a partir del
  mismo subset de la marca (言, oro sobre navy). Consola limpia.
- ~~Animación maelstrom~~ — **IMPLEMENTADA**, ver decisión cerrada arriba. Falta
  sólo verla en un teléfono real (arriba, con lo demás de móvil).
- **~70 placeholders `TODO`** pendientes de redacción.
- **Vista explotada del cubo: sin plan.** Mencionada como pendiente; no hay
  registro de que se haya discutido ni decidido nada al respecto.
- **`/naming/`**: los siete bloques están como andamiaje; falta el texto.

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
- **En headless el loop del cubo corre a ~7–15 ticks/s, no a 30.** Las pruebas
  de física tienen que esperar **por ticks, no por reloj**.
- **Un test roto se disfraza de bug de la página.** Si el JS de una guarda lanza,
  tiene que reventar el script, no devolver `undefined` en silencio.
