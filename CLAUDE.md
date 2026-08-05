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
- **La vista explotada del cubo está INTEGRADA acá (2026-08-05)**: el merge
  `cube-exploded` → `redesign-trust` lo decidió explícitamente el autor, tras
  dos verificaciones previas (móvil emulado y no-divergencia). Fue
  fast-forward sobre `0693216` — la rama venía rebaseada — con las cuatro
  guardas corridas DESPUÉS del merge. **La rama `cube-exploded` se borró**
  (local y origin): tras el fast-forward no tenía historia propia, y un
  puntero viejo se lee como trabajo pendiente que no existe. El registro
  completo de sus decisiones (las cinco tandas) está en la sección de la
  vista explotada, más abajo.
- **`main` no se toca**: publica kotodamafinance.com y todavía sirve la landing
  vieja. Nada de esto está publicado.
- El sitio es estático: sin backend, sin frameworks, sin build step.
- Último cierre: **2026-08-05, cuarta tanda del día: el bloque 5 de /musubi/
  («How the reading divides», texto del autor)** — la página pasó de cuatro a
  CINCO bloques. Las tandas anteriores del día: los kanji de las subcaras
  (太一 · 万 · 幽玄, con subset regenerado), la tarjeta de LibraryThing
  completa, y la redacción de las tres subpáginas de Hajime — **LA REDACCIÓN
  DEL SITIO ESTÁ TERMINADA.** **Árbol limpio y todo pusheado** en
  `redesign-trust`, con las guardas corridas (structure y modes en verde,
  pendulum en verde, **ready en `0`: LISTO PARA PUBLICAR** — ver el punto
  siguiente).
  *(Este bloque no puede nombrar su propio commit, así que siempre queda uno
  atrás: `git log -1 redesign-trust` es la respuesta exacta. El ancla fija que no
  deriva es el tag.)*
- **EL SITIO VOLVIÓ A CERO PLACEHOLDERS (2026-08-05) — la redacción terminó
  por segunda vez.** Los 16 que la revisión de quince puntos reintrodujo a
  propósito se redactaron todos con texto del autor: la línea de LibraryThing
  y las tres subpáginas de Hajime (5+5+5). **`check-ready` sale `0` — LISTO
  PARA PUBLICAR — y `2` vuelve a ser regresión**; el significado del código 2
  ya cambió TRES veces y la historia completa está en el docstring de
  `check-ready.py`. El baseline está en cero: cualquier placeholder que
  informe `check-structure` es un bug, no trabajo pendiente.
- **Ahora son CATORCE páginas**, no once: se sumaron las tres subpáginas de
  Hajime. El sitemap tiene 13 URLs (todas menos la 404).
- **NO queda ninguna decisión del autor pendiente.** Las dos últimas se
  cerraron el 2026-08-05: los kanji de las subcaras (**太一 Taichi · 万
  Yorozu · 幽玄 Yūgen**, dictados por el autor desde la tabla del cubo de su
  `context.md` — no localizable desde este repo: se copiaron literales de su
  mensaje, la misma regla de no inventar), y **el logo de LibraryThing, que
  ya está puesto**: va el archivo oficial EN SU PALETA ORIGINAL, sin alterar
  — criterio nuevo del autor que REVIERTE el monocromo en oro y DISUELVE el
  pendiente de permiso de marca (usar la marca tal cual se distribuye es lo
  que cualquier guía permite). Ver la decisión de tarjetas de perfil.

**Lo que dejó la última tanda (la revisión de quince puntos)**, todo integrado
en las decisiones de abajo: las anclas de la nav aterrizando con el layout ya
estable (la hidratación del cubo insertaba ~406px DESPUÉS del aterrizaje — se
arregló con la reserva del layout 3D en la carga, más `scroll-margin` para el
footer y el ancla `#cube-view` para «Back to the Cube»); el lazy-init que en
realidad no difería nada (el hero mide exactamente 100vh y tocar el fold cuenta
como intersecar — `rootMargin` pasó a `-1px` abajo); la costura cubo→About en
140px y el margen del hint en 12; la lista de fuentes de la portada sin japonés
y con el enlace centrado; la lista de /method/ con el japonés como línea
secundaria bajo el inglés; el footer a dos columnas sin «Platform», con la
bajada sin «Japan's» y sin el rótulo 免責事項; seis correcciones de texto que
des-anclan el proyecto de Japón como tema; los rótulos de vuelta por origen;
`user-select: none` en la grilla clip; y dos reportes que NO reproducían contra
el servidor (ayuda 3D con texto de grilla, subpáginas «descentradas») — otra
vez el patrón de la copia vieja en el navegador del autor.

**La tanda anterior** (mismo día): la rama `maintenance` con su generador y su
guarda; la regla de credenciales, escrita antes de que exista la primera; Zen
Kaku embebido en el cartel; y las dos declaraciones de procedencia de `/method/`
reducidas a una línea.

**Dos tags, y el segundo es el que importa ahora:**

- `v1-dark` — la versión navy+oro con el cubo Three.js, con registro visual en
  `docs/v1-dark/`.
- **`v1-content-complete`** — el sitio terminado de contenido, y **el punto de
  restauración de la migración de DNS**. Apunta a `fb38ffb`, que era el último
  estado verificado en verde al crearlo. **No se mueve** aunque el trabajo siga:
  ver la regla más abajo. Falta el tercero: la publicación, al mergear a `main`.

**Existe una rama `maintenance`, lista y NO activa.** No se ve desde acá y
ninguna de las cuatro guardas la mira; su decisión cerrada está más abajo.

### AL RETOMAR, EMPEZAR ACÁ

**Levantar el servidor en `:8000` y correr `python tools/check-structure.py`
—tiene que dar verde—.** Si da rojo, eso es lo primero: algo cambió fuera de
sesión.

**LO QUE FALTA ES SOLO INFRAESTRUCTURA.** El pase de redacción que la revisión
de quince puntos había reintroducido **terminó el 2026-08-05** (los 16, todos
con texto del autor), y `check-ready` sale `0`. El merge a `main` espera una
sola cosa: la migración de DNS (trabajo fuera de este repo, pasos 2–4 de
abajo).

**PASO 0 — HECHO. Ya se sabe dónde está el DNS**: **Namecheap BasicDNS**, con
los seis registros del `.com` documentados (cuatro `A` de GitHub Pages, el
`CNAME` de `www`, y el `TXT`/SPF del forwarding). **DNSSEC ya se desactivó**,
antes de transferir. El detalle vive fuera del repo.

**PASO 1 — HECHO (2026-08-04). iCloud+ ya corre en el DNS de Namecheap,
verificado por el autor: recibe y responde.** Con esto el correo dejó de
depender del forwarding de Namecheap, que era lo que moría al salir del
registrador — `contact@kotodamafinance.com` ya sobrevive a la transferencia, y
con él la única vía de contacto de la página de mantenimiento. El detalle de la
configuración vive fuera del repo, en el `.md` de infraestructura del autor.

**ORDEN VIGENTE — Y OJO, CAMBIÓ. Éste reemplaza al anterior**, que decía
transferir → correo → merge:

1. ~~Configurar iCloud+ en el DNS de Namecheap, y verificar que recibe y
   responde.~~ **HECHO.**
2. **Transferir el registro a Xserver.** Los nameservers **no** cambian con la
   transferencia. ← **EL FRENTE ACTIVO**
3. **Cargar la zona completa en Xserver y verificarla** consultando sus NS
   **directamente**, sin tocar todavía la delegación. Ojo: la zona a cargar
   ahora incluye los registros de iCloud+ (MX/SPF/DKIM), no los seis del
   inventario del paso 0 — el inventario vigente es el de después del paso 1.
4. **Recién ahí, cambiar los nameservers.**
5. **Merge a `main`** + tag de publicación. ~~El prerrequisito de redacción
   que dejó la revisión de quince puntos~~ **se cumplió el 2026-08-05**:
   `check-ready` ya sale `0`. Antes de mergear, releer «Antes de publicar»
   del README — son cuatro guardas, no una.

**Por qué el correo fue PRIMERO, que era el cambio de fondo.** El forwarding de
Namecheap **muere al salir del registrador**, y `contact@kotodamafinance.com`
está publicado en el sitio, en LinkedIn, en X y **en la propia página de
mantenimiento** — donde además es el **único** enlace que tiene. O sea que si el
correo se caía durante la obra, se caía junto con la única vía de contacto que
queda cuando el sitio está abajo. Por eso se resolvió antes de mover nada — y
quedó resuelto.

**Por qué 2, 3 y 4 están separados.** Que los nameservers no cambien con la
transferencia es lo que permite partirlo: se puede **cargar la zona en Xserver y
probarla contra sus propios NS mientras Namecheap sigue sirviendo el tráfico
real**. Así el único paso que mueve tráfico —el 4— se hace contra una zona ya
verificada, y deja de ser «cambiar y ver qué pasa». Cada paso se comprueba solo,
que es lo que hace el fallo diagnosticable.

**No es que el sitio no esté listo.** Está listo, y esa distinción importa: si
alguien retoma y ve el merge pendiente, la pregunta no es «¿qué falta escribir?»
sino «¿en qué paso del DNS estamos?».

La revisión legal del `免責事項` **no es un pendiente**: se decidió publicar sin
ella.

**No queda nada sin decidir** dentro del sitio. El `domain` de las tarjetas, que
era lo último, se cerró.

**Al llegar al paso 5 —el merge—, releer primero** la sección «Antes de
publicar» del README: son cuatro guardas, no una, y `check-ready` no mira el
comportamiento del cubo ni la física.

**Y durante toda la obra, la rama `maintenance` es la red.** Es lo que se
publica si hay que dejar el sitio abajo mientras se mueve el DNS; está lista y
se activa cambiando la rama de Pages. Su única vía de contacto es ese mismo
correo — la otra razón por la que el paso 1 fue primero, y con él hecho, la red
ya tiene el contacto asegurado.

### Cabos abiertos vigentes — el resumen corto

Ninguno bloquea publicar. Cada uno tiene su sección con el detalle.

