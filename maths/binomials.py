#!/usr/bin/env python3
# coding=utf-8
"""Functions for calculating the binomial expansion of any power."""
import argparse
import time


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
        self.add_argument(
            "--bowap", type=float, default="0",
            help="time to wait between terms in seconds"
        )


def binomial_expansion(n, a="a", b="b"):
    """Yield terms in the expanded form of (a + b)^n."""
    if n == 0:
        return "1"  # Uncomment me A.
        # yield "1"  # Uncomment me B.
        # return  # Uncomment me B.
    if n == 1:
        return f"{a} + {b}"  # Uncomment me A.
        # yield f"{a} + {b}"  # Uncomment me B.
        # return  # Uncomment me B.
    coefficients = list(pascal_triangle(n))
    # coefficients = pascal_triangle(n + 1)[n]  # Uncomment me B.
    result = [f"{a}^{n}"]  # Uncomment me A.
    # yield f"{a}^{n}"  # Uncomment me B.
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
        result.append("".join(term))  # Uncomment me A.
        # yield " + " + "".join(term)  # Uncomment me B.
    result.append(f"{b}^{n}")  # Uncomment me A.
    # yield f" + {b}^{n}"  # Uncomment me B.
    return " + ".join(result)  # Uncomment me A.


# def pascal_triangle(n):
#     """Return n rows of Pascal's triangle."""
#     if n == 0:
#         return []
#     rows = [[1]]
#     for i in range(n - 1):
#         prev_row = [0] + rows[i] + [0]
#         new_row = []
#         for j, num in enumerate(prev_row[:-1]):
#             new_row.append(num + prev_row[j + 1])
#         rows.append(new_row)
#     return rows


def pascal_triangle(n):
    """Yield numbers from the nth row of Pascal's triangle."""
    if n < 0:
        raise ValueError("Negative rows don't exist.")
    # Handle special case of zeroth number of each row.
    rows = [[1] for _ in range(n + 1)]
    yield 1
    for column in range(1, n + 1):
        # Handle special case of last number of each row.
        rows[column].append(1)  # rows[column][column] = 1
        for row in range(column + 1, n + 1):
            prev_row = rows[row - 1]
            result = prev_row[column - 1] + prev_row[column]
            rows[row].append(result)  # rows[row][column] = result
        if column != n:
            yield result
        else:
            yield 1



def main(argv=None):
    """Print the expansion of a binomial."""
    argparser = ArgParser()
    args = argparser.parse_args(argv)
    plus = " + "
    for i, term in enumerate(
            binomial_expansion(args.n, a=args.a, b=args.b).split(plus)
    ):
    # for term in binomial_expansion(args.n, a=args.a, b=args.b):  # Uncomment me B.
        if i != args.n:
            end = plus
        else:
            end = ""
        print(term, end=end, flush=True)  # Uncomment me B.
        if args.bowap:  # Uncomment me B.
            time.sleep(args.bowap)  # Uncomment me B.
    print()  # Uncomment me B.


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
# TODO: Rewrite binomial_expansion to use pascal_triangle as generator.
