import httpx

from helldivepy.models import SteamNews
from helldivepy.modules import BaseModule


class SteamModule(BaseModule):
    def get_all(self) -> list[SteamNews]:
        return [SteamNews.model_validate(d) for d in self._get("/v1/steam")]

    def get(self, gid: str) -> SteamNews | None:
        try:
            return SteamNews.model_validate(self._get(f"/v1/steam/{gid}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
