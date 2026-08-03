# v1-dark — registro visual

Capturas del estado etiquetado como `v1-dark` (commit `9b5d811`): la versión
navy oscuro + oro, con el cubo de navegación en Three.js.

Existen para poder comparar contra rediseños posteriores sin tener que
reconstruir el tag, levantar un servidor y esperar a que renderice.

| Archivo | Qué es |
|---|---|
| `cube-front.png` | Cara frontal del cubo (肇 Hajime), rotación 0°/0°. Muestra el kanji abarcando los 9 cubies de la cara. |
| `cube-three-quarter.png` | Vista 3/4 (rx 18°, ry −26°), la orientación con la que el cubo aparece al cargar. Se ven tres caras: 肇, 素顔 y 鳥居. |
| `page-full.png` | Página completa, 1440px de ancho. |

## Cómo se generaron

Con Chrome headless. Las del cubo, desde `_dev/capture-cube.html`, que renderiza
el cubo a una rotación fija sobre el fondo real de su sección. La de página
completa, vía CDP (`Page.captureScreenshot` con `captureBeyondViewport`), con un
viewport real de 1440×900 para que las secciones de `100vh` conserven su
proporción.

## Advertencia sobre la captura de página completa

`captureBeyondViewport` no maneja bien lo que está anclado al viewport, así que
la captura se toma con tres ajustes que **no** alteran lo que ve un usuario:

- `background-attachment` del `body` pasa de `fixed` a `scroll`. Con `fixed`, el
  fondo se pinta sólo dentro del viewport; más abajo la captura queda sin pintar
  y el lienzo por defecto es blanco, sobre el que el degradado superior de la
  sección del cubo componía una banda clara espuria.
- Color de base en `<html>`, por si queda algún hueco sin pintar.
- Los elementos `position:fixed` (canvas del mar, viñeta, nav) pasan a
  `absolute`, para que se dibujen una sola vez arriba en lugar de repetirse.

Verificado contra una captura de viewport real: la transición del hero a la
sección del cubo es un fundido limpio a casi negro, sin ninguna banda.

## Estado del cubo en estas capturas — HISTÓRICO, NO ES EL ACTUAL

> **Todo lo de esta sección son los valores del tag `v1-dark`.** Es un registro
> de un momento, no la definición del cubo. Dos de estos números **ya no son los
> de hoy** y están marcados abajo. Los vigentes se leen de `assets/js/cube.js` y
> del `:root` de `assets/css/styles.css`, y están tabulados en el README de la
> raíz, sección «El cubo: parámetros vigentes».

- Cuerpo del cubie `#040d18` (navy de marca) — **sigue vigente**, es
  `--c-cube-body`.
- Fondo de sección `#020509` — **YA NO.** Hoy es `--c-surface-cube` = `#05111d`.
  Ese casi negro hacía leer la página como tres páginas pegadas y se reemplazó
  por una rampa suave entre secciones.
- Kanji incrustado en oro `#c8a85a` (`--c-gold`), abarcando la cara entera a
  través de los nueve cubies; el trazo se interrumpe en las juntas — **sigue
  vigente**.
- Luz difusa `hemi 2.2 · key 1.8 · rim 0.4 · back 0.8` — **YA NO.** Hoy es
  `hemi 3.5 · key 2.9 · rim 0.65 · back 1.3`. Subieron precisamente al aclarar el
  fondo del punto anterior: la separación del cubo contra su fondo se sostiene
  con luz, no oscureciendo la página. El reparto entre las cuatro no cambió.
- Material `roughness 0.72 · metalness 0.02` — **sigue vigente**.
