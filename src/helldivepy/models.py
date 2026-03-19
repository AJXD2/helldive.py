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
    """Base model for all API responses. Handles camelCase ↔ snake_case aliasing."""

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
    """Contains statistics of missions, kills, success rate etc."""

    missions_won: int
    missions_lost: int
    mission_time: int
    """Total planetside time in seconds."""
    terminid_kills: int
    automaton_kills: int
    illuminate_kills: int
    bullets_fired: int
    """Total rounds discharged."""
    bullets_hit: int
    """Total rounds on target."""
    time_played: int
    """Total playtime including off-planet in seconds."""
    deaths: int
    """Human casualties."""
    revives: int
    friendlies: int
    """Friendly fire casualties."""
    mission_success_rate: float
    accuracy: float
    """Average marksmanship percentage."""
    player_count: int
    """Current active participants."""


class War(APIModel):
    """Global information of the ongoing war."""

    started: datetime
    ended: datetime
    now: datetime
    """Snapshot timestamp."""
    client_version: str
    """Minimum game version required."""
    factions: list[str]
    """Participating factions."""
    impact_multiplier: float
    """Mission impact calculation factor."""
    statistics: Statistics
    """Aggregated warfare metrics."""


class Dispatch(APIModel):
    """Communications from high command regarding war status updates."""

    id: int
    published: datetime
    type: DispatchType
    """Dispatch category."""
    message: str
    """
    Dispatch content. Contains HTML span markup: <span data-ah='...'>[text]</span>.
    """


class Region(APIModel):
    """Planetary subdivision. Some fields may be absent when the region is inactive."""

    id: int
    hash: int
    """ArrowHead internal hash."""
    name: str | None = None
    description: str | None = None
    health: int | None = None
    """Current durability."""
    max_health: int
    """Maximum durability capacity."""
    size: RegionSize
    """Settlement/Town/City/MegaCity classification."""
    regen_per_second: float | None = None
    """Autonomous regeneration rate."""
    availability_factor: float | None = None
    """Operational parameter (unknown purpose)."""
    is_available: bool
    """Whether the region is currently playable."""
    players: int
    """Active combatants in this region."""


class Biome(APIModel):
    """Environmental classification system for planetary surfaces."""

    name: str
    description: str


class Hazard(APIModel):
    """Environmental threat present on a planet."""

    name: str
    description: str


class Position(APIModel):
    """Coordinate on the galactic war map."""

    x: float
    """Horizontal coordinate."""
    y: float
    """Vertical coordinate."""


class Event(APIModel):
    """Active planetary occurrence with temporal boundaries (e.g. a defense event)."""

    id: int
    event_type: int
    """Occurrence category."""
    faction: Factions
    """Initiating faction."""
    health: int
    """Current durability snapshot."""
    max_health: int
    """Peak durability capacity."""
    start_time: datetime
    end_time: datetime
    campaign_id: int
    """Associated campaign reference."""
    joint_operation_ids: list[int]
    """Connected operation references."""


class Planet(APIModel):
    """Comprehensive planetary data integrating all available information."""

    index: int
    """ArrowHead planet identifier."""
    name: str
    sector: str
    """Geographic sector classification."""
    biome: Biome
    hazards: list[Hazard]
    hash: int
    """ArrowHead internal identifier."""
    position: Position
    """Map coordinates."""
    waypoints: list[int]
    """Connected planet indices."""
    max_health: int
    """Liberation capacity."""
    health: int
    """Current liberation status."""
    disabled: bool
    """Whether the planet is currently inactive."""
    initial_owner: Factions
    current_owner: Factions
    regen_per_second: float
    """Uncontested enemy regeneration rate."""
    event: Event | None = None
    """Active occurrence, if any."""
    statistics: Statistics
    """Planetary warfare metrics."""
    attacking: list[int]
    """Target planet indices this planet is attacking."""
    regions: list[Region]
    """Subdivisions with individual health and availability status."""


class Campaign(APIModel):
    """Ongoing planetary warfare operation."""

    id: int
    planet: Planet
    """Theater of operations."""
    type: CampaignType
    """Operation classification."""
    count: int
    """Historical occurrence count for this planet."""
    faction: Factions
    """Enemy faction being fought."""


class HomeWorld(APIModel):
    """Factional territorial origins."""

    race: int
    """Faction identifier."""
    planet_indices: list[int]
    """Possessed world identifiers."""


class Task(APIModel):
    """Constituent objective within an assignment requiring completion.

    Note: `type` and the keys of `values` are community-reverse-engineered
    (TaskType, TaskValueType) and may be incomplete. Unknown values fall back to int.
    """

    type: TaskType | int
    """Objective classification (community-reverse-engineered, may be incomplete)."""
    values: dict[TaskValueType | int, int]
    """
    Parsed valueType → value mapping. Keys are TaskValueType where known, else raw int.
    """
    progress: int = 0
    """Raw progress value injected by Assignment during validation."""

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
    """Completion incentive for an assignment."""

    type: int
    """Reward classification (medals, credits, etc.)."""
    amount: int
    """Compensation quantity."""


class Assignment(APIModel):
    """Directive issued to Helldivers by high command (a.k.a. Major Order)."""

    id: int
    progress: list[int]
    """Per-task advancement values; injected into each Task during validation."""
    title: str
    briefing: str
    description: str | None = None
    tasks: list[Task]
    reward: Reward | None = None
    """Primary reward (deprecated in favour of rewards)."""
    rewards: list[Reward]
    expiration: datetime
    flags: int

    @model_validator(mode="after")
    def inject_task_progress(self) -> "Assignment":
        for i, task in enumerate(self.tasks):
            task.progress = self.progress[i] if i < len(self.progress) else 0
        return self


class Cost(APIModel):
    """Resource requirement for activating a tactical action."""

    id: str
    item_mix_id: int
    """Resource classification identifier."""
    target_value: int
    """Required accumulation to activate the action."""
    current_value: float
    """Present accumulation."""
    delta_per_second: float
    """Accumulation rate."""
    max_donation_ammount: int
    """Individual contribution ceiling. Note: 'ammount' is an upstream API typo."""
    max_donation_period_seconds: int
    """Contribution window duration in seconds."""


class TacticalAction(APIModel):
    """Strategic capability deployable by a space station."""

    id32: int
    """Action identifier (32-bit ArrowHead ID)."""
    media_id32: int
    """Associated media asset reference."""
    name: str
    description: str
    """Functional overview of the action."""
    strategic_description: str
    """Military context and in-game effects."""
    status: int
    """Current operational state."""
    status_expire: datetime
    """Timestamp when the current status transitions."""
    costs: list[Cost]
    """Resource expenditures required to activate."""
    effect_ids: list[int]
    """References to gameplay consequence definitions."""


class SpaceStation(APIModel):
    """Orbital democracy platform supporting humanity's war effort."""

    id32: int
    """Station identifier (32-bit ArrowHead ID)."""
    planet: Planet
    """Planet the station is currently orbiting."""
    election_end: datetime
    """Timestamp when the next destination vote concludes."""
    flags: int
    """Configuration parameters."""
    tactical_actions: list[TacticalAction]
    """Available operations that Helldivers can collectively fund and activate."""


class SteamNews(APIModel):
    """Steam news article associated with the game."""

    id: str
    title: str
    url: str
    author: str
    content: str
    published_at: datetime
