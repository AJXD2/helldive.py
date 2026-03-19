from typing import get_type_hints

import httpx

from helldivepy.modules import BaseModule

# Modules
from helldivepy.modules.assignments import AssignmentsModule
from helldivepy.modules.campaigns import CampaignModule
from helldivepy.modules.dispatches import DispatchesModule
from helldivepy.modules.planets import PlanetModule
from helldivepy.modules.space_stations import SpaceStationsModule
from helldivepy.modules.steam import SteamModule
from helldivepy.modules.war import WarModule


class HelldiveAPIClient:
    war: WarModule
    dispatches: DispatchesModule
    planets: PlanetModule
    assignments: AssignmentsModule
    campaigns: CampaignModule
    space_stations: SpaceStationsModule
    steam: SteamModule

    def __init__(
        self,
        client: str = "helldivepy",
        contact: str = "github:ajxd2/helldive.py",
        base_url: str = "https://api.helldivers2.dev/api",
    ):
        """Create a new API client.

        Args:
            client: Your application name, sent as `X-Super-Client`. Identifies your
                app to the API operators.
            contact: Contact info for your app, sent as `X-Super-Contact`. Typically
                a GitHub URL or email address.
            base_url: API base URL. Override for testing or alternative deployments.
        """
        self.base_url = base_url
        self.headers = {"X-Super-Client": client, "X-Super-Contact": contact}
        self.client = httpx.Client()

        for attr, cls in get_type_hints(type(self)).items():
            if isinstance(cls, type) and issubclass(cls, BaseModule):
                setattr(self, attr, cls(self))

    def __enter__(self) -> "HelldiveAPIClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.client.close()
