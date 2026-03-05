# Quickstart: Structured Output Formatting

## Overview

This cross-cutting feature provides two functions that every
AI module (004, 006, 008) uses to enforce consistent output
formatting: structured section headings, concise tone, and
clean Markdown.

## Usage

### 1. Get the formatting system prompt

```python
from src.output.prompt import get_system_prompt

# Returns a system prompt fragment with section headings
# and formatting rules for the given module
formatting_instructions = get_system_prompt("004")

# Append to your module's system prompt
full_prompt = my_module_prompt + "\n\n" + formatting_instructions
```

### 2. Normalize LLM output

```python
from src.output.normalizer import normalize_output

# Post-process LLM response: fix Markdown, ensure all
# sections present, insert placeholders for empty sections
clean_output = normalize_output("004", raw_llm_response)

# Display or return clean_output
st.markdown(clean_output)
```

## Integration Pattern

Each AI module follows this flow:

1. Build module-specific prompt (content instructions)
2. Append `get_system_prompt(module_id)` (formatting rules)
3. Call LLM with combined prompt
4. Pass raw response through `normalize_output(module_id, text)`
5. Render or return the cleaned output

## Adding a New Module

To add formatting support for a new AI module:

1. Open `src/output/schema.py`
2. Add a new entry to the `MODULE_SCHEMAS` dictionary:
   ```python
   "NEW_ID": ModuleSectionSchema(
       module_id="NEW_ID",
       module_name="New Module Name",
       sections=["Section A", "Section B", "Section C"],
   )
   ```
3. The prompt builder and normalizer automatically pick up
   the new schema — no other changes needed.

## Testing

```bash
cd src && pytest tests/ -k "output"
```

Verify:
- `get_system_prompt()` returns correct section headings
  for each module
- `normalize_output()` fixes `*` → `-`, strips HTML,
  inserts missing sections
- Output contains all required headings in order
