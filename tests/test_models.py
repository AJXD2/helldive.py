"""Tests for helldivepy models."""

from datetime import datetime

from helldivepy.enums import (
    Factions,
    RegionSize,
    TaskType,
    TaskValueType,
)
from helldivepy.models import (
    Assignment,
    Biome,
    Campaign,
    Dispatch,
    Event,
    Hazard,
    HDMLString,
    HomeWorld,
    Planet,
    Position,
    Region,
    Reward,
    Statistics,
    Task,
    War,
)

# ---------------------------------------------------------------------------
# HDMLString
# ---------------------------------------------------------------------------


class TestHDMLString:
    def test_str(self) -> None:
        s = HDMLString("hello")
        assert str(s) == "hello"

    def test_repr(self) -> None:
        s = HDMLString("hello")
        assert repr(s) == "HDMLString('hello')"

    def test_to_md_inline_styles(self) -> None:
        s = HDMLString("<i=1>Alert</i> and <i=3>Bold</i>")
        result = s.to_md()
        assert '<span style="color: yellow">Alert</span>' in result
        assert '<span style="font-weight: bold">Bold</span>' in result

    def test_to_md_css_classes(self) -> None:
        s = HDMLString("<i=1>Alert</i> and <i=3>Bold</i>")
        result = s.to_md(use_classes=True)
        assert '<span class="text-yellow">Alert</span>' in result
        assert '<span class="text-bold">Bold</span>' in result

    def test_pydantic_field_accepts_str(self) -> None:
        d = Dispatch.model_validate(
            {"id": 1, "published": "2026-01-01", "type": 0, "message": "<i=1>Hi</i>"}
        )
        assert isinstance(d.message, HDMLString)
        assert str(d.message) == "<i=1>Hi</i>"


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


class TestStatistics:
    def test_camel_to_snake(self, raw_statistics: dict) -> None:  # type: ignore[type-arg]
        s = Statistics.model_validate(raw_statistics)
        assert s.missions_won == 100
        assert s.mission_success_rate == 90.0
        assert s.player_count == 5000

    def test_accuracy_int_coerced_to_float(self, raw_statistics: dict) -> None:  # type: ignore[type-arg]
        s = Statistics.model_validate(raw_statistics)
        assert isinstance(s.accuracy, float)


# ---------------------------------------------------------------------------
# War
# ---------------------------------------------------------------------------


class TestWar:
    def test_timestamps_parsed_as_datetime(self) -> None:
        w = War.model_validate(
            {
                "started": "2024-01-23T20:05:13Z",
                "ended": "2099-01-01T00:00:00Z",
                "now": "2026-03-12T10:00:00Z",
                "clientVersion": "1.0.0",
                "factions": ["Humans", "Terminids"],
                "impactMultiplier": 0.02,
                "statistics": {
                    "missionsWon": 0,
                    "missionsLost": 0,
                    "missionTime": 0,
                    "terminidKills": 0,
                    "automatonKills": 0,
                    "illuminateKills": 0,
                    "bulletsFired": 0,
                    "bulletsHit": 0,
                    "timePlayed": 0,
                    "deaths": 0,
                    "revives": 0,
                    "friendlies": 0,
                    "missionSuccessRate": 0,
                    "accuracy": 0,
                    "playerCount": 0,
                },
            }
        )
        assert isinstance(w.started, datetime)
        assert w.started.year == 2024
        assert w.started.tzinfo is not None


# ---------------------------------------------------------------------------
# Region
# ---------------------------------------------------------------------------


class TestRegion:
    def test_full_region(self, raw_region: dict) -> None:  # type: ignore[type-arg]
        r = Region.model_validate(raw_region)
        assert r.name == "TEST REGION"
        assert r.health == 500000
        assert r.max_health == 1000000
        assert r.size == RegionSize.City
        assert r.regen_per_second == 1.5
        assert r.is_available is True

    def test_nullable_fields_accept_none(self, raw_region_nullable: dict) -> None:  # type: ignore[type-arg]
        r = Region.model_validate(raw_region_nullable)
        assert r.name is None
        assert r.description is None
        assert r.health is None
        assert r.regen_per_second is None
        assert r.availability_factor is None
        assert r.size == RegionSize.MegaCity


# ---------------------------------------------------------------------------
# Planet
# ---------------------------------------------------------------------------


class TestPlanet:
    def test_basic_fields(self, raw_planet: dict) -> None:  # type: ignore[type-arg]
        p = Planet.model_validate(raw_planet)
        assert p.index == 42
        assert p.name == "HELLMIRE"
        assert p.max_health == 1000000  # camelCase alias
        assert p.health == 750000
        assert p.current_owner == Factions.Terminids
        assert p.initial_owner == Factions.Humans
        assert p.disabled is False
        assert p.event is None

    def test_nested_models(self, raw_planet: dict) -> None:  # type: ignore[type-arg]
        p = Planet.model_validate(raw_planet)
        assert isinstance(p.biome, Biome)
        assert isinstance(p.position, Position)
        assert isinstance(p.statistics, Statistics)
        assert len(p.hazards) == 1
        assert isinstance(p.hazards[0], Hazard)

    def test_waypoints_and_attacking(self, raw_planet: dict) -> None:  # type: ignore[type-arg]
        p = Planet.model_validate(raw_planet)
        assert p.waypoints == [10, 20]
        assert p.attacking == [15]

    def test_event_parsed_when_present(self, raw_planet_with_event: dict) -> None:  # type: ignore[type-arg]
        p = Planet.model_validate(raw_planet_with_event)
        assert p.event is not None
        assert isinstance(p.event, Event)
        assert p.event.faction == Factions.Automaton
        assert p.event.health == 300000
        assert p.event.max_health == 500000
        assert isinstance(p.event.start_time, datetime)
        assert p.event.joint_operation_ids == [1, 2]


