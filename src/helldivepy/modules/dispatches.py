import httpx

from helldivepy.models import Dispatch, DispatchV2
from helldivepy.modules import BaseModule


class DispatchesModuleV1(BaseModule):
    def get_all(self) -> list[Dispatch]:
        return [Dispatch.model_validate(d) for d in self._get("/v1/dispatches")]

    def get(self, index: int) -> Dispatch | None:
        try:
            return Dispatch.model_validate(self._get(f"/v1/dispatches/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise


class DispatchesModuleV2(BaseModule):
    def get_all(self) -> list[DispatchV2]:
        return [DispatchV2.model_validate(d) for d in self._get("/v2/dispatches")]

    def get(self, index: int) -> DispatchV2 | None:
        try:
            return DispatchV2.model_validate(self._get(f"/v2/dispatches/{index}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
