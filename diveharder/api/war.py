from diveharder.api.base import BaseApiModule
import typing
import diveharder.models as models

if typing.TYPE_CHECKING:
    from diveharder.api_client import ApiClient


class WarModule(BaseApiModule):
    """
    The War API module.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_war_info(self) -> models.WarInfo:
        """
        Gets the information about the current war.
        """
        data = self.get("community", "api", "v1", "war")

        return models.WarInfo(**data)