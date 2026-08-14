#!/usr/bin/env python3
"""Genera la copia DERIVADA de CLAUDE.md que lee el Claude del chat.

    python tools/make-copia-claudemd.py

EL PROBLEMA QUE RESUELVE (2026-08-14, pedido del autor): el Claude del chat
de diseño no llega a C:\\Dev — su alcance es la carpeta de Claude en
OneDrive—, así que armaba prompts a ciegas sobre el archivo que tiene las
respuestas: en una sola sesión preguntó tres cosas ya registradas. La copia
pone el registro donde él SÍ lee.

LAS REGLAS DEL ARTEFACTO (la decisión completa vive en CLAUDE.md):

- La copia va ENTERA, no un extracto: un criterio de selección es el que
  deriva; «entero» no tiene criterio que mantener.
- Deriva SIEMPRE del CLAUDE.md de HEAD (los bytes del blob — sin autocrlf:
  lo copiado es lo commiteado, byte a byte) y ABORTA si el del árbol de
  trabajo difiere: el encabezado declara fecha y commit, y una copia de un
  estado sin commitear haría mentir esa declaración.
- El gatillo es el COMMIT, no el deploy: tras cada commit que toque
  CLAUDE.md se corre esto. El olvido tiene guarda: check-structure compara
  la copia contra HEAD:CLAUDE.md y frena nombrando este comando.
- La copia NO se edita nunca — se regenera. El encabezado lo dice, y la
  guarda ve cualquier edición como divergencia (que es lo correcto:
  «arreglar» la copia en vez de la fuente es exactamente la deriva que la
  marca DERIVADA existe para evitar).
"""
import datetime
import subprocess
import sys

import _guardas as G

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def git(*args):
    return subprocess.run(["git", "-C", str(G.RAIZ)] + list(args),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout.strip()


def main():
    destino = G.COPIA_CLAUDEMD
    if not destino.parent.exists():
        sys.exit(f"no existe la carpeta destino {destino.parent} — la copia es "
                 f"un artefacto de la máquina del autor (OneDrive); en otra "
                 f"máquina no hay nada que generar")

    blob = G.claudemd_en_head()
    if blob is None:
        sys.exit("no se pudo leer HEAD:CLAUDE.md — ¿git disponible? ¿repo?")
    # El árbol de trabajo puede estar en CRLF por autocrlf; el blob es LF.
    arbol = (G.RAIZ / "CLAUDE.md").read_bytes().replace(b"\r\n", b"\n")
    if arbol != blob:
        sys.exit("el CLAUDE.md del árbol de trabajo difiere del de HEAD — "
                 "commitear primero: la copia deriva de un commit, para que "
                 "su encabezado (fecha y commit) no mienta")

    commit = git("rev-parse", "HEAD")
    titulo = git("log", "-1", "--format=%s")
    fecha_commit = git("log", "-1", "--format=%cs")
    hoy = datetime.date.today().isoformat()

    # La plantilla vive en _guardas (encabezado_copia): la guarda RECONSTRUYE
    # el encabezado con la misma función para compararlo — sin eso, una
    # edición a mano del encabezado pasaba en verde (revisión adversarial).
    encabezado = G.encabezado_copia(commit, titulo, fecha_commit, hoy)

    destino.write_bytes(encabezado.encode("utf-8") + blob)
    print(f"copia escrita: {destino}")
    print(f"  fuente: CLAUDE.md de {commit[:12]} («{titulo[:60]}»)")
    print(f"  {len(blob)} bytes de cuerpo + encabezado derivado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
