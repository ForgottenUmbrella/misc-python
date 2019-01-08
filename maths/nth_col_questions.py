#!/usr/bin/env python3
# coding=utf-8
"""Determine which questions to do (by letter) when asked to do the nth
column or a given number of questions.
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
    argparser.add_argument(
        "-n", "--num-questions", action="store_true",
        help="interpret column_number to be the number of questions to get"
    )
    argparser.add_argument(
        "-l", "--include-last", action="store_true",
        help="include last question"
    )
    args = argparser.parse_args(argv)

    total_num_questions = letter_number.letter_number(args.last_letter)

    if args.num_questions:
        step = round(total_num_questions / args.column_number)
    else:
        step = args.column_number

    if args.include_last:
        start = total_num_questions
        end = 0
        step = -step
    else:
        start = step
        end = total_num_questions + 1

    question_letters = []
    for i in range(start, end, step):
        question_letter = letter_number.nth_letter(i)
        question_letters.append(question_letter)

    if args.include_last:
        question_letters.reverse()
    print(", ".join(question_letters))


if __name__ == "__main__":
    main()
