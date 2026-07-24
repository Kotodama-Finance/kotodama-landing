#!/usr/bin/env python3
"""Guarda previa a publicar. Falla si el sitio no está listo para ir a main.

    python tools/check-ready.py

Comprueba dos cosas:

1. Que no queden placeholders de redacción (`class="todo"`) en ningún HTML
   publicable. Un placeholder en producción es texto en castellano dirigido al
   autor apareciendo en un sitio en inglés.

2. Que el subset de Zen Kaku Gothic New cubra TODOS los glifos japoneses que
   aparecen en el sitio. Si falta uno, ese carácter se renderiza con una fuente
   del sistema y desentona, de forma silenciosa.

   La comprobación se hace contra la tabla `cmap` de la fuente. NO se usa
   document.fonts.check() del navegador: informa si la fuente está cargada, no
   si contiene el glifo, y devuelve falsos positivos.

Devuelve 0 si todo está bien, 1 si hay algo que corregir.
"""
import re
import sys
from pathlib import Path

# La consola de Windows usa cp1252 por defecto: sin esto, imprimir un glifo
# japonés (justo lo que este script reporta) lanza UnicodeEncodeError.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parent.parent
# Directorios que no se publican
EXCLUIDOS = {"_dev", "_ref", ".git", "docs", "tools", "node_modules"}
# Rango de caracteres japoneses: kana, kanji y espacio ideográfico
JAPONES = re.compile(r"[぀-ヿ㐀-鿿　]")


def htmls():
    for p in sorted(RAIZ.rglob("*.html")):
        if any(parte in EXCLUIDOS for parte in p.relative_to(RAIZ).parts):
            continue
        yield p


def texto_visible(html: str) -> str:
    """HTML sin scripts, estilos ni comentarios: sólo lo que ve el lector.

    Los comentarios se excluyen a propósito: llevan notas en castellano y
    japonés que nunca se renderizan.
    """
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def revisar_todos():
    total = 0
    for p in htmls():
        n = len(re.findall(r'class="[^"]*\btodo\b[^"]*"', p.read_text(encoding="utf-8")))
        if n:
            print(f"  {p.relative_to(RAIZ).as_posix()}: {n} placeholder(s) sin escribir")
            total += n
    return total


def revisar_subset():
    """Devuelve la lista de glifos japoneses del sitio que faltan en el subset."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("  (omitido: falta fontTools — pip install fonttools brotli)")
        return None

    usados = set()
    for p in htmls():
        usados |= set(JAPONES.findall(texto_visible(p.read_text(encoding="utf-8"))))

    faltan = {}
    for fuente in sorted((RAIZ / "assets" / "fonts").glob("zen-kaku-*-subset.woff2")):
        f = TTFont(fuente)
        cubiertos = set().union(*[set(t.cmap) for t in f["cmap"].tables])
        ausentes = sorted(c for c in usados if ord(c) not in cubiertos)
        if ausentes:
            faltan[fuente.name] = ausentes
    return faltan


def revisar_chrome():
    """El nav y el footer están duplicados en las ocho páginas: no hay build step
    que los comparta. La duplicación es aceptable si está vigilada, así que en
    vez de templetizar se verifica que no derive: los bloques tienen que ser
    idénticos carácter por carácter en todas las páginas."""
    def bloque(html, ini, fin):
        try:
            a = html.index(ini); b = html.index(fin, a) + len(fin)
            return html[a:b]
        except ValueError:
            return None

    ref = {}
    problemas = []
    for p in htmls():
        html = p.read_text(encoding="utf-8")
        nombre = p.relative_to(RAIZ).as_posix()
        for etiqueta, ini, fin in (("nav", "<header id=\"nav\"", "</header>"),
                                   ("footer", "<footer id=\"footer\"", "</footer>")):
            b = bloque(html, ini, fin)
            if b is None:
                problemas.append(f"{nombre}: no tiene {etiqueta}")
                continue
            if etiqueta not in ref:
                ref[etiqueta] = (nombre, b)
            elif b != ref[etiqueta][1]:
                problemas.append(f"{nombre}: el {etiqueta} difiere del de {ref[etiqueta][0]}")
    return problemas


def main():
    print("Placeholders de redacción")
    pendientes = revisar_todos()
    if pendientes == 0:
        print("  sin placeholders")

    print("\nCobertura del subset japonés")
    faltan = revisar_subset()
    if faltan == {}:
        print("  todos los glifos cubiertos")
    elif faltan:
        for nombre, glifos in faltan.items():
            print(f"  {nombre}: faltan {''.join(glifos)}")
        print("  -> regenerar el subset (ver README, «Tipografías»)")

    print("\nNav y footer compartidos")
    problemas = revisar_chrome()
    paginas = len(list(htmls()))
    if problemas:
        for x in problemas:
            print(f"  {x}")
    else:
        print(f"  idénticos en las {paginas} páginas")

    ok = pendientes == 0 and not faltan and not problemas
    print("\nLISTO PARA PUBLICAR" if ok else "\nNO PUBLICAR TODAVÍA")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
