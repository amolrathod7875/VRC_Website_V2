import hashlib
from pathlib import Path
from app.rag.utils.hashing import calculate_sha256


def test_calculate_sha256_stable(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello world", encoding="utf-8")
    first = calculate_sha256(file_path)
    second = calculate_sha256(file_path)
    assert first == second
    assert len(first) == 64
