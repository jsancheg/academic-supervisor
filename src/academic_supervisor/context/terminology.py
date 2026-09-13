import re

VARIANT_GROUPS: dict[str, list[str]] = {
    "email": ["email", "e-mail"],
    "dataset": ["dataset", "data set", "data-set"],
    "colour": ["colour", "color"],
    "coordinate": ["coordinate", "co-ordinate"],
    "organise": ["organise", "organize"],
    "analyse": ["analyse", "analyze"],
}


def build_terminology_map(paragraphs: list[str]) -> dict[str, dict[str, list[int]]]:
    terminology_map: dict[str, dict[str, list[int]]] = {}

    for canonical, variants in VARIANT_GROUPS.items():
        occurrences: dict[str, list[int]] = {}
        for variant in variants:
            pattern = re.compile(rf"\b{re.escape(variant)}\b", re.IGNORECASE)
            indices = [i for i, paragraph in enumerate(paragraphs) if pattern.search(paragraph)]
            if indices:
                occurrences[variant] = indices

        if len(occurrences) > 1:
            terminology_map[canonical] = occurrences

    return terminology_map
