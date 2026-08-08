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
sitio; el trabajo vive en la rama de desarrollo. Esto tapa las notas como
DOCUMENTOS con URL propia; NO tapa las menciones dentro de lo servido (los
comentarios de los HTML, en castellano, nombran CLAUDE.md y tools/ — política
ya decidida) ni el repo público en GitHub, donde la rama de desarrollo sigue
visible (limitación aceptada: repo privado + Pages exige plan de pago).

MAIN ES UNA RAMA-ARTEFACTO QUE NADIE EDITA A MANO, igual que `maintenance`: un
artefacto derivado no se mantiene, se regenera. La tentación contra la que esto
defiende es el hotfix directo en main «porque es una línea»: el próximo deploy
lo pisaría en silencio. Por eso el script compara el main actual contra lo que
él mismo generaría desde el hash que ese commit declara (la línea `Fuente:`) y
FRENA si no coinciden — ver verificar_main_intacta().

EL MECANISMO ES PLUMBING, SIN CHECKOUT — el patrón de make-maintenance.py: se
leen los blobs del commit fuente (mismos OID, así que lo probado y lo publicado
son byte-idénticos POR CONSTRUCCIÓN: ni copia por filesystem, ni riesgo CRLF),
se arma el árbol filtrado con un índice temporal, y se commitea sobre main con
el hash fuente en el mensaje. El árbol de trabajo y HEAD no se tocan en ningún
momento. El push lo hace el autor, aparte — este script sólo mueve la rama
LOCAL.

LA GUARDA ES TODO-O-NADA y corre adentro, antes de commitear (probada EN ROJO
contra sus tres modos de falla antes de confiar en su verde — el registro está
en CLAUDE.md, decisión de la rama de deploy):

1. COMPLETO — cada URL del sitemap tiene su index.html; cada referencia
   relativa o absoluta-de-sitio de los HTML (href/src + import map), el CSS
   (url()) y los JS (import) resuelve dentro del árbol; y los archivos
   requeridos están — en dos niveles: los CRITICOS (CNAME, .nojekyll, index,
   404) son duros SIEMPRE, el CONTRATO (favicons, manifest, og-image, robots,
   sitemap) es duro desde HEAD y aviso bajo --fuente. La partición está
   explicada junto a las constantes.
2. SIN NOTAS — por TIPO además de por lista: cero .md, .py y .json en lo
   publicado (el sitio no sirve ninguno de esos tipos; el manifest es
   .webmanifest), cero tools/ y docs/. Una nota futura con CUALQUIER nombre
   cae por el tipo, sin depender de que la lista de exclusión esté al día.
   La excepción que el tipo NO caza es maelstrom.css —un .css legítimo—, por
   eso está en la lista explícita Y en una comprobación propia.
3. IDENTIDAD — cada blob del árbol publicado tiene el mismo OID que en el
   commit fuente. Hoy es trivialmente cierto por construcción; existe para que
   una refactorización futura que transforme archivos en el camino no pase en
   silencio.

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
    """Cada blob publicado es EL MISMO objeto que en el commit fuente."""
    problemas = []
    for ruta, (modo, oid) in sorted(arbol_pub.items()):
        if ruta not in arbol_fuente:
            problemas.append(f"{ruta}: está en el árbol publicado y no en el commit fuente")
        elif arbol_fuente[ruta] != (modo, oid):
            problemas.append(f"{ruta}: blob distinto del commit fuente "
                             f"({oid[:12]} != {arbol_fuente[ruta][1][:12]})")
    return problemas


# ---------------------------------------------------------------------------
# Escritura y protección de main
# ---------------------------------------------------------------------------

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
        regenerado = escribir_arbol(filtrar(arbol_de(m.group(1))))
        actual = git("rev-parse", f"{cabeza}^{{tree}}").strip()
        if regenerado != actual:
            return (False, cabeza,
                    f"la punta de {RAMA_DESTINO} ({cabeza[:12]}) declara Fuente {m.group(1)[:12]} "
                    f"pero su árbol NO coincide con lo regenerado desde ahí:\n"
                    f"  alguien editó {RAMA_DESTINO} a mano, o las reglas de exclusión cambiaron "
                    f"desde ese deploy.\n"
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

    arbol_pub = filtrar(arbol_todo)
    leer = lambda ruta: contenido(arbol_pub[ruta][1])
    requeridos = (CRITICOS + CONTRATO) if fuente_ref is None else CRITICOS
    if fuente_ref is not None:
        for r in CONTRATO:
            if r not in arbol_pub:
                print(f"  aviso: {r} no existe en {etiqueta} — el sitio de ese "
                      f"día no lo tenía; se publica como era")
    problemas = (verificar_sin_notas(arbol_pub)
                 + verificar_completo(arbol_pub, leer, requeridos)
                 + verificar_identidad(arbol_pub, arbol_todo))
    if problemas:
        print("LA GUARDA FRENÓ EL DEPLOY — nada se commiteó:")
        for p in problemas:
            print("  " + p)
        return 1

    excluidos = sorted(set(arbol_todo) - set(arbol_pub))
    print(f"Fuente: {fuente[:12]} ({etiqueta})")
    print(f"Árbol publicable: {len(arbol_pub)} archivos; excluidos {len(excluidos)} de trabajo")

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
    print(f"  1. verificar el artefacto una vez en navegador (check-modes contra el árbol de {RAMA_DESTINO})")
    print(f"  2. git push origin {RAMA_DESTINO}")
    print(f"  3. el tag de publicación va en el commit FUENTE ({fuente[:12]}), no en {RAMA_DESTINO}")
    print("  4. después del push: kotodamafinance.com/CLAUDE.md y /tools/check-ready.py tienen que dar 404")
    return 0


if __name__ == "__main__":
    sys.exit(main())
