from helldivepy.models import Planet

from . import BaseModule


class PlanetModule(BaseModule):
    def get_all(self) -> list[Planet]:
        return [Planet(**planet_data) for planet_data in self._get("/v1/planets")]

    def get(self, id: int) -> Planet | None:
        try:
            return Planet(**self._get(f"/v1/planets/{id}"))
        except Exception:
            return None
