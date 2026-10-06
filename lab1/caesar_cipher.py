"""
Task 1.1: Caesar Cipher over the Romanian Alphabet.
Complies with Laboratory Work No. 1:
- Alphabet length n = 31 (Table 2 encoding).
- Key k in {1, 2, ..., 30}.
- Encryption formula: c = (x + k) mod 31
- Decryption formula: m = (y - k) mod 31
- Full validation with re-prompting on invalid input.
"""

import sys
from typing import Optional
from romanian_alphabet import (
    ROMANIAN_ALPHABET,
    ALPHABET_SIZE,
    CHAR_TO_INDEX,
    INDEX_TO_CHAR,
    validate_text,
    validate_key,
    format_alphabet_table,
)


def encrypt_caesar(plaintext: str, key: int) -> str:
    """
    Encrypts a validated plaintext using Caesar cipher with numeric shift key.
    c = (x + k) mod 31
    Uses Table 2 letter encoding explicitly.
    """
    ciphertext_chars = []
    for char in plaintext:
        x = CHAR_TO_INDEX[char]
        c_code = (x + key) % ALPHABET_SIZE
        ciphertext_chars.append(INDEX_TO_CHAR[c_code])
    return "".join(ciphertext_chars)


def decrypt_caesar(ciphertext: str, key: int) -> str:
    """
    Decrypts a validated ciphertext using Caesar cipher with numeric shift key.
    m = (y - k) mod 31
    Uses Table 2 letter encoding explicitly.
    """
    plaintext_chars = []
    for char in ciphertext:
        y = CHAR_TO_INDEX[char]
        m_code = (y - key) % ALPHABET_SIZE
        plaintext_chars.append(INDEX_TO_CHAR[m_code])
    return "".join(plaintext_chars)


def prompt_valid_key() -> int:
    """
    Prompts the user repeatedly until a valid key (integer 1..30) is provided.
    """
    while True:
        try:
            raw_key = input("Enter shift key (integer between 1 and 30): ")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, err, key_val = validate_key(raw_key)
        if is_valid:
            return key_val
        print(f"\n{err}\nPlease try again.\n")


def prompt_valid_text(prompt_msg: str) -> str:
    """
    Prompts the user repeatedly until valid text (Romanian alphabet letters) is provided.
    Spaces are removed and text is converted to uppercase.
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


def run_interactive_task1() -> None:
    """
    Interactive command-line loop for Task 1.1.
    """
    print("=" * 60)
    print(" TASK 1.1: CAESAR CIPHER OVER THE ROMANIAN ALPHABET (n = 31) ")
    print("=" * 60)
    print(format_alphabet_table(ROMANIAN_ALPHABET, "Standard Romanian Alphabet (Table 2)"))
    print()

    while True:
        print("\nChoose an option:")
        print("  1. Encrypt a message")
        print("  2. Decrypt a message")
        print("  3. Display alphabet table")
        print("  4. Return to main menu / Exit")
        choice = input("Select option (1-4): ").strip()

        if choice == '1':
            print("\n--- ENCRYPTION ---")
            key = prompt_valid_key()
            plaintext = prompt_valid_text("Enter plaintext message to encrypt: ")
            ciphertext = encrypt_caesar(plaintext, key)
            print("-" * 40)
            print(f"Original Text (processed): {plaintext}")
            print(f"Shift Key:                 {key}")
            print(f"Encrypted Ciphertext:      {ciphertext}")
            print("-" * 40)

        elif choice == '2':
            print("\n--- DECRYPTION ---")
            key = prompt_valid_key()
            ciphertext = prompt_valid_text("Enter ciphertext to decrypt: ")
            plaintext = decrypt_caesar(ciphertext, key)
            print("-" * 40)
            print(f"Ciphertext:                {ciphertext}")
            print(f"Shift Key:                 {key}")
            print(f"Decrypted Plaintext:       {plaintext}")
            print("-" * 40)

        elif choice == '3':
            print()
            print(format_alphabet_table(ROMANIAN_ALPHABET, "Standard Romanian Alphabet (Table 2)"))

        elif choice == '4':
            print("Exiting Task 1.1.")
            break
        else:
            print("Invalid option selected. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_interactive_task1()
