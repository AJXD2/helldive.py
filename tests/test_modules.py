"""Tests for helldivepy modules using respx HTTP mocking."""

import httpx
import pytest
import respx

from helldivepy.client import HelldiveAPIClient
from helldivepy.models import (
    Assignment,
    Campaign,
    Dispatch,
    Event,
    Planet,
    SpaceStation,
    War,
)

BASE_URL = "https://api.helldivers2.dev/api"


@pytest.fixture
def client() -> HelldiveAPIClient:
    return HelldiveAPIClient()


# ---------------------------------------------------------------------------
# WarModule
# ---------------------------------------------------------------------------


class TestWarModule:
    def test_get_returns_war(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_war: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/war").mock(
            return_value=httpx.Response(200, json=raw_war)
        )
        result = client.war.get()
        assert isinstance(result, War)
        assert result.client_version == "1.0.0"
        assert result.factions == ["Humans", "Terminids"]
        assert result.impact_multiplier == 0.02

    def test_get_sends_headers(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_war: dict,  # type: ignore[type-arg]
    ) -> None:
        route = respx_mock.get(f"{BASE_URL}/v1/war").mock(
            return_value=httpx.Response(200, json=raw_war)
        )
        client.war.get()
        assert route.called
        request = route.calls.last.request
        assert request.headers["X-Super-Client"] == "helldivepy"
        assert request.headers["X-Super-Contact"] == "github:ajxd2/helldive.py"


# ---------------------------------------------------------------------------
# DispatchesModule
# ---------------------------------------------------------------------------


class TestDispatchesModule:
    def test_get_all_returns_list(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_dispatch: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/dispatches").mock(
            return_value=httpx.Response(200, json=[raw_dispatch])
        )
        result = client.dispatches.get_all()
        assert len(result) == 1
        assert isinstance(result[0], Dispatch)
        assert result[0].id == raw_dispatch["id"]

    def test_get_all_empty_list(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/dispatches").mock(
            return_value=httpx.Response(200, json=[])
        )
        assert client.dispatches.get_all() == []

    def test_get_returns_dispatch(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_dispatch: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/dispatches/1").mock(
            return_value=httpx.Response(200, json=raw_dispatch)
        )
        result = client.dispatches.get(1)
        assert isinstance(result, Dispatch)
        assert result.id == 1

    def test_get_returns_none_on_404(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/dispatches/999").mock(
            return_value=httpx.Response(404)
        )
        assert client.dispatches.get(999) is None

    def test_get_reraises_non_404_errors(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/dispatches/1").mock(
            return_value=httpx.Response(500)
        )
        with pytest.raises(httpx.HTTPStatusError):
            client.dispatches.get(1)


# ---------------------------------------------------------------------------
# PlanetModule
# ---------------------------------------------------------------------------


class TestPlanetModule:
    def test_get_all_returns_list(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_planet: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/planets").mock(
            return_value=httpx.Response(200, json=[raw_planet])
        )
        result = client.planets.get_all()
        assert len(result) == 1
        assert isinstance(result[0], Planet)
        assert result[0].name == "HELLMIRE"

    def test_get_all_empty_list(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/planets").mock(
            return_value=httpx.Response(200, json=[])
        )
        assert client.planets.get_all() == []

    def test_get_returns_planet(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_planet: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/planets/42").mock(
            return_value=httpx.Response(200, json=raw_planet)
        )
        result = client.planets.get(42)
        assert isinstance(result, Planet)
        assert result.index == 42

    def test_get_returns_none_on_404(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/planets/999").mock(
            return_value=httpx.Response(404)
        )
        assert client.planets.get(999) is None

    def test_get_reraises_non_404_errors(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/planets/1").mock(
            return_value=httpx.Response(503)
        )
        with pytest.raises(httpx.HTTPStatusError):
            client.planets.get(1)

    def test_get_events_returns_list(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_event: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/planet-events").mock(
            return_value=httpx.Response(200, json=[raw_event])
        )
        result = client.planets.get_events()
        assert len(result) == 1
        assert isinstance(result[0], Event)
        assert result[0].id == 99

    def test_get_events_empty_list(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/planet-events").mock(
            return_value=httpx.Response(200, json=[])
        )
        assert client.planets.get_events() == []


