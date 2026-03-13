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

    KILL_ENEMIES = 3
    SUCCEED_IN_DEFENSE = 11
    LIBERATE_PLANET = 12
    EARN_MEDALS = 13
    EXTRACT_WITH_ITEM = 14
    COMPLETE_MISSIONS = 15


class TaskValueType(enum.IntEnum):
    """
    Community-reverse-engineered value type codes for Task.values. May be incomplete.
    """

    FACTION = 1
    GOAL = 3
    PLANET_HASH = 4
    LIBERATE_STATE = 11
    PLANET_INDEX = 12
