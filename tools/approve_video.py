#!/usr/bin/env python3
"""Copia un vídeo aprobado a entregables/<flujo>/ (fase 9). Nunca sobrescribe sin permiso.

Uso:
  python3 tools/approve_video.py --video .tmp/renders/<flujo>/<nombre>.mp4 --flow <flujo> [--replace]

Si ya existe un vídeo con ese nombre en entregables/, es uno aprobado antes
(quizá ya publicado): la herramienta se niega salvo con --replace, que solo
se usa cuando la persona lo ha confirmado.
"""
import argparse
import shutil

from _common import REPO_ROOT, emit, fail, repo_path, rel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--flow", required=True)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    video = repo_path(args.video)
    if not video.exists():
        fail(f"no existe el vídeo: {video}")
    dest = REPO_ROOT / "entregables" / args.flow / video.name
    if dest.exists() and not args.replace:
        fail(f"ya hay un vídeo aprobado con ese nombre: {rel(dest)}. Pregunta antes de sustituirlo (--replace).",
             exists=rel(dest))
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(video, dest)
    emit({"ok": True, "approved": rel(dest), "replaced": args.replace})


if __name__ == "__main__":
    main()
