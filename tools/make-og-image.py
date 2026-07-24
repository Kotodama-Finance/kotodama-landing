#!/usr/bin/env python3
"""Genera og-image.png: la tarjeta que se ve al compartir un enlace del sitio.

    python tools/make-og-image.py            # regenera y vuelve a sellar
    python tools/make-og-image.py --sellar   # acepta la imagen actual sin regenerar
    python tools/make-og-image.py --prueba   # además, la versión a 500 px

1200x630 es la medida canónica (relación 1.91:1): es la que piden Facebook,
LinkedIn, Slack, Discord y X, y la que Google usa para las tarjetas grandes.
Se compone al doble y se baja, porque en pantallas densas se muestra a 2x.
Debajo de 600x315 varias plataformas degradan a miniatura cuadrada.

SÓLO TIPOGRAFÍA. Antes se capturaba el cubo del sitio servido; ya no. Dos
consecuencias, y las dos son mejoras: este script no necesita navegador ni
servidor (sólo las fuentes), y una tarjeta puramente tipográfica se lee como
institucional, que es la dirección del proyecto.

LA MEDIDA QUE MANDA NO ES 1200 PX. En un feed de escritorio la tarjeta se ve a
unos 500 px de ancho, o sea a un 42%. Todo lo que no se lea ahí no está
sirviendo, por más bien que se vea a tamaño completo. `--prueba` deja al lado la
versión reducida justamente para juzgarla así.

Jerarquía, de más a menos peso: 言霊 (lo que mejor sobrevive a la miniatura),
el nombre de la marca, y la bajada.

La bajada va en Inter y no en Cormorant por la misma razón por la que el romaji
del cubo tuvo que dejar Cormorant: es una serif de display con astas finas, y a
un 42% las astas desaparecen. Cormorant es la voz de marca en el sitio, donde el
texto se ve a tamaño real; una tarjeta social no es ese medio.
"""
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "og-image.png")
PRUEBA = os.path.join(RAIZ, "_dev", "og-image-500px.png")

W, H, SS = 1200, 630, 2          # SS: se compone al doble y se baja
ANCHO_FEED = 500                 # cómo se ve en un feed de escritorio


def tokens():
    """Lee la paleta del :root de styles.css.

    NO se copian los colores acá. make-favicon.py sí los copia, porque un icono
    de 16 px no puede depender de parsear un CSS, pero acá la copia tendría dos
    costos: la tarjeta derivaría de la paleta sin que nadie lo note, y `:root`
    dejaría de ser una entrada real de la imagen — con lo cual la guarda que
    avisa que la og-image quedó vieja avisaría por cambios que no la afectan, o
    peor, no avisaría por los que sí.

    Sin fallback, igual que cube.js: si falta un token, falla con su nombre en
    vez de disfrazarlo con un hex de repuesto.
    """
    css = open(os.path.join(RAIZ, "assets", "css", "styles.css"),
               encoding="utf-8").read()
    m = re.search(r":root\s*\{.*?\n\}", css, flags=re.S)
    if not m:
        sys.exit("no se encontró el bloque :root en styles.css")
    bloque = m.group(0)

    def tok(nombre):
        h = re.search(rf"{re.escape(nombre)}\s*:\s*(#[0-9a-fA-F]{{6}})\s*;", bloque)
        if not h:
            sys.exit(f"falta el token {nombre} en :root")
        v = h.group(1).lstrip("#")
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))

    return {n: tok(n) for n in (
        "--c-navy", "--c-surface-cube", "--c-gold", "--c-text", "--c-text-mist")}


_convertidas = {}


def ttf(nombre):
    """woff2 -> ttf en temporal: FreeType (y por lo tanto Pillow) no abre woff2.

    Cacheado, y no por velocidad: ImageFont.truetype deja el archivo ABIERTO, así
    que convertir la misma fuente dos veces intenta sobrescribir un archivo en
    uso, y en Windows eso es un error y no una espera.
    """
    if nombre in _convertidas:
        return _convertidas[nombre]
    from fontTools.ttLib import TTFont
    f = TTFont(os.path.join(RAIZ, "assets", "fonts", nombre))
    f.flavor = None
    destino = os.path.join(os.environ.get("TEMP", "/tmp"), "kf-og-" + nombre + ".ttf")
    f.save(destino)
    _convertidas[nombre] = destino
    return destino


def fuente(nombre, tam, peso=None):
    f = ImageFont.truetype(ttf(nombre), tam)
    if peso is not None:
        try:                      # Inter y Cormorant son variables
            f.set_variation_by_axes([peso])
        except Exception:
            pass
    return f


def ancho_espaciado(d, texto, fnt, tracking):
    return sum(d.textlength(c, font=fnt) for c in texto) + tracking * (len(texto) - 1)


def texto_espaciado(d, texto, fnt, cx, y, fill, tracking):
    """PIL no tiene letter-spacing y la marca lo lleva en toda la web."""
    x = cx - ancho_espaciado(d, texto, fnt, tracking) / 2
    for c in texto:
        d.text((x, y), c, font=fnt, fill=fill)
        x += d.textlength(c, font=fnt) + tracking


