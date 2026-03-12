from typing import get_type_hints

import httpx

from helldivepy.modules import BaseModule
from helldivepy.modules.dispatches import DispatchesModule
from helldivepy.modules.war import WarModule


class HelldiveAPIClient:
    war: WarModule
    dispatches: DispatchesModule

    def __init__(
        self,
        base_url: str = "https://api.helldivers2.dev/api",
        client: str = "helldivepy",
        contact: str = "github:ajxd2/helldive.py",
    ):
        self.base_url = base_url
        self.headers = {"X-Super-Client": client, "X-Super-Contact": contact}
        self.client = httpx.Client()

        for attr, cls in get_type_hints(type(self)).items():
            if isinstance(cls, type) and issubclass(cls, BaseModule):
                setattr(self, attr, cls(self))
