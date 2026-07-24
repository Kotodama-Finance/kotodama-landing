#!/usr/bin/env python3
"""Guarda de comportamiento del cubo. Requiere el sitio servido en :8000.

    python tools/check-modes.py [http://localhost:8000]

Existe porque estas dos cosas ya se rompieron dos veces, las dos por un cambio
de layout que pisó una regla de CSS, y las dos se detectaron mirando la página:

1. En modo cubo la grilla tiene que estar RECORTADA (visually-hidden con clip),
   no en flujo. Es la capa semántica: no puede ir a display:none, pero tampoco
   puede verse debajo del cubo.
2. En modo grilla el escenario tiene que computar display:none.

Y verifica el ciclo de selección completo, que asume que "ninguna cara activa"
es un estado válido:
   carga (nada) -> clic (estado + botón) -> arrastre (nada) -> otro clic

check-ready.py no puede hacer esto: son estilos computados y eventos, no texto
en un archivo. Hace falta un navegador de verdad.
"""
import json, os, shutil, subprocess, sys, time, urllib.request

try:
    import websocket
except ImportError:
    sys.exit("falta websocket-client: pip install websocket-client")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9333
PROFILE = os.path.join(os.environ.get("TEMP", "/tmp"), "kf-check-modes")

fallos = []


def revisar(cond, descripcion, detalle=""):
    print(("  OK   " if cond else "  FALLA") + "  " + descripcion + (f"  [{detalle}]" if detalle and not cond else ""))
    if not cond:
        fallos.append(descripcion)


def main():
    shutil.rmtree(PROFILE, ignore_errors=True)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
         f"--user-data-dir={PROFILE}", "--hide-scrollbars",
         "--window-size=1440,1000", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(60):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as r:
                    tabs = json.load(r)
                pg = [t for t in tabs if t.get("type") == "page"]
                if pg:
                    ws_url = pg[0]["webSocketDebuggerUrl"]
                    break
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

        def js(expr):
            r = cmd("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
            # Una excepción en el JS tiene que reventar acá. Si se traga en
            # silencio, el script reporta "falla" cuando el bug está en el test
            # y no en la página: ya pasó una vez, con un error de comillas.
            if "exceptionDetails" in r:
                d = r["exceptionDetails"]
                raise RuntimeError(f"JS falló: {d.get('text')} :: {expr[:90]}")
            return r.get("result", {}).get("value")

        cmd("Page.enable"); cmd("Runtime.enable")
        cmd("Page.navigate", url=BASE + "/index.html")
        time.sleep(5)
        # el cubo se hidrata al acercarse su sección
        js("document.getElementById('cube').scrollIntoView({behavior:'auto'}); true")
        time.sleep(3)

        estado = """(() => {
          const g = document.querySelector('.face-grid');
          const st = document.getElementById('cube-stage');
          const cs = getComputedStyle(g);
          return {
            hidratado: !!document.querySelector('#cube-stage canvas'),
            gridRecortada: cs.clipPath !== 'none' || g.getBoundingClientRect().width <= 2,
            gridEnDom: document.contains(g),
            gridDisplay: cs.display,
            stageDisplay: getComputedStyle(st).display,
            activas: document.querySelectorAll('.face-card.is-active').length,
            statusVisible: !document.getElementById('cube-status').hidden,
            botonVisible: !document.getElementById('cube-open').hidden,
            botonTexto: document.getElementById('cube-open').textContent.trim(),
            botonHref: document.getElementById('cube-open').getAttribute('href'),
          };})()"""

        print("Modo cubo, recién cargado")
        e = js(estado)
        revisar(e["hidratado"], "el cubo hidrató")
        revisar(e["gridRecortada"], "la grilla está recortada (no en flujo)", f"clip/ancho: {e['gridDisplay']}")
        revisar(e["gridEnDom"], "la grilla sigue en el DOM (capa semántica)")
        revisar(e["gridDisplay"] != "none", "la grilla NO usa display:none")
        revisar(e["stageDisplay"] != "none", "el escenario está visible")
        revisar(e["activas"] == 0, "ninguna cara resaltada", f"{e['activas']} activas")
        revisar(not e["statusVisible"], "sin línea de estado")
        revisar(not e["botonVisible"], "sin botón")

        print("\nClic en una cara (渡世 Tosei)")
        js("document.querySelectorAll('.face-card')[2].click(); true")
        time.sleep(0.4)
        e = js(estado)
        revisar(e["activas"] == 1, "exactamente una cara resaltada", f"{e['activas']}")
        revisar(e["statusVisible"], "aparece la línea de estado")
        revisar(e["botonVisible"], "aparece el botón")
        revisar("Tosei" in e["botonTexto"], "el botón nombra la cara", e["botonTexto"])
        revisar(e["botonHref"] == "/tosei/", "el botón apunta a su subpágina", str(e["botonHref"]))

        print("\nArrastrar el cubo")
        r = js("""(() => {const c = document.querySelector('#cube-stage canvas');
                   const b = c.getBoundingClientRect();
                   return {x: Math.round(b.left + b.width/2), y: Math.round(b.top + b.height/2)};})()""")
        for tipo, dx in (("mousePressed", 0), ("mouseMoved", 40), ("mouseReleased", 40)):
            cmd("Input.dispatchMouseEvent", type=tipo, x=r["x"] + dx, y=r["y"],
                button="left", clickCount=1, buttons=1)
            time.sleep(0.15)
        time.sleep(0.4)
        e = js(estado)
        revisar(e["activas"] == 0, "se deselecciona al arrastrar", f"{e['activas']} activas")
        revisar(not e["botonVisible"], "el botón desaparece al arrastrar")
        revisar(not e["statusVisible"], "el estado desaparece al arrastrar")

        print("\nClic en otra cara (絆 Kizuna)")
        js("document.querySelectorAll('.face-card')[5].click(); true")
        time.sleep(0.4)
        e = js(estado)
        revisar("Kizuna" in e["botonTexto"], "el botón se actualiza a la nueva cara", e["botonTexto"])
        revisar(e["botonHref"] == "/kizuna/", "y su enlace también", str(e["botonHref"]))

        print("\nModo grilla")
        js("document.querySelector('.cube__toggle button[data-view=\"grid\"]').click(); true")
        time.sleep(0.5)
        e = js(estado)
        revisar(e["stageDisplay"] == "none", "el escenario computa display:none", e["stageDisplay"])
        revisar(not e["gridRecortada"], "la grilla se ve completa")

        print("\nVuelta a modo cubo")
        js("document.querySelector('.cube__toggle button[data-view=\"3d\"]').click(); true")
        time.sleep(0.5)
        e = js(estado)
        revisar(e["gridRecortada"], "la grilla vuelve a recortarse")
        revisar(e["stageDisplay"] != "none", "el escenario vuelve")

        ws.close()
    finally:
        proc.terminate()

    print("\n" + ("TODO OK" if not fallos else f"{len(fallos)} FALLA(S): " + "; ".join(fallos)))
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
