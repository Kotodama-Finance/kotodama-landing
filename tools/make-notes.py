#!/usr/bin/env python3
"""Genera las TRES salidas del sistema de notas, de UNA sola pasada.

    python tools/make-notes.py            # reescribe feed, listado e índice
    python tools/make-notes.py --check    # sólo informa si algo quedó viejo

UN generador y no tres: los tres artefactos derivan de la MISMA lista de
notas, y tres scripts recorriendo el mismo árbol es la divergencia que el
patrón del sitemap ya resolvió. Las salidas:

  1. El FEED de la portada — entre los centinelas «FEED DE NOTAS» de
     index.html. SOLO ese bloque: la portada sigue siendo una página de mano,
     no un artefacto derivado — si el generador la escribiera entera, editarla
     a mano pasaría a ser el mismo modo de falla que main ya tiene mitigado
     con el detector de hotfix. Va DESPUÉS del cubo y ANTES del About.
  2. El LISTADO de /notes/ — entre los centinelas «LISTADO DE NOTAS» de
     notes/index.html, con cara y fecha por ítem.
  3. notes/search-index.json — el índice del buscador (título + texto
     completo), que assets/js/notes.js consume en el navegador.

QUÉ ES UNA NOTA Y QUÉ ENTRA: una página bajo /hajime/<slug>/ que declara
<meta name="kotodama-type" content="note">. Entra a las tres salidas si es
publicable (sin noindex) — el MISMO criterio de paginas_publicas que usan
sitemap.xml y el mapa. El contrato completo de metadatos (título=h1,
cara=meta, fecha=<time>, resumen=lead con clase note-lead) vive en
_guardas.notas_publicables(), que es también lo que la guarda compara: sin
segunda implementación. CON CERO notas publicables los bloques quedan en
solo-centinelas (ninguna caja vacía en la portada) y el índice sin entradas.

TODO EN MEMORIA PRIMERO, después el disco (la lección del mapa): si el
contrato de una nota no se cumple o un centinela falta, ABORTA con nombre y
no se escribe NADA — un feed a medias en la portada es peor que frenar.
"""
import sys
from pathlib import Path

import _guardas as G

RAIZ = Path(__file__).resolve().parent.parent

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def inyectar(html: str, ini: str, fin: str, bloque: str, ruta: str) -> str:
    """Reemplaza el bloque entre centinelas; sin centinelas, aborta con nombre."""
    a, b = html.find(ini), html.find(fin)
    if a < 0 or b < 0:
        raise G.NotaInvalida(
            f"{ruta}: sin los centinelas del bloque de notas "
            f"(«{ini} …» / «{fin}») — reponerlos donde va el bloque generado")
    i = html.rfind("\n", 0, a) + 1
    return html[:i] + bloque + html[b + len(fin):]


def main():
    try:
        notas = G.notas_publicables()
        portada = RAIZ / G.RUTA_PORTADA
        pagina = RAIZ / G.RUTA_NOTAS
        if not pagina.exists():
            raise G.NotaInvalida(f"no existe {G.RUTA_NOTAS} — la página del archivo")
        h_portada = portada.read_text(encoding="utf-8")
        h_pagina = pagina.read_text(encoding="utf-8")
        nueva_portada = inyectar(h_portada, G.FEED_INI, G.FEED_FIN,
                                 G.feed_bloque(notas), G.RUTA_PORTADA)
        nueva_pagina = inyectar(h_pagina, G.LISTA_INI, G.LISTA_FIN,
                                G.listado_bloque(notas), G.RUTA_NOTAS)
        indice = G.indice_notas(notas)
    except G.NotaInvalida as e:
        print(f"  ABORTA sin escribir nada: {e}")
        return 1

    if "--check" in sys.argv:
        problemas = G.notas_desactualizadas()
        if not problemas:
            print(f"  feed, listado e índice al día ({len(notas)} nota(s) publicable(s))")
            return 0
        for x in problemas:
            print(f"  {x}")
        print("  -> correr: python tools/make-notes.py")
        return 1

    cambios = []
    if nueva_portada != h_portada:
        portada.write_text(nueva_portada, encoding="utf-8")
        cambios.append(G.RUTA_PORTADA)
    if nueva_pagina != h_pagina:
        pagina.write_text(nueva_pagina, encoding="utf-8")
        cambios.append(G.RUTA_NOTAS)
    p_indice = RAIZ / G.RUTA_INDICE
    if not p_indice.exists() or p_indice.read_text(encoding="utf-8") != indice:
        p_indice.write_text(indice, encoding="utf-8")
        cambios.append(G.RUTA_INDICE)

    for n in notas:
        print(f"  {n['fecha']}  {n['ruta']}  ({G.CARAS_ROMAJI[n['cara']]}) {n['titulo_plano']}")
    print(f"{len(notas)} nota(s) publicable(s); "
          f"{'reescrito: ' + ', '.join(cambios) if cambios else 'todo ya estaba al día'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
