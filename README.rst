Slow Combinatorics in Python (slowcomb)
---------------------------------------

A Mounaiban mini-project.

What is slowcomb?
=================
Slowcomb is a mini-library of combinatorics classes, each one attempting
to implement the two major combinatorics operations, permutations and
combinations, and their variations, using an approach which makes the
results of these operations addressable.

These classes are implemented as sequences, allowing the results to be
systematically enumerated and instantly accessed with integer and slice
indices, just as seen on tuples, lists or arrays.

Its aim is to make combinations and permutations instantly repeatable,
aiming for an *O log(n)* time complexity when looking up a combinatorial
subset.

*Slowcomb is free software, licensed to you under the Terms of the GNU
General Public License, Version 3 or later. Please view the LICENSE file
for full terms and conditions.*

Also, I Am Not A Mathematician.

How To Use It
=============
Please see the ``INSTALL.rst`` file in the repository root directory.

When To Use It
==============
Slowcomb is intended for use in applications which make extensive use
of combinatorics where:

1. You need to address and repeat combinatorial results and operations
   (e.g. repeating a problematic or favoured configuration, or retaining
   a specific game world state).

2. Your combinatorial results are not easily named by its literal form
   (e.g. colour schemes, other graphic or fashion design variations,
   scenario variations in games and visual novels).

3. You have a big-n, small-r situation where you have to make a
   comparatively small selection from a large pool of elements.

4. The combinatorial results take up significant amounts of memory,
   yet can be deterinistically rebuilt from scratch when needed in a
   reasonable amount of time.

When Not To Use It
==================
Other solutions, such as Python's itertools may be sufficient or even
superior if:

1. The combinatorial results are better represented by their literal
   form, such as passwords and brand names. For example, it is more useful
   to refer to ``cant_break_this_123`` or *iSointoyou* than say, "password
   #471" or "brand 2 variation A".

2. The combinatorial process is a performance-critical part of your 
   workflow. While detailed performance studies have not been conducted at
   this stage, the rate of operations is expected to be significantly
   inferior to alternatives (and competitors!).
  
3. The combinatorial process is a space-critical part of your workflow.
   Despite efforts in attempting to minimise memory use, the 
   addressability features will always incur a memory overhead.

4. You have a combinatorial operation where the n and r factors are
   most of the time either:

   a. Very small. It may be faster to expand them onto a list,
      dictionary, or even a tuple, while still not using much more
      memory.

   b. Such that r is much larger than n. This means the combinatorial
      results involve a lot of repetition of the source elements, which
      is arguably more efficiently done using block memory copies, which
      slowcomb doesn't use.

5. Your combinatorial results tend to be mostly minor variations of the
   source sequence. In these cases, targeted deletions and in-memory swaps
   of elements are probably more efficient, but slowcomb doesn't use them.

Is It Really Slow?
==================
This library was branded as being slow, based on the expectation that
someone out there has a faster alternative, and also on the project's
initial focus on repeatability of results over speed.

Combinatorial operations in slowcomb are multi-stage processes that
involve figuring out the read order of a source sequence, then rebuilding
a new sequence using the said order to achieve the combinatorial result.
As you may already notice, this involves a lot of memory read and write
operations per result.

The performance penalty may not be great when you are making a small
selection from a big source pool of elements, or if the permutation is
remarkably different from the original pool. However, there is a lot of
opportunity for optimisation for other cases, of which slowcomb is not
made to take advantage of for the time being.
 
A fast library is one that can derive combinatorial results with highly-
optimised memory accesses. At the moment, slowcomb is not one of them.

 Note from Moses: Even if slowcomb ends up being much faster in the
 future, the name would likely remain unchanged, for nostalgic purposes.

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
* Review and reduce word count in docstrings in ``slowcomb`` and ``slowseq``.

* Reorganise docstrings for easier reading when using ``help()`` from the
  Python interpreter in interactive mode.
  
* Use correct reStructuredText formatting for easier reading for those who
  prefer to use HTML renders of docstrings.

* Improve consistency in use of terminology, choose terms in order to avoid
  confusion with similar or identical words used in Python and other famous
  projects. The aim is to stick with a tenth-year school vocabulary while
  reserving more advanced and technical terms for the most appropriate contexts. 

Testing
#######
* Create a more user-friendly Test Planner. The current ``plan.py`` isn't
  exactly *Fit for Public Use*.

* Consolidate test data, so the same specimens may be used in both manual
  and automatic testing.

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

* Testing: even more unit tests, detailed performance tests.

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

