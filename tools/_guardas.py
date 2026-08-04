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


def url_propia(p: Path) -> str:
    """La URL canónica de una página, en el esquema por directorios del sitio."""
    rel = p.relative_to(RAIZ)
    if p.name == "index.html":
        carpeta = rel.parent.as_posix()
        return SITIO + ("/" if carpeta == "." else f"/{carpeta}/")
    return SITIO + "/" + rel.as_posix()


def urls_no_absolutas():
    """canonical, og:url y og:image tienen que ser ABSOLUTAS y apuntarse a sí mismas.

    Es EL fallo clásico de Open Graph: quien arma la vista previa —LinkedIn,
    Slack, X, WhatsApp— no es el navegador del lector y no tiene contra qué
    resolver una ruta relativa, así que la tarjeta sale sin imagen. No falla de
    forma visible en el sitio: falla afuera, donde nadie lo mira.

    Un canonical que apunta a otra página es peor que no tenerlo: le está
    diciendo al buscador que ésta no es la versión buena y que no la indexe.
    """
    problemas = []
    for p in htmls():
        h = p.read_text(encoding="utf-8")
        indexable = p.relative_to(RAIZ).as_posix() not in NO_INDEXABLES
        propia = url_propia(p)
        campos = {
            "canonical": re.search(r'<link rel="canonical" href="([^"]*)"', h),
            "og:url": re.search(r'<meta property="og:url" content="([^"]*)"', h),
            "og:image": re.search(r'<meta property="og:image" content="([^"]*)"', h),
        }
        for campo, m in campos.items():
            if m is None:
                if indexable:
                    problemas.append(f"{nombre(p)}: falta {campo}")
                continue
            v = m.group(1)
            if not v.startswith("https://"):
                problemas.append(f"{nombre(p)}: {campo} NO es absoluta: «{v}»")
            elif not v.startswith(SITIO + "/"):
                problemas.append(f"{nombre(p)}: {campo} apunta fuera del sitio: «{v}»")
            elif campo in ("canonical", "og:url") and v != propia:
                problemas.append(
                    f"{nombre(p)}: {campo} apunta a «{v}» y no a sí misma «{propia}»")
    return problemas


# --- og-image: detectar que quedó vieja -------------------------------------
# La imagen es un ARCHIVO, no una vista: no se re-renderiza sola. Si cambia algo
# de lo que la determina, el PNG sigue mostrando la versión anterior y nada
# avisa. Mismo problema que el sitemap; distinta solución, porque el sitemap se
# puede regenerar barato y comparar la SALIDA, y acá se comparan las ENTRADAS.
#
# LA LISTA TIENE QUE SER EXACTA EN LAS DOS DIRECCIONES. Una entrada de más
# significa avisos por cambios que ya no influyen — señal falsa, que es lo que
# hace que una guarda se deje de mirar. Una de menos significa que la imagen
# queda vieja en silencio, que es el fallo que esto viene a tapar.
#
# Vigentes desde que la tarjeta es puramente tipográfica (sin captura del cubo):
#   - el script, que define la composición entera;
#   - el :root de styles.css, que es de donde el script LEE los colores (por eso
#     no los copia: si los copiara, :root dejaría de ser una entrada real);
#   - las dos fuentes que se dibujan.
# Salieron de la lista al sacar el cubo:
#   - cube.js, que ya no aparece en la imagen;
#   - Cormorant, que ya no se usa (la bajada pasó a Inter por legibilidad).
# Se hashea el :root y no styles.css entero: el CSS cambia todo el tiempo por
# cosas que no tocan la tarjeta.
OG_LOCK = RAIZ / "tools" / "og-image.lock.json"
OG_FUENTES = ("zen-kaku-gothic-new-500", "inter-")


