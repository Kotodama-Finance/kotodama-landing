"""Lógica compartida por las guardas de texto. No es ejecutable por sí sola.

Vive acá porque `check-structure.py` y `check-ready.py` miran las mismas cosas
con criterios distintos, y duplicar el escaneo garantizaba que se desincronizaran.
El nombre lleva guión bajo (y no guión medio como los scripts) para que sea
importable: `import _guardas`.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
# Directorios que no se publican
EXCLUIDOS = {"_dev", "_ref", ".git", "docs", "tools", "node_modules"}
# Rango de caracteres japoneses: kana, kanji y espacio ideográfico
JAPONES = re.compile(r"[぀-ヿ㐀-鿿　]")
BASELINE = RAIZ / "tools" / "placeholders-baseline.json"


def htmls():
    for p in sorted(RAIZ.rglob("*.html")):
        if any(parte in EXCLUIDOS for parte in p.relative_to(RAIZ).parts):
            continue
        yield p


def nombre(p: Path) -> str:
    return p.relative_to(RAIZ).as_posix()


def texto_visible(html: str) -> str:
    """HTML sin scripts, estilos ni comentarios: sólo lo que ve el lector.

    Los comentarios se excluyen a propósito: llevan notas en castellano y
    japonés que nunca se renderizan.
    """
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def placeholders() -> dict:
    """{página: cantidad de class="todo"}, sólo las que tienen alguno."""
    cuenta = {}
    for p in htmls():
        n = len(re.findall(r'class="[^"]*\btodo\b[^"]*"',
                           p.read_text(encoding="utf-8")))
        if n:
            cuenta[nombre(p)] = n
    return cuenta


def leer_baseline() -> dict:
    if not BASELINE.exists():
        return {}
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def escribir_baseline(cuenta: dict):
    BASELINE.write_text(
        json.dumps(cuenta, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")


def comparar_baseline(actual: dict, base: dict):
    """Devuelve (subieron, bajaron) contra el baseline.

    `subieron` es lo que rompe la guarda estructural: placeholders NUEVOS, o sea
    texto en castellano dirigido al autor que alguien acaba de introducir sin
    querer. `bajaron` es progreso de redacción y sólo se informa.
    """
    subieron, bajaron = [], []
    for pagina in sorted(set(actual) | set(base)):
        a, b = actual.get(pagina, 0), base.get(pagina, 0)
        if a > b:
            subieron.append((pagina, b, a))
        elif a < b:
            bajaron.append((pagina, b, a))
    return subieron, bajaron


def glifos_faltantes():
    """Glifos japoneses del sitio que NO están en el subset de Zen Kaku.

    Se comprueba contra la tabla `cmap` de la fuente, que es la única fuente de
    verdad. NO se usa document.fonts.check(): informa si la fuente está cargada,
    no si contiene el glifo, y da falsos positivos.

    Devuelve {} si está todo cubierto, None si falta fontTools.
    """
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
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


def chrome_divergente():
    """El nav y el footer están duplicados en las ocho páginas: no hay build step
    que los comparta. La duplicación es aceptable si está vigilada, así que en
    vez de templetizar se verifica que no derive: los bloques tienen que ser
    idénticos carácter por carácter en todas las páginas."""
    def bloque(html, ini, fin):
        try:
            a = html.index(ini)
            b = html.index(fin, a) + len(fin)
            return html[a:b]
        except ValueError:
            return None

    ref, problemas = {}, []
    for p in htmls():
        html = p.read_text(encoding="utf-8")
        for etiqueta, ini, fin in (("nav", '<header id="nav"', "</header>"),
                                   ("footer", '<footer id="footer"', "</footer>")):
            b = bloque(html, ini, fin)
            if b is None:
                problemas.append(f"{nombre(p)}: no tiene {etiqueta}")
                continue
            if etiqueta not in ref:
                ref[etiqueta] = (nombre(p), b)
            elif b != ref[etiqueta][1]:
                problemas.append(
                    f"{nombre(p)}: el {etiqueta} difiere del de {ref[etiqueta][0]}")
    return problemas
