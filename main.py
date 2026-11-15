"""FieldTank. Run with: python main.py"""

from __future__ import annotations

import sys
from pathlib import Path

import pygame

from game.assets import AssetBank
from game.data import DataError, load_game_data
from game.render import draw_frame
from game.state import Run
from game.ui import H, W

GOALS = ("yield", "water", "stress")


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent


def fit_scale(window_size):
    sw, sh = window_size
    scale = min(sw // W, sh // H)
    if scale < 1:
        scale = 1
    ox = (sw - W * scale) // 2
    oy = (sh - H * scale) // 2
    return scale, ox, oy


def to_logical(pos, scale, offset):
    x = (pos[0] - offset[0]) // scale
    y = (pos[1] - offset[1]) // scale
    return int(x), int(y)


def main():
    pygame.init()
    pygame.display.set_caption("FieldTank")
    window = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    fullscreen = False
    logical = pygame.Surface((W, H))
    clock = pygame.time.Clock()
    root = app_root()
    assets = AssetBank(root / "assets")
    error_messages = []
    try:
        data, lst, _scene_path, _lst_path = load_game_data(root)
        run = Run(data, lst)
    except DataError as exc:
        run = Run(
            {
                "farmer": "",
                "lat": 0,
                "capacity_mm": 0,
                "scenes": [],
            },
            None,
        )
        run.phase = "error"
        error_messages = exc.messages
    mouse = (0, 0)
    tick = 0
    buttons = []
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        tick = (tick + 1) % 100000
        scale, ox, oy = fit_scale(window.get_size())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                window = pygame.display.set_mode((max(W, event.w), max(H, event.h)), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((W, H), pygame.RESIZABLE)
                elif event.key == pygame.K_F1 and run.phase != "error":
                    run.open_overlay("assumptions")
                elif event.key == pygame.K_F2 and run.phase != "error":
                    run.open_overlay("credits")
                elif event.key == pygame.K_SPACE and run.phase == "play":
                    run.skip_play()
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    activate(run, buttons, 0 if not buttons else None, enter=True)
                elif pygame.K_1 <= event.key <= pygame.K_6:
                    index = event.key - pygame.K_1
                    on_key(run, index)
            elif event.type == pygame.MOUSEMOTION:
                mouse = to_logical(event.pos, scale, (ox, oy))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = to_logical(event.pos, scale, (ox, oy))
                for i, button in enumerate(buttons):
                    if button.hit(mouse):
                        activate(run, buttons, i, enter=False)
                        break
        if run.phase == "play":
            run.update_play(dt)
        buttons = draw_frame(logical, assets, run, mouse, tick, error_messages)
        scaled = pygame.transform.scale(logical, (W * scale, H * scale))
        window.fill((0, 0, 0))
        window.blit(scaled, (ox, oy))
        pygame.display.flip()
    pygame.quit()


def on_key(run, index):
    if run.phase == "title" and index < 3:
        run.set_goal(GOALS[index])
    elif run.phase == "ask":
        run.pick(index)


def activate(run, buttons, index, enter):
    if run.phase == "title":
        if enter:
            return
        if index is None or index >= len(buttons):
            return
        if index < 3:
            run.set_goal(GOALS[index])
        elif index == 3:
            run.open_overlay("assumptions")
        elif index == 4:
            run.open_overlay("credits")
        return
    if run.phase == "intro":
        run.phase = "ask"
        return
    if run.phase == "ask" and not enter and index is not None:
        run.pick(index)
        return
    if run.phase == "result" and (enter or index is not None):
        run.continue_after_result()
        return
    if run.phase in ("over", "final") and (enter or index is not None):
        run.reset()
        return
    if run.phase in ("assumptions", "credits") and (enter or index is not None):
        run.close_overlay()
        return
    if run.phase == "error" and (enter or index is not None):
        pygame.event.post(pygame.event.Event(pygame.QUIT))


if __name__ == "__main__":
    main()
