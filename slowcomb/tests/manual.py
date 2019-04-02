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
from . import examples
from slowcomb import slowcomb, slowseq
from slowcomb.tests.slowprime import *

# Functions
#
def test_all_docs():
    """Verify examples in main module docstrings"""

    doctest.testfile('../slowseq.py')
    doctest.testfile('../slowcomb.py')


# Classes
# 
class SeqTest:
    
    def run_as_iter(self):
        self._seq._i = 0
        for i in self._seq:
            print(i)

    def run(self, i_start=None, i_stop=None):
        if i_stop is None:
            if i_start is not None:
                i_stop=i_start+1
            else:
                i_start=0
                i_stop=len(self._seq)

        count = 0
        for i in range(i_start, i_stop):
            self.print_term(i)
            count += 1
        print("Showing {0}/{1} terms".format(count, len(self._seq)) )

    def print_term(self, i):
        print(self._seq[i])

    def __repr__(self):
        banner = "Invoke .run() to see all items"
        name = self.__class__.__name__
        return "{0}: {1}\n{2}".format(name, repr(self.seq), banner)

    def __init__(self, seq):
        self._seq = seq


class CombrTest(SeqTest):

    def _get_bitmap_str(self, i):
        """
        Get the selection bitmap for the first+i'th combinatioral term,
        of the combinatorial unit wrapped by this CombrTest, assuming
        that it uses bitmaps.

        """
        bm = self._seq._bitmap_src[i]
        if isinstance(bm, int):
            len_src = len(self._seq._seq_src)
            return ("{:0"+ str(len_src) +"b}").format(bm)
        else:
            raise TypeError('unexpected bitmap format, expected an int')

    def _get_tree_path_str(self, i):
        """
        Get the combinatorial tree path for the first+i'th term
        of the combinatorial unit wrapped by this CombrTest, assuming
        that it uses trees.

        """
        tpath = self._seq._get_comb_tree_path(i)
        return str(tpath)

    def print_term(self, i):
        # Output combinatorial terms with selection data
        ii=self._seq._resolve_i(i)
        out_form = "{0}\t{1}"
        out=out_form.format(self._selection_data_method(ii), self._seq[i])
        print(out)

    def __repr__(self):
        banner = "Invoke .run() to see all items and selection data"
        name = self.__class__.__name__
        return "{0}: {1}\n{2}".format(name, repr(self._seq), banner)

    def __init__(self, seq):
        super().__init__(seq)
        if(hasattr(self._seq, '_bitmap_src')):
            self._selection_data_method = self._get_bitmap_str
        elif(hasattr(self._seq, '_get_comb_tree_path')):
            self._selection_data_method = self._get_tree_path_str
        else:
            raise TypeError('unknown or non-combinatorial unit specified')

# Python Interactive Prompt Welcome Message
#
if __name__ != '__main__':
    print((('hey babe...\n','Hey, brother!\n')\
        [datetime.datetime.now().microsecond%2]))
    print('Welcome to the Slowcomb Manual Testing Environment')
    print("For a list of ready-to-play test items, try typing")
    print("'examples.' (with the dot) and press the tab key twice.")

