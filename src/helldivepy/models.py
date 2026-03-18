from datetime import datetime

from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler, model_validator
from pydantic.alias_generators import to_camel
from pydantic_core import core_schema

from helldivepy.enums import (
    CampaignType,
    DispatchType,
    Factions,
    RegionSize,
    TaskType,
    TaskValueType,
)


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
    # <span ah-data='...'>[message]</span>
    message: str


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
    type: CampaignType
    count: int
    faction: Factions


class HomeWorld(APIModel):
    race: int
    planet_indices: list[int]


class Task(APIModel):
    type: TaskType | int
    # valueType → value, keyed by TaskValueType where known
    values: dict[TaskValueType | int, int]
    # Raw progress value injected by Assignment during validation
    progress: int = 0

    @model_validator(mode="before")
    @classmethod
    def zip_values(cls, data: dict[str, object]) -> dict[str, object]:
        raw_values: list[int] = data.get("values", [])  # type: ignore[assignment]
        raw_types: list[int] = data.get("valueTypes") or data.get("value_types", [])  # type: ignore[assignment]
        data["values"] = (
            {
                TaskValueType(t) if t in TaskValueType._value2member_map_ else t: v
                for t, v in zip(raw_types, raw_values, strict=False)
            }
            if raw_values and raw_types
            else {}
        )
        return data

    @property
    def goal(self) -> int | None:
        """The target value for this task (kill count, liberation %, etc.)"""
        return self.values.get(TaskValueType.GOAL)

    @property
    def progress_perc(self) -> float | None:
        """Progress towards goal as a percentage (0.0–100.0), or None if not applicable."""  # noqa: E501
        goal = self.goal
        if goal is None or goal == 0:
            return None
        return min(self.progress / goal * 100, 100.0)

    @property
    def is_liberation_task(self) -> bool:
        """Liberation/defense tasks track progress via Campaign health, not Assignment.progress."""  # noqa: E501
        return self.type in (
            TaskType.DEFENSE,
            TaskType.LIBERATION,
            TaskType.CONTROL,
            TaskType.COMPLETE_MISSIONS,
        )


class Reward(APIModel):
    type: int
    amount: int


class Assignment(APIModel):
    id: int
    progress: list[int]
    title: str
    briefing: str
    description: str | None = None
    tasks: list[Task]
    reward: Reward | None = None
    rewards: list[Reward]
    expiration: datetime
    flags: int

    @model_validator(mode="after")
    def inject_task_progress(self) -> "Assignment":
        for i, task in enumerate(self.tasks):
            task.progress = self.progress[i] if i < len(self.progress) else 0
        return self


class Cost(APIModel):
    id: str
    item_mix_id: int
    target_value: int
    current_value: float
    delta_per_second: float
    max_donation_ammount: int
    max_donation_period_seconds: int


class TacticalAction(APIModel):
    id32: int
    media_id32: int
    name: str
    description: str
    strategic_description: str
    status: int
    status_expire: datetime
    costs: list[Cost]
    effect_ids: list[int]


class SpaceStation(APIModel):
    id32: int
    planet: Planet
    election_end: datetime
    flags: int
    tactical_actions: list[TacticalAction]


class SteamNews(APIModel):
    id: str
    title: str
    url: str
    author: str
    content: str
    published_at: datetime
