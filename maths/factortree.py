#!/usr/bin/env python3
# coding=utf-8
"""Print a factor tree for any given number."""

import argparse
import collections
import logging


# logging.basicConfig(level=logging.DEBUG)


class MyArgparser(argparse.ArgumentParser):
    """ArgumentParser for this script."""
    def __init__(self):
        super().__init__(description="print prime factors")
        self.add_argument("n", type=int, help="number to get prime factors of")


class BinaryTree:
    """A binary tree defined recursively, with binary trees as nodes.

    http://openbookproject.net/thinkcs/python/english3e/trees.html
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        """Return the value of the node."""
        return str(self.value)

    # def repr(self, level=0):
    #     """Return a string representation of the tree."""
    #     if self is None:
    #         return "\n"
    #     rep = self.right.repr(level + 1)
    #     rep += "    " * level + str(self.value)
    #     rep += self.left.repr(level + 1)
    #     return rep

    def add(self, tree):
        """Add a branch to the tree."""
        if self.left is None:
            self.left = tree
        elif self.right is None:
            self.right = tree
        else:
            raise ValueError("Tree full.")
        logging.debug(f"tree =\n{repr_tree(tree)}")


def repr_tree(tree, level=0):
    """Return a string representation of a tree."""
    if tree is None:
        return "\n"
    representation = repr_tree(tree.right, level + 1)
    representation += "    " * level + str(tree.value)
    representation += repr_tree(tree.left, level + 1)
    return representation


def factor(n):
    """Return a tuple of two factors of a number.

    If `n` cannot be factored (prime or less than 2), then return `None`.
    """
    for potential_factor in range(2, n):
        if n % potential_factor == 0:
            other_factor = int(n / potential_factor)
            factors = (potential_factor, other_factor)
            logging.debug(f"factor({n}) = {factors}")
            return factors
    return None


def is_prime(n):
    """Return whether a number is prime."""
    prime_check = factor(n) is None and n >= 2
    logging.debug(f"{n} prime? {prime_check}")
    return prime_check


def prime_factor(n):
    """Return a Counter of the prime factors of a number."""
    counter = collections.Counter()
    if is_prime(n):
        # Counters only accept iterables and maps, so `n` must be in a
        # list.
        counter.update([n])
        return counter
    if n < 2:
        counter.update([None])
        return counter

    for i in factor(n):
        if is_prime(i):
            primes = [i]
        else:
            primes = prime_factor(i)
        counter.update(primes)
    return counter


def product(nums):
    """Return the product of some numbers."""
    result = 1
    for num in nums:
        result *= num
    return result


def format_tree_prime(n):
    """Return `n` "circled" to emphasise that it's prime."""
    # Backspace once to overwrite a space with a parenthesis because it
    # looks nicer.
    return f"\b({n})"


def factor_tree(n):
    """Return a tree of factors of a number."""
    logging.debug(f"in factor_tree({n})")
    if is_prime(n):
        root = BinaryTree(format_tree_prime(n))
        return root

    root = BinaryTree(n)
    for i in factor(n):
        if is_prime(i):
            branch = BinaryTree(format_tree_prime(i))
        else:
            branch = factor_tree(i)
        root.add(branch)
        logging.debug(f"root so far =\n{repr_tree(root)}")
    return root


def main(argv=None):
    """Print a factor tree."""
    argparser = MyArgparser()
    args = argparser.parse_args(argv)
    primes = prime_factor(args.n)
    print(
        f"{args.n} = "
        + " * ".join(f"{prime}^{count}" for prime, count in primes.items())
        )
    is_correct = (
        product(prime ** count for prime, count in primes.items()) == args.n
        )
    print(repr_tree(factor_tree(args.n)))
    # tree = BinaryTree(
    #     12, BinaryTree(2), BinaryTree(6, BinaryTree(3), BinaryTree(2))
    #     )
    # print(repr_tree(tree))
    assert is_correct, "Factorisation failed."


if __name__ == "__main__":
    assert factor(12) == (2, 6), "Unexpected factorisation."
    assert factor(2) is None, "Primes cannot be factored."
    assert factor(-1) is None, "Numbers less than 2 cannot be factored."

    assert not is_prime(12), "Composites are not primes."
    assert is_prime(2), "Primes should be primes."
    assert not is_prime(-1), "Numbers less than 2 are not primes."

    assert prime_factor(12) == {
        3: 1,
        2: 2,
        }, "Unexpected prime factors."
    assert prime_factor(2) == {
        2: 1,
        }, "Unexpected prime factors of a prime."
    assert prime_factor(-1) == {
        None: 1,
        }, "Unexpected prime factors for a number without prime factors."

    assert product((12, 2, -1)) == -24, "Unexpected product."

    main()
