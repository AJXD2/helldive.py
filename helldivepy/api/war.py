from helldivepy.api.base import BaseApiModule
import typing
import helldivepy.models as models

if typing.TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class WarModule(BaseApiModule):
    """The War module of the API. This module is used to get all info about the current war.

    Methods:
        get_war_info(): Gets the information about the current war.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_war_info(self) -> models.WarInfo:
        """
        Gets the information about the current war.
        """
        data = self.get("community", "api", "v1", "war")

        return models.WarInfo(**data)
