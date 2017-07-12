#!/usr/bin/env python
# Python script with my own original prime-generating function.


def gen_primes(n):
    """Yield n primes.

    Funnily enough, using the `is_prime()` function to generate primes
    is inefficient.
    """
    primes_list = []
    possible_prime = 2
    while len(primes_list) < n:
        if all(possible_prime % prime != 0 for prime in primes_list):
        # for prime in primes_list:
        #     if possible_prime % prime == 0:
        #         break
        # else:
            primes_list.append(possible_prime)
            yield possible_prime
        possible_prime += 1


def nth_prime(n):
    """Return the nth prime."""
    for prime in gen_primes(n):
        pass
    return prime


def is_prime(n):
    """Return whether `n` is a prime.

    Funnily enough, using the `gen_primes()` function to check for
    membership is inefficient.
    """
    if any(n % i == 0 for i in range(2, n)):
        return False
    else:
        return True
