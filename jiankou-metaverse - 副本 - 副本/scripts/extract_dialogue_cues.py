# -*- coding: utf-8 -*-
"""Extract approximate dialogue-start timestamps from scene MP3s."""
import json
import pathlib
import sys

ROOT = pathlib.Path(r"C:\Users\15810\Desktop\w.web")
AUDIO = ROOT / "jiankou-metaverse" / "audio"
OUT = ROOT / "jiankou-metaverse" / "scripts" / "dialogue_cues.json"

# (relative path under audio/, keyword fragments to find in transcript)
TARGETS = [
    ("scene1.mp3", ["客官", "红纸", "白纸", "掌柜"]),
    ("scene3.mp3", ["相信", "trust", "林迈可", "How"]),
    ("sujing/scene1.mp3", ["老家", "闺女", "哪儿"]),
    ("guxiangdao/scene2.mp3", ["推车", "过来"]),
    ("chuxin/scene2.mp3", ["梁站长", "梁戰長", "来看"]),
]


def main():
    import whisper
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    # whisper looks for ffmpeg on PATH; ensure available
    import os
    os.environ["PATH"] = str(pathlib.Path(ffmpeg).parent) + os.pathsep + os.environ.get("PATH", "")

    model = whisper.load_model("base")
    results = {}
    for rel, keys in TARGETS:
        path = AUDIO / rel
        if not path.exists():
            print("missing", path)
            continue
        print("transcribing", rel, "...")
        r = model.transcribe(str(path), language="zh", word_timestamps=False, verbose=False)
        duration = 0.0
        cue = None
        segments = []
        for seg in r.get("segments") or []:
            text = (seg.get("text") or "").strip()
            start = float(seg.get("start") or 0)
            end = float(seg.get("end") or 0)
            duration = max(duration, end)
            segments.append({"start": round(start, 2), "end": round(end, 2), "text": text})
            if cue is None:
                low = text.lower()
                if any(k.lower() in low for k in keys):
                    cue = round(start, 2)
        # fallback: last 35% of audio
        if cue is None and duration > 0:
            cue = round(duration * 0.65, 2)
        results[rel.replace("\\", "/")] = {
            "duration": round(duration, 2),
            "dialogueAt": cue,
            "segments": segments,
        }
        print(f"  duration={duration:.1f}s dialogueAt={cue}")

    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
