#!/usr/bin/env python3
"""Barrido de verificacion del encuadre anisotropico.

La garantia que se verifica: NINGUNA rotacion alcanzable recorta. Alcanzable =
cualquier rx (el arrastre no esta acotado) x cualquier ry. El barrido cubre:
  - el arco del pendulo con sobrepaso: rx -8..44
  - el peor caso teorico: rx 45 (arista arriba, altura sqrt(2)*S)
  - los snap de torii/kizuna: rx +-90
  - poses de arrastre manual: rx 60, 135, 180
por ry cada 15 grados. En cada pose: setRotation + render + captura compositada
(leer el canvas WebGL fuera de su frame da vacio) y distancia minima del pixel
dibujado a cada borde del canvas.

Se espera: margen minimo > 0 en TODAS, y el minimo global en rx~45.
El loop se pausa con setEnabled(false) para que el pendulo no mueva la pose
entre el setRotation y la captura.
"""
import base64, io, json, os, shutil, subprocess, sys, time, urllib.request
import websocket
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9403
PROFILE = os.path.join(os.environ.get("TEMP", "/tmp"), "kf-barrido")

RXS = [-8, 0, 10, 18, 26, 35, 40, 44, 45, 50, 60, 90, -90, 135, 180]
RYS = list(range(0, 360, 15))

shutil.rmtree(PROFILE, ignore_errors=True)
proc = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
                         f"--user-data-dir={PROFILE}", "--hide-scrollbars",
                         "--window-size=760,680", "about:blank"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


try:
    ws = None
    for _ in range(80):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
            pg = [t for t in tabs if t.get("type") == "page"]
            if pg:
                ws = websocket.create_connection(pg[0]["webSocketDebuggerUrl"],
                                                 timeout=90, suppress_origin=True); break
        except Exception:
            pass
        time.sleep(0.2)
    n = [0]

    def cmd(m, **p):
        n[0] += 1
        ws.send(json.dumps({"id": n[0], "method": m, "params": p}))
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == n[0]:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def js(e):
        r = cmd("Runtime.evaluate", expression=e, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"].get("text") or r["exceptionDetails"])
        return r.get("result", {}).get("value")

    cmd("Page.enable"); cmd("Runtime.enable"); cmd("Network.enable")
    cmd("Network.setCacheDisabled", cacheDisabled=True)
    # El banco a 720x620, la misma caja que la portada en escritorio.
    cmd("Emulation.setDeviceMetricsOverride", width=720, height=620,
        deviceScaleFactor=1, mobile=False)
    cmd("Page.navigate", url="http://localhost:8000/_dev/pendulum-test.html")
    time.sleep(5)
    if not js("!!window.__cube"):
        sys.exit("el banco no cargo")
    js("window.__cube.setEnabled(false); true")   # pausa el loop: la pose no se mueve
    time.sleep(0.5)
    print("distancia de camara:", js("(() => window.__cube ? 'banco ok' : '')()") and "", end="")
    # la distancia real de la camara, para reportarla
    # (no esta expuesta; se deduce del margen medido)

    r = js("""(() => {const c=document.querySelector('canvas');
              const b=c.getBoundingClientRect();
              return {x:Math.round(b.left),y:Math.round(b.top),
                      w:Math.round(b.width),h:Math.round(b.height)};})()""")
    print(f"canvas {r['w']}x{r['h']}")
    fondo_ref = None

    peor = None
    recortes = []
    t0 = time.time()
    for rx in RXS:
        fila_min = 1e9
        for ry in RYS:
            js(f"window.__cube.setRotation({rx}, {ry}); window.__cube.render(); true")
            time.sleep(0.06)
            d = cmd("Page.captureScreenshot", format="png", fromSurface=True)["data"]
            im = Image.open(io.BytesIO(base64.b64decode(d))).convert("RGB")
            caja = im.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
            W, H = caja.size
            px = caja.load()
            if fondo_ref is None:
                fondo_ref = lum(px[2, 2])   # esquina: siempre fondo
            vivo = lambda x, y: abs(lum(px[x, y]) - fondo_ref) > 6
            # distancia minima del dibujo a cada borde
            top = next((y for y in range(H) if any(vivo(x, y) for x in range(0, W, 2))), H)
            bot = next((y for y in range(H - 1, -1, -1) if any(vivo(x, y) for x in range(0, W, 2))), -1)
            izq = next((x for x in range(W) if any(vivo(x, y) for y in range(0, H, 2))), W)
            der = next((x for x in range(W - 1, -1, -1) if any(vivo(x, y) for y in range(0, H, 2))), -1)
            m = min(top, H - 1 - bot, izq, W - 1 - der)
            fila_min = min(fila_min, m)
            if m <= 0:
                recortes.append((rx, ry, m))
            if peor is None or m < peor[2]:
                peor = (rx, ry, m)
        print(f"   rx {rx:>4}   margen minimo en la fila: {fila_min:>3}px")
    print(f"\n   {len(RXS)*len(RYS)} poses en {time.time()-t0:.0f}s")
    print(f"   PEOR POSE: rx {peor[0]}, ry {peor[1]}  ->  margen {peor[2]}px")
    print(f"   recortes (margen <= 0): {len(recortes)}")
    if recortes:
        for rc in recortes[:10]:
            print("     RECORTA:", rc)
        sys.exit(1)
    print("\n   SIN RECORTE EN NINGUNA POSE ALCANZABLE")
finally:
    proc.terminate()
