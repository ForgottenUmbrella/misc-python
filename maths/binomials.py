#!/usr/bin/env python3
# coding=utf-8
"""Functions for calculating the binomial expansion of any power."""
import argparse


class ArgParser(argparse.ArgumentParser):
    """ArgumentParser for this program."""

    def __init__(self):
        super().__init__(
            description="print the binomial expansion of any power",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self.add_argument("n", type=int, help="power to raise the binomial to")
        self.add_argument(
            "-a", default="a", help="first variable of the binomial"
        )
        self.add_argument(
            "-b", default="b", help="second variable of the binomial"
        )


def binomial_expansion(n, a="a", b="b"):
    """Return the expanded form of (a + b)^n."""
    if n == 0:
        return 1
    elif n == 1:
        return f"{a} + {b}"
    coefficients = pascal_triangle(n + 1)[n]
    result = [f"{a}^{n}"]
    for i in range(1, n):
        coefficient = coefficients[i]
        term_parts = {
            a: n - i,
            b: i
        }
        term = [str(coefficient)]
        for variable, power in term_parts.items():
            if power == 1:
                term.append(variable)
            else:
                term.append(f"({variable}^{power})")
        result.append("".join(term))
    result.append(f"{b}^{n}")
    return " + ".join(result)


def pascal_triangle(n):
    """Return n rows of Pascal's triangle."""
    if n == 0:
        return []
    rows = [[1]]
    for i in range(n - 1):
        prev_row = [0] + rows[i] + [0]
        new_row = []
        for j, num in enumerate(prev_row[:-1]):
            new_row.append(num + prev_row[j + 1])
        rows.append(new_row)
    return rows


def main(argv=None):
    """Print the expansion of a binomial."""
    argparser = ArgParser()
    args = argparser.parse_args(argv)
    print(binomial_expansion(args.n, a=args.a, b=args.b))


if __name__ == "__main__":
    main()
