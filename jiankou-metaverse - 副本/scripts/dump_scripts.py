# -*- coding: utf-8 -*-
import pathlib
import re
import sys

META = pathlib.Path(r"C:\Users\15810\Desktop\w.web\jiankou-metaverse")
NEW = pathlib.Path(r"C:\Users\15810\Desktop\w.web\新建文件夹")
OUT = META / "scripts" / "script_texts.txt"


def extract_concat_string(src: str, name: str):
    m = re.search(
        rf"{name}\s*=\s*((?:'(?:\\'|[^'])*'\s*\+\s*)*'(?:\\'|[^'])*')\s*;",
        src,
        re.S,
    )
    if not m:
        return None
    parts = re.findall(r"'((?:\\'|[^'])*)'", m.group(1))
    return "".join(p.replace("\\'", "'") for p in parts)


def main():
    lines = []
    lines.append("=== NEW AUDIO ===")
    for p in sorted(NEW.glob("*.mp3")):
        lines.append(f"{p.name}\t{p.stat().st_size}")

    for name in ["w", "sujing", "guxiangdao", "chuxin", "yingxiongshan"]:
        t = (META / f"{name}.html").read_text(encoding="utf-8")
        lines.append("")
        lines.append(f"=== {name} ===")
        for key in ["INTRO_TEXT", "SCENE1_INTRO_TEXT", "INTRO_NARRATION"]:
            s = extract_concat_string(t, key)
            if s:
                lines.append(f"{key}\tlen={len(s)}\t{s}")
        for i, m in enumerate(re.finditer(r"narration:\s*'((?:\\'|[^'])*)'", t), 1):
            s = m.group(1).replace("\\'", "'")
            lines.append(f"narration{i}\tlen={len(s)}\t{s}")
        for i, m in enumerate(re.finditer(r"dialogue:\s*\{([^}]*)\}", t), 1):
            block = m.group(1)
            tm = re.search(r"text:\s*'((?:\\'|[^'])*)'", block)
            nm = re.search(r"name:\s*'((?:\\'|[^'])*)'", block)
            if tm:
                lines.append(
                    f"dialogue{i}\t{(nm.group(1) if nm else '?')}\t{tm.group(1).replace(chr(92)+chr(39), chr(39))}"
                )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
