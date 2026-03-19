import httpx

from helldivepy.models import SteamNews
from helldivepy.modules import BaseModule


class SteamModule(BaseModule):
    """Access the Helldivers 2 Steam news feed."""

    def get_all(self) -> list[SteamNews]:
        """Fetch all Steam news articles for Helldivers 2.

        Returns:
            A list of Steam news articles, most recent first.
        """
        return [SteamNews.model_validate(d) for d in self._get("/v1/steam")]

    def get(self, gid: str) -> SteamNews | None:
        """Fetch a specific Steam news article by its global ID.

        Args:
            gid: The Steam article global ID.

        Returns:
            The matching SteamNews article, or None if not found.
        """
        try:
            return SteamNews.model_validate(self._get(f"/v1/steam/{gid}"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
