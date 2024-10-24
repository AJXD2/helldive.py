from helldivepy.api.base import BaseApiModule
import typing
import helldivepy.models as models

if typing.TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class PlanetsModule(BaseApiModule):
    """
    The Planets API module. This module is used to interact with the planets.

    Methods:
        get_planets(): Gets all planets.
        get_planet(index: int): Gets a planet using the index.
        get_planets_with_events(): Gets all planets with events.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)
        self._planets: list[models.Planet] = []

    def get_planets(self) -> typing.List[models.Planet]:
        """Get all planets

        Returns:
            typing.List[models.Planet]: The list of planet objects
        """
        data = self.get("community", "api", "v1", "planets")

        self._planets = [models.Planet(**planet) for planet in data]
        return self._planets

    def get_planet(self, index: int, cached: bool = False) -> models.Planet:
        """Gets a planet using the index

        Args:
            index (int): The index of the planet

        Returns:
            models.Planet: The planet object
        """
        if cached:
            if len(self._planets) < index:
                self.logger.warning(f"Planet {index} not cached. Fetching from API.")
                self.get_planets()
                return self._planets[index]
            return self._planets[index]
        data = self.get("community", "api", "v1", "planets", str(index))
        return models.Planet(**data)

    def get_planets_with_events(self) -> typing.List[models.Planet]:
        """Gets all planets with an active event

        Returns:
            typing.List[models.Planet]: The list of planet objects
        """
        data = self.get("community", "api", "v1", "planet-events")
        return [models.Planet(**planet) for planet in data]
