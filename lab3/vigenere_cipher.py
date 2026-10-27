import sys
from typing import List
from romanian_alphabet import (
    ROMANIAN_ALPHABET,
    ALPHABET_SIZE,
    CHAR_TO_INDEX,
    INDEX_TO_CHAR,
    validate_key,
    validate_text,
    format_alphabet_table,
)


def encrypt_vigenere(plaintext: str, key: str) -> str:
    """Encrypts plaintext using Vigenere cipher: ci = (mi + ki) mod 31."""
    cipher_chars: List[str] = []
    key_len = len(key)

    for i, char in enumerate(plaintext):
        m_i = CHAR_TO_INDEX[char]
        k_i = CHAR_TO_INDEX[key[i % key_len]]
        c_i = (m_i + k_i) % ALPHABET_SIZE
        cipher_chars.append(INDEX_TO_CHAR[c_i])

    return "".join(cipher_chars)


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    """Decrypts ciphertext using Vigenere cipher: mi = (ci - ki) mod 31."""
    plain_chars: List[str] = []
    key_len = len(key)

    for i, char in enumerate(ciphertext):
        c_i = CHAR_TO_INDEX[char]
        k_i = CHAR_TO_INDEX[key[i % key_len]]
        # Python's modulo operator handles negative numbers correctly: (-k) % 31 -> [0..30]
        m_i = (c_i - k_i) % ALPHABET_SIZE
        plain_chars.append(INDEX_TO_CHAR[m_i])

    return "".join(plain_chars)


def format_vigenere_table(text: str, key: str, is_encrypt: bool = True) -> str:
    """Formats calculation table matching the mathematical model shown in the lab guide."""
    key_len = len(key)
    repeated_key = [key[i % key_len] for i in range(len(text))]

    text_indices = [CHAR_TO_INDEX[c] for c in text]
    key_indices = [CHAR_TO_INDEX[k] for k in repeated_key]

    if is_encrypt:
        res_indices = [(m + k) % ALPHABET_SIZE for m, k in zip(text_indices, key_indices)]
        res_label = "M + K (mod 31)"
        text_label = "Plaintext M"
        res_text_label = "Ciphertext C"
    else:
        res_indices = [(c - k) % ALPHABET_SIZE for c, k in zip(text_indices, key_indices)]
        res_label = "C - K (mod 31)"
        text_label = "Ciphertext C"
        res_text_label = "Plaintext M"

    res_chars = [INDEX_TO_CHAR[r] for r in res_indices]

    lines = [
        f"{text_label:<16}: " + " ".join(f"{c:>2}" for c in text),
        f"{'Key K':<16}: " + " ".join(f"{k:>2}" for k in repeated_key),
        f"{text_label:<16}: " + " ".join(f"{idx:>2}" for idx in text_indices),
        f"{'Key K':<16}: " + " ".join(f"{idx:>2}" for idx in key_indices),
        f"{res_label:<16}: " + " ".join(f"{idx:>2}" for idx in res_indices),
        f"{res_text_label:<16}: " + " ".join(f"{c:>2}" for c in res_chars),
    ]
    return "\n".join(lines)


def prompt_valid_key() -> str:
    while True:
        try:
            raw = input("Enter key (at least 7 Romanian letters): ")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, err, cleaned = validate_key(raw)
        if is_valid:
            return cleaned
        print(f"\n{err}\nPlease try again.\n")


def prompt_valid_text(prompt_message: str) -> str:
    while True:
        try:
            raw = input(prompt_message)
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, err, cleaned = validate_text(raw)
        if is_valid:
            return cleaned
        print(f"\n{err}\nPlease try again.\n")


def run_interactive_task3_2() -> None:
    """Interactive command-line loop for Task 3.2."""
    print("=" * 60)
    print(" TASK 3.2: VIGENÈRE CIPHER OVER THE ROMANIAN ALPHABET (n = 31) ")
    print("=" * 60)
    print(format_alphabet_table(ROMANIAN_ALPHABET, "Standard Romanian Alphabet (31 letters)"))
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
            ciphertext = encrypt_vigenere(plaintext, key)
            print("-" * 50)
            print(f"Original Text (processed): {plaintext}")
            print(f"Key (K):                   {key}")
            print(f"Encrypted Ciphertext (C): {ciphertext}")
            print("-" * 50)
            print("\nStep-by-step mathematical calculation table:")
            print(format_vigenere_table(plaintext, key, is_encrypt=True))
            print("-" * 50)

        elif choice == '2':
            print("\n--- DECRYPTION ---")
            key = prompt_valid_key()
            ciphertext = prompt_valid_text("Enter ciphertext to decrypt: ")
            plaintext = decrypt_vigenere(ciphertext, key)
            print("-" * 50)
            print(f"Ciphertext (C):           {ciphertext}")
            print(f"Key (K):                   {key}")
            print(f"Decrypted Plaintext (M):  {plaintext}")
            print("-" * 50)
            print("\nStep-by-step mathematical calculation table:")
            print(format_vigenere_table(ciphertext, key, is_encrypt=False))
            print("-" * 50)

        elif choice == '3':
            print()
            print(format_alphabet_table(ROMANIAN_ALPHABET, "Standard Romanian Alphabet (31 letters)"))

        elif choice == '4':
            print("Exiting Task 3.2.")
            break
        else:
            print("Invalid option selected. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_interactive_task3_2()
