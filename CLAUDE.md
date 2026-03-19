# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Commands

```bash
uv sync                                                      # install dependencies
uv run ruff check .                                          # lint
uv run ruff format .                                         # format
uv run pyright                                               # type check (strict)
uv run pytest                                                # run tests
uv run pytest tests/path/to/test_file.py::test_name         # run single test
uv run pytest --live                                         # run live API tests (needs network)
uv build                                                     # build package
uv run mkdocs serve                                          # preview docs locally
uv run mkdocs gh-deploy                                      # deploy docs to GitHub Pages
```

## Architecture

**helldive.py** is a typed Python client for the Helldivers 2 community API (`https://api.helldivers2.dev/api`).

### Request flow

```
HelldiveAPIClient → ModuleX → BaseModule._get() → httpx → Pydantic model
```

`BaseModule` (`modules/__init__.py`) provides `_url(path)` and `_get(path, **kwargs)`. Every module inherits it and lives in `src/helldivepy/modules/`.

### Module auto-registration

`HelldiveAPIClient` inspects its own type hints at `__init__` time and instantiates every attribute typed as a `BaseModule` subclass. **No manual registration needed** — declaring a type-annotated attribute on the client is sufficient.

### Modules

| Attribute | Class | Endpoints | Notes |
|---|---|---|---|
| `war` | `WarModule` | `/v1/war` | `get()` only, no `get_all()` |
| `dispatches` | `DispatchesModule` | `/v2/dispatches` | — |
| `planets` | `PlanetModule` | `/v1/planets` | `get_events() -> list[Event]` |
| `campaigns` | `CampaignModule` | `/v1/campaigns` | — |
| `assignments` | `AssignmentsModule` | `/v1/assignments` | — |
| `space_stations` | `SpaceStationsModule` | `/v2/space-stations` | — |
| `steam` | `SteamModule` | `/v1/steam` | `get(gid: str)` takes a string ID |

All modules: `get_all() -> list[T]`, `get(index) -> T | None` (returns `None` on 404, re-raises everything else).

### Data models

All models extend `APIModel` (`models.py`), which configures Pydantic with:
- `alias_generator=to_camel` — automatic camelCase ↔ snake_case aliasing
- `populate_by_name=True` — accepts both forms as input

The API returns HTML span markup in text fields (`<span data-ah="1">text</span>`). These are plain `str` fields — there is no custom markup type.

#### Task parsing

`Task.zip_values` (before-validator) zips the raw parallel `values`/`valueTypes` arrays into `dict[TaskValueType | int, int]`. Unknown type codes stay as raw `int`.

`Assignment.inject_task_progress` (after-validator) distributes `Assignment.progress[i]` into each `Task.progress`, enabling `Task.progress_perc` and `Task.goal`.

#### Community-reverse-engineered enums

`TaskType`, `TaskValueType`, and `CampaignType` in `enums.py` are based on community research and are **incomplete**. Unknown integer codes fall back to raw `int` rather than raising.

### API headers

Every request requires:
- `X-Super-Client` — your application name
- `X-Super-Contact` — contact info (URL or email)

Rate limit: **5 requests per 10 seconds**.

## Testing

### Files

| File | Covers |
|---|---|
| `tests/conftest.py` | Module-level constants + `@pytest.fixture` functions (all deep-copied) |
| `tests/test_models.py` | Pydantic model parsing, camelCase aliasing, nullable fields, validators |
| `tests/test_enums.py` | Every member value, round-trip from int/str, invalid value errors |
| `tests/test_client.py` | Initialization, auto-registration, headers, context manager |
| `tests/test_modules.py` | HTTP methods via `respx_mock` |
| `tests/test_live.py` | Real network calls; skipped by default, run with `--live` |

### Rules

- **New model** → add constant + fixture to `conftest.py`; add tests to `test_models.py`.
- **New enum** → add tests to `test_enums.py` covering every member and round-trip from int/str.
- **New module** → add fixture to `conftest.py`; add tests to `test_modules.py`:
  - `get_all()` — non-empty list, empty list.
  - `get(index)` — success, 404 → `None`, non-404 re-raises `httpx.HTTPStatusError`.
  - Any extra methods (`get_events()`, etc.) — success and empty list.
- **HTTP mocking** — always use the `respx_mock` pytest fixture; never make real network calls in unit tests.
- **Fixture data** — define as module-level constants in `conftest.py`; `copy.deepcopy` in the fixture function.
- **Live tests** — add to `test_live.py` with `@pytest.mark.live`; use a `scope="module"` client fixture; call `pytest.skip()` if the endpoint returns an empty list.

## Tooling

- **Pyright** strict mode — all types must be fully annotated.
- **Ruff** rules: E, F, I, UP, B, SIM — line length 88.
- **Pre-commit** runs ruff + pyright on every commit.
- **Python 3.11+** required.

## Key files

| File | Purpose |
|---|---|
| `src/helldivepy/client.py` | `HelldiveAPIClient` — entry point, auto-registers modules |
| `src/helldivepy/modules/__init__.py` | `BaseModule` abstract base |
| `src/helldivepy/modules/<name>.py` | Module implementations |
| `src/helldivepy/models.py` | All Pydantic models |
| `src/helldivepy/enums.py` | Game enumerations |
| `tests/conftest.py` | Shared fixtures |
| `docs/api/` | MkDocs API reference pages |
| `.github/workflows/ci.yml` | Lint, typecheck, test on Python 3.11/3.12/3.13 |
| `.github/workflows/docs.yml` | Deploy docs to GitHub Pages on push to main |
