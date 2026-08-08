#!/usr/bin/env python3
"""Genera la página de mantenimiento y la publica en la rama `maintenance`.

    python tools/make-maintenance.py              # construye en _dev/maintenance/
    python tools/make-maintenance.py --publicar   # además, actualiza la rama

LA RAMA ES UN ARTEFACTO DERIVADO, NO UNA COPIA A MANO. Ésa es la respuesta a la
pregunta que abrió esto: copiar el woff2 del sitio queda desactualizado y
mantener un subset propio duplica el trabajo — pero sólo si la rama se edita a
mano. Generada, no se mantiene: se regenera. Es el mismo trato que ya tienen
sitemap.xml, og-image.png y los favicons, y por eso el script vive acá.

QUÉ TIENE QUE SER CIERTO DE ESTA PÁGINA, porque todo lo demás sale de ahí:

1. **Es un cartel, no una página.** Una sola petición HTTP: el HTML trae adentro
   el CSS, el favicon y las fuentes. Con archivos aparte el titular aparecería
   primero en una fuente del sistema y saltaría al llegar la buena — en una
   página de cinco líneas ese salto es lo único que se ve.
2. **La rama tiene DOS archivos de contenido y nada más**, así que cualquier
   referencia externa —un <link>, un <script>, un <img>— es un 404 por
   construcción. No es una preferencia de tamaño: no hay dónde poner el archivo.
3. **No depende de JavaScript ni de WebGL.** El degradado del fondo es el mismo
   «piso atmosférico» que styles.css declara para cuando el océano no arranca.

LOS SUBSETS SON MICRO Y ESTÁN CONGELADOS. Se derivan del texto de esta misma
página (ver `caracteres()`), que es fijo y no va a crecer: por eso este subset
no tiene la deriva que sí tiene el del sitio, donde el japonés se agranda cada
vez que se escribe una página. Un conjunto de entrada cerrado no se desactualiza.

EL JAPONÉS ES EL CASO DELICADO Y NO FALLA COMO UNO ESPERA. 守, 作 y 中 NO están
en el subset de Zen Kaku del sitio: son tres de los cinco glifos del titular.
Lo intuitivo es pensar que copiar el woff2 commiteado daría tofu y se vería al
instante. NO: el fallback de fuentes es POR GLIFO, así que el titular se dibuja
entero y parece bien. Medido con CSS.getPlatformFontsForNode:

    'Zen Kaku', sans-serif          ->  2 glifos Zen Kaku + 3 Microsoft YaHei
    'Hiragino', 'Yu Gothic', s-s    ->  5 glifos Yu Gothic Medium
    sans-serif CON lang="ja"        ->  5 glifos Noto Sans JP
    sans-serif SIN lang             ->  5 glifos Microsoft YaHei

O sea que el modo de fallo de copiar el subset no es un hueco visible: es un
titular en dos tipografías, y una de ellas **china**. Se lee bien, pasa la
inspección visual y nadie lo nota — en la rama que ninguna guarda del sitio
mira. Ver JA_EMBEBIDO.

Y la última fila explica por qué `lang="ja"` no es decoración semántica acá:
es lo que decide si el navegador elige una fuente japonesa o una china cuando
tiene que recurrir al genérico. Va en los dos <span> japoneses.
"""
import base64
import io
import os
import re
import subprocess
import sys

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "_dev", "maintenance")
RAMA = "maintenance"

# --------------------------------------------------------------------------
# EL TEXTO. Dictado por el autor; es el único lugar donde vive.
# --------------------------------------------------------------------------
JA_TITULO = "保守作業中"
JA_LOGO = "言霊"
EN_TITULO = "The site is being rebuilt."
EN_CUERPO = ("Kotodama Finance is undergoing substantial work and is offline "
             "for now. Nothing has been lost — it will be back.")
