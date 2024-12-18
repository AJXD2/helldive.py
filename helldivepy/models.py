from pydantic import BaseModel, Field
from datetime import datetime
import typing
import helldivepy.enums as enums
import helldivepy.utils as utils
import helldivepy.constants as constants


class APIURLConfiguration(BaseModel):
    """Configuration for API endpoints.

    Contains URLs for different API services used by the application.

    Attributes:
        diveharder (str): Base URL for the Diveharder API endpoint.
        community (str): Base URL for the Community API endpoint.
    """

    diveharder: str = constants.OFFICIAL_DIVEHARDER_URL
    community: str = constants.OFFICIAL_COMMUNITY_URL


class Statistics(BaseModel):
    """War statistics tracking various gameplay metrics.

    Tracks mission outcomes, combat statistics, and player performance metrics
    for the current war campaign.

    Attributes:
        missions_won (int): Number of successfully completed missions.
        missions_lost (int): Number of failed missions.
        mission_time (int): Total time spent in missions (seconds).
        terminid_kills (int): Number of Terminid enemies eliminated.
        automaton_kills (int): Number of Automaton enemies eliminated.
        illuminate_kills (int): Number of Illuminate enemies eliminated.
        bullets_fired (int): Total ammunition expended.
        bullets_hit (int): Total successful hits on targets.
        time_played (int): Total gameplay duration (seconds).
        deaths (int): Total player deaths.
        revives (int): Total teammate revivals performed.
        friendlies (int): Total friendly fire incidents.
        mission_success_rate (float): Percentage of successful missions.
        accuracy (int): Overall shooting accuracy percentage.
        player_count (int): Current number of active players.
    """

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
    """Information about the current galactic war.

    Contains timing information, client details, and overall war statistics.

    Attributes:
        started (datetime): War start timestamp.
        ended (datetime): War end timestamp.
        now (datetime): Current war time.
        client_version (str): Game client version.
        factions (list[str]): List of participating factions.
        impact_multiplier (float): Current war impact multiplier.
        statistics (Statistics): Comprehensive war statistics.
    """

    started: datetime
    ended: datetime
    now: datetime
    client_version: str = Field(alias="clientVersion")
    factions: list[typing.Literal["Humans", "Terminids", "Automaton", "Illuminate"]]
    impact_multiplier: float = Field(alias="impactMultiplier")
    statistics: Statistics


class Dispatch(BaseModel):
    """War dispatch message container.

    Represents official communications during the war campaign.

    Attributes:
        id (int): Unique dispatch identifier.
        published (datetime): Dispatch publication timestamp.
        type (Literal[0]): Message type identifier.
        message (str): Dispatch content.
    """

    id: int
    published: datetime
    type: typing.Literal[0]
    message: str


class SteamNews(BaseModel):
    """Steam platform update information.

    Contains details about game patches and updates published on Steam.

    Attributes:
        id (str): Unique news article identifier.
        title (str): Update title.
        url (str): Full update documentation URL.
        author (str): Update author.
        content (str): Update content.
        published_at (datetime): Publication timestamp.
    """

    id: str
    title: str
    url: str
    author: str
    content: str
    published_at: datetime = Field(alias="publishedAt")


class PlanetEvent(BaseModel):
    """Planetary event information.

    Tracks events affecting individual planets during the war.

    Attributes:
        id (int): Unique event identifier.
        event_type (int): Type of planetary event.
        faction (FactionType): Associated faction.
        health (int): Current planet health.
        max_health (int): Maximum planet health.
        start_time (datetime): Event start timestamp.
        end_time (datetime): Event end timestamp.
        campaign_id (int): Associated campaign identifier.
        joint_operation_ids (list[int]): Related joint operation identifiers.
    """

    id: int
    event_type: int = Field(alias="eventType")
    faction: enums.FactionType
    health: int
    max_health: int = Field(alias="maxHealth")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    campaign_id: int = Field(alias="campaignId")
    joint_operation_ids: list[int] = Field(alias="jointOperationIds")

    @property
    def planet(self) -> "Planet | None":
        """Retrieves the planet associated with this event.

        Returns:
            Planet | None: Associated planet object if available, None otherwise.
        """
        from helldivepy import ApiClient

        if ApiClient._instance:
            return ApiClient._instance.planets.get_planet(self.campaign_id)
        return None


class Position(BaseModel):
    """2D coordinate position.

    Represents a location in 2D space.

    Attributes:
        x (float): Horizontal coordinate.
        y (float): Vertical coordinate.
    """

    x: float
    y: float


class PlanetaryHazard(BaseModel):
    """Planetary environmental hazard.

    Describes environmental dangers present on a planet.

    Attributes:
        name (str): Hazard identifier.
        description (str): Detailed hazard description.
    """

    name: str
    description: str


class Biome(BaseModel):
    """Planetary biome characteristics.

    Describes the environmental characteristics of a planet.

    Attributes:
        name (str): Biome identifier.
        description (str): Detailed biome description.
    """

    name: str
    description: str


