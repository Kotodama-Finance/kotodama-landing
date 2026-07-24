#!/usr/bin/env python3
"""Genera og-image.png: la tarjeta que se ve al compartir un enlace del sitio.

    python tools/make-og-image.py          # requiere el sitio servido en :8000

1200x630 es la medida canónica (relación 1.91:1): es la que piden Facebook,
LinkedIn, Slack, Discord y X, y la que Google usa para las tarjetas grandes.
Se genera a 2x y se baja, porque en pantallas densas la vista previa se muestra
al doble. Debajo de 600x315 varias plataformas degradan a miniatura cuadrada.

EL CUBO SE CAPTURA DEL SITIO DE VERDAD, no se redibuja: es geometría con luz
calibrada, y una reproducción a mano derivaría del original en cuanto cambie
cualquier parámetro. Por eso hace falta el servidor, a diferencia de
make-favicon.py, que sólo necesita la fuente.

La pose es la de llegada (rx 18, ry -26), que muestra tres caras: 肇 al frente,
素顔 a la derecha, 鳥居 arriba. Es la que ve alguien que abre la portada.
"""
import base64, io, json, os, shutil, subprocess, sys, time, urllib.request

try:
    import websocket
except ImportError:
    sys.exit("falta websocket-client: pip install websocket-client")
from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9236
PROFILE = os.path.join(os.environ.get("TEMP", "/tmp"), "kf-og")
SALIDA = os.path.join(RAIZ, "og-image.png")

W, H, SS = 1200, 630, 2          # SS: se compone al doble y se baja
# Copias de los tokens de :root, como en make-favicon.py: la tarjeta se
# renderiza fuera del navegador y no puede leer el CSS.
NAVY = (4, 13, 24)
FONDO = (5, 17, 29)              # --c-surface-cube, el fondo de la sección
GOLD = (200, 168, 90)
TEXTO = (234, 241, 248)
MIST = (138, 171, 204)


_convertidas = {}


