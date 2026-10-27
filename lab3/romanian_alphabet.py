from typing import Tuple, List, Dict, Optional

# 31 uppercase letters of the Romanian alphabet
ROMANIAN_ALPHABET: List[str] = [
    'A', 'Ă', 'Â', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'Î', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'Ș', 'T', 'Ț', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

ALPHABET_SIZE: int = len(ROMANIAN_ALPHABET)  # 31

CHAR_TO_INDEX: Dict[str, int] = {char: idx for idx, char in enumerate(ROMANIAN_ALPHABET)}
INDEX_TO_CHAR: Dict[int, str] = {idx: char for idx, char in enumerate(ROMANIAN_ALPHABET)}

# Normalize legacy cedilla characters (Ş, Ţ) to official comma-below forms (Ș, Ț)
CEDILLA_MAPPING: Dict[str, str] = {
    'Ş': 'Ș',
    'ş': 'ș',
    'Ţ': 'Ț',
    'ţ': 'ț',
}


def normalize_character(char: str) -> str:
    char = CEDILLA_MAPPING.get(char, char)
    return char.upper()


def normalize_text(text: str) -> str:
    return "".join(normalize_character(c) for c in text)


def validate_text(raw_text: str) -> Tuple[bool, Optional[str], str]:
    if not raw_text:
        return False, "Error: Text input cannot be empty.", ""

    # Task 3.2 requirement: spaces must be removed before uppercase transformation
    without_spaces = "".join(raw_text.split())
    if not without_spaces:
        return False, "Error: Text cannot contain only spaces.", ""

    normalized = normalize_text(without_spaces)
    invalid_chars = sorted(list(set(c for c in normalized if c not in CHAR_TO_INDEX)))

    if invalid_chars:
        return (
            False,
            f"Error: Invalid character(s) detected: {', '.join(repr(c) for c in invalid_chars)}.\n"
            f"Allowed characters: Only Romanian alphabet letters ('A'-'Z', 'a'-'z', including Ă, Â, Î, Ș, Ț).",
            "",
        )

    return True, None, normalized


def validate_key(raw_key: str) -> Tuple[bool, Optional[str], str]:
    if not raw_key:
        return False, "Error: Key cannot be empty.", ""

    without_spaces = "".join(raw_key.split())
    normalized = normalize_text(without_spaces)

    invalid_chars = sorted(list(set(c for c in normalized if c not in CHAR_TO_INDEX)))
    if invalid_chars:
        return (
            False,
            f"Error: Invalid character(s) in key: {', '.join(repr(c) for c in invalid_chars)}.\n"
            f"Allowed characters: Only Romanian alphabet letters ('A'-'Z', 'a'-'z', including Ă, Â, Î, Ș, Ț).",
            "",
        )

    # Task 3.2 requirement: key length >= 7
    if len(normalized) < 7:
        return (
            False,
            f"Error: Key '{raw_key.strip()}' is too short ({len(normalized)} characters). "
            f"Key must have a length of at least 7 characters.",
            "",
        )

    return True, None, normalized


def format_alphabet_table(alphabet: List[str] = ROMANIAN_ALPHABET, title: str = "Alphabet Table") -> str:
    """Formats the alphabet table showing 0..30 numeric mappings in two lines."""
    mid = 16
    indices_row1 = "Code:   " + " ".join(f"{i:>2}" for i in range(mid))
    letters_row1 = "Letter: " + " ".join(f"{alphabet[i]:>2}" for i in range(mid))
    sep1 = "-" * len(indices_row1)

    indices_row2 = "Code:   " + " ".join(f"{i:>2}" for i in range(mid, len(alphabet)))
    letters_row2 = "Letter: " + " ".join(f"{alphabet[i]:>2}" for i in range(mid, len(alphabet)))
    sep2 = "-" * len(indices_row2)

    return (
        f"{title}:\n"
        f"{sep1}\n"
        f"{indices_row1}\n"
        f"{letters_row1}\n\n"
        f"{indices_row2}\n"
        f"{letters_row2}\n"
        f"{sep2}"
    )
