"""
test_slowprime — Slow prime number finder self-test module
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

# NOTE: I personally feel that the practice of using lowercase-initial
#   camelCaps names in unittest members is somewhat un-Pythonic.
#   One other such built-in library that does this is plistlib. -Moses
#
import unittest, timeit
from slowcomb.tests.slowprime import faster_prime, fasterer_prime, slow_prime


# Classes
#
class SlowPrimeLimitsTests(unittest.TestCase):
    """
    Verify that Slow Primes is rejecting non-integers and integers
    smaller than 1 for i.
    """
    func = lambda self,x:slow_prime(x)

    def test_float(self):
        with self.assertRaises(TypeError, msg='Reject non-integers'):
            self.func(3.141592653589793)

    def test_neg_int(self):
        with self.assertRaises(ValueError, msg='Reject integers < 1'):
            self.func(-1)

    def test_zero_int(self):
        with self.assertRaises(ValueError, msg='Reject integers < 1'):
            self.func(0)

class FasterPrimeOutputTests(unittest.TestCase):
    """
    Verify that Faster Primes is returning genuine prime numbers.
    OEIS A000040 (four zeroes and a forty) is used as a reference
    for this test, and the numbers are sourced from Sloane, N. J. A.
    'Table of n, prime(n) for n = 1..100000'.
    """

    func = lambda self,x:faster_prime(x)

    def test_i_100(self):
        self.assertEqual(self.func(100),541)

    def test_i_500(self):
        self.assertEqual(self.func(500),3571)
    
    def test_i_1000(self):
        self.assertEqual(self.func(1000),7919)

    @unittest.skip('Slow test skipped, edit test_slowprime to run')
    def test_i_2000(self):
        # This took ~21s on an AMD A4-7210 in Fedora 29
        self.assertEqual(self.func(2000),17389)

    @unittest.skip('Slow test skipped, edit test_slowprime to run')
    def test_i_5000(self):
        self.assertEqual(self.func(5000),48611)
    
    @unittest.skip('Slow test skipped, edit test_slowprime to run')
    def test_i_16384(self):
        self.assertEqual(self.func(16384),180503)

    @unittest.skip('Slow test skipped, edit test_slowprime to run')
    def test_i_32767(self):
        self.assertEqual(self.func(32767),386083)
        
    @unittest.skip('Slow test skipped, edit test_slowprime to run')
    def test_i_65536(self):
        self.assertEqual(self.func(65536),821641)

    @unittest.skip('Slow test skipped, edit test_slowprime to run')
    def test_i_100k(self):
        self.assertEqual(self.func(100_000),1299709)

class FasterPrimeSyncTests(unittest.TestCase):
    """
    Verify that the faster_prime alternative to slow_prime()
    is returning the same results, using the drift check method.

    The method used in this test compares very deep primes 
    (i.e. 65536'th prime or deeper) in order to identify
    discrepencies caused by false positives or negatives due to
    algorithmic oversights in alternative prime number finders. 

    """
    func_alt_prime = lambda self,i:faster_prime(i)

    @unittest.skip('Slow test skipped, edit test_slowprime to run')
    def test_func_output_sync(self):
        # This is a very slow test, allow to run for a few hours.
        i = 2**15
        self.assertEqual(self.func_alt_prime(i), slow_prime(i),
                'slow_prime alternative must return exact results')

class FasterPrimeLimitsTests(SlowPrimeLimitsTests):
    """Repeat limits tests for the Not-Much-Faster Primes Finder,
    faster_prime()
    """
    func = lambda self,x:faster_prime(x)

class FastererPrimeLimitsTests(SlowPrimeLimitsTests):
    """Repeat limits tests for the Actually Faster Primes Finder,
    fasterer_prime()
    """
    func = lambda self,x:fasterer_prime(x)

class FastererPrimeOutputTests(FasterPrimeOutputTests):
    """Repeat output tests for the Actually Faster Primes Finder,
    faster_prime()
    """
    func = lambda self,x:fasterer_prime(x)

@unittest.skip('Slow test suite skipped, edit test_slowprime to run')
class SlowPrimeOutputTests(FasterPrimeOutputTests):
    """Repeat output tests for Slow Primes Finder, slow_prime()"""
    func = lambda self,x:faster_prime(x)
    # SlowPrimeOutputTests were made to be a derivative test of
    # the Faster Prime Tests to make this test case easier to skip

# Functions
#
def test_faster_primes(i):
    # Preliminary test for faster prime number finder functions
    # Find the i'th prime number

    print("Faster Prime vs Fasterer Prime Number Finders")
    print("First value is authoritative")
    stmt_run = "print( '{0}:', {0}({1}) )"
    stmt_setup = "from tests.slowprime import {0}"
        # I hope these format templates were easy enough
        # to understand
    r_faster=timeit.timeit(stmt_run.format("faster_prime",i),
        setup=stmt_setup.format("faster_prime"),
        number=1
    )
    r_fasterer=timeit.timeit(stmt_run.format("fasterer_prime",i),
        setup=stmt_setup.format("fasterer_prime"),
        number=1
    )
    print("{0}s vs {1}s".format(r_faster, r_fasterer))


if __name__ == 'main':
    unittest.main()

