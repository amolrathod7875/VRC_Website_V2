"""Stateless conversation context validation tests.

Validates that the stateless ConversationService correctly tracks product context
across multi-turn conversations without any database session. These tests verify
the 5 critical conversation flows identified in the Phase 10 evaluation:

1. Tiger 30:150 -> 150cc (output per cycle preserved)
2. Tiger 30:150 -> AI question -> 150cc (product context survives general question)
3. Dragon -> Polyurea -> variants -> Polyurea (product switch resolves correctly)
4. VRC MIX HP -> LP -> LOW-MEDIUM pressure ratio (variant disambiguation)
5. Barrel Pump -> Tiger 30:150 -> 30:1 (cross-product context switch)
"""
from app.rag.conversation.conversation_service import ConversationService


def make_user_msg(content: str):
    return {"role": "user", "content": content}


def make_assistant_msg(content: str, sources=None):
    return {
        "role": "assistant",
        "content": content,
        "sources": sources or [],
        "retrieval_metadata": {},
    }


def test_scenario_1_tiger_30_150_to_150cc():
    """User asks about Tiger 30:150, gets answer, then asks 'What is its output?'."""
    messages = [
        make_user_msg("Tell me about Tiger 30:150."),
        make_assistant_msg(
            "Tiger 30:150 is a low-pressure spray pump.",
            sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}],
        ),
        make_user_msg("What is its output?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] == "Tiger.pdf"

    augmented = ConversationService.build_augmented_query(
        "What is its output?",
        messages[:-1],  # history excluding current user message
        ctx,
    )
    assert "tiger" in augmented.lower()
    assert "30:150" in augmented


def test_scenario_2_tiger_30_150_then_ai_question_then_150cc():
    """Product context survives a general (non-product) question."""
    messages = [
        make_user_msg("Tell me about Tiger 30:150."),
        make_assistant_msg(
            "Tiger 30:150 outputs 150 cc per cycle.",
            sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}],
        ),
        make_user_msg("Can you tell me a joke?"),
        make_assistant_msg("Why did the chicken cross the road?"),
        make_user_msg("What is its output?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    # 'What is its output?' is ambiguous -> should carry Tiger context
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"


def test_scenario_3_dragon_to_polyurea_to_variants_to_polyurea():
    """Product switch from Dragon to Polyurea persists through variant questions."""
    messages = [
        make_user_msg("Tell me about Dragon."),
        make_assistant_msg(
            "Dragon is a passive fire protection coating system.",
            sources=[{"document": "dragon.pdf", "product_slug": "dragon", "model": None}],
        ),
        make_user_msg("Now tell me about Polyurea."),
        make_assistant_msg(
            "Polyurea is a two-component spray coating.",
            sources=[{"document": "polyurea.pdf", "product_slug": "polyurea", "model": None}],
        ),
        make_user_msg("What variants are available?"),
        make_assistant_msg(
            "Polyurea comes in several formulations.",
            sources=[{"document": "polyurea.pdf", "product_slug": "polyurea", "model": None}],
        ),
        make_user_msg("What is its pressure ratio?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "polyurea"


def test_scenario_4_vrc_mix_hp_to_lp_to_low_medium_ratio():
    """VRC MIX HP context switches to LP, then pressure ratio resolves to LP variant."""
    messages = [
        make_user_msg("Tell me about VRC MIX HP."),
        make_assistant_msg(
            "VRC MIX HP is a high-pressure mixing system.",
            sources=[{"document": "VRC - MIX HP.pdf", "product_slug": "vrc-mix-hp", "model": None}],
        ),
        make_user_msg("What about VRC MIX (LOW - MEDIUM) PRESSURE?"),
        make_assistant_msg(
            "VRC MIX Low-Medium Pressure is the low-pressure variant.",
            sources=[{"document": "VRC MIX (LOW - MEDIUM) PRESSURE.pdf", "product_slug": "vrc-mix-low-medium-pressure", "model": None}],
        ),
        make_user_msg("What is its pressure ratio?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "vrc-mix-low-medium-pressure"


def test_scenario_5_barrel_pump_to_tiger_30_150_to_30_1():
    """Barrel Pump context switches to Tiger 30:150, then output resolves to Tiger."""
    messages = [
        make_user_msg("Tell me about Barrel Pump."),
        make_assistant_msg(
            "Barrel Pump 210 liters is a drum pump system.",
            sources=[{"document": "Barrel Pump.pdf", "product_slug": "barrel-pump", "model": "210 liters"}],
        ),
        make_user_msg("Now tell me about Tiger 30:150."),
        make_assistant_msg(
            "Tiger 30:150 outputs 150 cc.",
            sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}],
        ),
        make_user_msg("What is its ratio?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"

    augmented = ConversationService.build_augmented_query(
        "What is its ratio?",
        messages[:-1],
        ctx,
    )
    assert "tiger" in augmented.lower()
    assert "30:150" in augmented


def test_scenario_5b_tiger_30_150_output_preservation():
    """Verify that '30:1' resolves to the Tiger 30:150 model identifier."""
    messages = [
        make_user_msg("Tell me about Tiger 30:150."),
        make_assistant_msg(
            "Tiger 30:150 outputs 150 cc.",
            sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}],
        ),
        make_user_msg("What is the output of the 30:1?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"


def test_stateless_no_db_required():
    """ConversationService must work without any database dependency."""
    service = ConversationService()
    assert service is not None
    # All methods are static, so instance creation requires no DB
    assert ConversationService.get_active_product_context([]) == {
        "product_slug": None, "model": None, "document": None
    }
