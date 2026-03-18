"""Tests for HelldiveAPIClient."""

import httpx

from helldivepy.client import HelldiveAPIClient
from helldivepy.modules.assignments import AssignmentsModule
from helldivepy.modules.campaigns import CampaignModule
from helldivepy.modules.dispatches import DispatchesModuleV1, DispatchesModuleV2
from helldivepy.modules.planets import PlanetModule
from helldivepy.modules.war import WarModule


class TestHelldiveAPIClient:
    def test_default_base_url(self) -> None:
        c = HelldiveAPIClient()
        assert c.base_url == "https://api.helldivers2.dev/api"

    def test_custom_base_url(self) -> None:
        c = HelldiveAPIClient(base_url="https://custom.example.com/api")
        assert c.base_url == "https://custom.example.com/api"

    def test_default_headers(self) -> None:
        c = HelldiveAPIClient()
        assert c.headers["X-Super-Client"] == "helldivepy"
        assert c.headers["X-Super-Contact"] == "github:ajxd2/helldive.py"

    def test_custom_headers(self) -> None:
        c = HelldiveAPIClient(client="myapp", contact="contact@example.com")
        assert c.headers["X-Super-Client"] == "myapp"
        assert c.headers["X-Super-Contact"] == "contact@example.com"

    def test_all_modules_auto_registered(self) -> None:
        c = HelldiveAPIClient()
        assert isinstance(c.war, WarModule)
        assert isinstance(c.dispatches, DispatchesModuleV2)
        assert isinstance(c.dispatches_v1, DispatchesModuleV1)
        assert isinstance(c.planets, PlanetModule)
        assert isinstance(c.assignments, AssignmentsModule)
        assert isinstance(c.campaigns, CampaignModule)

    def test_httpx_client_created(self) -> None:
        c = HelldiveAPIClient()
        assert isinstance(c.client, httpx.Client)