# ---------------------------------------------------------------------------
# AssignmentsModule
# ---------------------------------------------------------------------------


class TestAssignmentsModule:
    def test_get_all_returns_list(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_assignment: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/assignments").mock(
            return_value=httpx.Response(200, json=[raw_assignment])
        )
        result = client.assignments.get_all()
        assert len(result) == 1
        assert isinstance(result[0], Assignment)
        assert result[0].id == 9001

    def test_get_all_empty_list(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/assignments").mock(
            return_value=httpx.Response(200, json=[])
        )
        assert client.assignments.get_all() == []

    def test_get_returns_assignment(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_assignment: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/assignments/9001").mock(
            return_value=httpx.Response(200, json=raw_assignment)
        )
        result = client.assignments.get(9001)
        assert isinstance(result, Assignment)
        assert result.title == "MAJOR ORDER"

    def test_get_returns_none_on_404(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/assignments/999").mock(
            return_value=httpx.Response(404)
        )
        assert client.assignments.get(999) is None

    def test_get_reraises_non_404_errors(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/assignments/1").mock(
            return_value=httpx.Response(429)
        )
        with pytest.raises(httpx.HTTPStatusError):
            client.assignments.get(1)


# ---------------------------------------------------------------------------
# CampaignModule
# ---------------------------------------------------------------------------


class TestCampaignModule:
    def test_get_all_returns_list(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_campaign: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/campaigns").mock(
            return_value=httpx.Response(200, json=[raw_campaign])
        )
        result = client.campaigns.get_all()
        assert len(result) == 1
        assert isinstance(result[0], Campaign)
        assert result[0].id == 5

    def test_get_all_empty_list(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/campaigns").mock(
            return_value=httpx.Response(200, json=[])
        )
        assert client.campaigns.get_all() == []

    def test_get_returns_campaign(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_campaign: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/campaigns/5").mock(
            return_value=httpx.Response(200, json=raw_campaign)
        )
        result = client.campaigns.get(5)
        assert isinstance(result, Campaign)
        assert result.planet.name == "HELLMIRE"

    def test_get_returns_none_on_404(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/campaigns/999").mock(
            return_value=httpx.Response(404)
        )
        assert client.campaigns.get(999) is None

    def test_get_reraises_non_404_errors(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v1/campaigns/1").mock(
            return_value=httpx.Response(401)
        )
        with pytest.raises(httpx.HTTPStatusError):
            client.campaigns.get(1)


# ---------------------------------------------------------------------------
# SpaceStationsModule
# ---------------------------------------------------------------------------


class TestSpaceStationsModule:
    def test_get_all_returns_list(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_spacestation: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v2/space-stations").mock(
            return_value=httpx.Response(200, json=[raw_spacestation])
        )
        result = client.spacestations.get_all()
        assert len(result) == 1
        assert isinstance(result[0], SpaceStation)
        assert result[0].id32 == 749875195

    def test_get_all_empty_list(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v2/space-stations").mock(
            return_value=httpx.Response(200, json=[])
        )
        assert client.spacestations.get_all() == []

    def test_get_returns_spacestation(
        self,
        client: HelldiveAPIClient,
        respx_mock: respx.MockRouter,
        raw_spacestation: dict,  # type: ignore[type-arg]
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v2/space-stations/749875195").mock(
            return_value=httpx.Response(200, json=raw_spacestation)
        )
        result = client.spacestations.get(749875195)
        assert isinstance(result, SpaceStation)
        assert result.id32 == 749875195

    def test_get_returns_none_on_404(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v2/space-stations/999").mock(
            return_value=httpx.Response(404)
        )
        assert client.spacestations.get(999) is None

    def test_get_reraises_non_404_errors(
        self, client: HelldiveAPIClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get(f"{BASE_URL}/v2/space-stations/1").mock(
            return_value=httpx.Response(503)
        )
        with pytest.raises(httpx.HTTPStatusError):
            client.spacestations.get(1)
