from typing import get_type_hints

import httpx

from helldivepy.modules import BaseModule

# Modules
from helldivepy.modules.assignments import AssignmentsModule
from helldivepy.modules.campaigns import CampaignModule
from helldivepy.modules.dispatches import DispatchesModuleV1, DispatchesModuleV2
from helldivepy.modules.planets import PlanetModule
from helldivepy.modules.space_stations import SpaceStationsModule
from helldivepy.modules.steam import SteamModule
from helldivepy.modules.war import WarModule


class HelldiveAPIClient:
    war: WarModule
    dispatches: DispatchesModuleV2
    dispatches_v1: DispatchesModuleV1
    planets: PlanetModule
    assignments: AssignmentsModule
    campaigns: CampaignModule
    spacestations: SpaceStationsModule
    steam: SteamModule

    def __init__(
        self,
        client: str = "helldivepy",
        contact: str = "github:ajxd2/helldive.py",
        base_url: str = "https://api.helldivers2.dev/api",
    ):
        self.base_url = base_url
        self.headers = {"X-Super-Client": client, "X-Super-Contact": contact}
        self.client = httpx.Client()

        for attr, cls in get_type_hints(type(self)).items():
            if isinstance(cls, type) and issubclass(cls, BaseModule):
                setattr(self, attr, cls(self))
