from pydantic import BaseModel, Field
from datetime import datetime
import typing
import helldivepy.enums as enums
import helldivepy.utils as utils


class APIURLConfiguration(BaseModel):
    diveharder: str
    community: str


class Statistics(BaseModel):
    """The statistics of a player."""

    missions_won: int = Field(alias="missionsWon")
    missions_lost: int = Field(alias="missionsLost")
    mission_time: int = Field(alias="missionTime")
    terminid_kills: int = Field(alias="terminidKills")
    automaton_kills: int = Field(alias="automatonKills")
    illuminate_kills: int = Field(alias="illuminateKills")
    bullets_fired: int = Field(alias="bulletsFired")
    bullets_hit: int = Field(alias="bulletsHit")
    time_played: int = Field(alias="timePlayed")
    deaths: int
    revives: int
    friendlies: int
    mission_success_rate: float = Field(alias="missionSuccessRate")
    accuracy: int
    player_count: int = Field(alias="playerCount")


class WarInfo(BaseModel):
    """The information about the current war."""

    started: datetime
    ended: datetime
    now: datetime
    client_version: str = Field(alias="clientVersion")
    factions: list[typing.Literal["Humans", "Terminids", "Automaton", "Illuminate"]]
    impact_multiplier: float = Field(alias="impactMultiplier")
    statistics: Statistics


class Dispatch(BaseModel):
    """The information about the current war."""

    id: int
    published: datetime
    type: typing.Literal[0]
    message: str


class SteamNews(BaseModel):
    """Steam patchh notes."""

    id: str
    title: str
    url: str
    author: str
    content: str
    published_at: datetime = Field(alias="publishedAt")


class PlanetEvent(BaseModel):
    """An event on a planet."""

    id: int
    event_type: typing.Literal[1] = Field(alias="eventType")
    faction: enums.FactionType
    health: int
    max_health: int = Field(alias="maxHealth")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    campaign_id: int = Field(alias="campaignId")
    joint_operation_ids: list[int] = Field(alias="jointOperationIds")

    @property
    def planet(self) -> "Planet | None":
        from helldivepy import ApiClient

        if ApiClient._instance:
            return ApiClient._instance.planets.get_planet(self.campaign_id)
        return None


class Position(BaseModel):
    """A position in the game."""

    x: float
    y: float


class PlanetaryHazard(BaseModel):
    """A hazard on a planet."""

    name: str
    description: str


class Biome(BaseModel):
    """A biome on a planet."""

    name: str
    description: str


class Planet(BaseModel):
    """A planet in the game."""

    index: int
    name: str
    sector: str
    biome: "Biome"
    hazards: list["PlanetaryHazard"]
    hash: int
    position: "Position"
    waypoints: list[int]
    max_health: int = Field(alias="maxHealth")
    health: int
    disabled: bool
    initial_owner: enums.FactionType = Field(
        alias="initialOwner",
    )
    current_owner: enums.FactionType = Field(alias="currentOwner")
    regen_per_second: float = Field(alias="regenPerSecond")
    event: PlanetEvent | None
    statistics: Statistics
    attacking: list[int]


# TODO: make better docstrings
class AssignmentTaskData(BaseModel):
    liberate: bool | None
    planet: Planet | None
    target_count: int | None
    race: enums.FactionType | None


class AssignmentTask(BaseModel):
    """A task in an assignment"""

    type: enums.AssignmentTypes
    values: list[int]
    value_types: list[enums.ValueTypes] = Field(alias="valueTypes")
    data: AssignmentTaskData = AssignmentTaskData(
        liberate=None, planet=None, target_count=None, race=None
    )

    def model_post_init(self, __context: typing.Any) -> None:
        from helldivepy.api_client import ApiClient

        client = ApiClient._instance
        if client is None:
            raise ValueError("ApiClient is not initialized")

        for k, v in zip(self.value_types, self.values):
            match k:
                case enums.ValueTypes.PLANET:
                    self.data.planet = client.planets.get_planet(v, cached=True)
                case enums.ValueTypes.RACE:
                    self.data.race = utils.parse_faction(v)
                case enums.ValueTypes.TARGET_COUNT:
                    self.data.target_count = v
                case enums.ValueTypes.LIBERATE:
                    self.data.liberate = bool(v)


class AssignmentReward(BaseModel):
    """
    A reward in an assignment\n
    Medals: 1
    """

    type: typing.Literal[1]
    amount: int


class Assignment(BaseModel):
    """An assignment (Major Order)"""

    id: int
    progress: list[int]
    title: str | None = None
    briefing: str | None = None
    description: str | None = None
    tasks: list[AssignmentTask]
    reward: AssignmentReward
    expiration: datetime

    @property
    def is_complete(self) -> bool:
        return all(
            task.data.target_count == self.progress[index]
            for index, task in enumerate(self.tasks)
        )

    def __str__(self) -> str:
        return f"{self.title} - {self.briefing}"


class Campaign(BaseModel):
    """A campaign or battle in the game."""

    id: int
    planet: Planet
    type: int
    count: int
