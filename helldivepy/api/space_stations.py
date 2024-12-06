from helldivepy.api.base import BaseApiModule
import typing
import helldivepy.models as models

if typing.TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class SpaceStationModule(BaseApiModule):
    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_space_stations(self) -> list[models.SpaceStation]:
        """Gets all spacestations

        Returns:
            list[models.SpaceStation]: The response from the server.
        """
        data = self.get("community", "api", "v1", "space-stations")
        return [models.SpaceStation(**i) for i in data]

    def get_space_station(self, index: int) -> typing.Optional[models.SpaceStation]:
        """Get a space station by its ID.

        Args:
            index (int): The ID of the space station

        Returns:
            typing.Optional[models.SpaceStation]: The response from the server.
        """
        data = self.get("community", "api", "v1", "space", "stations", str(index))
        if not data:
            return None
        return models.SpaceStation(**data)
