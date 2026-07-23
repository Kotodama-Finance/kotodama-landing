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

## Estado del cubo en estas capturas

- Cuerpo del cubie `#040d18` (navy de marca) sobre fondo de sección `#020509`.
- Kanji incrustado en oro `#c8a85a`, abarcando la cara entera a través de los
  nueve cubies; el trazo se interrumpe en las juntas.
- Luz difusa: `hemi 2.2 · key 1.8 · rim 0.4 · back 0.8`, material
  `roughness 0.72 · metalness 0.02`.
