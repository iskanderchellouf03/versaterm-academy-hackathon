# Data Model: App Shell Layout with Sidebar Navigation

This feature has no persistent data entities. All state is
in-memory via Streamlit session state.

## Session State: Active Module

| Field | Type | Description |
|-------|------|-------------|
| active_module | string | Display name of the currently selected module |

### Default Value

On page load (or after refresh), `active_module` defaults to
the first entry in the `MODULES` registry dict.

## Configuration Entity: Module Registry

Defined in `src/pages/__init__.py` as an ordered dict.

| Field | Type | Description |
|-------|------|-------------|
| key (display name) | string | Module name shown in sidebar (e.g., "Requirement Analyzer") |
| value (render fn) | callable | Function that renders the module's content |

### Initial Module List

| Display Name | Render Function | Source Feature |
|-------------|-----------------|----------------|
| Requirement Analyzer | `placeholder` | 004 (not yet implemented) |
| KB Article Generator | `placeholder` | 006 (not yet implemented) |
| Onboarding Planner | `placeholder` | 008 (not yet implemented) |

All modules initially point to the shared placeholder
renderer. Each module's feature (004, 006, 008) replaces the
placeholder with its real render function upon implementation.

## Relationships

- `active_module` value MUST be a valid key in the `MODULES`
  dict.
- Auth gate (001) MUST pass before the shell renders.
- Sign-out button (002) is placed in the sidebar below the
  module list.
