"""
manual — Manual Testing environment for interactive Python prompt
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
import doctest
import pdb
import timeit
from slowcomb.slowcomb import *
from slowcomb.slowseq import *

# Test Data
#
test_data = {'pokies':('💖', '💎', '🦄', '🍒', '🌴', '💰'),
            'pokies_short':('💖', '💎', '🦄', '🍒'),
            'abcd':('a','B','c','D'),
            'abcdef':('a','B','c','D','e','F'),
            'colonel':(('I'),('need','want'),('sugar', 'spice', 'scissors')),
}
# Special thanks to the contributors at Emojipedia!

# Functions
#
def test_all_docs():
    doctest.testfile('../slowseq.py')
    doctest.testfile('../slowcomb.py')

# Classes
# 
class SeqTest:

    def print_all_terms(self):
        self.seq._i = 0
        for i in self.seq:
            print(i)

    def run(self):
        self.print_all_terms()

    def __init__(self, seq):
        self.seq = seq


class CombrTest(SeqTest):

    def extract_str(self, t):
        """Extracts strings from an iterable, then combines them into a
        new single string.
        """
        sep = ' '
        out = ""
        for i in t:
            if isinstance(i, str):
                out="".join( (out, sep, str(i)) )
        return out

    def print_all_addrs(self):
        for a in range(len(self.seq)):
            readout = str(self.seq._get_seq_addresses(a))
            print("Address of {0} is {1}".format(a, readout))

    def run(self):
        self.print_all_terms()
        self.print_all_addrs()

    def __init__(self, seq):
        super().__init__(seq)

# Manual Testing Environment Preparation
#
abcd = test_data['abcd']
abcdef = test_data['abcdef']
colonel = test_data['colonel']
pokies = test_data['pokies']
pokies_short = test_data['pokies_short']

test_p_abcd = CombrTest(Permutation(abcd))
test_p_pokies = CombrTest(Permutation(pokies))
test_p_pokies_short = CombrTest(Permutation(pokies_short))

test_pr_pokies = CombrTest(PermutationWithRepeats(pokies,r=6))
test_pr_pokies_short = CombrTest( PermutationWithRepeats(pokies_short,r=4))

test_cc_colonel = CombrTest(CatCombination(colonel))

test_c_abcdef = CombrTest(Combination(abcdef,r=3))
test_c_pokies_short = CombrTest(Combination(pokies_short,r=2))

test_cr_abcd = CombrTest(CombinationWithRepeats(abcd,r=4))
test_cr_pokies_short = CombrTest(CombinationWithRepeats(pokies_short,r=4))

test_seq_snob = SeqTest(SNOBSequence(6,4))
test_cc_node_counts = SeqTest( CacheableSequence(lambda x:len(colonel[x]),
    length=len(colonel)) )
test_cc_thresholds = SeqTest( SumSequence(lambda x:len(colonel[x]),
    length=len(colonel)) )

# Python Interactive Prompt Welcome Message
#
if __name__ != '__main__':
    print((('hey babe...','Hey, brother!')\
        [datetime.datetime.now().microsecond%2]))
    print('This is the Slowcomb Manual Testing Environment')
    print("Test items available from dict test_data: {0}".format( tuple(test_data.keys())) )
    print("More items are also available!")
    print("Just try 'test_' and press the tab key!")