EN_CONTACTO = "If you need to reach us in the meantime:"
CORREO = "contact@kotodamafinance.com"
MARCA = "Kotodama Finance"

TITULO_HTML = "Under maintenance — Kotodama Finance"
DESCRIPCION = "Kotodama Finance is offline while the site is rebuilt."

# --------------------------------------------------------------------------
# ZEN KAKU VA EMBEBIDO. Estuvo en False mientras al subset del repo le faltaban
# 守 (U+5B88), 作 (U+4F5C) y 中 (U+4E2D); se regeneró con el conjunto derivado y
# ahora los tiene, así que el cartel no depende de las fuentes del visitante.
#
# POR QUÉ SE EMBEBE Y NO SE DEJA LA PILA DEL SISTEMA. La pila declarada funciona
# —medido: los cinco glifos en Yu Gothic Medium, una sola cara japonesa— pero
# hace que la página se vea distinta en cada máquina, y ésta es justo la que se
# muestra cuando algo salió mal. Ahí la consistencia vale más que los 2 KB. El
# hueco que cierra es Linux pelado sin fuentes CJK, donde el titular era tofu.
#
# LOS TRES GLIFOS VIVEN EN EL SUBSET DEL SITIO AUNQUE NINGUNA PÁGINA LOS USE, y
# es a propósito: este script sólo puede leer archivos del repo. Si leyera la
# TTF de origen —que no está versionada, a propósito— la rama dejaría de poder
# regenerarse en otra máquina. Mismo trato que 立方体 y 一次資料, que están
# reservados para /ja/; la fórmula de derivación los preserva sola porque la
# primera mitad es la unión con el subset ACTUAL.
#
# Puesto en True, el script NO adivina: si falta un glifo aborta nombrándolo.
# Es la diferencia que importa, porque el fallback por glifo hace que la versión
# rota se vea bien (ver el encabezado): acá el fallo tiene que ser ruidoso.
# --------------------------------------------------------------------------
JA_EMBEBIDO = True

# Los tokens que usa la página. Se LEEN del :root de styles.css, no se copian:
# la paleta tiene que seguir siendo una entrada real de este archivo. Igual que
# make-og-image.py, y por el mismo motivo.
TOKENS = (
    "--c-navy", "--c-surface-about", "--c-sea-hi",
    "--c-gold", "--c-gold-soft",
    "--c-text", "--c-text-body", "--c-text-mist",
    "--rgb-mist", "--rgb-gold",
)


def tokens():
    """Devuelve {nombre: valor} leyendo el :root, con el valor tal cual está.

    Sin fallback, igual que cube.js y make-og-image.py: si falta un token, falla
    con su nombre en vez de disfrazarlo con un hex de repuesto.
    """
    css = open(os.path.join(RAIZ, "assets", "css", "styles.css"),
               encoding="utf-8").read()
    m = re.search(r":root\s*\{.*?\n\}", css, flags=re.S)
    if not m:
        sys.exit("no se encontró el bloque :root en styles.css")
    bloque = m.group(0)
    vals = {}
    for n in TOKENS:
        h = re.search(rf"{re.escape(n)}\s*:\s*([^;]+);", bloque)
        if not h:
            sys.exit(f"falta el token {n} en :root")
        vals[n] = h.group(1).strip()
    return vals


def caracteres():
    """Los tres conjuntos de caracteres, DERIVADOS del texto de arriba.

    Derivados y no transcritos, por la misma razón que el subset del sitio: una
    lista escrita a mano es una copia, y una copia se desfasa del texto en
    silencio. Acá además el fallo sería mudo — un glifo que falta no rompe nada,
    sólo cae a otra fuente.
    """
    ja = set(JA_TITULO + JA_LOGO)
    display = set(EN_TITULO)
    ui = set(MARCA + MARCA.upper() + EN_CUERPO + EN_CONTACTO + CORREO + " ")
    return "".join(sorted(ja)), "".join(sorted(display)), "".join(sorted(ui))


