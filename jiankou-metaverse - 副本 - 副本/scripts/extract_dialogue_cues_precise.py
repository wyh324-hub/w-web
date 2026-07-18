# -*- coding: utf-8 -*-
import json
import os
import pathlib
import shutil

import imageio_ffmpeg
import whisper

ROOT = pathlib.Path(r"C:\Users\15810\Desktop\w.web")
AUDIO = ROOT / "jiankou-metaverse" / "audio"
SCRIPTS = ROOT / "jiankou-metaverse" / "scripts"
OUT = SCRIPTS / "dialogue_cues_precise.json"

ff = imageio_ffmpeg.get_ffmpeg_exe()
shutil.copy2(ff, SCRIPTS / "ffmpeg.exe")
os.environ["PATH"] = str(SCRIPTS) + os.pathsep + os.environ.get("PATH", "")

# cue phrase fragments (any match in word/segment text)
JOBS = [
    {
        "file": "scene1.mp3",
        "label": "pingxi_shopkeeper",
        "phrases": ["不紧不慢", "不仅不慢", "不緊不慢", "慢的问", "慢地问", "慢的問"],
    },
    {
        "file": "scene3.mp3",
        "label": "pingxi_linmaike",
        "phrases": ["how can i trust", "trust you", "相信你", "相信"],
    },
    {
        "file": "sujing/scene1.mp3",
        "label": "sujing_popo",
        "phrases": ["随口问", "隨口問", "一边", "一邊", "老家是哪儿", "老家是哪兒", "闺女", "閨女"],
    },
    {
        "file": "chuxin/scene2.mp3",
        "label": "chuxin_elder",
        "phrases": ["缓缓开口", "緩緩開口", "开口", "開口", "梁站长", "梁戰長", "来看梁"],
    },
    {
        "file": "guxiangdao/scene2.mp3",
        "label": "guxiang_soldier",
        "phrases": ["推车", "推車", "过来", "過來", "招手"],
    },
]


def find_cue(result, phrases):
    # Prefer word-level timestamps
    for seg in result.get("segments") or []:
        words = seg.get("words") or []
        if words:
            # sliding window join
            for i, w in enumerate(words):
                chunk = "".join((x.get("word") or "") for x in words[i : i + 6]).lower()
                for p in phrases:
                    if p.lower() in chunk:
                        return float(w.get("start") or seg.get("start") or 0), "word:" + p
        text = (seg.get("text") or "").lower()
        for p in phrases:
            if p.lower() in text:
                return float(seg.get("start") or 0), "seg:" + p
    return None, None


def main():
    model = whisper.load_model("base")
    out = {}
    for job in JOBS:
        path = AUDIO / job["file"]
        print("===", job["label"], path.name)
        r = model.transcribe(str(path), language="zh", word_timestamps=True, verbose=False)
        cue, how = find_cue(r, job["phrases"])
        segs = []
        for seg in r.get("segments") or []:
            segs.append(
                {
                    "start": round(float(seg.get("start") or 0), 2),
                    "end": round(float(seg.get("end") or 0), 2),
                    "text": (seg.get("text") or "").strip(),
                    "words": [
                        {
                            "w": (w.get("word") or "").strip(),
                            "start": round(float(w.get("start") or 0), 2),
                        }
                        for w in (seg.get("words") or [])
                    ],
                }
            )
        dur = max((s["end"] for s in segs), default=0)
        out[job["label"]] = {
            "file": job["file"],
            "duration": dur,
            "dialogueAt": round(cue, 2) if cue is not None else None,
            "matched": how,
            "segments": segs,
        }
        print("  dialogueAt=", cue, how)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
