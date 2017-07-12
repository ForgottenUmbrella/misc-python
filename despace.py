#!/usr/bin/env python3
import sys


def remove_chars(text, chars):
    """Return `text` with all `chars` removed"""
    new_text = "".join([char for char in text if char not in chars])
    return new_text


def main(text):
    """Print and return despaced `text`."""
    despaced = remove_chars(text, ' ')
    print(despaced)
    return despaced


if __name__ == '__main__':
    if sys.argv[1:]:
        text = ' '.join(sys.argv[1:])
    else:
        text = input('Text to despace: ')
    main(text)