| Cabo | Estado |
|---|---|
| ~~Redacción de Hajime~~ | **CERRADA 2026-08-05**: los 15, con texto del autor. Baseline en cero, `check-ready` en `0`. Cualquier placeholder nuevo es regresión. |
| ~~Logo de LibraryThing~~ | **CERRADO 2026-08-05**: va el archivo oficial en su paleta original, sin alterar — criterio nuevo que disuelve el pendiente de permiso (ver la decisión de tarjetas y `assets/img/README.md`). |
| ~~Kanji de Taichi/Yorozu/Yūgen~~ | **CERRADO 2026-08-05**: 太一 · 万 · 幽玄, del `context.md` del autor. Aplicados en h1 y `<title>` con el patrón de las caras; subset regenerado (太/幽/玄 eran nuevos). |
| **Móvil** | **nunca medido en dispositivo real.** Congelado por decisión del autor. Mediciones: la de escritorio, y la EMULACIÓN de la vista explotada (2026-08-05, `docs/mediciones/explotada-movil-emulada.md` — verde del lado CPU; no reemplaza al dispositivo real). |
| **Maelstrom** | apartado en `assets/css/maelstrom.css`, **no lo carga nadie** —ahora con guarda en `check-modes`—, reactivable. Al retomarlo, empezar por el **bug de la variante táctil** —definía keyframes sin blur y nunca los asignaba—, no por recalibrar. |
| ~~Vista explotada del cubo~~ | **INTEGRADA 2026-08-05**: mergeada a esta rama por decisión del autor, guardas en verde después del merge. Lo que sigue siendo posterior a publicar es la v2 (corrientes de agua) — sólo si el autor la pide. |
| **Dieta de fuentes** | **~79 KB disponibles** quitando features que el sitio no usa. **Decidido: no se hace ahora.** Se revisa si el CSS llega a usar `font-feature-settings`, `font-variant` o `small-caps`. |
| **Guarda de castellano** | **incompleta a propósito, y lo dice en su salida.** Cubre diacríticos y una lista de palabras; se le escapa castellano sin ninguna de las dos. Al agregar una página, leer su superficie además de correrla. |
| **Rama `maintenance`** | **existe, está lista y NO está activa.** Se activa cambiando la rama que publica Pages. Ver la decisión cerrada más abajo. |

---

## Decisiones cerradas — no rediscutir

### NINGUNA CREDENCIAL ENTRA AL REPO. Nunca.

Ninguna clave, token ni secreto se commitea. **Ni siquiera en un commit que
después se borra**: git guarda el historial, así que un archivo commiteado y
después ignorado **sigue siendo accesible**. Agregarlo al `.gitignore` no lo
saca de la historia — sólo evita el próximo.

**Y este repo es PÚBLICO, o sea que «se commiteó» equivale a «se publicó».** No
hay ventana entre una cosa y la otra: en cuanto el push termina, el objeto está
servido por GitHub y puede haber sido clonado, indexado o barrido por un bot que
justamente busca eso.

**Dónde van**: en variables de entorno, o en un archivo **ignorado desde el
primer día** —antes de escribirle nada adentro—. El `.gitignore` ya trae los
patrones típicos (`.env`, `*.key`, `*.pem`, `secrets.*`, `credentials.*`,
`*.token`), probados en las dos direcciones. **Pero eso es una red, no el
mecanismo**: sólo ataja el descuido de nombre previsible, y una key pegada
dentro de un `.py` cualquiera pasa igual.

**El error típico tiene nombre y es «sólo para probar».** Se pega la key en el
código para ver si el endpoint responde, con la intención de sacarla antes de
commitear. Cuando el commit sale, ya es tarde: lo único que queda por hacer es
rotarla. Si hace falta probar, la variable de entorno funciona igual de rápido.

**Va a importar pronto**, y por eso está escrito antes de que exista el primer
archivo: el pipeline de datos necesita la key de **不動産情報ライブラリ**
(solicitada desde abril de 2024), la de **J-Quants**, y las que vengan.

**SI PASA IGUAL, EL ORDEN ES: ROTAR PRIMERO, LIMPIAR DESPUÉS.** Y conviene tener
claro por qué, porque el instinto es al revés. Reescribir la historia
—`filter-repo`, `force-push`— **no des-publica nada**: lo que ya estuvo arriba
pudo haber sido copiado, y GitHub conserva objetos alcanzables por forks y por
la API un tiempo. La única acción que revoca el acceso de verdad es **invalidar
la credencial en el proveedor**. La limpieza del historial es prolijidad
posterior, reescribe commits, y **se decide con el autor** — nunca de oficio.

**Estado verificado al 2026-08-04**: se auditó el historial completo —78 commits,
todas las ramas y el tag— y **no hay ni hubo nunca** credenciales, `.env`,
`.ttf`, `_ref/` ni ningún archivo sensible. Ese cero es el punto de partida: de
acá en más, cualquier hallazgo es nuevo y hay que tratarlo como incidente.

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

### Encuadre de cámara ANISOTRÓPICO — esto REEMPLAZA a la esfera envolvente

**Cambió el 2026-08-04, a pedido del autor.** La esfera completa (`√3·S`) pagaba
~8 % de distancia por la pose de vértice arriba, que **es inalcanzable**: el
cubo no tiene roll (`rotation.z` siempre 0, order `'YXZ'`), y como `ry` no
cambia la coordenada vertical, la altura máxima real es `√2·S` — arista arriba,
`rx≈45°`. Fórmula vigente, en `frameCamera()`:

```
d_vertical   = M · S · (√2/tan(halfV) + 1)
d_horizontal = M · √3·S / sin(halfH)
camera.z     = max(d_vertical, d_horizontal)
```

Sigue siendo una **garantía geométrica, no un ajuste empírico**, y cubre TODAS
las rotaciones alcanzables: péndulo, snap (`rx=±90`) y **arrastre manual sin
acotar**. El hallazgo que salió del cálculo: restringir al arco del péndulo
**no ganaba nada** — el máximo vertical está en `rx=45°` y el arco llega a 44°,
o sea que ya contiene el peor caso. Por eso **cambiar `PEND_AMP` no invalida el
encuadre**; lo único que lo invalida es **introducir roll**, y ese día vuelve
la esfera (`√3·S/sin(min(halfV,halfH))`). Está anotado en `frameCamera()`.

**«Con seno, no tangente» ya no es la regla entera**: la vertical va con
tangente A PROPÓSITO (acota un punto concreto — la arista más alta, a radio S
del eje, cuyo peor azimut la acerca S a la cámara: de ahí el «+1»), y la
horizontal sigue con seno (radio de revolución, `ry` libre). Quien "corrija" la
tangente a seno aleja la cámara sin ganar nada.

Verificado con barrido de 360 poses: cero recortes, margen mínimo **17 px**
exactamente en el peor caso teórico. Efecto en la portada: el cubo pasó de 442
a **483 px** de alto (71 % → 78 % del canvas). El aire restante (~137 px) es la
reserva para las poses de arista arriba, que el arrastre sí alcanza — no es
recortable por encuadre. Números y condiciones en `docs/mediciones/encuadre.md`.

**Manda la condición más exigente de las dos**: en apaisado la vertical, en uno
más alto que ancho la horizontal. Es la misma variable que queda sin medir en
móvil, donde el escenario cambia de proporción.

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

Va con **`rootMargin: '0px 0px -1px 0px'` — margen NEGATIVO abajo — y el signo
es la corrección de una premisa que resultó falsa.** Este archivo decía «la
sección arranca ~20px debajo del fold, con margen 0 no interseca en la carga» —
y ya no era cierto: el hero mide **exactamente** `100vh`, la sección del cubo
**toca el fold en la carga**, y para el observer dos rects que comparten el
borde **intersecan**. Medido en la tercera tanda del 2026-08-04: con margen
`0px` el canvas existía antes de scrollear — el lazy-init no difería nada y
nadie lo había notado, porque ninguna guarda miraba el estado pre-hidratación.
El `-1px` encoge el viewport observado lo justo para que tocar el borde no
cuente. **Si alguien "mejora" esto agregando un `rootMargin` positivo generoso,
desactiva la optimización entera sin que se note** — y ahora `check-modes` sí
lo nota, porque mide que el canvas NO exista antes del scroll.

**Y EL LAYOUT DEL MODO 3D NO ESPERA A LA HIDRATACIÓN — es otra decisión, y
protege las anclas.** `main.js` reserva en la carga el layout 3D completo
(`setView('3d')`: escenario vacío con su alto de CSS, toggle visible y cableado,
grilla recortada, ayuda de 3D). Sin la reserva, el escenario y el toggle
aparecían recién al resolver el import de Three.js e insertaban **~406px + 59px
de alto ARRIBA de `#about`/`#method`/`#footer` DESPUÉS de que el ancla
aterrizara** — los destinos de la nav quedaban corridos exactamente eso, y
`scroll-margin-top` no puede arreglar un destino que se mueve después del
aterrizaje. Lo diferido sigue siendo lo caro (crear el contexto WebGL); lo que
se adelanta es sólo la geometría de la página. Si la hidratación falla, el
`catch` revierte a la grilla y esconde el toggle. `check-modes` verifica que la
altura del documento sea estable al hidratar, midiendo ANTES y DESPUÉS — con
detección de verde vacío si la medición pre-hidratación llega tarde.

**Tres reglas que la reserva arrastra, cerradas al día siguiente de escribirla**
(auditoría instrumentada + análisis adversarial, mismo día):

- **La hidratación re-aplica el modo VIGENTE, no `'3d'` fijo.** El toggle está
  vivo desde la reserva, así que el usuario puede elegir la grilla mientras el
  import de Three.js resuelve — y el `setView('3d')` incondicional de la
  versión inicial le pisaba la elección. `stage.hidden` es el modo. Verificado
  con red a 40KB/s: la elección sobrevive al import.
- **`initCube` devolviendo null se trata como fallo (throw)**: con la reserva
  puesta, el `return` silencioso de antes dejaba el escenario visible y VACÍO
  para siempre, sin catch y sin reintento. Hoy es camino muerto (initCube o
  devuelve el cubo o lanza), pero la semántica de fallo tiene que ser segura
  por defecto.
- **El camino de fallo se EJECUTA en la guarda, no se lee**: `check-modes`
  fuerza la hidratación a fallar (cube.js bloqueado por CDP) y verifica el
  estado del fallback completo, y además lee la ayuda ANTES del scroll — el
  momento que un usuario ve primero, que ninguna otra comprobación cubría.
  Las dos probadas en rojo con `main.js` mutilado antes de confiar en su
  verde (sin el bloque del hint: 3 fallas; sin la reversión del catch: 4).

**EL FINGERPRINT DE UN `main.js` VIEJO EJECUTANDO** (para el diagnóstico
DOM-contra-red): `15edc84` hizo DOS cosas a la vez — agregó la escritura del
hint a `setView()` Y cambió el baseline del HTML al texto de grilla. Un
`main.js` anterior corriendo contra el HTML vigente da **cubo 3D funcional con
el hint de grilla congelado**, sin ningún error de consola: el síntoma exacto.
La prueba de un segundo, desde la pestaña afectada: **alternar Grid↔3D con el
toggle — si el texto de la ayuda no cambia, el módulo ejecutado es
pre-`15edc84`**. Y ojo con el instrumento: `fetch(..., {cache:'reload'})` mide
la RED, no el módulo EJECUTADO — un module script se evalúa una vez por
documento (module map), y la caché heurística de Chrome (sin `Cache-Control`,
el 10% del Last-Modified) puede servir el módulo viejo aun tras un F5, porque
desde 2017 el reload normal sólo revalida el documento principal. El que
delata al módulo ejecutado es
`performance.getEntriesByType('resource')` sobre main.js (`transferSize: 0` =
salió de caché) y `performance.timeOrigin` (¿la pestaña cargó antes del push?).