def ttf(nombre):
    """woff2 -> ttf en temporal: FreeType (y por lo tanto Pillow) no abre woff2.

    Cacheado, y no por velocidad: ImageFont.truetype deja el archivo ABIERTO, así
    que convertir la misma fuente dos veces intenta sobrescribir un archivo en
    uso y en Windows eso es un error, no una espera.
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


def capturar_cubo():
    """Devuelve el recorte del cubo con su fondo de sección."""
    shutil.rmtree(PROFILE, ignore_errors=True)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
         f"--user-data-dir={PROFILE}", "--hide-scrollbars",
         "--window-size=1440,900", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(60):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as r:
                    pg = [t for t in json.load(r) if t.get("type") == "page"]
                if pg:
                    ws_url = pg[0]["webSocketDebuggerUrl"]; break
            except Exception:
                pass
            time.sleep(0.2)
        if not ws_url:
            sys.exit("no se pudo conectar a Chrome por CDP")

        ws = websocket.create_connection(ws_url, timeout=60, suppress_origin=True)
        n = [0]

        def cmd(m, **p):
            n[0] += 1
            ws.send(json.dumps({"id": n[0], "method": m, "params": p}))
            while True:
                msg = json.loads(ws.recv())
                if msg.get("id") == n[0]:
                    return msg.get("result", {})

        def js(e):
            r = cmd("Runtime.evaluate", expression=e, returnByValue=True, awaitPromise=True)
            if "exceptionDetails" in r:
                raise RuntimeError(f"JS: {r['exceptionDetails'].get('text')}")
            return r.get("result", {}).get("value")

        cmd("Page.enable"); cmd("Runtime.enable")
        cmd("Emulation.setDeviceMetricsOverride", width=1000, height=900,
            deviceScaleFactor=2, mobile=False)
        cmd("Page.navigate", url=BASE + "/index.html")
        time.sleep(6)
        js("document.getElementById('cube').scrollIntoView({behavior:'auto'}); true")
        time.sleep(4)
        if not js("!!document.querySelector('#cube-stage canvas')"):
            sys.exit("el cubo no hidrató: ¿está el sitio servido en :8000?")

        # Pose de llegada, quieta. El loop está pausado mientras no cambie el
        # ángulo (render bajo demanda), así que hay que forzar un cuadro.
        js("""(() => {
          const s = document.getElementById('cube-stage');
          s.scrollIntoView({block:'center'});
          return true;})()""")
        time.sleep(1.5)
        caja = js("""(() => {const c = document.querySelector('#cube-stage canvas');
                     const b = c.getBoundingClientRect();
                     return {x:Math.round(b.left), y:Math.round(b.top),
                             w:Math.round(b.width), h:Math.round(b.height)};})()""")
        shot = cmd("Page.captureScreenshot", format="png", fromSurface=True)
        im = Image.open(io.BytesIO(base64.b64decode(shot["data"]))).convert("RGB")
        # la captura viene a deviceScaleFactor=2; la caja está en px CSS
        e = im.width / 1000
        return im.crop((int(caja["x"] * e), int(caja["y"] * e),
                        int((caja["x"] + caja["w"]) * e),
                        int((caja["y"] + caja["h"]) * e)))
    finally:
        proc.terminate()


def recortar_al_cubo(im, margen=0.06):
    """Recorta al contenido: el escenario tiene mucho aire alrededor."""
    g = im.convert("L")
    umbral = 0.2126 * FONDO[0] + 0.7152 * FONDO[1] + 0.0722 * FONDO[2] + 6
    mascara = g.point(lambda v: 255 if v > umbral else 0)
    caja = mascara.getbbox()
    if not caja:
        return im
    x0, y0, x1, y1 = caja
    mx, my = int((x1 - x0) * margen), int((y1 - y0) * margen)
    return im.crop((max(0, x0 - mx), max(0, y0 - my),
                    min(im.width, x1 + mx), min(im.height, y1 + my)))


def componer(cubo):
    w, h = W * SS, H * SS
    tarjeta = Image.new("RGB", (w, h), FONDO)
    d = ImageDraw.Draw(tarjeta)

    # Viñeta suave: el mismo recurso que usa la página para dar profundidad.
    for i in range(90):
        k = i / 90
        c = tuple(int(FONDO[j] + (NAVY[j] - FONDO[j]) * k) for j in range(3))
        d.rectangle([i, i, w - i, h - i], outline=c)

    # El cubo, a la derecha, ocupando casi todo el alto.
    alto = int(h * 0.80)
    escala = alto / cubo.height
    cubo = cubo.resize((int(cubo.width * escala), alto), Image.LANCZOS)
    cx = int(w * 0.72) - cubo.width // 2
    tarjeta.paste(cubo, (cx, (h - cubo.height) // 2))

    ja = ImageFont.truetype(ttf("zen-kaku-gothic-new-500-subset.woff2"), int(96 * SS))
    ui = ImageFont.truetype(ttf("inter-latin.woff2"), int(23 * SS))
    # La bajada es el título del hero palabra por palabra, así que va en la
    # misma voz: Cormorant. Más grande que en Inter a propósito — una tarjeta
    # se ve a un tercio de su tamaño en un chat, y una serif fina a ese tamaño
    # se deshace antes que una sans.
    display = ImageFont.truetype(ttf("cormorant-garamond-latin.woff2"), int(44 * SS))

    x = int(w * 0.075)
    y = int(h * 0.28)
    d.text((x, y), "言霊", font=ja, fill=GOLD)

    y += int(126 * SS)
    # letterspacing a mano: PIL no lo hace, y la marca lo lleva en toda la web
    esp = int(7.5 * SS)
    cx2 = x
    for ch in "KOTODAMA FINANCE":
        d.text((cx2, y), ch, font=ui, fill=MIST)
        cx2 += d.textlength(ch, font=ui) + esp

    # Apóstrofo tipográfico (U+2019), no el recto: es el que usa el sitio.
    y += int(56 * SS)
    d.text((x, y), "Japan’s financial system,", font=display, fill=TEXTO)
    d.text((x, y + int(52 * SS)), "made legible — from the source.",
           font=display, fill=TEXTO)

    return tarjeta.resize((W, H), Image.LANCZOS)


def main():
    print("capturando el cubo del sitio servido…")
    cubo = recortar_al_cubo(capturar_cubo())
    componer(cubo).save(SALIDA, optimize=True)
    kb = os.path.getsize(SALIDA) / 1024
    print(f"  og-image.png  {W}x{H}  {kb:.0f} KB")
    if kb > 300:
        print("  OJO: >300 KB. Algunas plataformas descartan imágenes pesadas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
