import copy

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="Run tests that make real HTTP calls to the Helldivers 2 API.",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if not config.getoption("--live"):
        skip = pytest.mark.skip(reason="Pass --live to run live API tests.")
        for item in items:
            if item.get_closest_marker("live"):
                item.add_marker(skip)


STATISTICS = {
    "missionsWon": 100,
    "missionsLost": 10,
    "missionTime": 50000,
    "terminidKills": 9000,
    "automatonKills": 1000,
    "illuminateKills": 500,
    "bulletsFired": 99999,
    "bulletsHit": 88888,
    "timePlayed": 50000,
    "deaths": 300,
    "revives": 50,
    "friendlies": 20,
    "missionSuccessRate": 90,
    "accuracy": 89,
    "playerCount": 5000,
}

WAR = {
    "started": "2024-01-23T20:05:13Z",
    "ended": "2099-01-01T00:00:00Z",
    "now": "2026-03-12T10:00:00Z",
    "clientVersion": "1.0.0",
    "factions": ["Humans", "Terminids"],
    "impactMultiplier": 0.02,
    "statistics": STATISTICS,
}

DISPATCH = {
    "id": 1,
    "published": "2026-03-10T12:00:00Z",
    "type": 0,
    "message": "<i=1>Important alert</i>",
}

REGION = {
    "id": 1,
    "hash": 123456,
    "name": "TEST REGION",
    "description": "A test region.",
    "health": 500000,
    "maxHealth": 1000000,
    "size": "City",
    "regenPerSecond": 1.5,
    "availabilityFactor": 0.8,
    "isAvailable": True,
    "players": 200,
}

REGION_NULLABLE = {
    "id": 0,
    "hash": 987654,
    "name": None,
    "description": None,
    "health": None,
    "maxHealth": 600000,
    "size": "MegaCity",
    "regenPerSecond": None,
    "availabilityFactor": None,
    "isAvailable": False,
    "players": 0,
}

EVENT = {
    "id": 99,
    "eventType": 1,
    "faction": "Automaton",
    "health": 300000,
    "maxHealth": 500000,
    "startTime": "2026-03-10T12:00:00Z",
    "endTime": "2026-03-17T12:00:00Z",
    "campaignId": 55,
    "jointOperationIds": [1, 2],
}

PLANET = {
    "index": 42,
    "name": "HELLMIRE",
    "sector": "Kaus Australis",
    "biome": {"name": "Scorched", "description": "Hot and fiery."},
    "hazards": [{"name": "Fire Tornadoes", "description": "Deadly fire tornadoes."}],
    "hash": 111222333,
    "position": {"x": 0.5, "y": -0.3},
    "waypoints": [10, 20],
    "maxHealth": 1000000,
    "health": 750000,
    "disabled": False,
    "initialOwner": "Humans",
    "currentOwner": "Terminids",
    "regenPerSecond": 2.5,
    "event": None,
    "statistics": STATISTICS,
    "attacking": [15],
    "regions": [],
}

PLANET_WITH_EVENT = {
    **PLANET,
    "event": EVENT,
}

CAMPAIGN = {
    "id": 5,
    "planet": PLANET,
    "type": 0,
    "count": 3,
    "faction": "Terminids",
}

KILL_TASK = {
    "type": 3,
    "values": [3, 1, 100000, 111222333, 0, 0, 0, 0, 0, 0],
    "valueTypes": [1, 2, 3, 4, 6, 5, 8, 9, 11, 12],
}

LIBERATE_TASK = {
    "type": 11,
    "values": [1, 1, 42],
    "valueTypes": [3, 11, 12],
}

ASSIGNMENT = {
    "id": 9001,
    "progress": [50000, 0],
    "title": "MAJOR ORDER",
    "briefing": "Destroy the cyborg megafactories.",
    "description": None,
    "tasks": [KILL_TASK, LIBERATE_TASK],
    "reward": {"type": 1, "amount": 50},
    "rewards": [{"type": 1, "amount": 50}],
    "expiration": "2026-03-16T16:38:53.254825Z",
    "flags": 0,
}


@pytest.fixture
def raw_statistics() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(STATISTICS)


@pytest.fixture
def raw_war() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(WAR)


@pytest.fixture
def raw_dispatch() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(DISPATCH)


@pytest.fixture
def raw_region() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(REGION)


@pytest.fixture
def raw_region_nullable() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(REGION_NULLABLE)


@pytest.fixture
def raw_event() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(EVENT)


@pytest.fixture
def raw_planet() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(PLANET)


@pytest.fixture
def raw_planet_with_event() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(PLANET_WITH_EVENT)


@pytest.fixture
def raw_campaign() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(CAMPAIGN)


@pytest.fixture
def raw_kill_task() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(KILL_TASK)


@pytest.fixture
def raw_liberate_task() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(LIBERATE_TASK)


@pytest.fixture
def raw_assignment() -> dict:  # type: ignore[type-arg]
    return copy.deepcopy(ASSIGNMENT)