def recortar(archivo, texto, ejes=None, exigir=True):
    """Subsetea un woff2 del repo a `texto` y lo devuelve en base64.

    `ejes` fija o acota los ejes variables DESPUÉS de subsetear: al revés
    fontTools revienta con un KeyError de glifo. Fijar opsz y acotar wght al
    rango que la página realmente usa es lo que hace que Inter pase de 34,7 KB a
    14,2 KB en base64 — el peso variable entero está de más en un cartel.

    Se conservan los name IDs completos porque ahí viven el copyright y la
    licencia OFL, y esto es redistribución de la fuente aunque vaya embebida.

    EFECTO SECUNDARIO DE ESO, que confunde una medición: la tabla `name` viene
    de la fuente de origen y NO la actualiza el instanciado, así que
    `CSS.getPlatformFontsForNode` informa «Cormorant Garamond Light» para una
    cara fijada en 500. Es sólo la etiqueta. Verificado en los contornos:
    `usWeightClass` da 500 y la bbox de la «T» coincide con la instancia 500 y
    no con la 300. El CSS empareja por el nombre del @font-face, no por éste.

    SE PRESERVA head.modified DE LA FUENTE DE ORIGEN. Al guardar, fontTools
    escribe ahí la hora actual, o sea el reloj de pared como entrada del
    artefacto. Copiarlo de la fuente en vez de fijar una constante mantiene la
    propiedad útil: si cambia el woff2 de origen, el resultado cambia de verdad.

    OJO: ESTO NO ALCANZA PARA QUE LA SALIDA SEA REPRODUCIBLE, y conviene saberlo
    antes de escribir una guarda que lo suponga. Medido: tres corridas seguidas
    dan tres sha1 distintos, y siguen dándolos con head fijado y con
    PYTHONHASHSEED=0. La diferencia arranca dentro del woff2 —en el propio
    tamaño comprimido—, así que el no-determinismo es del codificador Brotli, no
    de nada que este script controle.
    Consecuencia práctica: `check-maintenance.py` NO compara bytes. Compara el
    HTML con los base64 elididos (eso sí es estable, verificado) y las fuentes
    por su cmap. Una guarda de «regenerar y comparar» habría estado en rojo
    siempre, que es la clase de señal que se aprende a ignorar.
    """
    ruta = os.path.join(RAIZ, "assets", "fonts", archivo)
    f = TTFont(ruta)
    sello = (f["head"].created, f["head"].modified)
    cmap = set().union(*[set(t.cmap) for t in f["cmap"].tables])
    faltan = [c for c in texto if ord(c) not in cmap]
    if faltan and exigir:
        sys.exit(f"{archivo}: faltan {' '.join(f'{c} U+{ord(c):04X}' for c in faltan)}\n"
                 f"  -> regenerar el subset del sitio (ver el @font-face de styles.css)")

    o = subset.Options()
    o.flavor = "woff2"
    o.name_IDs = ["*"]
    # Las latinas van con layout_features='*' por lo mismo que en el sitio:
    # sin el flag el archivo sale distinto. Acá el subset es de 30 glifos y la
    # diferencia es de bytes, pero la regla es que el comando reproduzca lo que
    # se sirve, y dos criterios distintos en el mismo repo se confunden.
    o.layout_features = ["*"]
    s = subset.Subsetter(options=o)
    s.populate(text=texto)
    s.subset(f)

    if ejes:
        f = instancer.instantiateVariableFont(f, ejes, inplace=False)

    f["head"].created, f["head"].modified = sello
    b = io.BytesIO()
    f.flavor = "woff2"
    f.save(b)
    return base64.b64encode(b.getvalue()).decode("ascii"), len(b.getvalue())


