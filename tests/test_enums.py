"""Tests for helldivepy enums."""

import pytest

from helldivepy.enums import (
    CampaignType,
    DispatchType,
    Factions,
    RegionSize,
    TaskType,
    TaskValueType,
)


class TestFactions:
    def test_values(self) -> None:
        assert Factions.Humans.value == "Humans"
        assert Factions.Terminids.value == "Terminids"
        assert Factions.Automaton.value == "Automaton"
        assert Factions.Illuminate.value == "Illuminate"

    def test_from_string(self) -> None:
        assert Factions("Humans") == Factions.Humans
        assert Factions("Automaton") == Factions.Automaton
        assert Factions("Illuminate") == Factions.Illuminate

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError):
            Factions("Unknown")


class TestDispatchType:
    def test_normal_value(self) -> None:
        assert DispatchType.NORMAL == 0

    def test_from_int(self) -> None:
        assert DispatchType(0) == DispatchType.NORMAL

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError):
            DispatchType(99)


class TestRegionSize:
    def test_values(self) -> None:
        assert RegionSize.Settlement.value == "Settlement"
        assert RegionSize.Town.value == "Town"
        assert RegionSize.City.value == "City"
        assert RegionSize.MegaCity.value == "MegaCity"

    def test_from_string(self) -> None:
        assert RegionSize("City") == RegionSize.City
        assert RegionSize("MegaCity") == RegionSize.MegaCity

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError):
            RegionSize("Village")


class TestTaskType:
    def test_values(self) -> None:
        assert TaskType.EXTRACT == 2
        assert TaskType.ERADICATE == 3
        assert TaskType.COMPLETE_MISSIONS == 7
        assert TaskType.COMPLETE_OPERATIONS == 9
        assert TaskType.LIBERATION == 11
        assert TaskType.DEFENSE == 12
        assert TaskType.CONTROL == 13
        assert TaskType.EXPAND == 15

    def test_from_int(self) -> None:
        assert TaskType(3) == TaskType.ERADICATE
        assert TaskType(11) == TaskType.LIBERATION
        assert TaskType(12) == TaskType.DEFENSE

    def test_is_int_enum(self) -> None:
        assert isinstance(TaskType.ERADICATE, int)
        assert TaskType.ERADICATE == 3


class TestTaskValueType:
    def test_values(self) -> None:
        assert TaskValueType.RACE == 1
        assert TaskValueType.UNKNOWN == 2
        assert TaskValueType.GOAL == 3
        assert TaskValueType.UNIT_ID == 4
        assert TaskValueType.ITEM_ID == 5
        assert TaskValueType.DIFFICULTY == 9
        assert TaskValueType.LOCATION_TYPE == 11
        assert TaskValueType.LOCATION_INDEX == 12

    def test_from_int(self) -> None:
        assert TaskValueType(1) == TaskValueType.RACE
        assert TaskValueType(3) == TaskValueType.GOAL
        assert TaskValueType(12) == TaskValueType.LOCATION_INDEX

    def test_is_int_enum(self) -> None:
        assert isinstance(TaskValueType.GOAL, int)
        assert TaskValueType.GOAL == 3


class TestCampaignType:
    def test_values(self) -> None:
        assert CampaignType.LIBERATION == 0
        assert CampaignType.RECON == 1
        assert CampaignType.STORY == 2

    def test_from_int(self) -> None:
        assert CampaignType(0) == CampaignType.LIBERATION
        assert CampaignType(1) == CampaignType.RECON
        assert CampaignType(2) == CampaignType.STORY

    def test_is_int_enum(self) -> None:
        assert isinstance(CampaignType.LIBERATION, int)