# ---------------------------------------------------------------------------
# Campaign
# ---------------------------------------------------------------------------


class TestCampaign:
    def test_embedded_planet(self, raw_planet: dict) -> None:  # type: ignore[type-arg]
        c = Campaign.model_validate(
            {"id": 1, "planet": raw_planet, "type": 0, "count": 3, "faction": "Humans"}
        )
        assert isinstance(c.planet, Planet)
        assert c.planet.name == "HELLMIRE"
        assert c.faction == Factions.Humans


# ---------------------------------------------------------------------------
# HomeWorld
# ---------------------------------------------------------------------------


class TestHomeWorld:
    def test_parse(self) -> None:
        hw = HomeWorld.model_validate({"race": 2, "planetIndices": [10, 20, 30]})
        assert hw.race == 2
        assert hw.planet_indices == [10, 20, 30]


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------


class TestTask:
    def test_values_zipped_to_dict(self, raw_kill_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_kill_task)
        assert isinstance(t.values, dict)
        assert t.values[TaskValueType.RACE] == 3
        assert t.values[TaskValueType.GOAL] == 100000

    def test_unknown_value_types_kept_as_int(self, raw_kill_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_kill_task)
        # valueTypes 2, 5, 6, 8, 9 are not in TaskValueType
        assert 2 in t.values
        assert 5 in t.values

    def test_task_type_resolved_to_enum(self, raw_kill_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_kill_task)
        assert t.type == TaskType.ERADICATE

    def test_task_type_unknown_kept_as_int(self) -> None:
        t = Task.model_validate({"type": 99, "values": [], "valueTypes": []})
        assert t.type == 99

    def test_goal_property(self, raw_kill_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_kill_task)
        assert t.goal == 100000

    def test_goal_none_when_no_goal_value(self) -> None:
        t = Task.model_validate({"type": 99, "values": [7], "valueTypes": [1]})
        assert t.goal is None

    def test_progress_perc(self, raw_kill_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_kill_task)
        t.progress = 25000
        assert t.progress_perc == 25.0

    def test_progress_perc_capped_at_100(self, raw_kill_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_kill_task)
        t.progress = 999999999
        assert t.progress_perc == 100.0

    def test_progress_perc_none_without_goal(self) -> None:
        t = Task.model_validate({"type": 99, "values": [1], "valueTypes": [1]})
        t.progress = 100
        assert t.progress_perc is None

    def test_is_liberation_task_true(self, raw_liberate_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_liberate_task)
        assert t.is_liberation_task is True

    def test_is_liberation_task_false(self, raw_kill_task: dict) -> None:  # type: ignore[type-arg]
        t = Task.model_validate(raw_kill_task)
        assert t.is_liberation_task is False


# ---------------------------------------------------------------------------
# Assignment
# ---------------------------------------------------------------------------


class TestAssignment:
    def test_progress_injected_into_tasks(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        a = Assignment.model_validate(raw_assignment)
        assert a.tasks[0].progress == 50000  # kill task
        assert a.tasks[1].progress == 0  # liberate task

    def test_progress_zero_when_out_of_bounds(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        # Only 1 progress value but 2 tasks
        raw_assignment["progress"] = [12345]
        a = Assignment.model_validate(raw_assignment)
        assert a.tasks[0].progress == 12345
        assert a.tasks[1].progress == 0

    def test_description_nullable(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        a = Assignment.model_validate(raw_assignment)
        assert a.description is None

    def test_reward_nullable(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        raw_assignment["reward"] = None
        a = Assignment.model_validate(raw_assignment)
        assert a.reward is None

    def test_expiration_is_datetime(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        a = Assignment.model_validate(raw_assignment)
        assert isinstance(a.expiration, datetime)
        assert a.expiration.tzinfo is not None

    def test_tasks_parsed(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        a = Assignment.model_validate(raw_assignment)
        assert len(a.tasks) == 2
        assert a.tasks[0].type == TaskType.ERADICATE
        assert a.tasks[1].type == TaskType.LIBERATION

    def test_kill_task_progress_perc(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        a = Assignment.model_validate(raw_assignment)
        kill_task = a.tasks[0]
        assert kill_task.goal == 100000
        assert kill_task.progress_perc == 50.0

    def test_reward_parsed(self, raw_assignment: dict) -> None:  # type: ignore[type-arg]
        a = Assignment.model_validate(raw_assignment)
        assert isinstance(a.reward, Reward)
        assert a.reward.type == 1
        assert a.reward.amount == 50
