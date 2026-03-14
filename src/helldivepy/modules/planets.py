import httpx

from helldivepy.models import Event, Planet
from helldivepy.modules import BaseModule


class PlanetModule(BaseModule):
    def get_all(self) -> list[Planet]:
        return [Planet.model_validate(p) for p in self._get("/v1/planets")]

    def get(self, index: int) -> Planet | None:
        try:
            return Planet.model_validate(self._get(f"/v1/planets/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    def get_events(self) -> list[Event]:
        return [Event.model_validate(e) for e in self._get("/v1/planet-events")]
