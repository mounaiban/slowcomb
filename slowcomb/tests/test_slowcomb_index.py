
"""
test_slowcomb_index — Slow Addressable Combinatorics Addressing Test Module
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


import itertools, unittest
from slowcomb.slowcomb import CatCombination, Combination, \
    CombinationWithRepeats, Permutation, PermutationWithRepeats

class TestData:
    pref_r = 5
    seq = tuple([chr(65+i) for i in range(5)])
        # First few Capital Letters
        # The tests are currently reasonably fast up to a length of
        #  7 letters.

class PermutationIndexTest(unittest.TestCase):
    """Verifies the result of slowcomb.Permutation.index(), the
    method which returns the external index of a term if it is
    a member of a Permutator sequence
    """
    cand_class = Permutation

    def setUp(self):
        self.cand_seq = self.cand_class(TestData.seq, TestData.pref_r)

    def test_index_no_i_no_j(self):
        """Verifies the results of using index() without a specified
        value of i (search start index) or j (search stop index)
        """
        for i in range(len(self.cand_seq)-1):
            out = self.cand_seq[i]
            with self.subTest(i=i, out=out):
                self.assertEqual(i, self.cand_seq.index(out))

    def test_index_no_i_no_j_no_r(self):
        """Verifies the results of using index() without a specified
        start, stop or fixed term length (r).

        """
        cand_seq_no_r = self.cand_class(TestData.seq)
        for i in range(len(self.cand_seq)-1):
            out = cand_seq_no_r[i]
            with self.subTest(i=i, out=out):
                self.assertEqual(i, cand_seq_no_r.index(out))

    def test_index_none_term(self):
        """Verifies that using None as a search term raises a ValueError
        """
        with self.assertRaises(ValueError):
            self.cand_seq.index(None)

    def test_index_excess_len_term(self):
        """Verifies that search terms that are too long raise a
        ValueError when r is set
        """
        with self.assertRaises(ValueError):
            term = TestData.seq*10
            self.cand_seq.index(term)
            
    def test_index_inadeq_len_term(self):
        """Verifies that search terms that are too short raise a
        ValueError when r is set
        """
        with self.assertRaises(ValueError):
            term = TestData.seq[0]
            self.cand_seq.index(term)
            
class PermutationWithRepeatsIndexTest(PermutationIndexTest):
    """Repeat Permutation Index tests with the
    PermutationsWithRepeats class
    """
    cand_class = PermutationWithRepeats

    def test_index_no_i_no_j_no_r(self):
        """Exempt PermutationWithRepeats class from the no-r test.
        This is because the repeats-permitted permutation requires
        a fixed term length r.

        """
        pass

class CatCombinationIndexTest(unittest.TestCase):
    """Verifies the result of slowcomb.CatCombination.index(), the
    method which returns the external index of a term if it is
    a member of a Permutator sequence
    """
    
    def test_index_no_i_no_j(self):
        src = (('I'),('need','want'),('scissors','sugar','spice'))
        cand_seq = CatCombination(src, r=len(src))

        for i in range(len(cand_seq)-1):
            out = cand_seq[i]
            with self.subTest(i=i, out=out):
                self.assertEqual(i, cand_seq.index(out))

