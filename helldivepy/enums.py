from enum import Enum
import typing

# {"1": "race", "2": "unknown", "3": "goal", "11": "liberate", "12": "planet_index"}


class BetterEnum(Enum):
    @classmethod
    def parse(cls, value):
        try:
            return cls(value)
        except ValueError:
            return None


class CampaignTypes(BetterEnum):

    LIBERATION_DEFENSE = 0
    RECON = 1
    STORY = 2


class ValueTypes(BetterEnum):
    RACE = 1
    UNKNOWN = 2
    TARGET_COUNT = 3
    UNIT_ID = 4
    ITEM_ID = 5
    LIBERATE = 11
    PLANET = 12


class RewardTypes(BetterEnum):
    MEDALS = 1


class AssignmentTypes(BetterEnum):
    ERADICATE = 3
    LIBERATION = 11
    DEFENSE = 12
    CONTROL = 13


FactionType = typing.Literal["Humans", "Terminids", "Automaton", "Illuminate"]
