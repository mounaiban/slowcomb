"""
Unit Tests for supporting sequence classes

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

class TestData:
    func_dummy = lambda x:x

# Attributes: Defaults 
#
class NumberSequenceDefaultAttributeTests(unittest.TestCase):
    """Verify the attributes of an instance of the NumberSequence
    class when the bare minimum arguments are given.
    """

    def setUp(self):
        self.TestSeqClass=NumberSequence
    
    def test_defaults(self):
        """Verifies default settings of a NumberSequence class"""
        seq = self.TestSeqClass(TestData.func_dummy,length=0)
        self.assertEqual(seq._ii_start, 0, 'ii is zero by default')
        self.assertEqual(seq._i, 0, 'iter index is zero by default')
        self.assertEqual(
            seq._func,
            TestData.func_dummy,
            'function must be assigned'
        )

class CacheableSequenceDefAttrTests(NumberSequenceDefaultAttributeTests):
    def setUp(self):
        self.TestSeqClass=CacheableSequence

class BlockCacheableSequenceDefAttrTests(NumberSequenceDefaultAttributeTests):
    def setUp(self):
        self.TestSeqClass=BlockCacheableSequence


# Attributes: Length
#
class NumberSequenceLengthAttributeTests(unittest.TestCase):
    """Verify that the length of an instance of any NumberSequence
    class is being correctly reported
    """
    
    def setUp(self):
        self.TestSeqClass=NumberSequence

    def test_a_len_pos_ii_start(self):
        """ Verifies the results of using len() with a NumberSequence
        class when the internal index start is a positive value
        """
        length = 12
        start = 6
        seq = self.TestSeqClass(
            TestData.func_dummy,
            length=length,
            ii_start=start
        )
        self.assertEqual(len(seq), length, 'len() must be as requested')

    def test_a_len_neg_ii_start(self):
        """ Verifies the results of using len() with a NumberSequence
        class when the internal index start is a negative value
        """
        length = 12
        start = -12
        seq = self.TestSeqClass(
            TestData.func_dummy,
            length=length,
            ii_start=start
        )
        self.assertEqual(len(seq), length, 'len() must be as requested')

    def test_a_len_neg_zero_x_ii_start(self):
        """ Verifies the results of using len() with a NumberSequence
        class when the internal index start is a negative value, but
        the last index is a positive value
        """
        length = 12
        start = -6
        seq = self.TestSeqClass(
            TestData.func_dummy,
            length=length,
            ii_start=start
        )
        self.assertEqual(len(seq), length, 'len() must be as requested')

    def test_a_len_zero_ii_start(self):
        """
        Verifies the results of using len() on a NumberSequence class
        when the internal index starts at zero
        """
        length = 12
        seq = self.TestSeqClass(TestData.func_dummy,length=length)
        self.assertEqual(len(seq), length, 'len() must be as requested')

class CacheableSequenceLenAttrTests(NumberSequenceLengthAttributeTests):
    """
    Repeat Length Attribute tests with the CacheableSequence
    """
    def setUp(self):
        self.TestSeqClass=CacheableSequence

class BlockCacheableSequenceLenAttrTests(NumberSequenceLengthAttributeTests):
    """
    Repeat Length Attribute tests with the BlockCacheableSequence
    """
    def setUp(self):
        self.TestSeqClass=BlockCacheableSequence


# Index Resolution Tests
#
class NumberSequenceIndexResolutionTests(unittest.TestCase):
    
    def setUp(self):
        self.TestSeqClass=NumberSequence

    def test_resolve_i_pos_i_pos_ii_start(self):
        """
        Verifies the results of _resolve_i() with a positive external
        index with a positive internal index start offset
        """
        start = 5 
        length = 12
        seq = self.TestSeqClass(
            TestData.func_dummy,
            ii_start=start,
            length=length
        )
        for i in range(1,length):
            with self.subTest(i=i):
                self.assertEqual(
                    seq._resolve_i(i),
                    i + start,
                    'index offset must be applied'
                )

    def test_resolve_i_pos_i_neg_ii_start(self):
        """
        Verifies the results of _resolve_i() with a positive input value
        and a negative internal index start offset
        """
        start = -12
        length = 12
        seq = self.TestSeqClass(
            TestData.func_dummy,
            ii_start=start,
            length=length
        )
        for i in range(1,length):
            with self.subTest(i=i):
                self.assertEqual(seq._resolve_i(i), i+start,
                'neg index offset must be applied')

    def test_resolve_i_pos_i_zero_ii_start(self):
        """
        Verifies the results of _resolve_i() with no internal index
        redirection
        """
        length = 12
        seq = self.TestSeqClass(TestData.func_dummy,length=length)
        for i in range(1,length):
            with self.subTest(i=i):
                self.assertEqual(seq._resolve_i(i), i, 'index must match')
    
    def test_resolve_i_neg_i_pos_ii_start(self):
        """
        Verifies the results of _resolve_i() with a negative input value
        with a positive internal index start offset
        """
        start = 5
        length = 8 
        seq = self.TestSeqClass(
            TestData.func_dummy,
            ii_start=start,
            length=length
        )
        self.assertEqual(seq._resolve_i(-8), 5, 'last neg index -> start')
        self.assertEqual(seq._resolve_i(-1), 12, 'first neg index -> end')
        self.assertEqual(seq._resolve_i(-4), 9, 'mid neg index -> middle')

    def test_resolve_i_neg_i_neg_ii_start(self):
        """
        Verifies the results of _resolve_i() with a negative input value
        and a negative internal index start offset
        """
        start = -12
        length = 12
        seq = self.TestSeqClass(
            TestData.func_dummy,
            ii_start=start,
            length=length
        )
        self.assertEqual(seq._resolve_i(-12), -12, 'last neg index -> start')
        self.assertEqual(seq._resolve_i(-1), -1, 'first neg index -> end')
        self.assertEqual(seq._resolve_i(-6), -6, 'mid neg index -> middle')

    def test_resolve_neg_i_zero_ii_start(self):
        """
        Verifies the results of _resolve_i() with a negative input value
        without internal index redirection
        """
        length = 5 
        seq = self.TestSeqClass(TestData.func_dummy,length=length)
        self.assertEqual(seq._resolve_i(-5), 0, 'last neg index -> 0')
        self.assertEqual(seq._resolve_i(-1), 4, 'first neg index -> end')
        self.assertEqual(seq._resolve_i(-3), 2, 'mid neg index -> middle')

    def test_zero_i_pos_ii_start(self):
        """
        Verifies the results of _resolve_i() with the zero external
        index a positive internal index start offset
        """
        length = 5 
        start = 5
        seq = self.TestSeqClass(TestData.func_dummy,length=length,
            ii_start=start)
        self.assertEqual(seq._resolve_i(0), start, 'first index -> start')

    def test_zero_i_neg_ii_start(self):
        """
        Verifies the results of _resolve_i() with the zero external
        index a negative internal index start offset
        """
        length = 5 
        start = -10
        seq = self.TestSeqClass(TestData.func_dummy,length=length,
            ii_start=start)
        self.assertEqual(seq._resolve_i(0), start, 'first index -> start')

    def test_zero_i_zero_ii_start(self):
        """
        Verifies the results of _resolve_i() with the zero external
        index a negative internal index start offset
        """
        # This is the most basic kind of Sequence :)
        length = 5 
        seq = self.TestSeqClass(TestData.func_dummy,length=length)
        self.assertEqual(seq._resolve_i(0), 0, 'first index -> 0')

    def test_resolve_i_pos_i_neg_ii_start_zero_cross(self):
        """
        Verifies the results of _resolve_i() with a positive input value
        and a negative internal index start offset, where the first
        internal index in range is negative and the last is positive.
        """
        start = -6
        length = 12
        seq = self.TestSeqClass(
            TestData.func_dummy,
            ii_start=start,
            length=length
        )
        self.assertEqual(seq._resolve_i(0),-6, 'zero index -> start')
        self.assertEqual(seq._resolve_i(11),5, 'last index -> end')
        self.assertEqual(seq._resolve_i(6),0, 'mid index -> middle')

    def test_resolve_i_neg_i_neg_ii_start_zero_cross(self):
        """
        Verifies the results of _resolve_i() with a negative input value
        and a negative internal start offset, where the first internal
        index in range is negative and the last is positive
        """
        start = -6
        length = 12
        seq = self.TestSeqClass(TestData.func_dummy,
            ii_start=start, length=length)
        self.assertEqual(seq._resolve_i(-1),5, 'zero index -> start')
        self.assertEqual(seq._resolve_i(-12),-6, 'last index -> end')
        self.assertEqual(seq._resolve_i(-6),0, 'mid index -> middle')

    def test_resolve_i_zero_i_neg_ii_start_zero_cross(self):
        """
        Verifies the results of _resolve_i() with a zero external index
        and a negative internal start offset, where the first internal
        index in range is negative and the last is positive
        """
        start = -6
        length = 12
        seq = self.TestSeqClass(TestData.func_dummy,
            ii_start=start, length=length)
        self.assertEqual(seq._resolve_i(0),start, 'zero index -> start')

class CacheableSequenceIResTests(NumberSequenceIndexResolutionTests):
    """
    Repeat the Integer Index Resolution Tests on the CacheableSeqeunce
    """
    def setUp(self):
        self.TestSeqClass=CacheableSequence

class BlockCacheableSequenceIResTests(NumberSequenceIndexResolutionTests):
    """
    Repeat the Integer Resolution Tests on the BlockCacheableSequence
    """
    def setUp(self):
        self.TestSeqClass=BlockCacheableSequence


class BoundsTests(unittest.TestCase):

    def test_check_i_oob(self):
        """
        Verifies that an IndexError exception will be raised when
        an attempt is made to access an index past the end of the
        sequence
        """
        size = 8
        seq = NumberSequence(TestData.func_dummy,length=size)
        with self.assertRaises(IndexError):
            seq._check_i(size)

    def test_check_neg_i_oob(self):
        """
        Verifies that an IndexError exception is raised when an
        attempt is made to access an index past the beginning of
        the sequence using a negative external index
        """
        size = 8
        seq = NumberSequence(TestData.func_dummy,length=size)
        with self.assertRaises(IndexError):
            seq._check_i(-size-1)

    def test_negative_n(self):
        """
        Verifies that a ValueError exception is raised when an
        attempt is made to create a NumberSequence of a negative
        length.
        """
        size = -100
        with self.assertRaises(ValueError):
            seq = NumberSequence(TestData.func_dummy,length=size)

