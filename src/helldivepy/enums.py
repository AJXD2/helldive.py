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
