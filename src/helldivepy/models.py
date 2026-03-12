from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

# Convert snake_case to camelCase for JSON serialization.
# This removes adding an extra step to the request methods while enforcing standards.
class APIModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
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
    started: str
    ended: str
    now: str
    client_version: str
    factions: list[str]
    impact_multiplier: float
    statistics: Statistics
