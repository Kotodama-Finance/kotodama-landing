#!/usr/bin/env python3
"""Genera los iconos del sitio. Reproducible: los binarios salen de acá.

    python tools/make-favicon.py            # genera los archivos definitivos
    python tools/make-favicon.py --strip    # además, la tira de comparación

Produce, en la raíz del sitio (que es donde el navegador los busca):
  favicon.ico          16+32+48 px, PNG embebido. Mata el 404 implícito:
                       el navegador pide /favicon.ico haya o no <link>.
  favicon.svg          vectorial, con el kanji como PATH (no como <text>):
                       un favicon no carga webfonts, así que un <text
                       font-family="Zen Kaku..."> caería a una fuente del
                       sistema y el trazo no sería el de la marca.
  apple-touch-icon.png 180x180, para «añadir a pantalla de inicio» en iOS.

El glifo sale del MISMO subset que usa la página (peso 500, el de la marca en
el nav), así que el icono y el logo son literalmente la misma letra.

Los colores están duplicados acá y en favicon.svg porque un icono se renderiza
aislado: no ve el CSS y no puede leer :root. Si cambia la paleta, hay que
volver a correr este script. Es la misma excepción que el shader del mar.
"""
import argparse
import io
import os
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "assets" / "fonts" / "zen-kaku-gothic-new-500-subset.woff2"

# Copias de los tokens de :root — ver nota de arriba.
NAVY = (4, 13, 24)        # --c-navy    #040d18
GOLD = (200, 168, 90)     # --c-gold    #c8a85a

SS = 8                    # supersampling: el hinting CJK a 16px es peor que esto


def ttf_temporal() -> Path:
    """woff2 -> ttf: FreeType (y por lo tanto Pillow) no abre woff2."""
    from fontTools.ttLib import TTFont
    f = TTFont(FUENTE)
    f.flavor = None
    destino = Path(os.environ.get("TEMP", "/tmp")) / "kf-favicon-src.ttf"
    f.save(destino)
    return destino


def lienzo(px: int, fondo) -> Image.Image:
    return Image.new("RGBA", (px, px), fondo + (255,))


def dibujar_kanji(px: int, texto: str, ttf: Path, fondo, tinta, relleno=0.76) -> Image.Image:
    """Kanji centrado por su caja real de tinta, no por la métrica de la fuente.

    Centrar por métricas deja el glifo alto: la caja em reserva espacio para
    descendentes que un kanji no usa. A 16px ese desplazamiento se ve.
    """
    grande = px * SS
    im = lienzo(grande, fondo)
    d = ImageDraw.Draw(im)

    objetivo = grande * relleno
    tam = int(objetivo)
    for _ in range(40):
        fuente = ImageFont.truetype(str(ttf), tam)
        izq, arr, der, aba = d.textbbox((0, 0), texto, font=fuente)
        ancho, alto = der - izq, aba - arr
        may = max(ancho, alto)
        if abs(may - objetivo) <= 1 or tam <= 4:
            break
        tam = max(4, int(tam * objetivo / max(may, 1)))
    fuente = ImageFont.truetype(str(ttf), tam)
    izq, arr, der, aba = d.textbbox((0, 0), texto, font=fuente)
    x = (grande - (der - izq)) / 2 - izq
    y = (grande - (aba - arr)) / 2 - arr
    d.text((x, y), texto, font=fuente, fill=tinta + (255,))
    return im.resize((px, px), Image.LANCZOS)


def dibujar_cubo(px: int, fondo, tinta) -> Image.Image:
    """Cubo isométrico: hexágono + tres radios. Tres rombos, nada más."""
    import math
    grande = px * SS
    im = lienzo(grande, fondo)
    d = ImageDraw.Draw(im)
    c = grande / 2
    r = grande * 0.40
    hexa = [(c + r * math.cos(math.radians(a)), c + r * math.sin(math.radians(a)))
            for a in range(-90, 270, 60)]
    grosor = max(1, int(grande * 0.055))
    d.polygon(hexa, outline=tinta + (255,), width=grosor)
    for i in (0, 2, 4):
        d.line([(c, c), hexa[i]], fill=tinta + (255,), width=grosor)
    return im.resize((px, px), Image.LANCZOS)


# Las cuatro variantes que se comparan. La que se publica es la primera.
def variantes(ttf):
    return [
        ("A  言 oro sobre navy",  lambda px: dibujar_kanji(px, "言", ttf, NAVY, GOLD)),
        ("B  言 navy sobre oro",  lambda px: dibujar_kanji(px, "言", ttf, GOLD, NAVY)),
        ("C  言霊 completo",      lambda px: dibujar_kanji(px, "言霊", ttf, NAVY, GOLD, 0.86)),
        ("D  cubo isométrico",    lambda px: dibujar_cubo(px, NAVY, GOLD)),
    ]


