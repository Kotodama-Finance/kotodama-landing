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
# Una página que declara noindex no existe para buscadores NI para el mapa del
# footer: la meta en la PROPIA página es la única fuente de verdad — criterio
# generalizado de la 404 el 2026-08-07; el caso vivo es el andamiaje de
# seguros mientras sea placeholder. make-sitemap deriva de acá.
RE_NOINDEX = re.compile(r'<meta name="robots"[^>]*noindex')
# Rango de caracteres japoneses: puntuación CJK (U+3000-303F: espacio
# ideográfico, 、y 。), kana, kanji, y formas de ancho completo (U+FF00-FFEF:
# los paréntesis （） y todo el bloque). ENSANCHADO el 2026-08-06: la versión
# anterior ([぀-ヿ㐀-鿿　]) no miraba puntuación ni full-width, así que 、
# (U+3001, en un nombre de fuente de /method/) faltó del subset CON la guarda
# en verde — se dibujaba con fuente del sistema por el fallback por glifo, y
# los （） de la vez pasada tampoco estaban vigilados. Mismo criterio que
# japones() en check-maintenance.py: si se toca acá, tocar allá.
JAPONES = re.compile(r"[　-〿぀-ヿ㐀-鿿＀-￯]")
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


def sin_comentarios(html: str) -> str:
    """HTML sin comentarios, para las regex que miran MARCADO VIVO.

    Las búsquedas del mapa y del noindex tienen que ignorar comentarios: una
    tarjeta comentada no presenta nada, y un comentario que meramente CITA
    `<meta name="kotodama-type" content="note">` no convierte la página en
    nota — lo probó la revisión adversarial del mapa (2026-08-07): sin esto,
    comentar una tarjeta evadía el abort y una cita en comentario sacaba a
    /musubi/ del mapa en silencio. `placeholders()` NO usa esto A PROPÓSITO:
    su conteo-dentro-de-comentarios es el quirk documentado del andamiaje de
    seguros, y cambiarlo movería el baseline.
    """
    return re.sub(r"<!--.*?-->", " ", html, flags=re.S)


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
    página de error es lo contrario de lo que hace falta. Y desde el
    2026-08-07 CUALQUIER página con `noindex` queda afuera de las esperadas
    — el mismo criterio derivado que usa make-sitemap: la meta en la página
    es la única fuente de verdad. Las dos direcciones quedan vigiladas:
    noindex listada en el sitemap es la contradicción de abajo, y sacar el
    noindex sin regenerar el sitemap cae en «falta en el sitemap»."""
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
        if RE_NOINDEX.search(sin_comentarios(p.read_text(encoding="utf-8"))):
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
        h = sin_comentarios(p.read_text(encoding="utf-8"))
        if RE_NOINDEX.search(h):
            carpeta = p.relative_to(RAIZ).parent.as_posix()
            ruta = ("/" if carpeta == "." else f"/{carpeta}/") \
                if p.name == "index.html" else "/" + rel
            if SITIO + ruta in listadas:
                problemas.append(f"{rel} tiene noindex pero está en el sitemap")
    return problemas


# --- El mapa del sitio: la subpágina /sitemap/ -------------------------------
# El árbol completo vive en UNA página, /sitemap/, y el footer lleva sólo un
# enlace («Site map», en la línea de abajo, vigilado por la identidad del
# footer). ESTO REVIERTE el bloque-en-los-quince-footers del mismo día, por
# decisión del autor: un árbol de tantas entradas repetido en todas las
# páginas es demasiado footer, y crece con cada sección nueva.
#
# El bloque de la página lo GENERA tools/make-sitemap.py en la misma corrida
# que escribe sitemap.xml. Nada se escribe a mano: las URLs son el MISMO
# conjunto que el sitemap (sin la 404 ni las noindex — paginas_publicas es la
# fuente común), los nombres salen del face-page__romaji con que cada página
# se presenta en su h1 («Home» para la portada, cuyo h1 es el titular del
# hero, no un nombre), y el orden de los hijos es el orden en que el PADRE los
# presenta como tarjetas .face-card (la grilla del cubo para las seis caras;
# .face-page__cards para las subcaras). Lo único que no se puede derivar es
# el orden de las páginas de nivel superior que no son caras —un orden es una
# decisión de presentación—, y por eso ORDEN_SITIO existe COMO LISTA CON
# GUARDA: una página que no esté ni en tarjetas ni acá ni declarada nota
# ABORTA la generación nombrándola, en vez de caer a un orden inventado.
# Y EL ABORT NO ES UN CHEQUEO AGREGADO ENCIMA — es consecuencia del diseño
# (el autor, 2026-08-07): el orden del mapa se DERIVA del orden de las
# tarjetas, así que sin tarjeta NO HAY orden derivable, y caer a alfabético
# sería una decisión de presentación que no tomó nadie. La fricción de
# «agregá la tarjeta primero» es el diseño diciendo que la puerta de
# navegación va antes que el listado.
# /sitemap/ se lista A SÍ MISMA (vía ORDEN_SITIO) y va al sitemap.xml: es una
# página indexable más, y una excepción rompería el conjunto único. Kanji NO
# lleva: en una lista densa el kanji junto al romaji sólo duplicaría el
# nombre de al lado — la prueba del japonés ornamental de la prosa de
# /hajime/, y la nav ya escribe «Musubi» pelado.
#
# LAS NOTAS FUTURAS NO ENTRAN AL MAPA (decisión del autor, 2026-08-07): con
# veinte notas sería una lista interminable. En su lugar entrará LA PÁGINA DE
# ARCHIVO cuando exista — sin mecanismo especial: es una página normal, el
# descubrimiento la encuentra y el abort obliga a ubicarla conscientemente en
# ORDEN_SITIO. Una nota se declara con <meta name="kotodama-type"
# content="note"> EN SU PROPIO HTML, desde la primera: la ruta sola no
# distingue una nota de una subcara (viven al mismo nivel bajo /hajime/), así
# que la distinción es una declaración explícita — y el abort hace imposible
# crear una sin declararla: ni tarjeta ni marca es rojo con nombre. Las notas
# SÍ van a sitemap.xml (son contenido indexable); sólo el mapa las resume en
# la entrada del archivo.

RE_NOTA = re.compile(r'<meta name="kotodama-type" content="note"')
RE_ROMAJI_H1 = re.compile(r'<span class="face-page__romaji[^"]*">([^<]*)</span>')
ORDEN_SITIO = ("musubi", "method", "sitemap", "disclaimer")
RUTA_MAPA = "sitemap/index.html"


def tarjetas_de(html: str) -> list:
    """hrefs de los <a> con clase face-card, en orden de aparición.

    Tolera el orden de los atributos y las clases compuestas (el precedente
    es RE_ROMAJI_H1, que tolera «face-page__romaji todo»): un href-antes-de-
    class o un «face-card face-card--x» son marcado válido que renderiza
    idéntico, y la primera versión —regex de orden exacto— abortaba con un
    diagnóstico FALSO («no la presenta como tarjeta» con la tarjeta a la
    vista). Lo cazó la revisión adversarial del mapa (2026-08-07).
    """
    hrefs = []
    for m in re.finditer(r"<a\b[^>]*>", html):
        tag = m.group(0)
        if re.search(r'class="[^"]*\bface-card\b[^"]*"', tag):
            h = re.search(r'href="([^"]+)"', tag)
            if h:
                hrefs.append(h.group(1))
    return hrefs
MAPA_INI = "<!-- MAPA DEL SITIO"
MAPA_FIN = "<!-- FIN DEL MAPA DEL SITIO -->"


class MapaInconstruible(Exception):
    """El mapa no se puede derivar completo; el mensaje nombra qué falta."""


def paginas_publicas():
    """[(Path, ruta)] de las páginas que existen para un lector.

    El MISMO conjunto que lista sitemap.xml — make-sitemap deriva de acá, así
    que el sitemap y el mapa del footer no pueden divergir: la 404 y las
    páginas noindex quedan afuera por el mismo criterio en el mismo lugar.
    """
    filas = []
    for p in htmls():
        rel = p.relative_to(RAIZ)
        if rel.as_posix() in NO_INDEXABLES:
            continue
        if RE_NOINDEX.search(sin_comentarios(p.read_text(encoding="utf-8"))):
            continue
        if p.name == "index.html":
            carpeta = rel.parent.as_posix()
            ruta = "/" if carpeta == "." else f"/{carpeta}/"
        else:
            ruta = "/" + rel.as_posix()
        filas.append((p, ruta))
    return filas


def mapa_bloque() -> str:
    """El bloque canónico del mapa, marcadores incluidos, con sangría de footer.

    Deriva TODO y aborta (MapaInconstruible) ante lo que no puede derivar:
    página sin nombre, página que su padre no presenta como tarjeta, página de
    nivel superior fuera de ORDEN_SITIO. Un mapa que adivina es peor que uno
    que frena: el hueco se publicaría idéntico en todas las páginas.
    """
    html_de, paginas = {}, {}
    for p, ruta in paginas_publicas():
        # Sin comentarios: las regex de acá abajo miran marcado VIVO — una
        # tarjeta comentada no presenta nada, y citar la meta de nota en un
        # comentario no convierte la página en nota (ver sin_comentarios).
        h = sin_comentarios(p.read_text(encoding="utf-8"))
        if RE_NOTA.search(h):
            continue  # las notas no entran; las listará la página de archivo
        paginas[ruta] = p
        html_de[ruta] = h

    def etiqueta(ruta):
        if ruta == "/":
            return "Home"
        m = RE_ROMAJI_H1.search(html_de[ruta])
        if not m or not m.group(1).strip() or "TODO" in m.group(1):
            raise MapaInconstruible(
                f"{ruta}: sin face-page__romaji del que derivar su nombre para el mapa")
        return m.group(1).strip()

    def padre(ruta):
        # El ancestro más cercano CON página: /hajime/yorozu/japan/seguros/
        # cuelga de /hajime/yorozu/, porque /japan/ no lleva página (decisión).
        partes = ruta.strip("/").split("/")
        for corte in range(len(partes) - 1, 0, -1):
            r = "/" + "/".join(partes[:corte]) + "/"
            if r in paginas:
                return r
        return "/"

    hijos = {}
    for ruta in paginas:
        if ruta != "/":
            hijos.setdefault(padre(ruta), []).append(ruta)

    def orden_tarjetas(ruta_padre, lista):
        """(en el orden de las tarjetas del padre, lo que el padre no presenta).

        Un mismo destino tarjeteado DOS veces aborta: el duplicado se
        publicaría como entrada repetida en el mapa de todas las páginas, con
        todas las guardas en verde (mapa_desactualizado compara contra esta
        misma derivación). Reproducido por la revisión adversarial.
        """
        tarjetas = tarjetas_de(html_de[ruta_padre])
        repetidas = sorted({u for u in tarjetas
                            if u in lista and tarjetas.count(u) > 1})
        if repetidas:
            raise MapaInconstruible(
                f"{ruta_padre}: presenta {', '.join(repetidas)} como tarjeta "
                f"MÁS DE UNA VEZ — el mapa duplicaría la entrada en todas las "
                f"páginas; dejar una sola tarjeta por destino")
        return ([u for u in tarjetas if u in lista],
                [u for u in lista if u not in tarjetas])

    def arbol(ruta, sangria):
        s = " " * sangria
        propios = hijos.get(ruta, [])
        if not propios:
            return [f'{s}<li><a href="{ruta}">{etiqueta(ruta)}</a></li>']
        en_tarjetas, sueltos = orden_tarjetas(ruta, propios)
        if sueltos:
            raise MapaInconstruible(
                f"{', '.join(sorted(sueltos))}: bajo {ruta} pero {ruta} no la "
                f"presenta como tarjeta — agregarle su .face-card, o declararla "
                f'nota con <meta name="kotodama-type" content="note">')
        lineas = [f'{s}<li><a href="{ruta}">{etiqueta(ruta)}</a>',
                  f'{s}  <ul class="map-list map-list--sub">']
        for h in en_tarjetas:
            lineas += arbol(h, sangria + 4)
        lineas += [f"{s}  </ul>", f"{s}</li>"]
        return lineas

    caras, sueltos_raiz = orden_tarjetas("/", hijos.get("/", []))
    sitio = [f"/{slug}/" for slug in ORDEN_SITIO if f"/{slug}/" in sueltos_raiz]
    sin_lugar = sorted(set(sueltos_raiz) - set(sitio))
    # EL AUTOENLACE SE VA (2026-08-08, decisión del autor): la entrada «Site
    # map» enlazaría a la página que el lector ya está mirando — este bloque
    # se renderiza SOLO en /sitemap/, así que la exclusión es incondicional y
    # la entrada DESAPARECE (no queda como texto plano). Es una exclusión del
    # RENDERIZADO nada más: paginas_publicas() no se toca, sitemap.xml sigue
    # listando /sitemap/ (página indexable legítima que Google ya conoce) y
    # el slug SIGUE en ORDEN_SITIO — sin su lugar ahí, el abort de
    # nivel-superior-sin-lugar frenaría la generación. La guarda
    # (mapa_desactualizado) compara contra esta MISMA función, así que sigue
    # el cambio sola. Si /sitemap/ tuviera HIJOS algún día, esta exclusión
    # también los escondería: ese día se decide de nuevo, no antes.
    ruta_propia = "/" + RUTA_MAPA.rsplit("/", 1)[0] + "/"
    sitio = [r for r in sitio if r != ruta_propia]
    if sin_lugar:
        raise MapaInconstruible(
            f"{', '.join(sin_lugar)}: página(s) de nivel superior sin lugar en el "
            f"mapa — para un directorio, sumar su slug a ORDEN_SITIO en "
            f"tools/_guardas.py (o, si es una cara, darle su tarjeta en la "
            f"grilla de la portada); un .html suelto en la raíz NO tiene lugar "
            f"posible —el sitio es URLs por directorios—: moverlo a su "
            f"directorio, declararlo nota, o sacarlo")

    # «The Site» ANTES que «The Cube» (orden del autor, 2026-08-07).
    lineas = [
        "      " + MAPA_INI + " — lo GENERA tools/make-sitemap.py; no editar a",
        "           mano: la próxima regeneración lo pisa. Mismo conjunto de",
        "           URLs que sitemap.xml MENOS esta misma página (el",
        "           autoenlace se quitó a propósito), nombres del",
        "           face-page__romaji de cada página, orden de las tarjetas",
        "           del padre. check-structure avisa si quedó viejo. -->",
        '      <section class="face-page__section" aria-labelledby="map-site">',
        '        <h2 id="map-site" class="face-page__subtitle">The Site</h2>',
        '        <ul class="map-list">',
        '          <li><a href="/">Home</a></li>',
    ]
    for ruta in sitio:
        lineas += arbol(ruta, 10)
    lineas += [
        "        </ul>",
        "      </section>",
        '      <section class="face-page__section" aria-labelledby="map-cube">',
        '        <h2 id="map-cube" class="face-page__subtitle">The Cube</h2>',
        '        <ul class="map-list">',
    ]
    for cara in caras:
        lineas += arbol(cara, 10)
    lineas += [
        "        </ul>",
        "      </section>",
        "      " + MAPA_FIN,
    ]
    return "\n".join(lineas)


def mapa_desactualizado():
    """El bloque de /sitemap/ contra el canónico que el generador escribiría hoy.

    La página es UNA, así que acá no hay divergencia entre copias que vigilar
    (el enlace del footer sí está en todas, y ése lo cubre chrome_divergente):
    lo que esta comprobación ve es el caso viejo-en-silencio — se agregó o
    redactó una página y nadie regeneró — y el caso peor, que la página del
    mapa no exista o haya perdido sus marcadores.
    """
    try:
        esperado = mapa_bloque()
    except MapaInconstruible as e:
        return [str(e)]
    p = RAIZ / RUTA_MAPA
    if not p.exists():
        return [f"no existe {RUTA_MAPA} — la página del mapa del sitio"]
    h = p.read_text(encoding="utf-8")
    a, b = h.find(MAPA_INI), h.find(MAPA_FIN)
    if a < 0 or b < 0:
        return [f"{RUTA_MAPA}: perdió los marcadores del bloque generado"]
    ini = h.rfind("\n", 0, a) + 1  # el canónico arranca con la sangría
    if h[ini:b + len(MAPA_FIN)] != esperado:
        return [f"{RUTA_MAPA}: el mapa quedó viejo"]
    return []


# --- El sistema de notas: feed en la portada, archivo /notes/, índice -------
# (2026-08-07, decidido por el autor.) Las notas viven en /hajime/<slug>/ y se
# declaran con la meta kotodama-type=note (RE_NOTA, arriba — la marca ya
# existía por el mapa). TODO el metadato sale del HTML de la propia nota, cero
# archivos laterales — el mismo criterio que el noindex del sitemap:
#   tipo    -> la meta kotodama-type
#   cara    -> la meta kotodama-face (una de las seis)
#   título  -> el <h1> de la nota
#   slug    -> el nombre del directorio
#   fecha   -> el primer <time datetime="YYYY-MM-DD"> (visible al lector Y
#              legible por máquina: es el primer elemento temporal del sitio)
#   resumen -> el párrafo lead, marcado con la clase note-lead. NO hay campo
#              summary aparte ni override: un solo texto no puede
#              contradecirse con el del feed. Si el lead no funciona suelto,
#              se reescribe el lead.
#
# UN generador (make-notes.py), UNA pasada, TRES salidas: el feed de la
# portada (entre centinelas — index.html sigue siendo de mano salvo ese
# bloque), el listado de /notes/ (ídem) y notes/search-index.json. La lógica
# vive acá para que la guarda compare contra EXACTAMENTE lo que el generador
# escribiría — el patrón del mapa, sin segunda implementación.
#
# QUÉ ENTRA: el criterio es paginas_publicas(), el mismo del sitemap y el
# mapa — una nota con noindex (andamiaje) no existe para ningún consumidor.
# Con CERO notas publicables los bloques quedan en solo-marcadores (ninguna
# caja vacía en la portada) y el índice queda sin entradas.
# REGLA DURA: el feed REFERENCIA la nota (título + lead + read more), nunca
# copia el cuerpo. El índice del buscador SÍ lleva el texto completo — es la
# herramienta de búsqueda por contenido, no un segundo lugar donde leerla.

RE_NOTA_FACE = re.compile(r'<meta name="kotodama-face" content="([^"]*)"')
RE_NOTA_FECHA = re.compile(r'<time datetime="(\d{4}-\d{2}-\d{2})"[^>]*>([^<]*)</time>')
RE_NOTA_LEAD = re.compile(r'<p class="[^"]*\bnote-lead\b[^"]*"[^>]*>(.*?)</p>', re.S)
RE_NOTA_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
RE_NOTA_MAIN = re.compile(r"<main>(.*?)</main>", re.S)
FEED_INI = "<!-- FEED DE NOTAS"
FEED_FIN = "<!-- FIN DEL FEED DE NOTAS -->"
LISTA_INI = "<!-- LISTADO DE NOTAS"
LISTA_FIN = "<!-- FIN DEL LISTADO DE NOTAS -->"
RUTA_PORTADA = "index.html"
RUTA_NOTAS = "notes/index.html"
RUTA_INDICE = "notes/search-index.json"
# Las últimas N en la portada; el archivo lista todas. Es una perilla, no un
# dogma: 3 mantiene el feed como escaparate y no como segundo archivo — el
# antecedente es el mapa en los quince footers, que murió por crecer sin tope.
FEED_MAX = 3
CARAS_ROMAJI = {"hajime": "Hajime", "sugao": "Sugao", "tosei": "Tosei",
                "kamon": "Kamon", "torii": "Torii", "kizuna": "Kizuna"}


class NotaInvalida(Exception):
    """El contrato de una nota no se cumple; el mensaje nombra página y campo."""


def notas_publicables():
    """[dict] de las notas publicables (declaradas Y sin noindex), nuevas primero.

    Valida el contrato completo y aborta (NotaInvalida) nombrando la página y
    el campo: un hueco o un «TODO» inyectado en la portada es peor que frenar
    — el mismo todo-o-nada del mapa. Las notas noindex (andamiaje) no llegan
    acá: quedan afuera por paginas_publicas, igual que en sitemap y mapa.
    """
    import html as _html
    notas = []
    for p, ruta in paginas_publicas():
        h = sin_comentarios(p.read_text(encoding="utf-8"))
        if not RE_NOTA.search(h):
            continue
        if not re.fullmatch(r"/hajime/[^/]+/", ruta):
            raise NotaInvalida(
                f"{ruta}: declara kotodama-type=note pero no vive en "
                f"/hajime/<slug>/ — las notas cuelgan de Hajime, no del árbol "
                f"sectorial (decisión del autor); mover la página o quitarle "
                f"la marca")
        m = RE_NOTA_H1.search(h)
        titulo = ""
        if m:
            titulo = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()
        if not titulo or "TODO" in titulo:
            raise NotaInvalida(f"{ruta}: sin <h1> del que derivar el título "
                               f"(o todavía es TODO) — el título ES el h1")
        m = RE_NOTA_FACE.search(h)
        if not m or m.group(1) not in CARAS_ROMAJI:
            raise NotaInvalida(
                f"{ruta}: sin <meta name=\"kotodama-face\"> válida — declarar "
                f"una de: {', '.join(CARAS_ROMAJI)}")
        cara = m.group(1)
        m = RE_NOTA_FECHA.search(h)
        if not m or not m.group(2).strip():
            raise NotaInvalida(
                f"{ruta}: sin <time datetime=\"YYYY-MM-DD\"> con texto visible "
                f"— la fecha es del lector Y de la máquina, no una sola")
        fecha, fecha_visible = m.group(1), " ".join(m.group(2).split())
        m = RE_NOTA_LEAD.search(h)
        lead = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        if not lead or "TODO" in lead:
            raise NotaInvalida(
                f"{ruta}: sin párrafo lead con la clase note-lead (o todavía "
                f"es TODO) — el lead ES el resumen del feed y del archivo")
        mm = RE_NOTA_MAIN.search(h)
        texto = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                                           mm.group(1) if mm else h)).strip()
        notas.append({"ruta": ruta, "titulo": titulo, "cara": cara,
                      "fecha": fecha, "fecha_visible": fecha_visible,
                      "lead_html": lead,
                      "titulo_plano": _html.unescape(titulo),
                      "lead_plano": _html.unescape(
                          re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", lead)).strip()),
                      "texto": _html.unescape(texto)})
    notas.sort(key=lambda n: (n["fecha"], n["ruta"]), reverse=True)
    return notas


def feed_bloque(notas) -> str:
    """El bloque canónico del feed de la portada, centinelas incluidos.

    Con cero notas publicables: SOLO los centinelas — ninguna caja vacía en la
    portada. El feed referencia (título + lead + read more), nunca copia el
    cuerpo; muestra las últimas FEED_MAX y manda el resto a /notes/.
    """
    cab = [
        "    " + FEED_INI + " — lo GENERA tools/make-notes.py; no editar a",
        "         mano: la próxima regeneración lo pisa. Título + lead (el",
        "         resumen ES el lead de la nota, sin campo aparte) + read",
        f"         more; las últimas {FEED_MAX}, el resto en /notes/. Con cero",
        "         notas publicables queda VACÍO a propósito: ninguna caja",
        "         vacía. check-structure avisa si quedó viejo. -->",
    ]
    if not notas:
        return "\n".join(cab + ["    " + FEED_FIN])
    lineas = cab + [
        '    <section id="notes" class="notes-feed">',
        '      <div class="notes-feed__wrap">',
        '        <p class="eyebrow">Notes</p>',
        '        <ul class="notes-feed__list">',
    ]
    for n in notas[:FEED_MAX]:
        lineas += [
            "          <li>",
            f'            <h3 class="notes-feed__title"><a href="{n["ruta"]}">{n["titulo"]}</a></h3>',
            f'            <p class="notes-feed__lead">{n["lead_html"]}</p>',
            f'            <p class="notes-feed__more"><a href="{n["ruta"]}">Read more &rarr;</a></p>',
            "          </li>",
        ]
    lineas += [
        "        </ul>",
        '        <p class="notes-feed__all"><a href="/notes/">All notes &rarr;</a></p>',
        "      </div>",
        "    </section>",
        "    " + FEED_FIN,
    ]
    return "\n".join(lineas)


def listado_bloque(notas) -> str:
    """El bloque canónico del listado de /notes/, centinelas incluidos.

    Cara y fecha por ítem (el vocabulario de rotulado por ítem de /method/,
    con el romaji de la cara como rótulo legible — un cuadrado para seis caras
    no distingue nada); data-url es la clave con la que el buscador
    (assets/js/notes.js) empareja cada fila con su entrada del índice.
    """
    cab = [
        "        " + LISTA_INI + " — lo GENERA tools/make-notes.py; no editar",
        "             a mano: la próxima regeneración lo pisa. data-url es la",
        "             clave que el buscador usa para emparejar cada fila con",
        "             el índice JSON. check-structure avisa si quedó viejo. -->",
    ]
    if not notas:
        return "\n".join(cab + ["        " + LISTA_FIN])
    lineas = cab + ['        <ul class="notes-list">']
    for n in notas:
        lineas += [
            f'          <li class="note-item" data-url="{n["ruta"]}">',
            f'            <a class="note-item__link" href="{n["ruta"]}">',
            f'              <span class="note-item__title">{n["titulo"]}</span>',
            f'              <span class="note-item__tags">'
            f'<span class="note-item__face">{CARAS_ROMAJI[n["cara"]]}</span>'
            f' &middot; <time datetime="{n["fecha"]}">{n["fecha_visible"]}</time></span>',
            f'              <span class="note-item__lead">{n["lead_html"]}</span>',
            "            </a>",
            "          </li>",
        ]
    lineas += ["        </ul>", "        " + LISTA_FIN]
    return "\n".join(lineas)


def indice_notas(notas) -> str:
    """El texto EXACTO de notes/search-index.json (para escribir Y comparar).

    En inglés: el JSON se sirve tal cual — superficie publicada, como el
    comentario del sitemap.xml. Lleva el texto completo de cada nota porque
    ES el índice de búsqueda por contenido; no es una copia del feed.
    """
    datos = {
        "_generated": "tools/make-notes.py - do not edit by hand; "
                      "check-structure.py verifies it is current.",
        "notes": [{"url": n["ruta"], "title": n["titulo_plano"],
                   "face": n["cara"], "date": n["fecha"],
                   "lead": n["lead_plano"], "text": n["texto"]}
                  for n in notas],
    }
    return json.dumps(datos, ensure_ascii=False, indent=1) + "\n"


def notas_desactualizadas():
    """Los tres artefactos de notas contra lo que el generador escribiría hoy.

    El mismo patrón que mapa_desactualizado: misma derivación, sin segunda
    implementación. Ve el caso viejo-en-silencio (nota agregada o redactada
    sin regenerar) y el peor: centinelas perdidos o artefacto ausente.
    """
    try:
        notas = notas_publicables()
    except NotaInvalida as e:
        return [str(e)]
    problemas = []
    for ruta_arch, ini, fin, canon in (
            (RUTA_PORTADA, FEED_INI, FEED_FIN, feed_bloque(notas)),
            (RUTA_NOTAS, LISTA_INI, LISTA_FIN, listado_bloque(notas))):
        p = RAIZ / ruta_arch
        if not p.exists():
            problemas.append(f"no existe {ruta_arch}")
            continue
        h = p.read_text(encoding="utf-8")
        a, b = h.find(ini), h.find(fin)
        if a < 0 or b < 0:
            problemas.append(f"{ruta_arch}: perdió los centinelas del bloque de notas")
            continue
        i = h.rfind("\n", 0, a) + 1
        if h[i:b + len(fin)] != canon:
            problemas.append(f"{ruta_arch}: el bloque de notas quedó viejo")
    p = RAIZ / RUTA_INDICE
    if not p.exists():
        problemas.append(f"no existe {RUTA_INDICE}")
    elif p.read_text(encoding="utf-8") != indice_notas(notas):
        problemas.append(f"{RUTA_INDICE}: el índice del buscador quedó viejo")
    return problemas


def leer_baseline():
    """None = NO HAY archivo. {} = hay archivo y dice CERO placeholders.

    La distinción no es cosmética y costó un rojo. Antes esto devolvía {} en los
    dos casos y quien llamaba hacía `if not base`, así que un baseline vacío se
    leía como baseline ausente. Mientras quedaban placeholders eso no se notaba
    nunca; el día que la redacción terminó, el baseline legítimo pasó a ser {} y
    la guarda empezó a fallar sin que nada estuviera roto.

    Es un caso borde que sólo puede ocurrir UNA vez —al terminar— y por eso
    sobrevivió a todas las corridas anteriores: la guarda funcionaba en todos
    los estados menos en el estado final.
    """
    if not BASELINE.exists():
        return None
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


def noindex_olvidado():
    """Páginas SIN placeholders que siguen llevando noindex (la 404 no cuenta).

    La mitad silenciosa del noindex-mientras-placeholder (2026-08-07): mientras
    una página es andamiaje, su noindex es deliberado — que un deploy
    intermedio no publique TODOs en los resultados de búsqueda—; redactada, un
    noindex olvidado la publica invisible PARA SIEMPRE y ninguna otra guarda lo
    ve: placeholders en cero, sitemap consistente (la noindex queda afuera de
    las esperadas), todo verde. Igual que hrefs_muertos, esto falla exactamente
    cuando empieza a importar y no antes.
    """
    con_todo = placeholders()
    problemas = []
    for p in htmls():
        rel = nombre(p)
        if rel in NO_INDEXABLES or rel in con_todo:
            continue
        if RE_NOINDEX.search(sin_comentarios(p.read_text(encoding="utf-8"))):
            problemas.append(f"{rel}: lleva noindex y ya no tiene placeholders — "
                             f"sacar la meta (con su comentario) y regenerar el sitemap")
    return problemas


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


# --- Castellano en lo que se publica ----------------------------------------
# El sitio está en inglés y el repo se trabaja en castellano. La frontera entre
# las dos cosas es invisible: un comentario en castellano es correcto, la misma
# frase en un `content=` viaja en cada enlace compartido. Ya pasó — og:image:alt
# decía «El cubo de seis caras de Kotodama Finance» en las diez páginas.
#
# LA IDEA NO ES DETECTAR CASTELLANO EN EL REPO, sino AISLAR LA SUPERFICIE
# PUBLICABLE —que es finita— y mirar sólo ahí. Sobre ese conjunto reducido, un
# detector simple alcanza para las regresiones.
#
# QUÉ NO ATRAPA, y hay que decirlo porque una guarda que aparenta completitud es
# peor que ninguna: castellano sin diacríticos y sin ninguna de las palabras de
# abajo. Concretamente se le escapó «no se pudo hidratar; se mantiene la grilla»
# —ni una palabra de la lista, ni un acento—, que apareció por inspección
# dirigida a console.*. Esta guarda cubre la reincidencia de lo conocido, no
# reemplaza leer la superficie cuando se agrega una página.
CASTELLANO = """
 el los las del que con para por una unos unas este esta esto estos estas
 ese esa esos esas cada cuando donde como pero aunque entre hacia desde hasta
 muy todo toda todos todas otro otra otros otras estan tiene tienen sus segun
 tambien asi aqui porque cual cuales quien quienes cubo caras pagina paginas
 texto nombre nombres linea lineas seccion descripcion titulo rotulo enlace
 enlaces frase frases volver acerca pudo mantiene grilla perdido rehidratando
