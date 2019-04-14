"""
Informal Comparative Performance Tests for caching plans in
CacheableSequence classes

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
import random
import sys
import timeit
from slowcomb.slowseq import BlockCacheableSequence, CacheableSequence
from slowcomb.slowseq import AccumulateSequence, NumberSequence
from slowcomb.slowcomb import CatCombination
from slowcomb.tests.slowprime import fasterer_prime

# TODO: Implement the Python CSV API (in builtin module 'csv').
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
      in the benchmark unit or class.

    * comment - a single line, preferably less than 60 characters long,
      that will appear in the heading of the benchmark report

    Note
    ----
    * Sorry about the one-dimensional tabular format, if you did not like
      redundant information in your reports. This format was chosen
      as it was felt that it would be easier to handle by data importers.
    
    """
    # Get arguments
    benchmarks_default = (
        CacheableSequencePerformanceBenchmark(),
        BlockCacheableSequencePerformanceBenchmark(),
        SequencePerformanceBenchmark(),
    )
    benchmarks = kwargs.get('benchmarks', benchmarks_default)
    comment = kwargs.get('comment')

    # Print report title, start time and column headings
    print("Slowcomb Cacheable Sequence Benchmarks")
    print("Benchmark Started: {0}".format(datetime.datetime.now() ))
    print("All times shown are in seconds")
    if comment is not None:
        print("Comments: {0}".format(comment))

    # Run benchmarks, output results in columns
    for b in benchmarks:
        b._set_bench_seq(1)
        class_name = b._bench_seq.__class__.__name__
        print("Class: {0}".format(class_name))
        cols = {
            "Depth" : None,
            "Lookups" : None,
            "Mu" : None,
            "TimeSU" : None,
            "TimeLU" : None
        }
        for k in cols.keys():
            print(k, end='\t')
        print("")

        for i in range(len(b)):
            params = b[i]
            result = b.run_bench_test(i)
            cols['Depth'] = params[0]
            cols['Lookups'] = params[1]
            cols['Mu'] = params[2]
            cols['TimeSU']=round(result[1],3)
            cols['TimeLU']=round(result[0],3)
            for k in cols.keys():
                print(cols[k], end='\t')
            print("")
        print("\n")

    print("Benchmark Finished: {0}".format(datetime.datetime.now() ))


