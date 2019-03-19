"""
slow_prime — Slow prime number finder
"""

# Copyright © 2019 Moses Chong
#
# This file is part of the Slow Addressable Combinatorics Library (slowcomb)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# NOTE: This module is so trivial, I wanted to release it under CC0
#  or Public Domain, but I'll leave it as GPLv3 for now, just to keep
#  things simple. -Moses

from math import sqrt

def slow_prime(i):
    """Find the i'th prime number, using the slowest possible 
    linear search method.

    Arguments
    ---------
    i - integer: i'th prime number to be requested.

    Returns integer: i'th prime number
    Raises ValueError when i is negative or smaller than 1.
    Raises TypeError when i is not an `int`.

    Synopsis
    --------
    The process of finding the prime numbers is as follows:
    1. For all positive integers x, attempt to divide x by all
        positive integers smaller than x.
    2. Any term x that is found not to be divisible by any integer
        larger than one is regarded as a prime number.
    3. Repeat 1 and 2 until i prime numbers are found. Return the i'th
        prime number.
    
    This process can take a long time, particularly with later terms
    of i (> 1000), and is therefore used as a stand-in for slow 
    operations.

    As you will have noticed, the definition used for prime number herein
    is 'any positive integer with only two positive divisors: itself, and
    one', in line with the definition in OEIS A000040: The Prime Numbers.

    The speed advantages of using the Sieve of Eratosthenes have been
    completely disregarded.
    """

    if i < 1:
        raise ValueError("Argument must be a positive integer")
    if isinstance(i,int) is False:
        raise TypeError("Argument must be a positive integer")
    primes_found = 0
    a = 1
    while primes_found < i:
        a += 1
        assume_prime = True
        for b in range(a-1,1,-1):
            if(a % b == 0):
                assume_prime = False
                break
        if assume_prime is True:
            primes_found += 1
    return a


