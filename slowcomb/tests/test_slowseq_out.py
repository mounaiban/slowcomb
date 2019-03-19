"""
test_slowseq_out — Output Tests for supporting sequence classes
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

import unittest
from slowcomb.slowseq import *

class TestNumberSequenceFactory:
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

# Slice Indexing Output Tests
#
class NumberSequenceSliceOutputTests(unittest.TestCase):

    def setUp(self):
        self.item_factory=TestNumberSequenceFactory(NumberSequence)
        self.test_item_pos_ii=self.item_factory.get_test_seq_pos_ii()
        self.test_item_neg_ii=self.item_factory.get_test_seq_neg_ii()
        self.test_item_zero_ii=self.item_factory.get_test_seq_zero_ii()
        # Please see the TestNumberSequenceFactory for test
        # standards used throughout these tests.
        # NumberSequences return tuples for multiple item lookups.

    def test_getitem_s_pos_start_pos_stop_pos_step_pos_ii_start(self):
        out = self.test_item_pos_ii[1:6:2]
        expected = (6_000_000, 800_000_000, 100_000_000_000)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_pos_stop_pos_step_neg_ii_start(self):
        out = self.test_item_neg_ii[4:9:2]
        expected = (-0.000006, -0.0004, -0.02)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_pos_stop_pos_step_zero_ii_start(self):
        out = self.test_item_zero_ii[1:6:2]
        expected = (10,3000,500000)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_pos_stop_neg_step_pos_ii_start(self):
        out = self.test_item_pos_ii[5:0:-2]
        expected = (100_000_000_000, 800_000_000, 6_000_000)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_pos_stop_neg_step_neg_ii_start(self):
        out = self.test_item_neg_ii[9:4:-2]
        expected = (-0.1,-0.003,-0.00005)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_pos_stop_neg_step_zero_ii_start(self):
        out = self.test_item_zero_ii[5:0:-2]
        expected = (500_000, 3000, 10)
        self.assertEqual(out,expected)
        
    def test_getitem_s_pos_start_neg_stop_pos_step_pos_ii_start(self):
        out = self.test_item_pos_ii[1:-4:2]
        expected=(6_000_000, 800_000_000, 100_000_000_000)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_neg_stop_pos_step_neg_ii_start(self):
        out = self.test_item_neg_ii[4:-1:2]
        expected = (-0.000006, -0.0004, -0.02)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_neg_stop_pos_step_zero_ii_start(self):
        out = self.test_item_zero_ii[1:-4:2]
        expected = (10,3000,500_000)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_neg_stop_neg_step_pos_ii_start(self):
        out = self.test_item_pos_ii[6:-9:-2]
        expected=(1_100_000_000_000, 9_000_000_000, 70_000_000)
        self.assertEqual(out,expected)
    
    def test_getitem_s_pos_start_neg_stop_neg_step_neg_ii_start(self):
        out = self.test_item_neg_ii[9:-6:-2]
        expected = (-0.1, -0.003, -0.00005)
        self.assertEqual(out,expected)

    def test_getitem_s_pos_start_neg_stop_neg_step_zero_ii_start(self):
        out = self.test_item_zero_ii[6:-9:-2]
        expected = (6000000,40000,200)
        self.assertEqual(out,expected)

class CacheableSequenceSOTests(NumberSequenceSliceOutputTests):

    # Class Variables
    #
    TestClass=CacheableSequence

    def setUp(self):
        self.item_factory=TestNumberSequenceFactory(self.TestClass)
        self.test_item_pos_ii=self.item_factory.get_test_seq_pos_ii()
        self.test_item_pos_ii.enable_cache()
        self.test_item_neg_ii=self.item_factory.get_test_seq_neg_ii()
        self.test_item_neg_ii.enable_cache()
        self.test_item_zero_ii=self.item_factory.get_test_seq_zero_ii()
        self.test_item_zero_ii.enable_cache()
        # The tests will be performed with the cache on to ensure that
        # the cache does not affect the results

class BlockCacheableSequenceSOTests(CacheableSequenceSOTests):

    # Class Variables
    #
    TestClass=BlockCacheableSequence

    def setUp(self):
        self.item_factory=TestNumberSequenceFactory(self.TestClass)
        seq_len = TestNumberSequenceFactory.test_len
            # Shortcut: the length of the sequences is equal to the
            # value defined by TestNumberSequenceFactory.test_len
        self.test_item_pos_ii=self.item_factory.get_test_seq_pos_ii()
        self.test_item_pos_ii.enable_cache()
        self.test_item_pos_ii[0:seq_len:2]
        self.test_item_neg_ii=self.item_factory.get_test_seq_neg_ii()
        self.test_item_neg_ii.enable_cache()
        self.test_item_neg_ii[0:seq_len:2]
        self.test_item_zero_ii=self.item_factory.get_test_seq_zero_ii()
        self.test_item_zero_ii.enable_cache()
        self.test_item_zero_ii[0:seq_len:2]
        # The tests will be performed with the cache on and primed to
        # check that correct results are returned

