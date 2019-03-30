"""
test_slowcomb_index — Combinatorial Unit index() reverse-lookup tests
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

# Test Settings
#
TEST_MIN_N = 1
TEST_MAX_N = 5

class PermutationIndexTest(unittest.TestCase):
    """Verifies the result of slowcomb.Permutation.index(), by informal
    proofs, where r (the permutation size) is set.

    Glossary
    --------
    * combu: A combinatorial unit being tested.

    * i : The first index *from* which to start searching.

    * j : The last index *before* which to stop searching.

    * n : The size of the source sequence. 

    * r : The requested size of the combinatorial result. Optional for
        some combinatorial units, mandatory for others.

    """
    # Test Case Settings
    #
    combu_class = Permutation

    # Tests
    #
    def test_index_no_i_no_j(self):
        """Result of index() with no i and no j.

        Verification is done by requesting every item of the sequence,
        and then checking the index used in requesting the item with the
        result of index().

        This verification is repeated for different values of n and r.
        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(n+1):
                src = examples.get_latin_upper_alphas(n)
                combu = self.combu_class(src, r)
                for i in range(len(combu)):
                    out = combu[i]
                    with self.subTest(n=n, r=r, i=i, out=out):
                        self.assertEqual(i, combu.index(out))

    def test_index_empty_term(self):
        """ValueError when an empty sequence is used as search term
        
        Verifies that using the empty sequence as a search term on a valid
        combinatorial unit raises a ValueError.

        This verification is repeated for different values of n and r.
        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(1,n+1):
                # Skip r=0, because CUs with a zero r-value are
                # not valid and will not raise ValueError when
                # an attempt is made to find the index the empty
                # sequence.
                src = examples.get_latin_upper_alphas(n)
                combu = self.combu_class(src, r)
                with self.subTest(n=n, r=r):
                    with self.assertRaises(ValueError):
                        combu.index(())

    def test_index_empty_term(self):
        """ValueError when an the default value is used as search term
        
        Verifies that using the default value as a search term on a valid
        combinatorial unit raises a ValueError.

        This verification is repeated for different values of n and r.
        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(1,n+1):
                # Skip r=0, because CUs with a zero r-value are
                # not valid and will not raise ValueError when
                # an attempt is made to find the index of the
                # default value
                src = examples.get_latin_upper_alphas(n)
                combu = self.combu_class(src, r)
                with self.subTest(n=n, r=r):
                    with self.assertRaises(ValueError):
                        combu.index(combu._default)


    def test_index_none_term(self):
        """ValueError when None is used as a search term.

        Verifies that using None as a search term raises a TypeError.

        This verification is repeated for different values of n and r.

        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(n+1):
                src = examples.get_latin_upper_alphas(n)
                combu = self.combu_class(src, r)
                with self.subTest(n=n, r=r):
                    with self.assertRaises(TypeError):
                        combu.index(None)

    def test_index_too_long_term(self):
        """ValueError on excessively long search terms
        
        Verifies that using search terms that are longer than a
        combinatorial unit's r-value (when set) raises a ValueError.
        Setting an r-value should cause the CU to produce results of
        length r only.

        This verification is repeated for different values of n and r.

        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            for r in range(n+1):
                src = examples.get_latin_upper_alphas(n)
                combu = self.combu_class(src, r)
                with self.subTest(n=n, r=r):
                    with self.assertRaises(ValueError):
                        term = src*10
                        combu.index(term)
            
    def test_index_too_short_term(self):
        """ValueError on excessively short search terms

        Verifies that using search terms that are shorter than a
        combinatorial unit's r-value (when set) raises a ValueError.
        Setting an r-value should cause the CU to produce results of
        length r only.

        This verification is repeated for different values of n and r.

        """

        # NOTE: For this test, the minimum values for r and n have been 
        # been set to 2, as r <= n and when r=1 the only shorter search
        # term would be an empty sequence. 
        # 
        # Testing for empty search terms is handled by 
        # test_index_empty_term()
        #
        for n in range(2, TEST_MAX_N+1):
            for r in range(2, n+1):
                src = examples.get_latin_upper_alphas(n)
                combu = self.combu_class(src, r)
                with self.subTest(n=n, r=r):
                    with self.assertRaises(ValueError):
                        term = src[0]
                        combu.index(term)
 

