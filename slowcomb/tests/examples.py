
"""
slowcomb.tests.examples — Shared Specimens for Manual and Automated Tests
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


import itertools
from slowcomb.slowcomb import CatCombination, Combination, \
    CombinationWithRepeats, Permutation, PermutationWithRepeats
from slowcomb.slowseq import NumberSequence, CacheableSequence, \
    BlockCacheableSequence
from slowcomb.slowseq import AccumulateSequence, SNOBSequence, SumSequence
from slowcomb.tests import slowprime


# Loose Items
#
src_colonel = (('I',),('need', 'want'), ('sugar', 'spice', 'scissors'))
    # A sequence of sequences for use with the CatCombination
    # combinatorial unit


# Test Data Helper Functions
#
def get_latin_upper_alphas(n):
    """Get the first n uppercase letters of the Latin Alphabet
    (also called the Roman Alphabet) in a tuple.

    """
    if n<1 or n>26:
        raise ValueError('Latin alphabet test seqs are 1-26 letters')
    return tuple([chr(65+x) for x in range(n)])

def get_hindu_arabic_digits(n):
    """Get the first n uppercase letters of the Hindu-Arabic numerals
    (better known as the '0123456789') in a tuple.

      PROTIP: A one-digit sequence contains the digit zero ('0'),
      and not '1'.

    """
    if n<1 or n>10:
        raise ValueError('Hindu-Arabic numeral test seqs are 1-10 digits')
    return tuple([chr(0x30+x) for x in range(n)])

def get_fruits(n):
    """Get a tuple of fruit symbols (Emoji) from the Unicode 6.0
    character set.

    Note that the grocer's definition of fruits is used herein,
    genetics and taxonomics be damned. This means that the
    aubergine/brinjal/eggplant and tomato are excluded. Also, the 
    newer fruit Emoji are not included.

    Special thanks to the contributors at Emojipedia!

    """
    if n<1 or n>13:
        raise ValueError('The fruit test seq is 1-13 symbols long')
    return tuple([chr(0x1f347+x) for x in range(n)])


# Test Data Helper Classes
#
class OrderOfMagnitudeSequenceFactory:
    """Helper class to prepare standard test items for sequence
    output tests.
    """

    # Class Variables
    #
    func_n_ord_mag = lambda self,n: n * 10**n
        # Returns n raised (for positive n) or lowered 
        # (for negative n) by n orders of magnitude.
        # i.e. 0, 10, 200, 3000, 40000, 500000 ... , and
        #  -0.1, -0.02, -0.003, -0.0004 ...
        # A safe and sane limit of 12 is recommended.
        #
        # TODO: Why do I need to have a self argument when I define
        #  a lambda at class level, but not when it is inside a method?
    pos_ii_start = 5
        # All positive ii_start sequences start at internal index 5
    neg_ii_start = -10
        # All negative ii_start sequences start at internal index -10
    neg_ii_start_zero_x = -5
        # All zero-crossing negative ii_start sequences start at 
        # internal index -10
    test_len = 10
        # All test items are 10 terms long, including the zero'th item
        # where applicable
    
    def get_test_seq_pos_ii(self):
        return self._seq_class(self.func_n_ord_mag,
            ii_start=self.pos_ii_start, length=self.test_len)

    def get_test_seq_neg_ii(self):
        return self._seq_class(self.func_n_ord_mag,
            ii_start=self.neg_ii_start, length=self.test_len)

    def get_test_seq_neg_ii_zero_x(self):
        return self._seq_class(self.func_n_ord_mag,
            ii_start=neg_ii_start_zero_x, length=test_len)

    def get_test_seq_zero_ii(self):
        return self._seq_class(self.func_n_ord_mag,
            ii_start=0, length=self.test_len)

    def __init__(self, seq_class):
        if issubclass(seq_class, NumberSequence) is True:
            self._seq_class = seq_class


# Ready-made Number Sequences
#
seq_blk_cache = BlockCacheableSequence(slowprime.fasterer_prime, length=65536)
seq_blk_cache.enable_cache()
    # A Block Cacheable Sequence of the first 65,536 lazily-evaluated
    # prime numbers that caches all previously-requested numbers.
    # Only single lookups are cached. To cache some numbers, request
    # them as part of a slice like:
    #
    # seq_blk_cache[10000:10032]
    #
    # Preferably, request very high prime numbers (e.g. 10000th
    # onwards). Then, observe the time it takes for single
    # numbers within the slice to be returned, as opposed to
    # numbers outside the slice. 
    #
seq_dict_cache = CacheableSequence(slowprime.fasterer_prime, length=65536)
seq_dict_cache.enable_cache()
    # A Cacheable Sequence of the first 65,536 lazily-evaluated
    # prime numbers that individually caches previously-requested
    # numbers. Observe the time it takes for a high prime number
    # (e.g. the 10000th) to be returned when it is first requested,
    # and when it is requested again.
    #
seq_sum = SumSequence(lambda x:x**2, length=65536)
    # A Sum Sequence which includes the first 65,536 stages of
    # 'the sum of squares to x'.
seq_accu = AccumulateSequence(lambda x:x+1, lambda x,a:x*a, length=65536)
    # An Accumulate Sequence which includes the first 65,536
    # stages of 'the multiple of all numbers until x'. Almost 
    # equivalent to factorial(n+1), or (n+1)!, where
    # 0 ≤ n ≤ 65536.
seq_accu_2 = AccumulateSequence(lambda x:x, lambda x,a:x+(-a),
    length=4096)
    # A strange Accumulate Sequence which alternates between
    # adding the latest term to sum of all previous values, and
    # subtracting the value of all previous terms from the latest
    # term. The net effect is a sequence where every consecutive
    # natural number appears twice. Can you figure this one out?


# Ready-made Number Sequences Supporting index()
#
seq_snob = SNOBSequence(8,4)
    # A Same Number of Bits (SNOB) sequence which includes all
    # 8-bit binary numbers with four bits active. The numbers are
    # ordered from the largest to the smallest.
    # All outputs from the sequence are in decimal by default.
    # To see them in binary, try the "{:b}" format with print
    # or str():
    #
    # "{:b}".format(seq_snob[0])
    #


# Ready-made Combinatorial Units
#
cc = CatCombination(src_colonel, r=3)
    # Catenating Combination with a fixed r-size of three words.
cc_no_r = CatCombination(src_colonel)
    # Catenating Combination with no defined r-size.
    # Includes all combinations of length 1 to the longest 
    # possible length (i.e. 3, see src_colonel above).
comb = Combination(get_latin_upper_alphas(8), r=4)
    # Combination: including selections of four Latin alphabets
    # out of the first 8, (A, B, C, D, E, F, G, H).
comr = CombinationWithRepeats(get_latin_upper_alphas(4), r=4)
    # Repeats-Permitted Combination: including selections of
    # four (or less) Latin alphabets, out of the first 4.
    # Each alphabet may be selected more than once.
perm = Permutation(get_latin_upper_alphas(4), r=4)
    # Permutation: every possible arrangement of the first four
    # Latin alphabets, (A, B, C, D). This is an example of the
    # strictest definition of 'permutation'.
perm_part_no_r = Permutation(get_latin_upper_alphas(4))
    # Permutation with no defined r-size.
    # Includes every possible arrangement of any selection of
    # any number of the first four Latin alphabets.
perm_part = Permutation(get_latin_upper_alphas(8), r=4)
    # Permutation: every possible arrangement of a selection of
    # four Latin alphabets out of the first 8.
prmr = PermutationWithRepeats(get_hindu_arabic_digits(10), r=5)
    # Repeats-permitted Permutation: every possible arrangement
    # of a selection of five Hindu-Arabic digits out of the full
    # set (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), permitting repetitions
    # of digits.
    # This is effectively a counter from 0 to 99999, or the
    # readouts on a five-dial combination lock.
prmr_pokies = PermutationWithRepeats(get_fruits(13), r=7)
    # Repeats-permitted Permuation: every possible arrangement
    # of a selection of five fruits from a collection of thirteen,
    # with repetitions allowed.
    # This is effectively a readout of the payline of a slot
    # gambling machine.

