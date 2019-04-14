"""
Informal Comparative Performance Tests for sequential combinatorial output

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
import timeit
import itertools 
import sys
from slowcomb.slowseq import NumberSequence
from slowcomb.slowcomb import CatCombination, Combination,\
    CombinationWithRepeats, Permutation, PermutationWithRepeats

def run_all_tsv(**kwargs):
    """
    Run all benchmarks in a predefined sequence, and produce a report
    in the form of a tab-separated, newline-delimited spreadsheet.
    This function is intended to be run from a command-line shell with
    the results piped to into file.
    
    The default benchmark sequence is in benchmarks_default, in the body
    of the code of this function.

    Optional Arguments
    ------------------
    * benchmarks - a sequence of benchmarks to be run in order of
      appearance. The default list of benchmarks can be found in this
      function's body in the module source file.
      To customise a benchmark, please consult the documentation
      in the benchmark object or class.

    * comment - a single line, preferably less than 60 characters long,
      that will appear in the heading of the benchmark report

    Note
    ----
    * The two-dimensional tabular format was chosen, despite its tendency
      to repeat information excessively, as opposed to the multi-dimensional
      format (e.g. a list of tables, where there are columns for each r and
      rows for each n for each table) as it was felt that this format would
      allow use of simpler, more primitive programs (which are easier to
      code) for data imports.
    
    """
    # Get arguments
    benchmarks_default = (
        CombinationSPB(),
        PermutationSPB(),
        PermutationWithRepeatsSPB(),
    )
    benchmarks = kwargs.get('benchmarks', benchmarks_default)
    comment = kwargs.get('comment')

    # TODO: Implement the Python CSV API (in builtin module 'csv').

    # Print Title, Time and Column Headings
    print("Slowcomb Sequential Combinatorial Benchmarks")
    print("Benchmark Started: {0}".format(datetime.datetime.now() ))
    print("All times shown are in milliseconds")
    if comment is not None:
        print("Comments: {0}".format(comment))
    cols = {
        "Class" : None,
        "n" : None,
        "r" : None,
        "TimeA" : None
    }
    for k in cols.keys():
        print(k, end='\t')
    print("")

    # Run benchmarks, output results in columns
    for b in benchmarks:
        for i in range(len(b)):
            result = b.run_bench_test(i)
            cols['Class'] = result[0]
            cols['n'] = result[1]
            cols['r'] = result[2]
            cols['TimeA'] = round(result[3]*1000,3)
            for k in cols.keys():
                print(cols[k], end='\t')
            print('')

    # Close report
    print("Benchmark Finished: {0}".format(datetime.datetime.now() ))

class CombinationSPB(CatCombination):
    """
    Informal Sequential Performance Benchmarks (SPBs) for selection
    combinatorial units (combination classes).

    This class is essentially a CatCombinator combinatorial unit,
    a sequence of all possible benchmark configurations. Each 
    configuration is in a tuple of arguments. The elements in the
    arguments are, in this order:
    
    1. The benchmark to be run,

    2. The n argument of the benchmark,

    3. The r argument of the benchmark.

    The benchmark test is invoked using run_bench_test(), using the
    index of the configuration as the argument.

    Optional Arguments
    ------------------
    * classes - A sequence of benchmarks to be run. All benchmarks in
      the sequence will be run in order of appearance in the sequence.

    * ns - A sequence of n-values to be used with the benchmarks.

    * rs - A sequence of r-values to be used with the benchmarks.

    Example
    -------
    On the default Combination SPB, benchmark zero is a timed test on
    itertools.combinations, with an eight-element source and a term size
    of four.

    >>> import itertools
    >>> import slowcomb.demos.benchmark_comb_seq_out as mod_bcomb
    >>> bench = mod_bcomb.CombinationSPB()
    >>> bench[0]
    (<class 'itertools.combinations'>, 8, 4)

    Run bench.run_bench_test(0), to run a benchmark on an
    itertools.combinations combinatiorial unit, with an eight-element
    source and four-element terms.


    Smaller numbers generally indicate faster performance.

    """
    ns_default = (8,12,20)
    rs_default = (4,5,6,7)
    defaults = {
        'classes' : (itertools.combinations,
            itertools.combinations_with_replacement,
            Combination,
            CombinationWithRepeats,
        ),
        'ns' : ns_default,
        'rs' : rs_default
    }
    
    def run_bench_test(self, i):
        """
        Runs the benchmark of index i.

        Returns a float number indicating the approxiate time taken to
        run the benchmark in milliseconds.

        The benchmark test measures the amount of time taken to perform
        dummy lookups of every term in a combinatorial unit in order
        from the first term to the last term.

        Tests where the r-value (term length) is larger than the
        n-value (items in source sequence) will not run and return
        a time of zero milliseconds.

        Recall that this class is a CatCombination in disguise, containing
        all possible benchmark configurations, lazily-evaluated.

        A particular benchmark test's configuration may be examined by
        requesting the term of index i in the benchmark object as a
        sequence:

        >>> import itertools
        >>> from slowcomb.demos.benchmark_comb_seq_out import CombinationSPB
        >>> bench = CombinationSPB()
        >>> bench[0]
        (<class 'itertools.combinations'>, 8, 4)

        Thus, invoking test 0 with run_bench_test(0) will perform
        a benchmark on the itertools.combination class, where n=8 and
        r=4.

        """
        params = self[i]
        cu_class = params[0]
        class_name = cu_class.__name__
        n = params[1]
        r = params[2]
        # Invoke the timing process
        if n<r:
            time_sec = 0
            # Ignore n < r situations for now
        else:
            cu = self._get_cu(cu_class, n, r)
            def test_cu(cu):
                for x in cu:
                    pass
            time_sec = timeit.timeit('test_cu(cu)', globals=locals(),
                number=1)
                # PROTIP: To run timeit.timeit() in function scope,
                # use the variables returned by locals() for the globals
                # argument.
        return (class_name, n, r, time_sec)


    def _get_cu(self, cu_class, n, r):
        """
        Return a test combinatorial unit of class cu_class, with a
        source sequence of n items, which produces terms of length
        r.

        The source sequence of the test CU is a tuple of integers from
        0 to n-1.

        """
        seq_src = tuple([x for x in range(n)])
        cu = cu_class(seq_src, r)
        return cu

    def __init__(self, **kwargs):
        """
        Special constructor method supporting setup and configuration
        of the benchmark. For details, see the class-scope documentation
        for CombinationSPB.

        """
        self.classes = kwargs.get('classes', self.defaults['classes'])
        self.ns = kwargs.get('ns', self.defaults['ns'])
            # Sequence of n-values
        self.rs = kwargs.get('rs', self.defaults['rs'])
            # Sequence of r-values
        seq_src = (self.classes, self.ns, self.rs)
            # Source sequence to be used in the test combinatorial units.
        super().__init__(seq_src, r=3)

class PermutationSPB(CombinationSPB):
    """
    Informal Sequential Performance Benchmarks (SPBs) for order 
    combinatorial units (permutation classes).

    Setup and configuration of this benchmark is identical to
    that of CombinationSPB. For details on setting up this benchmark
    refer to the documentation for CombinationSPB. All options
    available on CombinationSPB also apply to this benchmark.

    For argument defaults, see the section on 'Data and other attributes 
    attributes defined here' below

    """
    def __init__(self, **kwargs):
        """
        Special constructor method supporting setup and configuration
        of the benchmark. For details, see CombinationSPB

        """
        ns = (4,6,8,12)
        rs = (4,5,6,7)
        classes = (itertools.permutations, Permutation)
        super().__init__(classes=classes, ns=ns, rs=rs)

class PermutationWithRepeatsSPB(CombinationSPB):
    """
    Informal Sequential Performance Benchmarks (SPBs) for the
    repeats-permitted permutation combinatorial unit of slowcomb.

    Setup and configuration of this benchmark is identical to
    that of CombinationSPB. For details on setting up this benchmark
    refer to the documentation for CombinationSPB. All options
    available on CombinationSPB also apply to this benchmark.

    For argument defaults, see the section on 'Data and other attributes 
    attributes defined here' below.

    """
    def __init__(self, **kwargs):
        """
        Special constructor method supporting setup and configuration
        of the benchmark. For details, see CombinationSPB

        """
        ns = (4,6,8,10)
        rs = (4,5,6,7)
        classes = (PermutationWithRepeats,)
        super().__init__(classes=classes, ns=ns, rs=rs)

if __name__ == '__main__':
    try:
        comment=sys.argv[1]
        run_all_tsv(comment=comment)
    except IndexError:
        # If no comment is entered...
        print('Welcome to the Slowcomb Combinatorial Unit Informal SPB')
        print('Please enter a comment for this benchmark.')
        print('Surround your comment in straight/typewriter quotes.')
        print("Example: {0} 'Yet another Tuesday test'".format(sys.argv[0]))

