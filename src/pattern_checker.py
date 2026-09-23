
import re


def check_password_patterns(password, personal_terms=None):
    findings = []

    if not password:
        return findings

    lowered = password.lower()

    # Check for a character repeated three or more times.
    if re.search(r"(.)\1{2,}", password):
        findings.append(
            {
                "finding": (
                    "Contains a character repeated three or more times."
                ),
                "advice": (
                    "Avoid long runs of the same character; "
                    "use a less predictable combination."
                ),
            }
        )

    # Check for common sequences and keyboard patterns.
    common_sequences = [
        "1234", "2345", "3456", "4567",
        "5678", "6789", "abcd", "qwerty", "asdf"
    ]

    if any(sequence in lowered for sequence in common_sequences):
        findings.append(
            {
                "finding": (
                    "Contains a common sequence or keyboard pattern."
                ),
                "advice": (
                    "Avoid predictable sequences and keyboard patterns."
                ),
            }
        )

    # Check for a year-like number.
    if re.search(r"(19|20)\d{2}", password):
        findings.append(
            {
                "finding": "Contains a year-like number.",
                "advice": (
                    "Avoid using predictable years or dates "
                    "as part of a password."
                ),
            }
        )

    # Check for characters sometimes used in substitutions.
    if re.search(r"[@$!03]", password):
        findings.append(
            {
                "finding": (
                    "Contains characters sometimes used "
                    "in common substitutions."
                ),
                "advice": (
                    "Substituting letters with symbols or numbers "
                    "does not necessarily make a password unpredictable."
                ),
            }
        )

    # Optional check for supplied personal terms.
    for term in personal_terms or []:
        if not isinstance(term, str):
            continue

        term = term.strip()

        # Ignore very short terms to reduce noisy matches.
        if len(term) < 3:
            continue

        if term.lower() in lowered:
            findings.append(
                {
                    "finding": (
                        "Contains one of the supplied personal terms."
                    ),
                    "advice": (
                        "Avoid including names or other personal "
                        "details that someone might know or guess."
                    ),
                }
            )
            break

    return findings