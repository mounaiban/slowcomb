"""
Test Method Name Generator and Planner

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

    Arguments
    ---------
    * tags - a sequence of sequences containing test tags that will
      become part of the generated test names. Every tag combination
      from all sequences will be used. Tags will appear in the order
      as specified in the output format.

    * out_format - the output format which becomes the full name of
      the test. The format should be like:
      
      ::

        "test_cond_a_{0[x]}_cond_b_{0[x+1]}_cond_c_{0[x+2]}"

      and so on...
      
      The {0} replacement fields references the tag combination,
      while the subscripts after the 0 indicates which tag
      of the combination to use. For a more detailed explanation,
      see the Example below.

    Optional Arguments
    ------------------
    * include - Set to False to output nothing. This is just a means
      of excluding a test name combinator from a combinatorial chain
      without changing the list. Accepts True or False.
      True by default.

    Example
    -------
    Let's create a test name combinator for our role-playing-game:
    
    >>> from slowcomb.demos.test_planner import TestNameCombinator
    >>> tags_m = ('good', 'neutral', 'evil')
    >>>     # adapted from Dungeons and Dragons Morality
    >>> tags_a = ('chaotic', 'neutral', 'lawful')
    >>>     # adapted from D&D Adherence
    >>> tags_c = ('scientist', 'architect', 'hacker')
    >>>     # Our original classes
    >>> tags_all = (tags_m, tags_a, tags_c)
    >>> out_format = "test_ending_select_{0[2]}_{0[1]}_{0[0]}"
    >>> comb = TestNameCombinator(tags_all, out_format)

    Access the combinator as an iterator to see all the names:

    >>> for t in comb:
    ...     print(t)
    test_ending_select_scientist_chaotic_good
    test_ending_select_architect_chaotic_good
    test_ending_select_hacker_chaotic_good
    test_ending_select_scientist_neutral_good
    test_ending_select_architect_neutral_good
    test_ending_select_hacker_neutral_good
    test_ending_select_scientist_lawful_good
    test_ending_select_architect_lawful_good
    test_ending_select_hacker_lawful_good
    test_ending_select_scientist_chaotic_neutral
    test_ending_select_architect_chaotic_neutral
    test_ending_select_hacker_chaotic_neutral
    test_ending_select_scientist_neutral_neutral
    test_ending_select_architect_neutral_neutral
    test_ending_select_hacker_neutral_neutral
    test_ending_select_scientist_lawful_neutral
    test_ending_select_architect_lawful_neutral
    test_ending_select_hacker_lawful_neutral
    test_ending_select_scientist_chaotic_evil
    test_ending_select_architect_chaotic_evil
    test_ending_select_hacker_chaotic_evil
    test_ending_select_scientist_neutral_evil
    test_ending_select_architect_neutral_evil
    test_ending_select_hacker_neutral_evil
    test_ending_select_scientist_lawful_evil
    test_ending_select_architect_lawful_evil
    test_ending_select_hacker_lawful_evil

    Notice how the tags get inserted into the {0[x]} fields, and how
    the tags appear in reverse order. Observe in the format:

    ::

      out_format = "test_ending_select_{0[2]}_{0[1]}_{0[0]}"

    That the subscripts are in reverse order: 2, 1 and 0.

    This is merely a fraction of our possible endings, and there are
    already so many tests! Our game will miss Christmas at least twice
    at this rate!

    """
    def index():
        # TODO: Implement index()
        raise NotImplementedError('index() reverse-lookup not yet available')

    def _get_args(self):
        """
        Returns a string representation of a probable expression
        which may re-create this combinatorial unit.

        """
        out = "tags={0},include={1}".format(self._tags, self._r>0)
        return out

    def _get_comb(self, i):
        """
        Gets a tag combination of index i, formats it into a test
        name and outputs it as a string.
        """
        comb_data = super()._get_comb(i)
        return self._out_format.format(comb_data)

    def __init__(self, tags, out_format, **kwargs):
        """
        Create an instance of the TestNameCombinator. For instructions
        on using this class, please refer to the class-scope
        documentation for TestNameCombinator.

        """
        super().__init__(tags,len(tags))
        self._out_format = out_format
        self._tags = self._seq_src
        if kwargs.get('include',True) is False:
            self._r = 0

class ExampleTestNameCombinator(TestNameCombinator):
    """
    Generate test names for tropical/sidereal Zodiac-type astrological
    relationship compatibility tests.

    This is a hopefully more effective way of describing and documenting
    how the TestNameCombinator class works.

    The ExampleTestNameCombinator demonstrates how TestCombinators
    may be used as subclasses, in situtations where this is more
    advantageous than using instances.

    """
    def __init__(self, **kwargs):
        out_format = "test_{0[0]}_relationship_{0[1]}_with_{0[2]}"
        rel_type = ('erot','plat')
        zod_sign_greg_ord = ('aqu','pis','ari','tau','gem','can','leo',
            'vir','lbr','sco','sag','cap')
                # Zodiac signs with ordered by start date appearance
                # in Gregorian Calendar
        tags = (rel_type, zod_sign_greg_ord, zod_sign_greg_ord)
            # Group the tags to be combined into separate tuples,
            # then wrap the tag tuples in an outer tuple for the
            # the TestNameCombinator. 
            # Abbreviate the tags as much as readability is preserved,
            # to keep the name from getting to long.
            # Note that the Zodiac signs are used twice, to represent
            # the two parties in the relationship.
            #
            # NOTE: The Zodiac actually begins with Aries, although
            # newspapers like to begin with Aquarius or the star sign
            # of the month or something like that...

        super().__init__(tags, out_format, **kwargs)
            # Please always pass on the **kwargs!

# Shared Tags
#
tags_pnz = ('pos','neg','zero')
tags_ii_start_stop = ('pos','neg','neg_zero_x')

# Slice Start, Stop and Step Cases Suffixes
#
tags_slice_cases = (tags_pnz, tags_pnz, tags_pnz)
format_slice_cases = "{0[0]}_start_{0[1]}_stop_{0[2]}_step"
names_slice_cases = TestNameCombinator(tags_slice_cases, format_slice_cases)

# Slowcomb Sequences Integer Subscription Test Names
#
tags_intkey_cases = (tags_pnz, tags_ii_start_stop)
format_intkey_cases = "test_intkey_{0[0]}_i_{0[1]}_ii_start"
names_intkey_cases = TestNameCombinator(tags_intkey_cases,format_intkey_cases)

# Slowcomb Sequences Slice Subscription Test Names
# 
tags_slicekey_cases = (names_slice_cases, tags_ii_start_stop)
format_slicekey_cases = "test_slicekey_{0[0]}_{0[1]}_ii_start"
names_slicekey_cases = TestNameCombinator(tags_slicekey_cases,
    format_slicekey_cases)

# Preliminary Slowcomb Sequences Comprehensive Test Plan
#
# TODO: Re-implement this using the Python CSV API?
def get_csv():
    tests=itertools.chain(names_intkey_cases,names_slicekey_cases)
    test_list=[t for t in tests]
    classes=('NumberSequence', 'CacheableSequence', 'BlockCacheableSequence')
    # Output CSV Rows
    headings='Test name,Status'
    print(headings)
    count=0
    for c in classes:
        for t in test_list:
            print("{0}:{1}".format(c,t), end=',NOT_IMPLEMENTED\n')
            count+=1
    print("Tests In Total: {0}".format(count))

# Run get_csv() when called from a CLI shell
if __name__=='__main__':
    get_csv()

