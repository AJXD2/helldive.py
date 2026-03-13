# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run pyright

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/path/to/test_file.py::test_function_name

# Build package
uv build
```

## Architecture

**helldive.py** is a Python client library for the Helldivers 2 API (`https://api.helldivers2.dev/api`).

### Module Registration

`HelldiveAPIClient` auto-registers submodules by inspecting its own type annotations. Any attribute typed as a `BaseModule` subclass is automatically instantiated and bound to the client — no manual registration required. This means adding a new module only requires declaring it as a type-annotated attribute on the client.

### Request Flow

```
HelldiveAPIClient → ModuleX (e.g. DispatchesModule) → BaseModule._get() → httpx → Pydantic model
```

`BaseModule` provides `_url()` and `_get()` helpers. All modules inherit from it and live in `src/helldivepy/modules/`.

### Data Models

All models extend `APIModel` (in `models.py`), which configures Pydantic with automatic camelCase ↔ snake_case alias generation. This handles JSON deserialization from the API transparently.

`HDMLString` is a custom type wrapping the game's HDML markup language, with `to_md()` for converting to Markdown.

### Key Files

| File | Purpose |
|---|---|
| `src/helldivepy/client.py` | `HelldiveAPIClient` — main entry point, auto-registers modules |
| `src/helldivepy/modules/__init__.py` | `BaseModule` abstract base |
| `src/helldivepy/modules/[module_name].py` | Specific module implementation |
| `src/helldivepy/models.py` | All Pydantic models + `HDMLString` |
| `src/helldivepy/enums.py` | Game enumerations (`Factions`, `DispatchType`, `RegionSize`) |

### Tooling

- **Pyright** in strict mode — all types must be fully annotated
- **Ruff** rules: E, F, I, UP, B, SIM
- **Python 3.11+** required
- Pre-commit hooks run ruff + pyright automatically
