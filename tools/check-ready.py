#!/usr/bin/env python3
"""Guarda de PUBLICACIÓN. Responde una sola pregunta: ¿esto puede ir a main?

    python tools/check-ready.py

HOY SALE 2, Y ES LO ESPERADO — el significado del código 2 ya cambió CUATRO
veces, así que la historia completa antes de interpretar una corrida:

1. Nació esperada en rojo: ~70 placeholders de andamiaje. `2` era lo normal.
2. La redacción terminó (2026-08-04, `v1-content-complete`): baseline en cero,
   y `2` pasó a significar regresión.
3. La revisión del mismo día agregó A PROPÓSITO tres subpáginas nuevas
   (/hajime/taichi|yorozu|yugen/) y la línea de la tarjeta de LibraryThing,
   todas con placeholders del autor pendientes. `2` volvió a ser lo esperado.
4. La redacción terminó POR SEGUNDA VEZ (2026-08-05): la línea de
   LibraryThing y las tres subpáginas, todo texto del autor. Baseline en
   cero de nuevo, y `2` volvió a ser regresión. Así se publicó el sitio
   (2026-08-06, `v1-published`).
5. El andamiaje de la capa 1 de seguros (2026-08-07, decisión del autor):
   /hajime/yorozu/japan/seguros/ entra con 25 placeholders A PROPÓSITO — la
   primera página sectorial, molde de /method/, el texto lo escribe el
   autor. `2` vuelve a ser lo esperado hasta ese pase; el sitio PUBLICADO
   no cambia porque el andamiaje no se deploya.
6. El sistema de notas + la tarjeta de sector (2026-08-07, más tarde el
   mismo día): /notes/, la nota-fixture /hajime/nota-ejemplo/ y la tarjeta
   de seguros en /hajime/yorozu/ suman 13 placeholders deliberados
   (baseline 38). `2` sigue siendo lo esperado; nada de esto se deploya.

O sea: hoy `2` es el estado normal (los 38 del baseline, en cuatro páginas),
`0` significará que todo eso quedó redactado, y `1` sigue siendo estructura
rota. La lección de las eras 2→3→5 queda escrita: un `2` alterna entre
esperado y regresión según si el autor reintrodujo andamiaje a propósito —
antes de tratarlo como regresión, preguntarse si hubo una decisión así, y el
baseline de check-structure dice cuál era el techo acordado.

Sigue SIN entrar en el flujo de cada commit, y el motivo no caducó con el rojo:
esta guarda contesta «¿puede ir a `main`?», que es una pregunta que sólo se hace
al publicar. La de cada commit es `check-structure.py`. El razonamiento original
—una señal que siempre está en rojo se deja de mirar— es lo que hizo que fueran
dos guardas y no una, y por eso el reparto se queda como está.

Salida, con códigos distintos a propósito para poder distinguirlas:
    0  listo para publicar  — se recupera cuando la capa 1 quede redactada
    2  hay placeholders sin redactar — hoy: los 25 del andamiaje de seguros,
       esperado (más que eso, regresión: comparar contra el baseline)
    1  hay algo estructural roto — regresión

El 2 cubre UNA sola cosa: los placeholders. Hubo una segunda —la revisión legal
del 免責事項, detectada por una marca de borrador en el HTML— y se retiró cuando
el autor decidió publicar el descargo sin revisión de un profesional legal
japonés. El motivo y el marco legal que lo sostiene están en CLAUDE.md.
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

    print("\nNoindex olvidado en páginas ya redactadas")
    olvidados = G.noindex_olvidado()
    if olvidados:
        for x in olvidados:
            print(f"  FALLA  {x}")
        roto += olvidados
    else:
        print("  OK     ningún noindex sobrevive a su redacción")

    print("\nPlaceholders de redacción")
    actual = G.placeholders()
    total = sum(actual.values())
    if total:
        for pagina, n in sorted(actual.items()):
            print(f"  {pagina}: {n} sin escribir")
        print(f"  total: {total}")
    else:
        print("  OK     sin placeholders")

    # Acá se comprobaba que el 免責事項 hubiera pasado por revisión legal externa.
    # Se sacó junto con la guarda: el autor decidió publicarlo sin esa revisión,
    # así que no queda nada que esperar. El motivo, y el marco legal en el que se
    # apoya, están en CLAUDE.md.
    if roto:
        print("\nNO PUBLICAR: hay algo roto (no es la redacción)")
        return ROTO
    if total:
        print(f"\nNO PUBLICAR TODAVÍA: faltan {total} placeholders por redactar.")
        print("Es lo esperado en esta etapa. La estructura está sana:")
        print("  python tools/check-structure.py")
        return FALTA_REDACCION
    print("\nLISTO PARA PUBLICAR")
    return LISTO


if __name__ == "__main__":
    sys.exit(main())
