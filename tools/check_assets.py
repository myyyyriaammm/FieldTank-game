"""List present, missing, unreferenced files and out-of-bounds manifest rectangles."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "manifest.json"
SKIP = {"manifest.json", "CREDITS.txt"}


def image_size(path: Path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        w = int.from_bytes(data[16:20], "big")
        h = int.from_bytes(data[20:24], "big")
        return w, h
    if data[:6] in (b"GIF87a", b"GIF89a"):
        w = int.from_bytes(data[6:8], "little")
        h = int.from_bytes(data[8:10], "little")
        return w, h
    return None


def main():
    present = []
    missing = []
    unreferenced = []
    oob = []
    notes = []
    if not MANIFEST.is_file():
        print("missing manifest: %s" % MANIFEST)
        return 1
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print("manifest is not valid JSON: %s" % exc)
        return 1
    sprites = manifest.get("sprites", {})
    if not isinstance(sprites, dict):
        print("manifest sprites must be an object")
        return 1
    referenced = set()
    for name, spec in sprites.items():
        if not isinstance(spec, dict) or "file" not in spec:
            notes.append("%s: entry needs a file" % name)
            continue
        rel = spec["file"]
        referenced.add(rel.replace("\\", "/"))
        path = ASSETS / rel
        if not path.is_file():
            missing.append("%s -> %s" % (name, rel))
            continue
        present.append("%s -> %s" % (name, rel))
        if any(k in spec for k in ("x", "y", "w", "h")):
            try:
                x, y, w, h = int(spec["x"]), int(spec["y"]), int(spec["w"]), int(spec["h"])
            except (KeyError, TypeError, ValueError):
                oob.append("%s: x,y,w,h must all be integers" % name)
                continue
            size = image_size(path)
            if size is None:
                notes.append("%s: not a PNG or GIF, bounds not checked" % name)
                continue
            iw, ih = size
            if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > iw or y + h > ih:
                oob.append("%s: rect %s,%s %sx%s outside %sx%s" % (name, x, y, w, h, iw, ih))
    if ASSETS.is_dir():
        for path in ASSETS.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ASSETS).as_posix()
            if rel in SKIP or rel.startswith("fonts/"):
                continue
            if rel not in referenced and path.suffix.lower() in {".png", ".gif"}:
                unreferenced.append(rel)
    print("present (%d)" % len(present))
    for line in present:
        print("  " + line)
    print("missing (%d)" % len(missing))
    for line in missing:
        print("  " + line)
    print("unreferenced (%d)" % len(unreferenced))
    for line in unreferenced:
        print("  " + line)
    print("out-of-bounds (%d)" % len(oob))
    for line in oob:
        print("  " + line)
    if notes:
        print("notes")
        for line in notes:
            print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
