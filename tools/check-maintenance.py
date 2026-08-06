#!/usr/bin/env python3
"""Guarda de la rama `maintenance`. A DEMANDA, no en cada commit.

    python tools/check-maintenance.py

CUÁNDO CORRERLA: al tocar la rama, y **antes de activarla** en GitHub Pages.
No entra en el flujo de cuatro guardas de cada commit a propósito: mira una rama
que no cambia entre commits, así que ahí sólo agregaría ruido — y una guarda que
se corre por costumbre y siempre da lo mismo se deja de leer.

POR QUÉ NECESITA GUARDA PROPIA. Las del sitio no le sirven: no tiene nav ni
footer que comparar, ni sitemap, ni baseline de placeholders. Pero es la rama
con el peor perfil de fallo del repo — se publica justo cuando el sitio está
caído, o sea cuando nadie puede comparar contra nada, y cada cosa que puede
romperse ahí se rompe EN SILENCIO:

  · una referencia externa (un <link>, un <script>, un <img>) es un 404 seguro,
    porque en la rama no hay más archivos que éstos;
  · si falta CNAME, GitHub Pages da de baja el dominio propio;
  · si al japonés le falta un glifo NO se ve un hueco: el fallback es por glifo
    y el titular sale en dos tipografías, una de ellas china (ver
    make-maintenance.py);
  · si los dos archivos se separan, la portada dice una cosa y el resto otra.

Ninguna de esas cuatro se nota mirando la página.

NO COMPARA BYTES contra el generador, y no es por comodidad: el codificador
woff2 no es determinista —tres corridas, tres sha1— así que esa guarda estaría
en rojo siempre. Compara el HTML con los base64 elididos, que sí es estable, y
las fuentes por su tabla cmap, que es lo que de verdad importa.

Salida: 0 todo bien · 1 hay algo roto · 2 la rama no existe todavía.
"""
import base64
import io
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# El nombre de la rama se puede pasar por argumento. No es una comodidad: es lo
# que permite probar la guarda EN ROJO, armando una rama rota a un lado sin
# tocar la buena. Una guarda que sólo se vio en verde no está verificada.
RAMA = sys.argv[1] if len(sys.argv) > 1 else "maintenance"
ARCHIVOS = (".nojekyll", "404.html", "CNAME", "index.html")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

fallos = []


def revisar(ok, descripcion, detalle=""):
    print(("  OK    " if ok else "  FALLA ") + " " + descripcion
          + (f"  [{detalle}]" if detalle and not ok else ""))
    if not ok:
        fallos.append(descripcion)


