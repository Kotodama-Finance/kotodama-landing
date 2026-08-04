# Medición: encuadre anisotrópico de la cámara

**Fecha: 2026-08-04.** Acompaña al cambio de fórmula en `frameCamera()`
(`assets/js/cube.js`): de la esfera envolvente completa al cuerpo barrido real.

> **Una medición vale por sus condiciones.** Chrome headless a dpr 1,
> `Network.setCacheDisabled`, sitio servido en `:8000`. El barrido corre sobre
> `_dev/pendulum-test.html` (canvas 720×488 en ese viewport); la medición de la
> portada, sobre `/` a 1440×900 (canvas 720×620).

## Por qué cambió la fórmula

La esfera envolvente (radio `√3·S ≈ 2.579`) garantiza contra **cualquier**
rotación — incluida la que pone un vértice arriba. Pero esa pose **no existe en
este cubo**: `rotation.z` es siempre 0 (order `'YXZ'`, nadie lo escribe), y sin
roll la coordenada vertical sólo depende de `rx`. La altura máxima alcanzable es
`√2·S` (arista arriba, `rx≈45°`), un 18 % menos que el vértice.

La fórmula nueva acota cada eje por su peor caso real:

```
d_vertical   = M · S · (√2/tan(halfV) + 1)   // arista arriba, a radio S del eje
d_horizontal = M · √3·S / sin(halfH)         // ry libre: radio de revolución
camera.z     = max(d_vertical, d_horizontal)
```

**El hallazgo que salió del cálculo y no de la intuición**: restringir el
encuadre al arco del péndulo (`rx ∈ [−8°, 44°]`) **no gana nada** sobre
cubrir todo `rx`. El máximo vertical del cuerpo barrido está en `rx = 45°`
(`√2·cos(rx−45°)` es plano en el pico), así que el arco, que llega a 44°, ya
contiene el peor caso a 4 decimales. Consecuencia doble: la garantía cubre el
arrastre manual sin acotar **gratis**, y cambiar la amplitud del péndulo no
invalida el encuadre. El supuesto del que sí depende es **la ausencia de
roll** — está anotado en `frameCamera()`.

## Barrido de verificación (360 poses)

`rx ∈ {−8, 0, 10, 18, 26, 35, 40, 44, 45, 50, 60, 90, −90, 135, 180}` ×
`ry` cada 15°. Por pose: `setRotation` + `render` + captura compositada (leer el
canvas WebGL fuera de su frame devuelve vacío), y distancia mínima del píxel
dibujado a cada borde.

| rx | margen mínimo |
|---|---|
| −8 | 54 px |
| 0 | 73 px |
| 18 (centro del péndulo) | 36 px |
| 40 | 18 px |
| **44–45 (peor caso teórico)** | **17 px** |
| 60 | 23 px |
| ±90 (snap Torii/Kizuna) | 73 px |
| 135 (espejo del peor caso) | 17 px |
| 180 | 73 px |

**Cero recortes en 360 poses.** El mínimo cae exactamente donde la teoría lo
pone (arista arriba) y vale ~6 % del semieje, que es el `FIT_MARGIN = 1.06`
devuelto en píxeles: la fórmula está al hueso, el margen que queda es el
declarado.

## Efecto en la portada (720×620, 1440×900)

| | antes (esfera) | después | 
|---|---|---|
| `camera.z` | 13.15 | 12.08 |
| cubo dibujado, alto | 442 px (71 %) | **483 px (78 %)** |
| cubo dibujado, ancho | 415 px (58 %) | 467 px (65 %) |
| aire arriba | 102 px | 84 px |
| aire abajo | 76 px | 53 px |

El aire restante (~137 px) **no es recortable por encuadre**: es la reserva
para las poses de arista arriba, que el arrastre manual sí alcanza. Reducirlo
más exigiría acotar el arrastre o reencuadrar dinámicamente con la pose — y un
zoom continuo atado a la rotación se lee como respiración de la cámara, no como
encuadre.

## Los dos errores de medición que costó este número

1. **`captureScreenshot` sin `captureBeyondViewport` devuelve negro bajo el
   fold**, y el negro difiere del fondo más que el umbral: la primera medición
   contó media pantalla vacía como «cubo» y dio 100 % de ancho — un cubo que
   toca los dos bordes, que es la seña de que la métrica estaba rota. Ahora el
   guión verifica que el escenario esté entero dentro del viewport y aborta si
   aparecen filas de negro puro.
2. **El píxel más claro no distingue un disco de un aro** (medición de los
   puntos de estado, misma sesión): los dos usan `--c-gold`, así que su máximo
   es idéntico por construcción. Dio «0.0 de diferencia», demasiado redondo
   para ser real. Lo que separa esos estados es el relleno — se mide el centro
   y la proporción de píxeles encendidos.
