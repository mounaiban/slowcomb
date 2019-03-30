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
from slowcomb.tests.examples import *

# Test Data
#
#   Special thanks to the contributors at Emojipedia!
test_data = {
            'abcd':('a','B','c','D'),
            'abcdef':('a','B','c','D','e','F'),
            'atoz_upper':[chr(65+x) for x in range(26)],
            'colonel':(('I',),('need','want'),('sugar', 'spice', 'scissors')),
            'pokies':('💖', '💎', '🦄', '🍒', '🌴', '💰'),
            'pokies_short':('💖', '💎', '🦄', '🍒'),
}

# Test Sequences
#
#   Please place test candidates for Permutators, Combinators, or all
#   other support sequence inside the test_cand dictionary.
#
#   This makes it easier to automate the manual tests (contradictory,
#   but helpful!)
test_cand = {'test_c_abcdef' : Combination(test_data['abcdef'],r=3),
        'test_c_pokies_short' : Combination(test_data['pokies_short'],r=2),
        'test_cc_colonel' : CatCombination(test_data['colonel'], r=3),
        'test_cc_colonel_no_r' : CatCombination(test_data['colonel']),
        'test_cc_complex' : CatCombination(
            (
                Permutation(test_data['atoz_upper'], r=6),
                CatCombination(test_data['colonel'], r=3),
            ),
            r=2),
        'test_cr_abcd' : CombinationWithRepeats(test_data['abcd'],r=4),
        'test_cr_pokies_short' : CombinationWithRepeats(
            test_data['pokies_short'],r=4),
        'test_p_abcd' : Permutation(test_data['abcd']),
        'test_p_pokies_no_r' : Permutation(test_data['pokies']),
        'test_p_pokies_short_no_r' : Permutation(test_data['pokies_short']),
        'test_pr_pokies' : PermutationWithRepeats(test_data['pokies'],r=6),
        'test_pr_pokies_short' : PermutationWithRepeats(
             test_data['pokies_short'],r=4),
        'test_seq_snob' : SNOBSequence(6,4),
        'test_seq_node_counts' : CacheableSequence(lambda x:4**x, length=4),
        'test_sseq_thresholds' : SumSequence(lambda x:4**x, length=4), 
}

# Functions
#
def pretty_print_iter(it):
    for i in it:
        print("◆ " + i)

def test_all_docs():
    """Verify examples in main module docstrings """
    doctest.testfile('../slowseq.py')
    doctest.testfile('../slowcomb.py')

def test_class_repr():
    """
    Return the output of __repr__() of all test sequences in test_cand
    """
    for k in test_cand.keys():
        print("{0}: {1}".format(k, repr(test_cand[k])) )

def test_get_test_data_names():
    """Return the names of all test data items in test_data"""
    pretty_print_iter(test_data.keys())

def test_get_test_seq_names():
    """Return the names of all test sequences in test_cand"""
    pretty_print_iter(test_cand.keys())

def test_get_test_seq(name):
    """Return a test sequence of a specific name k"""
    item = test_cand[name]
    if issubclass(item.__class__, Combinatorics) is True:
        return CombrTest(item)
    elif issubclass(item.__class__, NumberSequence) is True:
        return SeqTest(item)
    else:
        return "This is not a Slowcomb sequence"

# Classes
# 
class SeqTest:

    def print_all_terms(self):
        self.seq._i = 0
        for i in self.seq:
            print(i)

    def run(self):
        self.print_all_terms()

    def __repr__(self):
        seq_repr = "Sequence: {0}".format(repr(self.seq) )
        banner = "Invoke .run() to see all items"
        return "{0}, {1}".format(seq_repr, banner)

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

    def __repr__(self):
        seq_repr = "Sequence: {0}".format(repr(self.seq) )
        banner = "Invoke .run() to see all items and address info"
        return "{0}, {1}".format(seq_repr, banner)

    def __init__(self, seq):
        super().__init__(seq)

# Manual Testing Environment Preparation
# 
#  Prepare test items for easy access
test_cc_colonel = test_get_test_seq('test_cc_colonel')
test_cc_colonel_no_r = test_get_test_seq('test_cc_colonel_no_r')
test_cc_complex = test_get_test_seq('test_cc_complex')
test_c_abcdef = test_get_test_seq('test_c_abcdef')
test_c_pokies_short = test_get_test_seq('test_c_pokies_short')
test_cr_abcd = test_get_test_seq('test_cr_abcd')
test_cr_pokies_short = test_get_test_seq('test_cr_pokies_short')
test_p_abcd = test_get_test_seq('test_p_abcd')
test_p_pokies_no_r = test_get_test_seq('test_p_pokies_no_r')
test_p_pokies_short_no_r = test_get_test_seq('test_p_pokies_short_no_r')
test_pr_pokies = test_get_test_seq('test_pr_pokies')
test_pr_pokies_short = test_get_test_seq('test_pr_pokies_short')
test_seq_snob = test_get_test_seq('test_seq_snob')
test_seq_node_counts = test_get_test_seq('test_seq_node_counts')
test_sseq_thresholds = test_get_test_seq('test_sseq_thresholds')

# Python Interactive Prompt Welcome Message
#
if __name__ != '__main__':
    print((('hey babe...','Hey, brother!')\
        [datetime.datetime.now().microsecond%2]))
    print('This is the Slowcomb Manual Testing Environment')
    print("Test items available from dict test_data:")
    test_get_test_data_names()
    print("Test candidates available from dict test_cand:")
    test_get_test_seq_names()
    print("To get a test data item, type: x = test_data['name']")
    print("To get a test sequence, type: x = test_cand['name']")
    print("Substitute 'name', with a name above, retain the quotes.")
    print("Substitute x with anything you want, then play with it!")
    print("For a list of ready-to-play test items, try typing")
    print("'test_' and press the tab key twice.")

