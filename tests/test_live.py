"""Live integration tests against the real Helldivers 2 API.

Run with: uv run pytest --live
These tests make real HTTP requests and require a network connection.
"""

import time

import pytest

from helldivepy.client import HelldiveAPIClient
from helldivepy.models import (
    Assignment,
    Campaign,
    Dispatch,
    DispatchV2,
    Event,
    Planet,
    SpaceStation,
    SteamNews,
    War,
)


@pytest.fixture(scope="module")
def live_client() -> HelldiveAPIClient:
    return HelldiveAPIClient()


# API limit: 5 requests per 10 seconds. Sleep between tests to avoid 429s.
@pytest.fixture(autouse=True)
def rate_limit_sleep() -> None:
    time.sleep(2.5)


# ---------------------------------------------------------------------------
# War
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLiveWarModule:
    def test_get_returns_war(self, live_client: HelldiveAPIClient) -> None:
        war = live_client.war.get()
        assert isinstance(war, War)
        assert war.started is not None
        assert war.impact_multiplier > 0
        assert len(war.factions) > 0
        assert war.statistics.player_count >= 0


# ---------------------------------------------------------------------------
# Dispatches
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLiveDispatchesModuleV1:
    def test_get_all_returns_list(self, live_client: HelldiveAPIClient) -> None:
        dispatches = live_client.dispatches_v1.get_all()
        assert isinstance(dispatches, list)
        for d in dispatches:
            assert isinstance(d, Dispatch)

    def test_get_first_by_index(self, live_client: HelldiveAPIClient) -> None:
        dispatches = live_client.dispatches_v1.get_all()
        if not dispatches:
            pytest.skip("No dispatches available.")
        first = live_client.dispatches_v1.get(dispatches[0].id)
        assert isinstance(first, Dispatch)
        assert first.id == dispatches[0].id

    def test_get_nonexistent_returns_none(self, live_client: HelldiveAPIClient) -> None:
        result = live_client.dispatches_v1.get(999999999)
        assert result is None


@pytest.mark.live
class TestLiveDispatchesModuleV2:
    def test_get_all_returns_list(self, live_client: HelldiveAPIClient) -> None:
        dispatches = live_client.dispatches.get_all()
        assert isinstance(dispatches, list)
        for d in dispatches:
            assert isinstance(d, DispatchV2)

    def test_get_first_by_index(self, live_client: HelldiveAPIClient) -> None:
        dispatches = live_client.dispatches.get_all()
        if not dispatches:
            pytest.skip("No dispatches available.")
        first = live_client.dispatches.get(dispatches[0].id)
        assert isinstance(first, DispatchV2)
        assert first.id == dispatches[0].id

    def test_get_nonexistent_returns_none(self, live_client: HelldiveAPIClient) -> None:
        result = live_client.dispatches.get(999999999)
        assert result is None


# ---------------------------------------------------------------------------
# Planets
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLivePlanetModule:
    def test_get_all_returns_planets(self, live_client: HelldiveAPIClient) -> None:
        planets = live_client.planets.get_all()
        assert isinstance(planets, list)
        assert len(planets) > 0
        for p in planets:
            assert isinstance(p, Planet)

    def test_get_planet_by_index(self, live_client: HelldiveAPIClient) -> None:
        planets = live_client.planets.get_all()
        first = live_client.planets.get(planets[0].index)
        assert isinstance(first, Planet)
        assert first.index == planets[0].index

    def test_get_nonexistent_returns_none(self, live_client: HelldiveAPIClient) -> None:
        result = live_client.planets.get(999999999)
        assert result is None

    def test_get_events_returns_list(self, live_client: HelldiveAPIClient) -> None:
        events = live_client.planets.get_events()
        assert isinstance(events, list)
        for e in events:
            assert isinstance(e, Event)


