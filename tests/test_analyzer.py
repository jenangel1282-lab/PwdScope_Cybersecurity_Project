
import pytest

from src.analyzer import analyze_password


def test_analyzer_returns_expected_fields():
    result = analyze_password("ExamplePassword123!")

    assert 0 <= result["score"] <= 4

    assert result["strength"] in [
        "Very Weak",
        "Weak",
        "Moderate",
        "Strong",
        "Very Strong",
    ]

    assert "warning" in result
    assert "suggestions" in result


def test_empty_password_raises_error():
    with pytest.raises(ValueError):
        analyze_password("")