### Las anclas aterrizan con el layout ya estable — y cada destino tiene el suyo

Cerrado en la revisión de quince puntos (2026-08-04):

- **`scroll-margin-top: calc(var(--nav-h) + 12px)`** (= 96px) sobre `section`,
  **`footer`** y `.cube__layout`. El footer va listado aparte porque no es
  `<section>` y era el único destino de la nav sin margen — Contact aterrizaba
  con la marca tapada por la nav fija. La nav real mide 63px (medida, no
  asumida); el resto es respiro.
- **«Back to the Cube» apunta a `/#cube-view`** (el ancla de `.cube__layout`),
  no a `/#cube`: quien vuelve ya leyó la introducción, y aterrizar en el título
  dejaba el cubo 57% visible. La nav sigue apuntando a `/#cube` — quien llega
  por primera vez necesita el contexto. Verificado: cubo 100% visible a
  1440×900; a 1280×720 se recorta un 4% del canvas que cae en el aire del
  encuadre, el cubo dibujado entra entero.
- La condición que hace que todo esto funcione es la **reserva del layout 3D**
  (ver la decisión del lazy-init): sin altura estable, el destino se corre
  después del aterrizaje y ningún scroll-margin lo salva.

### Rótulos de vuelta según el ORIGEN — criterio cerrado

Las páginas que se abren **desde el cubo** vuelven al cubo; las que se abren
desde otro lado vuelven a donde se llega. Concretamente: las seis caras →
«Back to the Cube» (`/#cube-view`); las tres subpáginas de Hajime → «Back to
Hajime» (`/hajime/`); `/musubi/`, `/method/`, `/disclaimer/` y la 404 →
«Back to the start» (`/`). Antes había cuatro rótulos distintos apuntando a
cuatro lugares sin criterio común («Back to the method summary», «Back to
Kotodama Finance»…).

### El footer quedó en dos columnas — la «Platform» se fue

Enlazaba a The Cube y Method: dos de cinco secciones, las dos ya presentes en
la nav. Una selección arbitraria que duplica navegación no orienta. El footer
es marca + bajada, «Reach us» y «Follow» — y la bajada dice «Where economic
currents become visible», sin «Japan's»: el motor es global y Japón es el
primer nodo, no el tema (la misma corrección de la revisión que pasó por el
About, /sugao/ p3 y /kizuna/ p2).

### Las tres subpáginas de Hajime son ANDAMIAJE deliberado

`/hajime/taichi/` (macro), `/hajime/yorozu/` (sectorial), `/hajime/yugen/`
(transparencia). Estructura de cara —línea de función + lead + un párrafo—,
**ya redactadas (2026-08-05) con texto del autor, tal cual lo dictó**: «The
macro picture» / «Sector by sector» / «Public money», descriptions derivadas
del texto. Los tres nombres de `/hajime/` pasaron de `<i class="name">` a
**enlaces** (`a.name`, oro y subrayado suave): eran lo único del sitio que se
destacaba sin llevar a ninguna parte.

Dos compromisos del texto que NO son redacción libre, anotados en los HTML:

- **«This is not a watchdog» (Yūgen) es un COMPROMISO del autor**, no una
  negación de relleno: su `context.md` define esa cara como contemplativa,
  no watchdog. No se saca por parecer innecesario — fija el límite de lo que
  esa línea de trabajo hace.
- **El cierre de Taichi («the parts only mean something against the whole»)
  rima A PROPÓSITO con el subtítulo de /musubi/ («Nothing means anything
  alone»)**: el mismo principio bajando a una cara. Dos copias deliberadas
  sin guarda que las compare — si se redacta una, mirar la otra. Anotado en
  los dos lados, igual que las frases del cubo.

- **Los kanji se cerraron el 2026-08-05** — esto reemplaza el «sin kanji a
  propósito» que decía acá: **太一 Taichi · 万 Yorozu · 幽玄 Yūgen**, dictados
  por el autor desde la tabla del cubo de su `context.md` (el archivo no está
  en esta máquina; se copiaron literales de su mensaje — la misma regla de no
  inventar, con otra fuente). En h1 y `<title>`/`og:title` con el patrón de
  las seis caras: kanji grande + romaji al lado, la línea de función debajo,
  sin gloss traducido. Entraron con regeneración de subset: **太/幽/玄 eran
  nuevos; 一 y 万 ya estaban** (一次資料, 百万円). Verificado contra cmap con
  猫 de control de ausencia; features y conservados intactos.
- **Los enlaces de /hajime/ quedaron en ROMAJI SOLO, y es decisión, no
  falta**: dentro de la oración inglesa, el kanji junto al romaji sólo
  duplicaría el nombre de al lado — la prueba exacta del japonés ornamental.
  El kanji vive donde el nombre se presenta como título (h1 y `<title>` de la
  subpágina), igual que las seis caras: ninguna mención en prosa del sitio
  lleva kanji. Anotado junto a los enlaces en /hajime/.
- **La guarda de castellano exime el texto que EMPIEZA con «TODO»** — se agregó
  en esta tanda, porque los placeholders son castellano deliberado (regla de
  este archivo) y la guarda los habría marcado: era una regla del proyecto
  peleando contra otra. La exención es angosta: castellano sin esa marca sigue
  siendo hallazgo.
- **En /musubi/ los nombres `.name` NO enlazan, y no hay que "emparejarlos"**
  — ahora son nueve, con dos razones que no hay que mezclar: los seis del
  marco no tienen página (enlazarlos prometería páginas que no existen), y
  los tres de Hajime del bloque 5 SÍ la tienen pero ahí se presentan como
  sistema conceptual, no como destinos. Está anotado en el HTML de /musubi/,
  en el de /hajime/ y en el CSS de `a.name`.

### La tanda tipográfica y de logos del 2026-08-05 — seis pedidos del autor

- **Escala global al 112.5% (18px de raíz)** — el cuerpo se veía chico. Todo
  el sitio mide en rem, así que es UNA perilla y la escala relativa se
  conserva. **Las columnas de prosa pasaron de px a rem** (45rem la
  subpágina, 47.5 el About, 55 el hero, 70 los marcos de método y footer):
  en px no acompañaban a la letra y agrandar la fuente no reducía el vacío
  lateral, que era el efecto buscado. OJO con el hero: su caja estaba en px
  por una razón medida (el corte por dos píxeles del titular) y en rem esa
  garantía escala CON el titular — está anotado en el CSS. El cubo y su
  `--maxw` NO se tocaron.
- **Títulos de las 13 subpáginas al DOBLE y CENTRADOS** (cabecera entera:
  eyebrow, título, gloss; el lead y el cuerpo siguen a la izquierda). El
  romaji NO se duplicó exacto (tope 2rem→3.4rem): duplicado quedaba gigante
  al lado del kanji — la pareja equilibra con el romaji ~0.45 del kanji. La
  frase de la 404 subió acotada por ancho (verificado: una línea).
- **«Read the full method →» al pie de la COLUMNA IZQUIERDA** — REVIERTE el
  centrado bajo las dos columnas; como hijo de `.method__how` no se estira
  al fondo de la columna de fuentes.
- **El aire tras los enlaces de /hajime/**: el espacio SIEMPRE estuvo
  (4,5px de avance, medido) — la cursiva de `.name` es OBLICUA SINTÉTICA
  (Inter no carga itálica) y la última letra pintaba sobre el espacio.
  Margen de 0.14em, no padding (el padding estira el subrayado). 7,6px
  después, medido.
- **Logos de las fuentes de la portada: SÓLO LA FSA** (su símbolo oficial,
  transparente, byte-idéntico — mismo criterio LibraryThing). **Las otras
  cuatro filas SIN logo y NO es olvido**: BOJ sólo publica fondo opaco
  (limpiarlo = alterarlo, prohibido), EDINET no tiene logo, bis.org rechaza
  conexiones desde acá, Damodaran es página personal sin marca. **Que nadie
  lo "complete" con SVGs de Wikipedia**: no son el archivo oficial. Detalle
  en `assets/img/README.md` y en el HTML de la portada.
- **El © del footer QUEDA** — aclarado por el autor: © es copyright del
  contenido (existe sin registro); marca registrada sería ®/™. Sin cambios.
- **Pendiente del autor: su veredicto sobre las capturas** (títulos al
  doble y cuerpo a 18px — «mostrame antes de fijarlo»). Está commiteado
  como estado vigente para que el árbol quede verde; si pide otro tamaño,
  son dos clamps y una perilla.

### Tarjetas de perfil en /sugao/ — completa: logo oficial sin alterar y texto

El registro de perfiles personales va en **tarjetas** desde ya, aunque haya una
sola (LibraryThing): un enlace suelto sirve para uno, no para los cinco que
vienen (IMDb, MyAnimeList, Steam, GitHub). **Fila que envuelve con ancho fijo
(232px), no grilla auto-fill**: la grilla estiraría la tarjeta única al ancho
completo como un banner. **Sin slots vacíos ni «próximamente»**. La tarjeta
entera es el enlace. El LinkedIn del perfil profesional NO se convierte en
tarjeta: es credencial de esa sección, no parte del registro.

**EL LOGO VA EN SU PALETA ORIGINAL, SIN ALTERAR — criterio fijado por el
autor (ago 2026), y REVIERTE el «monocromo en oro, silueta con
`fill=currentColor`» que decía acá.** El motivo del cambio: recolorear la
marca de otro es apropiársela; los logos de instituciones ajenas se muestran
como ellas los publican. El costo aceptado es que entren colores ajenos a la
paleta navy/oro, y **lo controla el TAMAÑO (26px, un sello, no una mancha),
no el recoloreo**. Aplica también a los cuatro que vienen. Quien encuentre la
instrucción del oro en el historial: la vigente es ésta, no hay que
"corregirla" de vuelta.

**Y el cambio de criterio DISUELVE el pendiente de permiso de marca**: los
términos siguen ilegibles por vía automatizada (403 en /press y /topic/45089),
pero usar el archivo oficial tal cual se distribuye es exactamente lo que
cualquier guía de marca permite — eso es lo que hace el uso defendible sin
haberlos leído, y está anotado en `assets/img/README.md`, al lado del archivo.

Lo puesto, verificado midiendo (2026-08-05): `flat-logo-rounded_1024w.png`
oficial, byte-idéntico al original (sha256 comprobado), en
`assets/img/librarything-flat-logo-rounded_1024w.png`. **El SVG oficial NO
sirve** — dibuja la L como `<text>` con una tipografía que el visitante no
tiene (análisis del autor, anotado en el README de img). Esquinas del PNG ya
transparentes (alfa 0, medido); sobre la tarjeta: anillo exterior sin halo
(delta de luminancia 0.0 contra el fondo), esquinas a +1,9 unidades (el
antialias del redondeo — bajo el umbral de 3 unidades sRGB que este proyecto
ya fijó como invisible), centro exacto `#553B39`, nítido a @2x (1024px de
origen para 52px de dispositivo). El `alt` va **vacío a propósito**: el
nombre «LibraryThing» está al lado y un lector de pantalla lo diría dos veces.

**El texto de la tarjeta es del autor y va tal cual: «My Library at Home»**,
con esas mayúsculas. No se ajustó al patrón en minúscula de los descriptores
de las seis tarjetas del cubo porque ése es otro sistema (dominios comprimidos
que se leen entre seis); `.profile-card__what` no tiene hermanos todavía, y en
mayúsculas se lee como el nombre propio de la colección — el registro justo
para esta tarjeta. Con esto **/sugao/ quedó en cero placeholders** y el
baseline bajó a 15.

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

