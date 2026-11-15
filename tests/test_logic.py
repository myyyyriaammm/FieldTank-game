"""Logic tests. The fixture is test data only and must never be loaded by the game."""

import json
from pathlib import Path

import pytest

from game.data import DataError, assert_not_fixture, load_scenes, validate_scenes
from game.state import (
    Run,
    filter_choices,
    heart_loss,
    lesson_numbers,
    score_choice,
    shuffle_options,
)

FIXTURE = Path(__file__).with_name("fixture_scenes.json")


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_fixture_comment_marks_test_data_only():
    raw = FIXTURE.read_text(encoding="utf-8")
    assert "TEST DATA ONLY" in raw


def test_load_scenes_accepts_fixture_schema_via_explicit_path_guard():
    data = load_fixture()
    assert validate_scenes(data) == []
    with pytest.raises(DataError):
        load_scenes(FIXTURE)
    with pytest.raises(DataError):
        assert_not_fixture(FIXTURE)


def test_game_source_does_not_name_the_fixture():
    root = Path(__file__).resolve().parents[1]
    text = (root / "game" / "data.py").read_text(encoding="utf-8")
    assert "fixture_scenes.json" not in text


def test_validate_rejects_bad_shape():
    errors = validate_scenes({"farmer": "A"})
    assert errors
    errors = validate_scenes(
        {
            "farmer": "A",
            "lat": 1,
            "capacity_mm": 10,
            "scenes": [],
        }
    )
    assert any("expected 5 scenes" in e for e in errors)


def test_filter_by_question_type():
    data = load_fixture()
    scene = data["scenes"][0]
    dry = filter_choices(scene, 0)
    assert len(dry) == 3
    assert all(c["irrigate"] is False for c in dry)
    maize = filter_choices(scene, 1)
    assert len(maize) == 2
    assert {c["crop"] for c in maize} == {"Maïs"}
    wet = filter_choices(scene, 2)
    assert len(wet) == 3
    assert all(c["irrigate"] is True for c in wet)
    soy = filter_choices(scene, 3)
    assert len(soy) == 2
    assert {c["crop"] for c in soy} == {"Soja"}
    free = filter_choices(scene, 4)
    assert len(free) == 6


def test_scoring_formula():
    choice = {"yield_pct": 80, "irrigation_mm": 25, "stress_days": 4}
    assert score_choice(choice, "yield") == 80
    assert score_choice(choice, "water") == 80 - 0.4 * 25
    assert score_choice(choice, "stress") == 80 - 1.5 * 4


def test_heart_loss_from_gap():
    assert heart_loss(0) == 0
    assert heart_loss(10) == 0
    assert heart_loss(10.5) == 1
    assert heart_loss(11) == 1
    assert heart_loss(30) == 1
    assert heart_loss(30.1) == 2
    assert heart_loss(31) == 2


def test_shuffle_is_stable_permutation():
    data = load_fixture()
    raw = filter_choices(data["scenes"][4], 4)
    a = shuffle_options(raw, 4, seed=20240701)
    b = shuffle_options(raw, 4, seed=20240701)
    assert [c["crop"] + str(c["irrigate"]) for c in a] == [
        c["crop"] + str(c["irrigate"]) for c in b
    ]
    assert sorted(id(c) for c in raw) != sorted(id(c) for c in a) or len(a) == 6
    keys = {(c["crop"], c["irrigate"]) for c in a}
    assert keys == {(c["crop"], c["irrigate"]) for c in raw}


def test_run_hearts_follow_score_gap():
    data = load_fixture()
    run = Run(data, None)
    run.set_goal("yield")
    run.phase = "ask"
    idx = next(i for i, c in enumerate(run.offered) if c["crop"] == "Maïs")
    run.pick(idx)
    run.finish_play()
    assert run.history[-1]["gap"] == 20
    assert run.history[-1]["hearts_lost"] == 1
    assert run.hearts == 4
    run2 = Run(data, None)
    run2.set_goal("yield")
    run2.phase = "ask"
    idx = next(i for i, c in enumerate(run2.offered) if c["crop"] == "Sorgho")
    run2.pick(idx)
    run2.finish_play()
    assert run2.history[-1]["gap"] == 0
    assert run2.hearts == 5


def test_scene1_water_goal_gap():
    data = load_fixture()
    run = Run(data, None)
    run.season = 1
    run.set_goal("water")
    run.season = 1
    run._prepare_season()
    idx = next(i for i, c in enumerate(run.offered) if c["irrigate"] is True)
    run.phase = "ask"
    run.pick(idx)
    run.finish_play()
    assert run.history[-1]["gap"] == 15
    assert run.hearts == 4


def test_lesson_numbers_from_fixture():
    data = load_fixture()
    facts = lesson_numbers(data["scenes"][0], "yield")
    assert facts["crop"] == "Maïs"
    assert facts["yield_delta"] == 5
    assert facts["stress_saved"] == 10
    assert facts["spread"] == 25
    assert facts["best_score"] == 65
    assert facts["worst_score"] == 40
