import enum


class Factions(enum.Enum):
    """Known factions in the Helldivers 2 universe."""

    Humans = "Humans"
    """Super Earth and its Helldivers."""
    Terminids = "Terminids"
    """Bug-like creatures spreading across the galaxy."""
    Automaton = "Automaton"
    """Robotic enemies fighting for machine dominion."""
    Illuminate = "Illuminate"
    """Ancient alien civilization returned from beyond the Galactic Barrier."""


class DispatchType(enum.IntEnum):
    """Category of a dispatch message."""

    NORMAL = 0
    """Standard high-command communication."""


class RegionSize(enum.Enum):
    """Size classification of a planetary region."""

    Settlement = "Settlement"
    Town = "Town"
    City = "City"
    MegaCity = "MegaCity"


class TaskType(enum.IntEnum):
    """Community-reverse-engineered task type codes. May be incomplete."""

    EXTRACT = 2
    """Extract samples or personnel."""
    ERADICATE = 3
    """Kill a target number of enemies."""
    COMPLETE_MISSIONS = 7
    """Complete a number of missions."""
    COMPLETE_OPERATIONS = 9
    """Complete a number of operations."""
    LIBERATION = 11
    """Liberate a planet."""
    DEFENSE = 12
    """Defend a planet from invasion."""
    CONTROL = 13
    """Maintain control of a planet."""
    EXPAND = 15
    """Expand the front line."""


class TaskValueType(enum.IntEnum):
    """
    Community-reverse-engineered value type codes for Task.values. May be incomplete.
    """

    RACE = 1
    """Target faction identifier."""
    UNKNOWN = 2
    GOAL = 3
    """Target quantity to reach."""
    UNIT_ID = 4
    """Specific enemy unit type."""
    ITEM_ID = 5
    """Specific item type."""
    DIFFICULTY = 9
    """Required mission difficulty."""
    LOCATION_TYPE = 11
    """Type of target location."""
    LOCATION_INDEX = 12
    """Planet index of the target location."""


class CampaignType(enum.IntEnum):
    """Community-reverse-engineered campaign type codes. May be incomplete."""

    LIBERATION = 0
    """Active liberation of an enemy-controlled planet."""
    RECON = 1
    """Reconnaissance operation."""
    STORY = 2
    """Story-driven campaign mission."""
