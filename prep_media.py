"""Copy captures into media/, sized for the web.

    python prep_media.py ../devlog-media/D3-1401-scene2-flood-and-fire.png [...]

Stills become JPEGs at most 1600 px wide (quality 86), keeping the capture's name.
MP4 clips are copied as they are. Needs: Pillow
"""
import shutil
import sys
from pathlib import Path

from PIL import Image

MAX_W = 1600
OUT = Path(__file__).resolve().parent / "media"


def main(paths):
    OUT.mkdir(exist_ok=True)
    for p in map(Path, paths):
        if p.suffix.lower() == ".mp4":
            shutil.copy2(p, OUT / p.name)
            print(f"MEDIA {p.name} (copied, {p.stat().st_size // 1024} KB)")
            continue
        im = Image.open(p).convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        dst = OUT / (p.stem + ".jpg")
        im.save(dst, quality=86, optimize=True, progressive=True)
        print(f"MEDIA {dst.name} {im.width}x{im.height} {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