**EL ARCHIVO DE REFERENCIA QUEDÓ ATRÁS EN LOS TRES CAMPOS.** Ya no queda nada de
Sugao que se copie literal de ahí:

| Campo | Referencia | Vigente |
|---|---|---|
| `gloss` | «the true face» | **«The person behind the platform»** |
| `status` | «Intro live · profiles deferred» | **«Live»** (`active`) |
| `domain` | «The human behind» | **«The person behind»** |

O sea que para esta cara **la regla de copiar literal del archivo de referencia
ya no aplica**: manda lo redactado. Vale la pena tenerlo presente antes de
"restaurar" un campo desde la referencia creyendo que se corrige una deriva —
y lo mismo vale para las otras cinco, ver la tabla de `domain` más abajo.

### La rama `maintenance` existe, está lista y NO está activa

Un cartel para bajar el sitio a propósito durante una obra grande. **Rama
aparte**, huérfana, con cuatro archivos: `index.html`, `404.html` idéntico,
`CNAME` y `.nojekyll`. Se activa **cambiando la rama que publica GitHub Pages**
y se revierte igual — el sitio y `main` no se tocan en ningún momento. El
procedimiento completo está en el README.

**Que exista es justamente lo que hay que recordar**: no se ve desde `main` ni
desde `redesign-trust`, no aparece en el árbol de trabajo, y ninguna de las
cuatro guardas la mira. Un cartel de mantenimiento que nadie recuerda que existe
se reescribe desde cero el día que hace falta, que es el peor día para hacerlo.

**Tres cosas que parecen detalles y no lo son:**

- **La rama lleva `CNAME`, y por eso son cuatro archivos y no dos.** Cuando
  Pages publica una rama sin `CNAME`, **da de baja el dominio propio**, y
  reponerlo obliga a reaprovisionar el certificado HTTPS. Eso pasaría con el
  sitio ya caído. El `.nojekyll` es por lo mismo: que Pages suba archivos en vez
  de correr un build que no hace falta y puede fallar.
- **Los dos HTML son el MISMO blob.** La raíz sirve el cartel y cualquier otra
  ruta cae en el 404, que dice lo mismo; no hay que replicar las once carpetas.
  Si se separan, la portada dice una cosa y el resto otra.
- **La rama se GENERA con `tools/make-maintenance.py`, no se edita.** El script
  escribe la rama con plumbing —sin checkout, sin mover `HEAD`—, así que corre
  con el árbol en cualquier estado. Ésa es la respuesta a «copiar el woff2 queda
  viejo / mantener uno propio duplica el trabajo»: **un artefacto derivado no se
  mantiene, se regenera**, igual que el sitemap, la og-image y los favicons.

**ZEN KAKU VA EMBEBIDO** — micro-subset de 1,46 KB con los siete glifos, dentro
del HTML. Verificado: los cinco del titular y los dos del logo se dibujan con
Zen Kaku Gothic New Medium, una sola cara. Se embebe porque **ésta es la página
que se muestra cuando algo salió mal**, y ahí que se vea distinta en cada máquina
es lo peor que puede pasar.

**守, 作 y 中 viven en el subset del SITIO aunque ninguna página los use**, y eso
no se poda: el generador de la rama sólo puede leer archivos del repo, así que si
leyera la TTF de origen —no versionada, a propósito— la rama dejaría de poder
regenerarse en otra máquina. Cuestan 0,3 KB. Es el mismo trato que 立方体 y
一次資料, reservados para /ja/, y la fórmula de derivación los preserva sola.
Está anotado en el `@font-face` de `styles.css`.

**EL HALLAZGO SIGUE VALIENDO AUNQUE EL PROBLEMA ESTÉ RESUELTO, y es lo que hay
que recordar: copiar el subset del sitio a la rama NO habría dado tofu.** Al
subset le faltaban tres de los cinco glifos del titular, pero el fallback de
fuentes es **por glifo**, así que el titular se dibuja entero y se ve bien.
Medido con `CSS.getPlatformFontsForNode`: `'Zen Kaku', sans-serif` daba
**2 glifos Zen Kaku + 3 Microsoft YaHei** — un titular en dos tipografías, una de
ellas **china**, que pasa cualquier inspección visual. Y `lang="ja"` **no es
decoración semántica**: con él el genérico cae en Noto Sans JP, sin él en
Microsoft YaHei; sigue puesto como red por si el `@font-face` no cargara.

`JA_EMBEBIDO` en el generador **no adivina**: si falta un glifo aborta
nombrándolo, precisamente porque la versión rota se ve bien.

**La guarda propia es `tools/check-maintenance.py`, y corre A DEMANDA** — al
tocar la rama y **antes de activarla**, no en cada commit. Las cuatro guardas
siguen siendo cuatro: ésta mira una rama que no cambia entre commits, así que
en el flujo de siempre sería ruido. Probada en las dos direcciones, con cuatro
ramas rotas armadas al lado.

### La vista explotada del cubo — INTEGRADA; la historia de sus decisiones

**Se desarrolló en la rama `cube-exploded`** (creada el 2026-08-05 desde
`6de21bd`, por instrucción del autor) **y se INTEGRÓ acá el 2026-08-05, por
su decisión explícita**, con dos verificaciones previas: la medición emulada
de móvil (`docs/mediciones/explotada-movil-emulada.md`) y la no-divergencia
(merge-base = punta de `redesign-trust`: fast-forward). **La rama se borró
después del merge** — sin historia propia tras el fast-forward, un puntero
viejo sólo invita a creer que hay trabajo pendiente ahí.

**Las condiciones bajo las que se trabajó** (cumplidas, quedan como registro
del método): `redesign-trust` intacta con las correcciones del sitio yendo
ahí y la rama rebaseándose encima — nunca al revés—; el merge como decisión
explícita de Manuel, no por estar «casi»; y las guardas corriendo igual en
la rama — `check-pendulum` verde en cada tanda.

**Qué es (primera versión, SIN corrientes de agua — van después si ésta
funciona; no se compensa la ausencia con otro efecto):** el cubo se abre a un
caparazón esférico —los 26 cubies viajan a un RADIO COMÚN, no en línea recta:
en línea recta el resultado es un cubo grande y hueco, porque las esquinas
siguen más lejos que los centros— con el núcleo en el centro: esfera de vidrio
dorada (transmission REAL: el vendor es **r160**, no el r128 que circulaba en
papeles — leído de REVISION en three.module.js). Clic en el núcleo →
/musubi/, único clicable explotado.
El control es el pie del cubo: «Explode the Cube» ↔ «Reassemble the Cube»
reemplaza al enlace «The idea behind the cube →» en modo 3D (decisión del
autor; el `<a>` queda en el HTML como capa sin JS y vuelve en modo grilla y en
el fallback). Explotar limpia la selección y cierra el folio; las caras dejan
de ser clicables; pasar a grilla rearma al instante; reduced-motion salta al
estado final sin transición y sin pulso (verificado midiendo, no leyendo).

**Correcciones del autor sobre la v1 (2026-08-05):**

- **Los kanji van EN LA SUPERFICIE de la esfera, no como sprites orbitando** —
  revierte la elección de la v1. La objeción que motivó los sprites (una
  textura clavada a la esfera se va de vista media órbita con el péndulo) se
  resuelve de otro modo: el péndulo no gira el núcleo; quien gira es el
  CASCARÓN de palabras, sobre su propio eje, lento (~35 s/vuelta) e
  independiente — las palabras desfilan y se leen todas, por turnos.
- **Explotado se esconden la ayuda y el toggle — visualmente**: la ayuda con
  `visibility` (conserva su caja: nada se mueve bajo el cursor), el toggle
  con `opacity`+`pointer-events` para que SIGA en el árbol de accesibilidad
  y reaparezca con `:focus-within` — la salida de teclado queda.

**Segunda tanda (2026-08-05, tras la calibración en vivo del autor) — REVIERTE
tres puntos de la primera; lo vigente es esto:**

- **Radios fijados: `EXPLODE_R` 5.0 y `CORE_R` 0.5** (antes 4.2/0.72).
  Caparazón bien abierto y núcleo chico es el punto donde se lee como plasma
  globe: a 5.0 las caras se agrupan menos que a 4.2, y el autor prefiere
  errar del lado del globo. `?explodeR=` y `?coreR=` siguen para recalibrar.
- **El material y el pulso VOLVIERON a la v1, tal cual** (emisiva 0.16→0.26,
  ±1.5% de escala). El boost de la primera tanda (0.10→0.55, ±3%) se probó,
  se MIDIÓ —el vaivén pasó de 34 a 73,9 unidades sRGB, senoidal limpio— y el
  autor lo DESCARTÓ por costo visual: con la emisiva alta la esfera dejaba
  de leerse como vidrio. **QUE EL PULSO NO SE PERCIBA ESTÁ BIEN**: el vidrio
  vale más que el pulso, y no se compensa por otra vía (ni escala, ni color,
  ni keyframes). Que nadie lo "arregle" de vuelta.
- **La tinta de los kanji dejó el navy** — daba contraste pero ensuciaba la
  esfera y rompía el sistema de color; el contraste tiene que salir del
  TEXTO. En esta tanda se fue al bronce oscuro (`#6b4906`, delta 39,9), y
  **la TERCERA tanda lo REVIRTIÓ**: fue interpretación equivocada de
  «dorado duro» — ver abajo, donde está la dirección vigente.
