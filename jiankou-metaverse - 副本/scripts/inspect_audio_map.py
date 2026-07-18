# -*- coding: utf-8 -*-
import pathlib
import re
import wave
import contextlib

ROOT = pathlib.Path(r"C:\Users\15810\Desktop\w.web")
NEW = ROOT / "新建文件夹"
META = ROOT / "jiankou-metaverse"

SCENES = {
    "w": META / "w.html",
    "sujing": META / "sujing.html",
    "guxiangdao": META / "guxiangdao.html",
    "chuxin": META / "chuxin.html",
    "yingxiongshan": META / "yingxiongshan.html",
}


def extract_concat_string(src: str, name: str) -> str | None:
    m = re.search(rf"{name}\s*=\s*((?:'(?:\\'|[^'])*'\s*\+\s*)*'(?:\\'|[^'])*')\s*;", src, re.S)
    if not m:
        return None
    parts = re.findall(r"'((?:\\'|[^'])*)'", m.group(1))
    return "".join(p.replace("\\'", "'") for p in parts)


def extract_narrations(src: str):
    return [m.group(1).replace("\\'", "'") for m in re.finditer(r"narration:\s*'((?:\\'|[^'])*)'", src)]


def extract_dialogues(src: str):
    out = []
    for m in re.finditer(r"dialogue:\s*\{([^}]*)\}", src):
        block = m.group(1)
        tm = re.search(r"text:\s*'((?:\\'|[^'])*)'", block)
        nm = re.search(r"name:\s*'((?:\\'|[^'])*)'", block)
        if tm:
            out.append(((nm.group(1) if nm else "?"), tm.group(1).replace("\\'", "'")))
    return out


def main():
    print("=== NEW AUDIO FILES ===")
    for p in sorted(NEW.glob("*.mp3")):
        print(f"{p.name:32} {p.stat().st_size:8} bytes")

    print("\n=== SCRIPT TEXT LENGTHS ===")
    for key, path in SCENES.items():
        t = path.read_text(encoding="utf-8")
        print(f"\n--- {key} ---")
        for name in ("INTRO_TEXT", "SCENE1_INTRO_TEXT", "INTRO_NARRATION"):
            s = extract_concat_string(t, name)
            if s:
                print(f"  {name}: {len(s)} chars | {s[:60]}...")
        narrs = extract_narrations(t)
        for i, n in enumerate(narrs, 1):
            print(f"  narration{i}: {len(n)} chars | {n[:60]}...")
        for i, (name, text) in enumerate(extract_dialogues(t), 1):
            print(f"  dialogue{i} ({name}): {len(text)} chars | {text}")


if __name__ == "__main__":
    main()
