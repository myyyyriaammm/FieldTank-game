"""Manifest sprite loader. Missing art falls back to placeholders and never crashes."""

from __future__ import annotations

import json
from pathlib import Path

import pygame

LOGICAL_NAMES = (
    "farmer_happy",
    "farmer_neutral",
    "farmer_worried",
    "maize_good",
    "maize_mid",
    "maize_bad",
    "soy_good",
    "soy_mid",
    "soy_bad",
    "sorghum_good",
    "sorghum_mid",
    "sorghum_bad",
    "soil_ok",
    "soil_dry",
    "soil_cracked",
    "grass",
    "water_drop",
    "background",
    "logo",
)


def _int_field(spec, key):
    if key not in spec:
        return None
    value = spec[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("%s must be an integer" % key)
    return value


class AssetBank:
    def __init__(self, assets_dir: Path):
        self.assets_dir = Path(assets_dir)
        self.warnings = []
        self.sprites = {}
        self.manifest = {"sprites": {}}
        self.pixel_font = False
        self._load_manifest()
        self._load_sprites()
        self.font_s = self._font(12)
        self.font_m = self._font(16)
        self.font_l = self._font(22)

    def _load_manifest(self):
        path = self.assets_dir / "manifest.json"
        if not path.is_file():
            self.warnings.append("manifest.json missing")
            return
        try:
            obj = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            self.warnings.append("manifest.json unreadable: %s" % exc)
            return
        if not isinstance(obj, dict) or not isinstance(obj.get("sprites"), dict):
            self.warnings.append("manifest.json needs an object key 'sprites'")
            return
        self.manifest = obj

    def _load_sprites(self):
        if not pygame.get_init():
            pygame.init()
        for name, spec in self.manifest.get("sprites", {}).items():
            try:
                image = self._slice(spec)
            except Exception as exc:
                self.warnings.append("%s: %s" % (name, exc))
                image = None
            if image is not None:
                self.sprites[name] = image

    def _slice(self, spec):
        if not isinstance(spec, dict) or "file" not in spec:
            raise ValueError("sprite entry needs a file")
        path = self.assets_dir / spec["file"]
        if not path.is_file():
            return None
        image = pygame.image.load(str(path)).convert_alpha()
        keys = ("x", "y", "w", "h")
        if any(k in spec for k in keys):
            if any(k not in spec for k in keys):
                raise ValueError("x, y, w, h must all be set or all omitted")
            x = _int_field(spec, "x")
            y = _int_field(spec, "y")
            w = _int_field(spec, "w")
            h = _int_field(spec, "h")
            rect = pygame.Rect(x, y, w, h)
            if w <= 0 or h <= 0 or rect.right > image.get_width() or rect.bottom > image.get_height():
                raise ValueError("rectangle out of bounds")
            image = image.subsurface(rect).copy()
        return image

    def sprite(self, name):
        return self.sprites.get(name)

    def background_surface(self, hot, size=(1280, 720)):
        """Background scaled to the logical screen; warm and dark when hot. None if missing."""
        image = self.sprite("background")
        if image is None:
            return None
        key = (bool(hot), size)
        cache = self.__dict__.setdefault("_bg_cache", {})
        if key not in cache:
            surf = pygame.transform.scale(image, size)
            if hot:
                surf.fill((170, 120, 70), special_flags=pygame.BLEND_RGB_MULT)
            cache[key] = surf
        return cache[key]

    def blit_sprite(self, dest, name, rect):
        image = self.sprite(name)
        if image is None:
            return False
        rect = pygame.Rect(rect)
        factor = min(rect.w // image.get_width(), rect.h // image.get_height())
        if factor < 1:
            return False
        scaled = pygame.transform.scale(
            image, (image.get_width() * factor, image.get_height() * factor)
        )
        x = rect.x + (rect.w - scaled.get_width()) // 2
        y = rect.y + (rect.h - scaled.get_height()) // 2
        dest.blit(scaled, (x, y))
        return True

    def _font(self, size):
        path = self.assets_dir / "fonts" / "PressStart2P-Regular.ttf"
        if path.is_file():
            self.pixel_font = True
            return pygame.font.Font(str(path), size)
        return pygame.font.Font(None, size + 10)

    def credits_text(self) -> str:
        path = self.assets_dir / "CREDITS.txt"
        if not path.is_file():
            return ""
        return path.read_text(encoding="utf-8")
