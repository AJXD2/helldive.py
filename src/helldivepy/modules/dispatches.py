import httpx

from helldivepy.models import Dispatch
from helldivepy.modules import BaseModule


class DispatchesModule(BaseModule):
    def get_all(self) -> list[Dispatch]:
        return [Dispatch.model_validate(d) for d in self._get("/v1/dispatches")]

    def get(self, index: int) -> Dispatch | None:
        try:
            return Dispatch.model_validate(self._get(f"/v1/dispatches/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
