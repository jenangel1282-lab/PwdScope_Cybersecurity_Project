
from pathlib import Path

from src.text_processor import tokenize_profile_text


LEETSPEAK_MAP = {
    "a": "@",
    "e": "3",
    "i": "1",
    "o": "0",
    "s": "$",
}


def clean_input(value):
    return value.strip() if value else ""


def get_year_variations(year):
    year = clean_input(year)

    if not year:
        return []

    if not year.isdigit() or len(year) != 4:
        raise ValueError("Year must be a four-digit number.")

    year_number = int(year)

    return [
        str(year_number - 1),
        str(year_number),
        str(year_number + 1),
    ]


def create_basic_variations(word):
    word = clean_input(word)

    if not word:
        return set()

    variations = {
        word,
        word.lower(),
        word.upper(),
        word.capitalize(),
    }

    lowered = word.lower()

    for original, replacement in LEETSPEAK_MAP.items():
        if original in lowered:
            variations.add(lowered.replace(original, replacement))

    return variations


def generate_wordlist(
    name="",
    pet="",
    year="",
    phrase="",
    max_items=200,
):
    if max_items <= 0:
        raise ValueError("max_items must be greater than zero.")

    seeds = []

    if clean_input(name):
        seeds.append(clean_input(name))

    if clean_input(pet):
        seeds.append(clean_input(pet))

    seeds.extend(
        tokenize_profile_text(clean_input(phrase))
    )

    candidates = set()

    # Generate basic variations
    for seed in seeds:
        candidates.update(create_basic_variations(seed))

    # Add year variations before and after each seed
    years = get_year_variations(year)

    for seed in seeds:
        variations = create_basic_variations(seed)

        for variation in variations:
            for year_value in years:
                candidates.add(variation + year_value)
                candidates.add(year_value + variation)

    # Combine name and pet variations
    if clean_input(name) and clean_input(pet):
        name_variations = create_basic_variations(name)
        pet_variations = create_basic_variations(pet)

        for name_value in name_variations:
            for pet_value in pet_variations:
                candidates.add(name_value + pet_value)
                candidates.add(pet_value + name_value)

    # Return a sorted list within the requested limit
    return sorted(candidates)[:max_items]


def export_wordlist(candidates, output_file):
    path = Path(output_file)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for candidate in candidates:
            file.write(candidate + "\n")

    return path