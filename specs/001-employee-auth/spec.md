# Feature Specification: Employee Email & Access Code Authentication

**Feature Branch**: `001-employee-auth`
**Created**: 2026-03-04
**Status**: Draft
**Input**: User description: "As a Versaterm employee, I want to enter my company email and a one-time access code so only authorized staff can access the web app without external SSO."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Employee Login with Access Code (Priority: P1)

An employee navigates to the web app and sees a login screen.
They enter their Versaterm company email address. The system
validates the email domain and sends a one-time access code to
that address. The employee checks their inbox, copies the code,
enters it into the verification field, and gains access to the
application. Their session remains active until they log out or
the session expires.

**Why this priority**: This is the core authentication gate.
Without it, the app is either open to everyone or completely
inaccessible. Every other feature depends on this working.

**Independent Test**: Can be fully tested by navigating to the
app, entering a valid company email, receiving the code, and
entering it. Delivers secure access control as a standalone
capability.

**Acceptance Scenarios**:

1. **Given** an unauthenticated employee visits the app,
   **When** they enter a valid `@versaterm.com` email,
   **Then** the system sends a one-time access code to that
   email and displays a code entry form.

2. **Given** the employee has received a one-time code,
   **When** they enter the correct code within the validity
   window,
   **Then** they are authenticated and redirected to the main
   application.

3. **Given** the employee has received a one-time code,
   **When** they enter an incorrect code,
   **Then** the system displays an error message and allows
   them to retry.

4. **Given** the employee enters an email that is not a
   recognized company domain,
   **When** they submit the email,
   **Then** the system rejects the request with a clear
   message that only company email addresses are accepted.

---

### User Story 2 - Session Persistence (Priority: P2)

After a successful login, the employee can navigate across
pages and return to the app within a reasonable time window
without re-authenticating. Their session expires after a period
of inactivity, at which point they MUST re-authenticate.

**Why this priority**: Without session persistence, employees
would need to re-enter a code on every page load, making the
app unusable. This is essential for a functional experience but
depends on US1 being in place first.

**Independent Test**: After completing US1 login, close the
browser tab, reopen it within the session window, and confirm
access is retained without re-authentication.

**Acceptance Scenarios**:

1. **Given** an authenticated employee,
   **When** they navigate between pages within the app,
   **Then** they remain authenticated without re-entering
   credentials.

2. **Given** an authenticated employee whose session has been
   inactive beyond the timeout period,
   **When** they attempt to access any page,
   **Then** they are redirected to the login screen and MUST
   re-authenticate.

3. **Given** an authenticated employee,
   **When** they click "Log out",
   **Then** their session is terminated and they are returned
   to the login screen.

---

### User Story 3 - Code Expiry and Rate Limiting (Priority: P3)

One-time access codes expire after a short validity window.
If an employee requests too many codes in a short period, the
system temporarily blocks further requests to prevent abuse.

**Why this priority**: Hardening against misuse. The app is
functional without this (US1 + US2), but this prevents brute
force attacks and stale code reuse. Important for security
posture but not a blocker for the demo flow.

**Independent Test**: Request a code, wait beyond the expiry
window, and confirm the expired code is rejected. Then request
codes rapidly and confirm the rate limit kicks in.

**Acceptance Scenarios**:

1. **Given** an employee has received a one-time code,
   **When** they enter the code after the validity window has
   passed,
   **Then** the system rejects the code and prompts them to
   request a new one.

2. **Given** an employee has requested multiple codes in rapid
   succession,
   **When** they exceed the rate limit threshold,
   **Then** the system temporarily blocks further code
   requests and displays a "try again later" message.

---

### Edge Cases

- What happens when an employee enters a valid company email
  that does not belong to an actual employee? The system sends
  the code regardless (the email domain is the trust boundary,
  not an employee directory lookup).
- What happens if the email delivery is delayed or fails? The
  employee can request a new code after the previous one
  expires. The UI MUST provide a "Resend code" option.
- What happens if the employee has multiple unexpired codes?
  Only the most recently issued code is valid; all prior codes
  are invalidated upon issuing a new one.
- What happens on concurrent sessions from different devices?
  Each device maintains its own independent session.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST present a login screen as the
  default entry point for unauthenticated users.
- **FR-002**: System MUST accept only email addresses matching
  an allowed company domain (e.g., `@versaterm.com`).
- **FR-003**: System MUST generate a one-time access code and
  deliver it to the submitted email address.
- **FR-004**: One-time codes MUST be single-use; a code is
  invalidated after successful authentication or after a new
  code is issued to the same email.
- **FR-005**: One-time codes MUST expire after 10 minutes.
- **FR-006**: System MUST allow a maximum of 5 code requests
  per email address within a 15-minute window.
- **FR-007**: System MUST maintain an authenticated session
  after successful code verification.
- **FR-008**: Sessions MUST expire after 8 hours of inactivity.
- **FR-009**: System MUST provide a "Log out" action that
  terminates the current session.
- **FR-010**: System MUST reject authentication attempts with
  invalid, expired, or already-used codes and display a
  user-friendly error message.
- **FR-011**: All pages except the login screen MUST be
  inaccessible to unauthenticated users.

### Key Entities

- **Employee Session**: Represents an authenticated user's
  active session. Attributes: email address, session start
  time, last activity time, active/expired status.
- **Access Code**: A short-lived token tied to an email
  address. Attributes: code value, associated email, issued
  timestamp, expiry timestamp, used/unused status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Employees can complete the full login flow
  (email entry through code verification) in under 2 minutes,
  excluding email delivery time.
- **SC-002**: 100% of unauthenticated requests to protected
  pages are redirected to the login screen.
- **SC-003**: Expired or invalid codes are rejected 100% of
  the time.
- **SC-004**: 95% of employees successfully authenticate on
  their first attempt (correct code entered once).
- **SC-005**: Rate limiting activates correctly when the
  threshold is exceeded, blocking further requests.

## Assumptions

- The allowed email domain is `@versaterm.com`. If additional
  domains are needed, this can be configured later.
- Email delivery is handled by a standard transactional email
  service; delivery reliability is outside the scope of this
  feature.
- No employee directory or user provisioning is required; any
  valid company-domain email is accepted.
- The access code format is a 6-digit numeric code (common,
  user-friendly default).
- Session timeout of 8 hours aligns with a standard workday.
