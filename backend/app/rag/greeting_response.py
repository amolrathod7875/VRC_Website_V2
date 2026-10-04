from app.rag.greeting_detector import classify_greeting

_GREETING_RESPONSES = {
    "hi": "Hey! 👋 How can I help you with VR Coatings today?",
    "hello": "Hello! 👋 I can help you with VR Coatings products, applications, technical specifications, and company information. What would you like to know?",
    "hey": "Hey! 👋 How can I help you with VR Coatings today?",
    "good_morning": "Good morning! How can I help you with VR Coatings today?",
    "good_afternoon": "Good afternoon! How can I help you with VR Coatings today?",
    "good_evening": "Good evening! How can I help you with VR Coatings today?",
    "how_are_you": "I'm doing well! How can I help you with VR Coatings products or company information?",
    "thanks": "You're welcome! Let me know if you'd like help with any VR Coatings product or technical specification.",
    "bye": "Goodbye! Feel free to come back anytime you need information about VR Coatings.",
    "general": "Hey! 👋 How can I help you with VR Coatings today?",
}


def get_greeting_response(message: str) -> str:
    category = classify_greeting(message)
    if not category:
        raise ValueError("Message is not a greeting-only message")
    return _GREETING_RESPONSES.get(category, _GREETING_RESPONSES["general"])
