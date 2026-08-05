# La vista explotada bajo emulación de móvil

**2026-08-05 · verificación previa al merge `cube-exploded` → `redesign-trust`,
pedida por el autor.** Emulación de dispositivo por CDP en Chrome headless
sobre la máquina de desarrollo (RTX 4060 Laptop, pantalla 165 Hz) — o sea:
**mide el costo del lado CPU con una GPU de escritorio. NO reemplaza la
medición en dispositivo real**, que sigue pendiente para el sitio entero.

## Condiciones

- `Emulation.setDeviceMetricsOverride`: 390×844, deviceScaleFactor 3,
  mobile — más touch emulation y `pointer: coarse` / `hover: none` por
  `setEmulatedMedia` (verificado: `matchMedia('(pointer: coarse)')` da true
  en la página).
- CPU throttling ×1 y ×4 (`Emulation.setCPUThrottlingRate`).
- Servido desde `:8000`, commit `81152e5` (defaults finales: modelo
  anillo+0.85, explodeR 5.5, coreR 0.7, wordSpin 24 s, tinta `#ffd24a`).

## 1. La degradación declarada, verificada EJECUTANDO

La lección de la variante táctil del maelstrom: lo declarado no cuenta hasta
verse ejecutar. Las dos perillas de `pointer: coarse` del cubo son del
RENDERER (no por-modo), así que cubren la vista explotada frame por frame:

| Perilla | Declarada | Medida en la sesión emulada |
|---|---|---|
| Tope de DPR | `min(dpr, 1.5)` con coarse (2 en escritorio) | buffer 525×630 sobre 350×420 CSS = **1.50 efectivo** (la ventana estaba a DPR 3) |
| Antialias | `antialias: !coarse` | `getContextAttributes().antialias === false` |

Nada de la vista explotada tiene degradación PROPIA (ni menos cubies, ni
material más barato para el núcleo): hereda la del renderer, y eso es todo.

## 2. Cadencia rAF (ms por cuadro)

| Estado | CPU ×1 | CPU ×4 |
|---|---|---|
| Armado (péndulo) | mediana 6,0 · p95 6,6 · máx 6,9 | mediana 6,1 · p95 6,3 · máx 18,3 |
| Transición de explosión | mediana 6,1 · p95 6,7 · **máx 284,2** | mediana 6,1 · p95 12,2 · máx 30,3 |
| Explotado estable (palabras girando) | mediana 6,1 · p95 6,5 · máx 6,8 | mediana 6,1 · p95 6,2 · máx 12,2 |

**Veredicto: verde del lado CPU.** Con CPU ×4 todo queda dentro del
presupuesto de 16,7 ms de un teléfono a 60 Hz (peor p95: 12,2 en la
transición). El estado explotado estable —que renderiza continuo por el giro
de las palabras— cuesta lo mismo que el péndulo armado.

## Dos hallazgos menores, anotados sin resolver

- **La PRIMERA explosión tiene un solo cuadro largo (~284 ms a CPU ×1)**: la
  asignación de los buffers del pase de transmisión, que Three.js crea en el
  primer render que los necesita. Las explosiones siguientes no lo tienen
  (a ×4 el máximo fue 30 ms porque los buffers ya existían de la pasada ×1).
  En un teléfono ese hitch único será mayor; si alguna vez molesta, la salida
  es pre-calentar el pase (un render con el núcleo visible fuera de pantalla
  al hidratar), no bajar la calidad.
- **El botón «Explode the Cube» mide 23 px de alto** como objetivo táctil
  (la guía usual pide ~44). Es el mismo control de enlace del pie del cubo;
  si móvil se retoma en serio, entra en ese pase.

## Lo que esta medición NO dice

El pase de transmisión del núcleo renderiza la escena a textura en cada
cuadro: es costo de GPU, y acá la GPU era una RTX de escritorio. El buffer
móvil es chico (525×630) y la expectativa razonable es que una GPU de
teléfono lo maneje, pero **eso es expectativa, no medición** — el congelado
de móvil (dispositivo real) sigue en pie.
