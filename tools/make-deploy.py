#!/usr/bin/env python3
"""Genera el commit de publicación en `main`: el sitio SOLO, sin las notas.

    python tools/make-deploy.py                     # verifica y arma el commit en main (local)
    python tools/make-deploy.py --solo-verificar    # arma el árbol y corre la guarda, sin commitear
    python tools/make-deploy.py --fuente <ref>      # publica desde otro commit (rollback)
    python tools/make-deploy.py --pisar             # publica aunque main tenga ediciones a mano

POR QUÉ MAIN SE GENERA Y NO SE MERGEA (decisión del autor, ago 2026). GitHub
Pages publica la rama entera, así que un merge de redesign-trust habría servido
CLAUDE.md, tools/ y docs/ desde kotodamafinance.com — las notas de trabajo en
la misma URL que la credencial profesional del autor. main publica SOLO el
sitio; el trabajo vive en la rama de desarrollo.

Y DESDE EL 2026-08-08 EL DEPLOY ADEMÁS QUITA LOS COMENTARIOS de los HTML, CSS
y JS publicados — ver «LA TRANSFORMACIÓN DEL ARTEFACTO», abajo. Esto REVIERTE
la política que decía acá que los comentarios se quedaban en lo servido: el
autor la revisó — el filtro por tipo tapaba las notas como DOCUMENTOS, pero
los comentarios viajaban DENTRO de archivos publicados, y eso era un hueco del
filtro, no una decisión. Los comentarios NO se tocan en el fuente: viven donde
cumplen su función, pegados a la línea que explican; lo único que cambia es
que dejan de viajar a main. Lo que sigue sin taparse es el repo público en
GitHub, donde la rama de desarrollo sigue visible (limitación aceptada: repo
privado + Pages exige plan de pago).

MAIN ES UNA RAMA-ARTEFACTO QUE NADIE EDITA A MANO, igual que `maintenance`: un
artefacto derivado no se mantiene, se regenera. La tentación contra la que esto
defiende es el hotfix directo en main «porque es una línea»: el próximo deploy
lo pisaría en silencio. Por eso el script compara el main actual contra lo que
él mismo generaría desde el hash que ese commit declara (la línea `Fuente:`) y
FRENA si no coinciden — ver verificar_main_intacta().

EL MECANISMO ES PLUMBING, SIN CHECKOUT — el patrón de make-maintenance.py: se
leen los blobs del commit fuente, los .html/.css/.js publicables pasan por la
transformación (función PURA de los bytes: mismo fuente -> mismo artefacto, en
cualquier máquina) y el resto conserva su OID. Desde el 2026-08-08 «lo probado
y lo publicado son el mismo objeto» vale MÓDULO LA TRANSFORMACIÓN DECLARADA:
la guarda 3 la recomputa blob por blob y la 4 verifica el contenido por
derivaciones independientes. Los blobs nuevos se escriben con `hash-object -w
--stdin` SIN `--path`, a propósito: con --path git aplicaría el filtro clean
de autocrlf y el determinismo entre máquinas moriría por el mismo riesgo CRLF
que este mecanismo existe para eliminar. Efecto lateral asumido: también las
corridas de verificación (--solo-verificar, verificar_main_intacta) ESCRIBEN
objetos sueltos en la base — inofensivo, los junta el gc. El árbol de trabajo
y HEAD no se tocan en ningún momento. El push lo hace el autor, aparte — este
script sólo mueve la rama LOCAL.

LA GUARDA ES TODO-O-NADA y corre adentro, antes de commitear (probada EN ROJO
contra sus modos de falla antes de confiar en su verde — el registro está
en CLAUDE.md, decisión de la rama de deploy):

1. COMPLETO — cada URL del sitemap tiene su index.html; cada referencia
   relativa o absoluta-de-sitio de los HTML (href/src + import map), el CSS
   (url()) y los JS (import) resuelve dentro del árbol; y los archivos
   requeridos están — en dos niveles: los CRITICOS (CNAME, .nojekyll, index,
   404) son duros SIEMPRE, el CONTRATO (favicons, manifest, og-image, robots,
   sitemap) es duro desde HEAD y aviso bajo --fuente. La partición está
   explicada junto a las constantes. Desde la transformación corre sobre los
   bytes TRANSFORMADOS: lo que se verifica ES lo que se publica.
2. SIN NOTAS — por TIPO además de por lista: cero .md, .py y .json en lo
   publicado (el sitio no sirve ninguno de esos tipos; el manifest es
   .webmanifest), cero tools/ y docs/. Una nota futura con CUALQUIER nombre
   cae por el tipo, sin depender de que la lista de exclusión esté al día.
   La excepción que el tipo NO caza es maelstrom.css —un .css legítimo—, por
   eso está en la lista explícita Y en una comprobación propia.
3. IDENTIDAD — en DOS clases desde la transformación: los tipos NO
   transformados exigen el MISMO OID que en el commit fuente (la guarda
   original, que existía justamente «para que una refactorización futura que
   transforme archivos no pase en silencio» — disparó a propósito una vez,
   con este cambio); los transformados exigen bytes == transformar(blob
   fuente) RECOMPUTADO, que es además la corrida doble que verifica el
   determinismo (la lección del woff2). OJO: para el camino transformado esa
   comparación es TAUTOLÓGICA frente a un bug del stripper — los dos lados
   salen de la misma función—; de eso se ocupa la guarda 4.
4. TRANSFORMACIÓN — cero comentarios en el artefacto y NADA MÁS cambiado,
   verificado por derivaciones INDEPENDIENTES del stripper: html.parser del
   stdlib (stream de eventos fuente↔artefacto, cero eventos de comentario),
   texto_visible de _guardas, el chrome idéntico ENTRE páginas del artefacto,
   el contrato de supervivencia con nombre (meta de Search Console, import
   map, gc-pixel por página, las noindex, el @license del vendor) y la
   igualdad de tokens en CSS/JS. Es la red real contra un stripper con un
   bug: check-modes contra el artefacto solo navega la portada y /hajime/ —
   las otras páginas las cubre esto.

Y una cuarta, de mantenimiento de la propia lista: si una entrada de
NO_PUBLICABLES no matchea nada en el commit fuente, el script FRENA — una
exclusión que no excluye nada es la lista desactualizada (¿se renombró el
archivo?), y maelstrom.css renombrado se publicaría sin que el tipo lo cace.
"""
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

# La lógica compartida de las guardas de texto: texto_visible, RE_NOINDEX,
# sin_comentarios y los marcadores del chrome. Importarla y no copiarla es la
# regla del mapa: la guarda de transformación compara contra LAS MISMAS
# derivaciones que usan check-structure y check-ready, sin segunda
# implementación.
import _guardas as G

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAMA_DESTINO = "main"