class SequencePerformanceBenchmark(CatCombination):
    """
    Informal Sequence Performance Benchmarks (SPBs) to evaulate the
    effectiveness of caching plans on lazy sequences in Slowcomb.

    The SequencePerformanceBenchmark is an uncached control benchmark
    that is intended to be a performance baseline.

    This benchmark performs random lookups on a NumberSequence (or
    subclass of) set to perform the same predefined slow lazy evaluation
    for every index. The benchmark is intended to be repeated on a
    cached sequence to test how well it is able to speed up lookups.

    Multiple benchmark tests are performed. The benchmark plan
    comprises all possible test configurations given several
    lists of settings. This benchmark object is a CatCombination
    combinatorial unit that can be subscripted for test configurations.

    Setup
    -----
    This class is essentially a CatCombinator combinatorial unit,
    a sequence of all possible benchmark configurations. Each 
    configuration is in a tuple of arguments. The elements in the
    arguments are, in this order:
    
    1. Depth. When the default benchmark function is used (i.e.
       find the i'th prime number, where i=depth), the depth of
       the prime number to be evaluated.
       
       * An example: setting this to 500 means that the test
         sequence will evaluate the 500th prime number for lookups
         for every index. All indices will return the same value.
         The test sequence will also be 500 terms long.

       * This definition no longer applies when a custom benchmark
         function has been assigned to _func_bench.

       * The default function was chosen to simulate a lazily-evaluated
         sequence with a slow but consistent and uniform evaluation
         time on every access.

    2. Number of lookups. Refers to the number of lookups to perform
       on the test sequence. Lookups are performed using random indices
       of Gaussian distribution.

    3. The mu value, or the tendency for the random indices (which are
       of Gaussian distribution) to stray from the average value,
       defined as depth/2. Higher values increase the average difference
       from depth/2.

       * A high mu value simulates an access pattern with low spatial
         locality, while a low mu value simulates an access pattern 
         with high spatial locality.

    Operation
    ---------
    The benchmark test is invoked using run_bench_test(), using the
    index of the configuration as the argument. For example, with the
    default configuration:

    >>> import slowcomb.demos.benchmark_cache as mod_bc
    >>> spb = mod_bc.SequencePerformanceBenchmark()

    The configuration for test of index 59 is as follows:

    >>> spb[59]
    (500, 2000, 0.0625)

    This test will involve performing 2000 dummy lookups on a test
    sequence set to always evaluate the 500th prime number.

    To run a benchmark with these settings, invoke run_bench_test(59).

    Repeating Tests on Cached Sequences
    -----------------------------------
    In order to repeat the tests on cached sequence classes, this
    benchmark must be subclassed, with the _set_bench_seq() method
    overridden to initialise an instance of the cached class, and
    assign it to _bench_seq.

    The benchmark class was designed this way, to require subclassing,
    as it was expected that caching systems would require initialisation
    procedures that differ enough to make a trivial class swap
    impractical.

    About _lu_indices, the Lookup History
    -------------------------------------
    For those interested in studying the benchmarks further, the indices
    used in the benchmarks are retained in a cached lazy sequence called
    _lu_indices. The indices intended to be set once per test, and remain
    the same until the benchmark object is deleted.

    The history is accessible only when the benchmark is run from an
    interactive prompt and set up by a manual import like:
    
    >>>  import slowcomb.demos.benchmark_cache as mod_bc
    >>>  b = bc.SequencePerformanceBenchmark()

    Run the tests by invoking run_bench_test(). When the test completes,
    the indices used in the benchmark of index i can be recalled from
    _lu_indices:

    ::

      # Run the test
      b.run_bench_test(59)
      # Get the indices
      b._lu_indices[59]


    Optional Arguments
    ------------------
    * depths - a sequence of depths to cycle through.

    * lookups - a sequence of lookup sizes to cycle through.

    * mus - a sequence of mu-values to cycle through.

    * func_bench - the benchmark function to be performed for every
      lookup on the test sequence. The definition should look like:

      ::
         
         fun(x)

      For functions defined at module, function or method scope, and

      ::

        fun(self, x)
      
      For methods defined at class scope.

    """
    defaults = {
        'depths' : [5, 250, 500],
        'lookups' : [2, 250, 500, 1000, 2000],
        'mus' : NumberSequence(lambda x:0.5/2**x, length=4),
        'func_bench' : fasterer_prime
    }

    def _get_random_indices(self, i_limit, lookups, mu):
        """
        Return a tuple of Gaussian-distributed random integers (a.k.a
        numbers that are kinda random yet still predictably to an
        average)

        Arguments
        ---------
        * i_limit - the limit on the integer value allowed in the tuple of
          random numbers. The highest integer in the sequence will be
          i_limit-1. Accepts int, where i_limit > 0.

        * lookups - the number of integers in the tuple. Accepts int,
          where lookups > 0.

        * mu - the propensity of the integers in the tuple to stray
          from an average value, which is set to half of i_limit.
          Larger values result in a greater average difference from
          i_limit/2.  Accepts float, where mu > 0.

        """
        # Just trying out a more functional style here. I hope that the
        # expressions are clear enough to understand on their own.
        def clip(x):
            if x >= i_limit:
                return i_limit-1
            elif x < 0:
                return 0
            else:
                return x
        half_limit = i_limit/2
        get_rand = lambda mu:random.gauss(0,mu)*half_limit + half_limit
        d=[int(clip(get_rand(mu))) for x in range(lookups)]
        return tuple(d)

    def _set_bench_seq(self, i):
        """
        Sets up this benchmark to use an uncached NumberSequence
        of the test of index i of this benchmark. The sequence
        is assigned to the attribute _bench_seq of this benchmark
        unit.

        This method always returns None.

        Recall that this benchmark unit is a sequence of all
        possible combinations of pre-set settings. Invoking
        _set_bench_seq(0) returns a test sequence of configuration
        recalled by self[0].

        Note
        ----
        * Due to differences in caching methodology, this method must 
          be overridden where appropriate for each different class of
          cacheable sequence, as the exact method to enable the cache
          may differ enough to make a simple class swap unusable.

        * This benchmark unit holds the test sequence at instance
          scope instead of passing it directly to the
          _run_benchmark_test() method. This usage pattern opens
          up an opportunity to measuring the amount of time taken
          to set up the test sequences.

        Example
        -------
        Suppose there is this instance of this
        SequencePerformanceBenchmark:

        >>> import slowcomb.demos.benchmark_cache as mod_bc
        >>> spb = mod_bc.SequencePerformanceBenchmark()
        >>> spb[0]
        (5, 2, 0.5)

        Then, invoking _set_bench_seq(0) will cause a sequence of
        depth 5 to be assigned to _bench_seq. For details on what
        depth means, please refer to the class-scope docstring of
        SequencePerformanceBenchmark.        

        """
        params = self[i]
        depth = params[0]
        self._bench_seq = NumberSequence(
            lambda x:self._func_bench(depth+(x*0)), length=depth
        )
            # Please tell me I got the benchmark function right this time...
        self._lu_indices[i]
            # Precache indices

    def run_bench_test(self, i):
        """
        Runs the benchmark of index i. Returns a tuple t of floats
        where:

        * t[0] - the time taken for the lookup benchmark to complete

        * t[1] - the time taken to set up the benchmark 

        The benchmark performs a predefined number of dummy lookups
        using indices sourced from _lu_indices. Please refer to the
        class-scope documentation on how _lu_indices works.

        """
        # Setup benchmark sequence, measure time taken by setup
        timesu_start = datetime.datetime.now()
        self._set_bench_seq(i)
        timesu_end = datetime.datetime.now()
        ts = (timesu_end - timesu_start).total_seconds()
        # Perform the main benchmark
        indices = self._lu_indices[i]
        def _do_dummy_lookups():
            for iii in indices:
                self._bench_seq[iii]
        tb = timeit.timeit('_do_dummy_lookups()',globals=locals(),number=1)
        return (tb, ts)

    def __init__(self, **kwargs):
        """
        Special constructor method supporting setup and configuration
        of the benchmark. For details, see the class-scope documentation
        for SequencePerformanceBenchmark.

        """
        self._bench_seq = None
        self.depths = kwargs.get('depths', self.defaults['depths'])
        self.lookups = kwargs.get('lookups', self.defaults['lookups'])
        self.mus = kwargs.get('mus', self.defaults['mus'])
        self._func_bench = kwargs.get('func_bench',self.defaults['func_bench'])
        self._lu_indices = None

        seq_src = (self.depths, self.lookups, self.mus)
        super().__init__(seq_src, r=3)

        # Please leave the following two statements here, as len(self)
        # is only known once super().__init__() is run.
        self._lu_indices = CacheableSequence(
            lambda x:self._get_random_indices(
                i_limit=self[x][0], lookups=self[x][1], mu=self[x][2]),
            length=len(self)
        )
        self._lu_indices.enable_cache()