def escribir_ico(destino: Path, imagenes):
    """ICO con PNG embebido, escrito a mano.

    Pillow reescala solo al guardar .ico y no controlo con qué filtro; acá cada
    tamaño se renderiza aparte, que es justo lo que importa a 16px.
    """
    trozos = []
    for im in imagenes:
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True)
        trozos.append((im.size[0], buf.getvalue()))

    cabecera = struct.pack("<HHH", 0, 1, len(trozos))
    desplazamiento = 6 + 16 * len(trozos)
    directorio, cuerpo = b"", b""
    for lado, datos in trozos:
        directorio += struct.pack("<BBBBHHII",
                                  lado if lado < 256 else 0,
                                  lado if lado < 256 else 0,
                                  0, 0, 1, 32, len(datos), desplazamiento)
        desplazamiento += len(datos)
        cuerpo += datos
    destino.write_bytes(cabecera + directorio + cuerpo)


def escribir_svg(destino: Path, ttf: Path, texto: str = "言"):
    """SVG con el contorno del glifo como <path>, en un viewBox de 64."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.misc.transform import Transform

    f = TTFont(ttf)
    glifos = f.getGlyphSet()
    cmap = f.getBestCmap()
    nombre = cmap[ord(texto)]

    bp = BoundsPen(glifos)
    glifos[nombre].draw(bp)
    x0, y0, x1, y1 = bp.bounds

    caja, relleno = 64.0, 0.76
    escala = caja * relleno / max(x1 - x0, y1 - y0)
    # y invertida: en tipografía crece hacia arriba, en SVG hacia abajo
    t = Transform(escala, 0, 0, -escala,
                  (caja - (x1 - x0) * escala) / 2 - x0 * escala,
                  (caja + (y1 - y0) * escala) / 2 + y0 * escala)
    pluma = SVGPathPen(glifos)
    glifos[nombre].draw(TransformPen(pluma, t))

    navy = "#%02x%02x%02x" % NAVY
    gold = "#%02x%02x%02x" % GOLD
    destino.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        "  <!-- Kotodama Finance. Colores copiados de :root (--c-navy, --c-gold):\n"
        "       un favicon se renderiza aislado y no puede leer el CSS.\n"
        "       Regenerar con tools/make-favicon.py si cambia la paleta. -->\n"
        f'  <rect width="64" height="64" fill="{navy}"/>\n'
        f'  <path fill="{gold}" d="{pluma.getCommands()}"/>\n'
        "</svg>\n", encoding="utf-8")


def tira(ttf: Path, destino: Path):
    """Las cuatro variantes a tamaño REAL, más el 16px ampliado sin suavizar.

    Un favicon se juzga a 16px o no se juzga: cualquier vista ampliada y suave
    miente. El bloque de la derecha es el pixelado de verdad, a escala 10x.
    """
    tamanos = [16, 32, 48, 180]
    pad, sep, col_izq, fila = 26, 40, 300, 200
    zoom = 10
    ancho = col_izq + sum(t + sep for t in tamanos) + 16 * zoom + sep + pad
    alto = pad * 2 + len(variantes(ttf)) * (fila + sep)
    hoja = Image.new("RGB", (ancho, alto), (12, 22, 36))
    d = ImageDraw.Draw(hoja)
    try:
        rot = ImageFont.truetype(str(ttf), 20)
        chico = ImageFont.truetype(str(ttf), 15)
    except Exception:
        rot = chico = ImageFont.load_default()

    y = pad
    for etiqueta, hacer in variantes(ttf):
        d.text((pad, y + fila // 2 - 10), etiqueta, font=rot, fill=(220, 232, 244))
        x = col_izq
        for t in tamanos:
            im = hacer(t)
            hoja.paste(im.convert("RGB"), (x, y + (fila - t) // 2))
            d.text((x, y + (fila + t) // 2 + 6), f"{t}px", font=chico, fill=(125, 156, 187))
            x += t + sep
        amp = hacer(16).convert("RGB").resize((16 * zoom, 16 * zoom), Image.NEAREST)
        hoja.paste(amp, (ancho - pad - 16 * zoom, y + (fila - 16 * zoom) // 2))
        y += fila + sep
    d.text((ancho - pad - 16 * zoom, y - sep + 8), "16px ampliado 10x (sin suavizar)",
           font=chico, fill=(125, 156, 187))
    hoja.save(destino)
    return hoja.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strip", action="store_true", help="genera la tira de comparación")
    ap.add_argument("--variante", default="A", help="cuál se publica (A/B/C/D)")
    args = ap.parse_args()

    ttf = ttf_temporal()
    elegida = dict(zip("ABCD", [v[1] for v in variantes(ttf)]))[args.variante.upper()]

    escribir_ico(RAIZ / "favicon.ico", [elegida(t) for t in (16, 32, 48)])
    elegida(180).convert("RGB").save(RAIZ / "apple-touch-icon.png")
    escribir_svg(RAIZ / "favicon.svg", ttf)

    for n in ("favicon.ico", "favicon.svg", "apple-touch-icon.png"):
        print(f"  {n:22} {os.path.getsize(RAIZ / n):>6} B")

    if args.strip:
        destino = RAIZ / "_dev" / "favicon-opciones.png"
        print(f"  tira: {destino}  {tira(ttf, destino)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
