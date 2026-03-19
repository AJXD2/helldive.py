import httpx

from helldivepy.models import Campaign
from helldivepy.modules import BaseModule


class CampaignModule(BaseModule):
    """Access active planetary campaigns."""

    def get_all(self) -> list[Campaign]:
        """Fetch all active campaigns.

        Returns:
            A list of all ongoing campaigns.
        """
        return [Campaign.model_validate(d) for d in self._get("/v1/campaigns")]

    def get(self, index: int) -> Campaign | None:
        """Fetch a specific campaign by ID.

        Args:
            index: The campaign ID.

        Returns:
            The matching Campaign, or None if not found.
        """
        try:
            return Campaign.model_validate(self._get(f"/v1/campaigns/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
