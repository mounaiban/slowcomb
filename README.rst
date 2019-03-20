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

Short Term (by 2019-12-25)
**************************
* Addressability: ``index()``, and ``__contains__()``. This allows you to
  perform a reverse lookup to find out if a sequence is a possible output
  of a combinatorial class, and if it is, what its index is.

* Reporting Tools, Stage 1: ``__repr__()`` and ``__str__()``, maybe JSON
  export, so that you can export information vital to reproducing setups.

* Documentation: reviews and cleanups

* Testing: Cleanup of ``plan.py``, slowcomb vs. ``itertools`` performance
  tests.

* API Stability: Make up my mind about argument, attribute and method names.

The version number will be bumped to 1.0 upon completion of most of these
goals.

Long Term (indefinite schedule)
*******************************
* Combinatorics features (subject to change):

  - ``ChainSequence``, addressable version of ``itertools.chain``, with
    ``__add__()``
 
  - ``FilteredSNOBSequence``, same number of bits, but with some bits stuck 
    on or off.
 
  - ``CombinationWithExclusion``, or some variation of, supported by 
    ``FilteredSNOBSequence``

* Examples: demos (that will hopefully become useful in their own right)

* Exceptions: more exception handling, make ``is_valid()`` useful

* Peformance:

  - ``__sizeof__()``, to monitor memory consumption
 
  - ``DequeCacheableSequence``, a cache that keeps a fixed number of results

* Testing: even more unit tests, detailed performance tests.

* Refactoring: improve the way dependency injection is used, so that the
  library is easier to unit-test, and also to make things easier for you,
  the Hacker, to (re-)implement your own features.

* Reporting Tools, Stage 2 and Beyond: visualisations, definite JSON export
  features.

* More easter eggs??

