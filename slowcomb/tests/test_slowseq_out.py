"""
Output Tests for supporting sequence classes

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
from slowcomb.tests.examples import OrderOfMagnitudeSequenceFactory
from slowcomb.slowseq import *

# Slice Indexing Output Tests
#
class NumberSequenceSliceOutputTests(unittest.TestCase):
    def setUp(self):
        self.item_factory=OrderOfMagnitudeSequenceFactory(
            NumberSequence)
        self.test_item_pos_ii=self.item_factory.get_test_seq_pos_ii()
        self.test_item_neg_ii=self.item_factory.get_test_seq_neg_ii()
        self.test_item_zero_ii=self.item_factory.get_test_seq_zero_ii()
        # Please see the OrderOfMagnitudeSequenceFactory for test
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
        self.item_factory=OrderOfMagnitudeSequenceFactory(
            self.TestClass)
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
        self.item_factory=OrderOfMagnitudeSequenceFactory(
            self.TestClass)
        seq_len = OrderOfMagnitudeSequenceFactory.test_len
            # Shortcut: the length of the sequences is equal to the
            # value defined by OrderOfMagnitudeSequenceFactory.test_len
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

    def test_getitem_i_pos_cache_border_repeat_zero_ii_start(self):
        out = self.test_item_zero_ii[3]
        expected = 3000
        self.assertEqual(out, expected)

    def test_getitem_i_pos_cache_border_repeat_neg_ii_start(self):
        out = self.test_item_neg_ii[-2]
        expected = -0.02
        self.assertEqual(out, expected)

    def test_getitem_i_neg_cache_step_pos_i_neg_ii_start(self):
        seq_len = OrderOfMagnitudeSequenceFactory.test_len
        test_item_neg_cs_zero_ii=self.item_factory.get_test_seq_zero_ii()
        test_item_neg_cs_zero_ii[seq_len-1:0:-2]
        out_id = id(test_item_neg_cs_zero_ii[1])
        cache_item_id = id(test_item_neg_cs_zero_ii._cache[-1])
        self.assertEqual(out_id, cache_item_id)
        