def git(*args):
    r = subprocess.run(("git",) + args, cwd=RAIZ, capture_output=True)
    if r.returncode:
        sys.exit(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace')}")
    return r.stdout


def japones(txt):
    """Los caracteres japoneses del texto. Mismo criterio que _guardas.JAPONES
    (unificado el 2026-08-06: esta copia decía «mismo criterio» y ya había
    derivado — miraba full-width pero no puntuación CJK, y su rango de kanji
    empezaba en U+4E00 en vez de U+3400)."""
    return {c for c in txt if "　" <= c <= "〿" or "぀" <= c <= "ヿ"
            or "㐀" <= c <= "鿿" or "＀" <= c <= "￯"}


def main():
    ref = subprocess.run(("git", "rev-parse", "--verify", "-q", f"refs/heads/{RAMA}"),
                         cwd=RAIZ, capture_output=True).stdout.decode().strip()
    if not ref:
        print(f"La rama {RAMA} no existe. Crearla con:")
        print("  python tools/make-maintenance.py --publicar")
        return 2

    print(f"Rama {RAMA} en {ref[:7]}\n")

    print("Contenido de la rama")
    arbol = git("ls-tree", "--name-only", RAMA).decode().split()
    revisar(sorted(arbol) == sorted(ARCHIVOS),
            f"exactamente {len(ARCHIVOS)} archivos: " + ", ".join(ARCHIVOS),
            "hay " + ", ".join(sorted(arbol)))

    # Los dos HTML tienen que ser EL MISMO blob: la portada y cualquier ruta
    # inexistente sirven el mismo cartel. Comparar sha del árbol y no el texto
    # es más fuerte y más barato.
    sha = {}
    for n in ("index.html", "404.html"):
        linea = git("ls-tree", RAMA, n).decode().split()
        sha[n] = linea[2] if len(linea) > 2 else None
    revisar(sha["index.html"] is not None and sha["index.html"] == sha["404.html"],
            "index.html y 404.html son el mismo blob",
            f"{sha['index.html']} vs {sha['404.html']}")

    # CNAME: si falta o cambia, Pages da de baja el dominio propio. Se compara
    # contra el del sitio, no contra una constante escrita acá.
    try:
        cname_rama = git("show", f"{RAMA}:CNAME")
        cname_sitio = open(os.path.join(RAIZ, "CNAME"), "rb").read()
        revisar(cname_rama == cname_sitio, "CNAME idéntico al del sitio",
                f"{cname_rama!r} vs {cname_sitio!r}")
    except SystemExit:
        revisar(False, "CNAME idéntico al del sitio", "no está en la rama")

    html = git("show", f"{RAMA}:index.html").decode("utf-8")

    print("\nAutonomía (en la rama no hay ningún otro archivo que servir)")
    revisar("<script" not in html.lower(), "sin <script>")
    externos = [u for u in re.findall(r'\b(?:src|href)\s*=\s*"([^"]+)"', html)
                if not u.startswith(("data:", "mailto:"))]
    revisar(not externos, "ninguna referencia externa (src/href)",
            ", ".join(externos[:4]))
    revisar("@import" not in html and "url(http" not in html,
            "el CSS no trae nada de afuera")

    print("\nMetadatos")
    revisar(re.search(r'name="robots"[^>]*content="[^"]*noindex', html) is not None,
            "noindex declarado")
    revisar("<html lang=\"en\">" in html, "lang del documento en inglés")

    # El correo se compara contra el del sitio: dos direcciones distintas en el
    # mismo proyecto es exactamente el fallo que esta rama no puede permitirse,
    # porque acá es el ÚNICO camino de vuelta.
    sitio = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
    esperado = set(re.findall(r'mailto:([^"]+)"', sitio))
    en_rama = set(re.findall(r'mailto:([^"]+)"', html))
    revisar(len(en_rama) == 1 and en_rama <= esperado,
            "el mailto es el mismo que usa el sitio",
            f"rama {en_rama or '(ninguno)'} vs sitio {esperado}")

    print("\nCobertura de las fuentes embebidas")
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("  (omitido: falta fontTools — pip install fonttools brotli)")
        TTFont = None

    if TTFont:
        cubierto, familias = set(), []
        for fam, b64 in re.findall(
                r"font-family:'([^']+)'[^}]*?base64,([A-Za-z0-9+/=]+)\)", html):
            f = TTFont(io.BytesIO(base64.b64decode(b64)))
            cubierto |= set().union(*[set(t.cmap) for t in f["cmap"].tables])
            familias.append(fam)
        revisar(bool(familias), "hay al menos una fuente embebida",
                "no se encontró ninguna @font-face con data:")

        # El texto visible, sin etiquetas ni CSS. Se toma el INTERIOR de <body>
        # con un grupo, no partiendo la cadena: `split("<body")[-1]` deja
        # colgando el «>» de la propia etiqueta, y ese «>» suelto se cuela como
        # carácter visible. Lo dio esta guarda en su primera corrida, contra una
        # página que estaba bien: un test roto disfrazado de bug de la página.
        cuerpo = re.sub(r"<style.*?</style>|<!--.*?-->", " ", html, flags=re.S)
        m = re.search(r"<body[^>]*>(.*)</body>", cuerpo, flags=re.S)
        cuerpo = re.sub(r"<[^>]+>", " ", m.group(1) if m else "")
        ja = japones(cuerpo)
        latin = {c for c in cuerpo if 0x20 <= ord(c) < 0x250 and not c.isspace()}

        faltan_l = sorted(c for c in latin if ord(c) not in cubierto)
        revisar(not faltan_l, f"latín cubierto ({len(latin)} caracteres)",
                " ".join(f"{c} U+{ord(c):04X}" for c in faltan_l))

        faltan_ja = sorted(c for c in ja if ord(c) not in cubierto)
        if faltan_ja and len(faltan_ja) == len(ja):
            # Modo declarado: NINGÚN glifo japonés embebido. Es una decisión
            # tomada (ver JA_EMBEBIDO), no una regresión, así que no falla —
            # pero se informa, porque un lector merece saber que el titular
            # depende de la fuente del visitante.
            print(f"  nota    japonés NO embebido: {''.join(sorted(ja))} "
                  f"van por la pila del sistema")
            print("          -> es la decisión vigente (JA_EMBEBIDO en make-maintenance.py);")
            print("             el riesgo es un equipo sin fuentes CJK")
        else:
            revisar(not faltan_ja, f"japonés cubierto ({len(ja)} caracteres)",
                    " ".join(f"{c} U+{ord(c):04X}" for c in faltan_ja))

    print("\nLa rama es lo que produce el generador")
    r = subprocess.run((sys.executable, os.path.join(RAIZ, "tools", "make-maintenance.py")),
                       cwd=RAIZ, capture_output=True)
    if r.returncode:
        revisar(False, "el generador corre sin error",
                r.stderr.decode("utf-8", "replace")[-160:])
    else:
        recien = open(os.path.join(RAIZ, "_dev", "maintenance", "index.html"),
                      encoding="utf-8").read()
        elidir = lambda s: re.sub(r"base64,[A-Za-z0-9+/=]+", "base64,-", s)
        revisar(elidir(recien) == elidir(html),
                "el HTML publicado coincide con el generado (fuentes elididas)",
                "regenerar y republicar: python tools/make-maintenance.py --publicar")

    ok = not fallos
    print("\nMAINTENANCE OK" if ok else f"\nMAINTENANCE ROTA: {len(fallos)} problema(s)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
