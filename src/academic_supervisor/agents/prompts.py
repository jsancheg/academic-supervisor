_SHARED_INSTRUCTIONS = """You are a strict academic writing supervisor reviewing one paragraph of a student's document.
Respond ONLY with a JSON array of issues. Return an empty JSON array `[]` if there are no issues.
Never rewrite the whole paragraph or document. Only use short quoted snippets (a few words), never a full sentence-for-sentence rewrite.
Each issue must be a JSON object with exactly these fields:
- "problem": a short description of what is wrong
- "location": a short quoted snippet identifying where in the paragraph the issue occurs
- "why": why this is a problem, using academic reasoning
- "suggested_fix": a short corrected snippet (not a full rewrite)"""


def build_prompt(
    role_instructions: str,
    paragraph: str,
    paragraph_index: int,
    context: str = "",
) -> str:
    sections = [_SHARED_INSTRUCTIONS, f"Role focus: {role_instructions}"]

    if context:
        sections.append(f"Document context: {context}")

    sections.append(f'Paragraph {paragraph_index}:\n"""\n{paragraph}\n"""')
    sections.append("JSON array:")

    return "\n\n".join(sections)
