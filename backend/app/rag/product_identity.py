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
    "paint-preparation-unit": {
        "canonical_slug": "paint-preparation-unit",
        "aliases": [
            "paint preparation unit",
            "paint prep unit",
            "drum heater",
            "drum jacket",
        ],
    },
    "portable-pressure-feed-pot": {
        "canonical_slug": "portable-pressure-feed-pot",
        "aliases": [
            "portable pressure feed pot",
            "pressure feed pot",
            "portable pressure pot",
        ],
    },
    "turbine": {
        "canonical_slug": "turbine",
        "aliases": [
            "turbine",
            "turbine stirrer",
            "turbine stirrer series",
            "paint agitation system",
        ],
    },
    "cub": {
        "canonical_slug": "cub",
        "aliases": [
            "cub",
            "cub pump",
            "four-ball piston pump",
            "cub 2:400",
            "cub 4:400",
            "cub 6:400",
        ],
    },
    "drum-press": {
        "canonical_slug": "drum-press",
        "aliases": [
            "drum press",
            "drum-press",
            "drum press dispensing",
            "airless drum press",
        ],
    },
    "pneumatic-stirrer": {
        "canonical_slug": "pneumatic-stirrer",
        "aliases": [
            "pneumatic stirrer",
            "pneumatic stirrers",
            "air stirrer",
            "pneumatic driven stirrer",
        ],
    },
    "ball-valves": {
        "canonical_slug": "ball-valves",
        "aliases": [
            "ball valves",
            "ball valve",
            "high pressure ball valve",
            "high pressure ball valves",
        ],
    },
    "automatic-spray-guns": {
        "canonical_slug": "automatic-spray-guns",
        "aliases": [
            "automatic spray guns",
            "automatic gun",
            "automatic_gun",
            "automatic spray painting gun",
            "automatic spray painting guns",
        ],
    },
    "kingfisher": {
        "canonical_slug": "kingfisher",
        "aliases": [
            "kingfisher",
            "kingfisher silver",
            "kingfisher blue",
            "kingfisher red",
            "kingfisher gold",
            "conventional guns",
            "conventional gun",
        ],
    },
    "manual-spray-guns": {
        "canonical_slug": "manual-spray-guns",
        "aliases": [
            "manual spray guns",
            "manual gun",
            "manual_guns",
            "manual spray painting guns",
            "manual spray painting gun",
        ],
    },
    "vria": {
        "canonical_slug": "vria",
        "aliases": [
            "vria",
            "vria aluminium",
            "vria stainless steel",
            "vria ss",
            "vria al",
        ],
    },
    "vriad": {
        "canonical_slug": "vriad",
        "aliases": [
            "vriad",
            "vriad aluminium",
            "vriad stainless steel",
            "vriad ss",
            "vriad al",
        ],
    },
    "400b": {
        "canonical_slug": "400b",
        "aliases": [
            "400b",
            "400 b",
        ],
    },
    "hotmelt-dispenser": {
        "canonical_slug": "hotmelt-dispenser",
        "aliases": [
            "hotmelt",
            "hot melt",
            "hotmelt dispensing gun",
            "hot melt dispensing gun",
        ],
    },
    "flamingo": {
        "canonical_slug": "flamingo",
        "aliases": [
            "flamingo",
            "flamingo gun",
        ],
    },
    "am250": {
        "canonical_slug": "am250",
        "aliases": [
            "am250",
            "am 250",
        ],
    },
    "vril": {
        "canonical_slug": "vril",
        "aliases": [
            "vril",
        ],
    },
    "eagle": {
        "canonical_slug": "eagle",
        "aliases": [
            "eagle",
            "eagle gun",
        ],
    },
    "falcon": {
        "canonical_slug": "falcon",
        "aliases": [
            "falcon",
            "falcon gun",
        ],
    },
    "ext-i": {
        "canonical_slug": "ext-i",
        "aliases": [
            "ext-i",
            "ext i",
            "extrusion gun",
            "extrusion gun ext-i",
        ],
    },
    "hawk": {
        "canonical_slug": "hawk",
        "aliases": [
            "hawk",
            "hawk gun",
            "dispensing gun hawk",
        ],
    },
    "wax-spray-gun": {
        "canonical_slug": "wax-spray-gun",
        "aliases": [
            "wax spray gun",
            "wax gun",
        ],
    },
    "pole-gun": {
        "canonical_slug": "pole-gun",
        "aliases": [
            "pole gun",
            "polegun",
        ],
    },
    "barrel-pump": {
        "canonical_slug": "barrel-pump",
        "aliases": [
            "barrel pump",
            "barrel-pump",
            "barrel pump 210 liters",
        ],
    },
    "vrid": {
        "canonical_slug": "vrid",
        "aliases": [
            "vrid",
            "vrid gun",
            "airless manual dispensing gun vrid",
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

    Matching is deterministic and case-insensitive. Whitespace is normalized so that
    aliases match even when words are split across lines or separated by extra spaces.
    If no known product is found, return None.
    """
    if not text:
        return None

    normalized = " ".join(text.lower().split())
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
