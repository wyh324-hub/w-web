"""Crop badge PNGs: remove white background, tight bounding box."""
from pathlib import Path
from PIL import Image

SRC = Path(r"C:\Users\15810\.cursor\projects\c-Users-15810-Desktop-jiankou-metaverse\assets")
OUT = Path(__file__).resolve().parent.parent / "assets" / "badges"

MAPPING = {
    "c__Users_15810_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_6e38823009da39f7f8e4b48cc4d24d66-d4e7d91d-0f79-4a0f-a1bb-884ccdaa2005.png": "qingbaojianbing.png",
    "c__Users_15810_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_bd752127dec8a4698fbc1b248e3134d0-02f43ae5-969a-442b-ba94-24ab36a66bbb.png": "wumingjianshouzhe.png",
    "c__Users_15810_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_298ab575ac024f0f66fd2c86ff65095e-e29c01bf-7887-4638-a71d-9e03ba4b509e.png": "gudaojiaotongyuan.png",
    "c__Users_15810_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_dd89d04db85bc1d8f099940210d5793d-b2035737-7597-43e4-89ac-d1b457e08d63.png": "chuxinmingjizhe.png",
    "c__Users_15810_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_123254813532ab9c1c345f2dbecdd5a8-b530b485-3768-4fb3-bf84-664684c61401.png": "yingxiongzhiqingren.png",
}

THRESHOLD = 235


def remove_white(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= THRESHOLD and g >= THRESHOLD and b >= THRESHOLD:
                px[x, y] = (r, g, b, 0)
    bbox = img.getbbox()
    if bbox:
        pad = 2
        bbox = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(w, bbox[2] + pad),
            min(h, bbox[3] + pad),
        )
        img = img.crop(bbox)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, out_name in MAPPING.items():
        src = SRC / src_name
        out = OUT / out_name
        img = remove_white(Image.open(src))
        img.save(out, "PNG")
        print(f"{out_name}: {img.size}")


if __name__ == "__main__":
    main()
