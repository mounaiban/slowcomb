"""
test_slowcomb_out — Slow Addressable Combinatorics Output Test Module
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
from slowcomb.tests import examples

class TestData:
    pref_r = 4
    seq = tuple([chr(65+i) for i in range(5)])
        # First few Capital Letters
        # The tests are currently reasonably fast up to a length of
        #  7 letters.

class SCCTestData:
    """
    Contains Test Data for CatCombination. The Combinator is
    checked to verify that it is able to reconstruct all possible
    sentences from a word combination table, similar to those
    seen in language instruction materials.

    The following combination table shall be used in all tests
    in this suite:

    CatCombination Test, 1st Ed, 2019 February (SCCT1)
    a.k.a. the Kerpal Test

    ========  ======  ====  ====
    1st Word  2nd     3rd   4th
    ========  ======  ====  ====
    He        kicked  my    dog
    She       punted        cat 
    You
    =======   ======  ====  ====

    max_r is defined as 4
    median_r is defined as 2
    min_r is defined as 1
    """

    c1 = ('He', 'She', 'You')
    c2 = ('kicked', 'punted')
    c3 = ('my',)
    c4 = ('dog','cat')
    seqs = [c1, c2, c3, c4]

class IterComparativeTest(unittest.TestCase):
    """Verifies the result of a sequence class against the
    contents of an iterator, when the sequence is accessed both
    as a sequence and as an iterator.
    """

    # PROTIP: All sequences are iterators. See: Iterator Types.
    # Built-in Types. Python Standard Library. Python Documentation.

    def verify_output_as_iter(self, cand, ref_iter):
        """Verify if contents are the same between a candidate
        sequence and a reference iterator, when both are accessed
        as iterators.
        """
        # NOTE: may cause excessive memory usage if the
        # test is incorrectly planned.
        cand_as_list = [d for d in cand]
        ref_as_list = [d for d in ref_iter]
        self.assertEqual(len(cand_as_list), len(ref_as_list),
            'both must have same length to have same contents')
        for i in range (len(cand_as_list)):
            with self.subTest(test='as_iter',i=i):
                self.assertEqual(cand_as_list[i], ref_as_list[i])

    def verify_output_as_seq(self, cand_seq, ref_iter):
        """Verify if contents are the same between a candidate
        sequence and a reference iterator, when the candidate
        is accessed as a sequence.
        """
        i = 0
        for d in ref_iter:
            # d is for Data
            with self.subTest(test='as_seq',ref_item=d, i=i):
                self.assertEqual(cand_seq[i], d)
            i+=1

    def verify_output(self, cand_seq, ref_iter):
        self.verify_output_as_iter(cand_seq, ref_iter)
        self.verify_output_as_seq(cand_seq, ref_iter)

class CatCombinationOutputTests(unittest.TestCase):
    """
    Verifies the output of the CatCombination combinatorial unit.

    This test case verifies results explicitly; it uses manually
    prepared, hard-coded data seen below as an indication of correct
    operation

    """
    seq = examples.src_colonel
        # See examples.py for exact content of this source 

    def setUp(self):
        self.comb = CatCombination(self.seq)
        self.comb_min_r = CatCombination(self.seq,1)
        self.comb_median_r = CatCombination(self.seq,2)
        self.comb_max_r = CatCombination(self.seq,3)

        # Expected Results
        self.expected_addr_min_r = ((0,),(0,),(0,))

        self.expected_data_min_r = (('I',),)
        self.expected_data_median_r =(
            ('I','need'),
            ('I','want'),
        )
        self.expected_data_max_r = (
            ('I','need','sugar'),
            ('I','need','spice'),
            ('I','need','scissors'),
            ('I','want','sugar'),
            ('I','want','spice'),
            ('I','want','scissors'),
        )

    def test_iter_max_r(self):
        # r=4, i.e. Full sentences only
        # Access as iterator
        i = 0
        for d in self.comb_max_r:
            with self.subTest(i=i):
                self.assertEqual(d, self.expected_data_max_r[i])
                i += 1

    def test_getitem_max_r(self):
        # r=4, i.e. Full sentences only
        # Access as sequence
        for i in range(len(self.comb_max_r) - 1):
            with self.subTest(i=i):
                self.assertEqual(self.comb_max_r[i],
                    self.expected_data_max_r[i])
    
    def test_getitem_median_r(self):
        # r=2, i.e. First two words only
        # Access as sequence
        for i in range(len(self.comb_median_r) - 1):
            with self.subTest(i=i):
                self.assertEqual(self.comb_median_r[i],
                    self.expected_data_median_r[i]
                )

    def test_iter_median_r(self):
        # r=2, i.e. first two words only
        # Access as iterator
        i = 0
        for d in self.comb_median_r:
            with self.subTest(i=i):
                self.assertEqual(d, self.expected_data_median_r[i])
                i += 1

    def test_iter_min_r(self):
        # r=1, i.e. First word only
        # Access as iterator
        i = 0
        for d in self.comb_min_r:
            with self.subTest(i=i):
                self.assertEqual(d, self.expected_data_min_r[i])
                i += 1

    def test_getitem_min_r(self):
        # r=1, i.e. First word only
        # Access as sequence
        for i in range(len(self.comb_min_r)):
            with self.subTest(i=i):
                self.assertEqual(self.comb_min_r[i], 
                    self.expected_data_min_r[i]) 

class CombinationOutputTests(IterComparativeTest):
    """
    Verify the output of the Combination class using
    itertools.combinations as the authoritative reference
    """

    def test_out_seq(self):
        for r in range(0, len(TestData.seq)):
            ref_iter = itertools.combinations(TestData.seq, r)
            cand_seq = Combination(TestData.seq, r=r)
            with self.subTest(r=r):
                self.verify_output(cand_seq, ref_iter)

class CombinationWithRepeatsOutputTests(IterComparativeTest):
    """
    Verify the output of the CombinationWithRepeats class using
    itertools.combinations_with_replacement as the authoritative
    reference
    """

    def test_out_seq(self):
        for r in range(0, len(TestData.seq)):
            ref_iter=itertools.combinations_with_replacement(TestData.seq, r)
            cand_seq=CombinationWithRepeats(TestData.seq, r=r)
            with self.subTest(r=r):
                self.verify_output(cand_seq, ref_iter)

class PermutationOutputTests(IterComparativeTest):
    """
    Verify the output of the Permutation class using
    itertools.permutations as the authoritative reference
    """
    
    def test_out_seq(self):
        for r in range(0, len(TestData.seq)):
            # Prepare reference test data
            ref_iter = itertools.permutations(TestData.seq, r)
            cand_seq= Permutation(TestData.seq, r=r)
            with self.subTest(r=r):
                self.verify_output(cand_seq, ref_iter)

class PermutationWithRepeatsOutputTests(unittest.TestCase):
    """
    Verify that PermutationWithRepeats is returning the correct
    output.
    """

    def test_out_seq(self):
        r = TestData.pref_r
        test_len = 10**r
        dec_digits = '0123456789'
        perm = PermutationWithRepeats(dec_digits,r)
            # This is functionally a fixed-length decimal number
            #  counter.
            # Calling perm[n] returns the number n with its
            #  digits as separate str's in a tuple
        for i in range(test_len):
            expected = ("{:0"+str(r)+"d}").format(i)
                # The test number i padded with leading zeroes
                #  until it is r digits long, converted to a
                #  string
            out_expected = tuple(expected)
            out = perm[i]
            self.assertEqual(out, out_expected)
            

