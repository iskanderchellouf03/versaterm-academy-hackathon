# Data Model: Demo Scope Banner

No persistent data. Minimal session state.

## Session State

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| banner_dismissed | bool | False | Whether user has dismissed the banner this session |

## Configuration

| Constant | Location | Value |
|----------|----------|-------|
| DEMO_BANNER_TEXT | config.py | "Demo — This is a prototype. No data is persisted. All information is local to your current session." |

## State Transitions

```
[Page load]
  → Check st.session_state.get("banner_dismissed", False)
  → If False: render banner with dismiss button
  → If True: skip banner rendering

[User clicks Dismiss]
  → st.session_state["banner_dismissed"] = True
  → st.rerun() → banner no longer rendered

[New session (new tab / re-auth)]
  → banner_dismissed defaults to False → banner shown again
```

## Relationships

- Called from `app.py` before auth gate (visible on login)
- Compatible with 013-branded-theme (banner renders above
  themed header)
- No dependency on any AI module
