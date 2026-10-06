"""
Core module for Romanian Alphabet operations and validation.
Complies with Laboratory Work No. 1 specifications:
- Alphabet length n = 31
- Encoding Table 2 (A=0, Ă=1, ..., Z=30)
- Normalization of cedilla variants (Ş -> Ș, Ţ -> Ț)
- Input validation and informative error reporting
"""

from typing import Tuple, List, Dict, Optional

# The 31 Romanian alphabet uppercase letters according to Table 2
ROMANIAN_ALPHABET: List[str] = [
    'A', 'Ă', 'Â', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'Î', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'Ș', 'T', 'Ț', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

ALPHABET_SIZE: int = len(ROMANIAN_ALPHABET)  # 31

# Map characters to their 0-based indices and vice-versa
CHAR_TO_INDEX: Dict[str, int] = {char: idx for idx, char in enumerate(ROMANIAN_ALPHABET)}
INDEX_TO_CHAR: Dict[int, str] = {idx: char for idx, char in enumerate(ROMANIAN_ALPHABET)}

# Cedilla to comma-below mapping for Romanian standard compliance
CEDILLA_MAPPING: Dict[str, str] = {
    'Ş': 'Ș',
    'ş': 'ș',
    'Ţ': 'Ț',
    'ţ': 'ț',
}


def normalize_character(char: str) -> str:
    """
    Normalizes a single character:
    - Converts cedilla variants (Ş, Ţ, ş, ţ) to comma-below (Ș, Ț, ș, ț).
    - Converts to uppercase.
    """
    char = CEDILLA_MAPPING.get(char, char)
    return char.upper()


def normalize_text(text: str) -> str:
    """
    Normalizes text by replacing cedillas with comma-below and converting to uppercase.
    Does not remove spaces.
    """
    return "".join(normalize_character(c) for c in text)


def validate_text(raw_text: str) -> Tuple[bool, Optional[str], str]:
    """
    Validates that raw_text contains only Romanian letters and spaces.
    If valid, returns (True, None, cleaned_uppercase_text_without_spaces).
    If invalid, returns (False, error_message, "").
    """
    if raw_text is None:
        return False, "Error: Text input cannot be null or empty.", ""

    normalized = normalize_text(raw_text)
    cleaned_chars = []

    for idx, ch in enumerate(normalized):
        if ch.isspace():
            continue
        if ch in CHAR_TO_INDEX:
            cleaned_chars.append(ch)
        else:
            original_ch = raw_text[idx]
            error_msg = (
                f"Error: Invalid character '{original_ch}' (Unicode U+{ord(original_ch):04X}) "
                f"found at position {idx + 1}.\n"
                f"Allowed characters: Romanian alphabet letters (A-Z, Ă, Â, Î, Ș, Ț) and spaces."
            )
            return False, error_msg, ""

    if not cleaned_chars:
        return False, "Error: Text contains no letters. Please enter at least one Romanian letter.", ""

    return True, None, "".join(cleaned_chars)


def validate_key(key_input: str) -> Tuple[bool, Optional[str], int]:
    """
    Validates Key 1 (shift value).
    Key must be an integer between 1 and 30 inclusive.
    Returns (True, None, key_int) or (False, error_message, -1).
    """
    key_str = key_input.strip()
    try:
        k = int(key_str)
    except ValueError:
        return (
            False,
            f"Error: Invalid key '{key_input}'. Key must be an integer between 1 and 30 inclusive.",
            -1,
        )

    if 1 <= k <= (ALPHABET_SIZE - 1):
        return True, None, k
    else:
        return (
            False,
            f"Error: Key value {k} is out of range. Allowed range is 1 to 30 inclusive (0 < k < 31).",
            -1,
        )


def validate_keyword(keyword_input: str) -> Tuple[bool, Optional[str], str]:
    """
    Validates Key 2 (keyword for alphabet permutation).
    - Length must be at least 7 characters.
    - Must contain only Romanian alphabet letters.
    Returns (True, None, normalized_keyword) or (False, error_message, "").
    """
    keyword_str = keyword_input.strip()
    normalized = normalize_text(keyword_str)

    # Check for invalid characters
    for idx, ch in enumerate(normalized):
        if ch not in CHAR_TO_INDEX:
            original_ch = keyword_str[idx]
            return (
                False,
                f"Error: Invalid character '{original_ch}' in keyword at position {idx + 1}.\n"
                f"Allowed characters: Only Romanian alphabet letters (A-Z, Ă, Â, Î, Ș, Ț).",
                "",
            )

    if len(normalized) < 7:
        return (
            False,
            f"Error: Keyword '{keyword_str}' is too short (length {len(normalized)}). "
            f"Key 2 must have a length of at least 7 characters.",
            "",
        )

    return True, None, normalized


def build_permuted_alphabet(keyword: str) -> List[str]:
    """
    Constructs the permuted alphabet of 31 Romanian letters using the keyword:
    - Characters of the keyword are placed first, keeping only their first occurrence.
    - Followed by the remaining letters of the Romanian alphabet in their natural order (Table 2).
    """
    normalized_kw = normalize_text(keyword)
    permuted: List[str] = []
    seen = set()

    for ch in normalized_kw:
        if ch in CHAR_TO_INDEX and ch not in seen:
            seen.add(ch)
            permuted.append(ch)

    for ch in ROMANIAN_ALPHABET:
        if ch not in seen:
            seen.add(ch)
            permuted.append(ch)

    assert len(permuted) == ALPHABET_SIZE, f"Alphabet size must be {ALPHABET_SIZE}, got {len(permuted)}"
    return permuted


def format_alphabet_table(alphabet: List[str], title: str = "Alphabet Table") -> str:
    """
    Formats the alphabet into a formatted table showing positions 0..30.
    """
    indices_row1 = "Code:   " + " ".join(f"{i:>2}" for i in range(16))
    letters_row1 = "Letter: " + " ".join(f"{alphabet[i]:>2}" for i in range(16))
    sep1 = "-" * len(indices_row1)

    indices_row2 = "Code:   " + " ".join(f"{i:>2}" for i in range(16, len(alphabet)))
    letters_row2 = "Letter: " + " ".join(f"{alphabet[i]:>2}" for i in range(16, len(alphabet)))
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
