# Medición: la luz del cubo a lo largo del arco del péndulo

Barrido hecho el 2026-07-24 sobre `redesign-trust`. **Guardado para no tener que
remedirlo.** Datos crudos en `luz-arco-rx.json` y `luz-arco-opciones.json`.

## Qué se mide

**Silueta fundida**: porcentaje de píxeles del cubo que quedan a menos de 3
unidades sRGB del fondo de sección (`--c-surface-cube` = `#05111d`, luminancia
15.3). Es cuánta silueta literalmente desaparece.

Se excluyen los píxeles dorados del kanji, para medir el cuerpo y no el trazo.
**Ver la salvedad al final: esa exclusión puede estar inflando el número.**

Condiciones: escenario 720×520, luz `hemi 3.5 · key 2.9 · rim 0.65 · back 1.3`,
material `roughness 0.72 · metalness 0.02`, cuerpo `#040d18`.

## Por qué un barrido y no poses sueltas

Tres mediciones anteriores en poses fijas dieron conclusiones equivocadas. A
`rx=18` el promedio sobre `ry` es **10.0%** pero el peor caso es **33.3%**: una
medición en `ry=-26` daba 5.1% y parecía sano.

Y **el `ry` que peor cae cambia con `rx`** (≈45° en rx bajo, 0° en rx alto), así
que ninguna pose fija lo encuentra. El rango barrido incluye el sobrepaso de ±6°
del péndulo, que no estaba contemplado: el recorrido real es ~[-8, 44], no
[-2, 38].

## Curva: silueta fundida contra rx

Cada fila es el **peor caso sobre 24 valores de `ry`** (cada 15°). 696 poses.

| rx | peor % | peor ry | medio % | |
|---|---|---|---|---|
| -10 |  24.2 | 240 |   5.7 | `############` |
|  -8 |  23.1 | 240 |   4.2 | `###########` |
|  -6 |  13.4 | 240 |   3.2 | `######` |
|  -4 |   4.8 | 315 |   2.8 | `##` |
|  -2 |   3.8 |  45 |   2.5 | `#` |
|   0 |   3.8 |  45 |   2.5 | `#` |
|   2 |   3.7 |  45 |   2.5 | `#` |
|   4 |   4.7 | 135 |   2.9 | `##` |
|   6 |  12.4 |  60 |   3.2 | `######` |
|   8 |  21.0 |  60 |   4.2 | `##########` |
|  10 |  21.9 |  60 |   5.6 | `##########` |
|  12 |  29.4 |  45 |   6.6 | `##############` |
|  14 |  33.5 |  45 |   7.4 | `################` |
|  16 |  33.8 |  45 |   8.3 | `################` |
|  18 |  33.3 |  45 |  10.0 | `################` |
|  20 |  42.5 |  30 |  11.1 | `#####################` |
|  22 |  42.0 |  30 |  13.2 | `#####################` |
|  24 |  51.0 |  15 |  14.5 | `#########################` |
|  26 |  54.5 |   0 |  16.9 | `###########################` |
|  28 |  54.3 |   0 |  21.2 | `###########################` |
|  30 |  51.8 |   0 |  22.3 | `#########################` |
|  32 |  49.6 |   0 |  22.8 | `########################` |
|  34 |  48.4 |   0 |  23.0 | `########################` |
|  36 |  48.3 |   0 |  23.2 | `########################` |
|  38 |  46.8 |   0 |  23.5 | `#######################` |
|  40 |  45.8 |   0 |  23.7 | `######################` |
|  42 |  43.3 |   0 |  23.8 | `#####################` |
|  44 |  42.5 |   0 |  23.9 | `#####################` |
|  46 |  45.5 | 180 |  24.0 | `######################` |

- Peor punto absoluto: **rx = 26° con 54.5%** (ry = 0°).
- Único tramo con peor ≤ 8%: **[-4, 4]**.
- El centro del péndulo (rx=18) **no aguanta**: 33.3%.

## Opciones de iluminación probadas

Peor caso sobre 12 valores de `ry`, por variante de intensidad:

| config | rx=0 | rx=18 | rx=30 | rx=38 | rx=44 | **peor** |
|---|---|---|---|---|---|---|
| A actual | 3.8 | 32.6 | 51.8 | 46.8 | 42.5 | **51.8** |
| B ambiente 6.0 | 3.3 | 21.0 | 53.4 | 48.0 | 42.2 | **53.4** |
| C ambiente 8.0 | 2.9 | 19.7 | 53.6 | 48.1 | 42.1 | **53.6** |
| D +relleno y contraluz | 1.9 | 16.8 | 36.4 | 45.9 | 41.5 | **45.9** |

**Subir el ambiente no sirve.** De `hemi 3.5` a `8.0` el peor caso empeora
levemente (51.8 → 53.6). Ayuda en el centro (32.6 → 19.7) pero nada por encima
de rx=30. El trade-off volumen/estabilidad que ya se recorrió dos veces ni
siquiera compra la mejora.

**Mover la clave quedó sin medir.** Requiere recrear el cubo con otro `keyPos`,
y el `await import()` dentro de la evaluación por CDP devolvía `null` sin error.
Es la única opción sin número y, por descarte, la más prometedora.

**Achicar la amplitud del péndulo, sola, no alcanza.** Para peor ≤8% el recorrido
tiene que quedar en [-4, 4]; sumando el sobrepaso de ±6°, eso obliga a centro ≈ 0
y amplitud ≈ 0 — matar el péndulo y además perder la vista 3/4, que es la firma
del cubo.

## Salvedad: la métrica puede estar exagerando

Al excluir el dorado, en poses donde una cara con kanji grande domina el encuadre
lo que queda medido es sobre todo el navy **entre** los trazos, que son las zonas
en sombra del relieve. Eso inflaría el porcentaje sin que el cubo se vea peor, y
explicaría que rx=26 dé 54% y rx=0 dé 3.8% con la misma luz.

**Antes de rehacer la iluminación hay que mirar una captura a rx=26 en su peor
`ry` (0°)** y confirmar si el cubo realmente se deshace. Si es artefacto, lo que
hay que corregir es la métrica, no la luz.

## Cómo reproducirlo

El barrido corre en el banco de pruebas `_dev/capture-cube.html`, que expone
`window.__cube`. Para cada pose: `setRotation(rx, ry)`, `render()`, y leer los
píxeles **en el mismo turno de JS** — un canvas WebGL leído fuera de su frame
devuelve vacío.
