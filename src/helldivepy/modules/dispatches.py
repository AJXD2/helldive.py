import httpx

from helldivepy.models import Dispatch
from helldivepy.modules import BaseModule


class DispatchesModule(BaseModule):
    """Access in-game dispatches (high-command broadcasts)."""

    def get_all(self) -> list[Dispatch]:
        """Fetch all available dispatches.

        Returns:
            A list of all dispatches, most recent first.
        """
        return [Dispatch.model_validate(d) for d in self._get("/v2/dispatches")]

    def get(self, index: int) -> Dispatch | None:
        """Fetch a specific dispatch by ID.

        Args:
            index: The dispatch ID.

        Returns:
            The matching Dispatch, or None if not found.
        """
        try:
            return Dispatch.model_validate(self._get(f"/v2/dispatches/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