def mezcla(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def componer():
    T = tokens()
    w, h = W * SS, H * SS
    cx = w // 2

    tarjeta = Image.new("RGB", (w, h), T["--c-surface-cube"])
    d = ImageDraw.Draw(tarjeta)

    # Viñeta: el mismo recurso que usa la página para dar profundidad. Ancha y
    # con curva suave; corta y abrupta se lee como un marco dibujado.
    borde = int(150 * SS)
    for i in range(borde):
        k = (1 - i / borde) ** 2.2
        d.rectangle([i, i, w - i, h - i],
                    outline=mezcla(T["--c-surface-cube"], T["--c-navy"], k))

    ja = fuente("zen-kaku-gothic-new-500-subset.woff2", int(150 * SS))
    # El nombre de la marca era el elemento MÁS DÉBIL de la tarjeta: 23 px en
    # azul grisáceo, o sea ~10 px en un feed. Ahora va al doble de tamaño, con
    # más tracking y en blanco: es el nombre, tiene que sobrevivir la miniatura.
    marca = fuente("inter-latin.woff2", int(46 * SS), 500)
    # A 42% son ~16 px: el piso para que una línea larga se lea de un vistazo.
    bajada = fuente("inter-latin.woff2", int(38 * SS), 400)

    # Alturas reales medidas, no métricas de la fuente: un kanji no usa el
    # espacio de descendentes que la caja em reserva, y centrar por métricas lo
    # deja alto.
    def alto(txt, fnt):
        a = d.textbbox((0, 0), txt, font=fnt)
        return a[3] - a[1], a[1]

    LINEA = "Japan’s financial system, made legible — from the source."
    h_ja, off_ja = alto("言霊", ja)
    h_marca, off_marca = alto("KOTODAMA FINANCE", marca)
    h_baj, off_baj = alto(LINEA, bajada)

    hueco1, hueco2, hueco3 = int(52 * SS), int(30 * SS), int(34 * SS)
    alto_filete = int(1.4 * SS)
    total = h_ja + hueco1 + h_marca + hueco2 + alto_filete + hueco3 + h_baj
    y = (h - total) // 2

    d.text((cx - d.textlength("言霊", font=ja) / 2, y - off_ja),
           "言霊", font=ja, fill=T["--c-gold"])
    y += h_ja + hueco1

    texto_espaciado(d, "KOTODAMA FINANCE", marca, cx, y - off_marca,
                    T["--c-text"], int(11 * SS))
    y += h_marca + hueco2

    # Filete: el mismo separador que el hero, en oro apagado.
    ancho_filete = int(150 * SS)
    d.rectangle([cx - ancho_filete // 2, y, cx + ancho_filete // 2, y + alto_filete],
                fill=mezcla(T["--c-surface-cube"], T["--c-gold"], 0.55))
    y += alto_filete + hueco3

    # La bajada entra en UNA línea: en dos, cada mitad queda más corta y el
    # bloque compite con el nombre de la marca por el segundo lugar.
    ancho_baj = d.textlength(LINEA, font=bajada)
    margen = int(70 * SS)
    if ancho_baj > w - 2 * margen:
        sys.exit(f"la bajada no entra en una línea ({ancho_baj:.0f} px de "
                 f"{w - 2 * margen}); achicar el cuerpo o partirla")
    d.text((cx - ancho_baj / 2, y - off_baj), LINEA, font=bajada,
           fill=mezcla(T["--c-text-mist"], T["--c-text"], 0.62))

    return tarjeta.resize((W, H), Image.LANCZOS)


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _guardas as G

    if "--sellar" in sys.argv:
        # Para cuando la imagen la pone el autor a mano y no este script.
        if not os.path.exists(SALIDA):
            sys.exit("no hay og-image.png que sellar")
        G.sellar_og()
        print("  sellada la og-image.png actual sin regenerarla")
        return 0

    tarjeta = componer()
    tarjeta.save(SALIDA, optimize=True)
    # El sello guarda el hash de lo que determina cómo se ve la imagen, para que
    # check-structure avise si alguna entrada cambió.
    G.sellar_og()
    kb = os.path.getsize(SALIDA) / 1024
    print(f"  og-image.png  {W}x{H}  {kb:.0f} KB")
    print("  tools/og-image.lock.json sellado")
    if kb > 300:
        print("  OJO: >300 KB. Algunas plataformas descartan imágenes pesadas.")

    if "--prueba" in sys.argv:
        os.makedirs(os.path.dirname(PRUEBA), exist_ok=True)
        chica = tarjeta.resize((ANCHO_FEED, round(H * ANCHO_FEED / W)), Image.LANCZOS)
        chica.save(PRUEBA)
        print(f"  {PRUEBA}  {chica.size[0]}x{chica.size[1]}  (así se ve en un feed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
