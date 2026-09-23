
from src.text_processor import tokenize_profile_text
from src.wordlist_generator import (
    generate_wordlist,
    export_wordlist,
)


def test_nltk_tokenizes_profile_phrase():
    assert tokenize_profile_text(
        "Alex loves Coco!"
    ) == ["Alex", "loves", "Coco"]


def test_generator_returns_candidates():
    candidates = generate_wordlist(
        name="Alex",
        pet="Coco",
        year="2024",
        phrase="Alex loves Coco",
    )

    assert candidates
    assert any(
        "Alex" in item or "alex" in item.lower()
        for item in candidates
    )


def test_generator_respects_max_items():
    candidates = generate_wordlist(
        name="Alex",
        pet="Coco",
        year="2024",
        phrase="Alex loves Coco",
        max_items=10,
    )

    assert len(candidates) <= 10


def test_generator_rejects_zero_limit():
    try:
        generate_wordlist(name="Alex", max_items=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")


def test_export_creates_text_file(tmp_path):
    output_file = tmp_path / "test_wordlist.txt"

    export_wordlist(
        ["Alex", "Coco", "Alex2024"],
        output_file,
    )

    assert output_file.exists()

    contents = output_file.read_text(encoding="utf-8")

    assert "Alex" in contents
    assert "Coco" in contents