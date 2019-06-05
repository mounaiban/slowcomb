Contributing to Slowcomb on GitHub for EXPERTS
----------------------------------------------
Wow! I'd never expect someone to be actually interested in contributing to,
let alone using the Slow Combinatorics Library, but here you are.

Slowcomb was intended to be some kind of personal learning journal in Python
programming (and a bit of a high school maths refresher), but if you are going
to be a force in taking this project beyond what it is right now, let me thank
you in advance for your interest in my little project, whatever the motivation,
as long as it is for the good of humankind.

Contributing to Slowcomb should not be too different from how it's done
with some of the major projects on GitHub, perhaps with only one real
difference: I am the sole authority on what gets pulled into master.😈

If you are a fairly seasoned developer who uses GitHub a lot, or has had
reasonable experience with other communities (e.g. GitLab, SourceForge),
you are likely familiar with the contribution process endorsed here already.
I hope you have a good time messing around, and may your contributions
become something to be proud of!

Cheers,

\- Moses

  For information on using slowcomb in another project, please see
  ``INSTALL.rst``

Executive Summary
-----------------
The process endorsed on this project is basically like:

1. Optionally, learn how to use Git and Virtual Environments (VE).
   You might have chosen to go with GitHub Desktop, or an IDE that
   handles VEs and packaging in one spot.

2. Optionally, set up a VE on your file system

3. Fork Slowcomb, thus creating your personal branch of the Slowcomb
   master branch.

4. Clone Slowcomb to your file system.

5. If using a VE, activate it.
  
6. Hack: play around as necessary, add your modifications, enhancements
   or bugfixes

7. Write and run Tests

8. If satisfied, commit your changes to your local Git repository,
   then push those changes to your branch on GitHub.

9. If interrupted by the need to make an urgent change which may
   affect an incomplete change, stash your work in progress. Then,
   pop your WIP back when you are done with the urgent edit.

10. When you feel ready, make a pull request to the master branch at
    https://github.com/mounaiban/slowcomb.

11. Pull *from* master to keep your other files up-to-date

12. Goto Step 4


Important Information
---------------------
Here are some clarifications about this project that have not been 
documented anywhere else:

Use of Directories
==================
* ``/`` - the repo root is only for important documents that everyone
  must read if they want to use or make contributions to this project,
  and scripts and specification files for preparing installation
  packages.

* ``/slowcomb`` - the source root (which maps to the ``slowcomb``
  namespace). Only used for the main modules ``slowcomb.py`` and 
  ``slowseq.py`` for now...

* ``/slowcomb/demos`` - runnable examples on how Slowcomb should (or 
  should not) be used, non-essential tests unrelated to operational
  correctness, such as performance benchmarks.

* ``/slowcomb/tests`` - essential unit tests that verify operational
  correctness; basically tests that indicate trouble when they fail,
  and must pass for a release to be deemed 'suitable for production use'.

Prefixes
========
Some module files may begin with specific words to indicate their purpose
and intended use.

* ``benchmark_`` - usually non-essential, *quantitative* performance and
  memory consumption tests that are placed in the ``/demos`` directory
  and run manually with commands like
  ``python -m slowcomb.demos.benchmark_whatever``.

* ``test_`` - **important** test modules intended to be run with Python's
  ``unittest`` test automation module; these are to be placed only in
  the ``/tests`` directory. By default, all tests in modules with this prefix
  will be run with the ``python -m unittest`` command.

* ``test_benchmark_`` - **important** benchmark modules intended to be run
  with Python's ``unittest`` module; these benchmarks are qualitative, with
  specific requirements such as *take no more than a second* or
  *no more than 2KB memory overhead per record*, with no regard for the
  quantitative measure (e.g. taking 0.005s is as good as taking 0.998s,
  as long as it is 1.00s or less). By default, all tests in modules with
  this prefix will be run with the ``python -m unittest`` command.

* ``xtest_`` - non-essential extra test modules intended for use with
  Python's ``unittest`` module that are allowed to fail on releases
  deemed 'suitable for production use'.
 
