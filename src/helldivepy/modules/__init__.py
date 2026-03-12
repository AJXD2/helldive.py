from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from helldivepy.client import HelldiveAPIClient


class BaseModule:
    def __init__(self, client: "HelldiveAPIClient") -> None:
        self._client = client

    def _url(self, path: str) -> str:
        return self._client.base_url.rstrip("/") + "/" + path.lstrip("/")

    def _get(self, path: str, **kwargs):
        response = self._client.client.get(self._url(path), headers=self._client.headers, **kwargs)
        response.raise_for_status()
        return response.json()

    async def _aget(self, path: str, **kwargs):
        response = await self._client.async_client.get(self._url(path), headers=self._client.headers, **kwargs)
        response.raise_for_status()
        return response.json()
