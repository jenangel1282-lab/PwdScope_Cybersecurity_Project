
from zxcvbn import zxcvbn

STRENGTH_LABELS = {
    0: "Very Weak",
    1: "Weak",
    2: "Moderate",
    3: "Strong",
    4: "Very Strong",
}


def analyze_password(password, personal_terms=None):
    """Analyze password strength, optionally considering personal terms."""
    if not password:
        raise ValueError("Password cannot be empty.")

    # Keep only non-empty personal terms.
    user_inputs = [
        term.strip()
        for term in (personal_terms or [])
        if isinstance(term, str) and term.strip()
    ]

    result = zxcvbn(password, user_inputs=user_inputs)
    score = result["score"]

    return {
        "score": score,
        "strength": STRENGTH_LABELS[score],
        "warning": result["feedback"]["warning"],
        "suggestions": result["feedback"]["suggestions"],
    }