# ---------------------------------------------------------------------------
# LO QUE NO SE PUBLICA. Ésta es la lista autoritativa (CLAUDE.md la resume,
# no la duplica). Los directorios terminan en "/"; el resto es ruta exacta.
# ---------------------------------------------------------------------------
NO_PUBLICABLES = (
    "CLAUDE.md",             # las notas de sesión: el motivo de toda esta separación
    "README.md",             # documenta el repo de trabajo, no el sitio
    ".gitignore",            # protege el árbol de TRABAJO; main no se edita
    "docs/",                 # mediciones fechadas y registro visual
    "tools/",                # guardas, generadores y los JSON de estado
    "assets/img/README.md",  # nota de trabajo (la investigación de logos)
    # maelstrom.css es material de trabajo en FORMATO .css — la regla por tipo
    # no lo caza, por eso está acá Y en una comprobación propia de la guarda:
    # nadie lo carga (check-modes lo verifica en cada corrida) y su encabezado
    # es documentación de calibración con el bug táctil conocido. Si algún día
    # se reactiva, se reactiva en desarrollo y el deploy lo lleva ese día,
    # junto con el <link> que lo cargue.
    "assets/css/maelstrom.css",
    # EL SISTEMA DE NOTAS, EXCLUSIÓN TEMPORAL (2026-08-08, decisión del autor:
    # se publica todo lo que no dependa de contenido; las notas se estrenan
    # con la primera nota real). Son archivos del SITIO, no de trabajo — están
    # acá por estado, no por naturaleza: construidos y esperando su estreno.
    # Nada publicado los referencia (el feed de la portada está en
    # solo-centinelas y /notes/ es huérfana con noindex), así que la
    # comprobación de referencias no los extraña. AL ESTRENAR /notes/: sacar
    # estas TRES entradas y devolver notes/search-index.json a CONTRATO (ver
    # su comentario ahí) — el pase completo, en CLAUDE.md, decisión del
    # sistema de notas.
    "notes/",
    "hajime/nota-ejemplo/",
    "assets/js/notes.js",
)

# LA EXCEPCIÓN INVERSA DE MAELSTROM (2026-08-07, sistema de notas): allá, un
# archivo de trabajo en formato de sitio (.css) que la regla por tipo no caza
# y se excluye por nombre; acá, un ARTEFACTO DEL SITIO en formato de trabajo
# (.json) que la regla por tipo mataría y se admite por nombre.
# notes/search-index.json es el índice del buscador del archivo de notas — el
# navegador lo pide por fetch desde assets/js/notes.js, o sea que es parte de
# lo servido. Va por RUTA EXACTA y nada más: la regla por tipo NO se abre —
# su valor es cazar cualquier nota futura (.md de borrador, .py suelto, otro
# .json) sin que nadie mantenga una lista, y una excepción nombrada no la
# debilita: cualquier otro .json sigue cayendo por el tipo.
# MIENTRAS notes/ esté en NO_PUBLICABLES esta excepción queda DORMIDA (el
# filtro por ruta corre antes y el archivo nunca llega a la regla por tipo);
# se queda puesta para que el estreno no tenga que reconstruirla.
PUBLICABLES_PESE_AL_TIPO = ("notes/search-index.json",)

# Los que tienen que estar en el árbol publicado, en DOS niveles — y la
# partición salió de medir, no de deducir: el freno único bloqueaba el
# rollback a v1-content-complete, que es anterior al juego completo de
# favicons y a assets/img/, y cuyo sitio era consistente igual (su HTML no
# los referenciaba).
#
# CRITICOS rompen Pages o el dominio si faltan (CNAME da de baja el dominio
# propio; sin .nojekyll corre Jekyll; index/404 son lo que Pages sirve) y son
# duros SIEMPRE. CONTRATO es lo que el sitio de HOY promete: duro al publicar
# desde HEAD, aviso bajo --fuente — en un rollback, el sitio de ese día se
# publica como era, y la comprobación de referencias garantiza igual que nada
# de lo que ESE HTML pide quede afuera.
CRITICOS = ("CNAME", ".nojekyll", "index.html", "404.html")
CONTRATO = (
    "robots.txt", "sitemap.xml", "site.webmanifest", "og-image.png",
    "favicon.ico", "favicon.svg", "favicon-16x16.png", "favicon-32x32.png",
    "favicon-192x192.png",  # 言霊 maciza para Google (2026-08-08), con <link> propio
    "apple-touch-icon.png", "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    # notes/search-index.json ENTRARÁ acá al estrenar /notes/: lo pide
    # notes.js por fetch — una referencia que verificar_completo no ve (busca
    # href/src/import, no strings de fetch), así que su presencia habrá que
    # exigirla acá. HOY el sistema de notas entero está excluido del artefacto
    # (ver NO_PUBLICABLES) y un requerido ausente frenaría todo deploy.
)

# La marca que enlaza cada commit de main con su commit fuente. Si cambia el
# formato hay que mantener compatibilidad hacia atrás: verificar_main_intacta
# la busca en el main YA publicado.
MARCA_FUENTE = re.compile(r"^Fuente: ([0-9a-f]{40})", re.M)


