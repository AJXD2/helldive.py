from helldivepy.api.base import BaseApiModule
import helldivepy.models as models
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class SpaceStationModule(BaseApiModule):
    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_space_stations(self) -> list[models.SpaceStation]:
        """
        Retrieves all space stations.

        Returns:
            list[SpaceStation]: A list of space station objects from the server.
        """
        data = self.get("community", "api", "v1", "space-stations")
        return [models.SpaceStation(**item) for item in data]

    def get_space_station(self, index: int) -> Optional[models.SpaceStation]:
        """
        Retrieves a space station by its ID.

        Args:
            index (int): The ID of the space station.

        Returns:
            Optional[SpaceStation]: The space station object if found, or None.
        """
        data = self.get("community", "api", "v1", "space", "stations", str(index))
        return models.SpaceStation(**data) if data else None
