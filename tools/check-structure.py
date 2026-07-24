#!/usr/bin/env python3
"""Guarda ESTRUCTURAL. Tiene que estar en verde SIEMPRE, en cada commit.

    python tools/check-structure.py
    python tools/check-structure.py --actualizar-baseline

Comprueba tres cosas que nunca deberían romperse, ni durante el andamiaje:

1. El nav y el footer son idénticos carácter por carácter en las ocho páginas.
   Están duplicados porque no hay build step; la duplicación se banca sólo si
   está vigilada.
2. El subset de Zen Kaku cubre todos los glifos japoneses del sitio. Si falta
   uno, ese carácter cae a una fuente del sistema y desentona en silencio.
3. No aparecieron placeholders NUEVOS respecto del baseline. Los ~70 que hay
   son andamiaje esperado; lo que se vigila es que no se agregue uno sin querer,
   que sería texto en castellano dirigido al autor en un sitio en inglés.

Existe aparte de check-ready.py por una razón de señal: check-ready está en rojo
por diseño hasta el pase de redacción, y una guarda que siempre está en rojo deja
de mirarse. Ésta es la que tiene que estar verde, así que su rojo significa algo.

Salida: 0 todo bien · 1 hay algo roto.
"""
import sys

import _guardas as G

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main():
    actualizar = "--actualizar-baseline" in sys.argv
    problemas = []

    print("Nav y footer compartidos")
    divergencias = G.chrome_divergente()
    if divergencias:
        for x in divergencias:
            print(f"  FALLA  {x}")
        problemas += divergencias
    else:
        print(f"  OK     idénticos en las {len(list(G.htmls()))} páginas")

    print("\nCobertura del subset japonés")
    faltan = G.glifos_faltantes()
    if faltan is None:
        print("  (omitido: falta fontTools — pip install fonttools brotli)")
    elif faltan:
        for nombre, glifos in faltan.items():
            print(f"  FALLA  {nombre}: faltan {''.join(glifos)}")
            problemas.append(f"subset {nombre}")
        print("  -> regenerar el subset (ver README, «Tipografías»)")
    else:
        print("  OK     todos los glifos cubiertos")

    print("\nPlaceholders contra el baseline")
    actual = G.placeholders()
    base = G.leer_baseline()
    total = sum(actual.values())

    if actualizar:
        G.escribir_baseline(actual)
        print(f"  baseline actualizado: {total} placeholders en {len(actual)} páginas")
        return 0 if not problemas else 1

    if not base:
        print("  FALLA  no hay baseline; crearlo con --actualizar-baseline")
        problemas.append("sin baseline")
    else:
        subieron, bajaron = G.comparar_baseline(actual, base)
        for pagina, b, a in subieron:
            print(f"  FALLA  {pagina}: {b} -> {a} placeholders NUEVOS")
            problemas.append(f"placeholders nuevos en {pagina}")
        for pagina, b, a in bajaron:
            print(f"  ok     {pagina}: {b} -> {a} (se redactaron {b - a})")
        if not subieron:
            print(f"  OK     sin placeholders nuevos ({total} en total, los esperados)")
        if bajaron:
            print("  -> hubo redacción: fijar el nuevo piso con --actualizar-baseline")

    ok = not problemas
    print("\nESTRUCTURA OK" if ok else f"\nESTRUCTURA ROTA: {len(problemas)} problema(s)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
