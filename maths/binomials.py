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
    """Yield terms in the expanded form of (a + b)^n."""
    # Handle formatting special cases for powers of zero and one.
    if n == 0:
        yield "1"
        return
    if n == 1:
        yield f"{a} + {b}"
        return

    coefficients = pascal_triangle(n)
    # Handle formatting special case of coefficient of 1.
    next(coefficients)
    yield f"{a}^{n}"
    for i in range(1, n):
        coefficient = next(coefficients)
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
        yield "".join(term)
    yield f"{b}^{n}"


def pascal_triangle(n):
    """Yield numbers from the nth row of Pascal's triangle."""
    if n < 0:
        raise ValueError("Negative rows don't exist.")

    # Handle special case of zeroth number of each row.
    rows = [[1] for _ in range(n + 1)]
    yield 1
    for column in range(1, n + 1):
        # Handle special case of last number of each row.
        rows[column].append(1)
        for row in range(column + 1, n + 1):
            prev_row = rows[row - 1]
            result = prev_row[column - 1] + prev_row[column]
            rows[row].append(result)
        if column != n:
            yield result
        else:
            yield 1



def main(argv=None):
    """Print the expansion of a binomial."""
    argparser = ArgParser()
    args = argparser.parse_args(argv)
    for i, term in enumerate(binomial_expansion(args.n, a=args.a, b=args.b)):
        # Don't print a plus for the last number.
        if i != args.n:
            end = " + "
        else:
            end = ""
        print(term, end=end, flush=True)
    print()


def test():
    """Test functions."""
    assert list(pascal_triangle(0)) == [1]
    assert list(pascal_triangle(1)) == [1, 1]
    assert list(pascal_triangle(2)) == [1, 2, 1]
    assert list(pascal_triangle(3)) == [1, 3, 3, 1]
    assert list(pascal_triangle(4)) == [1, 4, 6, 4, 1]


if __name__ == "__main__":
    test()
    main()
