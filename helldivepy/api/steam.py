from helldivepy.api.base import BaseApiModule
import typing
import helldivepy.models as models

if typing.TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class SteamModule(BaseApiModule):
    """
    The Steam API module. Used to get all the Game updates and News.

    Methods:
        get_all_steam_news(): Gets all the steam news.
        get_steam_news(gid: str): Gets a steam news item by its ID.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_all_steam_news(self) -> typing.List[models.SteamNews]:
        """
        Gets the information about the current war.
        """
        data = self.get("community", "api", "v1", "steam")

        return [models.SteamNews(**news) for news in data]

    def get_steam_news(self, gid: str) -> models.SteamNews:
        """
        Gets the information about the current war.
        """
        data = self.get("community", "api", "v1", "steam", gid)
        return models.SteamNews(**data)
