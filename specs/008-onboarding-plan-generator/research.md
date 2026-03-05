# Research: Onboarding Plan Generator

## R1 — Input Design: Free-Text vs Dropdown

**Decision**: Role and Product are `st.text_input()` fields
(free text). Level is `st.selectbox()` with three fixed
options (Beginner, Intermediate, Advanced).

**Rationale**: Per spec assumptions, Versaterm has a broad
and evolving set of products and job titles. Fixed dropdowns
would need constant maintenance. Free text lets users enter
any role/product. Level is fixed (3 options) and maps to
distinct prompt behaviors, so a selectbox is appropriate.

**Alternatives considered**:
- Dropdown for all three: Requires maintaining product and
  role lists. Rejected per spec assumption.
- All free text including level: Level has exactly 3 values
  that map to specific prompt instructions. Free text would
  introduce parsing ambiguity. Rejected.
- Autocomplete/suggestions: Adds complexity (suggestion
  list, fuzzy matching). Nice-to-have but rejected for MVP.

## R2 — Prompt Design for 2-Week Plan

**Decision**: System prompt explicitly instructs:
1. Five sections in order (from 014 schema)
2. Learning Plan structured as Day 1-5 (Week 1) and Day 6-10
   (Week 2) with specific activities per day
3. Level adjusts depth: Beginner = fundamentals first,
   Intermediate = assumes basics, Advanced = expert workflows
4. Key Terms minimum 5 entries as term-definition pairs
5. Checkpoints minimum 2 (end of week 1, end of week 2)

**Rationale**: Explicit structure in the prompt produces
consistent day-by-day plans. The LLM naturally adapts
activity complexity based on the stated level. Role and
product provide context for activity types.

**Alternatives considered**:
- Separate LLM calls per section: 5x latency. Rejected.
- Template fill-in (extract activities, fill slots): Loses
  LLM's ability to create coherent, progressive plans.
  Rejected.
- Multi-turn conversation: Over-engineering for MVP. Rejected.

## R3 — Handling Unknown Roles/Products

**Decision**: The prompt includes: "If the role or product
is not recognized, generate a plan based on your best
understanding and note in the output that the plan is based
on inferred knowledge." No validation against a known list.

**Rationale**: The LLM handles unknown inputs gracefully.
It can infer "Support Analyst" means customer-facing support
even if it doesn't know Versaterm's specific title. The spec
explicitly says "best-effort" for unknown inputs (edge case).

**Alternatives considered**:
- Reject unknown roles/products: Too restrictive. Many valid
  titles would fail. Rejected.
- Fuzzy-match against a known list: Requires maintaining the
  list. Rejected per Simplicity First.

## R4 — Resource References in Plans

**Decision**: Generated activities reference generic resources
(e.g., "Review the product's admin guide", "Complete the
onboarding quiz in the LMS") rather than linking to specific
URLs. A note at the end of the plan reminds users to verify
resource availability.

**Rationale**: Per spec, no proprietary Versaterm training
materials are ingested. The LLM doesn't have access to
internal URLs. Generic references are useful enough — the
user/HR supplements with actual links. The note manages
expectations.

**Alternatives considered**:
- Hallucinated URLs: Dangerous — broken links. Rejected.
- No resource references at all: Reduces plan usefulness.
  Generic references are better than none. Rejected.
- Feature 012 (local doc grounding) could enhance this
  later: Out of scope for base 008. Noted as future
  enhancement.

## R5 — Copy and Output Pattern

**Decision**: Same pattern as 004 and 006. Output rendered
with `st.markdown()` for reading, "Copy plan" button for
clipboard. Feature 010 will standardize copy/download later.

**Rationale**: Consistent UX across all three AI modules.
No need for editable output (unlike 006) — onboarding plans
are typically shared as-is with minor manual tweaks outside
the tool.

**Alternatives considered**:
- Editable output like 006: Spec doesn't require it (no
  FR-013 equivalent). Rejected for simplicity.
