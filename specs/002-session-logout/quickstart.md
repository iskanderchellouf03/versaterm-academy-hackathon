# Quickstart: Session Sign-Out

## Overview

Adds a "Sign out" button to the sidebar that clears session
state and returns the user to the login screen.

## Prerequisites

- Feature 001-employee-auth must be implemented (provides
  the session model and login screen).

## How It Works

1. User clicks "Sign out" in the sidebar
2. `logout()` clears auth keys from `st.session_state`
3. `st.rerun()` restarts the script
4. Auth gate in `app.py` sees no session → shows login screen

## Code Location

- `src/auth/service.py` — `logout()` function
- `src/app.py` — Sidebar button wiring

## Usage

```python
from src.auth.service import logout

# In the sidebar (app.py)
with st.sidebar:
    if st.button("Sign out"):
        logout()
```

## Testing

```bash
cd src && pytest tests/ -k "logout"
```

Verify:
- After `logout()`, `st.session_state` has no `authenticated`
  or `user_email` keys
- The auth gate redirects to login when session is cleared
- Sign-out button renders in the sidebar on all authenticated
  pages
