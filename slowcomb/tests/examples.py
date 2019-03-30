
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

