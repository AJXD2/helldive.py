from typing import get_type_hints

import httpx

from helldivepy.modules import BaseModule
from helldivepy.modules.assignments import AssignmentsModule
from helldivepy.modules.campaigns import CampaignModule
from helldivepy.modules.dispatches import DispatchesModule
from helldivepy.modules.planets import PlanetModule
from helldivepy.modules.war import WarModule


class HelldiveAPIClient:
    war: WarModule
    dispatches: DispatchesModule
    planets: PlanetModule
    assignments: AssignmentsModule
    campaigns: CampaignModule

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
