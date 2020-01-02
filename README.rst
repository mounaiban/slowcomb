Slow Combinatorics in Python (slowcomb)
---------------------------------------

*A Mounaiban mini-project*

What is Slowcomb?
=================
Slowcomb is a mini-library of combinatorics classes for the Python programming
language and platform, implementing two of the most common combinatorics 
operations: permutations and combinations.

Slowcomb implements its classes as sequences (called Combinatorial Units, or
CUs), allowing the results of these operations to be recalled instantly with
integer indices.

Why Use It?
===========
The expected benefits of using Slowcomb for combinatorial operations include
reproducibility of results and significantly reduced memory requirements when
working with very large sets of combinatorial terms.

Slowcomb works best in situations where a very small but random and
unpredicatble subsample of a very large set of terms are needed at any given
time.

The Slowcomb project was mainly motivated by the lack of random access to
terms when using Python's extremely fast combinatorial classes from the
``itertools`` module. An unpublished game engine that made heavy use of
combinatorics was found to be using excessive amounts of memory, due to the 
use of large combinatorial term dumps.

Things You Can Do 
=================
Here is a basic example of recalling a single term from a Permutation CU:  

::

    >>> source = ('A', 'B', 'C', 'D')
    >>> perm_abcd = Permutation(source, r=4)
    >>> perm_abcd[11]
    ('B', 'D', 'C', 'A')

