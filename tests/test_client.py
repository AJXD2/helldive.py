"""Tests for HelldiveAPIClient."""

import httpx

from helldivepy.client import HelldiveAPIClient
from helldivepy.modules.assignments import AssignmentsModule
from helldivepy.modules.campaigns import CampaignModule
from helldivepy.modules.dispatches import DispatchesModule
from helldivepy.modules.planets import PlanetModule
from helldivepy.modules.space_stations import SpaceStationsModule
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
        assert isinstance(c.dispatches, DispatchesModule)
        assert isinstance(c.planets, PlanetModule)
        assert isinstance(c.assignments, AssignmentsModule)
        assert isinstance(c.campaigns, CampaignModule)
        assert isinstance(c.space_stations, SpaceStationsModule)

    def test_httpx_client_created(self) -> None:
        c = HelldiveAPIClient()
        assert isinstance(c.client, httpx.Client)

    def test_context_manager_closes_client(self) -> None:
        with HelldiveAPIClient() as c:
            assert not c.client.is_closed
        assert c.client.is_closed
