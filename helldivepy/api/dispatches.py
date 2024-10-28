from helldivepy.api.base import BaseApiModule
import typing
import helldivepy.models as models

if typing.TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class DispatchModule(BaseApiModule):
    """The Dispatch API module. This module is used to interact with all dispatches (Ingame News)

    Methods:
        get_dispatches(old_to_new: bool): Gets all dispatches and orders them based on the `old_to_new` argument.
        get_dispatch(dispatch_id: int): Gets a dispatch by its ID.

    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_dispatches(self, old_to_new: bool = True) -> typing.List[models.Dispatch]:
        """
        Gets the information about the current war.
        """

        # Sort the dispatches by published date
        data = sorted(
            self.get("community", "api", "v1", "dispatches"),
            key=lambda x: x["published"],
            reverse=not old_to_new,
        )

        return [models.Dispatch(**dispatch) for dispatch in data]

    def get_dispatch(self, dispatch_id: int) -> models.Dispatch:
        """
        Gets the information about the current war.
        """
        # Get the dispatch by the ID/Index
        data = self.get("community", "api", "v1", "dispatches", str(dispatch_id))
        return models.Dispatch(**data)
