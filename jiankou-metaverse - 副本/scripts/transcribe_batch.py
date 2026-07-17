import re
from pathlib import Path
import whisper
import imageio_ffmpeg

AUDIO_DIR = Path(r"C:\Users\15810\Desktop\w.web\新建文件夹")
OUT = Path(r"C:\Users\15810\Desktop\w.web\jiankou-metaverse\scripts\transcripts.txt")

FILES = [
    "pingxiqingbaolianluozhan.mp3", "pingxichangjingyi.mp3", "pingxichangjing2.mp3", "pingxichangjing3.mp3",
    "sujingshandong.mp3", "sujingchangjingyi.mp3", "sujingchangjing2.mp3", "sujingchangjing3.mp3",
    "guxiangdao.mp3", "guxiangdao1.mp3", "guxiangdao2.mp3",
    "chuxinguangchang.mp3", "chuxin1.mp3", "chuxin2.mp3", "chuxin3.mp3",
    "yingxiongshan.mp3", "yingxiongshan1.mp3", "yingxiongshan2.mp3", "yingxiongshan3.mp3",
]

import os
os.environ["PATH"] = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe()) + os.pathsep + os.environ.get("PATH", "")

def classify(text: str, fname: str) -> str:
    t = text.strip()
    if not t:
        return "unknown (empty/silent)"
    dialogue_markers = len(re.findall(r"[「」""''？！]", t))
    you_i = len(re.findall(r"(你|您|我们|咱们)", t))
    said = len(re.findall(r"(说道|问道|回答|喊道|说：|说,|说，)", t))
    intro = bool(re.search(r"(欢迎|介绍|概览|简介|情报联络|联络站|进入|开启|接下来)", t))
    narrative_third = len(re.findall(r"(这里|此处|当年|如今|位于|展现|讲述|记录|场景)", t))
    short_lines = [s.strip() for s in re.split(r"[。！？\n]", t) if s.strip()]
    avg_len = sum(len(s) for s in short_lines) / max(len(short_lines), 1)
    q_count = t.count("？") + t.count("?")
    fn = fname.lower()

    is_dialogue_heavy = (q_count >= 2 and you_i >= 3) or dialogue_markers >= 2 or said >= 2
    is_mostly_dialogue = is_dialogue_heavy and narrative_third <= 2 and avg_len < 35

    if is_mostly_dialogue and narrative_third <= 1:
        return "character dialogue only"
    if is_dialogue_heavy and narrative_third >= 2:
        return "narration+character dialogue"
    if intro and not is_dialogue_heavy:
        return "intro narration only"
    if narrative_third >= 2 and not is_dialogue_heavy:
        return "scene narration only"
    if is_dialogue_heavy:
        return "narration+character dialogue"
    if "changjing" in fn or re.search(r"(chuxin|yingxiong|guxiang)\d", fn):
        if is_dialogue_heavy:
            return "narration+character dialogue"
        return "scene narration only"
    if "qingbao" in fn or fn.endswith("guangchang.mp3") or fn in ("guxiangdao.mp3", "sujingshandong.mp3", "yingxiongshan.mp3", "chuxinguangchang.mp3"):
        return "intro narration only"
    return "scene narration only"

print("Loading whisper base...", flush=True)
model = whisper.load_model("base")

results = []
for i, fn in enumerate(FILES, 1):
    path = AUDIO_DIR / fn
    print(f"[{i}/{len(FILES)}] {fn}", flush=True)
    out = model.transcribe(str(path), language="zh", fp16=False)
    text = (out.get("text") or "").strip()
    ctype = classify(text, fn)
    results.append((fn, text, ctype))

lines = []
for fn, text, ctype in results:
    lines.append(f"=== {fn} ===")
    lines.append(text if text else "(no speech detected)")
    lines.append(f"[Content type: {ctype}]")
    lines.append("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print("WROTE", OUT, flush=True)
for fn, _, ctype in results:
    print(f"{fn}: {ctype}", flush=True)
