"""
performance_cache — Informal Comparative Performance Tests for caching plans 
in CacheableSequence classes
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

import datetime
import itertools
import random
import unittest
from slowcomb.slowseq import BlockCacheableSequence, CacheableSequence, \
    NumberSequence
from tests.slowprime import slow_prime

class LowSpatialLocalityPerformanceTest(unittest.TestCase):

    depth = 500
        # How far down the sequence to go.
        # Higher numbers means longer sequences. Some sequences,
        #  such as the Slow Prime Number Finders can take considerably
        #  longer to return terms towards the end of the sequence.
    func = lambda self,x:slow_prime(x)
    runs = [2,50,100,500]
    test_case_name = 'Low Spatial Locality'
    mu = 0.2

    def setUp(self):
        self._indices = []
        for r in self.runs:
            self._indices.append(self._get_random_indices(r,self.mu))
            
    def _get_random_indices(self, n, mu):
        out=[]
        for i in range(n):
            half_depth = self.depth/2
            d=int( random.gauss(0,mu)*half_depth + half_depth )
            # Clip values if the random generator spits out
            # out-of-bounds values, usually due to mu set
            # too high (i.e. > 0.3)
            if d > self.depth:
                d=self.depth
            elif d < 0:
                d=0
            out.append(d)
        return tuple(out)

    def _do_dummy_lookups(self, seq):
        class_name = seq.__class__.__name__
        banner_format = "{0}: {1}(mu={2}, depth={3})"
        print(banner_format.format(class_name, self.test_case_name,
            self.mu, self.depth))
        for i in self._indices:
            print("{0}r".format(len(i)),end=' ')
            dt_start = datetime.datetime.now()
            for j in i:
                seq[j]
            dt_end = datetime.datetime.now()
            dt_elapsed = dt_end-dt_start
            print("{0}s".format(dt_elapsed.total_seconds()), end=', ')
        if hasattr(seq,'_cache'):
            print('Cache size: {0}'.format(len(seq._cache)), end='')
        print('\n')
 
    def test_number_sequence(self):
        seq = NumberSequence(self.func, length=self.depth)
        self._do_dummy_lookups(seq)
 
    def test_cacheable_sequence(self):
        seq = CacheableSequence(self.func, length=self.depth)
        seq.enable_cache()
        self._do_dummy_lookups(seq)
 
    def test_block_cacheable_sequence(self):
        seq = BlockCacheableSequence(self.func, length=self.depth)
        half_depth = self.depth//2
        seq.enable_cache()
        # Prime the block cache after enabling it
        seq[half_depth-10:half_depth+10]
        self._do_dummy_lookups(seq)


class MediumSpatialLocalityTest(LowSpatialLocalityPerformanceTest):
    test_case_name = 'Medium Spatial Locality'
    mu = 0.05

class HighSpatialLocalityTest(LowSpatialLocalityPerformanceTest):
    test_case_name = 'High Spatial Locality'
    mu = 0.0125