class PermutationNoRIndexTest(unittest.TestCase):
    """Verifies the result of slowcomb.Permutation.index(), by informal
    proofs, where r (permutation size) is not set.

    Glossary
    --------
    Please see the Glossary under PermutationIndexTest above

    """
    # Test Case Settings
    #
    combu_class = Permutation

    # Tests
    #
    def test_index_no_i_no_j_no_r(self):
        """Result of index() with no i, no j and no r.

        Verifies the result of reverse lookups of valid combinatorial
        results.

        Verification is done by requesting every item of the sequence,
        and then checking the index used in requesting the item with the
        result of index().

        This verification is repeated for different values of n.
        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            src = examples.get_latin_upper_alphas(n)
            combu = self.combu_class(src)
            for i in range(len(combu)-1):
                out = combu[i]
                with self.subTest(n=n, i=i, out=out):
                    self.assertEqual(i, combu.index(out))

    def test_index_none_term_no_r(self):
        """ValueError when None is used as a search term.

        Verifies that using None as a search term raises a ValueError.

        This verification is repeated for different values of n.

        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            src = examples.get_latin_upper_alphas(n)
            combu = self.combu_class(src)
            with self.subTest(n=n):
                with self.assertRaises(TypeError):
                    combu.index(None)

    def test_index_too_long_term_no_r(self):
        """ValueError on excessively long search terms
        
        Verifies that using search terms that are longer than a
        combinatorial unit's r-value (when set) raises a ValueError.

        This verification is repeated for different values of n.

        """
        for n in range(TEST_MIN_N, TEST_MAX_N+1):
            src = examples.get_latin_upper_alphas(n)
            combu = self.combu_class(src)
            with self.subTest(n=n):
                with self.assertRaises(ValueError):
                    term = src*10
                    combu.index(term)

class PermutationWithRepeatsIndexTest(PermutationIndexTest):
    """Repeat Permutation Index Tests with slowcomb.PermutationsWithRepeats.index()
    """
    # Test Case Settings
    combu_class = PermutationWithRepeats

class CombinationIndexTest(PermutationIndexTest):
    """
    Repeat Permutation Index Tests with the slowcomb.Combination.index()

    """
    # Test Case Settings
    combu_class = Combination

class CombinationWithRepeatsIndexTest(PermutationIndexTest):
    """
    Repeat Permutation Index tests with the CombinationWithRepeats class
    """
    # Test Case Settings
    combu_class = CombinationWithRepeats

class CatCombinationIndexTest(unittest.TestCase):
    """Verifies the result of slowcomb.CatCombination.index(), by 
    informal proofs.
    """
    
    def test_index_no_i_no_j(self):
        """Result of index() with no i and no j
        
        Verifies the result of reverse lookups of valid combinatorial
        results.

        Verification is done by requesting every possible result using all
        valid indices, then comparing the the indices returned by index()
        with the original index used in the original request.

        This test is repeated for all accepted values of r
        
        """
        src = examples.src_colonel
        combu = CatCombination(src, r=len(src))
        for i in range(len(combu)-1):
            out = combu[i]
            with self.subTest(i=i, out=out):
                self.assertEqual(i, combu.index(out))

    def test_index_no_i_no_j_no_r(self):
        """Result of index() with no i, no j and no r.
        
        Verifies the result of reverse lookups of valid combinatorial
        results on the CatCombination class when an r-value is not set.

        Verification is done by requesting every possible result using all
        valid indices, then comparing the the indices returned by index()
        with the original index used in the original request.
        
        """
        src = examples.src_colonel
        combu = CatCombination(src)
        for i in range(len(combu)-1):
            out = combu[i]
            with self.subTest(i=i, out=out):
                self.assertEqual(i, combu.index(out))


