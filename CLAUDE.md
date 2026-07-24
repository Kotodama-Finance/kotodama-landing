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

- **Luz a lo largo del arco del péndulo.** Prioritario. Barrido completo medido
  y guardado en **`docs/mediciones/luz-arco.md`** (+ los JSON crudos). No
  remedir: leer eso primero. Resumen:
  - El peor punto es **rx≈26 con 54.5%** de silueta fundida, no rx=38.
  - **El centro del péndulo no aguanta**: 33.3% a rx=18. Sólo `rx ∈ [-4, 4]`
    queda bajo 8%.
  - El `ry` que peor cae **cambia con `rx`**, así que ninguna pose fija lo
    encuentra. Medir siempre barriendo los dos ejes.
  - **Subir el ambiente NO sirve** (medido: de hemi 3.5 a 8.0 el peor caso pasa
    de 51.8% a 53.6%). Mover la clave quedó sin medir y es lo más prometedor.
    Achicar la amplitud sola tampoco alcanza: obligaría a centro ≈ 0 y amplitud
    ≈ 0, matando el péndulo y la vista 3/4.
  - **Salvedad pendiente**: la métrica excluye el dorado y puede estar inflando
    el número en poses donde el kanji domina el encuadre. Confirmar con una
    captura a rx=26 / ry=0 **antes** de tocar la luz.
- **Móvil sin medir en dispositivo real.** Incluye: degradación del cubo, y que
  con escenario más alto que ancho manda el FOV horizontal, la cámara se aleja y
  queda aire vertical desperdiciado. El shader ya va a media resolución y 25 fps.
- **`favicon.ico` 404** — único error de consola en carga limpia.
- **~70 placeholders `TODO`** pendientes de redacción.
- **Animación maelstrom**: plan entregado (View Transitions cross-document,
  precarga al seleccionar, bfcache para el botón atrás, sin remolino con
  `prefers-reduced-motion`), **sin implementar**.
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
