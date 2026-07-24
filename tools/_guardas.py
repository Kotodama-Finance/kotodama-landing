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
SITIO = "https://kotodamafinance.com"
# Directorios que no se publican
EXCLUIDOS = {"_dev", "_ref", ".git", "docs", "tools", "node_modules"}
# Páginas que existen pero NO se indexan (ver sitemap_incompleto)
NO_INDEXABLES = {"404.html"}
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
    """{página: cantidad de placeholders sin redactar}, sólo las que tienen.

    Cuenta DOS familias, y la segunda se agregó tarde por un agujero real: los
    placeholders de metadatos no llevan `class="todo"` porque no son elementos
    —viven en `content="…"` y en `<title>`— así que no se contaban. El sitio
    podía dar «LISTO PARA PUBLICAR` con seis descriptions que decían «TODO:
    descripción de esta cara.», que es exactamente el fallo que esta guarda
    existe para evitar: castellano dirigido al autor en producción.
    """
    cuenta = {}
    for p in htmls():
        h = p.read_text(encoding="utf-8")
        n = len(re.findall(r'class="[^"]*\btodo\b[^"]*"', h))
        # metadatos: <title> y cualquier content="…" (description, og:*)
        for m in re.findall(r"<title>(.*?)</title>", h, flags=re.S):
            if "TODO" in m:
                n += 1
        for m in re.findall(r'<meta[^>]*\bcontent="([^"]*)"', h):
            if "TODO" in m:
                n += 1
        if n:
            cuenta[nombre(p)] = n
    return cuenta


def metadatos() -> dict:
    """{página: {'titulo': …, 'descripcion': …}} tal como los ve un buscador."""
    datos = {}
    for p in htmls():
        h = p.read_text(encoding="utf-8")
        t = re.search(r"<title>(.*?)</title>", h, flags=re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', h)
        datos[nombre(p)] = {
            "titulo": t.group(1).strip() if t else None,
            "descripcion": d.group(1).strip() if d else None,
        }
    return datos


def metadatos_repetidos():
    """Títulos o descriptions compartidos entre páginas, y los que faltan.

    Dos páginas con el mismo <title> o la misma description es el fallo clásico
    de descubribilidad: buscadores y crawlers las tratan como duplicados y se
    quedan con una sola. Con seis subpáginas hermanas, generadas del mismo
    molde, es lo más fácil de que pase sin que nadie lo note.
    """
    datos = metadatos()
    problemas = []
    for campo, etiqueta in (("titulo", "<title>"),
                            ("descripcion", 'meta name="description"')):
        visto = {}
        for pagina, m in sorted(datos.items()):
            v = m[campo]
            if not v:
                problemas.append(f"{pagina}: no tiene {etiqueta}")
                continue
            visto.setdefault(v, []).append(pagina)
        for valor, paginas in visto.items():
            if len(paginas) > 1:
                corto = valor if len(valor) <= 48 else valor[:45] + "…"
                problemas.append(
                    f"{etiqueta} repetido en {', '.join(paginas)}: «{corto}»")
    return problemas


def sitemap_incompleto():
    """Páginas publicables que faltan en sitemap.xml (y URLs de más).

    La 404 queda afuera a propósito: lleva `noindex` y pedir que se indexe la
    página de error es lo contrario de lo que hace falta.
    """
    sm = RAIZ / "sitemap.xml"
    if not sm.exists():
        return ["no existe sitemap.xml -> python tools/make-sitemap.py"]

    listadas = set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>",
                              sm.read_text(encoding="utf-8")))
    esperadas = set()
    for p in htmls():
        rel = p.relative_to(RAIZ)
        if rel.as_posix() in NO_INDEXABLES:
            continue
        if p.name == "index.html":
            carpeta = rel.parent.as_posix()
            ruta = "/" if carpeta == "." else f"/{carpeta}/"
        else:
            ruta = "/" + rel.as_posix()
        esperadas.add(SITIO + ruta)

    problemas = []
    for u in sorted(esperadas - listadas):
        problemas.append(f"falta en el sitemap: {u}")
    for u in sorted(listadas - esperadas):
        problemas.append(f"sobra en el sitemap (no existe la página): {u}")
    # una página con noindex listada en el sitemap se contradice a sí misma
    for p in htmls():
        rel = p.relative_to(RAIZ).as_posix()
        h = p.read_text(encoding="utf-8")
        if re.search(r'<meta name="robots"[^>]*noindex', h):
            carpeta = p.relative_to(RAIZ).parent.as_posix()
            ruta = ("/" if carpeta == "." else f"/{carpeta}/") \
                if p.name == "index.html" else "/" + rel
            if SITIO + ruta in listadas:
                problemas.append(f"{rel} tiene noindex pero está en el sitemap")
    return problemas


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
