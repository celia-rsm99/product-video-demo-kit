#!/usr/bin/env python3
"""Saca el momento exacto de cada palabra de una locución, en local y gratis.

Sirve para anclar el vídeo a la voz: cada corte, movimiento de cámara o
subtítulo se ata a la palabra que se oye, nunca a un segundo escrito a mano
(ver fases/extras/video-explicativo-con-voz.md).

Uso:
  .venv/bin/python tools/transcribe_words.py <audio> <salida.json> [--modelo small] [--idioma es]

Necesita faster-whisper, que no viene con el kit (solo hace falta para vídeos
con voz): `.venv/bin/pip install faster-whisper`. La primera vez descarga el
modelo (~500 MB para `small`). Todo se queda en este ordenador.

Escribe [[palabra, inicio_s, fin_s], ...] en la salida e imprime un resumen.
"""
import argparse
import json

from _common import emit, fail, rel, repo_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio")
    parser.add_argument("salida")
    parser.add_argument("--modelo", default="small", help="small (multilingüe), small.en, medium…")
    parser.add_argument("--idioma", default=None, help="código del idioma de la voz (es, en…); sin él lo detecta")
    args = parser.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        fail("falta faster-whisper: instálalo con `.venv/bin/pip install faster-whisper` (o `pip3 install faster-whisper`)")

    audio = repo_path(args.audio)
    if not audio.exists():
        fail(f"no encuentro el audio: {args.audio}")

    model = WhisperModel(args.modelo, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio), word_timestamps=True, beam_size=5, language=args.idioma)
    words = [
        [w.word.strip(), round(w.start, 3), round(w.end, 3)]
        for seg in segments
        for w in seg.words
    ]
    if not words:
        fail("la transcripción no ha devuelto ninguna palabra: ¿el audio tiene voz?")

    out = repo_path(args.salida)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ",\n".join(json.dumps(w, ensure_ascii=False) for w in words)
    out.write_text(f"[\n{lines}\n]\n", encoding="utf-8")
    emit({
        "ok": True,
        "salida": rel(out),
        "idioma": info.language,
        "palabras": len(words),
        "duracion_s": words[-1][2],
        "texto": " ".join(w[0] for w in words),
    })


if __name__ == "__main__":
    main()
