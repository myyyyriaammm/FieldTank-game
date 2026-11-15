"""Blocky field, HUD, satellite panel, charts. Missing sprites use placeholders."""

from __future__ import annotations

import pygame

import strings
from game.data import kelvin_to_c, lst_hot_cutoff, lst_numeric
from game.state import (
    curve_day,
    curve_index,
    final_mood,
    lesson_numbers,
    live_kind,
    mood_from_gap,
    score_choice,
    soil_band,
    yield_kind,
)
from game.ui import (
    BAD,
    CRACK,
    DIRT,
    DRY,
    EDGE,
    GRASS,
    INK,
    NAME,
    OK,
    PLACE,
    SKY,
    SKY_HOT,
    SUN,
    SUN_HOT,
    TITLE,
    XP,
    YELLOW,
    Button,
    draw_button,
    draw_panel,
    draw_text,
    draw_wrapped,
    heat_rect,
    menu_rects,
    option_rects,
    tank_rect,
    wrap,
)

CROP_KEY = {"Maïs": "maize", "Soja": "soy", "Sorgho": "sorghum"}


def _heart(surf, x, y, filled):
    color = (220, 40, 60) if filled else (50, 50, 50)
    mask = (
        "01100110",
        "11111111",
        "11111111",
        "11111111",
        "01111110",
        "00111100",
        "00011000",
        "00001000",
    )
    for r, row in enumerate(mask):
        for c, ch in enumerate(row):
            if ch == "1":
                surf.fill(color, (x + c * 2, y + r * 2, 2, 2))


def draw_hud(surf, assets, run):
    font = assets.font_s
    pygame.draw.rect(surf, (17, 17, 17), (0, 0, 1280, 56))
    for i in range(5):
        _heart(surf, 16 + i * 22, 16, i < run.hearts)
    total = len(run.data["scenes"])
    if run.phase in ("title", "error"):
        label = strings.t("season_idle", total=total)
    else:
        label = strings.t("season", n=min(run.season + 1, total), total=total)
    draw_text(surf, font, label, INK, 1040, 18)
    bar = pygame.Rect(180, 20, 820, 16)
    pygame.draw.rect(surf, (34, 34, 34), bar)
    pygame.draw.rect(surf, EDGE, bar, 3)
    width = int(bar.w * (run.completed / total)) if total else 0
    if width:
        surf.fill(XP, (bar.x, bar.y, width, bar.h))


def _dot(surf, x, y, color):
    surf.fill(color, (x, y, 2, 2))


def draw_soil_tile(surf, assets, name, rect, band):
    if assets.blit_sprite(surf, name, rect):
        return
    rect = pygame.Rect(rect)
    if band == "ok":
        surf.fill(DIRT, rect)
        for i in range(4):
            _dot(surf, rect.x + 6 + (i * 7) % (rect.w - 8), rect.y + 8 + (i * 5) % (rect.h - 8), (0, 0, 0))
    elif band == "dry":
        surf.fill(DRY, rect)
        pygame.draw.line(surf, (0, 0, 0), (rect.x + 8, rect.y + 8), (rect.x + rect.w - 8, rect.y + rect.h - 6), 2)
    else:
        surf.fill(CRACK, rect)
        pygame.draw.line(surf, (0, 0, 0), (rect.x + 4, rect.y + 6), (rect.x + rect.w - 6, rect.y + rect.h - 4), 2)
        pygame.draw.line(surf, (0, 0, 0), (rect.x + rect.w - 8, rect.y + 6), (rect.x + 8, rect.y + rect.h - 6), 2)
    pygame.draw.rect(surf, (0, 0, 0), rect, 1)


