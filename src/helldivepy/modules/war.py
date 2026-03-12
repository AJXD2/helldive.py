from helldivepy.models import War
from . import BaseModule

class WarModule(BaseModule):
    def get(self) -> War:
        resp = self._get("/v1/war")
        war = War(**resp)
        return war