""".split()
# Se dejan FUERA a propósito: no, son, sin, hay, era, solo, van, la, de, a, o.
# Todas son palabras inglesas y darían falso positivo, que es la forma en que
# una guarda se vuelve ruido y se deja de mirar.
RE_CASTELLANO = re.compile(r"\b(" + "|".join(CASTELLANO) + r")\b", re.I)
RE_DIACRITICOS = re.compile(r"[áéíóúÁÉÍÓÚñÑ¿¡]")

ATRIBUTOS_VISIBLES = ("content", "alt", "aria-label", "title", "placeholder")
RE_ATRIBUTO = re.compile(
    r"\b(" + "|".join(ATRIBUTOS_VISIBLES) + r")\s*=\s*\"([^\"]*)\"", re.I)


def superficie_publicada():
    """[(origen, contexto, texto)] de todo lo que llega a un lector o crawler.

    Deja afuera a propósito los comentarios de HTML/CSS/JS, tools/, los .md y
    _ref/: están en castellano por decisión y no se publican.
    """
    filas = []
    for p in htmls():
        n, html = nombre(p), p.read_text(encoding="utf-8")
        sin_com = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
        for linea in texto_visible(html).splitlines():
            t = " ".join(linea.split())
            if t:
                filas.append((n, "texto visible", t))
        m = re.search(r"<title>(.*?)</title>", sin_com, flags=re.S | re.I)
        if m:
            filas.append((n, "<title>", m.group(1).strip()))
        for attr, val in RE_ATRIBUTO.findall(sin_com):
            if val.strip():
                filas.append((n, "@" + attr.lower(), val.strip()))

    # notes.js entró con el buscador del archivo (2026-08-07): sus strings son
    # superficie igual que las de main.js — la consola y los rótulos que él
    # mismo destapa. Al agregar OTRO .js publicado, sumarlo acá.
    for rel in ("assets/js/main.js", "assets/js/cube.js", "assets/js/notes.js"):
        f = RAIZ / rel
        if not f.exists():
            continue
        src = re.sub(r"/\*.*?\*/", " ", f.read_text(encoding="utf-8"), flags=re.S)
        src = re.sub(r"(?m)^\s*//.*$|(?<=[;\s{}])//.*$", " ", src)
        for a, b in re.findall(r"'([^'\n]{2,})'|\"([^\"\n]{2,})\"", src):
            val = (a or b).strip()
            if val:
                filas.append((rel, "string JS", val))

    for rel in ("sitemap.xml", "robots.txt"):
        f = RAIZ / rel
        if f.exists():
            for linea in f.read_text(encoding="utf-8").splitlines():
                if linea.strip():
                    filas.append((rel, "archivo", linea.strip()))
    return filas


def castellano_publicado():
    problemas = []
    for origen, ctx, texto in superficie_publicada():
        # Los placeholders TODO están en castellano A PROPÓSITO (regla de
        # CLAUDE.md: así no pueden confundirse con copy real en inglés), y
        # check-ready ya impide publicar mientras exista uno. Marcarlos acá
        # sería poner una regla del proyecto a pelear contra otra. La exención
        # es angosta a propósito: sólo texto que EMPIEZA con «TODO», que es la
        # convención de los placeholders; castellano sin esa marca sigue siendo
        # hallazgo aunque esté en la misma página.
        if texto.startswith("TODO"):
            continue
        motivos = []
        hits = sorted({h.lower() for h in RE_CASTELLANO.findall(texto)})
        if hits:
            motivos.append("palabras: " + " ".join(hits))
        if RE_DIACRITICOS.search(texto):
            motivos.append("diacríticos")
        if motivos:
            problemas.append(f"{origen} [{ctx}] {texto[:70]!r} -> " + "; ".join(motivos))
    return problemas


def chrome_divergente():
    """El nav, el footer y el bloque de iconos están duplicados en todas las
    páginas: no hay build step que los comparta. La duplicación es aceptable si
    está vigilada, así que en vez de templetizar se verifica que no derive: los
    bloques tienen que ser idénticos carácter por carácter en todas las páginas.

    El bloque de iconos va del primer <link rel="icon"> al <link rel="manifest">
    (2026-08-06): son cuatro etiquetas seguidas y el manifest cierra el grupo —
    si una página agrega, saca o reordena una, el bloque difiere y esto lo ve."""
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
                                   ("footer", '<footer id="footer"', "</footer>"),
                                   ("bloque de iconos",
                                    '<link rel="icon" href="/favicon.ico"',
                                    '<link rel="manifest" href="/site.webmanifest">')):
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
