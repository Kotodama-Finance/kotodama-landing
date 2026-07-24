# Medición: la luz del cubo a lo largo del arco del péndulo

> **ESTADO: CERRADO por inspección visual. No reabrir el barrido.**
> No hay problema de iluminación que arreglar. La contradicción entre la métrica
> y las capturas está explicada abajo, y no era un bug: era una lectura
> equivocada de un número correcto. **El tema se resuelve mirando, no midiendo.**
> Hoja de contactos: `hoja-contactos-arco.png`.

## Resolución: por qué "70% del perímetro con ΔL bajo" no significa nada malo

El cuerpo del cubie (`#040d18`) tiene luminancia **~11.5** y el fondo de sección
**15.3**. **El cubo es más oscuro que su fondo.** Por lo tanto toda porción de
perímetro que no esté iluminada da ΔL ≈ 4 y falla los tres umbrales **por
construcción**, sin que eso indique ningún defecto.

Y un objeto más oscuro que su fondo **se ve perfecto**: se lee como silueta. Lo
que hace desaparecer un contorno es **ΔL ≈ 0**, no un ΔL chico pero consistente.
Además la percepción cierra el contorno a partir de la arista iluminada aunque
medio perímetro esté en sombra.

O sea: la métrica **no estaba rota** — «70% del perímetro con ΔL bajo» es
verdadero. Lo que estaba mal era interpretarlo como «el cubo se deshace».

**La pregunta era perceptual y binaria, y se contesta mirando.** Se gastaron
cuatro tandas construyendo un instrumento para eso. Si alguien siente que el
cubo se pierde en alguna pose, la respuesta es una captura, no un barrido.

## Métrica vigente: contraste del perímetro

Qué fracción del **perímetro** de la silueta tiene contraste insuficiente contra
el fondo. Construcción:

1. **Silueta desde el canal alfa** del canvas del cubo (`alpha = 255`), no desde
   la luminancia: es exacta y no depende de lo que esté pintado adentro.
2. **Perímetro 4-conexo**: píxeles del objeto con al menos un vecino fuera. El
   interior queda excluido por construcción.
3. **Muestreo hacia adentro** siguiendo el gradiente de la máscara, a 3px y 6px,
   exigiendo `alpha = 255` (un píxel con alfa parcial es mezcla de cubo y fondo
   y da contraste falsamente bajo).
4. **Fondo local medido**, no asumido: se camina hacia afuera hasta el primer
   píxel con `alpha = 0`. Medido así, el fondo detrás del escenario resultó
   **plano en 15.3 en las 696 poses** — la constante habría servido, pero ahora
   está verificado en vez de supuesto.
5. **Sin excluir el oro.** El oro es el cubo siendo visible.
6. Se reportan **tres umbrales** (5, 8, 12 unidades sRGB), la **mediana de |ΔL|**
   y el **tramo fallido contiguo más largo**: un 15% en manchitas es invisible,
   un 15% en una arista entera es un borde que desapareció.

### Resultados (peor caso sobre 24 valores de ry)

