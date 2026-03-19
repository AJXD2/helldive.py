# helldive.py

A Python client library for the [Helldivers 2 API](https://helldivers-2.github.io/api/).

> **Note:** Some parts of the API have been reverse-engineered and may not reflect the current state of the game.

---

## Installation

```bash
pip install helldivepy
```

Requires Python 3.11+.

---

## Quick Start

```python
from helldivepy import HelldiveAPIClient
# api.helldivers2.dev requires a contact and a client ID in the X-Super-Contact and X-Super-Client headers for rate-limiting purposes. This is required by the API and can be any contact  (e.g. aj@ajxd2.dev,github/ajxd2,discord/ajxd2, etc).
client = HelldiveAPIClient(
    client="my-app",       # X-Super-Client header
    contact="me@example.com",  # X-Super-Contact header (required by the API)
)

# Get global war status
war = client.war.get()
print(war.now)                          # datetime
print(war.statistics.player_count)     # int

# Get recent dispatches
dispatches = client.dispatches.get_all()
for d in dispatches[:3]:
    print(d.message.to_md())           # converts HDML markup to HTML spans
```

---

## Modules

| Module | Status | Methods |
|---|---|---|
| `client.war` | ✅ Done | `get() -> War` |
| `client.dispatches` | ✅ Done | `get_all() -> list[Dispatch]`, `get(index) -> Dispatch \| None` |
| `client.planets` | ✅ Done | `get_all() -> list[Planet]`, `get(index) -> Planet` |
| `client.campaigns` | ✅ Done | `get_all() -> list[Campaign]`, `get(index) -> Campaign` |
| `client.assignments` | ✅ Done | `get_all() -> list[Assignment]`, `get(index) -> Assignment` |
| `client.space_stations` | ✅ Done | `get_all() -> list[SpaceStation]`, `get(index) -> SpaceStation` |
| `client.steam` | ✅ Done | `get_all() -> list[SteamNews]`, `get(gid) -> SteamNews` |

---

## Models

All models use automatic camelCase ↔ snake_case aliasing, so API responses deserialize transparently.

### Key models

**`Planet`** — full planet state including health, owner, biome, hazards, regions, and an optional active `Event`.

```python
planet = client.planets.get(42)  # coming soon
print(planet.name)
print(planet.current_owner)       # Factions.Terminids
print(planet.health / planet.max_health)
if planet.event:
    print(planet.event.faction, planet.event.end_time)
```

**`Assignment`** (Major Orders) — tasks with parsed progress.

```python
assignments = client.assignments.get_all()  # coming soon
for assignment in assignments:
    print(assignment.title, assignment.expiration)
    for task in assignment.tasks:
        if not task.is_liberation_task:
            print(f"  {task.progress_perc:.1f}% of {task.goal:,}")
```

**`Dispatch`** — in-game broadcasts with HDML (HellDivers Markup Language) markup.

```python
dispatches = client.dispatches.get_all()
latest = dispatches[0]
print(latest.message.to_md())                       # inline styles
print(latest.message.to_md(use_classes=True))       # CSS classes
```

---

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint + format
uv run ruff check .
uv run ruff format .

# Type check
uv run pyright
```

---

## Thanks
Thanks to the devs of the [Community API](https://github.com/helldivers-2/api) for keeping a well maintained and easy to use API.
- [dealloc](https://github.com/dealloc) 
- [lambstream](https://github.com/lambstream)
- [TheWizardofGauze](https://github.com/TheWizardofGauze)

---

## License

MIT
