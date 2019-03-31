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
from slowcomb.tests import examples

# Functions
#
def pretty_print_iter(it):
    for i in it:
        print("◆ " + i)

def test_all_docs():
    """Verify examples in main module docstrings """
    doctest.testfile('../slowseq.py')
    doctest.testfile('../slowcomb.py')

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


# Python Interactive Prompt Welcome Message
#
if __name__ != '__main__':
    print((('hey babe...','Hey, brother!')\
        [datetime.datetime.now().microsecond%2]))
    print('This is the Slowcomb Manual Testing Environment')
    print("For a list of ready-to-play test items, try typing")
    print("'examples' and press the tab key twice.")

