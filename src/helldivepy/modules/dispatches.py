from mkdocs.config.config_options import Optional
from helldivepy.models import Dispatch
from helldivepy.modules import BaseModule
class DispatchesModule(BaseModule):
    def get_all(self) -> list[Dispatch]:
        resp = self._get("/v1/dispatches")
        return [Dispatch(**dispatch) for dispatch in resp]

    def get(self, id: int) -> Dispatch | None:
        try:
            resp = self._get(f"/v1/dispatches/{id}")
            return Dispatch(**resp)
        except Exception:
            return None
