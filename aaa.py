"""Output screams."""

import random
# import time
import argparse


def argparser():
    """Return an ArgumentParser with the required arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--length", type=int, default=18,
        help="how many characters to print; defaults to 18"
        )
    parser.add_argument(
        "-c", "--chars", default="aA",
        help="which characters to use; defaults to 'aA'"
        )
    return parser


def aaa(length, chars):
    """Print a string of `length` `chars`. """
    for _ in range(length):
        print(random.choice(chars), end="")


def main(argv=None):
    """Main entry point for the program."""
    # start = time.time()
    parser = argparser()
    args = parser.parse_args(argv)
    aaa(args.length, args.chars)
    # end = time.time()
    # duration = end - start
    # print("Duration:", duration)


if __name__ == "__main__":
    main()