class Planet(BaseModel):
    """Planetary information and status.

    Contains comprehensive information about a planet in the war.

    Attributes:
        index (int): Planet index number.
        name (str): Planet name.
        sector (str): Galactic sector location.
        biome (Biome): Planet's biome characteristics.
        hazards (list[PlanetaryHazard]): Environmental hazards.
        hash (int): Unique planet identifier.
        position (Position): Galactic coordinates.
        waypoints (list[int]): Planetary waypoints.
        max_health (int): Maximum planetary health.
        health (int): Current planetary health.
        disabled (bool): Planet accessibility status.
        initial_owner (FactionType): Original controlling faction.
        current_owner (FactionType): Current controlling faction.
        regen_per_second (float): Health regeneration rate.
        event (PlanetEvent | None): Current planetary event.
        statistics (Statistics): Planet-specific statistics.
        attacking (list[int]): Attacking force identifiers.
    """

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
    initial_owner: enums.FactionType = Field(alias="initialOwner")
    current_owner: enums.FactionType = Field(alias="currentOwner")
    regen_per_second: float = Field(alias="regenPerSecond")
    event: PlanetEvent | None
    statistics: Statistics
    attacking: list[int]

    @property
    def has_space_station(self) -> bool:
        """Checks for presence of an orbital space station.

        Returns:
            bool: True if a space station is present, False otherwise.

        Raises:
            RuntimeError: If ApiClient is not properly initialized.
        """
        from helldivepy import ApiClient

        if not ApiClient._instance:
            raise RuntimeError("ApiClient not initialized.")

        client = ApiClient._instance
        stations = client.space_stations.get_space_stations()
        return self.index in [i.planet.index for i in stations]


class AssignmentTaskData(BaseModel):
    """Assignment task specific data.

    Contains details about objectives for an assignment task.

    Attributes:
        liberate (bool | None): Planet liberation objective flag.
        planet (Planet | None): Target planet for assignment.
        target_count (int | None): Required objective count.
        race (FactionType | None): Target faction type.
    """

    liberate: bool | None
    planet: Planet | None
    target_count: int | None
    race: enums.FactionType | None


class AssignmentTask(BaseModel):
    """Individual assignment task details.

    Represents a single task within an assignment.

    Attributes:
        type (AssignmentTypes): Task type classification.
        values (list[int]): Task-specific values.
        value_types (list[ValueTypes]): Types of provided values.
        data (AssignmentTaskData): Associated task data.
    """

    type: enums.AssignmentTypes
    values: list[int]
    value_types: list[enums.ValueTypes] = Field(alias="valueTypes")
    data: AssignmentTaskData = AssignmentTaskData(
        liberate=None, planet=None, target_count=None, race=None
    )

    def model_post_init(self, __context: typing.Any) -> None:
        """Initializes task data after model creation.

        Args:
            __context (Any): Initialization context data.

        Raises:
            ValueError: If ApiClient is not properly initialized.
        """
        from helldivepy.api_client import ApiClient

        client = ApiClient._instance
        if client is None:
            raise ValueError("ApiClient is not initialized")

        for k, v in zip(self.value_types, self.values):
            match k:
                case enums.ValueTypes.PLANET:
                    self.data.planet = client.planets.get_planet(v)
                case enums.ValueTypes.RACE:
                    self.data.race = utils.parse_faction(v)
                case enums.ValueTypes.TARGET_COUNT:
                    self.data.target_count = v
                case enums.ValueTypes.LIBERATE:
                    self.data.liberate = bool(v)


class AssignmentReward(BaseModel):
    """Assignment completion reward.

    Details about rewards given for completing an assignment.

    Attributes:
        type (int): Reward type identifier.
        amount (int): Reward quantity.
    """

    type: int
    amount: int


class Assignment(BaseModel):
    """Major Order assignment information.

    Contains complete information about a mission assignment.

    Attributes:
        id (int): Unique assignment identifier.
        progress (list[int]): Task completion progress.
        title (str | None): Assignment title.
        briefing (str | None): Mission briefing text.
        description (str | None): Detailed assignment description.
        tasks (list[AssignmentTask]): Required tasks.
        reward (AssignmentReward): Completion reward.
        expiration (datetime): Assignment expiration time.
    """

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
        """Checks if all assignment tasks are complete.

        Returns:
            bool: True if all tasks meet their target count, False otherwise.
        """
        return all(
            task.data.target_count == self.progress[index]
            for index, task in enumerate(self.tasks)
        )

    def __str__(self) -> str:
        """Creates a string representation of the assignment.

        Returns:
            str: Assignment title and briefing summary.
        """
        return f"{self.title} - {self.briefing}"


class Campaign(BaseModel):
    """Campaign battle information.

    Contains details about a specific war campaign.

    Attributes:
        id (int): Unique campaign identifier.
        planet (Planet): Campaign target planet.
        type (int): Campaign classification.
        count (int): Number of battles in campaign.
    """

    id: int
    planet: Planet
    type: enums.CampaignTypes
    count: int


class SpaceStation(BaseModel):
    """Orbital space station information.

    Contains details about a planetary space station.

    Attributes:
        id (int): Unique station identifier.
        planet (Planet): Host planet.
        election_end (datetime): Station election period end time.
        flags (int): Station status flags.
    """

    id: int = Field(alias="id32")
    planet: Planet
    election_end: datetime = Field(alias="electionEnd")
    flags: int
