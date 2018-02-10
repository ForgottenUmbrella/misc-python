#!/usr/bin/env python3
# coding=utf-8
"""Determine which questions to do (by letter) when asked to do the nth
column.
"""
import argparse

import letter_number


def main(argv=None):
    """Print question letters for a given column."""
    argparser = argparse.ArgumentParser(
        description="Determine which questions to do, given a column number."
        )
    argparser.add_argument("last_letter", help="letter of last question")
    argparser.add_argument(
        "column_number", type=int, help="column number to get questions for"
        )
    args = argparser.parse_args(argv)

    column_number = args.column_number
    last_letter = args.last_letter
    total_num_questions = letter_number.letter_number(last_letter)

    question_letters = []
    for n in range(column_number, total_num_questions + 1, column_number):
        question_letter = letter_number.nth_letter(n)
        question_letters.append(question_letter)
    print(", ".join(question_letters))


if __name__ == "__main__":
    main()


