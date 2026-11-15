"""Widgets, text wrapping, and click rectangles."""

from __future__ import annotations

import pygame

import strings

W = 1280
H = 720

INK = (255, 255, 255)
EDGE = (28, 28, 28)
PANEL = (59, 59, 59)
PANEL2 = (85, 85, 85)
OK = (45, 106, 30)
BAD = (122, 31, 31)
XP = (124, 252, 0)
NAME = (255, 170, 0)
PLACE = (85, 255, 255)
TITLE = (255, 85, 85)
YELLOW = (255, 255, 85)
SKY = (126, 192, 238)
SKY_HOT = (90, 70, 40)
DIRT = (122, 82, 48)
DRY = (168, 131, 79)
CRACK = (58, 36, 22)
GRASS = (95, 184, 58)
SUN = (255, 225, 77)
SUN_HOT = (255, 122, 26)


class Button:
    def __init__(self, rect, label, key_hint="", style="normal"):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.key_hint = key_hint
        self.style = style
        self.enabled = True

    def hit(self, pos):
        return self.enabled and self.rect.collidepoint(pos)


def wrap(font, text, width):
    words = str(text).split()
    if not words:
        return [""]
    lines = []
    cur = words[0]
    for word in words[1:]:
        trial = cur + " " + word
        if font.size(trial)[0] <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def draw_text(surf, font, text, color, x, y):
    image = font.render(str(text), True, color)
    surf.blit(image, (x, y))
    return image.get_width(), image.get_height()


def draw_wrapped(surf, font, text, color, rect, line_gap=4):
    rect = pygame.Rect(rect)
    y = rect.y
    height = font.get_height()
    for line in wrap(font, text, rect.w):
        if y + height > rect.bottom:
            break
        draw_text(surf, font, line, color, rect.x, y)
        y += height + line_gap
    return y


def draw_panel(surf, rect, fill=PANEL):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surf, fill, rect)
    pygame.draw.rect(surf, EDGE, rect, 4)


def draw_button(surf, font, button):
    fill = PANEL
    if button.style == "ok":
        fill = OK
    elif button.style == "bad":
        fill = BAD
    elif button.style == "best":
        fill = (36, 70, 36)
    draw_panel(surf, button.rect, fill)
    if button.style == "best":
        pygame.draw.rect(surf, (85, 255, 85), button.rect, 4)
    inner = button.rect.inflate(-16, -12)
    if button.key_hint:
        draw_text(surf, font, button.key_hint, (170, 170, 170), inner.x, inner.y)
        body = pygame.Rect(inner.x, inner.y + font.get_height() + 4, inner.w, inner.h)
    else:
        body = inner
    draw_wrapped(surf, font, button.label, INK, body, 2)


def option_rects(count):
    cols = 2
    rows = (count + 1) // 2
    gap = 8
    top = 470
    left = 24
    width = 500
    height = 70 if rows <= 2 else 58
    rects = []
    for i in range(count):
        c = i % cols
        r = i // cols
        rects.append(pygame.Rect(left + c * (width + gap), top + r * (height + gap), width, height))
    return rects


def menu_rects(count):
    rects = []
    y = 220
    for _ in range(count):
        rects.append(pygame.Rect(340, y, 600, 72))
        y += 84
    return rects


def heat_rect():
    return pygame.Rect(920, 150, 240, 240)


def heat_cell(mouse):
    grid = heat_rect()
    if not grid.collidepoint(mouse):
        return None
    cell = grid.w // 20
    col = (mouse[0] - grid.x) // cell
    row = (mouse[1] - grid.y) // cell
    if col < 0 or row < 0 or col > 19 or row > 19:
        return None
    return int(row), int(col)


def tank_rect():
    return pygame.Rect(820, 150, 36, 180)
