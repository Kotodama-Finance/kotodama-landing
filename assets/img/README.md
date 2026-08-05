# Logos de instituciones ajenas

`librarything-flat-logo-rounded_1024w.png` es el **archivo oficial de
LibraryThing TAL CUAL se distribuye, sin modificar** — mismo bytes que el
original (`flat-logo-rounded_1024w.png`, 11.026 bytes). No se recortó, no se
recoloreó, no se recomprimió. Las esquinas ya vienen transparentes (alfa 0,
medido): funciona sobre navy sin tocar nada.

**El criterio, fijado por el autor (ago 2026): los logos de instituciones
ajenas se usan en su paleta original.** Adaptarlos a la paleta del sitio es
apropiarse de una marca que no es nuestra. Esto REVIERTE una decisión
anterior (monocromo en oro, silueta con `fill=currentColor`) — si alguien
encuentra esa instrucción en el historial o en un comentario viejo, la
vigente es ésta. Aplica también a los logos que vienen (IMDb, MyAnimeList,
Steam, GitHub): archivo oficial, sin recolorear. El costo aceptado es que
entren colores ajenos a la paleta; lo controla el TAMAÑO (chico, como sello),
no el recoloreo.

**Usar el archivo sin alterar es además lo que hace el uso defendible**:
librarything.com devuelve 403 al acceso automatizado en su página de prensa y
en el FAQ de uso del logo (`/topic/45089`), así que los términos no se
pudieron leer — y mostrar la marca tal cual ella se publica es exactamente lo
que cualquier guía de marca permite.

Por qué el PNG y no el SVG oficial (`flat-logo-rounded.svg`): ese SVG no
dibuja la L como forma — la escribe como `<text>` con la tipografía
«ThomasPaineRegularSWFTE», que no está en el repo ni en la máquina del
visitante, así que la L saldría con una fuente de reemplazo y la marca se
vería mal. Verificado por el autor; el PNG de 1024 px sobra para el tamaño
de sello al que se muestra (@2x incluido).

---

## La lista de fuentes de la portada va SIN logos — y la investigación queda

**Ninguna de las cinco filas lleva logo, por decisión del autor
(2026-08-05).** Se investigaron los cinco y sólo la FSA servía un archivo
oficial utilizable; con cuatro filas sin logo y una con, el sello suelto
quedaba más raro que la columna pareja, así que se quitó también ése.

Lo investigado, para el día que se reponga:

- **FSA**: SÍ tiene archivo utilizable — su símbolo oficial en
  `https://www.fsa.go.jp/images/icon.png` (192×192, RGBA con fondo
  transparente — alfa 0 en las esquinas, medido; 11.912 bytes, sha256
  `87E9C94739B9E5B2B19F282058DF8BAB9AF6FB33846A80AE1D4ED8624FF447AF`,
  verificado byte-idéntico al descargado). Estuvo puesto como
  `fsa-icon.png` y se retiró del árbol con esta decisión; el blob vive en
  la historia (commit `ca96c72`) si hay que recuperarlo sin red.
- **BOJ**: sólo publica su logotipo sobre fondo opaco (JPG blanco y GIF con
  fondo gris — quitarle el fondo sería alterar el archivo, que es lo que
  este criterio prohíbe; su favicon es de 16px, insuficiente).
- **EDINET**: no distribuye ningún logo (favicon de 198 bytes).
- **BIS**: el servidor de bis.org rechaza conexiones desde este entorno, y
  sin archivo oficial no hay logo.
- **Damodaran Online**: página académica personal sin marca gráfica.

**El criterio de reposición no cambió**: el día que alguna de estas fuentes
publique un archivo oficial utilizable, se repone con el criterio
LibraryThing — oficial SIN alterar, paleta original, tamaño sello. **Y que
nadie "complete" las filas con SVGs de Wikipedia o similares**: no son el
archivo oficial, que es lo único que este criterio admite.