# ---------------------------------------------------------------------------
# Assignments
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLiveAssignmentsModule:
    def test_get_all_returns_list(self, live_client: HelldiveAPIClient) -> None:
        assignments = live_client.assignments.get_all()
        assert isinstance(assignments, list)
        for a in assignments:
            assert isinstance(a, Assignment)

    def test_get_first_by_index(self, live_client: HelldiveAPIClient) -> None:
        assignments = live_client.assignments.get_all()
        if not assignments:
            pytest.skip("No assignments available.")
        first = live_client.assignments.get(assignments[0].id)
        assert isinstance(first, Assignment)
        assert first.id == assignments[0].id

    def test_get_nonexistent_returns_none(self, live_client: HelldiveAPIClient) -> None:
        result = live_client.assignments.get(999999999)
        assert result is None

    def test_tasks_have_progress_injected(self, live_client: HelldiveAPIClient) -> None:
        assignments = live_client.assignments.get_all()
        if not assignments:
            pytest.skip("No assignments available.")
        for assignment in assignments:
            for task in assignment.tasks:
                assert isinstance(task.progress, int)


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLiveCampaignModule:
    def test_get_all_returns_list(self, live_client: HelldiveAPIClient) -> None:
        campaigns = live_client.campaigns.get_all()
        assert isinstance(campaigns, list)
        for c in campaigns:
            assert isinstance(c, Campaign)

    def test_get_first_by_index(self, live_client: HelldiveAPIClient) -> None:
        campaigns = live_client.campaigns.get_all()
        if not campaigns:
            pytest.skip("No campaigns available.")
        first = live_client.campaigns.get(campaigns[0].id)
        assert isinstance(first, Campaign)
        assert first.id == campaigns[0].id

    def test_get_nonexistent_returns_none(self, live_client: HelldiveAPIClient) -> None:
        result = live_client.campaigns.get(999999999)
        assert result is None

    def test_campaign_has_nested_planet(self, live_client: HelldiveAPIClient) -> None:
        campaigns = live_client.campaigns.get_all()
        if not campaigns:
            pytest.skip("No campaigns available.")
        for campaign in campaigns:
            assert isinstance(campaign.planet, Planet)
            assert campaign.planet.name


# ---------------------------------------------------------------------------
# SpaceStations
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLiveSpaceStationsModule:
    def test_get_all_returns_list(self, live_client: HelldiveAPIClient) -> None:
        stations = live_client.spacestations.get_all()
        assert isinstance(stations, list)
        for s in stations:
            assert isinstance(s, SpaceStation)

    def test_get_first_by_id(self, live_client: HelldiveAPIClient) -> None:
        stations = live_client.spacestations.get_all()
        if not stations:
            pytest.skip("No space stations available.")
        first = live_client.spacestations.get(stations[0].id32)
        assert isinstance(first, SpaceStation)
        assert first.id32 == stations[0].id32

    def test_get_nonexistent_returns_none(self, live_client: HelldiveAPIClient) -> None:
        result = live_client.spacestations.get(999999999)
        assert result is None

    def test_spacestation_has_nested_planet(
        self, live_client: HelldiveAPIClient
    ) -> None:
        stations = live_client.spacestations.get_all()
        if not stations:
            pytest.skip("No space stations available.")
        for station in stations:
            assert isinstance(station.planet, Planet)


# ---------------------------------------------------------------------------
# Steam
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestLiveSteamModule:
    def test_get_all_returns_list(self, live_client: HelldiveAPIClient) -> None:
        news = live_client.steam.get_all()
        assert isinstance(news, list)
        for item in news:
            assert isinstance(item, SteamNews)

    def test_get_first_by_id(self, live_client: HelldiveAPIClient) -> None:
        news = live_client.steam.get_all()
        if not news:
            pytest.skip("No steam news available.")
        first = live_client.steam.get(news[0].id)
        assert isinstance(first, SteamNews)
        assert first.id == news[0].id

    def test_get_nonexistent_returns_none(self, live_client: HelldiveAPIClient) -> None:
        result = live_client.steam.get("000000000000000")
        assert result is None