def favicon():
    """El favicon del sitio, inline. Es un PATH, no texto: no depende de fuentes."""
    svg = open(os.path.join(RAIZ, "favicon.svg"), encoding="utf-8").read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\s+", " ", svg).strip()
    # Sólo lo que rompe un atributo HTML o una data: URI. Dejar el resto legible
    # ahorra ~40% contra urlencodear todo.
    for a, b in (("%", "%25"), ("#", "%23"), ('"', "%22"), ("<", "%3C"), (">", "%3E")):
        svg = svg.replace(a, b)
    return "data:image/svg+xml," + svg


def stripper():
    """El stripper de comentarios del deploy, importado de make-deploy.py.

    CERO COMENTARIOS EN LO SERVIDO rige también acá (requisito del autor,
    2026-08-08 — la regla del deploy 8, extendida a esta rama el mismo día):
    los comentarios viven en la PLANTILLA de este script, que es el fuente, y
    se eliminan del artefacto. Se reusa LA MISMA transformación del deploy a
    propósito — dos implementaciones del mismo requisito derivan, y ésta ya
    está probada (17 fixtures + 11 mutaciones + revisión adversarial). El
    import es por ruta porque el guion del nombre impide el import normal.

    La procedencia («no editar la rama a mano») NO se pierde con el
    comentario GENERADO: vive en el mensaje del commit de la rama.
    """
    import importlib.util
    carpeta = os.path.dirname(os.path.abspath(__file__))
    if carpeta not in sys.path:
        sys.path.insert(0, carpeta)  # make-deploy importa _guardas
    spec = importlib.util.spec_from_file_location(
        "make_deploy", os.path.join(carpeta, "make-deploy.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def construir():
    tk = tokens()
    ja, display, ui = caracteres()
    caras, pesos = [], []

    if JA_EMBEBIDO:
        b64, n = recortar("zen-kaku-gothic-new-500-subset.woff2", ja)
        caras.append(("Zen Kaku Gothic New", "500", b64))
        pesos.append(("Zen Kaku 500", len(ja), n))

    b64, n = recortar("cormorant-garamond-latin.woff2", display, {"wght": 500})
    caras.append(("Cormorant Garamond", "500", b64))
    pesos.append(("Cormorant 500", len(display), n))

    # Inter mantiene el rango 400-500, no un peso fijo: el cuerpo va en 400 y el
    # rótulo de marca en 500, y son la misma cara. El rango declarado es el
    # mismo que el @font-face del sitio, con la misma consecuencia — pedir 700
    # acá lo recorta a 500.
    b64, n = recortar("inter-latin.woff2", ui, {"opsz": 14, "wght": (400, 400, 500)})
    caras.append(("Inter", "400 500", b64))
    pesos.append(("Inter 400-500", len(ui), n))

    caras_css = "\n".join(
        f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{peso};"
        f"font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}"
        for fam, peso, b in caras)

    raiz_css = ";".join(f"{n}:{v}" for n, v in tk.items())
    html = PLANTILLA.format(
        titulo=TITULO_HTML, descripcion=DESCRIPCION, favicon=favicon(),
        navy=tk["--c-navy"], raiz=raiz_css, caras=caras_css,
        ja_titulo=JA_TITULO, ja_logo=JA_LOGO, marca=MARCA,
        en_titulo=EN_TITULO, en_cuerpo=EN_CUERPO,
        en_contacto=EN_CONTACTO, correo=CORREO,
        modo_ja="Zen Kaku embebido" if JA_EMBEBIDO else "pila del sistema",
    )
    # El artefacto sale SIN comentarios, por la misma puerta que el deploy
    # (ver stripper()). Va acá y no en publicar() para que _dev/maintenance/
    # y la rama sean el mismo texto — check-maintenance compara uno contra
    # otro con los base64 elididos, y dos versiones romperían esa guarda.
    html = stripper().transformar("index.html", html.encode("utf-8")).decode("utf-8")
    return html, pesos


PLANTILLA = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<!-- noindex: no se quiere el estado de mantenimiento en el índice de nadie.
     El costo asumido: un noindex sostenido hace que un buscador deje caer las
     URLs, y volver a indexarlas lleva tiempo. Se acepta porque el sitio nuevo
     todavía no se publicó — no hay ranking que perder. Si esta rama llegara a
     estar meses arriba sobre un sitio ya indexado, hay que reabrirlo. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{navy}">
<link rel="icon" href="{favicon}">
<!-- GENERADO por tools/make-maintenance.py. No editar acá: se pierde en la
     próxima corrida. El texto y el diseño viven en ese script.
     Japonés: {modo_ja}. -->
<style>
{caras}
:root{{{raiz};--font-display:'Cormorant Garamond',Georgia,'Times New Roman',serif;--font-ui:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;--font-ja:'Zen Kaku Gothic New','Hiragino Kaku Gothic ProN','Yu Gothic',sans-serif}}
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
body{{
  background:
    radial-gradient(120% 90% at 62% 8%, rgb(var(--rgb-mist) / 0.10) 0%, rgb(var(--rgb-mist) / 0) 42%),
    linear-gradient(160deg, var(--c-sea-hi) 0%, var(--c-surface-about) 46%, var(--c-navy) 100%);
  background-attachment:fixed;
  color:var(--c-text-body);
  font-family:var(--font-ui);
  font-weight:400;
  line-height:1.6;
  -webkit-font-smoothing:antialiased;
  display:flex;align-items:center;justify-content:center;
  min-height:100vh;min-height:100svh;
  padding:clamp(28px,7vw,64px);
}}
:lang(ja){{font-family:var(--font-ja)}}
a:focus-visible{{outline:2px solid var(--c-gold);outline-offset:3px;border-radius:2px}}
.sign{{max-width:34rem;width:100%}}
.sign__brand{{display:flex;align-items:baseline;gap:12px;color:var(--c-gold);margin-bottom:clamp(30px,6vw,44px)}}
.sign__mark{{font-family:var(--font-ja);font-weight:500;font-size:1.6rem;letter-spacing:0.08em;line-height:1}}
.sign__word{{font-weight:500;font-size:0.72rem;letter-spacing:0.4em;color:var(--c-text-mist);text-transform:uppercase}}
.rule{{width:60px;height:1px;background:rgb(var(--rgb-gold) / 0.35);margin-bottom:clamp(26px,5vw,34px)}}
.sign__title{{display:flex;flex-direction:column;gap:14px;margin-bottom:28px;font-weight:500}}
.sign__ja{{font-family:var(--font-ja);font-weight:500;font-size:clamp(2rem,5.4vw,2.9rem);line-height:1.2;letter-spacing:0.06em;color:var(--c-text)}}
.sign__en{{font-family:var(--font-display);font-weight:500;font-size:clamp(1.45rem,3.4vw,1.95rem);line-height:1.25;color:var(--c-gold);text-wrap:balance}}
.sign__body{{font-size:1.02rem;line-height:1.8;color:var(--c-text-body);margin-bottom:24px;text-wrap:pretty}}
.sign__contact{{font-size:0.95rem;line-height:1.7;color:var(--c-text-mist)}}
.sign__contact a{{color:var(--c-gold);text-decoration:none;border-bottom:1px solid rgb(var(--rgb-gold) / 0.35)}}
.sign__contact a:hover{{color:var(--c-gold-soft);border-bottom-color:var(--c-gold-soft)}}
@media (max-width:420px){{.sign__word{{letter-spacing:0.28em}}}}
</style>
</head>
<body>
<main class="sign">
  <!-- El mismo lockup del nav del sitio, sin ser un enlace: en esta rama no hay
       ningún destino al que llevar. -->
  <p class="sign__brand">
    <span class="sign__mark" lang="ja">{ja_logo}</span>
    <span class="sign__word">{marca}</span>
  </p>
  <div class="rule"></div>
  <!-- Japonés arriba en blanco y el inglés abajo en oro: es el mismo reparto
       que el <h1> de las seis caras (kanji en --c-text, romaji en --c-gold). -->
  <h1 class="sign__title">
    <span class="sign__ja" lang="ja">{ja_titulo}</span>
    <span class="sign__en">{en_titulo}</span>
  </h1>
  <p class="sign__body">{en_cuerpo}</p>
  <p class="sign__contact">{en_contacto} <a href="mailto:{correo}">{correo}</a></p>
</main>
</body>
</html>
"""


def publicar(html):
    """Escribe la rama con plumbing, SIN checkout y SIN tocar el árbol.

    Es a propósito: un `git checkout --orphan` seguido de `git rm -rf .` sobre
    el repo de trabajo es la clase de comando que borra lo que no debía si algo
    sale mal en el medio. Acá el árbol de trabajo no se toca en ningún momento
    y HEAD tampoco se mueve.
    """
    def git(*args, entrada=None):
        r = subprocess.run(("git",) + args, cwd=RAIZ, input=entrada,
                           capture_output=True)
        if r.returncode:
            sys.exit(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace')}")
        return r.stdout.decode("utf-8").strip()

    def blob(datos):
        return git("hash-object", "-w", "--stdin", entrada=datos)

    # CNAME va COPIADO del repo, no escrito a mano: es el archivo del que
    # depende que kotodamafinance.com siga apuntando acá (ver README).
    cname = open(os.path.join(RAIZ, "CNAME"), "rb").read()
    h = html.encode("utf-8")
    entradas = {
        ".nojekyll": b"",
        "404.html": h,
        "CNAME": cname,
        "index.html": h,
    }
    lineas = "".join(f"100644 blob {blob(v)}\t{k}\n" for k, v in sorted(entradas.items()))
    arbol = git("mktree", entrada=lineas.encode("utf-8"))

    anterior = subprocess.run(("git", "rev-parse", "--verify", "-q", f"refs/heads/{RAMA}"),
                              cwd=RAIZ, capture_output=True).stdout.decode().strip()
    if anterior:
        previo = git("rev-parse", f"{RAMA}^{{tree}}")
        if previo == arbol:
            print(f"  la rama {RAMA} ya está en este contenido; no se commitea de nuevo")
            return
    padre = ("-p", anterior) if anterior else ()
    mensaje = ("Regenerar la pagina de mantenimiento\n\n"
               "Generada por tools/make-maintenance.py desde redesign-trust.\n"
               "No editar los archivos de esta rama a mano.\n")
    commit = git("commit-tree", arbol, *padre, "-m", mensaje)
    git("update-ref", f"refs/heads/{RAMA}", commit)
    print(f"  rama {RAMA} -> {commit[:7]} ({'nuevo commit' if anterior else 'rama nueva, sin padre'})")


def main():
    html, pesos = construir()
    os.makedirs(SALIDA, exist_ok=True)
    for nombre in ("index.html", "404.html"):
        with open(os.path.join(SALIDA, nombre), "w", encoding="utf-8", newline="\n") as f:
            f.write(html)

    print("Fuentes embebidas")
    for etq, n_car, n_bytes in pesos:
        print(f"  {etq:16} {n_car:3} caracteres  {n_bytes/1024:5.2f} KB  "
              f"({n_bytes*4//3/1024:5.2f} KB en base64)")
    if not JA_EMBEBIDO:
        print("  Japonés         pila del sistema (JA_EMBEBIDO = False)")

    print(f"\nPágina  {len(html.encode('utf-8'))/1024:.1f} KB, una sola petición")
    print(f"Escrita en _dev/maintenance/ (index.html y 404.html, idénticos)")

    if "--publicar" in sys.argv:
        print("\nPublicando en la rama")
        publicar(html)
    else:
        print("\n(no se publicó: correr con --publicar para actualizar la rama)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
