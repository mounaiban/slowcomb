"""
Combinatiorial Unit Output Test Module

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
from slowcomb.slowcomb import CatProduct, Combination, \
    CombinationWithRepeats, Permutation, PermutationWithRepeats
from slowcomb.tests import examples

# Test Settings
#
TEST_MIN_N = 1
TEST_MAX_N = 5

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

class CatProductOutputTests(unittest.TestCase):
    """
    Verifies the output of the CatProduct combinatorial unit,
    using itertools.product as the authoritative reference
    """
    seq = examples.src_colonel
        # See examples.py for exact content of this source 

    def setUp(self):
        self.comb_min_r = CatProduct(self.seq,1)
        self.comb_median_r = CatProduct(self.seq,2)
        self.comb_max_r = CatProduct(self.seq,3)

        # Expected Results
        self.ref_iter_compre = [t for t in itertools.product(*self.seq)]
        self.ref_iter_compre_median_r = [
            t for t in itertools.product(*self.seq[:2])
        ]
        self.ref_iter_compre_min_r= [
            t for t in itertools.product(*self.seq[:1])
        ]

    def test_iter_max_r(self):
        # r=4, i.e. Full sentences only
        # Access as iterator
        i = 0
        for d in self.comb_max_r:
            with self.subTest(i=i):
                self.assertEqual(d, self.ref_iter_compre[i])
                i += 1

    def test_getitem_max_r(self):
        # r=4, i.e. Full sentences only
        # Access as sequence
        for i in range(len(self.comb_max_r) - 1):
            with self.subTest(i=i):
                self.assertEqual(self.comb_max_r[i], self.ref_iter_compre[i])
    
    def test_getitem_median_r(self):
        # r=2, i.e. First two words only
        # Access as sequence
        for i in range(len(self.comb_median_r) - 1):
            with self.subTest(i=i):
                self.assertEqual(self.comb_median_r[i],
                    self.ref_iter_compre_median_r[i]
                )

    def test_iter_median_r(self):
        # r=2, i.e. first two words only
        # Access as iterator
        i = 0
        for d in self.comb_median_r:
            with self.subTest(i=i):
                self.assertEqual(d, self.ref_iter_compre_median_r[i])
                i += 1

    def test_iter_min_r(self):
        # r=1, i.e. First word only
        # Access as iterator
        i = 0
        for d in self.comb_min_r:
            with self.subTest(i=i):
                self.assertEqual(d, self.ref_iter_compre_min_r[i])
                i += 1

    def test_getitem_min_r(self):
        # r=1, i.e. First word only
        # Access as sequence
        for i in range(len(self.comb_min_r)):
            with self.subTest(i=i):
                self.assertEqual(self.comb_min_r[i], 
                    self.ref_iter_compre_min_r[i])

class CombinationOutputTests(IterComparativeTest):
    """
    Verify the output of the Combination class using
    itertools.combinations as the authoritative reference
    """

    def test_out_seq(self):
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(0, n+1):
                seq = examples.get_latin_upper_alphas(n)
                ref_iter = itertools.combinations(seq, r)
                cand_seq = Combination(seq, r=r)
                with self.subTest(r=r):
                    self.verify_output(cand_seq, ref_iter)

class CombinationWithRepeatsOutputTests(IterComparativeTest):
    """
    Verify the output of the CombinationWithRepeats class using
    itertools.combinations_with_replacement as the authoritative
    reference
    """

    def test_out_seq(self):
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(0, n+1):
                seq = examples.get_latin_upper_alphas(n)
                ref_iter=itertools.combinations_with_replacement(seq, r)
                cand_seq=CombinationWithRepeats(seq, r=r)
                with self.subTest(r=r):
                    self.verify_output(cand_seq, ref_iter)

class PermutationOutputTests(IterComparativeTest):
    """
    Verify the output of the Permutation class using
    itertools.permutations as the authoritative reference
    """
    
    def test_out_seq(self):
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(0, n+1):
                # Prepare reference test data
                seq = examples.get_latin_upper_alphas(n)
                ref_iter = itertools.permutations(seq, r)
                cand_seq= Permutation(seq, r=r)
                with self.subTest(r=r):
                    self.verify_output(cand_seq, ref_iter)

class PermutationWithRepeatsOutputTests(unittest.TestCase):
    """
    Verify that PermutationWithRepeats is returning the correct
    output.
    """

    def test_out_seq(self):
        for r in range(TEST_MIN_N, TEST_MAX_N+1):
            dec_digits = examples.get_hindu_arabic_digits(10)
            perm = PermutationWithRepeats(dec_digits,r)
                # This is functionally a fixed-length decimal number
                #  counter.
                # Calling perm[n] returns the number n with its
                #  digits as separate str's in a tuple
            times = (10**r) - 1
            for i in range(times+1):
                # The test number i padded with leading zeroes
                #  until it is r digits long, converted to a
                #  string
                expected = ("{:0"+str(r)+"d}").format(i)
                out_expected = tuple(expected)
                out = perm[i]
                self.assertEqual(out, out_expected)
                

