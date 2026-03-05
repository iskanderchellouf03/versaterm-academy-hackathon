import re

from src.output.schema import MODULE_SCHEMAS


def ensure_sections(module_id, text):
    schema = MODULE_SCHEMAS.get(module_id)
    if not schema:
        return text

    sections = schema["sections"]
    empty_note = schema["empty_note"]

    for section in sections:
        pattern = re.compile(rf"^## {re.escape(section)}\s*$", re.MULTILINE)
        if not pattern.search(text):
            text = text.rstrip() + f"\n\n## {section}\n\n{empty_note}\n"

    return text


def normalize_markdown(text):
    # Split into code-fenced and non-fenced segments
    parts = re.split(r"(```[\s\S]*?```)", text)
    result = []
    for i, part in enumerate(parts):
        if part.startswith("```"):
            result.append(part)
            continue

        # Replace * list markers with -
        part = re.sub(r"^(\s*)\* ", r"\1- ", part, flags=re.MULTILINE)

        # Strip raw HTML tags
        part = re.sub(r"<[^>]+>", "", part)

        # Normalize __text__ bold to **text**
        part = re.sub(r"__(.+?)__", r"**\1**", part)

        # Normalize section headings to ## (not # or ####)
        part = re.sub(r"^#{1}(?!#)\s+", "## ", part, flags=re.MULTILINE)
        part = re.sub(r"^#{4,}\s+", "### ", part, flags=re.MULTILINE)

        result.append(part)

    text = "".join(result)

    # Remove code fences without language that wrap only prose
    text = re.sub(
        r"```\n((?:(?!```)[^\n]*\n)*?)```",
        lambda m: m.group(1) if not any(
            line.strip().startswith(("def ", "class ", "import ", "from ", "if ", "for ", "while ", "return ", "{", "}", "//", "/*", "#include"))
            for line in m.group(1).split("\n") if line.strip()
        ) else m.group(0),
        text,
    )

    return text