- **Los kanji, proporcionalmente MÁS chicos**: el factor de la textura bajó
  de 0.24 a 0.19, ADEMÁS del arrastre del núcleo (0.72→0.5 ya los achicaba
  solo).

**Tercera tanda (2026-08-05) — el modelo de expansión y el sentido de la
tinta:**

- **El RADIO COMÚN puro se quedó corto y el modelo pasó a ser INTERPOLADO.**
  La instrucción original del autor pedía radio común, y él mismo la
  corrigió al verla a 5.0: los centros de cara, que parten más cerca del
  centro, viajan DE MÁS y sobresalen del globo (a 2.6-4.2 no saltaba).
  `EXPLODE_MIX` (`?explodeMix=`, 0 radial - 1 común) mezcla los dos
  extremos, **normalizado por la ESQUINA**: a cualquier mix las esquinas
  terminan en `EXPLODE_R` y el factor sólo decide cuánto se meten centros y
  aristas — calibrar no cambia la silueta. **Default 0.65, del barrido
  capturado**: a 0.5 todavía se lee grilla cúbica, a 0.8 el centro superior
  ya se despega del arco.
- **La tinta es ORO LUMINOSO: más clara y más saturada que la esfera, no
  más oscura.** «Dorado más duro» significaba un oro que RESALTE brillando,
  no hundiéndose — la serie bronce (deltas −20,7/−30,0/−39,9) se midió y se
  descartó entera. Serie luminosa medida con el mismo método de máscara de
  diff: `#ffd24a` +14,2 (el más saturado y más oro) · `#fae59a` +21,9 ·
  `#fdf3cf` +27,2 (roza el techo: se lee blanco). El default fue `#fae59a`
  y **la cuarta tanda lo movió a `#ffd24a`**: el autor vio la E demasiado
  blanca. **El techo es regla**: si el trazo llega a blanco deja de ser
  dorado. Los deltas luminosos son más chicos que los del bronce porque el
  tone mapping comprime arriba — y aun así se leen mejor: en polaridad
  positiva el trazo brilla.

**Cuarta tanda (2026-08-05) — la medición de la silueta, y tres ajustes:**

- **La medición que pidió el autor, con veredicto.** (a) **No hay bug**:
  las posiciones de los 26 coinciden con la fórmula con error 0, en mix
  0.2/0.65/1.0. (b) La hipótesis óptica se confirma con un matiz: los
  centros NO proyectan más silueta que el resto (tamaño proyectado 70-95 px
  en las tres clases) — sobresalen **LOCALMENTE**: en la pose de carga el
  centro superior queda **+31 px por encima del arco de sus vecinos
  angulares**. Y el mix nunca pudo arreglarlo porque ese eje mueve centros
  y aristas JUNTOS: el exceso relativo casi no cambia — era el eje
  equivocado, como sospechó el autor. (c) **ACERCAR sólo los centros
  funciona; ACHICAR no**: a 0.85·R el peor exceso local queda en −5,6 px y
  el contorno de píxeles no muestra bulto en poses adversarias; achicados
  al 78% el exceso sigue en +25 px — lo domina la distancia del centro, no
  el tamaño del cubie. Y un aviso de método: la métrica de ventana angular
  (±30°) dio un +47 FALSO en una pose, midiendo contra un hueco sin
  vecinos de anillo — **el árbitro es el contorno de PÍXELES** (ahí: meseta
  de 231 px contra arcos de 240-250, sin bulto).
- **PROPUESTA que la quinta tanda APROBÓ E IMPLEMENTÓ** (ver abajo): los
  20 del anillo (esquinas y aristas) al radio pleno, los 6 centros a
  ~0.85·EXPLODE_R con parámetro de URL — y EXPLODE_MIX retirado, porque
  quedó medido que ese eje no arregla el bulto.
- **El giro de los kanji se INVIRTIÓ** (desfile derecha→izquierda: signo
  negativo en WORD_SPIN) y la velocidad quedó calibrable EN VIVO con
  `?wordSpin=` (segundos por vuelta), **default 18** — el ~35 s original
  era demasiado lento para el autor. Verificado midiendo: centroide de la
  tinta −50 px en 2,5 s, glifos sin espejar. La legibilidad en movimiento
  la juzga el autor en vivo, no una captura.
- **La tinta quedó en D `#ffd24a`** — la E resultó demasiado blanca.
  **ORO SOBRE CONTRASTE**, criterio del autor: D es la que se lee como oro
  puro, y +14,2 de delta alcanza porque en polaridad positiva el trazo
  brilla sobre la esfera.

**Quinta tanda (2026-08-05) — la propuesta aprobada, y los valores del
autor:**

- **El modelo de silueta quedó IMPLEMENTADO** (aprobación explícita del
  autor): anillo —esquinas y aristas— al radio pleno, los 6 centros de
  cara a `CENTER_F`·R (`?centerF=`, default **0.85**, el valor medido).
  **`EXPLODE_MIX` SE RETIRÓ**, con la anotación en cube.js para que nadie
  lo reponga creyendo que falta: interpolaba radial↔común para los 26 a la
  vez y quedó medido que no arregla el bulto — una perilla que no hacía lo
  que prometía. Y la aparente contradicción, cerrada por el autor: el
  modelo vigente parte del extremo mix=1 (radio común) y corrige sólo los
  centros — retirar la perilla no contradice haber elegido ese extremo
  como base.
- **Valores elegidos EN VIVO con el modelo nuevo**: `EXPLODE_R` **5.5** y
  `CORE_R` **0.7** — reemplazan 5.0/0.5, que se habían elegido con el
  radio común puro. Caparazón un poco más abierto, núcleo algo más grande.
- **`wordSpin` default 24 s** — probado en vivo contra 18 y 12: a 24 el
  desfile deja leer sin apurar.
- **La tinta D `#ffd24a`, CONFIRMADA** en vivo: se lee como oro, no como
  blanco. Sin cambios.

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

**`/disclaimer/` SE PUBLICA SIN REVISIÓN DE UN PROFESIONAL LEGAL JAPONÉS, POR
DECISIÓN DE MANUEL.** Esto **revierte** lo que decía este archivo antes, que
pedía revisión de un benrishi o abogado antes de publicar a `main`.

**Fue decisión, no olvido**, y conviene que quede así de explícito porque el
rastro invita a pensar lo contrario: hubo una marca `BORRADOR-SIN-REVISION-LEGAL`
en el HTML y una comprobación en `check-ready.py` que bloqueaban la publicación,
y **las dos se retiraron a propósito**. Quien las encuentre en el historial y
crea que se perdieron algo, no: se sacaron cuando la espera terminó.

**Lo que sostiene la decisión es el marco legal que verificó Manuel** —no una
evaluación mía, que no estoy en posición de hacer—:

- **La FIEA no aplica**: el sitio no da asesoría de inversión bajo contrato ni
  emite recomendaciones. Es la línea que separa publicar análisis de operar como
  asesor registrado, y el proyecto se mantiene del lado de publicar.
- **El 景表法** (representaciones engañosas) **queda cubierto por el principio de
  rigor de fuentes**: toda cifra sale de fuente primaria y es trazable al
  documento. Ahí el rigor no es sólo método editorial, también es la defensa.

Las dos cláusulas donde un texto sin revisar puede no sostener lo que promete
—ley aplicable y limitación de responsabilidad— siguen declaradas y siguen sin
validar por un tercero. **Eso se asumió con la decisión.** Si alguna vez cambia
el alcance del sitio —asesoría, recomendaciones, cualquier cosa bajo contrato—
esta decisión hay que reabrirla, porque el marco que la sostiene deja de aplicar.

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

**Y `kf-rise` TAMBIÉN CORRE AL VOLVER CON EL BOTÓN ATRÁS**, que es el dato que
faltaba y el que explica por qué se confunde. Medido: entrar a una cara no anima
nada —en `/hajime/` sólo late `kf-pulse` en un punto de estado—, pero al volver
a la portada el hero sube y aparece durante 1,3 s. O sea que **lo único que se
parece a una transición de página aparece justo después de una navegación**, que
es exactamente cuando uno la atribuye a la transición. Si alguien reporta que
«el maelstrom sigue corriendo», éste es el primer candidato y se distingue en un
segundo: el maelstrom giraba y desenfocaba la **página entera**; `kf-rise` sólo
sube el hero, y sólo en la portada.

**Dónde está**: `assets/css/maelstrom.css`, entero y calibrado, **no enlazado
desde ninguna página**. Ese archivo lleva en su encabezado cómo reactivarla, los
valores medidos y el bug conocido. En `styles.css` quedó un comentario en el
lugar de donde salió.

**Que siga apartada ahora TIENE GUARDA**, dentro de `check-modes`: ninguna regla
de view-transition viva en la portada ni en una subpágina, nadie pide
`maelstrom.css`, y `/hajime/` entra seca. **No lee archivos, le pregunta al
navegador qué reglas están en efecto** — por eso ve con una sola comprobación
las formas de reponerla, en vez de una regla por vía. Verificada en rojo contra
**seis**: `@view-transition` inline, `::view-transition-old(root)` inline, un
`<link>` al `maelstrom.css` real, la regla anidada en un `@media`, un `@import`,
y una hoja adoptada por JS.

**Y HAY QUE SEGUIR `r.styleSheet`, NO SÓLO `r.cssRules`** — la primera versión de
esta guarda tenía justamente eso mal y vivió una hora. Una `CSSImportRule` no
expone `cssRules` sino `styleSheet`, así que recorrer sólo `cssRules` deja pasar
`@import url("maelstrom.css")`, **que es la vía de reactivación escrita en el
encabezado del propio `maelstrom.css`**: la guarda estaba ciega exactamente en
la puerta principal. Medido: con el `@import` puesto daba 0 hallazgos y con un
`<link>` equivalente daba 7. Lo mismo valía para `document.adoptedStyleSheets`,
que no aparece en `document.styleSheets`.

**Al reactivar la transición, esa comprobación hay que sacarla**: va a dar rojo,
y eso es lo que se busca. Una guarda que sólo se vio en verde no está verificada
—la misma trampa que dejó viva la variante táctil—, y ésta se probó rota antes
de confiar en ella.

**SI ALGUIEN VE EL MAELSTROM CORRIENDO, LA PRIMERA SOSPECHA ES UNA COPIA VIEJA
DE `styles.css` EN SU NAVEGADOR, NO UNA REGRESIÓN.** Y la regla ya no es sólo
del maelstrom: **el mismo día pasó DOS veces más, con otros dos síntomas** — la
ayuda del cubo mostrando el texto de grilla en modo 3D (un `main.js` viejo: el
servido contiene «Drag to turn…» y la guarda lo mide en verde) y las subpáginas
«descentradas» a 1920/2560 (medidas contra `:8000`: left = right exactos, 600 y
920px). Cuando un reporte visual no reproduce contra el servidor con perfil
limpio, el diagnóstico es DOM-contra-red, no una búsqueda de regresión.
Ya pasó, el 2026-08-04: la
consola devolvía **seis** reglas de view-transition mientras el servidor
entregaba un `styles.css` sin ninguna. Las dos cosas eran ciertas sobre archivos
distintos — **el maelstrom vivía DENTRO de `styles.css` hasta `af7c726`**, así
que cualquier copia anterior a ese commit las trae, y son exactamente esas seis.

