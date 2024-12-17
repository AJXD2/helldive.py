from enum import Enum
import typing


class BetterEnum(Enum):
    @classmethod
    def parse(cls, value):
        try:
            return cls(value)
        except ValueError:
            return None


class ValueTypes(BetterEnum):
    """Types of values returned from the major order/assignments endpoint."""

    RACE = 1
    UNKNOWN = 2
    TARGET_COUNT = 3
    UNIT_ID = 4
    ITEM_ID = 5
    LIBERATE = 11
    PLANET = 12


class RewardTypes(BetterEnum):
    """Types of rewards given out by the major order/assignments."""

    MEDALS = 1


class AssignmentTypes(BetterEnum):
    """Types of assignments."""

    ERADICATE = 3
    LIBERATION = 11
    DEFENSE = 12
    CONTROL = 13


FactionType = typing.Literal["Humans", "Terminids", "Automaton", "Illuminate"]
