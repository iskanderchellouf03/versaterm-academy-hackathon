from src.output.schema import MODULE_SCHEMAS


def get_format_prompt(module_id):
    schema = MODULE_SCHEMAS.get(module_id)
    if not schema:
        return ""

    sections = schema["sections"]
    empty_note = schema["empty_note"]

    section_list = "\n".join(f"{i+1}. ## {s}" for i, s in enumerate(sections))

    return (
        f"\n\nOutput Format Rules:\n"
        f"You MUST structure your output with exactly these sections, "
        f"in this order, using ## headings:\n{section_list}\n\n"
        f"IMPORTANT: Never omit a section. If you have no relevant content "
        f"for a section, include the heading with the note: '{empty_note}'\n\n"
        f"Tone rules:\n"
        f"- Do NOT include any introductory preamble "
        f"(e.g., 'Here is your analysis...')\n"
        f"- Do NOT include any closing sign-off "
        f"(e.g., 'I hope this helps!')\n"
        f"- Do NOT include meta-commentary about your process\n"
        f"- Use direct, active voice with imperative verbs "
        f"(e.g., 'System MUST validate' not 'It would be good if...')\n"
        f"- Use bullet points (-) for enumerable content instead of "
        f"long paragraphs\n"
        f"- Each bullet or paragraph conveys ONE idea — no redundant "
        f"restatements\n\n"
        f"Markdown rules:\n"
        f"- Use ## for top-level sections and ### for subsections\n"
        f"- Use - for unordered lists and 1. for ordered lists\n"
        f"- Use **text** for bold emphasis — never ALL CAPS or underscores\n"
        f"- Never output raw HTML\n"
        f"- Never wrap non-code content in code fences\n"
        f"- Format acceptance criteria with bold keywords: "
        f"**Given** / **When** / **Then**"
    )