def faster_prime(i):
    """Find the i'th prime number, using the speedup techniques
    described in the Sieve of Eratosthenes.
    
    This function is assumed to be correct up to i=100000.
    The average time to find the 100000th prime was measured to be
    around 59 seconds on the standard test machine, a low-end 2017-vintage
    PC with an AMD A4-7210 processor running Fedora 29.

    Arguments
    ---------
    i - integer: i'th prime number to be requested.

    Returns integer: i'th prime number
    Raises ValueError when i is negative or smaller than 1.
    Raises TypeError when i is not an `int`.
    
    Synposis
    --------
    The process of finding the prime numbers is as follows:
    1. Skip all even numbers
    2. Input a tuple of the first 35 prime numbers.
    3a. If searching for any prime up to the 35th, check the tuple.
    3b. Else, check if all odd numbers is divisible the first 35 
    prime numbers.
    3c. Else, check if the odd numbers beyond the 35th prime, by
    attempting to divide them by all **odd numbers counting up from
    the 35th prime (149) to 1/149th of the number**
    4. Any term x that is found to be non-divisible in any part of step 3
        is a prime number.
    5. Repeat 3 and 4 until i prime numbers are found. Return the i'th
        prime number.
    
    This process is significantly faster than slow_prime, and is able
    to find the 1000th prime in as low as 1/30th of second on a low-end
    2017-vintage x86 PC running Python 3.7 on Fedora 29.

    However, the method is suspected to have a limited range, as very
    large primes will be falsely rejected by the division algorithm
    due to running out of numbers to divide by. The maximum range is
    currently assumed to be the number whose smallest factor is more
    than the 35th prime.

    The definition of prime number herein is the same as that in
    slow_prime() above.

    See: Wikipedia. Sieve of Eratosthenes.
        https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

    """
    if i < 1:
        raise ValueError("Argument must be a positive integer")
    if isinstance(i,int) is False:
        raise TypeError("Argument must be a positive integer")

    precalc_primes = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,
        67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149)
        # Precalculated n'th first primes
        #
        # NOTE: As of Python 3.7, tuples were found to be up to an order 
        #   of magnitude faster than lists in preliminary tests.
    lower_bound = len(precalc_primes)

    if i < lower_bound:
        # Use the precalculated primes if we are finding
        # a prime within its range.
        # This is actually essential for correct operation
        # of the algorithm below, as evaluating a prime number
        # in precalc_primes generates a false negative.
        return precalc_primes[i-1]

    primes_found = lower_bound
        # We are doing this to account for the first n'th primes
    a = precalc_primes[ len(precalc_primes)-1 ]
        # Start from the last precalculated prime

    while primes_found < i:
        assume_prime = True
        last_precalc_prime = precalc_primes[len(precalc_primes)-1]
        a += 2
            # Keep increasing a, as we check if it is a prime number.
            # Only deal with odd numbers, as all prime numbers are odd.
            # This dramatically reduces the number of divisions.

        for x in precalc_primes:
            # Sieve out all numbers divisible by the n'th first primes
            # NOTE: Only valid for numbers larger than the last number
            #  in the n'th first primes list.
            # NOTE: This can reduce the number of operations necessary
            #  to reach a particular prime number, but will increase
            #  the number of operations for actual prime numbers by
            #  the number of precalculated primes in the n'th first
            #  primes list.
            if a%x == 0:
                assume_prime = False
                break

        if assume_prime is True:
            for b in range(last_precalc_prime, a//last_precalc_prime, 2):
                # For all numbers not caught by the sieve above:
                # Only test with odd numbers from the last prime
                # to a fraction of our candidate number.
                # 
                # 1. We can make use of the distributive nature of
                #   multiplication to find out if an odd number is not
                #   a prime sooner. The distributive nature of 
                #   multiplication states that when a larger divisor
                #   is not a prime number, the factors of the divisor
                #   are also divisors. For example, a number divisible
                #   by 81 is also divisible by 3, because 81 is 3*9.
                #   Thus, we start our division operations from smaller
                #   factors, potentially reducing the number of 
                #   operations by a large margin.
                #
                # 2. An odd number can never be divisible by an even
                #   number, as such a number will then be divisible
                #   by two (due to the distributive nature of
                #   multiplication). So we skip even numbers, halving
                #   the number of divisions required.
                #
                # 3a. Still keeping in mind the distributive nature of
                #   multiplication, we do not need to search every
                #   odd number until the candidate's half. We know that
                #   we don't have to get to half, because our odd number
                #   cannot be halved. Instead, we can stop searching at
                #   a third, excluding all factors also divisible by three.
                #   This is a safe threshold, as three is the smallest
                #   prime divisor capable of cleanly dividing odd numbers.
                #   Ending the search at a third reduces the number of
                #   operations by a third, which is a 1/6th improvement
                #   over the optimisations proposed in in [2].
                #
                # 3b. But what if the search space can be further reduced?
                #   This is actually possible. The first 35 prime numbers
                #   or so have been found to be safe thresholds. In this
                #   example, a threshold factor of 149 (the 35th prime)
                #   has been selected. This restricts our search range to
                #   1/149 of all odd numbers larger than our precalculated
                #   primes, as it is certain that a factor for a non-prime
                #   number will be found within that range. 
                #
                # TODO: Attempts with larger precalc lookup tables have
                #   either resulted in excessive memory usage and lookups
                #   due to significant increases in memory operations for
                #   prime numbers, or false negatives in prime number
                #   checking. Is there an even faster way to calculate
                #   primes?
                #
                # 4. The last precalculated prime is a safe number to
                #   start from, as any smaller odd number has already
                #   been tested against during the sieve stage
                #   above. This saves a little more operations per
                #   candidate :)
                #
                if(a%b == 0):
                    assume_prime = False
                    break

        if assume_prime is True:
            primes_found += 1

    return a
        # Return a if it is found to be the i'th prime.

def fasterer_prime(i):
    """Find the i'th prime number, using the fact that a number's
    largest factor is its square root.

    Unlike faster_prime(), the technique herein has unlimited range
    and a much more limited number of memory accesses.
    
    This function is assumed to be correct up to i=100000.
    The average time to find the 100000th prime was measured to be around
    12 seconds on the standard test machine, a low-end 2017-vintage
    PC with an AMD A4-7210 processor running Fedora 29.

    This function uses Python's math.sqrt()

    Arguments
    ---------
    i - integer: i'th prime number to be requested.

    Returns integer: i'th prime number
    Raises ValueError when i is negative or smaller than 1.
    Raises TypeError when i is not an `int`.

    Synopsis
    --------
    The process of finding the prime numbers is as follows:
    1. Skip all even numbers
    2. Keep the first few prime numbers that are too small to be correctly
        evaluated using the method employed in this function.
    3. For all suitable _odd_ positive integers, attempt to divide
        the number x by all odd numbers **from 3 to 1+sqrt(x)**, where
        sqrt() is the square root function.
    4. Any term x that is found not to be divisible in step 3 is a prime
        number.
    5. Repeat 3 and 4 until i prime numbers are found. Return the i'th
        prime number.
    
    This process is significantly faster than faster_prime for finding
    primes beyond the 20000th. It can find the 100000th prime in the
    order of 11 seconds on the standard test target.

    However, is is only about just as quick as faster_prime in finding
    primes up to the 10000th, and was found to be actually marginally
    slower in finding smaller primes from the 1000th to the 11000th.
    
    The standard test target was a low-end 2017-vintage x86 PC with an
    AMD A4-7210 processor, running Python 3.7 on Fedora 29. 

    The definition of prime number herein is the same as that in
    slow_prime() above.

    """
    if i < 1:
        raise ValueError("Argument must be a positive integer")
    if isinstance(i,int) is False:
        raise TypeError("Argument must be a positive integer")

    precalc_primes = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,
        67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149)
    primes_found = len(precalc_primes)
    if i < primes_found:
        return precalc_primes[i-1]

    primes_found = len(precalc_primes)
        # We are doing this to account for the first n'th primes
    a = precalc_primes[primes_found-1]
        # Start from the last precalculated prime

    while primes_found < i:
        assume_prime = True
        a += 2
            # Keep increasing a, as we check if it is a prime number.
            # Only deal with odd numbers, as all prime numbers are odd.
            # This dramatically reduces the number of divisions.

        for x in range(3, round(sqrt(a))+1, 2):
            # Check for divisibility with all odd numbers from 3
            # to the square root of a.
            if a%x == 0:
                assume_prime = False
                break

        if assume_prime is True:
            primes_found += 1

    return a
        # Return a if it is found to be the i'th prime.

