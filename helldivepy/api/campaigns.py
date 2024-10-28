from helldivepy.api.base import BaseApiModule
import typing
import helldivepy.models as models

if typing.TYPE_CHECKING:
    from helldivepy.api_client import ApiClient


class CampaignModule(BaseApiModule):
    """
    The Campaign API module. This module is used to interact with all campaigns (Battles/Planets that are accessible).

    Methods:
        get_campaigns(): Gets all current active campaigns.
        get_campaign(campaign_id: int): Gets a campaign by its ID.

    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_campaigns(self) -> typing.List[models.Campaign]:
        """Gets all current active campaigns.

        Returns:
            typing.List[models.Campaign]: The campaigns.
        """
        data = self.get("community", "api", "v1", "campaigns")
        return [models.Campaign(**campaign) for campaign in data]

    def get_campaign(self, campaign_id: int) -> models.Campaign:
        """Gets a campaign by its ID.

        Args:
            campaign_id (int): The ID of the campaign.

        Returns:
            models.Campaign: The campaign.
        """
        data = self.get("community", "api", "v1", "campaigns", str(campaign_id))

        return models.Campaign(**data)
