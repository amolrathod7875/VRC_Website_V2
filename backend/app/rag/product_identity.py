from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple


PRODUCT_ALIASES: Dict[str, Dict[str, object]] = {
    "tiger": {
        "canonical_slug": "tiger",
        "aliases": [
            "tiger",
            "tiger pump",
            "tiger 30:150",
        ],
    },
    "lion": {
        "canonical_slug": "lion",
        "aliases": [
            "lion",
            "lion pump",
            "lion_catalogue",
            "lion catalogue",
        ],
    },
    "rhino": {
        "canonical_slug": "rhino",
        "aliases": [
            "rhino",
            "rhino pump",
        ],
    },
    "elephant": {
        "canonical_slug": "elephant",
        "aliases": [
            "elephant",
            "elephant pump",
        ],
    },
    "hippo": {
        "canonical_slug": "hippo",
        "aliases": [
            "hippo",
            "hippo pump",
            "diaphragm pump",
        ],
    },
    "leopard": {
        "canonical_slug": "leopard",
        "aliases": [
            "leopard",
            "leopard electric pump",
            "electric pump",
        ],
    },
    "filters": {
        "canonical_slug": "filters",
        "aliases": [
            "filters",
            "filter",
            "vr filters",
        ],
    },
}

# Ordered so longer aliases match before shorter ones to avoid partial collisions.
_ALIAS_ORDER: List[str] = sorted(
    {
        alias.lower()
        for config in PRODUCT_ALIASES.values()
        for alias in config.get("aliases", [])
    },
    key=len,
    reverse=True,
)

_MODEL_PATTERN = re.compile(r"\b([A-Za-z]+)?\s*(\d+:\d+)\b", re.IGNORECASE)


def resolve_product_identity(text: str) -> Optional[Tuple[str, Optional[str]]]:
    """Return (canonical_slug, matched_alias_or_None) for the first product found in text.

    Matching is deterministic and case-insensitive. If no known product is found, return None.
    """
    if not text:
        return None

    normalized = text.lower()
    for alias in _ALIAS_ORDER:
        if alias in normalized:
            for slug, config in PRODUCT_ALIASES.items():
                if alias in [a.lower() for a in config.get("aliases", [])]:
                    return slug, alias
    return None


def get_canonical_slug(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    result = resolve_product_identity(raw)
    if not result:
        return None
    return result[0]


def extract_model_identifier(text: str) -> Optional[str]:
    if not text:
        return None
    match = _MODEL_PATTERN.search(text)
    if not match:
        return None
    return match.group(2)
