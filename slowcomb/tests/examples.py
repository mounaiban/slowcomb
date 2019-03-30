
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
from slowcomb.slowseq import NumberSequence


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

