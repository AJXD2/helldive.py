from datetime import datetime

from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler
from pydantic.alias_generators import to_camel
from pydantic_core import core_schema

from helldivepy.enums import DispatchType, Factions, RegionSize


# Convert snake_case to camelCase for JSON serialization.
# This removes adding an extra step to the request methods while enforcing standards.
class APIModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


# Helper class for the game markup lang HDML
class HDMLString:
    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"HDMLString({self.content!r})"

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type, handler: GetCoreSchemaHandler
    ):
        # source_type and handler are required by the signature but not used
        return core_schema.no_info_plain_validator_function(
            lambda v: cls(v) if isinstance(v, str) else v,
            serialization=core_schema.to_string_ser_schema(),
        )

    def to_md(self, use_classes: bool = False) -> str:
        if use_classes:
            return (
                self.content.replace("</i>", "</span>")
                .replace("<i=1>", '<span class="text-yellow">')
                .replace("<i=3>", '<span class="text-bold">')
            )
        return (
            self.content.replace("</i>", "</span>")
            .replace("<i=1>", '<span style="color: yellow">')
            .replace("<i=3>", '<span style="font-weight: bold">')
        )


class Statistics(APIModel):
    missions_won: int
    missions_lost: int
    mission_time: int
    terminid_kills: int
    automaton_kills: int
    illuminate_kills: int
    bullets_fired: int
    bullets_hit: int
    time_played: int
    deaths: int
    revives: int
    friendlies: int
    mission_success_rate: float
    accuracy: float
    player_count: int


class War(APIModel):
    started: datetime
    ended: datetime
    now: datetime
    client_version: str
    factions: list[str]
    impact_multiplier: float
    statistics: Statistics


class Dispatch(APIModel):
    id: int
    published: str
    type: DispatchType
    message: HDMLString


class Region(APIModel):
    id: int
    hash: int
    name: str | None = None
    description: str | None = None
    health: int | None = None
    max_health: int
    size: RegionSize
    regen_per_second: float | None = None
    # Unknown purpose
    availability_factor: float | None = None
    is_available: bool
    players: int


class Biome(APIModel):
    name: str
    description: str


class Hazard(APIModel):
    name: str
    description: str


class Position(APIModel):
    x: float
    y: float


class Event(APIModel):
    id: int
    event_type: int
    faction: Factions
    health: int
    max_health: int
    start_time: datetime
    end_time: datetime
    campaign_id: int
    joint_operation_ids: list[int]


class Planet(APIModel):
    index: int
    name: str
    sector: str
    biome: Biome
    hazards: list[Hazard]
    hash: int
    position: Position
    waypoints: list[int]
    max_health: int
    health: int
    disabled: bool
    initial_owner: Factions
    current_owner: Factions
    regen_per_second: float
    event: Event | None = None
    statistics: Statistics
    attacking: list[int]
    regions: list[Region]


class Campaign(APIModel):
    id: int
    planet: Planet
    type: int
    count: int
    faction: Factions


class HomeWorld(APIModel):
    race: int
    planet_indices: list[int]
