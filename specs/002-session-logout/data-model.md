# Data Model: Session Sign-Out

This feature introduces no new data entities. It operates on
the existing session model from 001-employee-auth.

## Existing Entity: Employee Session (from 001)

Stored in `st.session_state` (in-memory, per-tab).

| Field | Type | Description |
|-------|------|-------------|
| authenticated | bool | Whether the user has passed the auth gate |
| user_email | string | The verified employee email address |

## State Transition

```
authenticated=True  →  [Sign out click]  →  Keys cleared  →  st.rerun()  →  Login screen
```

### Logout Operation

The `logout()` function performs:

1. Delete `st.session_state["authenticated"]`
2. Delete `st.session_state["user_email"]`
3. Delete any other auth-related keys (future-proofed
   by iterating over a defined list of auth keys)
4. Call `st.rerun()` to restart the script

### Post-Logout State

After logout, `st.session_state` no longer contains
`authenticated` or `user_email`. The auth gate in `app.py`
checks `st.session_state.get("authenticated", False)` and
renders the login screen.

## Relationships

- Depends on 001-employee-auth session model (must exist).
- No database changes. No new tables or columns.
