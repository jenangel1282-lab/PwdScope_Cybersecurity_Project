
from nltk.tokenize import RegexpTokenizer


# Split text into words and numbers without needing a downloaded NLTK dataset
tokenizer = RegexpTokenizer(r"[A-Za-z0-9]+")


def tokenize_profile_text(text):
    if not text:
        return []

    tokens = tokenizer.tokenize(text)

    # Remove duplicate tokens while preserving their original order
    unique_tokens = []
    seen = set()

    for token in tokens:
        normalized = token.lower()

        if normalized not in seen:
            seen.add(normalized)
            unique_tokens.append(token)

    return unique_tokens