def draw_grass_tile(surf, rect, assets=None):
    if assets is not None and assets.blit_sprite(surf, "grass", rect):
        return
    rect = pygame.Rect(rect)
    surf.fill(GRASS, (rect.x, rect.y, rect.w, rect.h // 3))
    surf.fill(DIRT, (rect.x, rect.y + rect.h // 3, rect.w, rect.h - rect.h // 3))
    _dot(surf, rect.x + 6, rect.y + 6, (0, 0, 0))
    _dot(surf, rect.x + 16, rect.y + 8, (0, 0, 0))


def draw_crop_placeholder(surf, crop, kind, rect):
    rect = pygame.Rect(rect)
    cx = rect.centerx
    base = rect.bottom - 4
    scale = {"good": 22, "mid": 14, "bad": 8}[kind]
    color = {"Maïs": (240, 200, 40), "Soja": (40, 140, 50), "Sorgho": (190, 90, 30)}[crop]
    if kind == "bad":
        color = (120, 70, 40)
    pygame.draw.line(surf, (40, 90, 30), (cx, base), (cx, base - scale), 3)
    pygame.draw.circle(surf, color, (cx, base - scale), 5 if kind != "bad" else 3)


def draw_crop(surf, assets, crop, kind, rect):
    key = "%s_%s" % (CROP_KEY[crop], kind)
    if assets.blit_sprite(surf, key, rect):
        return
    draw_crop_placeholder(surf, crop, kind, rect)


def draw_sun(surf, hot, x=760, y=78):
    color = SUN_HOT if hot else SUN
    pygame.draw.rect(surf, color, (x, y, 36, 36))
    shade = (194, 65, 12) if hot else (240, 180, 0)
    pygame.draw.rect(surf, shade, (x + 18, y + 18, 14, 14))


def draw_farmer(surf, assets, mood, rect):
    key = "farmer_%s" % mood
    if assets.blit_sprite(surf, key, rect):
        return
    rect = pygame.Rect(rect)
    skin = (242, 196, 140)
    shirt = (40, 90, 180)
    if mood == "worried":
        shirt = (140, 40, 40)
    elif mood == "happy":
        shirt = (40, 120, 50)
    pygame.draw.rect(surf, skin, (rect.x + 16, rect.y + 4, 32, 24))
    pygame.draw.rect(surf, shirt, (rect.x + 10, rect.y + 30, 44, 28))
    pygame.draw.rect(surf, (40, 30, 20), (rect.x + 16, rect.y + 58, 10, 16))
    pygame.draw.rect(surf, (40, 30, 20), (rect.x + 38, rect.y + 58, 10, 16))
    eye = (20, 20, 20)
    pygame.draw.rect(surf, eye, (rect.x + 22, rect.y + 12, 4, 4))
    pygame.draw.rect(surf, eye, (rect.x + 36, rect.y + 12, 4, 4))


def draw_field(surf, assets, crop, band, kind, cols=12, origin=(40, 150), tile=32):
    ox, oy = origin
    for c in range(cols):
        draw_grass_tile(surf, (ox + c * tile, oy, tile, tile), assets)
    for r in range(3):
        for c in range(cols):
            rect = (ox + c * tile, oy + (r + 1) * tile, tile, tile)
            name = {"ok": "soil_ok", "dry": "soil_dry", "cracked": "soil_cracked"}[band]
            draw_soil_tile(surf, assets, name, rect, band)
            if r == 0:
                draw_crop(surf, assets, crop, kind, rect)


def draw_tank(surf, font, value):
    rect = tank_rect()
    pygame.draw.rect(surf, (20, 30, 50), rect)
    pygame.draw.rect(surf, EDGE, rect, 3)
    shown = max(0.0, min(100.0, float(value)))
    h = int(rect.h * shown / 100.0)
    if h:
        surf.fill((40, 140, 220), (rect.x, rect.bottom - h, rect.w, h))
    draw_text(surf, font, strings.t("tank"), PLACE, rect.x - 4, rect.y - 36)
    draw_text(surf, font, strings.fmt_num(value), INK, rect.x - 8, rect.bottom + 8)


def _hsv_to_rgb(h, s, v):
    i = int(h * 6.0)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)


def draw_satellite(surf, assets, lst, hot, mouse):
    font = assets.font_s
    panel = pygame.Rect(890, 64, 374, 390)
    draw_panel(surf, panel, (12, 16, 28))
    draw_wrapped(surf, font, strings.t("sat_label"), PLACE, (900, 70, 354, 70), 2)
    if lst is None:
        return
    values = lst["values_row_major_top_to_bottom"]
    nums = lst_numeric(lst)
    grid = heat_rect()
    cell = grid.w // 20
    vmin = min(nums) if nums else 0
    vmax = max(nums) if nums else 1
    cut = lst_hot_cutoff(lst)
    span = (vmax - vmin) or 1
    for n, value in enumerate(values):
        r, c = divmod(n, 20)
        box = pygame.Rect(grid.x + c * cell, grid.y + r * cell, cell, cell)
        if value is None:
            surf.fill((70, 80, 90), box)
            pygame.draw.circle(surf, INK, box.center, max(2, cell // 4))
        else:
            hue = (220 - 220 * ((value - vmin) / span)) / 360.0
            surf.fill(_hsv_to_rgb(hue, 0.75, 0.50), box)
            if hot and cut is not None and value >= cut:
                pygame.draw.rect(surf, INK, box, 1)
    lo = kelvin_to_c(vmin) if nums else 0
    hi = kelvin_to_c(vmax) if nums else 0
    draw_text(surf, font, strings.t("sat_range", lo=strings.fmt_num(lo), hi=strings.fmt_num(hi)), INK, 900, 396)
    extra = ""
    if mouse is not None:
        col_row = None
        if grid.collidepoint(mouse):
            col = (mouse[0] - grid.x) // cell
            row = (mouse[1] - grid.y) // cell
            if 0 <= col < 20 and 0 <= row < 20:
                value = values[row * 20 + col]
                if value is None:
                    extra = strings.t("sat_cloud", r=row + 1, c=col + 1)
                else:
                    extra = strings.t(
                        "sat_hover",
                        r=row + 1,
                        c=col + 1,
                        cels=strings.fmt_num(kelvin_to_c(value)),
                        kelvin=strings.fmt_num(value),
                    )
    if not extra:
        extra = strings.t("sat_hint")
    draw_wrapped(surf, font, extra, YELLOW, (900, 414, 354, 36), 2)


def draw_chart(surf, font, chosen, best, rect):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surf, (16, 16, 16), rect)
    pygame.draw.rect(surf, EDGE, rect, 2)
    a = chosen["water_curve"]
    b = best["water_curve"]
    n = max(len(a), len(b), 2)

    def xy(series, i):
        x = rect.x + 8 + int((rect.w - 16) * (i / (n - 1)))
        v = series[min(i, len(series) - 1)]
        y = rect.bottom - 8 - int((rect.h - 16) * max(0.0, min(100.0, v)) / 100.0)
        return x, y

    if len(b) >= 1:
        pts = [xy(b, i) for i in range(n)]
        if len(pts) > 1:
            pygame.draw.lines(surf, (85, 255, 85), False, pts, 2)
    if len(a) >= 1:
        pts = [xy(a, i) for i in range(n)]
        if len(pts) > 1:
            pygame.draw.lines(surf, YELLOW, False, pts, 2)
    draw_text(surf, font, strings.t("chart_chosen"), YELLOW, rect.x, rect.y - 16)
    draw_text(surf, font, strings.t("chart_best"), (85, 255, 85), rect.x + 160, rect.y - 16)


def sky_color(hot):
    return SKY_HOT if hot else SKY


def draw_background(surf, assets, hot, rect, src_y=None):
    """Draw background.png into rect (from src_y in the image, default: same place).

    Falls back to the flat sky colour if the image is missing.
    """
    rect = pygame.Rect(rect)
    bg = assets.background_surface(hot)
    if bg is None:
        surf.fill(sky_color(hot), rect)
        return
    top = rect.y if src_y is None else src_y
    surf.blit(bg, rect.topleft, area=pygame.Rect(rect.x, top, rect.w, rect.h))


def draw_drops(surf, assets, tick):
    for i in range(6):
        x = 80 + i * 64
        y = 90 + ((tick * 3 + i * 17) % 80)
        rect = pygame.Rect(x, y, 12, 16)
        if not assets.blit_sprite(surf, "water_drop", rect):
            pygame.draw.rect(surf, (80, 170, 255), rect)


def draw_shimmer(surf, tick):
    overlay = pygame.Surface((420, 20), pygame.SRCALPHA)
    overlay.fill((255, 120, 20, 50))
    surf.blit(overlay, (40, 120 + (tick % 20)))


def build_option_buttons(run, reveal=False):
    buttons = []
    rects = option_rects(len(run.offered))
    best = run.best_offered() if reveal and run.picked is not None else None
    best_score = score_choice(best, run.goal) if best is not None else None
    for i, choice in enumerate(run.offered):
        style = "normal"
        if reveal:
            score = score_choice(choice, run.goal)
            if i == run.picked:
                style = "ok" if score == best_score else "bad"
            elif score == best_score:
                style = "best"
        buttons.append(Button(rects[i], strings.option_label(choice), strings.t("slot", k=i + 1), style))
    return buttons


def draw_intro(surf, assets, run):
    scene = run.scene()
    hot = scene["hot_days"] > 0
    draw_background(surf, assets, hot, (0, 56, 1280, 664))
    draw_sun(surf, hot)
    font = assets.font_s
    draw_text(surf, assets.font_m, str(scene["year"]), PLACE, 40, 80)
    draw_wrapped(surf, assets.font_m, scene["title"], TITLE, (40, 110, 800, 60), 4)
    draw_wrapped(surf, font, scene["story"], INK, (40, 180, 820, 160), 4)
    y = 360
    for line in (
        strings.t("intro_rain", mm=strings.fmt_num(scene["rain_mm"])),
        strings.t("intro_hot", n=scene["hot_days"]),
        strings.t("intro_cap", mm=run.data["capacity_mm"]),
        strings.t("intro_lat", lat=strings.fmt_num(run.data["lat"])),
    ):
        draw_text(surf, font, line, YELLOW, 40, y)
        y += 28
    draw_satellite(surf, assets, run.lst, hot, None)
    return [Button((40, 620, 280, 56), strings.t("btn_continue"))]


def draw_ask(surf, assets, run, mouse):
    scene = run.scene()
    hot = scene["hot_days"] > 0
    draw_background(surf, assets, hot, (0, 56, 880, 400), src_y=320)
    draw_sun(surf, hot, 760, 70)
    draw_farmer(surf, assets, "neutral", (40, 300, 72, 80))
    bubble = pygame.Rect(130, 300, 720, 140)
    draw_panel(surf, bubble)
    draw_text(surf, assets.font_s, run.data["farmer"], NAME, 146, 312)
    draw_wrapped(surf, assets.font_s, strings.question_text(run.season), INK, (146, 336, 690, 90), 4)
    draw_satellite(surf, assets, run.lst, hot, mouse)
    if hot and run.lst is not None:
        cut = lst_hot_cutoff(run.lst)
        if cut is not None:
            draw_text(surf, assets.font_s, strings.t("sat_hot", cut=strings.fmt_num(cut)), YELLOW, 900, 64)
    buttons = build_option_buttons(run, False)
    for button in buttons:
        draw_button(surf, assets.font_s, button)
    return buttons


def draw_play(surf, assets, run, tick):
    scene = run.scene()
    choice = run.chosen()
    hot = scene["hot_days"] > 0 or choice["heat_days"] > 0
    draw_background(surf, assets, hot, (0, 56, 1280, 664))
    draw_sun(surf, hot)
    idx = curve_index(run.play_t, len(choice["water_curve"]))
    value = choice["water_curve"][idx]
    band = soil_band(value)
    kind = live_kind(value)
    if run.play_t >= 8.0:
        kind = yield_kind(choice["yield_pct"])
    draw_field(surf, assets, choice["crop"], band, kind)
    draw_tank(surf, assets.font_s, value)
    draw_text(surf, assets.font_m, strings.t("day", n=curve_day(idx)), INK, 40, 80)
    draw_text(surf, assets.font_s, strings.t("day_note"), YELLOW, 40, 112)
    draw_wrapped(surf, assets.font_s, strings.t("soil_rule"), INK, (440, 80, 360, 70), 2)
    if choice["irrigation_mm"] > 0:
        draw_drops(surf, assets, tick)
        draw_text(
            surf,
            assets.font_s,
            strings.t("anim_irr", mm=choice["irrigation_mm"]),
            PLACE,
            40,
            430,
        )
    if choice["heat_days"] > 0:
        draw_shimmer(surf, tick)
        draw_text(
            surf,
            assets.font_s,
            strings.t("anim_heat", n=choice["heat_days"]),
            TITLE,
            40,
            454,
        )
    draw_text(surf, assets.font_s, strings.t("play_skip"), YELLOW, 40, 660)
    return []


def draw_result(surf, assets, run):
    surf.fill((16, 18, 22), (0, 56, 1280, 664))
    choice = run.chosen()
    best = run.best_offered()
    gap = run.gap()
    mood = mood_from_gap(gap)
    draw_farmer(surf, assets, mood, (24, 70, 72, 80))
    font = assets.font_s
    draw_text(surf, font, run.data["farmer"], NAME, 110, 70)
    draw_text(surf, font, strings.t("sam_%s" % mood), INK, 110, 92)
    draw_text(surf, font, strings.t("mood_rule"), (180, 180, 180), 110, 114)
    draw_text(surf, assets.font_m, strings.t("result_title"), TITLE, 110, 140)
    draw_text(surf, font, strings.t("gap_line", gap=strings.fmt_num(gap)), YELLOW, 110, 172)
    lost = run.history[-1]["hearts_lost"] if run.history else 0
    draw_text(surf, font, strings.t("hearts_lost", n=lost), INK, 110, 196)
    draw_wrapped(surf, font, strings.t("hearts_rule"), (200, 200, 200), (110, 218, 700, 40), 2)
    facts = [
        strings.t("fact_yield", n=choice["yield_pct"]),
        strings.t("fact_min_file", v=strings.fmt_num(choice["min_water_pct"])),
        strings.t("fact_min_curve", v=strings.fmt_num(min(choice["water_curve"]))),
        strings.t("fact_stress", n=choice["stress_days"]),
        strings.t("fact_irr", n=choice["irrigation_mm"]),
        strings.t("fact_heat", n=choice["heat_days"]),
    ]
    y = 268
    for line in facts:
        draw_text(surf, font, line, INK, 24, y)
        y += 22
    draw_chart(surf, font, choice, best, (430, 280, 420, 140))
    _table(surf, font, run, (24, 430, 900, 160))
    facts_n = lesson_numbers(run.scene(), run.goal)
    if facts_n["crop"] is None:
        lesson = strings.t("lesson_spread", spread=strings.fmt_num(facts_n["spread"]))
    else:
        lesson = strings.t(
            "lesson_pair",
            crop=facts_n["crop"],
            dy=strings.fmt_num(facts_n["yield_delta"]),
            ds=strings.fmt_num(facts_n["stress_saved"]),
            spread=strings.fmt_num(facts_n["spread"]),
        )
    draw_wrapped(surf, font, lesson, YELLOW, (24, 600, 980, 50), 2)
    buttons = build_option_buttons(run, True)
    for button in buttons:
        button.rect = pygame.Rect(0, 0, 0, 0)
    label = strings.t("btn_over") if run.hearts <= 0 else (
        strings.t("btn_final") if run.season == len(run.data["scenes"]) - 1 else strings.t("btn_next")
    )
    go = Button((1000, 640, 250, 56), label)
    draw_button(surf, font, go)
    return [go]


def _table(surf, font, run, rect):
    rect = pygame.Rect(rect)
    headers = [
        strings.t("col_crop"),
        strings.t("col_irr"),
        strings.t("col_yield"),
        strings.t("col_stress"),
        strings.t("col_heat"),
        strings.t("col_imm"),
        strings.t("col_score"),
        strings.t("col_offer"),
    ]
    offered = {(c["crop"], c["irrigate"]) for c in run.offered}
    x0 = rect.x
    widths = (120, 70, 70, 70, 70, 70, 120, 90)
    y = rect.y
    x = x0
    for h, w in zip(headers, widths):
        draw_text(surf, font, h, PLACE, x, y)
        x += w
    y += 20
    for choice in run.scene()["choices"]:
        score = score_choice(choice, run.goal)
        flag = (choice["crop"], choice["irrigate"]) in offered
        cells = [
            choice["crop"],
            strings.t("yes") if choice["irrigate"] else strings.t("no"),
            str(choice["yield_pct"]),
            str(choice["stress_days"]),
            str(choice["heat_days"]),
            str(choice["irrigation_mm"]),
            strings.fmt_num(score),
            strings.t("offered_yes") if flag else strings.t("offered_no"),
        ]
        x = x0
        color = YELLOW if run.picked is not None and choice is run.chosen() else INK
        for cell, w in zip(cells, widths):
            draw_text(surf, font, cell, color, x, y)
            x += w
        y += 18


def draw_title(surf, assets, run):
    draw_background(surf, assets, False, (0, 56, 1280, 664))
    if not assets.blit_sprite(surf, "logo", (540, 70, 200, 80)):
        draw_text(surf, assets.font_l, strings.t("title"), EDGE, 470, 90)
    draw_text(surf, assets.font_s, strings.t("tag"), EDGE, 280, 160)
    draw_text(surf, assets.font_s, strings.t("pick_goal"), NAME, 360, 190)
    labels = [
        strings.t("goal_yield") + " — " + strings.t("goal_yield_hint"),
        strings.t("goal_water") + " — " + strings.t("goal_water_hint"),
        strings.t("goal_stress") + " — " + strings.t("goal_stress_hint"),
    ]
    buttons = []
    for rect, label, n in zip(menu_rects(3), labels, (1, 2, 3)):
        button = Button(rect, label, strings.t("slot", k=n))
        buttons.append(button)
        draw_button(surf, assets.font_s, button)
    extra = [
        Button((340, 500, 280, 52), strings.t("btn_assumptions"), "F1"),
        Button((640, 500, 280, 52), strings.t("btn_credits"), "F2"),
    ]
    for button in extra:
        draw_button(surf, assets.font_s, button)
    buttons.extend(extra)
    if assets.warnings:
        draw_text(surf, assets.font_s, strings.t("manifest_warn", msg=assets.warnings[0]), YELLOW, 40, 640)
    draw_text(surf, assets.font_s, strings.t("key_help"), (30, 30, 30), 24, 680)
    return buttons


def draw_end(surf, assets, run, holds):
    surf.fill((16, 18, 22), (0, 56, 1280, 664))
    mood = "worried"
    if holds and run.history:
        mood = final_mood(run.totals()[2])
    draw_farmer(surf, assets, mood if holds else "worried", (40, 80, 72, 80))
    title = strings.t("holds") if holds else strings.t("not_holds")
    draw_text(surf, assets.font_l, title, TITLE if not holds else (85, 255, 85), 140, 80)
    font = assets.font_s
    if holds:
        draw_text(surf, font, strings.t("final_mood_rule"), (180, 180, 180), 140, 130)
        draw_text(surf, font, strings.t("sam_%s" % mood), NAME, 140, 154)
    y = 190
    for item in run.history:
        choice = item["choice"]
        draw_text(
            surf,
            font,
            "%s  %s  %s"
            % (
                strings.t("hist_season", n=item["season"] + 1),
                strings.option_label(choice),
                strings.t(
                    "hist_score",
                    got=strings.fmt_num(item["score"]),
                    best=strings.fmt_num(item["best_score"]),
                ),
            ),
            INK,
            40,
            y,
        )
        y += 28
    if run.history:
        got, best, gap = run.totals()
        draw_text(surf, font, strings.t("total_line", got=strings.fmt_num(got), best=strings.fmt_num(best)), YELLOW, 40, y + 12)
        draw_text(surf, font, strings.t("total_gap", gap=strings.fmt_num(gap)), YELLOW, 40, y + 36)
    draw_text(surf, font, strings.t("replay_hint"), (180, 180, 180), 40, 640)
    button = Button((980, 640, 260, 56), strings.t("btn_replay"))
    draw_button(surf, font, button)
    return [button]


def draw_scroll_screen(surf, assets, title, body):
    surf.fill((16, 18, 22), (0, 56, 1280, 664))
    draw_text(surf, assets.font_m, title, PLACE, 40, 80)
    y = 130
    font = assets.font_s
    for paragraph in body.split("\n"):
        for line in wrap(font, paragraph, 1180):
            draw_text(surf, font, line, INK, 40, y)
            y += font.get_height() + 6
            if y > 620:
                break
        y += 8
    button = Button((40, 640, 240, 52), strings.t("btn_back"))
    draw_button(surf, font, button)
    return [button]


def draw_error(surf, assets, messages):
    body = "\n".join(messages)
    buttons = draw_scroll_screen(surf, assets, strings.t("error_title"), strings.t("error_hint") + "\n" + body)
    return buttons


def draw_frame(surf, assets, run, mouse, tick, error_messages):
    surf.fill((10, 10, 10))
    draw_hud(surf, assets, run)
    if run.phase == "error":
        return draw_error(surf, assets, error_messages)
    if run.phase == "title":
        return draw_title(surf, assets, run)
    if run.phase == "intro":
        return draw_intro(surf, assets, run)
    if run.phase == "ask":
        return draw_ask(surf, assets, run, mouse)
    if run.phase == "play":
        return draw_play(surf, assets, run, tick)
    if run.phase == "result":
        return draw_result(surf, assets, run)
    if run.phase == "over":
        return draw_end(surf, assets, run, False)
    if run.phase == "final":
        return draw_end(surf, assets, run, True)
    if run.phase == "assumptions":
        return draw_scroll_screen(surf, assets, strings.t("assumptions_title"), strings.t("assumptions_body"))
    if run.phase == "credits":
        text = assets.credits_text() or strings.t("credits_missing")
        text = strings.t("font_note") + "\n" + text
        return draw_scroll_screen(surf, assets, strings.t("credits_title"), text)
    return []
