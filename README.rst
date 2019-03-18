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
aiming for an O log(n) time complexity when looking up a combinatorial
subset.

*Slowcomb is free software, licensed to you under the Terms of the GNU
General Public License, Version 3.*

Also, I Am Not A Mathematician.

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
to refer to "cant_break_this_123" or "iSointoyou" than say, "password
#471" or "brand 2 variation A".

2. The combinatorial process is a performance-critical part of your 
workflow. While detailed performance studies have not been conducted at
this stage, the rate of operations is expected to be significantly
inferior to alternatives (and competitors!). This is due to the fact
combinatorial operations in this library are multi-stage processes that
involve rebuilding every combinatorial result. This involves multiple
memory accesses per result. A fast library is one that can derive
combinatorial results with a minimum of memory accesses.

3. The combinatorial process is a space-critical part of your workflow.
Despite efforts in attempting to minimise memory use, the addressability
features will always incur a memory overhead.

4. You have a combinatorial operation where the n and r factors are
most of the time either:

    a. Very close, or your selections are not much larger or smaller
    than the pool of elements to work from. In these cases, targeted
    deletions and in-memory swaps of elements are probably more
    efficient, but Slowcomb doesn't use them.

    b. Very small. It may be faster to expand them onto a list,
    dictionary, or even a tuple, while still not using much more
    memory.

    c. Such that r is much larger than n. This means the combinatorial
    results involve a lot of repetition of the source elements, which
    is arguably more efficiently done using block memory copies, which
    Slowcomb doesn't use.

Caveats
=======
The documentation in the code, and this introduction has not been
thoroughly proof-read, and may contain errors.

Please report all errors by filing issues. As usual, please be specific.

Wishlist
========
While the basic concept is pretty much done, I still think there is
some more work to be done to make slowcomb much more useful than it is
right now...

Short Term (by 2019-12-25)
**************************
* Addressability: index(), and __contains__(). This allows you to find
out if a sequence is a possible output of one of the combinatorial
operations, and if it is, what the index is.
* Reporting Tools, Stage 1: __repr__() and __str__(), maybe JSON export,
so that you can export information vital to reproducing setups.
* Documentation: reviews and cleanups
* Testing: Cleanup of plan.py, slowcomb vs. itertools performance tests.
* API Stability: Make up my mind about argument, attribute and method
names.

Long Term (indefinite schedule)
*******************************
* Combinatorics features (subject to change):
    * ChainSequence, addressable version of itertools.chain, with
    __add__()
    * FilteredSNOBSequence, same number of bits, but with some bits
    stuck on or off.
    * CombinationWithExclusion, or some variation of, supported by
    FilteredSNOBSequence
* Examples: demos (that will hopefully become useful in their own right)
* Exceptions: more exception handling, make is_valid() useful
* Peformance:
    * __sizeof__(), to monitor memory consumption
    * DequeCacheableSequence, a cache that keeps a fixed number of
    results
* Testing: even more unit tests, detailed performance tests.
* Refactoring: improve the way dependency injection is used, so that
the library is easier to unit-test, and also to make things easier for
you, the Hacker, to (re-)implement your own features.
* Reporting Tools, Stage 2 and Beyond: visualisations, definite JSON
export features.
* More easter eggs??

