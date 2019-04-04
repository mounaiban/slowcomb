Slow Combinatorics in Python (slowcomb)
---------------------------------------

*A Mounaiban mini-project*

What is Slowcomb?
=================
Slowcomb is a mini-library of combinatorics classes for the Python programming
language and platform, implementing two of the most common combinatorics 
operations: permutations and combinations (and their variations).

Slowcomb implements its classes as sequences, allowing the results of these
operations to be recalled instantly with integer indices, as shown in this
example:  

::

    >>> source = ('A', 'B', 'C', 'D')
    >>> perm_abcd = Permutation(source, r=4)
    >>> perm_abcd[11]
    ('B', 'D', 'C', 'A')

The 12th (or first+11'th) possible way of rearranging the letters
``A, B, C, D`` is ``B, D, C, A``, when using the canoncial method of
permutation seen in school mathematics textbooks, that is, considering all 
possible ways of switching the letters in order, from right to left.

Slowcomb's combinatorial operations work only with qualified sequence types,
or any container with elements addressable with integer indices, such as 
tuples and lists.

Slicing on the combinatorial unit is also supported:

::

    >>> perm_abcd[5:9]
    (('A', 'D', 'C', 'B'), ('B', 'A', 'C', 'D'), ('B', 'A', 'D', 'C'),
    ('B', 'C', 'A', 'D'))

The terms returned in an outer tuple are the sixth, seventh, eighth and ninth
permutations respectively

  PROTIP: first index of a sequence is 0.

You can find out the number of permutations using the ``len()`` function:

::

    >>> len(perm_abcd)
    24

As indicated, there are twenty-four possible ways four elements may be
arranged.

Where it may be useful, and where the source sequence of the combinatorial
unit supports it, the index of a combinatorial result can be recalled:

::

    >>> perm_abcd.index( ('D','C','B','A') )
    23

The source sequence used in this example is a tuple, which supports index
reverse lookups. Some sources may not support this; in such cases, the 
``index()`` method will not succeed.

  PROTIP: When working with strings, remember to separate its characters
  into individual elements of a tuple (or any other sequence).

As expected, ``D, C, B, A`` is reported to be the twenty-fourth and last
permutation of ``A, B, C, D``.

  PROTIP: Recall from maths class that the final permutation of a sequence
  is the sequence in reverse order.

All combinatorial operations in Slowcomb are 'lazy'; results are only
evaluated when requested.

At time of publication, this way of using permutations and combinations
are not supported by Python's built-in classes in ``itertools``. The 
creation of Slowcomb was motivated by the need for such functionality
in another unpublished game engine project.

*Slowcomb is free software, licensed to you under the Terms of the GNU
General Public License, Version 3 or later. Please view the LICENSE file
for full terms and conditions.*

Also, I Am Not A Mathematician.

How Do I Get Started Using It?
==============================
Please see the ``INSTALL.rst`` file in the repository root directory.

When To Use It
==============
The expected benefits of using Slowcomb for combinatorial operations include
repeatibility and reproducibility, short access time to specific results,
and reduced memory requirements.

Slowcomb is intended for use in applications which make extensive use
of combinatorics where:

1. You need to be able to reproduce combinatorial operations (e.g. testing),

2. Your combinatorial results cannot be expressed easily in their literal
   forms (e.g. design variations),

3. You need fast access to just a few different combinatorial results at
   a time from a source with a very large number of elements, yet cannot
   predict ahead of time which ones you need, or

4. You are working with combinatorial operations whose results take up 
   unreasonable amounts of memory, but can be deterministically reproduced
   in a reasonable amount of time (e.g. some games that feature procedurally-
   created content).


When Not To Use It
==================
Slowcomb has several identified weaknesses, namely its slowness in generating
successive results (hence its name), lack of proven reliability and performance
in massively parallel workflows, and inability to work on so-called 
*non-subscriptable* sources whose elements cannot be individually addressed
(such as generators and iterators).

Here are some circumstances where there is no expected benefit using Slowcomb:

1. The combinatorial results are conveniently represented by their literal
   form (e.g. generated passwords and brand names). It may be more practical
   to store the results.

2. You need to work with a large number of successive combinatorial results
   (e.g. first 10 million combinations). Python's ``itertools`` are a lot
   more adept in this type of operation.
  
3. Your workflow involves a large number of combinatorial units working
   in parallel (e.g. 50,000 simultaneous permutators). Slowcomb was not
   really tested for use in the inner parts of a massively-parallel
   workflow. You may need a more specialised library or framework for
   better performance.

4. You work with combinatorial operations that involve small selections
   from a source with a small number of items. Using tuples or 
   ``frozensets`` containing precomputed results generated using
   ``itertools`` may be much faster.

5. You work with combinatorial operations which involve a lot of 
   repetitions of elements in the source. Slowcomb reconstructs every term
   from scratch, element-by-element, missing many opportunities for
   optimisation in this type of operation. Improving performance for such
   operations is part of the Long Term goals in Slowcomb's development.

6. Your combinatorial results tend to be mostly minor variations of the
   source sequence. The weaknesses identified in circumstance 5 above,
   and the plans to address them, also apply.

7. You need to work on sources that do not have a practical way of
   supporting addressing of its contents by numerical indices.

Other solutions, such as Python's ``itertools`` may be sufficient or even
superior under these circumstances.

Caveats
=======
The documentation in the code, and this introduction has not been
thoroughly proof-read, and may contain errors.

Please report all errors by filing issues. As usual, please be specific
about bugs, and include detailed steps to reproduce the bug. Unit tests
would also be nice. For errors in the documentation, please quote the
line number (and column number if possible) as well as the file where
you found the error.

Wishlist
========
While the basic concept is pretty much done, I still think there is
some more work to be done to make slowcomb much more useful than it is
right now...

Short Term (by 2019-12-25🎄)
****************************
These goals aim to make Slowcomb usable for small-scale projects, with a
codebase clear enough to be used as a teaching aid for beginners to Python
and object-oriented programming.

The version number will be bumped to **1.0** upon completion of most of these
goals.

API
###
* Decide on final argument, attribute and method names. Names should be as 
  intuitive and clear as possible. Using names borrowed from other famous 
  projects or Python built-ins for completely different purposes is to be
  avoided.

Documentation
#############
* Reorganise docstrings for easier reading when using ``help()`` from the
  Python interpreter in interactive mode.
  
* Use correct reStructuredText formatting for easier reading for those who
  prefer to use HTML renders of docstrings.

* Improve consistency in use of terminology, choose terms in order to avoid
  confusion with similar or identical words used in Python and other famous
  projects. The aim is to stick with a tenth-year school vocabulary while
  reserving more advanced and technical terms for the most appropriate
  contexts. 

Management
##########
* Provide a graceful way of indicating if ``index()`` is available on a
  combinatorial sequence or not. The ``index()`` method is only supported
  on sequences that implement it. Complex setups which involve multiple
  levels of combinatorial sequences (e.g. permutation of combinations)
  may include sources that do not support ``index()``. A method to find
  out the parts of a combinatorial chain that do not support ``index()``
  will be useful.

Testing
#######
* Create a more user-friendly Test Planner. The current ``plan.py`` isn't
  exactly *Fit for Public Use*.

* Performance Tests, Second Edition: implement comparative performance
  tests to compare Slowcomb with ``itertools`` combinatorics across
  different source sequence (n-values) and selection sizes (r-values),
  as well as cache-based mitigations against slowness.


Long Term (indefinite schedule)
*******************************
These goals prepare Slowcomb for deeper involvement in software projects,
and also aim to make the project easier to work on with others in a
distributed, collaborative setting.

Completion of these goals will advance the version number towards **2.0**.

Demos
#####
There is a current lack of demos to illustrate Slowcomb's potential use cases.
A few good examples would be nice to have.

Combinatorics, Sequences and Supporting Features
################################################
* ``CombinationWithExclusion``, which is basically combinations with specific
  patterns excluded (e.g. Drug A and Drug C should never appear in the same
  prescription)
 
  - This may require a supporting class in the same vein as
    ``FilteredSNOBSequence``

* ``ChainSequence``, addressable version of ``itertools.chain``.
  
  - The ``__add__()`` and ``__sub__()`` (if feasible) methods for runtime
    modification of ``ChainSequences``
 
* ``FilteredSNOBSequence``, same number of bits, but with the ability to set
  specific bits to stay on or off.

* Testing: even more unit tests, detailed performance and exception handling
  tests.

  - Detailed unit tests, to account for edge cases, corner cases and
    circular recursion errors.

  - Detailed performance tests based on access patterns to investigate
    potential optimisations to reduce the time needed to generate terms.

  - Exception handling tests, to ensure users get the right error messages,
    and appropriate fallback paths are available.

Management
##########
* Inclusion and intersect tests, which can help in consolidating combinatorial
  sequences.

  - The ``__contains__()`` method, which finds out if a combinatorics sequence
    is completely covered by another.
  
  - A method to find out which terms are present in both of two
  ``Combinatorics`` sequences being compared.

* Reporting Tools, Stage 2 and Beyond -- these features are intended to aid
  with the replication of combinatorial setups, but it remains to be seen if
  this responsibility is better handled by a separate project or the 
  application using Slowcomb.
  
  * JSON export

  * Visualisations
  

Performance
###########
* ``DequeCacheableSequence``, a cache that keeps a fixed number of the most
  recent results.

* Implement ``__sizeof__()`` in combinatorics and sequence classes, to provide
  accurate feedback on memory consumption
 
* Explore optimisations which can speed up combinatorial operations where:

  - The resulting terms are similar to the source sequence (e.g. permutations
    with minor differences).

  - Results of small-n, big-r operations (e.g. repeats-permitted combinations
    with large blocks of repeated elements).

* Investigate if using ``__slots__`` improves performance.

Even in Slowcomb, speed matters!

Reliability
###########
* Implement Exception memory in combinatorics and supporting sequences, in
  order to help isolate and diagnose problematic sequences.

Architecture
############
* Refactor the codebase to improve the way dependency injection is used,
  in order to make unit testing easier, which in turn should make testing
  and implementation of new ideas and features quicker and easier. 

* Investigate the potential benefits (or lack of thereof) of basing the
  combinatorial classes on a Set Type instead.

Miscellaneous
#############
* More easter eggs??