**EL FINGERPRINT ES EL CONTEO DE `view-transition`, NO EL TAMAÑO**: el viejo
trae **9** ocurrencias en el texto; el vigente, **0**. Ese número sobrevive a
todo lo que rompe a los demás.

El tamaño ya falló acá DOS veces, de dos maneras distintas, y por eso no es la
referencia:

1. **Sin unidad no compara nada.** `wc -c` cuenta bytes; `(await
   res.text()).length` en la consola cuenta caracteres UTF-16, y los
   comentarios en castellano (~430 caracteres no-ASCII) hacen que difieran en
   cientos. Comparar el número de la consola contra el de `wc -c` hizo
   aparecer un tercer archivo que no existía.
2. **El número del VIGENTE deriva.** Se tabuló «47738 bytes = 47187
   caracteres» y a las pocas horas ya era falso: el commit siguiente agregó
   comentarios al CSS. Y deriva dos veces: con cada edición, y con el final de
   línea — el checkout de Windows sirve CRLF por `:8000` y el blob de git es
   LF, así que ni siquiera «el vigente de hoy» es un solo número. **Un
   fingerprint del archivo vigente caduca con el próximo commit; referencia
   fija sólo la da lo que no cambia**: el blob viejo (pre-`af7c726`, LF: 44054
   bytes = 43583 caracteres) y el conteo de arriba.

La comprobación que separa el DOM de la red, que es la pregunta real:

```js
(async () => { for (const s of document.styleSheets) {
  let dom = 0; try { dom = [...s.cssRules].filter(r => /view-transition/i.test(r.cssText)).length } catch {}
  const t = s.href ? await (await fetch(s.href, {cache:'reload'})).text() : '';
  console.log(s.href, '| VT en el DOM:', dom, '| VT en la red:', (t.match(/view-transition/gi)||[]).length, '| chars:', t.length);
} })()
```

**`VT en el DOM: 6` con `VT en la red: 0` es el diagnóstico completo**: el
archivo está bien y lo viejo está del lado del navegador. **Un `Ctrl+Shift+R` no
alcanza para descartarlo**: no toca los *Local Overrides* de DevTools, que
persisten una copia del archivo en el perfil y se sirven por encima de la red.
Descartar el service worker —`navigator.serviceWorker.getRegistrations()`— es
necesario y no es suficiente.

**`check-modes` no puede caer en esto**, y conviene saber por qué antes de
sospechar de su verde: borra su perfil de Chrome en cada corrida
(`shutil.rmtree(PROFILE)` antes de lanzarlo), así que arranca sin caché y sin
overrides. Mide contra el mismo `:8000` —`BASE` por defecto—, pero siempre
contra lo que el servidor entrega. Si la guarda y un navegador se contradicen,
**la copia vieja está en el navegador**.

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

- **Se sacaron**: `The Cube · 立方体`, `Method · 一次資料`, los kanji que
  encabezaban las tres tarjetas del método (`一次資料` / `追跡可能` / `公開`),
  y —en la revisión de quince puntos— **el rótulo `免責事項`** (del footer de
  todas las páginas y del `<title>`/eyebrow de `/disclaimer/`: es la traducción
  de «disclaimer») y **los nombres japoneses de la lista de fuentes DE LA
  PORTADA** (sólo BOJ y FSA los tenían y la columna quedaba dispareja).
