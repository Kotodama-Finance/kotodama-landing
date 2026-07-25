#!/usr/bin/env python3
"""Guarda de PUBLICACIÓN. Responde una sola pregunta: ¿esto puede ir a main?

    python tools/check-ready.py

Se espera en ROJO hasta que termine el pase de redacción: hoy quedan ~70
placeholders `class="todo"`, que en producción serían texto en castellano
dirigido al autor apareciendo en un sitio en inglés.

Eso NO la vuelve inútil, pero sí la vuelve inservible como guarda de commit: una
señal que siempre está en rojo se deja de mirar, y el día que se rompa algo de
verdad pasa inadvertido. Por eso lo que hay que correr en cada commit es
`check-structure.py`, que sí tiene que estar en verde siempre; ésta se corre
antes de publicar.

Salida, con códigos distintos a propósito para poder distinguirlas:
    0  listo para publicar
    2  falta trabajo previsto (redacción y/o la revisión legal del 免責事項)
       — ESPERADO en esta etapa, no es una regresión
    1  hay algo estructural roto — esto sí es una regresión
"""
import sys

import _guardas as G

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LISTO, ROTO, FALTA_REDACCION = 0, 1, 2


def main():
    roto = []

    print("Nav y footer compartidos")
    divergencias = G.chrome_divergente()
    if divergencias:
        for x in divergencias:
            print(f"  FALLA  {x}")
        roto += divergencias
    else:
        print(f"  OK     idénticos en las {len(list(G.htmls()))} páginas")

    print("\nCobertura del subset japonés")
    faltan = G.glifos_faltantes()
    if faltan is None:
        print("  (omitido: falta fontTools — pip install fonttools brotli)")
    elif faltan:
        for nombre, glifos in faltan.items():
            print(f"  FALLA  {nombre}: faltan {''.join(glifos)}")
            roto.append(f"subset {nombre}")
        print("  -> regenerar el subset (ver README, «Tipografías»)")
    else:
        print("  OK     todos los glifos cubiertos")

    print("\nPlaceholders de redacción")
    actual = G.placeholders()
    total = sum(actual.values())
    if total:
        for pagina, n in sorted(actual.items()):
            print(f"  {pagina}: {n} sin escribir")
        print(f"  total: {total}")
    else:
        print("  OK     sin placeholders")

    print("\nRevisión legal del 免責事項")
    sin_revisar = G.disclaimer_sin_revisar()
    if sin_revisar:
        for x in sin_revisar:
            print(f"  FALTA  {x}")
        print("  -> lo revisa un profesional legal japonés (benrishi o abogado);")
        print("     después se saca la marca de borrador del comentario en el HTML")
    else:
        print("  OK     revisado (ya no lleva la marca de borrador)")

    if roto:
        print("\nNO PUBLICAR: hay algo roto (no es la redacción)")
        return ROTO
    if total or sin_revisar:
        pendientes = []
        if total:
            pendientes.append(f"{total} placeholders por redactar")
        if sin_revisar:
            pendientes.append("la revisión legal del 免責事項")
        print(f"\nNO PUBLICAR TODAVÍA: falta {' y '.join(pendientes)}.")
        print("Es lo esperado en esta etapa. La estructura está sana:")
        print("  python tools/check-structure.py")
        return FALTA_REDACCION
    print("\nLISTO PARA PUBLICAR")
    return LISTO


if __name__ == "__main__":
    sys.exit(main())
