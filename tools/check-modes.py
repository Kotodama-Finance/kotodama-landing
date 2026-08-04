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

3. Que NO haya ninguna regla de view-transition viva. El maelstrom está
   reservado en assets/css/maelstrom.css y no lo carga nadie; se repone sin
   querer con un solo `<link>`. Ver `sin_view_transitions()`.

check-ready.py no puede hacer esto: son estilos computados y eventos, no texto
en un archivo. Hace falta un navegador de verdad.
"""
import base64, io, json, os, shutil, subprocess, sys, time, urllib.request

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


# --- El maelstrom no vuelve solo, pero se repone con un solo <link> ----------
# Le pregunta al NAVEGADOR qué reglas están en efecto, no al texto de un
# archivo. Ésa es la diferencia que importa: hay tres formas de reponer la
# transición —un <link> a maelstrom.css, las reglas pegadas de vuelta en
# styles.css, o un <style> inline— y un grep sobre un archivo sólo ataja la
# que se le ocurrió a quien escribió el grep. document.styleSheets las ve a
# las tres a la vez porque ve el resultado, no la causa. Es la lección que
# dejó el bug de la variante táctil del propio maelstrom: una regla que sólo
# se LEE no está verificada; hay que medir la propiedad efectiva.
#
# Recorre cssRules recursivamente: una regla dentro de @media, @supports o
# @layer está igual de viva y no aparece en el nivel de arriba.
#
# HAY QUE SEGUIR `r.styleSheet`, NO SÓLO `r.cssRules`, y ésta es la parte que
# la primera versión de esta guarda tenía mal. Una CSSImportRule NO expone
# cssRules —expone styleSheet—, así que recorrer sólo cssRules deja pasar
# `@import url("maelstrom.css")`... que es exactamente la vía de reactivación
# escrita en el encabezado de maelstrom.css, o sea la MÁS probable de las tres.
# La guarda estaba ciega justo en la puerta principal. Medido: con el @import
# puesto daba 0 hallazgos, y con un <link> equivalente daba 7.
# Por lo mismo va `document.adoptedStyleSheets`: una hoja construida por JS no
# aparece en document.styleSheets y también estaba fuera del alcance.
#
# Verificado en rojo antes de confiar en su verde, contra seis casos rotos:
# @view-transition inline, ::view-transition-old(root) inline, un <link> al
# maelstrom.css real, la regla anidada en un @media, un @import, y una hoja
# adoptada.
DETECTOR_VT = r"""(() => {
  const hallazgos = [], ilegibles = [], vistas = new Set();
  const mirar = (reglas, origen) => {
    for (const r of reglas) {
      const txt = (r.cssText || '').replace(/\s+/g, ' ').slice(0, 110);
      if (r.constructor.name === 'CSSViewTransitionRule' ||
          /^@view-transition/i.test(txt) ||
          /view-transition/i.test(r.selectorText || '')) {
        hallazgos.push(origen + ' :: ' + txt);
      }
      if (r.cssRules) mirar(r.cssRules, origen);       // @media, @supports, @layer
      if (r.styleSheet) hoja(r.styleSheet, origen + ' -> @import');
    }
  };
  const hoja = (s, origen) => {
    if (!s || vistas.has(s)) return;                   // un @import circular colgaría
    vistas.add(s);
    const n = s.href ? s.href.replace(/^https?:\/\/[^/]+/, '') : origen;
    // Una hoja que no se puede leer es una hoja que no se puede descartar: va
    // como fallo con su nombre, no como omisión silenciosa. Un verde por no
    // haber podido mirar es el peor de los verdes.
    try { mirar(s.cssRules, n); }
    catch (e) { ilegibles.push(n + ' (' + e.name + ')'); }
  };
  for (const s of document.styleSheets) hoja(s, '<style> inline');
  for (const s of (document.adoptedStyleSheets || [])) hoja(s, 'adoptedStyleSheets');
  return { hallazgos, ilegibles, hojas: vistas.size,
           pedidos: performance.getEntriesByType('resource')
                      .map(e => e.name).filter(n => /maelstrom/i.test(n)) };
})()"""


def sin_view_transitions(js, etiqueta):
    r = js(DETECTOR_VT)
    # Que haya mirado ALGO. Si la página no cargara ninguna hoja, todo lo de
    # abajo daría verde por no tener nada que revisar — el verde vacío que ya
    # dio una vez `máx |vel| dentro 0.0000`.
    revisar(r["hojas"] >= 1, f"{etiqueta}: hay hojas de estilo que mirar",
            f"{r['hojas']} hojas")
    revisar(not r["hallazgos"], f"{etiqueta}: ninguna regla de view-transition viva",
            "; ".join(r["hallazgos"])[:220])
    revisar(not r["pedidos"], f"{etiqueta}: nadie pide maelstrom.css",
            "; ".join(r["pedidos"])[:220])
    revisar(not r["ilegibles"], f"{etiqueta}: todas las hojas se pudieron leer",
            "; ".join(r["ilegibles"])[:220])


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

        print("Transición entre páginas: reservada, no activa")
        sin_view_transitions(js, "portada")

        # El estado y el botón viven en un FOLIO que se despliega al seleccionar
        # (grid-template-rows 0fr->1fr) y se repliega al arrastrar. Antes se
        # mostraban/ocultaban con el atributo `hidden`; ahora lo observable es:
        #   desplegado = clase is-open + sin `inert` + altura real
        #   plegado    = sin is-open + `inert` + altura ~0
        # No se mide por `hidden` porque display:none no anima, que es justo lo
        # que este folio evita. Ver .cube__folio en el CSS y la entrada de
        # CLAUDE.md que revierte «espacio reservado».
        estado = """(() => {
          const g = document.querySelector('.face-grid');
          const st = document.getElementById('cube-stage');
          const f = document.getElementById('cube-folio');
          const cs = getComputedStyle(g);
          const fcs = getComputedStyle(f);
          return {
            hidratado: !!document.querySelector('#cube-stage canvas'),
            gridRecortada: cs.clipPath !== 'none' || g.getBoundingClientRect().width <= 2,
            gridEnDom: document.contains(g),
            gridDisplay: cs.display,
            stageDisplay: getComputedStyle(st).display,
            stageTop: Math.round(st.getBoundingClientRect().top + window.scrollY),
            activas: document.querySelectorAll('.face-card.is-active').length,
            folioDesplegado: f.classList.contains('is-open') && !f.hasAttribute('inert'),
            folioAlto: Math.round(f.getBoundingClientRect().height),
            folioTransicion: fcs.transitionProperty,
            folioDuracion: fcs.transitionDuration,
            botonTexto: document.getElementById('cube-open').textContent.trim(),
            botonHref: document.getElementById('cube-open').getAttribute('href'),
          };})()"""

        # tras abrir/cerrar el folio hay que esperar la transición (0.42s) para
        # que la altura llegue a su valor final; is-open/inert son instantáneos.
        ESPERA_FOLIO = 0.7

        print("Modo cubo, recién cargado")
        e = js(estado)
        alto_plegado = e["folioAlto"]
        top_stage = e["stageTop"]
        revisar(e["hidratado"], "el cubo hidrató")
        revisar(e["gridRecortada"], "la grilla está recortada (no en flujo)", f"clip/ancho: {e['gridDisplay']}")
        revisar(e["gridEnDom"], "la grilla sigue en el DOM (capa semántica)")
        revisar(e["gridDisplay"] != "none", "la grilla NO usa display:none")
        revisar(e["stageDisplay"] != "none", "el escenario está visible")
        revisar(e["activas"] == 0, "ninguna cara resaltada", f"{e['activas']} activas")
        revisar(not e["folioDesplegado"], "el folio arranca plegado")
        revisar(e["folioAlto"] <= 6, "el folio plegado no ocupa alto", f"{e['folioAlto']}px")
        # El despliegue tiene que ser ANIMADO: instantáneo se lee como página
        # rota. Se verifica que la transición esté declarada sobre la propiedad
        # correcta y con duración real; que interpole visualmente se comprobó a
        # ojo (headless corre el reloj de animación a un ritmo poco fiable).
        revisar("grid-template-rows" in e["folioTransicion"] and e["folioDuracion"] not in ("0s", "0.01ms"),
                "el despliegue del folio está animado",
                f"{e['folioTransicion']} / {e['folioDuracion']}")

        print("\nClic en una cara (渡世 Tosei)")
        js("document.querySelectorAll('.face-card')[2].click(); true")
        time.sleep(ESPERA_FOLIO)
        e = js(estado)
        revisar(e["activas"] == 1, "exactamente una cara resaltada", f"{e['activas']}")
        revisar(e["folioDesplegado"], "el folio se despliega")
        revisar(e["folioAlto"] > alto_plegado + 20, "el folio ganó alto real", f"{e['folioAlto']}px")
        revisar("Tosei" in e["botonTexto"], "el botón nombra la cara", e["botonTexto"])
        revisar(e["botonHref"] == "/tosei/", "el botón apunta a su subpágina", str(e["botonHref"]))
        # Lo que hace seguro desplegar en vez de reservar: el folio está DEBAJO
        # del cubo, así que abrirlo no mueve el escenario ni la cara clickeada.
        revisar(e["stageTop"] == top_stage, "el cubo NO se mueve al desplegarse el folio",
                f"saltó {e['stageTop'] - top_stage}px")

        print("\nArrastrar el cubo")
        r = js("""(() => {const c = document.querySelector('#cube-stage canvas');
                   const b = c.getBoundingClientRect();
                   return {x: Math.round(b.left + b.width/2), y: Math.round(b.top + b.height/2)};})()""")
        for tipo, dx in (("mousePressed", 0), ("mouseMoved", 40), ("mouseReleased", 40)):
            cmd("Input.dispatchMouseEvent", type=tipo, x=r["x"] + dx, y=r["y"],
                button="left", clickCount=1, buttons=1)
            time.sleep(0.15)
        time.sleep(ESPERA_FOLIO)
        e = js(estado)
        revisar(e["activas"] == 0, "se deselecciona al arrastrar", f"{e['activas']} activas")
        revisar(not e["folioDesplegado"], "el folio se repliega al arrastrar")
        revisar(e["folioAlto"] <= 6, "y vuelve a no ocupar alto", f"{e['folioAlto']}px")

        print("\nClic en otra cara (絆 Kizuna)")
        js("document.querySelectorAll('.face-card')[5].click(); true")
        time.sleep(ESPERA_FOLIO)
        e = js(estado)
        revisar(e["folioDesplegado"], "el folio se vuelve a desplegar")
        revisar("Kizuna" in e["botonTexto"], "el botón se actualiza a la nueva cara", e["botonTexto"])
        revisar(e["botonHref"] == "/kizuna/", "y su enlace también", str(e["botonHref"]))

        # --- Repintado con el cubo detenido ---------------------------------
        # El cubo usa render bajo demanda: si nada cambia el ángulo, no
        # redibuja. Pero renderer.setSize() limpia el buffer, así que un resize
        # con el cubo detenido (parked) dejaría el canvas vacío si resize() no
        # forzara un cuadro. Se verifica sobre la captura COMPOSITADA: leer un
        # canvas WebGL desde JS fuera de su frame devuelve vacío y daría un
        # falso negativo.
        def cubo_visible(etiqueta):
            from PIL import Image
            r = js("""(() => {const c = document.querySelector('#cube-stage canvas');
                      const b = c.getBoundingClientRect();
                      return {x:Math.round(b.left),y:Math.round(b.top),
                              w:Math.round(b.width),h:Math.round(b.height)};})()""")
            shot = cmd("Page.captureScreenshot", format="png", fromSurface=True)
            im = Image.open(io.BytesIO(base64.b64decode(shot["data"]))).convert("RGB")
            caja = im.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
            px = list(caja.getdata())
            fondo = 0.2126 * 5 + 0.7152 * 17 + 0.0722 * 29   # --c-surface-cube
            claros = sum(1 for R, G, B in px if 0.2126 * R + 0.7152 * G + 0.0722 * B > fondo + 8)
            pct = 100.0 * claros / max(len(px), 1)
            revisar(pct > 3, etiqueta, f"sólo {pct:.1f}% de píxeles de cubo")

        print("\nRepintado con el cubo detenido (parked)")
        js("document.querySelectorAll('.face-card')[0].click(); true")
        time.sleep(1.6)      # que termine el snap y quede parked
        cmd("Emulation.setDeviceMetricsOverride", width=1100, height=900,
            deviceScaleFactor=1, mobile=False)
        time.sleep(1.3)
        cubo_visible("se repinta después de un resize")
        cmd("Emulation.setDeviceMetricsOverride", width=1440, height=1000,
            deviceScaleFactor=1, mobile=False)
        time.sleep(1.3)

        print("\nModo grilla")
        # El toggle no puede moverse al usarlo: si estuviera DEBAJO del
        # escenario, al pasar a grilla el escenario desaparece, la grilla mide
        # menos y el control saltaría hacia arriba justo cuando lo estás tocando.
        # Se mide pegado al cambio de modo: cualquier resize en el medio
        # reflowea el encabezado y la comparación deja de ser válida.
        pos_toggle = js("Math.round(document.querySelector('.cube__toggle')"
                        ".getBoundingClientRect().top + window.scrollY)")
        js("document.querySelector('.cube__toggle button[data-view=\"grid\"]').click(); true")
        time.sleep(0.5)
        e = js(estado)
        revisar(e["stageDisplay"] == "none", "el escenario computa display:none", e["stageDisplay"])
        revisar(not e["gridRecortada"], "la grilla se ve completa")
        pos2 = js("Math.round(document.querySelector('.cube__toggle').getBoundingClientRect().top + window.scrollY)")
        revisar(abs(pos2 - pos_toggle) <= 2, "el toggle NO se mueve al cambiar de modo",
                f"saltó {pos2 - pos_toggle}px")

        print("\nVuelta a modo cubo")
        js("document.querySelector('.cube__toggle button[data-view=\"3d\"]').click(); true")
        time.sleep(0.5)
        e = js(estado)
        revisar(e["gridRecortada"], "la grilla vuelve a recortarse")
        revisar(e["stageDisplay"] != "none", "el escenario vuelve")
        time.sleep(0.8)
        cubo_visible("y se repinta al volver de modo grilla")

        # La subpágina se mira aparte y no por prolijidad: @view-transition es
        # una transición ENTRE DOCUMENTOS y tiene que estar declarada en los
        # dos lados, así que mirar sólo la portada dejaría medio caso sin ver.
        # Y es el lado ciego: las diez subpáginas no cargan ningún JavaScript,
        # o sea que ninguna otra comprobación de runtime las toca nunca.
        print("\nSubpágina de una cara")
        cmd("Page.navigate", url=BASE + "/hajime/")
        time.sleep(2.5)
        sin_view_transitions(js, "/hajime/")
        # Y que entre seca: si algo la anima al llegar, la transición volvió por
        # otra puerta —una animación sobre .face-page en vez de sobre el pseudo.
        e = js("""(() => {const p = document.querySelector('.face-page');
                   const cs = getComputedStyle(p);
                   return {anim: cs.animationName, op: cs.opacity};})()""")
        revisar(e["anim"] == "none" and e["op"] == "1",
                "/hajime/ entra seca (sin animación de llegada)",
                f"{e['anim']} / opacity {e['op']}")

        ws.close()
    finally:
        proc.terminate()

    print("\n" + ("TODO OK" if not fallos else f"{len(fallos)} FALLA(S): " + "; ".join(fallos)))
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
