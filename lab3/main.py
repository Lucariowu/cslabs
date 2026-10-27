#!/usr/bin/env python3
"""
Main Entry Point for Laboratory Work No. 3: Polyalphabetic Ciphers (Task 3.2 - Vigenère Cipher).
Course: Cryptography & Security (CS)
Author: Șoimu Ionuț (FAF-243)
Supervisor: Zaica Maia
"""

import sys
import argparse
from romanian_alphabet import (
    ROMANIAN_ALPHABET,
    validate_key,
    validate_text,
    format_alphabet_table,
)
from vigenere_cipher import (
    encrypt_vigenere,
    decrypt_vigenere,
    format_vigenere_table,
    run_interactive_task3_2,
)


def main():
    parser = argparse.ArgumentParser(
        description="Laboratory Work No. 3: Polyalphabetic Ciphers (Task 3.2 - Vigenère Cipher)"
    )
    parser.add_argument("--task", type=int, choices=[2], default=2, help="Task number (2 for Task 3.2)")
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], help="Operation mode")
    parser.add_argument("--key", type=str, help="Vigenere key (at least 7 Romanian letters)")
    parser.add_argument("--text", type=str, help="Input message or ciphertext")

    args = parser.parse_args()

    # Non-interactive CLI invocation if arguments are passed
    if args.mode:
        if not args.key or not args.text:
            print("Error: CLI mode requires both --key and --text arguments.")
            sys.exit(1)

        is_valid_k, err_k, clean_key = validate_key(args.key)
        if not is_valid_k:
            print(err_k)
            sys.exit(1)

        is_valid_t, err_t, clean_text = validate_text(args.text)
        if not is_valid_t:
            print(err_t)
            sys.exit(1)

        if args.mode == "encrypt":
            res = encrypt_vigenere(clean_text, clean_key)
            print(f"Plaintext:  {clean_text}")
            print(f"Key:        {clean_key}")
            print(f"Ciphertext: {res}")
        else:
            res = decrypt_vigenere(clean_text, clean_key)
            print(f"Ciphertext: {clean_text}")
            print(f"Key:        {clean_key}")
            print(f"Plaintext:  {res}")
        return

    # Interactive Menu matching Lab 1 layout
    while True:
        print("\n" + "=" * 60)
        print(" LABORATORY WORK NO. 3: VIGENÈRE CIPHER IMPLEMENTATION ")
        print(" Course: Cryptography & Security | UTM FCIM FAF-243 ")
        print(" Author: Șoimu Ionuț | Supervisor: Zaica Maia ")
        print("=" * 60)
        print("  1. Task 3.2: Vigenère Cipher over Romanian Alphabet")
        print("  2. Exit")
        print("=" * 60)
        try:
            choice = input("Enter choice (1-2): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application. Goodbye!")
            break

        if choice == '1':
            run_interactive_task3_2()
        elif choice == '2':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1 or 2.")


if __name__ == "__main__":
    main()
