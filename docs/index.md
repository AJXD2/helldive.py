# helldive.py

A Python client library for the [Helldivers 2 API](https://helldivers-2.github.io/api/).

> **Note:** Some parts of the API have been reverse-engineered by the community and may not perfectly reflect the current state of the game.

## Installation

```bash
pip install helldivepy
```

Requires Python 3.11+.

## Quick Start

```python
from helldivepy import HelldiveAPIClient

# The API requires X-Super-Client and X-Super-Contact headers for rate-limiting.
with HelldiveAPIClient(
    client="my-app",
    contact="me@example.com",
) as client:
    # Global war status
    war = client.war.get()
    print(war.now)
    print(war.statistics.player_count)

    # Recent dispatches
    for dispatch in client.dispatches.get_all()[:3]:
        print(dispatch.message)

    # All planets
    planets = client.planets.get_all()
    for planet in planets:
        if planet.event:
            print(f"{planet.name} is under attack by {planet.event.faction}")
```

## Modules

| Attribute | Methods |
|---|---|
| `client.war` | `get() -> War` |
| `client.dispatches` | `get_all() -> list[Dispatch]`, `get(index) -> Dispatch \| None` |
| `client.planets` | `get_all() -> list[Planet]`, `get(index) -> Planet \| None`, `get_events() -> list[Event]` |
| `client.campaigns` | `get_all() -> list[Campaign]`, `get(index) -> Campaign \| None` |
| `client.assignments` | `get_all() -> list[Assignment]`, `get(index) -> Assignment \| None` |
| `client.space_stations` | `get_all() -> list[SpaceStation]`, `get(index) -> SpaceStation \| None` |
| `client.steam` | `get_all() -> list[SteamNews]`, `get(gid) -> SteamNews \| None` |
