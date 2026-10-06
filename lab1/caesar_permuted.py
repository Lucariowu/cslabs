"""
Task 1.2: Caesar Cipher with Keyword Permutation (Two Keys) over Romanian Alphabet.
Complies with Laboratory Work No. 1:
- Alphabet length n = 31.
- Key 1: Numeric shift k1 in {1, 2, ..., 30}.
- Key 2: Keyword k2 with length >= 7, letters in Romanian alphabet only.
- Permuted alphabet is displayed so results can be checked by hand.
- Encryption and decryption use the positions in the permuted alphabet.
- Full validation and re-prompting on invalid inputs.
"""

import sys
from typing import List, Dict, Tuple
from romanian_alphabet import (
    ROMANIAN_ALPHABET,
    ALPHABET_SIZE,
    validate_text,
    validate_key,
    validate_keyword,
    build_permuted_alphabet,
    format_alphabet_table,
)


def encrypt_caesar_permuted(plaintext: str, key1: int, permuted_alphabet: List[str]) -> str:
    """
    Encrypts plaintext using the permuted alphabet and numeric shift key1:
    c = (x + k1) mod 31, where x is index in permuted_alphabet.
    """
    char_to_pos = {char: idx for idx, char in enumerate(permuted_alphabet)}
    ciphertext_chars = []
    for char in plaintext:
        x = char_to_pos[char]
        c_code = (x + key1) % ALPHABET_SIZE
        ciphertext_chars.append(permuted_alphabet[c_code])
    return "".join(ciphertext_chars)


def decrypt_caesar_permuted(ciphertext: str, key1: int, permuted_alphabet: List[str]) -> str:
    """
    Decrypts ciphertext using the permuted alphabet and numeric shift key1:
    m = (y - k1) mod 31, where y is index in permuted_alphabet.
    """
    char_to_pos = {char: idx for idx, char in enumerate(permuted_alphabet)}
    plaintext_chars = []
    for char in ciphertext:
        y = char_to_pos[char]
        m_code = (y - key1) % ALPHABET_SIZE
        plaintext_chars.append(permuted_alphabet[m_code])
    return "".join(plaintext_chars)


def prompt_valid_key1() -> int:
    """
    Prompts the user repeatedly until a valid shift key (integer 1..30) is entered.
    """
    while True:
        try:
            raw_key = input("Enter Key 1 (Shift value, integer between 1 and 30): ")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, err, key_val = validate_key(raw_key)
        if is_valid:
            return key_val
        print(f"\n{err}\nPlease try again.\n")


def prompt_valid_key2() -> str:
    """
    Prompts the user repeatedly until a valid keyword (>= 7 Romanian letters) is entered.
    """
    while True:
        try:
            raw_kw = input("Enter Key 2 (Keyword, at least 7 Romanian letters): ")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, err, clean_kw = validate_keyword(raw_kw)
        if is_valid:
            return clean_kw
        print(f"\n{err}\nPlease try again.\n")


def prompt_valid_text(prompt_msg: str) -> str:
    """
    Prompts user repeatedly until valid text (Romanian letters and spaces) is entered.
    """
    while True:
        try:
            raw_text = input(prompt_msg)
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, err, clean_text = validate_text(raw_text)
        if is_valid:
            return clean_text
        print(f"\n{err}\nPlease try again.\n")


def run_interactive_task2() -> None:
    """
    Interactive command-line loop for Task 1.2.
    """
    print("=" * 70)
    print(" TASK 1.2: CAESAR CIPHER WITH TWO KEYS OVER ROMANIAN ALPHABET ")
    print("=" * 70)

    while True:
        print("\nChoose an option:")
        print("  1. Encrypt a message with Two Keys (Shift + Keyword)")
        print("  2. Decrypt a message with Two Keys (Shift + Keyword)")
        print("  3. Build and view permuted alphabet for a keyword")
        print("  4. Return to main menu / Exit")
        choice = input("Select option (1-4): ").strip()

        if choice in ('1', '2'):
            is_encrypt = (choice == '1')
            op_name = "ENCRYPTION" if is_encrypt else "DECRYPTION"
            print(f"\n--- {op_name} (TWO KEYS) ---")

            key1 = prompt_valid_key1()
            key2 = prompt_valid_key2()

            # Construct and display permuted alphabet (Task requirement: must display it!)
            permuted = build_permuted_alphabet(key2)
            print("\n" + "=" * 55)
            print(f"Permuted Alphabet for Key 2 ('{key2}'):")
            print("=" * 55)
            print(format_alphabet_table(permuted, f"Permuted Alphabet (Keyword: {key2})"))
            print("=" * 55 + "\n")

            if is_encrypt:
                plaintext = prompt_valid_text("Enter plaintext message to encrypt: ")
                ciphertext = encrypt_caesar_permuted(plaintext, key1, permuted)
                print("-" * 50)
                print(f"Plaintext (processed):  {plaintext}")
                print(f"Key 1 (Shift):          {key1}")
                print(f"Key 2 (Keyword):        {key2}")
                print(f"Ciphertext (result):    {ciphertext}")
                print("-" * 50)
            else:
                ciphertext = prompt_valid_text("Enter ciphertext to decrypt: ")
                plaintext = decrypt_caesar_permuted(ciphertext, key1, permuted)
                print("-" * 50)
                print(f"Ciphertext (input):     {ciphertext}")
                print(f"Key 1 (Shift):          {key1}")
                print(f"Key 2 (Keyword):        {key2}")
                print(f"Plaintext (decrypted):  {plaintext}")
                print("-" * 50)

        elif choice == '3':
            print("\n--- VIEW PERMUTED ALPHABET ---")
            key2 = prompt_valid_key2()
            permuted = build_permuted_alphabet(key2)
            print("\n" + format_alphabet_table(permuted, f"Permuted Alphabet (Keyword: {key2})"))

        elif choice == '4':
            print("Exiting Task 1.2.")
            break
        else:
            print("Invalid option selected. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_interactive_task2()
