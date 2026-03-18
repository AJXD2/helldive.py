import httpx

from helldivepy.models import SpaceStation
from helldivepy.modules import BaseModule


class SpaceStationsModule(BaseModule):
    def get_all(self) -> list[SpaceStation]:
        return [SpaceStation.model_validate(d) for d in self._get("/v2/space-stations")]

    def get(self, index: int) -> SpaceStation | None:
        try:
            return SpaceStation.model_validate(self._get(f"/v2/space-stations/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
