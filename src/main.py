
import argparse
import getpass

from src.analyzer import analyze_password
from src.pattern_checker import check_password_patterns
from src.wordlist_generator import (
    generate_wordlist,
    export_wordlist,
)



def run_analyze(args):
    password = getpass.getpass(
        "Enter a sample password (input hidden): "
    )

    personal_terms = []

    if args.personalized:
        print(
            "\nOptional context for the estimate. "
            "Use fictional details or leave blank."
        )

        name = input("Sample name: ").strip()
        pet = input("Sample pet name: ").strip()
        year = input("Sample year: ").strip()

        personal_terms = [
            term for term in [name, pet, year] if term
        ]

    try:
        result = analyze_password(
            password,
            personal_terms=personal_terms,
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    print("\n--- Password Analysis ---")
    print(f"Estimated score: {result['score']}/4")
    print(f"Estimated category: {result['strength']}")

    if result["warning"]:
        print(f"Warning: {result['warning']}")

    if result["suggestions"]:
        print("\nSuggestions:")
        for suggestion in result["suggestions"]:
            print(f"- {suggestion}")

    findings = check_password_patterns(
        password,
        personal_terms=personal_terms,
    )

    print("\nPattern checks:")

    if findings:
        for item in findings:
            print(f"- {item['finding']}")
            print(f"  Advice: {item['advice']}")
    else:
        print("- No listed patterns detected.")

    print(
        "\nNote: Password strength results are estimates "
        "and do not guarantee security."
    )

def run_generate(args):
    name = args.name or input(
        "Enter a fictional name (optional): "
    )

    pet = args.pet or input(
        "Enter a fictional pet name (optional): "
    )

    year = args.year or input(
        "Enter a four-digit year (optional): "
    )

    phrase = args.phrase or input(
        "Enter an optional sample phrase (optional): "
    )

    try:
        candidates = generate_wordlist(
            name=name,
            pet=pet,
            year=year,
            phrase=phrase,
            max_items=args.max_items,
        )

        output_path = export_wordlist(
            candidates,
            args.output,
        )

    except ValueError as error:
        print(f"Error: {error}")
        return

    print("\n--- Wordlist Generation ---")
    print(f"Candidates generated: {len(candidates)}")
    print(f"Saved to: {output_path}")
    print(
        "Use only in a controlled, authorized security-auditing lab."
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Password Strength Analyzer with "
            "Custom Wordlist Generator"
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )
    
    # Password analysis command.
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a sample password.",
    )

    analyze_parser.add_argument(
        "--personalized",
        action="store_true",
        help="Include optional personal terms in the estimate.",
    )

    # Wordlist generation command.
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a bounded custom wordlist.",
    )

    generate_parser.add_argument(
        "--name",
        default="",
        help="Fictional or authorized name seed.",
    )

    generate_parser.add_argument(
        "--pet",
        default="",
        help="Fictional or authorized pet-name seed.",
    )

    generate_parser.add_argument(
        "--year",
        default="",
        help="Four-digit year seed.",
    )

    generate_parser.add_argument(
        "--phrase",
        default="",
        help="Optional sample phrase to tokenize with NLTK.",
    )

    generate_parser.add_argument(
        "--max-items",
        type=int,
        default=200,
        help="Maximum number of candidates.",
    )

    generate_parser.add_argument(
        "--output",
        default="output/wordlist.txt",
        help="Output .txt file path.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        run_analyze(args)

    elif args.command == "generate":
        run_generate(args)


if __name__ == "__main__":
    main()