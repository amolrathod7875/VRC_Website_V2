from app.rag.ingestion.company_parser import parse_company_text, parse_section_heading


def test_parse_section_heading() -> None:
    assert parse_section_heading("SECTION 1 — Locations") == {
        "section_number": "1",
        "section_title": "Locations",
    }
    assert parse_section_heading("SECTION 10 — FAQS") == {
        "section_number": "10",
        "section_title": "FAQS",
    }
    assert parse_section_heading("Random line") is None


def test_parse_company_text_preserves_line_ranges() -> None:
    text = "PREAMBLE\nSECTION 1 — Locations\nLine 1\nLine 2\nSECTION 2 — History\nLine 3\n"
    sections = parse_company_text(text)
    assert len(sections) == 2
    assert sections[0]["section_title"] == "Locations"
    assert sections[0]["line_start"] == 2
    assert sections[1]["section_title"] == "History"
    assert sections[1]["line_start"] == 5
