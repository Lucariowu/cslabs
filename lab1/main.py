#!/usr/bin/env python3
"""
Main Entry Point for Laboratory Work No. 1: Caesar Cipher & Caesar Cipher with Permutation.
Course: Cryptography & Security (CS)
Author: Șoimu Ionuț (FAF-243)
Instructor: Zaica Maia
"""

import sys
import argparse
from romanian_alphabet import (
    ROMANIAN_ALPHABET,
    validate_key,
    validate_keyword,
    validate_text,
    build_permuted_alphabet,
    format_alphabet_table,
)
from caesar_cipher import (
    encrypt_caesar,
    decrypt_caesar,
    run_interactive_task1,
)
from caesar_permuted import (
    encrypt_caesar_permuted,
    decrypt_caesar_permuted,
    run_interactive_task2,
)


def run_automated_demo() -> None:
    """
    Runs a demonstration covering both tasks and error handling cases.
    """
    print("=" * 70)
    print(" AUTOMATED DEMONSTRATION OF LABORATORY WORK NO. 1 ")
    print("=" * 70)

    # 1. Task 1.1 Standard Caesar
    print("\n--- [DEMO 1] Task 1.1: Single Key Caesar Cipher (Romanian Alphabet) ---")
    demo_text = "Cifrul Cezar cu caractere românești: Șoimu Ionuț!"
    k = 5
    print(f"Input text:     '{demo_text}'")
    is_valid, err, clean = validate_text("Cifrul Cezar cu caractere românești Șoimu Ionuț")
    print(f"Cleaned text:   '{clean}'")
    print(f"Shift key (k):  {k}")
    c = encrypt_caesar(clean, k)
    print(f"Encrypted:      '{c}'")
    m = decrypt_caesar(c, k)
    print(f"Decrypted:      '{m}'")
    assert clean == m, "Decryption match check failed!"
    print("Decryption verification: SUCCESS (Matches original text)")

    # 2. Task 1.2 Caesar with Permutation
    print("\n--- [DEMO 2] Task 1.2: Two-Key Caesar Cipher (Permuted Alphabet) ---")
    keyword = "CRIPTOGRAFIE"
    shift = 3
    print(f"Keyword (Key 2): '{keyword}' (Length: {len(keyword)} >= 7)")
    print(f"Shift (Key 1):   {shift}")
    permuted = build_permuted_alphabet(keyword)
    print(format_alphabet_table(permuted, f"Permuted Alphabet (Keyword: {keyword})"))
    
    clean_msg = "CALCULATOARE SI MICROELECTRONICA"
    clean_msg = validate_text(clean_msg)[2]
    print(f"\nMessage:        '{clean_msg}'")
    c2 = encrypt_caesar_permuted(clean_msg, shift, permuted)
    print(f"Encrypted:      '{c2}'")
    m2 = decrypt_caesar_permuted(c2, shift, permuted)
    print(f"Decrypted:      '{m2}'")
    assert clean_msg == m2, "Decryption match check failed!"
    print("Decryption verification: SUCCESS (Matches original text)")

    # 3. Input Validation Demonstrations
    print("\n--- [DEMO 3] Error Handling & Validation Demonstrations ---")
    
    # 3a. Invalid key out of range
    print("\n[Test 3a] Key out of range (Key = 35):")
    valid, err, _ = validate_key("35")
    print(f"Validation result: valid={valid}")
    print(f"Message: {err}")

    # 3b. Invalid key non-integer
    print("\n[Test 3b] Non-numeric key (Key = 'xyz'):")
    valid, err, _ = validate_key("xyz")
    print(f"Validation result: valid={valid}")
    print(f"Message: {err}")

    # 3c. Invalid character in text
    print("\n[Test 3c] Text with invalid non-Romanian characters ('Cripto #123'):")
    valid, err, _ = validate_text("Cripto #123")
    print(f"Validation result: valid={valid}")
    print(f"Message:\n{err}")

    # 3d. Keyword too short
    print("\n[Test 3d] Keyword too short (Keyword = 'ROM'):")
    valid, err, _ = validate_keyword("ROM")
    print(f"Validation result: valid={valid}")
    print(f"Message: {err}")

    print("\n" + "=" * 70)
    print(" DEMONSTRATION COMPLETE ")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Laboratory Work No. 1: Caesar Cipher & Caesar Cipher with Permutation"
    )
    parser.add_argument("--task", type=int, choices=[1, 2], help="Task number (1 or 2)")
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], help="Operation mode")
    parser.add_argument("--key", type=int, help="Shift key for Task 1 (1..30)")
    parser.add_argument("--key1", type=int, help="Shift key for Task 2 (1..30)")
    parser.add_argument("--key2", type=str, help="Keyword for Task 2 (>= 7 Romanian chars)")
    parser.add_argument("--text", type=str, help="Input message or ciphertext")
    parser.add_argument("--demo", action="store_true", help="Run automated test & demonstration suite")

    args = parser.parse_args()

    if args.demo:
        run_automated_demo()
        return

    # Non-interactive CLI invocation if arguments are passed
    if args.task is not None:
        if args.task == 1:
            if not args.mode or args.key is None or not args.text:
                print("Error: Task 1 requires --mode, --key, and --text arguments.")
                sys.exit(1)
            is_valid_k, err_k, key_val = validate_key(str(args.key))
            if not is_valid_k:
                print(err_k)
                sys.exit(1)
            is_valid_t, err_t, clean_t = validate_text(args.text)
            if not is_valid_t:
                print(err_t)
                sys.exit(1)

            if args.mode == "encrypt":
                res = encrypt_caesar(clean_t, key_val)
                print(f"Plaintext:  {clean_t}")
                print(f"Key:        {key_val}")
                print(f"Ciphertext: {res}")
            else:
                res = decrypt_caesar(clean_t, key_val)
                print(f"Ciphertext: {clean_t}")
                print(f"Key:        {key_val}")
                print(f"Plaintext:  {res}")

        elif args.task == 2:
            if not args.mode or args.key1 is None or not args.key2 or not args.text:
                print("Error: Task 2 requires --mode, --key1, --key2, and --text arguments.")
                sys.exit(1)
            is_valid_k1, err_k1, k1_val = validate_key(str(args.key1))
            if not is_valid_k1:
                print(err_k1)
                sys.exit(1)
            is_valid_k2, err_k2, k2_val = validate_keyword(args.key2)
            if not is_valid_k2:
                print(err_k2)
                sys.exit(1)
            is_valid_t, err_t, clean_t = validate_text(args.text)
            if not is_valid_t:
                print(err_t)
                sys.exit(1)

            permuted = build_permuted_alphabet(k2_val)
            print(format_alphabet_table(permuted, f"Permuted Alphabet (Keyword: {k2_val})"))
            print()

            if args.mode == "encrypt":
                res = encrypt_caesar_permuted(clean_t, k1_val, permuted)
                print(f"Plaintext:  {clean_t}")
                print(f"Key 1:      {k1_val}")
                print(f"Key 2:      {k2_val}")
                print(f"Ciphertext: {res}")
            else:
                res = decrypt_caesar_permuted(clean_t, k1_val, permuted)
                print(f"Ciphertext: {clean_t}")
                print(f"Key 1:      {k1_val}")
                print(f"Key 2:      {k2_val}")
                print(f"Plaintext:  {res}")
        return

    # Interactive Menu
    while True:
        print("\n" + "=" * 60)
        print(" LABORATORY WORK NO. 1: CAESAR CIPHER IMPLEMENTATION ")
        print(" Course: Cryptography & Security | UTM FCIM FAF-243 ")
        print(" Author: Șoimu Ionuț | Supervisor: Zaica Maia ")
        print("=" * 60)
        print("  1. Task 1.1: Caesar Cipher over Romanian Alphabet")
        print("  2. Task 1.2: Caesar Cipher with Two Keys (Permutation)")
        print("  3. Run Automated Demonstration & Validation")
        print("  4. Exit")
        print("=" * 60)
        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            run_interactive_task1()
        elif choice == '2':
            run_interactive_task2()
        elif choice == '3':
            run_automated_demo()
        elif choice == '4':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose an option between 1 and 4.")


if __name__ == "__main__":
    main()