def git(*args, entrada=None, env=None):
    e = {**os.environ, **env} if env else None
    r = subprocess.run(("git",) + args, cwd=RAIZ, input=entrada,
                       capture_output=True, env=e)
    if r.returncode:
        sys.exit(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace')}")
    return r.stdout.decode("utf-8", "replace")


def contenido(oid):
    """Los bytes de un blob, directo de la base de objetos."""
    r = subprocess.run(("git", "cat-file", "blob", oid), cwd=RAIZ,
                       capture_output=True)
    if r.returncode:
        sys.exit(f"git cat-file {oid}: {r.stderr.decode('utf-8', 'replace')}")
    return r.stdout


def arbol_de(commit):
    """{ruta: (modo, oid)} de un commit, leído con ls-tree, sin checkout."""
    entradas = {}
    for reg in git("ls-tree", "-r", "-z", commit).split("\0"):
        if not reg:
            continue
        meta, ruta = reg.split("\t", 1)
        modo, _tipo, oid = meta.split(" ")
        entradas[ruta] = (modo, oid)
    return entradas


def excluida(ruta):
    for pat in NO_PUBLICABLES:
        if pat.endswith("/"):
            if ruta.startswith(pat):
                return True
        elif ruta == pat:
            return True
    return False


def filtrar(arbol):
    return {r: mo for r, mo in arbol.items() if not excluida(r)}


def exclusiones_sin_efecto(arbol):
    """Entradas de NO_PUBLICABLES que no matchean nada: lista desactualizada."""
    sin = []
    for pat in NO_PUBLICABLES:
        if pat.endswith("/"):
            if not any(r.startswith(pat) for r in arbol):
                sin.append(pat)
        elif pat not in arbol:
            sin.append(pat)
    return sin


# ---------------------------------------------------------------------------
# LA GUARDA. Funciones puras sobre el diccionario del árbol, a propósito: así
# la prueba en rojo puede mutarles la entrada sin tocar ningún ref de git.
# ---------------------------------------------------------------------------

RE_COMENT_HTML = re.compile(r"<!--.*?-->", re.S)
# Comillas dobles Y simples — la primera versión sólo veía dobles, y un
# src='...' (HTML válido) pasaba sin verificar: verde falso, la dirección
# peligrosa. Lo mismo srcset y el url() de un <style> inline, abajo.
RE_ATTR = re.compile(r"""(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""")
RE_SRCSET = re.compile(r"""srcset\s*=\s*(?:"([^"]*)"|'([^']*)')""")
RE_STYLE_INLINE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
RE_IMPORTMAP = re.compile(r'<script type="importmap">\s*(\{.*?\})\s*</script>', re.S)
RE_COMENT_BLOQUE = re.compile(r"/\*.*?\*/", re.S)
RE_LINEA_COMENT_JS = re.compile(r"^\s*//.*$", re.M)
RE_URL_CSS = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")
RE_IMPORT_JS = re.compile(r"""\b(?:from|import)\s*\(?\s*['"]([^'"]+)['"]""")


# ---------------------------------------------------------------------------
# LA TRANSFORMACIÓN DEL ARTEFACTO: cero comentarios en lo servido
# (2026-08-08, requisito del autor — condición sine qua non, no preferencia).
# Los comentarios del fuente son notas de trabajo en castellano y el filtro
# por TIPO no los veía: viven DENTRO de archivos que sí se publican. Se
# eliminan ACÁ, al generar el artefacto; el fuente NO se toca nunca.
#
# Función PURA de (ruta, bytes) -> bytes: sin timestamps, sin aleatoriedad,
# sin estado — el determinismo es lo que mantiene vivos el detector de hotfix
# y la idempotencia («ya está en este contenido»), y verificar_identidad lo
# comprueba recomputando.
#
# QUÉ NO SE TRANSFORMA, y por qué:
#   - assets/vendor/ (three.module.js): su primer comentario es el @license
#     MIT, que exige conservarse; los otros ~2350 son comentarios de la
#     biblioteca en inglés, no notas de trabajo. Queda en la clase
#     OID-idéntico de verificar_identidad. Decisión del autor (2026-08-08).
#   - El contenido de <script>/<style> en los HTML: texto crudo, se copia tal
#     cual (el único script inline del sitio es el import map, JSON sin
#     comentarios; <style> inline hoy no hay — verificado).
#   - Los template literals de los JS: opacos para el stripper — su contenido
#     es un STRING del programa (el caso real es el GLSL de background.js:
#     quitar sus comentarios sería editar el shader, que es código cerrado;
#     el autor los reescribió en inglés en el fuente, 2026-08-08).
#
# LOS RELLENOS NO SON IGUALES ENTRE LENGUAJES, y es semántica, no gusto:
# en HTML el comentario no aporta NI un espacio (foo<!-- -->bar renderiza
# «foobar»), así que se quita a nada; en CSS y JS un /* */ es SEPARADOR de
# tokens (a/* */b son DOS tokens), así que se reemplaza por UN espacio. El //
# muere en su \n, que se conserva — la inserción automática de ; (ASI) no se
# altera. Una línea que queda solo-espacios se elimina ENTERA; una que
# conserva contenido se recorta al final (rstrip).

VENDOR = "assets/vendor/"
_MARCA = "\x00"  # marcador interno del stripper; transformar() aborta si el
                 # archivo lo trae de fábrica (hoy: ninguno, verificado)

RE_RAW_HTML = re.compile(r"<(script|style)\b[^>]*>.*?</\1\s*>", re.S | re.I)


def transformable(ruta):
    return ruta.endswith((".html", ".css", ".js")) and not ruta.startswith(VENDOR)


# SOLO whitespace ASCII, en las tres operaciones de línea y en la
# normalización de la guarda. Python trata U+00A0 (nbsp) y U+3000 (el espacio
# ideográfico de la marca de agua 産霊　河川　言霊) como whitespace en
# strip/split, pero HTML los RENDERIZA siempre: un rstrip() pelado se los
# comería en silencio (hallazgo de la revisión adversarial, 2026-08-08).
_WS_ASCII = " \t\r\f"
RE_ESPACIOS_ASCII = re.compile(r"[ \t\n\r\f]+")


def _normalizar_espacios(texto):
    return RE_ESPACIOS_ASCII.sub(" ", texto).strip(" ")


def _limpiar_lineas(texto, relleno):
    lineas = []
    for linea in texto.split("\n"):
        if _MARCA in linea:
            limpia = linea.replace(_MARCA, relleno)
            if limpia.strip(_WS_ASCII):
                lineas.append(limpia.rstrip(_WS_ASCII))
            # solo-comentario(s): la línea entera se va, con su \n
        else:
            lineas.append(linea)
    return "\n".join(lineas)


RE_PRE_HTML = re.compile(r"<(pre|textarea)\b[^>]*>.*?</\1\s*>", re.S | re.I)


def quitar_comentarios_html(texto):
    """<!-- --> fuera de <script>/<style>; adentro de <pre>/<textarea> el
    comentario sale A NADA y SIN cirugía de líneas (ahí el whitespace es
    renderizado). UNA pasada posicional: el constructo que ARRANCA primero
    gana — un <script> dentro de un comentario es texto del comentario (un
    bloque comentado entero SE VA, como lo ve el parser HTML real), y un
    <!-- dentro de un bloque raw es texto del raw. La versión anterior
    protegía los raw ANTES de mirar comentarios y un <script> comentado
    partía el <!-- de su --> — el comentario sobrevivía y bloqueaba todo
    deploy (hallazgo de la revisión adversarial, reproducido)."""
    out, pos, n = [], 0, len(texto)
    while pos < n:
        c = texto.find("<!--", pos)
        m_raw = RE_RAW_HTML.search(texto, pos)
        m_pre = RE_PRE_HTML.search(texto, pos)
        candidatos = [x for x in ((c, "com", None),
                                  (m_raw.start() if m_raw else -1, "raw", m_raw),
                                  (m_pre.start() if m_pre else -1, "pre", m_pre))
                      if x[0] >= 0]
        if not candidatos:
            out.append(texto[pos:])
            break
        ini, tipo, m = min(candidatos)
        out.append(texto[pos:ini])
        if tipo == "com":
            fin = texto.find("-->", ini + 4)
            if fin < 0:
                sys.exit("transformación: un <!-- sin su --> — comentario sin "
                         "cerrar; nada se escribió")
            out.append(_MARCA)
            pos = fin + 3
        elif tipo == "raw":
            out.append(m.group(0))
            pos = m.end()
        else:
            out.append(RE_COMENT_HTML.sub("", m.group(0)))
            pos = m.end()
    return _limpiar_lineas("".join(out), "")


def _escanear_css(texto):
    """[(tipo, ini, fin)] cubriendo TODO el texto: 'code' | 'atomo' (string)
    | 'coment'. Los strings se saltan para que un /* adentro no arranque un
    comentario falso."""
    segs, i, n, a = [], 0, len(texto), 0
    while i < n:
        c = texto[i]
        if c in "'\"":
            if a < i:
                segs.append(("code", a, i))
            q, j = c, i + 1
            while j < n and texto[j] != q:
                j += 2 if texto[j] == "\\" else 1
            j = min(j + 1, n)
            segs.append(("atomo", i, j))
            a = i = j
        elif c == "/" and i + 1 < n and texto[i + 1] == "*":
            if a < i:
                segs.append(("code", a, i))
            j = texto.find("*/", i + 2)
            j = n if j < 0 else j + 2
            segs.append(("coment", i, j))
            a = i = j
        else:
            i += 1
    if a < n:
        segs.append(("code", a, n))
    return segs


# Palabras tras las que un / abre un REGEX y no una división. Es la
# heurística estándar de lexers de JS; los casos trampa reales del repo
# están en las pruebas en rojo (main.js /(^|-)2g$/ tras ||, notes.js con
# comilla doble dentro de la clase, */ dentro de un regex).
_PALABRAS_REGEX = frozenset((
    "return", "typeof", "case", "in", "of", "new", "delete", "void",
    "instanceof", "do", "else", "yield", "await"))


def _escanear_js(texto):
    """[(tipo, ini, fin)] SIN cubrir los huecos de código: 'atomo' (string,
    template literal con sus tramos crudos, regex) | 'coment'. Un template
    con ${} alterna tramos crudos (atomo) y código adentro — los comentarios
    dentro de un ${} sí se detectan; el texto crudo del template, jamás."""
    spans, i, n = [], 0, len(texto)
    prev, prev_word = "", ""
    pila = []

    def tramo_crudo(j):
        """Texto crudo de template desde j; devuelve (fin, abrió_expr)."""
        while j < n:
            ch = texto[j]
            if ch == "\\":
                j += 2
            elif ch == "`":
                return j + 1, False
            elif ch == "$" and j + 1 < n and texto[j + 1] == "{":
                return j + 2, True
            else:
                j += 1
        return n, False

    while i < n:
        c = texto[i]
        if c == "`":
            j, expr = tramo_crudo(i + 1)
            spans.append(("atomo", i, j))
            if expr:
                pila.append("tpl")
            prev, prev_word, i = "`", "", j
        elif c == "}" and pila and pila[-1] == "tpl":
            pila.pop()
            j, expr = tramo_crudo(i + 1)
            spans.append(("atomo", i, j))
            if expr:
                pila.append("tpl")
            prev, prev_word, i = "`", "", j
        elif c == "{":
            pila.append("{")
            prev, prev_word, i = c, "", i + 1
        elif c == "}":
            if pila:
                pila.pop()
            prev, prev_word, i = c, "", i + 1
        elif c in "'\"":
            q, j = c, i + 1
            while j < n and texto[j] != q:
                j += 2 if texto[j] == "\\" else 1
            j = min(j + 1, n)
            spans.append(("atomo", i, j))
            prev, prev_word, i = q, "", j
        elif c == "/" and i + 1 < n and texto[i + 1] == "/":
            j = texto.find("\n", i)
            j = n if j < 0 else j
            spans.append(("coment", i, j))
            i = j
        elif c == "/" and i + 1 < n and texto[i + 1] == "*":
            j = texto.find("*/", i + 2)
            j = n if j < 0 else j + 2
            spans.append(("coment", i, j))
            i = j
        elif c == "/" and (prev == "" or prev in "=([{,;:!&|?+-*%~^<>"
                           or prev_word in _PALABRAS_REGEX):
            j, en_clase = i + 1, False
            while j < n:
                ch = texto[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == "[":
                    en_clase = True
                elif ch == "]":
                    en_clase = False
                elif ch == "/" and not en_clase:
                    j += 1
                    break
                elif ch == "\n":
                    break  # no cerró: no era un regex — se trata como código
                j += 1
            spans.append(("atomo", i, j))
            prev, prev_word, i = "/", "", j
        else:
            if not c.isspace():
                m = re.match(r"[A-Za-z0-9_$]+", texto[i:])
                if m:
                    prev_word = m.group(0)
                    prev = prev_word[-1]
                    i += len(prev_word)
                    continue
                prev, prev_word = c, ""
            i += 1
    return spans


def _quitar_spans(texto, spans):
    out, pos = [], 0
    for tipo, a, b in spans:
        out.append(texto[pos:a])
        out.append(_MARCA if tipo == "coment" else texto[a:b])
        pos = b
    out.append(texto[pos:])
    return "".join(out)


def quitar_comentarios_css(texto):
    return _limpiar_lineas(_quitar_spans(texto, _escanear_css(texto)), " ")


def quitar_comentarios_js(texto):
    return _limpiar_lineas(_quitar_spans(texto, _escanear_js(texto)), " ")


def transformar(ruta, data):
    """bytes -> bytes. La única puerta: pura, determinista, todo-o-nada."""
    try:
        texto = data.decode("utf-8")
    except UnicodeDecodeError as e:
        sys.exit(f"transformación: {ruta} no decodifica como UTF-8 ({e}) — "
                 f"nada se escribió")
    if _MARCA in texto:
        sys.exit(f"transformación: {ruta} contiene el byte NUL que el "
                 f"stripper usa como marcador interno — nada se escribió")
    if ruta.endswith(".html"):
        nuevo = quitar_comentarios_html(texto)
    elif ruta.endswith(".css"):
        nuevo = quitar_comentarios_css(texto)
    else:
        nuevo = quitar_comentarios_js(texto)
    return nuevo.encode("utf-8")


def _tokens(texto, escanear):
    """Los tokens SIGNIFICATIVOS: átomos (strings/templates/regex) verbatim,
    el código partido por espacios, los comentarios afuera. La igualdad de
    esta secuencia entre original y transformado es lo que caza a un stripper
    que muerda un átomo o pegue dos tokens (a/* */b -> «ab»)."""
    toks, pos = [], 0
    for tipo, a, b in escanear(texto):
        if pos < a:
            toks += texto[pos:a].split()
        if tipo == "atomo":
            toks.append(texto[a:b])
        elif tipo == "code":
            toks += texto[a:b].split()
        pos = b
    toks += texto[pos:].split()
    return toks


class _EventosHTML(HTMLParser):
    """Stream de eventos para comparar fuente y artefacto SIN depender del
    stripper: html.parser es un tokenizer INDEPENDIENTE del stdlib. El texto
    se acumula y se normaliza por espacios — un comentario parte el texto en
    dos eventos; quitarlo los une, y la acumulación hace que las dos formas
    comparen iguales. Los comentarios van a su propia lista: en el artefacto
    esa lista tiene que estar VACÍA."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.eventos, self.comentarios, self._data = [], [], []

    def _flush(self):
        if self._data:
            # ASCII solo: normalizar con split() pelado colapsaría también
            # NBSP y U+3000, que HTML renderiza — la guarda quedaría ciega a
            # un stripper que se los coma.
            t = _normalizar_espacios("".join(self._data))
            if t:
                self.eventos.append(("data", t))
            self._data = []

    def handle_starttag(self, tag, attrs):
        self._flush()
        self.eventos.append(("in", tag, tuple(attrs)))

    def handle_startendtag(self, tag, attrs):
        self._flush()
        self.eventos.append(("inout", tag, tuple(attrs)))

    def handle_endtag(self, tag):
        self._flush()
        self.eventos.append(("out", tag))

    def handle_data(self, data):
        self._data.append(data)

    def handle_comment(self, data):
        self.comentarios.append(data)  # sin flush: el texto de alrededor se une

    def handle_decl(self, decl):
        self._flush()
        self.eventos.append(("decl", decl))

    def handle_pi(self, data):
        self._flush()
        self.eventos.append(("pi", data))

    def close(self):
        self._flush()
        super().close()


def _eventos_html(texto):
    p = _EventosHTML()
    p.feed(texto)
    p.close()
    return p


def _resolver(base_dir, ref):
    """Normaliza una referencia a ruta dentro del árbol; None si es externa
    o un fragmento de la misma página."""
    ref = ref.strip()
    if not ref or ref.startswith(("http://", "https://", "mailto:", "data:", "#")):
        return None
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    if not ref:
        return None  # era "/#ancla" ya sin la parte de ruta: no pasa, pero por si acaso
    con_barra = ref.endswith("/")
    if ref.startswith("/"):
        ruta = ref[1:]
    else:
        ruta = posixpath.normpath(posixpath.join(base_dir, ref))
    if ruta in ("", "."):
        return "index.html"
    if con_barra:
        return ruta.rstrip("/") + "/index.html"
    return ruta


def verificar_completo(arbol, leer, requeridos=CRITICOS + CONTRATO):
    """Nada referenciado quedó afuera. `leer` es callable(ruta) -> bytes."""
    problemas = []
    rutas = set(arbol)

    for r in requeridos:
        if r not in rutas:
            problemas.append(f"falta {r} (requerido por Pages o por los metadatos)")

    if "sitemap.xml" in rutas:
        sm = leer("sitemap.xml").decode("utf-8")
        for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
            ruta = loc.split("kotodamafinance.com", 1)[-1].lstrip("/")
            destino = (ruta.rstrip("/") + "/index.html") if ruta else "index.html"
            if destino not in rutas:
                problemas.append(f"el sitemap declara {loc} y {destino} no está en el árbol")

    for ruta in sorted(rutas):
        base = posixpath.dirname(ruta)
        refs = []
        if ruta.endswith(".html"):
            texto = RE_COMENT_HTML.sub("", leer(ruta).decode("utf-8"))
            refs = [a or b for a, b in RE_ATTR.findall(texto)]
            for a, b in RE_SRCSET.findall(texto):
                # srcset = lista de "url [descriptor]" separadas por coma
                refs += [t.split()[0] for t in (a or b).split(",") if t.strip()]
            for bloque in RE_STYLE_INLINE.findall(texto):
                refs += RE_URL_CSS.findall(RE_COMENT_BLOQUE.sub("", bloque))
            m = RE_IMPORTMAP.search(texto)
            if m:
                refs += list(json.loads(m.group(1)).get("imports", {}).values())
        elif ruta.endswith(".css"):
            texto = RE_COMENT_BLOQUE.sub("", leer(ruta).decode("utf-8"))
            refs = RE_URL_CSS.findall(texto)
        elif ruta.endswith(".js"):
            texto = RE_COMENT_BLOQUE.sub("", leer(ruta).decode("utf-8"))
            texto = RE_LINEA_COMENT_JS.sub("", texto)
            # Sólo especificadores relativos o absolutos: los desnudos («three»)
            # los resuelve el import map, que se verifica por el lado del HTML.
            refs = [r for r in RE_IMPORT_JS.findall(texto) if r.startswith((".", "/"))]
        for ref in refs:
            destino = _resolver(base, ref)
            if destino and destino not in rutas:
                problemas.append(f"{ruta}: referencia «{ref}» -> {destino}, que no está en el árbol")
    return problemas


def verificar_sin_notas(arbol):
    """Nada de trabajo entró: por tipo (lo robusto) y maelstrom por nombre."""
    problemas = []
    for ruta in sorted(arbol):
        if ruta.endswith((".md", ".py", ".json")) and ruta not in PUBLICABLES_PESE_AL_TIPO:
            problemas.append(f"{ruta}: tipo de archivo de trabajo (.md/.py/.json) en el árbol publicado")
        if ruta.startswith(("tools/", "docs/")) or ruta == ".gitignore":
            problemas.append(f"{ruta}: ruta de trabajo en el árbol publicado")
        if ruta == "assets/css/maelstrom.css":
            problemas.append("assets/css/maelstrom.css: material de trabajo en formato .css "
                             "(la regla por tipo no lo caza; ver NO_PUBLICABLES)")
    return problemas


def verificar_identidad(arbol_pub, arbol_fuente):
    """Cada blob publicado es el del fuente — o su transformación EXACTA.

    Dos clases desde el 2026-08-08: los tipos NO transformados exigen el
    MISMO OID (la guarda original — sigue cazando un blob ajeno colado); los
    transformados exigen bytes == transformar(blob fuente), RECOMPUTADO acá,
    que es a la vez la corrida doble que verifica el determinismo (la lección
    del woff2: correr el generador dos veces antes de confiar en comparar
    salidas). Para el camino transformado esta comparación es TAUTOLÓGICA
    frente a un bug del stripper — ambos lados salen de la misma función—;
    la que mira el CONTENIDO es verificar_transformacion."""
    problemas = []
    for ruta, (modo, oid) in sorted(arbol_pub.items()):
        if ruta not in arbol_fuente:
            problemas.append(f"{ruta}: está en el árbol publicado y no en el commit fuente")
            continue
        modo_f, oid_f = arbol_fuente[ruta]
        if transformable(ruta):
            if modo != modo_f:
                problemas.append(f"{ruta}: cambió el modo ({modo_f} -> {modo})")
            elif contenido(oid) != transformar(ruta, contenido(oid_f)):
                problemas.append(f"{ruta}: el blob publicado NO es la transformación "
                                 f"del blob fuente (¿no-determinismo, o un blob ajeno?)")
        elif (modo_f, oid_f) != (modo, oid):
            problemas.append(f"{ruta}: blob distinto del commit fuente "
                             f"({oid[:12]} != {oid_f[:12]}) y no es un tipo transformable")
    return problemas


def verificar_transformacion(arbol_pub, leer_fuente, leer_pub, desde_head=True):
    """La guarda 4: cero comentarios y NADA MÁS cambiado, por derivaciones
    INDEPENDIENTES del stripper. Es la red real contra un bug del stripper —
    la identidad recomputa la misma función (tautológica) y check-modes solo
    navega la portada y /hajime/: el resto del artefacto lo cubre esto.

    `desde_head=False` es el rollback (--fuente): las comprobaciones
    COMPARATIVAS rigen igual (nada que el fuente tenga puede perderse), pero
    las de PRESENCIA (la meta de Search Console, los bloques de chrome que
    ese árbol no tenía) siguen la partición del CONTRATO — «el sitio de ese
    día se publica como era». Sin esto, el rollback documentado a
    v1-published/v1-content-complete frenaba en seco (hallazgo ALTO de la
    revisión adversarial, reproducido ejecutando)."""
    problemas = []
    htmls = [r for r in sorted(arbol_pub) if r.endswith(".html")]

    for ruta in htmls:
        fuente = leer_fuente(ruta).decode("utf-8")
        pub = leer_pub(ruta).decode("utf-8")

        ef, ep = _eventos_html(fuente), _eventos_html(pub)
        # 1. Cero comentarios, contados por html.parser (no por el regex del
        #    stripper): un comentario que el stripper no vio, esto lo ve.
        if ep.comentarios:
            problemas.append(f"{ruta}: quedaron {len(ep.comentarios)} comentario(s) "
                             f"en el artefacto ({' '.join(ep.comentarios[0].split())[:60]!r}…)")
        # 2. Nada más cambió: mismos eventos (tags y atributos EXACTOS, texto
        #    normalizado por espacios ASCII). Caza el sobre-borrado en
        #    CUALQUIER página — metas, atributos, prosa.
        if ef.eventos != ep.eventos:
            detalle = f"{len(ef.eventos)} vs {len(ep.eventos)} eventos"
            for a, b in zip(ef.eventos, ep.eventos):
                if a != b:
                    detalle = f"fuente {a!r} vs artefacto {b!r}"
                    break
            problemas.append(f"{ruta}: la transformación cambió algo más que "
                             f"comentarios ({detalle})")
        # 3. El texto visible (_guardas.texto_visible). El fuente entra con
        #    los comentarios ya quitados A NADA: texto_visible los sustituye
        #    por UN espacio y con foo<!-- -->bar daba un rojo FALSO («el
        #    texto cambió») sobre un artefacto correcto — hallazgo de la
        #    revisión. El valor independiente de esta vara no es el regex de
        #    comentarios (trivial): es que NO pasa por la cirugía de líneas
        #    del stripper — la aísla.
        tf = _normalizar_espacios(G.texto_visible(RE_COMENT_HTML.sub("", fuente)))
        tp = _normalizar_espacios(G.texto_visible(pub))
        if tf != tp:
            problemas.append(f"{ruta}: el texto visible cambió con la transformación")
        # 3b. <pre>/<textarea>: ahí el whitespace SE RENDERIZA y las
        #     normalizaciones de 2 y 3 no lo ven — la comparación es BYTE a
        #     byte: bloque del artefacto == bloque del fuente sin comentarios,
        #     sin cirugía de líneas (hallazgo de la revisión: un <pre> con
        #     comentario perdía saltos e indentación con todo en verde).
        #     Límite documentado: white-space:pre aplicado por CSS a otro
        #     elemento no se puede ver estáticamente (hoy styles.css solo
        #     tiene nowrap).
        esperados = [RE_COMENT_HTML.sub("", m.group(0))
                     for m in RE_PRE_HTML.finditer(fuente)]
        reales = [m.group(0) for m in RE_PRE_HTML.finditer(pub)]
        if esperados != reales:
            problemas.append(f"{ruta}: un <pre>/<textarea> cambió byte a byte "
                             f"con la transformación (whitespace renderizado)")
        # 3c. Precondición del borde raw: un <script>/<style> inline cuyo
        #     contenido traiga «<!--» o «</script» entra en el estado
        #     double-escaped del spec, donde el primer </script> NO cierra —
        #     y ahí el stripper Y html.parser comparten la MISMA regla
        #     ingenua: la corrupción sería invisible para toda la guarda
        #     (hallazgo de la revisión, reproducido con fixture). Se prohíbe
        #     en el FUENTE, en rojo con nombre — hoy el único inline es el
        #     import map (JSON) y no lo trae.
        for m in RE_RAW_HTML.finditer(fuente):
            cuerpo = m.group(0)[m.group(0).index(">") + 1:].rsplit("</", 1)[0]
            if "<!--" in cuerpo or f"</{m.group(1).lower()}" in cuerpo.lower():
                problemas.append(f"{ruta}: un <{m.group(1)}> inline contiene "
                                 f"«<!--» o «</{m.group(1).lower()}» — el borde raw "
                                 f"se vuelve ambiguo (double-escaped) y el stripper "
                                 f"no puede garantizarlo; sacarlo del fuente")
        # 7. Idempotencia: transformar lo transformado no mueve un byte.
        if transformar(ruta, leer_pub(ruta)) != leer_pub(ruta):
            problemas.append(f"{ruta}: la transformación no es idempotente")

    # 4. El chrome idéntico ENTRE páginas DEL ARTEFACTO: la garantía de
    #    chrome_divergente, re-establecida donde se sirve (mismos marcadores,
    #    importados — no una segunda lista). QUÉ bloques exigir se deriva del
    #    FUENTE: v1-content-complete no tenía bloque de iconos y exigírselo
    #    hacía impublicable el punto de restauración del DNS (hallazgo ALTO
    #    de la revisión); un stripper que muerda un bloque existente sigue
    #    cayendo — el fuente lo tiene y el artefacto no.
    ref = {}
    for ruta in htmls:
        fuente = leer_fuente(ruta).decode("utf-8")
        pub = leer_pub(ruta).decode("utf-8")
        for etiqueta, ini, fin in G.BLOQUES_CHROME:
            if G.bloque_chrome(fuente, ini, fin) is None:
                continue  # ese árbol no lo tenía: no hay nada que preservar
            b = G.bloque_chrome(pub, ini, fin)
            if b is None:
                problemas.append(f"{ruta}: el artefacto quedó sin {etiqueta} "
                                 f"(el fuente lo tiene)")
            elif etiqueta not in ref:
                ref[etiqueta] = (ruta, b)
            elif b != ref[etiqueta][1]:
                problemas.append(f"{ruta}: el {etiqueta} del artefacto difiere "
                                 f"del de {ref[etiqueta][0]}")

    # 5. El contrato de supervivencia, con nombre: piezas que el punto 2 ya
    #    cubre pero cuyo rojo tiene que nombrar la pieza — el diagnóstico
    #    «cambió un evento» no le dice al operador que perdió Search Console.
    if "index.html" in arbol_pub:
        fuente = leer_fuente("index.html").decode("utf-8")
        pub = leer_pub("index.html").decode("utf-8")
        m = re.search(r'<meta name="google-site-verification" content="[^"]*"\s*/?>',
                      fuente)
        if not m:
            # PRESENCIA solo desde HEAD: bajo --fuente rige la partición del
            # CONTRATO («el sitio de ese día se publica como era») — los
            # fuentes anteriores al deploy 6 no tienen la meta, y exigirla
            # incondicional mataba el rollback documentado (hallazgo ALTO de
            # la revisión: --fuente v1-published frenaba y --pisar no exime
            # de la guarda).
            if desde_head:
                problemas.append("index.html (fuente): sin la meta google-site-verification "
                                 "— si falta en la portada se pierde la verificación de "
                                 "Search Console (regla de CLAUDE.md)")
        elif m.group(0) not in pub:
            problemas.append("index.html: la meta google-site-verification NO "
                             "sobrevivió a la transformación — publicarla así pierde "
                             "la verificación de Search Console")
        if ('<script type="importmap">' in fuente
                and '<script type="importmap">' not in pub):
            problemas.append("index.html: el import map no sobrevivió — el cubo "
                             "muere en silencio para todo visitante")
    for ruta in htmls:
        fuente = leer_fuente(ruta).decode("utf-8")
        pub = leer_pub(ruta).decode("utf-8")
        if fuente.count('class="gc-pixel"') != pub.count('class="gc-pixel"'):
            problemas.append(f"{ruta}: el pixel de GoatCounter no sobrevivió a la "
                             f"transformación")
        # El noindex del fuente se lee SIN comentarios (citarlo en un
        # comentario no es declararlo — el criterio de _guardas); en el
        # artefacto ya no hay comentarios que filtrar.
        tiene_f = bool(G.RE_NOINDEX.search(G.sin_comentarios(fuente)))
        tiene_p = bool(G.RE_NOINDEX.search(pub))
        if tiene_f != tiene_p:
            problemas.append(f"{ruta}: la meta noindex "
                             f"{'DESAPARECIÓ' if tiene_f else 'APARECIÓ'} con la "
                             f"transformación")
    v = VENDOR + "three.module.js"
    if v in arbol_pub and b"@license" not in leer_pub(v)[:400]:
        problemas.append(f"{v}: perdió su @license — el vendor NO se transforma "
                         f"(licencia MIT, exige conservarse)")

    # 6. CSS/JS: la secuencia de tokens significativos no cambió. Los átomos
    #    (strings, templates, regex) comparan VERBATIM; el código, por
    #    palabras. Caza un átomo mordido y dos tokens pegados.
    #    MÁS el conteo que a esta pareja le faltaba (hallazgo de la
    #    revisión): «/*» PROHIBIDO en el artefacto CSS/JS de la casa —
    #    tokens e idempotencia usan EL MISMO scanner del stripper, así que
    #    un comentario que el scanner clasifique mal (p.ej. tras una
    #    comilla despareada en código) sobreviviría con todo en verde. El
    #    ban es independiente de la clasificación. Si algún día un string
    #    legítimo necesita «/*», este check se revisa a conciencia — rojo
    #    visible, no publicación silenciosa. LÍMITE DOCUMENTADO: para el
    #    «//» de línea no hay ban posible (el GLSL del template de
    #    background.js lo usa legítimamente) — un comentario // atrapado en
    #    un pseudo-string quedaría; el caso exige una comilla despareada en
    #    CÓDIGO, que en JS es SyntaxError (check-modes lo ve para
    #    main/cube; background muere en consola).
    for ruta in sorted(arbol_pub):
        if not transformable(ruta) or ruta.endswith(".html"):
            continue
        fuente = leer_fuente(ruta).decode("utf-8")
        pub = leer_pub(ruta).decode("utf-8")
        if "/*" in pub:
            problemas.append(f"{ruta}: quedó un «/*» en el artefacto — comentario "
                             f"sobreviviente, o un string nuevo que obliga a "
                             f"revisar este check")
        escanear = _escanear_css if ruta.endswith(".css") else _escanear_js
        tf, tp = _tokens(fuente, escanear), _tokens(pub, escanear)
        if tf != tp:
            detalle = f"{len(tf)} vs {len(tp)} tokens"
            for a, b in zip(tf, tp):
                if a != b:
                    detalle = f"{a[:40]!r} vs {b[:40]!r}"
                    break
            problemas.append(f"{ruta}: los tokens divergen tras la transformación "
                             f"({detalle})")
        if transformar(ruta, leer_pub(ruta)) != leer_pub(ruta):
            problemas.append(f"{ruta}: la transformación no es idempotente")
    return problemas


# ---------------------------------------------------------------------------
# Escritura y protección de main
# ---------------------------------------------------------------------------

def escribir_blob(data):
    """Escribe bytes como blob y devuelve su OID. SIN --path a propósito: con
    --path, hash-object aplica el filtro clean de autocrlf y el determinismo
    entre máquinas muere por el mismo riesgo CRLF que el plumbing elimina."""
    r = subprocess.run(("git", "hash-object", "-w", "--stdin"), cwd=RAIZ,
                       input=data, capture_output=True)
    if r.returncode:
        sys.exit(f"git hash-object: {r.stderr.decode('utf-8', 'replace')}")
    return r.stdout.decode().strip()


def arbol_publicable(commit, _memo={}):
    """El árbol de deploy de un commit: filtrado + TRANSFORMADO.

    La única puerta de generación — main() y verificar_main_intacta pasan por
    acá, sin segunda implementación: si divergieran, el detector de hotfix
    creería que main se editó a mano. El memo por (oid, extensión) evita
    re-transformar el mismo blob entre la regeneración del detector y el
    deploy (vive lo que el proceso, a propósito)."""
    pub = {}
    for ruta, (modo, oid) in filtrar(arbol_de(commit)).items():
        if transformable(ruta):
            clave = (oid, ruta.rsplit(".", 1)[1])
            if clave not in _memo:
                _memo[clave] = escribir_blob(transformar(ruta, contenido(oid)))
            pub[ruta] = (modo, _memo[clave])
        else:
            pub[ruta] = (modo, oid)
    return pub


def escribir_arbol(arbol):
    """Escribe el árbol en la base de objetos con un índice TEMPORAL: ni el
    índice real ni el árbol de trabajo se tocan (el patrón make-maintenance,
    con update-index en vez de mktree porque acá hay subdirectorios)."""
    fd, ruta_idx = tempfile.mkstemp(prefix="kotodama-deploy-index-")
    os.close(fd)
    os.remove(ruta_idx)
    try:
        info = "".join(f"{modo} {oid} 0\t{ruta}\n"
                       for ruta, (modo, oid) in sorted(arbol.items()))
        env = {"GIT_INDEX_FILE": ruta_idx}
        git("update-index", "--index-info", entrada=info.encode("utf-8"), env=env)
        return git("write-tree", env=env).strip()
    finally:
        if os.path.exists(ruta_idx):
            os.remove(ruta_idx)


def verificar_main_intacta(ref=None):
    """Devuelve (ok, cabeza, mensaje). ok=False significa: main tiene algo que
    este script no generó (o no puede verificarlo), y publicarle encima PISA.

    Cuatro estados posibles de la punta de main:
    - Con marca `Fuente:` y árbol == regenerado desde esa fuente -> intacta.
    - Con marca pero árbol distinto, O sin marca pero con un deploy en su
      historia -> alguien tocó main a mano (o cambiaron las reglas de
      exclusión desde ese deploy, que también merece mirarse antes de pisar).
    - Con marca pero la Fuente declarada YA NO está en la base de objetos
      (historia reescrita, clon parcial) -> no verificable: frena con el hint
      de --pisar en vez de morir con el fatal crudo de git, que --pisar no
      podía saltear.
    - Sin marca y sin ningún deploy en la historia -> es el primer deploy
      sobre la landing vieja: se publica encima, que es el reemplazo buscado.
    """
    if ref is None:
        # Resuelto en runtime, no en el default de la firma: así una prueba
        # que parchee RAMA_DESTINO redirige TAMBIÉN esta lectura.
        ref = f"refs/heads/{RAMA_DESTINO}"
    r = subprocess.run(("git", "rev-parse", "--verify", "-q", ref),
                       cwd=RAIZ, capture_output=True)
    if r.returncode:
        sys.exit(f"no existe {ref} — este script publica sobre la rama, no la crea")
    cabeza = r.stdout.decode().strip()
    mensaje = git("log", "-1", "--format=%B", cabeza)
    m = MARCA_FUENTE.search(mensaje)
    if m:
        existe = subprocess.run(("git", "rev-parse", "--verify", "-q",
                                 m.group(1) + "^{commit}"),
                                cwd=RAIZ, capture_output=True)
        if existe.returncode:
            return (False, cabeza,
                    f"la punta de {RAMA_DESTINO} ({cabeza[:12]}) declara Fuente {m.group(1)[:12]} "
                    f"pero ese commit YA NO está en la base de objetos\n"
                    f"  (¿historia reescrita? ¿clon parcial?): no se puede verificar que "
                    f"{RAMA_DESTINO} esté intacta.\n"
                    f"  Para publicar igual, asumiendo el riesgo: --pisar")
        regenerado = escribir_arbol(arbol_publicable(m.group(1)))
        actual = git("rev-parse", f"{cabeza}^{{tree}}").strip()
        if regenerado != actual:
            # LA DOBLE REGENERACIÓN DIAGNÓSTICA (2026-08-08, decisión del
            # autor: nada de --pisar a ciegas ante un mismatch esperado). Un
            # deploy generado ANTES del stripper copiaba los blobs tal cual;
            # si la regla VIEJA (filtrado solo) reproduce la punta, main está
            # INTACTA — nadie la editó a mano, solo cambió el generador — y
            # se publica encima sin pisar nada. Un hotfix a mano no coincide
            # con NINGUNA de las dos regeneraciones y sigue frenando.
            pre = escribir_arbol(filtrar(arbol_de(m.group(1))))
            if pre == actual:
                return (True, cabeza,
                        f"{RAMA_DESTINO} intacta: su árbol es el deploy PRE-TRANSFORMACIÓN "
                        f"de su Fuente declarada ({m.group(1)[:12]}) — anterior al "
                        f"stripper de comentarios; se publica encima")
            return (False, cabeza,
                    f"la punta de {RAMA_DESTINO} ({cabeza[:12]}) declara Fuente {m.group(1)[:12]} "
                    f"pero su árbol NO coincide con lo regenerado desde ahí\n"
                    f"  (ni con transformación ni sin ella): alguien editó {RAMA_DESTINO} a mano, "
                    f"o las reglas de exclusión\n"
                    f"  o de transformación cambiaron desde ese deploy.\n"
                    f"  Revisar con: git diff {actual[:12]} {regenerado[:12]}\n"
                    f"  Para publicar igual (PISANDO esa diferencia): --pisar")
        return (True, cabeza, f"{RAMA_DESTINO} intacta: su árbol coincide con lo regenerado "
                              f"desde su Fuente declarada ({m.group(1)[:12]})")
    # El detector de deploys en la historia usa EL MISMO regex que la marca
    # (MARCA_FUENTE), no un substring: un `git log --grep="Fuente: "` laxo
    # confundía un commit manual que dijera «Fuente: la TTF...» con un deploy
    # y daba el diagnóstico equivocado. Un solo criterio, imposible de
    # divergir.
    historia = git("log", "--format=%H%x01%B%x00", cabeza)
    con_deploy = [seg.split("\x01", 1)[0] for seg in historia.split("\x00")
                  if "\x01" in seg and MARCA_FUENTE.search(seg.split("\x01", 1)[1])]
    if con_deploy:
        return (False, cabeza,
                f"la punta de {RAMA_DESTINO} ({cabeza[:12]}) no es un commit de deploy, pero su "
                f"historia SÍ tiene deploys: alguien commiteó a mano encima del último.\n"
                f"  Revisar ese commit antes de pisarlo. Para publicar igual: --pisar")
    return (True, cabeza, f"{RAMA_DESTINO} sin deploys previos (la landing vieja): "
                          f"primer deploy, se publica encima")


def main():
    solo_verificar = "--solo-verificar" in sys.argv
    pisar = "--pisar" in sys.argv
    fuente_ref = None
    if "--fuente" in sys.argv:
        i = sys.argv.index("--fuente")
        if i + 1 >= len(sys.argv):
            sys.exit("--fuente necesita un ref (tag, hash o rama)")
        fuente_ref = sys.argv[i + 1]

    if fuente_ref is None:
        # Desde HEAD se exige árbol limpio: las guardas corrieron contra el
        # árbol de trabajo, y un árbol sucio significa que lo verificado y lo
        # que se va a publicar no son lo mismo.
        if git("status", "--porcelain").strip() and not solo_verificar:
            sys.exit("el árbol de trabajo no está limpio — commitear (y correr las "
                     "guardas) antes de publicar, o publicar un commit concreto con --fuente")
        fuente = git("rev-parse", "HEAD").strip()
        etiqueta = "HEAD de " + git("rev-parse", "--abbrev-ref", "HEAD").strip()
    else:
        fuente = git("rev-parse", f"{fuente_ref}^{{commit}}").strip()
        etiqueta = fuente_ref

    arbol_todo = arbol_de(fuente)
    sin_efecto = exclusiones_sin_efecto(arbol_todo)
    if sin_efecto and fuente_ref is None:
        # Desde HEAD, una exclusión que no matchea es la lista desactualizada
        # (¿se renombró el archivo?) y hay que frenar: maelstrom.css renombrado
        # se publicaría sin que la regla por tipo lo cace.
        print("LA GUARDA FRENÓ EL DEPLOY — nada se commiteó:")
        for pat in sin_efecto:
            print(f"  la exclusión «{pat}» no matchea nada en el commit fuente: "
                  f"la lista NO_PUBLICABLES quedó desactualizada (¿se renombró?)")
        return 1
    if sin_efecto:
        # Con --fuente explícito es lo ESPERABLE si el commit es anterior a la
        # creación del archivo — medido: en v1-content-complete no existía
        # assets/img/README.md y el freno estricto rompía el rollback. Se avisa
        # y se sigue; la regla por tipo vigila igual lo que sí exista.
        for pat in sin_efecto:
            print(f"  aviso: la exclusión «{pat}» no matchea nada en {etiqueta} — "
                  f"esperable en un commit anterior a su creación; la regla por tipo sigue vigilando")

    arbol_filtrado = filtrar(arbol_todo)
    # El árbol que se PUBLICA: filtrado + transformado (cero comentarios en
    # .html/.css/.js fuera de assets/vendor/). Las guardas de contenido miran
    # los bytes TRANSFORMADOS: lo verificado es lo publicado.
    arbol_pub = arbol_publicable(fuente)
    leer = lambda ruta: contenido(arbol_pub[ruta][1])
    leer_fuente = lambda ruta: contenido(arbol_filtrado[ruta][1])
    requeridos = (CRITICOS + CONTRATO) if fuente_ref is None else CRITICOS
    if fuente_ref is not None:
        for r in CONTRATO:
            if r not in arbol_pub:
                print(f"  aviso: {r} no existe en {etiqueta} — el sitio de ese "
                      f"día no lo tenía; se publica como era")
    problemas = (verificar_sin_notas(arbol_pub)
                 + verificar_completo(arbol_pub, leer, requeridos)
                 + verificar_identidad(arbol_pub, arbol_todo)
                 + verificar_transformacion(arbol_pub, leer_fuente, leer,
                                            desde_head=fuente_ref is None))
    if problemas:
        print("LA GUARDA FRENÓ EL DEPLOY — nada se commiteó:")
        for p in problemas:
            print("  " + p)
        return 1

    excluidos = sorted(set(arbol_todo) - set(arbol_pub))
    transformados = sorted(r for r in arbol_pub if transformable(r))
    print(f"Fuente: {fuente[:12]} ({etiqueta})")
    print(f"Árbol publicable: {len(arbol_pub)} archivos; excluidos {len(excluidos)} de trabajo; "
          f"{len(transformados)} transformados (comentarios fuera)")

    if solo_verificar:
        print("\nPublicables:")
        for ruta in sorted(arbol_pub):
            print(f"  {ruta}")
        print("\nExcluidos:")
        for ruta in excluidos:
            print(f"  {ruta}")
        print("\nVerificación OK (sin --solo-verificar arma además el commit en "
              f"{RAMA_DESTINO} local)")
        return 0

    ok, cabeza, msj = verificar_main_intacta()
    print("  " + msj)
    if not ok and not pisar:
        return 1

    oid_arbol = escribir_arbol(arbol_pub)
    if oid_arbol == git("rev-parse", f"{cabeza}^{{tree}}").strip():
        print(f"{RAMA_DESTINO} ya está en este contenido; no se commitea de nuevo")
        return 0

    mensaje = (f"Publicar el sitio — generado de {fuente[:12]}\n\n"
               f"Generado por tools/make-deploy.py desde la rama de desarrollo:\n"
               f"el sitio solo, sin las notas de trabajo. No editar esta rama a\n"
               f"mano — el próximo deploy lo detecta y frena; el flujo es siempre\n"
               f"desarrollo -> guardas -> make-deploy.\n\n"
               f"Fuente: {fuente} ({etiqueta})\n")
    commit = git("commit-tree", oid_arbol, "-p", cabeza, "-m", mensaje).strip()
    # El tercer argumento es compare-and-swap: si la rama se movió entre la
    # verificación y este update-ref, git frena en vez de pisar en silencio.
    git("update-ref", f"refs/heads/{RAMA_DESTINO}", commit, cabeza)
    print(f"  {RAMA_DESTINO} -> {commit[:12]} (local)")
    print("\nLo que sigue (a mano, en este orden — el detalle en el README, «Publicar»):")
    print(f"  1. verificar el artefacto una vez en navegador (check-modes contra el árbol de {RAMA_DESTINO};")
    print("     navega la portada y /hajime/ — el resto del artefacto ya lo cubrió la guarda 4)")
    print(f"  2. git push origin {RAMA_DESTINO}")
    print(f"  3. el tag de publicación va en el commit FUENTE ({fuente[:12]}), no en {RAMA_DESTINO}")
    print("  4. después del push: kotodamafinance.com/CLAUDE.md y /tools/check-ready.py tienen que dar 404")
    return 0


if __name__ == "__main__":
    sys.exit(main())