| rx | 3px u5 | 3px u8 | 3px u12 | 6px u8 | contig u8 | mediana \|ΔL\| |
|---|---|---|---|---|---|---|
| -10 | 42.8 | 45.0 | 64.7 | 38.6 | 15.1 | 17.3 |
|  -8 | 43.8 | 44.5 | 56.4 | 37.6 | 15.7 | 19.2 |
|  -6 | 21.4 | 44.3 | 49.1 | 37.9 | 14.6 | 19.1 |
|  -4 | 11.5 | 44.7 | 49.6 | 36.8 | 12.8 | 18.3 |
|  -2 | 3.7 | 25.7 | 50.2 | 22.3 | 12.9 | 19.1 |
|   0 | 1.1 | 8.5 | 49.6 | 8.1 | 4.2 | 20.1 |
|   2 | 4.7 | 27.1 | 50.1 | 23.6 | 12.9 | 19.2 |
|   4 | 15.1 | 48.7 | 49.3 | 41.2 | 12.8 | 18.3 |
|   6 | 30.5 | 48.1 | 48.5 | 43.2 | 14.6 | 18.4 |
|   8 | 48.6 | 48.8 | 57.5 | 45.5 | 16.1 | 19.2 |
|  10 | 46.3 | 47.9 | 56.0 | 46.7 | 15.5 | 17.3 |
|  12 | 41.1 | 42.0 | 73.0 | 43.8 | 14.6 | 17.3 |
|  14 | 40.7 | 43.1 | 75.1 | 45.2 | 13.9 | 17.4 |
|  16 | 39.3 | 42.3 | 74.3 | 44.4 | 19.1 | 17.4 |
|  18 | 40.8 | 50.9 | 72.1 | 51.1 | 13.6 | 17.5 |
|  20 | 40.1 | 70.2 | 70.9 | 70.2 | 17.5 | 17.3 |
|  22 | 42.7 | 68.3 | 71.9 | 68.2 | 24.7 | 17.3 |
|  24 | 66.0 | 66.5 | 69.9 | 66.7 | 24.6 | 17.3 |
|  26 | 63.8 | 64.8 | 71.0 | 65.1 | 24.3 | 17.3 |
|  28 | 62.3 | 63.1 | 71.2 | 63.0 | 17.7 | 17.3 |
|  30 | 60.8 | 61.2 | 71.0 | 61.0 | 24.1 | 17.3 |
|  32 | 59.3 | 59.7 | 71.9 | 59.9 | 23.5 | 17.3 |
|  34 | 56.8 | 57.8 | 71.6 | 57.7 | 23.6 | 17.3 |
|  36 | 37.3 | 55.8 | 70.0 | 55.4 | 23.0 | 17.3 |
|  38 | 32.0 | 40.7 | 69.2 | 41.0 | 22.9 | 17.3 |
|  40 | 5.0 | 40.4 | 69.2 | 37.9 | 22.4 | 17.3 |
|  42 | 5.6 | 30.7 | 68.2 | 25.4 | 10.9 | 17.3 |
|  44 | 3.1 | 25.7 | 68.9 | 21.1 | 10.7 | 17.1 |
|  46 | 4.0 | 22.6 | 50.6 | 21.1 | 10.3 | 17.1 |

**La profundidad de muestreo no cambia la conclusión**: 3px y 6px dan valores
muy parecidos, así que no es un parámetro sensible y el bisel no está
contaminando la medición.

### Cómo leer estos números

Ver la resolución al principio: los porcentajes altos son consecuencia de que el
cubo es más oscuro que el fondo, no señal de un problema. **Sirven para comparar
esquemas de luz entre sí, no como umbral de aprobado/desaprobado.**

Dos bugs ya encontrados y corregidos en esta métrica, que muestran lo fácil que
es equivocarse acá:
- Se dibujaba el canvas sobre un lienzo **vacío**, así que "afuera" era
  transparente (luminancia 0) en vez del fondo, y el antialias dorado del borde
  se contaba como fondo brillante (daba "fondo" entre 0 y 85 en una página plana).
- Las muestras de afuera caían en el **antialias del borde**. Ahora se exige
  `alpha = 0` caminando hacia afuera.

## Métrica descartada: oscuridad interior

**No usar.** Medía el porcentaje de píxeles del cubo a menos de 3 unidades del
fondo, excluyendo los dorados. Dos errores de fondo:

1. **Excluir el oro era el bug.** El oro es el cubo siendo visible. Una cara con
   un kanji grande es la pose donde el cubo mejor se lee, y la métrica la
   penalizaba justamente ahí: al descartar esos píxeles terminaba midiendo el
   navy **entre** los trazos, que es sombra de relieve. Cuanto más legible el
   cubo, peor puntuaba.
2. **Medía interior y lo llamaba silueta.** Fundirse con el fondo es un fenómeno
   de **contorno**: un píxel oscuro rodeado de oro no disuelve nada, el ojo lo
   integra al objeto.

Quedó desmentida mirando las capturas: la pose que llamó la peor (rx=26, ry=0,
54.5%) es la que mejor se ve — 肇 enorme y nítido, contorno recortado — y la que
llamó sana (rx=0, 3.8%) es una vista de canto menos legible. **Ordenaba las
poses al revés.**

Sus datos quedan en `luz-arco-rx.json` sólo como registro de lo descartado.

## Qué se medía antes (histórico, con la métrica descartada)

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
