#!/usr/bin/env python3
"""Verifica el péndulo de rx del cubo. Requiere el sitio servido en :8000.

Mide la física REAL corriendo en un navegador (banco de pruebas en
_dev/pendulum-test.html, que crea el cubo con reduce:false), no una réplica del
cálculo en Python: una réplica puede diverger del código y dar un falso OK.

Comprueba tres cosas que no se pueden juzgar a ojo:

1. En reposo, rx queda acotado alrededor de la vista 3/4. Si corriera libre, el
   cubo daría vueltas completas y el romaji aparecería invertido.
2. Soltando desde una rotación extrema (rx=180), rx vuelve al rango.
3. En todo el recorrido no hay ESCALÓN de velocidad. Es lo mismo que se arregló
   interpolando la velocidad angular, y no se quiere perder al volver al rango.
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
PORT = 9335
PROFILE = os.path.join(os.environ.get("TEMP", "/tmp"), "kf-pend")

PEND_CENTER, PEND_AMP, PEND_PEAK, RETURN_MAX = 18, 20, 0.09, 0.6
fallos = []


def revisar(cond, desc, extra=""):
    print(("  OK   " if cond else "  FALLA") + "  " + desc + (f"  [{extra}]" if extra else ""))
    if not cond:
        fallos.append(desc)


def main():
    shutil.rmtree(PROFILE, ignore_errors=True)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
         f"--user-data-dir={PROFILE}", "--window-size=900,900", "about:blank"],
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

        ws = websocket.create_connection(ws_url, timeout=90, suppress_origin=True)
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
            if "exceptionDetails" in r:
                raise RuntimeError(f"JS falló: {r['exceptionDetails'].get('text')} :: {expr[:80]}")
            return r.get("result", {}).get("value")

        cmd("Page.enable"); cmd("Runtime.enable")
        cmd("Page.navigate", url=BASE + "/_dev/pendulum-test.html")
        time.sleep(4)
        revisar(js("!!window.__cube"), "el banco de pruebas cargó el cubo")

        def muestrear(segundos, cada=0.1):
            datos = []
            fin = time.time() + segundos
            while time.time() < fin:
                datos.append(js("window.__cube.getRotation()"))
                time.sleep(cada)
            return datos

        print("\n1. Reposo: rx acotado alrededor de la vista 3/4")
        m = muestrear(25)
        rxs = [d["rx"] for d in m]
        lim = PEND_CENTER + PEND_AMP + 6      # margen: velRx persigue con lerp
        dentro = all(PEND_CENTER - PEND_AMP - 6 <= r <= lim for r in rxs)
        revisar(dentro, "rx nunca se escapa del rango",
                f"min {min(rxs):.1f} max {max(rxs):.1f}")
        revisar(max(rxs) - min(rxs) > 1.0, "rx se mueve de verdad (no quedó clavado)",
                f"excursión {max(rxs)-min(rxs):.1f}°")
        rys = [d["ry"] for d in m]
        revisar(abs(rys[-1] - rys[0]) > 5, "ry sigue girando libre",
                f"{abs(rys[-1]-rys[0]):.1f}°")

        # No se puede exigir el rango completo por reloj: en headless el loop
        # corre a ~7 ticks/s y no a 30, así que una ventana de minutos apenas
        # barre media oscilación y el mínimo teórico nunca llega a verse.
        # Se deduce cuántos ticks pasaron (ry avanza AUTO_RY por tick) y se
        # compara contra la envolvente del tramo de fase REALMENTE barrido.
        AUTO_RY = 0.28
        import math
        ticks = abs(rys[-1] - rys[0]) / AUTO_RY
        fase = ticks * (PEND_PEAK / PEND_AMP)
        muestras = [PEND_CENTER + PEND_AMP * math.sin(fase * i / 400) for i in range(401)]
        esp_min, esp_max = min(muestras), max(muestras)
        print(f"     barrido {fase/(2*math.pi):.2f} períodos ({ticks:.0f} ticks)")
        print(f"     esperado [{esp_min:.1f}, {esp_max:.1f}]  medido [{min(rxs):.1f}, {max(rxs):.1f}]")
        # Tolerancia amplia por diseño: velRx persigue su objetivo con un lerp,
        # así que rx va con retardo y sobrepasa un poco cada extremo. Eso es
        # deseable (un péndulo real no frena en seco); lo que se verifica es que
        # NO se vaya lejos ni se quede corto.
        revisar(abs(min(rxs) - esp_min) < 9 and abs(max(rxs) - esp_max) < 9,
                "rx sigue la envolvente del péndulo en el tramo barrido",
                f"desvío {abs(min(rxs)-esp_min):.1f} / {abs(max(rxs)-esp_max):.1f}")

        print("\n1b. El extremo inferior no se pasa de largo")
        js(f"window.__cube.setRotation({PEND_CENTER - PEND_AMP}, 0); true")
        time.sleep(0.3)
        bajo = [d["rx"] for d in muestrear(12)]
        revisar(min(bajo) > PEND_CENTER - PEND_AMP - 6,
                "no se hunde por debajo del límite inferior", f"mínimo {min(bajo):.1f}°")

        print("\n2. Vuelta desde una rotación extrema (rx=180)")
        js("window.__cube.setRotation(180, 0); true")
        time.sleep(0.3)
        # Por ticks y no por reloj: en headless el loop corre a un ritmo
        # variable (~7-15 ticks/s), y una ventana fija daba falsos negativos.
        m2 = []
        limite = time.time() + 90
        while time.time() < limite:
            d = js("window.__cube.getRotation()")
            m2.append(d)
            if d["rx"] <= PEND_CENTER + PEND_AMP:
                break
            time.sleep(0.1)
        rx2 = [d["rx"] for d in m2]
        vel2 = [d["velRx"] for d in m2]
        revisar(rx2[-1] < rx2[0], "rx vuelve hacia el rango", f"{rx2[0]:.1f}° -> {rx2[-1]:.1f}°")
        revisar(rx2[-1] <= lim, "llega a entrar en el rango", f"terminó en {rx2[-1]:.1f}°")

        print("\n3. Sin escalón de velocidad en todo el recorrido")
        saltos = [abs(vel2[i] - vel2[i - 1]) for i in range(1, len(vel2))]
        peor = max(saltos)
        # el lerp es 0.095 por tick: entre dos muestras (~3 ticks) el cambio
        # posible es una fracción del pico. Un escalón sería del orden del pico.
        revisar(peor < RETURN_MAX * 0.25, "ningún salto brusco de velocidad",
                f"peor salto {peor:.4f} (techo {RETURN_MAX})")
        revisar(all(abs(v) <= RETURN_MAX * 1.05 for v in vel2), "la velocidad nunca supera el techo",
                f"máx |vel| {max(abs(v) for v in vel2):.4f}")
        # al reentrar al rango la velocidad tiene que valer el pico del péndulo,
        # no el techo de retorno: ahí se ve si el empalme es continuo
        cerca = [abs(v) for d, v in zip(m2, vel2) if abs(d["rx"] - PEND_CENTER) < PEND_AMP + 2]
        if cerca:
            revisar(max(cerca) <= PEND_PEAK * 1.6, "al entrar al rango la velocidad ya es la del péndulo",
                    f"máx |vel| dentro {max(cerca):.4f} (pico {PEND_PEAK})")

        ws.close()
    finally:
        proc.terminate()

    print("\n" + ("TODO OK" if not fallos else f"{len(fallos)} FALLA(S): " + "; ".join(fallos)))
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
