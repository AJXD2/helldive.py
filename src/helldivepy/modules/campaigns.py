import httpx

from helldivepy.models import Campaign
from helldivepy.modules import BaseModule


class CampaignModule(BaseModule):
    def get_all(self) -> list[Campaign]:
        return [Campaign.model_validate(d) for d in self._get("/v1/campaigns")]

    def get(self, index: int) -> Campaign | None:
        try:
            return Campaign.model_validate(self._get(f"/v1/campaigns/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
