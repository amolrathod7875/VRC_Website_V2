import re
import html


def clean_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def remove_html_entities(text: str) -> str:
    return html.unescape(text)


def remove_control_characters(text: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)


def normalize_text(text: str) -> str:
    text = remove_control_characters(text)
    text = remove_html_entities(text)
    text = clean_whitespace(text)
    return text


def truncate(text: str, max_length: int = 10000) -> str:
    return text[:max_length]
