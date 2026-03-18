import enum


class Factions(enum.Enum):
    Humans = "Humans"
    Terminids = "Terminids"
    Automaton = "Automaton"
    Illuminate = "Illuminate"


class DispatchType(enum.IntEnum):
    NORMAL = 0


class RegionSize(enum.Enum):
    Settlement = "Settlement"
    Town = "Town"
    City = "City"
    MegaCity = "MegaCity"


class TaskType(enum.IntEnum):
    """Community-reverse-engineered task type codes. May be incomplete."""

    EXTRACT = 2
    ERADICATE = 3
    COMPLETE_MISSIONS = 7
    COMPLETE_OPERATIONS = 9
    LIBERATION = 11
    DEFENSE = 12
    CONTROL = 13
    EXPAND = 15


class TaskValueType(enum.IntEnum):
    """
    Community-reverse-engineered value type codes for Task.values. May be incomplete.
    """

    RACE = 1
    UNKNOWN = 2
    GOAL = 3
    UNIT_ID = 4
    ITEM_ID = 5
    DIFFICULTY = 9
    LOCATION_TYPE = 11
    LOCATION_INDEX = 12


class CampaignType(enum.IntEnum):
    """
    Community-reverse-engineered value type codes for Campaign.type. May be incomplete.
    """

    LIBERATION = 0
    RECON = 1
    STORY = 2
