import pytest
from app.rag.greeting_detector import is_greeting_only, classify_greeting, normalize_for_greeting


@pytest.mark.parametrize(
    "message",
    [
        "hey",
        "Hey",
        " hey ",
        "HEY",
        "hii",
        "hiii",
        "hello",
        "Hello",
        "hey there",
        "hello there",
        "good morning",
        "good afternoon",
        "good evening",
        "morning",
        "afternoon",
        "evening",
        "namaste",
        "namaskar",
        "yo",
        "sup",
        "what's up",
        "whats up",
        "how are you",
        "how are you doing",
        "how's it going",
        "hows it going",
        "thanks",
        "thankyou",
        "thank you",
        "okay thanks",
        "ok thanks",
        "thx",
        "bye",
        "goodbye",
        "see you",
        "good night",
    ],
)
def test_greeting_only_messages_are_detected(message: str) -> None:
    assert is_greeting_only(message) is True


@pytest.mark.parametrize(
    "message",
    [
        "Hi, tell me about Tiger 30:150.",
        "Hello, what is Rhino used for?",
        "Hey, what is the pressure ratio of Tiger?",
        "hi how much does tiger cost",
        "hello i need information about lion",
        "good morning, what filters do you offer?",
        "tell me about elephant pumps",
        "what is the output per cycle",
        "how much does rhino cost",
        "thanks, what is the flow rate",
    ],
)
def test_greeting_plus_question_is_not_detected_as_greeting_only(message: str) -> None:
    assert is_greeting_only(message) is False


def test_greeting_plus_product_name_is_not_greeting_only() -> None:
    assert is_greeting_only("hi tiger") is False
    assert is_greeting_only("hello lion") is False
    assert is_greeting_only("hey rhino") is False


def test_classify_greeting_returns_category() -> None:
    assert classify_greeting("hey") == "hey"
    assert classify_greeting("hello") == "hello"
    assert classify_greeting("hi") == "hi"
    assert classify_greeting("good morning") == "good_morning"
    assert classify_greeting("good afternoon") == "good_afternoon"
    assert classify_greeting("good evening") == "good_evening"
    assert classify_greeting("how are you") == "how_are_you"
    assert classify_greeting("how's it going") == "how_are_you"
    assert classify_greeting("thanks") == "thanks"
    assert classify_greeting("thank you") == "thanks"
    assert classify_greeting("bye") == "bye"
    assert classify_greeting("goodbye") == "bye"
    assert classify_greeting("see you") == "bye"


def test_classify_greeting_returns_none_for_non_greeting() -> None:
    assert classify_greeting("hi tiger") is None
    assert classify_greeting("tell me about tiger") is None
    assert classify_greeting("what is the pressure ratio") is None


def test_normalize_for_greeting_lowercases_and_strips() -> None:
    assert normalize_for_greeting("  HEY!!  ") == "hey"
    assert normalize_for_greeting("Hey") == "hey"
    assert normalize_for_greeting("hello!!!") == "hello"
    assert normalize_for_greeting("hi...") == "hi"
