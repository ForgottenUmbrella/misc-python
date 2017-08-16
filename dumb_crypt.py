#!/usr/bin/env python3
# coding=utf-8
"""Encrypt a string using itself as the password.

Decrypting requires that you know what the decrypted string will be...
"""
import argparse
import getpass
import base64


class MyArgparser(argparse.ArgumentParser):
    """ArgumentParser suited for this script."""
    def __init__(self):
        super().__init__(description="encrypt/decrypt with itself")
        self.add_argument("text", help="string to encrypt/decrypt")
        self.add_argument(
            "-d", "--decrypt", action="store_true", default=False,
            help="decrypt text instead of encrypting"
            )


def encrypt(plaintext):
    """Return a string encrypted with itself."""
    key = plaintext
    encoded = []
    for i, c in enumerate(plaintext):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(c) + ord(key_c)) % 256)
        encoded.append(encoded_c)
    # Encode and decode to convert from bytes to string.
    encoded = base64.urlsafe_b64encode("".join(encoded).encode()).decode()
    return encoded


def decrypt(ciphertext, key):
    """Return a decrypted string, supposed to be equal to the key."""
    decoded = []
    encoded = base64.urlsafe_b64decode(ciphertext).decode()
    for i, c in enumerate(encoded):
        key_c = key[i % len(key)]
        decoded_c = chr((256 + ord(c) - ord(key_c)) % 256)
        decoded.append(decoded_c)
    decoded = "".join(decoded)
    return decoded


def main(argv=None):
    """Encrypt or decrypt a provided string."""
    argparser = MyArgparser()
    args = argparser.parse_args(argv)
    if not args.decrypt:
        result = encrypt(args.text)
    else:
        key = getpass.getpass("Key: ")
        result = decrypt(args.text, key)
        if result != key:
            print("Decrypt failed!")
    print(result)


if __name__ == "__main__":
    main()


