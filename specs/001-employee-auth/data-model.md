# Data Model: Employee Email & Access Code Authentication

**Feature**: 001-employee-auth
**Date**: 2026-03-04

## Entities

### AccessCode

Represents a one-time access code issued to an email address.

| Field      | Type     | Description                          |
|------------|----------|--------------------------------------|
| id         | integer  | Auto-incrementing primary key        |
| email      | text     | Employee email address (lowercase)   |
| code       | text     | 6-digit zero-padded numeric code     |
| created_at | datetime | UTC timestamp when code was issued   |
| expires_at | datetime | UTC timestamp when code expires      |
| used       | boolean  | Whether the code has been consumed   |

**Constraints**:
- `email` MUST match an allowed domain pattern.
- `code` MUST be exactly 6 characters.
- `expires_at` = `created_at` + 10 minutes.
- When a new code is issued to an email, all prior unused
  codes for that email are marked as used (invalidated).

**State transitions**:
- Created → Used (successful verification)
- Created → Expired (time elapsed past `expires_at`)
- Created → Invalidated (new code issued to same email)

### Session (in-memory via Streamlit session_state)

Represents an authenticated user's active session. Not
persisted to database — lives in Streamlit's server-side
session state per browser tab.

| Field          | Type     | Description                        |
|----------------|----------|------------------------------------|
| authenticated  | boolean  | Whether user has verified a code   |
| email          | text     | Authenticated user's email address |
| login_time     | datetime | UTC timestamp of authentication    |
| last_activity  | datetime | UTC timestamp of last page access  |

**Constraints**:
- Session expires when `now - last_activity > 8 hours`.
- Logout clears all session fields.
- `last_activity` is updated on every page load.

## Relationships

- One email can have many AccessCode records (historical).
- Only the most recent unused, unexpired code for an email
  is considered valid.
- A Session references an email but has no direct foreign key
  to AccessCode (stateless after verification).

## Rate Limiting (derived from AccessCode table)

Rate limiting is not a separate entity. It is computed by
counting AccessCode rows where:
- `email` matches the requesting address
- `created_at` is within the last 15 minutes

If count >= 5, the request is blocked.
