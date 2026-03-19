import httpx

from helldivepy.models import SpaceStation
from helldivepy.modules import BaseModule


class SpaceStationsModule(BaseModule):
    """Access the Democracy Space Station (DSS) and its tactical actions."""

    def get_all(self) -> list[SpaceStation]:
        """Fetch all space stations.

        Returns:
            A list of all space stations and their current state.
        """
        return [SpaceStation.model_validate(d) for d in self._get("/v2/space-stations")]

    def get(self, index: int) -> SpaceStation | None:
        """Fetch a specific space station by ID.

        Args:
            index: The station's 32-bit ArrowHead ID.

        Returns:
            The matching SpaceStation, or None if not found.
        """
        try:
            return SpaceStation.model_validate(self._get(f"/v2/space-stations/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
