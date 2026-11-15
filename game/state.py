"""Question plan, scoring, hearts, and run state. Outcomes are never random."""

from __future__ import annotations

import random

from game.data import CROPS

SHUFFLE_SEED = 20240701
PLAY_SECONDS = 8.0
HEARTS_START = 5
SEASON_TOTAL = 5

# Question plan by scene index. Edit this and strings q0..q4 together.
# 0 non-irrigated crops, 1 maize irrigate yes/no, 2 irrigated crops,
# 3 soybean irrigate yes/no, 4 all six choices.
QUESTION_PLAN = (0, 1, 2, 3, 4)


def score_choice(choice, goal) -> float:
    yield_pct = float(choice["yield_pct"])
    if goal == "yield":
        return yield_pct
    if goal == "water":
        return yield_pct - 0.4 * float(choice["irrigation_mm"])
    if goal == "stress":
        return yield_pct - 1.5 * float(choice["stress_days"])
    raise ValueError("unknown goal: %s" % goal)


def heart_loss(gap: float) -> int:
    if gap <= 10:
        return 0
    if gap <= 30:
        return 1
    return 2


def filter_choices(scene, index):
    choices = scene["choices"]
    plan = QUESTION_PLAN[index]
    if plan == 0:
        return [c for c in choices if c["irrigate"] is False]
    if plan == 1:
        return [c for c in choices if c["crop"] == "Maïs"]
    if plan == 2:
        return [c for c in choices if c["irrigate"] is True]
    if plan == 3:
        return [c for c in choices if c["crop"] == "Soja"]
    if plan == 4:
        return list(choices)
    raise ValueError("scene index out of plan: %s" % index)


def shuffle_options(choices, scene_index, seed=SHUFFLE_SEED):
    items = list(choices)
    rng = random.Random(seed + scene_index * 997)
    rng.shuffle(items)
    return items


def best_of(choices, goal):
    return max(choices, key=lambda c: score_choice(c, goal))


def gap_between(chosen, best, goal) -> float:
    return score_choice(best, goal) - score_choice(chosen, goal)


def lesson_numbers(scene, goal) -> dict:
    choices = scene["choices"]
    scores = [score_choice(c, goal) for c in choices]
    best = max(scores)
    worst = min(scores)
    pair = None
    for crop in CROPS:
        wet = next(c for c in choices if c["crop"] == crop and c["irrigate"] is True)
        dry = next(c for c in choices if c["crop"] == crop and c["irrigate"] is False)
        dy = wet["yield_pct"] - dry["yield_pct"]
        saved = dry["stress_days"] - wet["stress_days"]
        rank = abs(dy)
        if pair is None or rank > pair["rank"]:
            pair = {"crop": crop, "yield_delta": dy, "stress_saved": saved, "rank": rank}
    return {
        "spread": best - worst,
        "best_score": best,
        "worst_score": worst,
        "crop": None if pair is None else pair["crop"],
        "yield_delta": None if pair is None else pair["yield_delta"],
        "stress_saved": None if pair is None else pair["stress_saved"],
    }


def curve_index(play_t, length, duration=PLAY_SECONDS) -> int:
    if length <= 1:
        return 0
    t = min(max(play_t, 0.0), duration) / duration
    return min(length - 1, int(t * length))


def curve_day(index) -> int:
    return index * 3


def soil_band(value) -> str:
    if value >= 50:
        return "ok"
    if value >= 20:
        return "dry"
    return "cracked"


def yield_kind(pct) -> str:
    if pct >= 85:
        return "good"
    if pct >= 60:
        return "mid"
    return "bad"


def live_kind(value) -> str:
    if value >= 50:
        return "good"
    if value >= 20:
        return "mid"
    return "bad"


def mood_from_gap(gap) -> str:
    if gap <= 0:
        return "happy"
    if gap <= 30:
        return "neutral"
    return "worried"


def final_mood(total_gap) -> str:
    if total_gap <= 10:
        return "happy"
    if total_gap <= 50:
        return "neutral"
    return "worried"


class Run:
    def __init__(self, data, lst, seed=SHUFFLE_SEED):
        self.data = data
        self.lst = lst
        self.seed = seed
        self.goal = None
        self.season = 0
        self.hearts = HEARTS_START
        self.completed = 0
        self.history = []
        self.phase = "title"
        self.offered = []
        self.picked = None
        self.play_t = 0.0
        self._hearts_applied = False
        self.return_phase = "title"

    def scene(self):
        return self.data["scenes"][self.season]

    def set_goal(self, goal):
        self.goal = goal
        self.phase = "intro"
        self._prepare_season()

    def _prepare_season(self):
        raw = filter_choices(self.scene(), self.season)
        self.offered = shuffle_options(raw, self.season, self.seed)
        self.picked = None
        self.play_t = 0.0
        self._hearts_applied = False

    def pick(self, index):
        if self.phase != "ask":
            return
        if index < 0 or index >= len(self.offered):
            return
        self.picked = index
        self.play_t = 0.0
        self.phase = "play"

    def chosen(self):
        return self.offered[self.picked]

    def best_offered(self):
        return best_of(self.offered, self.goal)

    def gap(self) -> float:
        return gap_between(self.chosen(), self.best_offered(), self.goal)

    def update_play(self, dt):
        if self.phase != "play":
            return
        self.play_t += dt
        if self.play_t >= PLAY_SECONDS:
            self.play_t = PLAY_SECONDS
            self.finish_play()

    def skip_play(self):
        if self.phase != "play":
            return
        self.play_t = PLAY_SECONDS
        self.finish_play()

    def finish_play(self):
        self.phase = "result"
        self.apply_hearts()

    def apply_hearts(self):
        if self._hearts_applied:
            return
        self._hearts_applied = True
        gap = self.gap()
        lost = heart_loss(gap)
        self.hearts = max(0, self.hearts - lost)
        choice = self.chosen()
        self.history.append(
            {
                "season": self.season,
                "choice": choice,
                "score": score_choice(choice, self.goal),
                "best_score": score_choice(self.best_offered(), self.goal),
                "gap": gap,
                "hearts_lost": lost,
            }
        )

    def continue_after_result(self):
        if self.phase != "result":
            return
        self.completed += 1
        if self.hearts <= 0:
            self.phase = "over"
            return
        self.season += 1
        if self.season >= len(self.data["scenes"]):
            self.phase = "final"
            return
        self.phase = "intro"
        self._prepare_season()

    def totals(self):
        got = sum(item["score"] for item in self.history)
        best = sum(item["best_score"] for item in self.history)
        return got, best, best - got

    def open_overlay(self, name):
        if self.phase not in ("assumptions", "credits"):
            self.return_phase = self.phase
        self.phase = name

    def close_overlay(self):
        self.phase = self.return_phase

    def reset(self):
        data, lst, seed = self.data, self.lst, self.seed
        self.__init__(data, lst, seed)