- **Se quedan**: `素顔`, los seis nombres de las caras, los tres términos del
  núcleo, y **los nombres reales de los organismos en `/method/`** (`日本銀行`
  junto a Bank of Japan) — ahí no decoran: son el nombre por el que se llega a
  la fuente, y desde la revisión van como **línea secundaria bajo el nombre
  inglés**, no en columna propia. También quedan, con función y no como adorno:
  la marca de agua del About (`産霊　河川　言霊` — sostiene además el supuesto
  de glifos de la vista explotada), el selector `日本語（近日公開）` del footer
  (le habla al lector japonés), y las unidades `百万円/十億円/兆円` en la prosa
  de /method/ (son el contenido). **Todos los glifos retirados siguen en el
  subset para /ja/** — ver el @font-face.

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
el lector (`Odysseus`, `Aeolus`). **Desde el 2026-08-05 son CINCO**: el autor
sumó «How the reading divides» (la división de la lectura: `Taichi`, `Yorozu`,
`Yūgen`), entre el bloque del cubo y el del lector — el 3 explica por qué el
mapa es un cubo de caras al mismo nivel; el 5, cómo se divide el trabajo
DENTRO de una cara. Dos decisiones del bloque, anotadas junto al HTML:

- **Los tres nombres van en `.name` SIN enlace aunque SÍ tienen página** — la
  excepción más discutible del marcado: acá se presentan como parte del
  sistema conceptual, no como destinos (el camino es /hajime/, de donde
  cuelgan), y mezclar nombres enlazados y sin enlazar con el mismo marcado en
  la misma página sería inconsistente. También en el CSS de `a.name`.
- **Sin referentes filosóficos, a propósito**: el `context.md` respalda el
  bloque con Hegel, Jung, el yin-yang, Agustín y Amaterasu, y no se nombra
  ninguno — la página ya maneja seis conceptos de dos tradiciones, y cinco
  referencias más de otras tres la convierten en un ensayo, justo en la
  página cuya función es desactivar la lectura esotérica. Que nadie los
  agregue creyendo que faltan.

- **La tabla de las seis caras salió a propósito, no se perdió.** Cada cara dice
  lo suyo en su propia página; la tabla obligaba a mantener sincronizadas dos
  listas de la misma cosa.
- **La página no explica los nombres de las caras, y no hay que reponer eso.**
  Es la consecuencia buscada del punto anterior.
- **Los nombres del marco van en `<i class="name">`** (los seis originales y,
  desde el bloque 5, también Taichi/Yorozu/Yūgen), cursiva y a color de texto
  pleno. `<i>` y no `<em>` porque `<em>` es énfasis y un lector de pantalla
  lo entonaría; cada nombre se marca **una sola vez**, donde se lo presenta.
  Y no van en oro: el oro es de los subtítulos y los enlaces.
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

### La frontera castellano/inglés es invisible, y por eso tiene guarda

El repo se trabaja en castellano y el sitio se publica en inglés. **El problema
es que la frontera no se ve**: un comentario en castellano es correcto, y la
misma frase dentro de un `content=` viaja en cada enlace compartido. Ya pasó —
`og:image:alt` decía «El cubo de seis caras de Kotodama Finance» **en las diez
páginas**, y se descubrió de casualidad.

**En inglés, sin excepción**: texto visible, `<title>`, `description`, todo
Open Graph y Twitter, los atributos que ve un usuario o un crawler (`alt`,
`aria-label`, `title`, `placeholder`), `sitemap.xml`, `robots.txt`, la 404, y
**los mensajes de `console.*` de `main.js` y `cube.js`**.

**En castellano, deliberado**: comentarios de HTML, CSS y JS; `tools/` y sus
mensajes; `CLAUDE.md`, `README.md`, `docs/`; `_ref/`.

**La línea que separa un comentario de un `console.warn`** es la que costó
pensar: un comentario no se ejecuta; un `console.warn` **sí** — es salida que el
programa produce en runtime, dirigida a quien mire la consola. Es interfaz,
aunque sea técnica.

**Y `robots.txt` y `sitemap.xml` no tienen «comentarios» en el sentido del
HTML**: esos archivos **no tienen versión renderizada**, así que quien abre
`/robots.txt` ve el archivo tal cual, comentarios incluidos. Ahí el comentario
es superficie publicada. Por eso el de `sitemap.xml` se arregló **en el
generador** (`make-sitemap.py`), no en el archivo: si no, vuelve a la próxima
corrida.

**Buscar acentos NO alcanza** — «el cubo de seis caras» no tiene ninguno. El
método que sirve es **aislar la superficie publicable, que es finita, y
revisarla entera**; sobre ese conjunto reducido un detector simple alcanza para
las regresiones. Está en `check-structure`.

**La guarda es incompleta a propósito y lo dice en su salida.** Se le escapó
`«no se pudo hidratar; se mantiene la grilla»` —ni un acento, ni una palabra de
su lista—, que apareció revisando a mano los `console.*`. **Una guarda que
aparenta completitud es peor que ninguna**: cubre la reincidencia de lo
conocido, y al agregar una página hay que leer su superficie igual.

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
  escondía justo lo que el usuario de teclado necesita ver. Y lleva
  **`user-select: none` mientras está recortada** (repuesto en `:focus-within`):
  sin eso, copiar la sección del cubo en 3D arrastraba las seis tarjetas
  invisibles al portapapeles. No toca accesibilidad — AT y foco no pasan por la
  selección — ni a los crawlers, que leen el DOM.
- **URLs por directorios** (`/musubi/`, `/hajime/`…), sin extensión.
- **Cada texto japonés nuevo obliga a regenerar el subset** de Zen Kaku. Ver
  README. **`document.fonts.check()` no sirve** para verificarlo: informa si la
  fuente está cargada, no si contiene el glifo.
- **Los dos comandos de subset NO son iguales, y unificarlos rompe uno.** El
  japonés va **sin** `--layout-features`; el latino, **con** `'*'`. Medido en
  las dos direcciones: con el flag, Zen Kaku pasa de 163 glifos a 258 y suma
  `aalt fwid ordn sups`; sin él, las latinas pierden 374 y 503 glifos. **Cada
  uno reproduce su archivo commiteado sólo con su propia forma.** La regla real
  no es «usar el flag» sino **que el comando escrito reproduzca el archivo que
  se sirve**, y eso se comprueba regenerando y comparando glifos y features.
- **Y el subset LATINO tiene el mismo problema, sin guarda que lo mire.** La
  verificación automática cubre sólo el japonés. Ya mordió dos veces con
  caracteres que uno da por sentados: los **paréntesis de ancho completo**
  （U+FF08/U+FF09), que no entran por el rango latino, y **ū (U+016B)** de
  «Yūgen», que no entraba en ninguno de los rangos declarados. **Al escribir
  romaji con macrón —ō, ū— verificar contra la `cmap` antes de publicar.**

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
| `python tools/check-ready.py` | antes de publicar a `main` | instantánea | **verde** (`0`) desde el 2026-08-05 |

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

**Tags**: sólo en hitos, anotados. `v1-dark` (navy + oro con el cubo) y
**`v1-content-complete`** (sitio terminado de contenido: cero placeholders,
`check-ready` en 0). Queda uno pendiente: **la publicación**, al mergear a `main`.

**UN TAG NO SE MUEVE.** Ya pasó la tentación y la respuesta quedó cerrada: el
mensaje de `v1-content-complete` describe el plan de DNS **anterior** al vigente,
y aun así **no se re-taguea**. Un tag anotado es un **registro fechado del estado
en ese commit**; si se reescribe cada vez que cambia el plan deja de ser un punto
de restauración y pasa a ser una copia peor de este archivo — que sí es el
documento vivo. Y `--force` sobre un tag ya empujado **rompe los clones ajenos**,
que siguen con el objeto viejo. Un mensaje de tag desactualizado no es deriva:
es historia, igual que `docs/v1-dark/README.md`.

`v1-content-complete` **es el punto al que volver si algo se rompe en la
migración de DNS.** Apunta al último estado verificado en verde y no al commit
donde se redactó el último placeholder (`2115a4e`): ahí el contenido ya estaba
completo pero `check-structure` estaba en rojo —la guarda del baseline se rompía
justo al llegar a cero— y se arregló recién en el commit siguiente. **Un punto
de restauración tiene que estar verde**, si no es una trampa.

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

**Cero placeholders. La redacción terminó**, y con ella el único frente que
bloqueaba publicar. El baseline quedó en `0` — de ahora en más, cualquier
número distinto de cero que informe `check-structure` es una regresión, no
trabajo pendiente. Es un cambio de significado de esa guarda: hasta acá bajar
era progreso; ahora subir es un bug y no hay «bajar».

### La procedencia del texto se declara: UNA línea, y sólo en `/method/`

**Esto reemplaza una versión anterior de DOS bloques** —«How this is written» al
final de «What counts as a source», y un colofón al pie— que se retiraron por
decisión del autor. Hoy es **una sola línea**, en el lugar del primero:

> Credit where credit's due: This project would not have been possible without
> my AI assistant.

**«Credit where credit's due» va con WHERE.** La versión con «were» es un error
de tipeo y se lee como tal. Está anotado también en el HTML.

**Por qué en `/method/` y en ninguna otra parte.** Es donde se declara cómo se
produce lo que se publica, así que es donde corresponde decir cómo se produjo el
texto mismo. Un sitio que le exige trazabilidad al dato y no declara la de su
propia prosa tiene un punto ciego; y si alguien lo descubre después sin que esté
dicho, el daño al rigor es mayor que el costo de decirlo.

**No va al footer global**, aunque sea la clase de línea que suele ir ahí. El
footer se repite en las once páginas y esto pertenece a la que habla del método.
Es la regla opuesta a la del `免責事項` corto, y por el mismo criterio: una
advertencia legal sirve donde el lector esté leyendo; una declaración de
procedencia sirve donde se explica el procedimiento.

**Va sin título propio, dentro del cuerpo de la sección.** Es una línea; un `h3`
encima la anunciaría como tema aparte cuando es el cierre de qué cuenta como
fuente. Con el colofón se fueron también `.face-page__minor` y `.colophon` del
CSS, que quedaron sin ningún elemento que las usara.

### La 404 rompe el patrón del kanji a propósito

Lleva **una frase** —`この航路はありません`— donde las seis caras llevan un
nombre en kanji. **No es una inconsistencia que haya que corregir.** Las caras
nombran algo que existe; esta página no es una cara del cubo y no tiene
contenido que nombrar: tiene una **ausencia**, y un sustantivo suelto no puede
decir «esto no existe». Quien la unifique a un kanji suelto por coherencia está
eligiendo la simetría por encima del sentido.

Por eso usa `.face-page__phrase` y no `.face-page__kanji`: ese otro tamaño llega
a 4rem porque está dimensionado para uno o dos glifos, y diez a ese cuerpo miden
más que el ancho de la página.

### `/method/`: la lista de fuentes se DERIVA del `context.md`

**No se mantiene una copia paralela.** La lista de 50 fuentes sale de
`§Fuentes de Datos Mapeadas` de `kotodama_finance_context.md`, que es la fuente
de verdad. Al actualizarla se parte de ese archivo, no de la página.

- **34 Tier 1** (primaria oficial) + **16 Tier 2** (primaria no-oficial
  atribuida), en 12 grupos por dominio, Tier 1 primero dentro de cada uno.
- **La marca de tier es un cuadrado lleno contra hueco, en oro**, con leyenda.
  Reusa el vocabulario de los puntos de estado de las caras porque ya está
  establecido; cuadrado y no círculo para que no se confunda con ellos.
- **Tres cosas quedan fuera, cada una por su motivo**: el Tier 3, que lo cubre
  un párrafo del texto; **EDINET DB y Yahoo Finance Japan**, que parsean y
  redistribuyen dato ajeno y por lo tanto son **secundarias** —publicarlas
  contradiría, en la misma pantalla, el principio que la página declara—; y
  `japan_insurance_v2.xlsx`, que es un archivo interno del proyecto.
- **Ninguna URL se completó de memoria.** Las 17 que el `context.md` no traía se
  buscaron, se verificaron y las aprobó el autor una por una. En una página cuyo
  argumento es que toda cifra es trazable, un enlace inventado sería el peor
  error posible.
- **El subset japonés casi se duplicó**: 149 → 288 códigos, 13,2 → 29,8 KB por
  peso. Es el costo de nombrar 50 entidades en japonés, y entró hiragana y
  katakana por primera vez.

### Las seis caras quedaron con un molde común — y el eyebrow se fue

Al redactarlas se unificó la cabecera con la de `/sugao/`: **`<h1>` con kanji y
romaji, línea de función en `.face-page__gloss`, y nada más.** El
`<p class="eyebrow">` se eliminó de las cinco.

Había **tres capas diciendo lo mismo**: el eyebrow (`Data / Analysis`), el gloss
(`«the beginning»`) y el lead, que abre glosando el nombre. Dos señales de que
sobraban: el eyebrow de `/tosei/` ya decía literal la línea de función que se le
iba a poner, y el significado del kanji que llevaba el gloss lo dice ahora el
lead en prosa, en las cinco.

### El `domain` de las tarjetas: comprimido, no idéntico — decisión cerrada

**Las seis tarjetas se reescribieron.** No para igualarlas a la línea de función
de su página, sino para que **cada una sea la versión COMPRIMIDA de la suya**:

| Cara | Tarjeta (portada) | Línea de función (página) |
|---|---|---|
| `肇 Hajime` | Data and analysis | Data and analysis |
| `素顔 Sugao` | The person behind | The person behind the platform |
| `渡世 Tosei` | Personal finance | Personal finance in Japan |
| `家紋 Kamon` | Community | Community and network |
| `鳥居 Torii` | Learning | Learning and resources |
| `絆 Kizuna` | Acting on it | Understanding to action |

**Que no sean idénticas es deliberado**, y es la parte que se pierde si alguien
las "unifica": **la tarjeta se lee de un vistazo entre seis, la línea de función
se lee sola y con calma.** Son dos trabajos distintos. Lo que sí tienen que
compartir es la raíz — quien va de la tarjeta a la página encuentra continuidad,
no dos nombres para lo mismo.

**Todas sin barra**, mismo registro corto. El patrón anterior estaba a medias:
tres con barra (`Data / Analysis`, `Learn / Resources`, `Act / Business`) y tres
sin ella.

**Estos valores YA NO salen del archivo de referencia**, que sigue diciendo
`Data / Analysis`, `The human behind`, `Connect`, `Learn / Resources` y
`Act / Business`. Ese archivo **no se editó a propósito**: es la instantánea del
landing original, y cambiarle un campo lo convertiría en un híbrido que no es ni
el original ni el estado actual — además de estar en `.gitignore`, o sea que la
edición ni siquiera quedaría versionada. **La defensa contra la deriva es esta
tabla**, que sí está versionada y sí se lee al empezar.

**El folio del cubo no muestra el `domain`.** `FACES` en `assets/js/main.js`
tiene `romaji`, `state` y `status`, nada más; el folio muestra el estado y el
botón. El `domain` vive únicamente en las seis tarjetas de la grilla.

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

  **Hay dos mediciones de rendimiento y ninguna es de teléfono real**: la de
  escritorio, y la emulación móvil de la vista explotada (2026-08-05,
  `docs/mediciones/explotada-movil-emulada.md`: DPR 1.5 y sin antialias
  verificados EJECUTANDO, cadencia dentro del presupuesto de 60 Hz con CPU
  ×4 — pero la GPU era la de escritorio, así que no levanta este congelado).
  La de escritorio:
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
- **Vista explotada del cubo — YA NO ESTÁ CONGELADA: se construyó y está
  INTEGRADA** (2026-08-05, cinco tandas de calibración con el autor; el
  registro completo está en su sección). El núcleo muestra 産霊 · 河川 · 言霊
  horneados en la textura del cascarón (cube.js) y el clic lleva a
  `/musubi/`, como estaba decidido. La advertencia del subset sigue viva:
  los tres glifos están cubiertos porque viven en la marca de agua de la
  portada (`.about__watermark`) y `言`/`霊` son además el logo del nav —
  **si algún día se toca esa marca de agua, la cobertura de la textura del
  núcleo hay que re-verificarla contra la cmap**. Lo que queda para después
  de publicar es la **v2 (corrientes de agua)**, sólo si el autor la pide —
  no se compensa la ausencia con otro efecto.
- **Remolino ukiyo-e para la transición.** Ocho iteraciones fallidas entre Design
  y Claude: **el ruido procedural produce textura, no dibujo** — granulado, no la
  línea de una ola grabada. Requiere ilustrador humano o un enfoque distinto.
  **No reintentar con los mismos medios.** Y hoy la pregunta ni se plantea: la
  transición entera está **reservada y fuera del lanzamiento**, así que no hay
  nada que ilustrar hasta que se decida retomarla.

### Optimización disponible, decidida como NO — ~79 KB en las fuentes latinas

Los subsets latinos llevan features de OpenType que **el sitio no usa** —`smcp`,
`onum`, `dlig`, `ss01`…—, y con ellas 374 glifos de Inter y 503 de Cormorant.
Verificado: cero `font-feature-settings`, cero `font-variant`, cero `small-caps`
en todo el CSS y el HTML. Quitarlas baja las tres fuentes de **198 KB a 119 KB**.

**Decidido por el autor: no se hace ahora, y el motivo pesa más que el número.**
El sitio no está publicado, y esas features son exactamente el tipo de cosa que
alguien usa después sin acordarse de que se sacaron. Un ahorro que se paga con
un fallo silencioso más adelante no es un ahorro.

**La condición para revisarlo**: si algún día el CSS usa `font-feature-settings`,
`font-variant` o `small-caps`, la optimización deja de estar disponible **y** hay
que regenerar comprobando que la feature concreta sobreviva. El detalle y la
tabla por archivo, en el README.

`liga`, `kern` y `calt` nunca estuvieron en juego: sobreviven al subset por
defecto y son las que el navegador aplica solo.

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
- **La cobertura de glifos NO se verifica en el navegador. Ninguna forma
  funciona, y ya se probaron tres.** `document.fonts.check()` da falsos
  positivos: informa si la fuente está cargada, no si contiene el glifo. Medir
  el **ancho** tampoco: los CJK son todos de 1em, así que un glifo presente y
  uno ausente miden exactamente lo mismo. Y comparar los **píxeles** contra un
  fallback tampoco: la cadena de respaldo de `"Zen Kaku", serif` resuelve a una
  fuente distinta de `serif` a secas, así que todo «difiere» y no distingue
  nada. **Verificar contra la tabla `cmap`**, que es la única fuente de verdad.

  Lo que salvó las dos últimas fue **incluir un glifo de control** que se sabe
  ausente (`猫`). Las dos métricas lo dieron como presente, y ahí se ve que
  fallan. **Sin control, las dos habrían pasado por confirmación.** Cuando el
  control se comporta mal, lo que está mal es la métrica, no el sujeto.
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
- **El estado FINAL es un caso borde, y es el único que nunca se prueba.** El
  baseline de placeholders se leía con `if not base`, que confunde «archivo
  ausente» con «archivo que dice cero». Mientras quedaba un solo placeholder eso
  no se notaba; **al terminar la redacción el baseline legítimo pasó a ser `{}`
  y la guarda se rompió sin que nada estuviera mal**. Sobrevivió a decenas de
  corridas porque funcionaba en todos los estados menos en el último — y a ese
  se llega una sola vez. Cuando un contador puede llegar a cero, **cero tiene
  que ser distinguible de vacío**.
- **DOS GUARDAS DE NAVEGADOR A LA VEZ SE ARRUINAN, y una de las dos puede dar
  VERDE EN FALSO.** Lanzando `check-pendulum` en segundo plano y otra encima, la
  segunda murió con `ConnectionResetError` —se pelean el mismo Chrome— y la
  primera **terminó en 0 diciendo TODO OK**. Pero su número era
  `máx |vel| dentro 0.0000`, cuando lo sano es ~0.11: la ventana de medición
  quedó vacía y la comprobación pasó **por no tener nada que comprobar**.
  El rojo se ve; el verde vacío no. **Correrlas de a una**, y desconfiar de una
  métrica que da exactamente 0 donde antes daba otra cosa — un valor que no se
  parece a los anteriores es motivo de repetir la corrida, aunque el resultado
  sea el que uno quería.
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
- **«¿Se ve bien?» no mide la cobertura de glifos, porque el fallback de fuentes
  es POR GLIFO.** Un texto al que le faltan glifos en la fuente declarada **se
  dibuja entero igual**: el navegador va a buscar cada glifo ausente a otra
  familia, sin avisar y sin dejar hueco. Medido en la página de mantenimiento:
  `'Zen Kaku', sans-serif` sobre 保守作業中 dio **2 glifos Zen Kaku + 3 Microsoft
  YaHei** — dos tipografías en una palabra, una de ellas china, y a simple vista
  correcto. La métrica que sirve es **`CSS.getPlatformFontsForNode`**, que dice
  qué fuente REAL dibujó cada glifo; la cmap dice qué debería haber pasado, ésta
  dice qué pasó. Es la contracara del hallazgo de arriba: ahí el subset japonés
  se verificaba contra la cmap porque el navegador no sabía; acá el navegador es
  el único que sabe, porque la pregunta es sobre el fallback y no sobre el
  archivo. Y de paso: **`lang="ja"` decide si el genérico cae en una fuente
  japonesa o en una china** (Noto Sans JP con él, Microsoft YaHei sin él).
- **UNA LÍNEA QUE DECLARA HONESTIDAD ES EL PEOR LUGAR PARA UNA AFIRMACIÓN NO
  VERIFICADA.** El colofón de `/method/` ya no existe —se reemplazó por una
  línea de agradecimiento—, pero el criterio que lo redactó vale para lo que
  venga y por eso se guarda acá en vez de perderse con él. Decía *«the code is
  checked by automated guards»* y **no «reviewed by its author»**, porque el
  código no se revisa a mano: lo verifican las guardas que corren antes de cada
  commit. Poner «revisado por el autor» habría sido presumir un proceso que no
  ocurre, **justo en la frase que le pide al lector que confíe** — el error que
  el resto del sitio se prohíbe. Y los tiempos verbales eran parte de la
  afirmación: presente para las guardas, que siguen corriendo; pasado para el
  texto, que ya se revisó. La prueba antes de publicar una línea así es simple:
  **¿qué comprobación respalda cada verbo?** Si alguno no tiene ninguna, sobra.
- **«Regenerar y comparar bytes» parece la guarda perfecta para un artefacto
  generado, y acá no funciona.** El codificador woff2 **no es determinista**:
  tres corridas del mismo comando dan tres `sha1` distintos, y siguen dándolos
  fijando `head.modified` y con `PYTHONHASHSEED=0` — la diferencia arranca en el
  tamaño comprimido, o sea en Brotli. Una guarda así habría estado en rojo desde
  el primer día, que es la señal que uno aprende a ignorar. Lo que sí funciona
  es partir el artefacto: comparar la parte estable (el HTML con los base64
  elididos, verificado estable en tres corridas) y verificar la parte inestable
  por una propiedad y no por sus bytes (la `cmap` de la fuente). **Antes de
  escribir una guarda que compare salidas, correr el generador dos veces.**
- **PARA MEDIR QUE ALGO NO PASA, PRIMERO HAY QUE PROVOCAR EL MOMENTO EN QUE
  PASARÍA.** Buscando si la transición seguía viva, el primer intento clickeó la
  **tarjeta** de una cara y midió «no hubo transición». Era cierto y no
  significaba nada: la tarjeta hace `preventDefault()` —seleccionar y navegar son
  dos actos, navega el botón del folio—, así que **no hubo navegación**, y una
  transición entre documentos no puede ocurrir sin una. Es el mismo verde vacío
  que `máx |vel| dentro 0.0000`: la comprobación pasa por no tener nada que
  comprobar. Lo delató el propio script, que informaba `aterrizó en: /`.
  El segundo intento trajo la trampa opuesta: midiendo `getAnimations()` a 1,2 s
  del aterrizaje daba «nada corriendo», porque **una animación terminada
  desaparece de la lista**. Llegar tarde y no haber nada se ven idénticos. Se
  arregla muestreando desde `t=0` —0/80/250/600/1200 ms—, y ahí sí aparece lo
  que corre. **La pregunta útil no es «¿lo medí?» sino «¿mi medición podía haber
  dado otro resultado?»**
- **CUANDO DOS MEDICIONES SE CONTRADICEN Y LAS DOS ESTÁN BIEN HECHAS, NO ESTÁN
  MIRANDO EL MISMO ARCHIVO.** Yo medía cero reglas de view-transition por seis
  caminos y el autor veía seis en su consola, sobre la misma URL. El reflejo es
  desconfiar de una de las dos; lo que servía era preguntar **qué archivo mira
  cada una**. Servidor y árbol coincidían byte por byte —mismo `sha256`, cero
  ocurrencias— y el navegador tenía una copia anterior a `af7c726`, el commit
  que sacó el maelstrom de `styles.css`. La pregunta productiva no era «¿quién
  se equivoca?» sino «¿qué tendría que ser cierto para que las dos lo sean?».
  Y el corolario práctico: **para diagnosticarlo hace falta el `href` de la
  hoja, no la lista de reglas.** El primer comando que mandé devolvía
  `r.cssText` y por eso no distinguía nada — con las reglas solas, un archivo
  viejo y una regresión se ven idénticos.
- **UN FETCH MIDE LA RED; EL DOM MIDE LA EJECUCIÓN — y pueden estar los dos
  bien y contradecirse.** «`fetch(main.js, {cache:'reload'}) trae el texto
  correcto» convivía con «el DOM muestra el texto viejo», y las dos mediciones
  eran correctas: el fetch va a la red, pero el módulo que ESCRIBIÓ el DOM se
  evaluó una sola vez por documento (module map) y pudo salir de la caché
  heurística — sin `Cache-Control`, Chrome le da el 10% del Last-Modified de
  frescura y el reload normal no revalida subrecursos desde 2017. Para saber
  qué ejecutó, preguntarle a la ejecución: una huella observable de la versión
  (acá: si el hint cambia al alternar el toggle) o
  `performance.getEntriesByType('resource')` con su `transferSize`. Es la
  variante de «no están mirando el mismo archivo» donde el tercer archivo es
  el que corre en memoria.
- **UN FINGERPRINT NUMÉRICO SIN UNIDAD INVENTA ARCHIVOS QUE NO EXISTEN.** Cerrando
  lo anterior propuse distinguir el `styles.css` viejo del vigente por su tamaño,
  y di la referencia en **bytes** (`wc -c` → 47738) para una comprobación que
  corre en la consola y devuelve **caracteres UTF-16**
  (`(await res.text()).length` → 47187). Los 428 caracteres no-ASCII de los
  comentarios en castellano hacen 551 de diferencia, así que el número medido no
  coincidía con ninguna de las dos referencias y **la conclusión razonable pasó a
  ser «hay un tercer archivo»** — con un servidor y un worktree de más que buscar.
  No los había: era el mismo archivo medido con dos instrumentos distintos.
  La regla: **un número de referencia viaja con su unidad y con el comando que lo
  produce**, y si la comprobación va a correr en otro instrumento, la referencia
  se mide con *ése*. Lo delata tener tres números donde deberían ser dos, o una
  diferencia chica y estable que nadie sabe explicar.
  Y un corolario aparte: **el tamaño es un proxy, no la pregunta.** Lo que se
  quería saber era si el archivo trae las reglas, y eso se contesta contando
  `view-transition` en el texto que baja. Un proxy bien elegido igual contesta
  otra cosa.
  La segunda mordida llegó el mismo día, y es la otra mitad de la regla: **un
  fingerprint del archivo VIGENTE caduca con el próximo commit.** El «47187
  caracteres» corregido quedó tabulado como referencia y a las pocas horas ya
  era falso — el commit siguiente agregó comentarios al mismo CSS. La auditoría
  lo cazó antes que un lector. Referencia fija sólo la da lo que no cambia (un
  blob histórico, un conteo estructural); si el número describe el presente,
  hay que escribirle al lado cómo regenerarlo, no su valor.
