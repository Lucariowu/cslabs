"""
Frequency Analysis Module for Monoalphabetic Cryptanalysis.
Computes unigram, digram, trigram statistics, repeated letters,
and Index of Coincidence (IC) for cryptanalytic evaluation.
"""

from collections import Counter
import math
from typing import Dict, List, Tuple


# Reference frequency of letters in the English language (Table 2.2 from lab guide)
ENGLISH_LETTER_FREQ: Dict[str, float] = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70,
    'F': 2.23, 'G': 2.01, 'H': 6.09, 'I': 6.97, 'J': 0.15,
    'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51,
    'P': 1.93, 'Q': 0.09, 'R': 5.99, 'S': 6.33, 'T': 9.06,
    'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
    'Z': 0.07
}

# Standard frequent English digrams (ordered roughly by frequency)
COMMON_ENGLISH_DIGRAMS: List[str] = [
    'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST',
    'EN', 'AT', 'TO', 'NT', 'HA', 'ND', 'OU', 'EA', 'NG', 'AS',
    'OR', 'TI', 'IS', 'ET', 'IT', 'AR', 'TE', 'SE', 'HI', 'OF'
]

# Standard frequent English trigrams
COMMON_ENGLISH_TRIGRAMS: List[str] = [
    'THE', 'AND', 'ING', 'ENT', 'ION', 'HER', 'FOR', 'THA', 'NTH',
    'INT', 'ERE', 'TIO', 'TER', 'EST', 'ERS', 'ATI', 'HAT', 'ATE',
    'ALL', 'ETH', 'HES', 'VER', 'HIS', 'OFT', 'ITH', 'FTH', 'STH'
]


class FrequencyAnalyzer:
    """Performs statistical and linguistic analysis on ciphertext."""

    def __init__(self, text: str):
        self.raw_text = text
        self.clean_letters = [ch.upper() for ch in text if ch.isalpha()]
        self.total_letters = len(self.clean_letters)

    def compute_unigram_frequencies(self) -> List[Tuple[str, int, float]]:
        """
        Calculates letter frequencies, returned as a sorted list of
        (letter, count, percentage) in descending order of frequency.
        """
        counts = Counter(self.clean_letters)
        result = []
        for letter in sorted(counts.keys(), key=lambda l: counts[l], reverse=True):
            cnt = counts[letter]
            pct = (cnt / self.total_letters * 100.0) if self.total_letters > 0 else 0.0
            result.append((letter, cnt, pct))
        return result

    def compute_digram_frequencies(self, top_n: int = 15) -> List[Tuple[str, int, float]]:
        """Extracts top_n frequent digrams formed by adjacent alphabetic characters."""
        digrams = []
        for i in range(len(self.clean_letters) - 1):
            digrams.append(self.clean_letters[i] + self.clean_letters[i + 1])
        counts = Counter(digrams)
        total = len(digrams)
        return [(dg, cnt, (cnt / total * 100.0) if total > 0 else 0.0)
                for dg, cnt in counts.most_common(top_n)]

    def compute_trigram_frequencies(self, top_n: int = 10) -> List[Tuple[str, int, float]]:
        """Extracts top_n frequent trigrams formed by consecutive alphabetic characters."""
        trigrams = []
        for i in range(len(self.clean_letters) - 2):
            trigrams.append(self.clean_letters[i] + self.clean_letters[i + 1] + self.clean_letters[i + 2])
        counts = Counter(trigrams)
        total = len(trigrams)
        return [(tg, cnt, (cnt / total * 100.0) if total > 0 else 0.0)
                for tg, cnt in counts.most_common(top_n)]

    def compute_repeated_letters(self) -> List[Tuple[str, int]]:
        """Identifies double consecutive identical letters (e.g., LL, EE, SS)."""
        doubles = []
        for i in range(len(self.clean_letters) - 1):
            if self.clean_letters[i] == self.clean_letters[i + 1]:
                doubles.append(self.clean_letters[i] * 2)
        return Counter(doubles).most_common()

    def find_short_words(self, length: int = 1) -> List[Tuple[str, int]]:
        """Extracts isolated words of a specific length (ignoring punctuation)."""
        import re
        tokens = re.findall(r'[A-Za-z]+', self.raw_text)
        matched = [w.upper() for w in tokens if len(w) == length]
        return Counter(matched).most_common()

    def index_of_coincidence(self) -> float:
        """
        Computes the Index of Coincidence (IC):
        IC = sum(f_i * (f_i - 1)) / (N * (N - 1))
        English language baseline ~ 0.0667, random uniform text ~ 0.0385.
        """
        n = self.total_letters
        if n <= 1:
            return 0.0
        counts = Counter(self.clean_letters)
        numerator = sum(f * (f - 1) for f in counts.values())
        return numerator / (n * (n - 1))

    def format_frequency_table(self) -> str:
        """Generates a formatted text table comparing observed vs English frequencies."""
        unigrams = self.compute_unigram_frequencies()
        lines = []
        lines.append("=" * 68)
        lines.append(f"{'RANK':<5} {'CIPHER':<8} {'COUNT':<8} {'OBSERVED %':<14} {'ENG REF':<10} {'ENG %':<10}")
        lines.append("-" * 68)

        eng_sorted = sorted(ENGLISH_LETTER_FREQ.items(), key=lambda x: x[1], reverse=True)

        for rank, (c_char, c_cnt, c_pct) in enumerate(unigrams, start=1):
            eng_char, eng_pct = eng_sorted[rank - 1] if rank - 1 < len(eng_sorted) else ('-', 0.0)
            lines.append(f"{rank:<5} {c_char:<8} {c_cnt:<8} {c_pct:>6.2f}%       {eng_char:<10} {eng_pct:>5.2f}%")

        lines.append("=" * 68)
        ic_val = self.index_of_coincidence()
        lines.append(f"Total Letters: {self.total_letters} | Index of Coincidence (IC): {ic_val:.5f} (English ~0.067)")
        return "\n".join(lines)
