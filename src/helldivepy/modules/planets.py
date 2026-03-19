import httpx

from helldivepy.models import Event, Planet
from helldivepy.modules import BaseModule


class PlanetModule(BaseModule):
    """Access planet data and active planetary events."""

    def get_all(self) -> list[Planet]:
        """Fetch all planets.

        Returns:
            A list of all planets in the galaxy.
        """
        return [Planet.model_validate(p) for p in self._get("/v1/planets")]

    def get(self, index: int) -> Planet | None:
        """Fetch a specific planet by index.

        Args:
            index: The planet's ArrowHead index.

        Returns:
            The matching Planet, or None if not found.
        """
        try:
            return Planet.model_validate(self._get(f"/v1/planets/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    def get_events(self) -> list[Event]:
        """Fetch all planets with an active event (e.g. defense campaigns).

        Returns:
            A list of active Events across all planets.
        """
        return [Event.model_validate(e) for e in self._get("/v1/planet-events")]
