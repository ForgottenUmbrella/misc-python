#!/usr/bin/env python3
# coding=utf-8
"""For a given letter, determine its place in the Roman alphabet."""
import string
import argparse


def nth_letter(n):
    """Return the nth letter of the alphabet."""
    LETTERS = string.ascii_lowercase
    # Account for zero indexing.
    letter = LETTERS[n - 1]
    return letter


def letter_number(letter):
    """Return the number of the letter in the alphabet."""
    LETTERS = string.ascii_lowercase
    # Account for zero indexing.
    number = LETTERS.index(letter) + 1
    return number


def main(argv=None):
    """Output the number of the letter input."""
    argparser = argparse.ArgumentParser(
        description="Determine the number of the letter, or the nth letter."
        )
    argparser.add_argument("letter", help="letter (or number) to determine")
    argparser.add_argument(
        "-r", "--reverse", action="store_true", default=False,
        help="whether to get the letter given the number instead"
        )
    args = argparser.parse_args(argv)
    if not args.reverse:
        result = letter_number(args.letter)
    else:
        result = nth_letter(int(args.letter))
    print(result)


if __name__ == "__main__":
    main()
