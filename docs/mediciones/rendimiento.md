# Medición: rendimiento de la página completa

**Fecha: julio de 2026.** Es la única medición de rendimiento del proyecto.

> **Una medición vale por sus condiciones.** Están abajo, completas. Sin ellas el
> número no dice nada: «6,1 ms» en otra máquina, a otra resolución o a otra tasa
> de refresco no es el mismo dato.

## Condiciones

| | |
|---|---|
| GPU | **RTX 4060 Laptop** |
| Viewport | **1707 × 904 CSS px, a dpr 1.5** (≈ 2560 × 1356 px físicos, ~3,5 Mpx) |
| Pantalla | **165 Hz** → presupuesto de **6,06 ms por cuadro** |
| Qué se midió | la **página completa**: mar + cubo + composición |

El dpr importa: en escritorio el mar dibuja a resolución completa hasta dpr 2
(`background.js`), así que a 1.5 se estaba pagando el shader sobre los 3,5 Mpx
reales, no sobre los CSS.

## Resultado

**Página completa: 6,1 ms por cuadro — idéntico a no dibujar nada.**

O sea: la medición queda clavada en el presupuesto de refresco. Lo que se está
midiendo es el vsync, no el trabajo de la página, y por lo tanto **el costo real
está por debajo del presupuesto y este método no puede separarlo más**. Un número
igual al intervalo de refresco no es «tarda 6,1 ms»: es «no llega a ser el cuello
de botella».

**Dónde está el costo cuando lo hay: en el shader del mar.** El cubo es ruido
estadístico — no se distingue de la varianza de la medición.

**En escritorio sobra margen.** Ésa es la conclusión operativa, y es la razón por
la que no hay más mediciones: no hay nada que optimizar mientras el número no se
despegue del vsync.

## Por qué el mar y no el cubo

El cubo son 26 cubies opacos con material estándar: geometría trivial y una
pasada de depth buffer. El mar, en cambio, evalúa ruido procedural **por píxel**,
a pantalla completa.

Contando sobre el shader de `assets/js/background.js`, por píxel y por cuadro:

| Llamada | fbm | Dónde |
|---|---|---|
| `ocean(sp, t)` | 5 | `H`, la altura de ola |
| `oceanSmooth(...)` × 4 | 4 c/u = 16 | las dos diferencias centradas de la normal (`hx`, `hy`) |
| **Total** | **21 llamadas a `fbm`** | |

Y `fbm` corre **5 octavas**, o sea 5 evaluaciones de `snoise` cada una:

**21 × 5 = 105 evaluaciones de `snoise` por píxel y por cuadro.**

A 3,5 Mpx eso son ~365 millones de evaluaciones de ruido por cuadro. Es un orden
de magnitud que explica por qué el mar es el único término que aparece, y por qué
la variante táctil de la transición entre páginas **quería** evitar el desenfoque
a pantalla completa.

> **Quería, no evitaba.** Verificado en agosto de 2026: esa variante definía sus
> keyframes sin blur pero **nunca los asignaba** —sólo cambiaba la duración—, así
> que en táctil corría igual la versión con desenfoque. La transición está hoy
> reservada en `assets/css/maelstrom.css`, fuera del lanzamiento, y el bug está
> anotado en su encabezado.

> **Nota sobre una cifra que circulaba.** La anotación original de esta medición
> decía «~42 evaluaciones de ruido por píxel». Contado sobre el código son
> **105** (21 `fbm` × 5 octavas); las 21 llamadas a `fbm` tampoco dan 42. El `42`
> del shader es el factor de escala del `return` de `snoise`, que es otra cosa.
> **El conteo de arriba se rehace leyendo `background.js`**, que es la única
> fuente de verdad; si el shader cambia de octavas o de número de muestras para
> la normal, hay que rehacerlo.

La conclusión no se mueve: sea 42 o 105, el mar domina y el cubo no aparece.

## Lo que NO se midió

- **Móvil, en dispositivo real: nunca.** No hay ni un número. Y es justo donde el
  costo importa: el shader escala con los píxeles, y una GPU de teléfono no tiene
  el margen de una 4060. Por eso `background.js` ya baja a media resolución
  (`dpr × 0.5`) y limita a 25 fps en `pointer: coarse` — pero **esas decisiones
  son precaución, no medición**. Es el mismo hueco anotado en `CLAUDE.md` entre
  los congelados.

  El tercer ejemplo que estaba acá, «el maelstrom táctil va sin blur», salió
  porque **no era cierto** (ver la nota de arriba). Vale como advertencia por sí
  solo: una precaución documentada y nunca verificada es indistinguible de una
  que no existe.
- **La creación del contexto WebGL**, que es lo que difiere el lazy-init de
  `main.js`. Es un costo de una sola vez al inicializar y no aparece en un número
  por cuadro; se difiere por criterio, no porque se haya medido.
- **El pico de carga inicial** (compilación de los dos shaders + fuentes).
- **Cualquier GPU integrada.**

## Cómo repetirla

Con el sitio servido, mirando el tiempo de GPU por cuadro en las herramientas del
navegador. La comparación que da sentido al número es contra **la página sin
dibujar nada**: si los dos valores coinciden y coinciden con el intervalo de
refresco, no hay nada que medir todavía. Para separar términos hay que salirse
del vsync — bajar la tasa de refresco, subir mucho la resolución, o medir en
hardware más chico.
