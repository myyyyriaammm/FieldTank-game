"""Load scenes.json and optional lst_grid.json. No invented agronomic numbers."""

from __future__ import annotations

import json
from pathlib import Path

CROPS = ("Maïs", "Soja", "Sorgho")
SCENE_COUNT = 5
CHOICE_COUNT = 6


class DataError(Exception):
    def __init__(self, messages):
        self.messages = list(messages)
        super().__init__("\n".join(self.messages))


def assert_not_fixture(path: Path) -> None:
    parts = [p.lower() for p in path.parts]
    name = path.name.lower()
    if "fixture" in name or "tests" in parts:
        raise DataError(["Refusing to load a test fixture: %s" % path])


def _is_bool(value) -> bool:
    return isinstance(value, bool)


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value) -> bool:
    return (isinstance(value, float) or _is_int(value)) and not isinstance(value, bool)


def _need(obj, key, bucket, where):
    if not isinstance(obj, dict) or key not in obj:
        bucket.append("%s: missing '%s'" % (where, key))
        return None
    return obj[key]


def validate_scenes(obj) -> list:
    errors = []
    if not isinstance(obj, dict):
        return ["root value must be an object"]
    farmer = _need(obj, "farmer", errors, "root")
    if farmer is not None and not isinstance(farmer, str):
        errors.append("root.farmer must be a string")
    lat = _need(obj, "lat", errors, "root")
    if lat is not None and not _is_number(lat):
        errors.append("root.lat must be a number")
    cap = _need(obj, "capacity_mm", errors, "root")
    if cap is not None and not _is_int(cap):
        errors.append("root.capacity_mm must be an integer")
    scenes = _need(obj, "scenes", errors, "root")
    if not isinstance(scenes, list):
        errors.append("root.scenes must be a list")
        return errors
    if len(scenes) != SCENE_COUNT:
        errors.append("expected %d scenes, got %d" % (SCENE_COUNT, len(scenes)))
    for i, scene in enumerate(scenes):
        where = "scene %d" % i
        if not isinstance(scene, dict):
            errors.append("%s must be an object" % where)
            continue
        for key in ("year", "title", "story", "rain_mm", "hot_days", "choices"):
            if key not in scene:
                errors.append("%s: missing '%s'" % (where, key))
        if "title" in scene and not isinstance(scene["title"], str):
            errors.append("%s.title must be a string" % where)
        if "story" in scene and not isinstance(scene["story"], str):
            errors.append("%s.story must be a string" % where)
        if "year" in scene and not (isinstance(scene["year"], str) or _is_int(scene["year"])):
            errors.append("%s.year must be a string or integer" % where)
        if "rain_mm" in scene and not _is_number(scene["rain_mm"]):
            errors.append("%s.rain_mm must be a number" % where)
        if "hot_days" in scene and not _is_int(scene["hot_days"]):
            errors.append("%s.hot_days must be an integer" % where)
        choices = scene.get("choices")
        if not isinstance(choices, list):
            errors.append("%s.choices must be a list" % where)
            continue
        if len(choices) != CHOICE_COUNT:
            errors.append("%s: expected %d choices, got %d" % (where, CHOICE_COUNT, len(choices)))
        pairs = []
        for j, choice in enumerate(choices):
            cw = "%s choice %d" % (where, j)
            if not isinstance(choice, dict):
                errors.append("%s must be an object" % cw)
                continue
            crop = choice.get("crop")
            if crop not in CROPS:
                errors.append("%s.crop must be one of %s" % (cw, ", ".join(CROPS)))
            irrigate = choice.get("irrigate")
            if not _is_bool(irrigate):
                errors.append("%s.irrigate must be a boolean" % cw)
            else:
                pairs.append((crop, irrigate))
            for key in ("yield_pct", "stress_days", "heat_days", "irrigation_mm"):
                if key not in choice or not _is_int(choice[key]):
                    errors.append("%s.%s must be an integer" % (cw, key))
            if "min_water_pct" not in choice or not _is_number(choice["min_water_pct"]):
                errors.append("%s.min_water_pct must be a number" % cw)
            curve = choice.get("water_curve")
            if not isinstance(curve, list) or not curve:
                errors.append("%s.water_curve must be a non-empty list" % cw)
            elif any(not _is_number(v) for v in curve):
                errors.append("%s.water_curve values must be numbers" % cw)
        expected = {(c, flag) for c in CROPS for flag in (False, True)}
        if len(choices) == CHOICE_COUNT and pairs and set(pairs) != expected:
            errors.append("%s: choices must be exactly 3 crops x irrigation yes/no" % where)
        if len(pairs) != len(set(pairs)):
            errors.append("%s: duplicate crop/irrigation pair" % where)
    return errors


def validate_lst(obj) -> list:
    errors = []
    if not isinstance(obj, dict):
        return ["lst root must be an object"]
    for key in ("time_utc", "unit", "rows", "cols", "values_row_major_top_to_bottom"):
        if key not in obj:
            errors.append("lst missing '%s'" % key)
    if obj.get("unit") != "K":
        errors.append("lst.unit must be 'K'")
    if obj.get("rows") != 20 or obj.get("cols") != 20:
        errors.append("lst.rows and lst.cols must be 20")
    values = obj.get("values_row_major_top_to_bottom")
    if not isinstance(values, list) or len(values) != 400:
        errors.append("lst values must be a list of 400 numbers or null")
    else:
        for i, value in enumerate(values):
            if value is not None and not _is_number(value):
                errors.append("lst value %d must be a number or null" % i)
                break
    return errors


def load_json(path: Path):
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise DataError(["cannot read %s: %s" % (path, exc)]) from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise DataError(["%s is not valid JSON: %s" % (path, exc)]) from exc


def load_scenes(path: Path) -> dict:
    assert_not_fixture(Path(path))
    obj = load_json(Path(path))
    errors = validate_scenes(obj)
    if errors:
        raise DataError(errors)
    return obj


def load_lst(path: Path) -> dict:
    obj = load_json(Path(path))
    errors = validate_lst(obj)
    if errors:
        raise DataError(errors)
    return obj


def locate_file(root: Path, names) -> Path | None:
    for name in names:
        path = root / name
        if path.is_file():
            return path
    return None


def load_game_data(root: Path):
    root = Path(root)
    scene_path = locate_file(root, ("scenes.json", "data/scenes.json"))
    if scene_path is None:
        raise DataError(["scenes.json not found in project root or data/"])
    scenes = load_scenes(scene_path)
    lst_path = locate_file(root, ("lst_grid.json", "data/lst_grid.json"))
    lst = None
    if lst_path is not None:
        lst = load_lst(lst_path)
    return scenes, lst, scene_path, lst_path


def lst_numeric(lst) -> list:
    return [v for v in lst["values_row_major_top_to_bottom"] if v is not None]


def lst_hot_cutoff(lst):
    values = lst_numeric(lst)
    if not values:
        return None
    ordered = sorted(values, reverse=True)
    return ordered[int(len(values) * 0.1)]


def kelvin_to_c(value):
    return value - 273.15
