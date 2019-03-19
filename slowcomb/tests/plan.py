"""
plan — Test Planner: Unit Test Method Name Generator
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
from slowcomb.slowcomb import CatCombination

# Utility Classes
#
class TestNameCombinator(CatCombination):
    """
    Template class for systematically generating names for tests.
    """

    desc = 'Test Name Combinator Class'
    def _get_names(self, types):
        raise NotImplementedError
         
    def _get_comb(self, i):
        types = super()._get_comb(i)
        return self._get_names(types)

    def __str__(self):
        return "{0} (Tests: {1})".format(self.desc, len(self))

    def __repr__(self):
        return self.__str__()
        
    def __init__(self,tags,**kwargs):
        """Create a test name combinator

        Optional Arguments
        ------------------
        include - Set to False to output nothing. This is just a way
            to quickly exclude a test name combinstor from a list without
            changing the list.
            Accepts True or False. True by default.
        """
        super().__init__(tags,len(tags))
        if kwargs.get('include',True) is False:
            self._r = 0

class ExampleTestNameCombinator(TestNameCombinator):
    """A hopefully more effective way of describing and documenting
    how this TestNameCombinator works.

    The TestNameCombinator is a CatCombinator which generates formatted
    names from all possible combinations of tags presented to it.
    To get the names, simply create an instance of the TestNameCombinator
    and use it like a Python sequence or iterator.

    >>> from tests.plan import *
    >>> for d in ExampleTestNameCombinator():
    ...     print(d)

    >>> ExampleTestNameCombinator()[7]
    'test_erotic_relationship_aqu_with_vir'

    TestNameCombinators are meant to be used as classes, and not as
    instances of the same class, due to operational circumstances during
    the early parts of the project involving slowcomb. This may change
    in the future.
    """

    desc = 'Astrology Test Suite Demonstraton'
    def _get_names(self, types):
        # Override this function to implement the actual name
        # generation routine
        prefix = 'test'
        out_format = "{0}_{1[0]}_relationship_{1[1]}_with_{1[2]}"
        return out_format.format(prefix,types)
            # Read up on how to use format() if you don't know
            # how to use it, because it will save your life.

    def __init__(self, **kwargs):
        rel_type = ('erotic','platonic')
        zod_sign_greg_ord = ('aqu','pis','ari','tau','gem','can','leo',
            'vir','lbr','sco','sag','cap')
        all_types = (rel_type, zod_sign_greg_ord, zod_sign_greg_ord)
            # Group the tuples into an outer tuple, and feed it to
            #  the TestNameCombinator. Here, the underlying
            #  CatCombinator will run through all star signs for all
            #  star signs for two relationship types.
            # You can repeat the same group twice or more!
        super().__init__(all_types, **kwargs)
            # Please always pass on the **kwargs!

            # The Zodiac actually begins with Aries, although newspapers
            #  like to begin with Aquarius or the star sign of the
            #  month or something like that...

# Length Attribute Test Interfixes 
#
class LengthAttributeTestInterfixes(TestNameCombinator):
    desc = 'Length Attribute Test Name Interfixes'
    def _get_names(self, types):
        subprefix = 'a_len_'
        return "{0}{1[0]}_ii_start".format(subprefix,types)

    def __init__(self, **kwargs):
        offset_types = [['pos','neg','neg_zero_x','zero'],]
        super().__init__(offset_types, **kwargs)

# Slowcomb Sequences Length Attribute Test Names
# 
class SlowseqLengthAttributeTestNames(TestNameCombinator):
    desc = 'Slowcomb Sequences Length Attribute Tests'

    def _get_names(self, types):
        return "{0[0]}.test_{0[1]}".format(types)

    def __init__(self, **kwargs):
        classes = ['NumberSequence','CacheableSequence',
            'BlockCacheableSequence']
        test_types = LengthAttributeTestInterfixes()
        all_types = [classes, test_types]
        super().__init__(all_types, **kwargs)

# Index Test Interfixes
#
class IndexTestInterfixes(TestNameCombinator):
    desc = 'Integer Index Test Interfixes'
    def _get_names(self, types):
        subprefix = 'i_'
        return "{0}{1[0]}_i_{1[1]}_ii_start".format(subprefix,types)
         
    def __init__(self, **kwargs):
        index_types = ['pos','neg','zero']
        offset_types = ['pos','neg','zero']
        all_types = [index_types, offset_types]
        super().__init__(all_types,**kwargs)

class SliceTestInterfixes(TestNameCombinator):
    desc = 'Slice Index Test Interfixes'
    def _get_names(self, types):
        subprefix = 's_'
        out_format="{0}{1[0]}_start_{1[1]}_stop_{1[2]}_step_{1[3]}_ii_start"
        return out_format.format(subprefix,types)
         
    def __init__(self, **kwargs):
        start_types = ['pos','neg','zero']
        stop_types = ['pos','neg','zero']
        step_types = ['pos','neg']
        ii_starts = ['pos','neg','zero']
        all_types = [start_types, stop_types, step_types, ii_starts]
        super().__init__(all_types,**kwargs)

class ZeroXIndexTestInterfixes(TestNameCombinator):
    desc = 'Zero-Crossing Integer Index Test Interfixes'
    def _get_names(self, types):
        subprefix = 'i_'
        subsuffix = 'zero_cross'
        out_format = "{0}{1[0]}_i_{1[1]}_ii_start_{2}"
        return out_format.format(subprefix,types,subsuffix)
         
    def __init__(self, **kwargs):
        index_types = ['pos','neg','zero']
        offset_types = ['neg']
        all_types = [index_types, offset_types]
        super().__init__(all_types,**kwargs)

class ZeroXSliceTestInterfixes(TestNameCombinator):
    desc = 'Zero-Crossing Slice Index Test Interfixes'
    def _get_names(self, types):
        subprefix = 's_'
        subsuffix = 'zero_cross'
        out_format="{0}{1[0]}_start_{1[1]}_stop_{1[2]}_step_{1[3]}_ii_start_{2}"
        return out_format.format(subprefix,types,subsuffix)
         
    def __init__(self, **kwargs):
        start_types = ['neg','pos']
        stop_types = ['pos','neg','zero']
        step_types = ['pos','neg']
        ii_starts = ['neg']
        all_types = [start_types, stop_types, step_types, ii_starts]
        super().__init__(all_types, **kwargs)

# NOTE: Recall that every Combinatorics class is an iterable... ;)

# Resolution and Output Tests Interfixes
# 
class TestTypesInterfixes(TestNameCombinator):
    desc = 'Resolution and Output Test Interfixes'

    def _get_names(self, types):
        return "{0[0]}_{0[1]}".format(types)

    def __init__(self, **kwargs):
        index_types = itertools.chain(
            IndexTestInterfixes(),
            ZeroXIndexTestInterfixes(),
            SliceTestInterfixes(),
            ZeroXSliceTestInterfixes(),
        )
        outcome_types = ['resolve','getitem']
        all_types = [outcome_types, list(index_types)]
        super().__init__(all_types, **kwargs)

# Slowcomb Sequences Resolution and Output Test Names
# 
class SlowseqIndexGetItemTestNames(TestNameCombinator):
    desc = 'Slowcomb Sequences Basic Tests'

    def _get_names(self, types):
        return "{0[0]} using test_{0[1]}".format(types)

    def __init__(self, **kwargs):
        classes = ['NumberSequence','CacheableSequence',
            'BlockCacheableSequence','AccumulateSequence',
            'SumSequence']
        test_types = TestTypesInterfixes()
        all_types = [classes, test_types]
        super().__init__(all_types, **kwargs)

# Slow Combinatorics Tests
#
class CombinatoricsBasicSequenceTestNames(TestNameCombinator):
    desc = 'Combinatorics Basic Sequence Test Names'

    def _get_names(self, types):
        return "{0[0]}:{0[1]}_output_test".format(types)

    def __init__(self, **kwargs):
        classes = ['Combinator','CombinatorWithRepeats','CatCombinator',
            'Permutator','PermutatorWithRepeats',]
        slowseq_test_types = ['iter','i_neg','i_pos','s_neg','s_pos']
        all_types = (classes, slowseq_test_types)
        super().__init__(all_types, **kwargs)

class SlowcombSuiteComprehensiveSequenceTestNames(TestNameCombinator):
    desc = 'Slowcomb Suite Comprehensive Sequence Test Names'

    def _get_names(self, types):
        return "{0[0]} using {0[1]}".format(types)

    def __init__(self, **kwargs):
        classes = ['Combinator','CombinatorWithRepeats','CatCombinator',
            'Permutator','PermutatorWithRepeats','AccumulateSequence',
            'SumSequence']
        slowseq_test_types = TestTypesInterfixes()
        all_types = (classes, slowseq_test_types)
        super().__init__(all_types, **kwargs)

# Basic Performance Tests
#
class CacheableSequencePerformanceTestNames(TestNameCombinator):
    desc = 'Basic Cacheable Performance Test Names'

    def _get_names(self, types):
        out_format="{0[0]}.test_perf_{0[1]}_spat_locality"
        return out_format.format(types)

    def __init__(self, **kwargs):
        classes = ('NumberSequence', 'CacheableSequence',
            'BlockCacheableSequence')
        spat_locality = ('low','low_but_eqdist','medium','high')
        all_types = (classes, spat_locality)
        super().__init__(all_types, **kwargs)

# Combinatorics Performance Tests
#
class CombinatoricsPerformanceTestNames(TestNameCombinator):
    desc = 'Basic Combinatorics Performance Test Names'

    def _get_names(self, types):
        out_format="{0[0]}.test_perf_{0[1]}_n_{0[2]}_r"
        return out_format.format(types)

    def __init__(self, **kwargs):
        classes = ('Combination', 'CombinationWithRepeats','CatCombination',
            'Permutation','PermutationWithRepeats')
        n_values = ('big','small')
        r_values = ('big','small')
        all_types = (classes, n_values, r_values)
        super().__init__(all_types, **kwargs)


# Test Plan CSV File Output
#
# TODO: Re-implement this using the Python CSV API?
def get_csv():
    test_all=itertools.chain(
        SlowseqLengthAttributeTestNames(),
        SlowseqIndexGetItemTestNames(),
        CombinatoricsBasicSequenceTestNames(),
        SlowcombSuiteComprehensiveSequenceTestNames(include=False),
        CacheableSequencePerformanceTestNames(),
        CombinatoricsPerformanceTestNames(),
    )
    # Output CSV Rows
    headings='Test name, Status'
    print(headings)
    name_list = [r for r in test_all]
    for d in name_list:
        print(d, end=',\n')
    print("Tests In Total: {0}".format(len(name_list)))

# Run get_csv() when called from a CLI shell
if __name__=='__main__':
    get_csv()

