from app.rag.ingestion.pdf_table_parser import parse_spec_table


def test_table_parser_never_guesses_missing_cells() -> None:
    rows = [
        ["Type", "30:150", "35:70"],
        ["Pressure ratio", "30:1", "35:1"],
        ["Output per cycle", "150", "70"],
        ["Max pressure", "450", "280"],
    ]
    parsed = parse_spec_table(rows)
    assert len(parsed) == 2
    assert parsed[0]["model"] == "30:150"
    assert parsed[1]["model"] == "35:70"
    for item in parsed:
        for v in item["values"]:
            assert v["value"] != ""


def test_table_parser_column_mismatch_warning() -> None:
    rows = [
        ["Type", "30:150", "35:70"],
        ["Pressure ratio", "30:1"],
    ]
    parsed = parse_spec_table(rows)
    assert parsed == []
