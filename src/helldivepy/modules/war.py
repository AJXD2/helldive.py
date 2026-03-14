from helldivepy.models import War

from . import BaseModule


class WarModule(BaseModule):
    def get(self) -> War:
        return War.model_validate(self._get("/v1/war"))
