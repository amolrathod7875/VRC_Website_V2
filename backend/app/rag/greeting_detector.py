import re
from typing import Optional


_GREETING_PATTERNS = [
    # General greetings
    re.compile(r"^(hi+|hii+|hiii+)[\s!.,;:?)]*$", re.IGNORECASE),
    re.compile(r"^(hello)[\s!.,;:?)]*$", re.IGNORECASE),
    re.compile(r"^(hey+|heyy+)[\s!.,;:?)]*$", re.IGNORECASE),
    re.compile(r"^(hey\s+there|hello\s+there)[\s!.,;:?)]*$", re.IGNORECASE),
    re.compile(r"^(good\s+(morning|afternoon|evening))[\s!.,;:?)]*$", re.IGNORECASE),
    re.compile(r"^(morning|afternoon|evening)[\s!.,;:?)]*$", re.IGNORECASE),
    re.compile(r"^(namaste|namaskar)[\s!.,;:?)]*$", re.IGNORECASE),
    re.compile(r"^(yo|sup)[\s!.,;:?)]*$", re.IGNORECASE),
    # What's up (colloquial greeting)
    re.compile(r"^((what'?s\s+up)|(whats\s+up))[\s!.,;:?)]*$", re.IGNORECASE),
    # How are you
    re.compile(r"^(how\s+are\s+you(\s+doing)?|how'?s\s+it\s+going)[\s!.,;:?)]*$", re.IGNORECASE),
    # Thanks
    re.compile(r"^(thanks|thankyou|thank\s*you|ok\s*thanks|okay\s*thanks|thx)[\s!.,;:?)]*$", re.IGNORECASE),
    # Bye
    re.compile(r"^(bye|goodbye|see\s+you|good\s+night)[\s!.,;:?)]*$", re.IGNORECASE),
]

# Patterns that indicate the message contains a real query beyond a pure greeting.
_NON_GREETING_INDICATORS = [
    # Product names
    "tiger", "lion", "rhino", "elephant", "hippo", "leopard", "filters",
    # Question starters / query indicators
    " what ", " where ", " when ", " why ", " who ", " which ",
    " tell ", " describe ", " explain ", " show ", " list ", " compare ", " vs ",
    " need ", " want ", " looking ", " about ", " help ", " price ", " cost ",
    # Technical terms
    "pressure ratio", "output", "flow rate", "viscosity", "max pressure",
    # Model identifier pattern like "30:150", "75:210"
    re.compile(r"\b\d+:\d+\b"),
]


def normalize_for_greeting(text: str) -> str:
    """Normalize text for greeting detection without over-normalizing product strings."""
    stripped = text.strip()
    lowered = stripped.lower()
    # Collapse repeated letters only at the start of known greeting words.
    lowered = re.sub(r"\b(hi+)\b", "hi", lowered)
    lowered = re.sub(r"\b(hey+)\b", "hey", lowered)
    lowered = re.sub(r"\b(hello+)\b", "hello", lowered)
    # Remove leading/trailing simple punctuation and closing parens.
    lowered = lowered.strip("!.,;:? )")
    return lowered


def _has_non_greeting_content(text: str) -> bool:
    """Return True if the message contains content beyond a pure greeting."""
    normalized = f" {text.lower()} "
    for indicator in _NON_GREETING_INDICATORS:
        if isinstance(indicator, re.Pattern):
            if indicator.search(normalized):
                return True
        elif indicator in normalized:
            return True
    return False


def classify_greeting(text: str) -> Optional[str]:
    """Return a greeting category if the text is a pure greeting, else None.

    The function is conservative: it only returns a category when the message
    is essentially conversational and contains no real query content.
    """
    normalized = normalize_for_greeting(text)
    for pattern in _GREETING_PATTERNS:
        match = pattern.match(normalized)
        if match:
            # The matched portion must consume the entire normalized text.
            if match.group(0) != normalized:
                continue
            # If the matched greeting itself contains non-greeting indicators,
            # it is not a pure greeting.
            if _has_non_greeting_content(match.group(0)):
                continue
            return _category_for_pattern(pattern, match.group(0))
    return None


def is_greeting_only(text: str) -> bool:
    return classify_greeting(text) is not None


def _category_for_pattern(pattern: re.Pattern, matched: str) -> str:
    lowered = matched.lower()
    if lowered.startswith("good morning"):
        return "good_morning"
    if lowered.startswith("good afternoon"):
        return "good_afternoon"
    if lowered.startswith("good evening"):
        return "good_evening"
    if "how" in lowered:
        return "how_are_you"
    if "thanks" in lowered or "thank" in lowered:
        return "thanks"
    if lowered in {"bye", "goodbye", "see you", "good night"}:
        return "bye"
    if lowered.startswith("hi"):
        return "hi"
    if lowered.startswith("hello"):
        return "hello"
    if lowered.startswith("hey"):
        return "hey"
    return "general"