The 12th (or first+11'th) possible way of rearranging the letters
``A, B, C, D`` is ``B, D, C, A``, when using the canoncial method of
permutation seen in school mathematics textbooks, that is, considering all 
possible ways of switching the letters in order, from right to left.

Slicing on combinatorial units is also supported:

::

    >>> perm_abcd[5:9]
    (('A', 'D', 'C', 'B'), ('B', 'A', 'C', 'D'), ('B', 'A', 'D', 'C'),
    ('B', 'C', 'A', 'D'))

Only the sixth, seventh, eighth and ninth permutations are returned 

  PROTIP: first index of a sequence is 0.

You can find out the number of permutations using the ``len()`` function:

::

    >>> len(perm_abcd)
    24

As indicated, there are twenty-four possible ways four elements may be
arranged.

The index of a combinatorial result can be recalled:

::

    >>> perm_abcd.index( ('D','C','B','A') )
    23

Remember to split the elements of the terms in the exact form they supplied
to the CU, especially when working on strings.

Index reverse lookups are only supported when the source sequence supports
reverse lookups through a method named ``index()``. Using sources that do
not fulfill this requirement will disable reverse lookup.

As expected, ``D, C, B, A`` is reported to be the twenty-fourth and last
permutation of ``A, B, C, D``.

  PROTIP: Recall from maths class that the final permutation of a sequence
  is the sequence in reverse order.

All combinatorial operations in Slowcomb are 'lazy'; results are only
evaluated when requested.

Slowcomb's combinatorial operations work only with container types in which
elements are addressable with integer indices, such as tuples and lists.

How Do I Get Started Using It?
==============================
Please see the ``INSTALL.rst`` file in the repository root directory.

Also check out the ``demos`` folder for usage examples and performance
benchmarks. To start the Introductory Demo, run

::
        ``python -m slowcomb.demos.demo``

from a command line while in the same directory as this file.

*Slowcomb is free software, licensed to you under the Terms of the GNU
General Public License, Version 3 or later. Please view the LICENSE file
for full terms and conditions.*

Also, I Am Not A Mathematician.

Known Strengths and Weaknesses
==============================

Strengths
*********
Slowcomb makes it practical to work on small parts of a very large
combinatorial set (in maths jargon, *large-n, small-p* problems) with reduced
memory usage and instant access to specific terms and the ability to identify
specific terms with a single number.  It finds use where it is not feasible or
necessary to unpack the entire range of combinatorial terms.

Example situations where Slowcomb is expected to be of use include:

1. Software testing. Test configurations may be difficult to express in their
   literal forms. When the range of configurations is expressed as a CU,
   configurations can be easily identified with numerical indices.

2. Graphic or product design. The range of variations on a design can be
   expressed as a CU, and each specific design can be identified with a
   numerical index.

3. Procedural synthesis in games or multimedia arts. The range of possible
   configurations of a synthesis can be expressed as a CU, allowing specific
   results to be recalled and identified with a numerical index.

In the above situations, there is no need to store a large number of results,
as they can be quickly or at least predictably and deterministically repeated
with the use of the index.

Weaknesses
**********
Slowcomb also has several identified weaknesses, mostly due to its slow rate of 
generating successive results (hence its name) and inability to work on
so-called *non-subscriptable* sources whose elements cannot be individually
addressed (such as generators, iterators and some data streams).

Here are some situations where there is no expected benefit using Slowcomb:

1. Password recovery. Most password recovery operations tend to use large
   numbers of successive combinatorial results, making other means such as
   Python's ``itertools`` more useful due to their performance advantage in
   such operations. Also, passwords are often most conveniently identified by
   their literal form, making the repeatability of results by using numerical
   indices irrelevant.

2. Brand name surveys. When conducting research in order to pick the best
   variation of a brand name, it is usually best to narrow down the
   range of brands. Thus, the number of combinatorial terms is highly likely
   to be too small for Slowcomb to be of any benefit.

3. Any situation where combinatorial operations must be performed on a source
   in which data is not individually and randomly addressable.

Other solutions, such as Python's ``itertools`` may be superior or necessary
under these circumstances.

Caveats
=======
The documentation in the code, and this introduction has not been thoroughly
proof-read, and may contain errors.

Please report all errors by filing issues. As usual, please be specific about
bugs, and include detailed steps to reproduce the bug. Unit tests would also be
nice. For errors in the documentation, please quote the line number (and column
number if possible) as well as the file where you found the error.

Wishlist
========
Slowcomb is largely a labour of love, and very much a learning journal of
Python programming (and using GTK via PyGObject for the demos).
The possibility that this library might be useful enough to be used in other
projects is being explored. Here are some ideas:

Specific Ideas (toward 1.2)
***************************

Express wishlist (can be done by 2020-12-25) 🎄🎅 
#################################################
* Consolidate all essential components of Slowcomb into the ``slowcomb``
  module, and make ``slowseq`` completely optional.

* Fix excess memory usage issue in the term derivation routine in 
  ``Permutation``, especially when it is used as the root of a compound CU.


Not-so-specific Ideas (toward 2.0)
**********************************
These are just ideas which are not specific enough to have a deadline:

Code and Documentation Quality
##############################
* Further reduce word count and increase clarity in docstrings to the point
  it becomes a good example for teaching programming to (tenth?) grade school
  students.

* Improve dependency injection use patterns to make unit testing easier.

Demos
#####
More demos to illustrate Slowcomb's potential use cases would be nice to have.

* Combinatorial Test Suite - an extended test suite for the Slowcomb library
  which would take too long to write manually.

* Combinatorial Text Editor - a tool that incorporates combinatorics in 
  generating text documents, such as configuration files or experimental
  writing works.

* Demo App Improvements

  - Implement the GTK Application API in the demo app. This allows Ctrl-key
    shortcuts to be used. The current demo app has nigh exhausted all available
    Alt-key shortcuts.

  - Implement a more intuitive Editor. The current tabular tree view is
    somewhat serviceable, but was found to be hard to read at times.

* Test Planner - a user-friendly app that would generate a list of unit tests
  to be performed, and even keep track of them and generate template code.

Features and Additional CUs
###########################
* ``ChainSequence``, addressable version of ``itertools.chain``.
  
  - The ``__add__()`` and ``__sub__()`` (if feasible) methods for runtime
    modification of ``ChainSequences``

* ``CombinationWithExclusion``, which is basically ``Combinations``, but with
  the ability to exclude specific elements (e.g. Drug A and Drug C should never
  appear in the same prescription)

* Exception memory to help isolate and diagnose problems in compound CUs. 
  The unused ``_exceptions`` property in ``CombinatorialUnit`` is reserved
  for this feature.
 
* Extended unit and integration tests:

  - Detailed unit tests, to account for edge cases, corner cases and
    circular recursion errors.

  - Detailed performance tests based on access patterns to investigate
    potential optimisations to reduce the time needed to generate terms.

  - Exception handling tests, to ensure users get the right error messages,
    and appropriate fallback paths are available.

* ``FilteredSNOBSequence``, a sequence of numbers with a fixed length and
  number of active bits, but with the ability to set specific bits to stay
  on or off.

* Management features to help with consolidating or expanding CUs:

  - The ``__contains__()`` method, which finds out if a CU contains all the
    terms of another.
  
  - A method to find out the indices of terms of one CU *A* in another *B*,
    if *B* has some or all of *A*'s terms.

  - A method to find out which terms are present in two CUs.

Performance Optimisations
#########################
* ``DequeCacheableSequence``, a cache that keeps a fixed number of the most
  recent results.

* Memory usage profiling.
   
  - A method to accurately measure the memory footprint of a CU when it is
    not in use, through ``__sizeof__()``.

* Optimised codepaths for the following types of situations:

  - Permutations where the terms are just minor variations of the source
    sequence. Memory access and usage can be minimised by performing as
    much of the combinatorial process as possible in-place.

  - High-likelihood repetitions of elements in combinations and permutations.

  - Small-n, big-r applications of CUs with repeating elements.

* Optimisations for potential uses in highly-parallel workflows, especially
  as a work dispatch system.

Miscellaneous
#############
* Easter eggs??  

