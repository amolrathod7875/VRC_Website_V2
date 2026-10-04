import pytest
from app.rag.greeting_response import get_greeting_response


def test_greeting_response_hey() -> None:
    response = get_greeting_response("hey")
    assert "Hey!" in response
    assert "VR Coatings" in response


def test_greeting_response_hello() -> None:
    response = get_greeting_response("hello")
    assert "Hello!" in response
    assert "VR Coatings" in response


def test_greeting_response_hi() -> None:
    response = get_greeting_response("hi")
    assert "Hey!" in response


def test_greeting_response_good_morning() -> None:
    response = get_greeting_response("good morning")
    assert "Good morning!" in response


def test_greeting_response_good_afternoon() -> None:
    response = get_greeting_response("good afternoon")
    assert "Good afternoon!" in response


def test_greeting_response_good_evening() -> None:
    response = get_greeting_response("good evening")
    assert "Good evening!" in response


def test_greeting_response_how_are_you() -> None:
    response = get_greeting_response("how are you")
    assert "I'm doing well" in response


def test_greeting_response_thanks() -> None:
    response = get_greeting_response("thanks")
    assert "You're welcome" in response


def test_greeting_response_bye() -> None:
    response = get_greeting_response("bye")
    assert "Goodbye" in response


def test_greeting_response_raises_for_non_greeting() -> None:
    with pytest.raises(ValueError):
        get_greeting_response("tell me about tiger")
