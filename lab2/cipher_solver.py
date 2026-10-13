"""
Monoalphabetic Cipher Solver Module.
Implements progressive linguistic deduction, partial text substitution,
key recovery, and affine cipher mathematical verification.
"""

from typing import Dict, List, Tuple


# Complete recovered key: Cipher letter (uppercase) -> Plain letter (lowercase)
SOLVED_KEY: Dict[str, str] = {
    'A': 'b', 'B': 'q', 'C': 'f', 'D': 'u', 'E': 'j', 'F': 'y', 'G': 'n',
    'H': 'c', 'I': 'r', 'J': 'g', 'K': 'v', 'L': 'k', 'M': 'z', 'N': 'o',
    'O': 'd', 'P': 's', 'Q': 'h', 'R': 'w', 'S': 'l', 'T': 'a', 'U': 'p',
    'V': 'e', 'W': 't', 'X': 'i', 'Y': 'x', 'Z': 'm'
}


class CipherSolver:
    """Provides methods for step-by-step cryptanalysis and decryption."""

    def __init__(self, ciphertext: str):
        self.ciphertext = ciphertext

    def apply_partial_mapping(self, mapping: Dict[str, str]) -> str:
        """
        Replaces decrypted letters with lowercase, keeping unmapped
        letters as uppercase ciphertext and preserving punctuation.
        """
        result = []
        for ch in self.ciphertext:
            if ch.isalpha():
                upper_ch = ch.upper()
                if upper_ch in mapping:
                    plain_char = mapping[upper_ch]
                    result.append(plain_char.upper() if ch.isupper() else plain_char.lower())
                else:
                    # Keep unmapped characters in uppercase
                    result.append(ch.upper())
            else:
                result.append(ch)
        return "".join(result)

    def decrypt(self, custom_key: Dict[str, str] = None) -> str:
        """Decrypts the full ciphertext using the solved or custom key."""
        key = custom_key if custom_key is not None else SOLVED_KEY
        return self.apply_partial_mapping(key)

    @staticmethod
    def get_milestones() -> List[Dict]:
        """
        Returns structured stages of progressive cryptanalytic deduction
        matching Section 2.3 of the lab manual.
        """
        return [
            {
                "step": 1,
                "title": "Identification of Trigram 'wqv' -> 'the' and Unigram 'V' -> 'e'",
                "rationale": (
                    "In the ciphertext, the trigram 'wqv' is the most frequent (52 occurrences), "
                    "matching the most common English trigram 'THE'. Furthermore, 'V' has the highest "
                    "individual frequency (12.28%), matching English 'E' (12.70%). "
                    "This establishes: W->t, Q->h, V->e."
                ),
                "mapping": {'W': 't', 'Q': 'h', 'V': 'e'},
                "sample_cipher": "wqv jivtwvpw xp Rxssxtz",
                "sample_plain": "the jietwpt xp Rxssxtz"
            },
            {
                "step": 2,
                "title": "Two-Letter Words & Consonant Detections: 'to', 'that', 'what', 'is'",
                "rationale": (
                    "Examining short words with established letters: 'wn' appears frequently with 'W'->'t', "
                    "identifying 'wn' as 'to' (N->o). 'wqtw' ('t*at') is unequivocally 'that' (T->a). "
                    "'rqtw' ('*hat') in 'to *hat he did' is 'what' (R->w). The frequent word 'xp' "
                    "in 'the greatest xp William' yields 'is' (X->i, P->s)."
                ),
                "mapping": {
                    'W': 't', 'Q': 'h', 'V': 'e', 'N': 'o', 'T': 'a',
                    'R': 'w', 'X': 'i', 'P': 's'
                },
                "sample_cipher": "wn rqtw qv oxo",
                "sample_plain": "to what he oio"
            },
            {
                "step": 3,
                "title": "Frequent Digrams & Conjunctions: 'in', 'and', 'may', 'be'",
                "rationale": (
                    "The two-letter word 'xg' with 'X'->'i' gives 'in' (G->n). The very frequent trigram "
                    "'tgo' with 'T'->'a' and 'G'->'n' gives 'and' (O->d). The phrase 'ztf av' becomes "
                    "'may be' (Z->m, F->y, A->b)."
                ),
                "mapping": {
                    'W': 't', 'Q': 'h', 'V': 'e', 'N': 'o', 'T': 'a',
                    'R': 'w', 'X': 'i', 'P': 's', 'G': 'n', 'O': 'd',
                    'Z': 'm', 'F': 'y', 'A': 'b'
                },
                "sample_cipher": "ztf av wqv avpw lgnrg",
                "sample_plain": "may be the best known"
            },
            {
                "step": 4,
                "title": "Historical Names & Cryptological Stems: 'William', 'Frederick', 'Yardley'",
                "rationale": (
                    "Analyzing proper names: 'Rxssxtz' ('Wi**iam') yields 'William' (S->l). "
                    "'Civovixhl' ('F*ede*ick') yields 'Frederick' (C->f, I->r, H->c, L->k). "
                    "'Ftiosvf' ('Yardley') validates F->y, T->a, I->r, O->d, S->l, V->e. "
                    "'Cixvoztg' resolves to 'Friedman'."
                ),
                "mapping": {
                    'W': 't', 'Q': 'h', 'V': 'e', 'N': 'o', 'T': 'a',
                    'R': 'w', 'X': 'i', 'P': 's', 'G': 'n', 'O': 'd',
                    'Z': 'm', 'F': 'y', 'A': 'b', 'S': 'l', 'C': 'f',
                    'I': 'r', 'H': 'c', 'L': 'k'
                },
                "sample_cipher": "Rxssxtz Civovixhl Cixvoztg",
                "sample_plain": "William Frederick Friedman"
            },
            {
                "step": 5,
                "title": "Completing Low-Frequency Letters & Mathematical Affine Validation",
                "rationale": (
                    "Remaining letters are deduced from contextual roots: 'dghngwvpwtasf' -> 'uncontestably' (D->u), "
                    "'jivtwvpw' -> 'greatest' (J->g), 'vkvi' -> 'ever' (K->v), 'uithwxhts' -> 'practical' (U->p), "
                    "'cxy' -> 'fix' (Y->x), 'Edgv' -> 'June' (E->j), 'tgtztmxgj' -> 'amazing' (M->z), "
                    "'wvhqgxbdv' -> 'technique' (B->q). This completes all 26 alphabet letters."
                ),
                "mapping": SOLVED_KEY,
                "sample_cipher": "dghngwvpwtasf wqv jivtwvpw",
                "sample_plain": "uncontestably the greatest"
            }
        ]

    @staticmethod
    def get_affine_parameters() -> Tuple[int, int, int]:
        """
        Mathematical proof of the variant generation:
        Plain 'a' (0) -> Cipher 'T' (19)
        Plain 'b' (1) -> Cipher 'A' (0)
        Affine encryption: E(x) = (7*x + 19) mod 26
        Affine decryption: D(y) = 15*(y - 19) mod 26 = (15*y + 1) mod 26
        """
        a = 7
        b = 19
        a_inv = 15  # (7 * 15) % 26 == 1
        return a, b, a_inv

    @staticmethod
    def format_key_table() -> str:
        """Formats the reconstructed key table (matching Table 2.5 of the lab manual)."""
        cipher_row = " ".join(sorted(SOLVED_KEY.keys()))
        plain_row = " ".join([SOLVED_KEY[c] for c in sorted(SOLVED_KEY.keys())])
        separator = "-" * len(cipher_row)
        return (
            f"Ciphertext: {cipher_row}\n"
            f"            {separator}\n"
            f"Plaintext:  {plain_row}"
        )