def og_entradas() -> dict:
    """{entrada: sha256} de todo lo que determina cómo se ve og-image.png.

    LOS ARCHIVOS DE TEXTO SE HASHEAN NORMALIZADOS, los binarios por bytes.
    No es un detalle: con `core.autocrlf=true` —el valor por defecto en Windows—
    git guarda LF en el repo y escribe CRLF al checkout. Hashear los bytes
    crudos de un .py hacía que la guarda avisara «la og-image quedó vieja» al
    cambiar de rama o al CLONAR DE NUEVO, cuando no había cambiado nada que
    mueva un solo píxel del PNG.

    Eso es una señal falsa, que es exactamente el modo de fallo que esta guarda
    existe para no tener; y encima rompía en el caso que motivó hashear
    contenido en vez de fechas, que era justamente sobrevivir a un clon.

    Las fuentes siguen por bytes a propósito: son binarias, git no las convierte
    y ahí el byte crudo SÍ es el contenido.
    """
    import hashlib

    def sha(datos: bytes) -> str:
        return hashlib.sha256(datos).hexdigest()[:16]

    def sha_texto(ruta) -> str:
        # read_text() aplica universal newlines: CRLF y CR entran como LF.
        return sha(ruta.read_text(encoding="utf-8").encode("utf-8"))

    entradas = {}
    css = RAIZ / "assets" / "css" / "styles.css"
    if css.exists():
        m = re.search(r":root\s*\{.*?\n\}", css.read_text(encoding="utf-8"), flags=re.S)
        entradas["styles.css :root"] = sha(m.group(0).encode("utf-8")) if m else "SIN-:root"

    gen = RAIZ / "tools" / "make-og-image.py"
    if gen.exists():
        entradas["make-og-image.py"] = sha_texto(gen)

    for f in sorted((RAIZ / "assets" / "fonts").glob("*.woff2")):
        if f.name.startswith(OG_FUENTES):
            entradas["fuente " + f.name] = sha(f.read_bytes())
    return entradas


def og_desactualizada():
    """Entradas que cambiaron desde que se generó la imagen."""
    salida = RAIZ / "og-image.png"
    if not salida.exists():
        return ["no existe og-image.png -> python tools/make-og-image.py"]
    if not OG_LOCK.exists():
        return ["no existe tools/og-image.lock.json -> python tools/make-og-image.py"]

    import json
    guardado = json.loads(OG_LOCK.read_text(encoding="utf-8")).get("entradas", {})
    actual = og_entradas()
    cambiadas = [k for k in sorted(set(actual) | set(guardado))
                 if actual.get(k) != guardado.get(k)]
    if not cambiadas:
        return []
    return [f"og-image.png quedó vieja: cambió {', '.join(cambiadas)}"]


def sellar_og():
    import json
    OG_LOCK.write_text(json.dumps(
        {"_comentario": "Generado por tools/make-og-image.py. Hashes de lo que "
                        "determina cómo se ve og-image.png; check-structure "
                        "avisa si alguno cambió. No editar a mano.",
         "entradas": og_entradas()},
        ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


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


# Acá vivían MARCA_BORRADOR y disclaimer_sin_revisar(), que bloqueaban la
# publicación mientras /disclaimer/ llevara una marca de borrador en su HTML.
#
# SE ELIMINARON PORQUE LA CONDICIÓN QUE VIGILABAN YA NO EXISTE: el autor decidió
# publicar el 免責事項 sin revisión de un profesional legal japonés. No es que la
# guarda estorbara — es que ya no queda nada que esperar, y una guarda que vigila
# una espera que terminó sólo enseña a ignorar su salida.
#
# El motivo de la decisión, con el marco legal que la sostiene, está en CLAUDE.md.
# Si algún día se decide sí mandarlo a revisar, esto se reconstruye en veinte
# líneas; lo que no hay que reconstruir es la lección que dejó, que sigue escrita
# en el README: la marca tiene que ser un TOKEN SIN ESPACIOS, porque una frase se
# parte en el salto de línea de un comentario HTML y deja de encontrarse. La
# primera versión decía «revisado» con el borrador intacto.


def hrefs_muertos():
    """Un href="#" no navega a ningún lado: es un enlace muerto.

    Se ADMITE mientras el ancla lleve adentro un placeholder que lo anuncie —
    eso es andamiaje declarado, y check-ready ya impide publicar mientras queden
    placeholders. Lo que esta guarda ataja es el caso SILENCIOSO: que alguien
    redacte el rótulo, borre el TODO y se olvide de pegar la URL. En ese momento
    el placeholder desaparece, todas las guardas se ponen verdes y el enlace
    queda muerto sin que nadie se entere.

    O sea que falla exactamente cuando empieza a importar, y no antes. Existe
    porque hoy /sugao/ tiene el href de LinkedIn pendiente de que lo complete
    Manuel; si algún día no queda ningún href="#", esta guarda no molesta.
    """
    problemas = []
    for p in htmls():
        h = p.read_text(encoding="utf-8")
        for m in re.finditer(r'<a\b[^>]*href="#"[^>]*>.*?</a>', h, flags=re.S):
            if 'class="todo"' not in m.group(0):
                problemas.append(
                    f'{nombre(p)}: href="#" ya sin placeholder — el enlace quedó muerto')
    return problemas


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