class CacheableSequencePerformanceBenchmark(SequencePerformanceBenchmark):
    """
    Informal Cache Benchmarks for the CacheableSequence.

    Setup and configuration of this benchmark is identical to that of
    SequencePerformanceBenchmark. For details on setting up this
    benchmark, refer to the documentation for SequencePerformanceBenchmark.
    All options available on SequencePerformanceBenchmark also apply here.

    For argument defaults, see the section on 'Data and other attributes 
    attributes defined here' below.

    """
    def _set_bench_seq(self, i):
        """
        Sets up this benchmark to use the CacheableSequence
        of the test of index i of this benchmark. The sequence
        is assigned to the attribute _bench_seq of this benchmark
        unit.

        This method always returns None.

        For further details on how this method works and its role
        in the benchmarking process, please refer to the
        documentation for the parent implementation in 
        SequencePerformanceTest._set_bench_seq().

        All details of the parent implementation also apply here,
        with the exception of the process of creating and assigning
        the test sequence.

        """
        params = self[i]
        depth = params[0]
        bseq = CacheableSequence(
            lambda x:self._func_bench(depth+(x*0)), length=depth
        )
        bseq.enable_cache()
        self._bench_seq = bseq

class BlockCacheableSequencePerformanceBenchmark(SequencePerformanceBenchmark):
    """
    Informal Cache Benchmarks for the BlockCacheableSequence.

    Setup and configuration of this benchmark is identical to that of
    SequencePerformanceBenchmark. For details on setting up this
    benchmark, refer to the documentation for SequencePerformanceBenchmark.
    All options available on SequencePerformanceBenchmark also apply here.

    For argument defaults, see the section on 'Data and other attributes 
    attributes defined here' below.

    """
    def _set_bench_seq(self, i):
        """
        Sets up this benchmark to use the BlockCacheableSequence 
        of the test of index i of this benchmark. The sequence
        is assigned to the attribute _bench_seq of this benchmark
        unit.

        This method always returns None.

        As the BlockCacheableSequence must be primed for the cache
        to be effective, this method pre-caches an eighth of the
        sequence: a sixteenth of the sequence right before the median,
        and anohter sixteenth from the median.

        For further details on how this method works and its role
        in the benchmarking process, please refer to the
        documentation for the parent implementation in 
        SequencePerformanceTest._set_bench_seq().

        All details of the parent implementation also apply here,
        with the exception of the process of creating and assigning
        the test sequence.

        Notes
        -----
        This benchmark reveals that priming the cache may take
        a long time if the terms of the sequence are slow to derive.

        The delay in preparing the block means that the block cache
        is suited for scenarios in which cached terms will be 
        accessed many times over a long period.

        This characteristic should be considered when making decisions
        to choose and implement the BlockCacheableSequence.

        """
        params = self[i]
        depth = params[0]
        bseq = BlockCacheableSequence(
            lambda x:self._func_bench(depth+(x*0)), length=depth
        )
        bseq.enable_cache()
        i_mid = depth//2
        i_sixteenth = depth//16 
        slice_start = i_mid - i_sixteenth
        slice_end = max(i_mid + i_sixteenth, depth)
        bseq[slice_start:slice_end]
            # Prime the block cache. This causes about an eighth of the 
            # sequence to be cached.
        self._bench_seq = bseq

if __name__ == '__main__':
    try:
        comment=sys.argv[1]
        run_all_tsv(comment=comment)
    except IndexError:
        # If no comment is entered...
        print('Welcome to the Slowcomb Cache Informal Performance Benchmark')
        print('Please enter a comment for this benchmark.')
        print('Surround your comment in straight/typewriter quotes.')
        print("Example: {0} 'Yet another Tuesday test'".format(sys.argv[0]))


