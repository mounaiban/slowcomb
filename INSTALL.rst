Installing and Using Slowcomb for Virgins
-----------------------------------------

  For information on contributing to the slowcomb project, please see
  ``CONTRIBUTING.rst``

Due to its minimal dependency footprint (only Python built-in libraries
are linked), slowcomb is easy to set up for use in your projects and 
hopefully difficult to mess up with.

If you are already fairly experienced with Python software development
in a Git-managed environment, and you use virtual environments regularly,
you can stop reading this file and start coding, as you probably already
know what you're doing, unless you want to join in the fun.

  Note: The advice given herein is rather Unix-focused, as the author
  uses this library mostly on Linux and macOS systems. The procedures
  on Windows should not be too different, apart from differences in 
  path formats (e.g. ``/home`` vs ``C:\Users``) and command line
  interfaces (e.g. ``ls`` vs ``dir``).  Windows 10 users have the
  rather compelling *Windows Subsystem for Linux* option, which supports
  a legit Linux system.

The installation and usage process endorsed here is basically:

  1. Clone slowcomb using the ``git clone`` command.

  2. Run unit tests with ``python3 -m unittest discover -s slowcomb/tests``
     in the repository root directory (same directory where you see the
     ``README.rst`` and ``LICENSE`` files.

  3. Prepare a virtual environment, install the package generated in
     step 3 above in your virtual environment using ``pip``.
     
     * Alternatively, the package may be installed system-wide, also
       using ``pip``.

  4. Generate a package by running ``setup.py``.

  5. Import the ``slowcomb.slowcomb`` module, or parts of it, into the 
     modules of your project.

     * Alternatively, import ``slowcomb.slowcomb`` while in the
       interactive Python shell, or ``slowcomb.tests.manual`` if you
       want to mess around...

  6. Goto step 4 above to update the slowcomb modules in your project
     when changes are pushed to the repo.

Step 1: Clone This Thing
========================
Prepare a directory on the file system of your working (virtual) machine.
If you have a special directory set aside for checkouts from source
control repositories, such as a ``downloads-github`` directory (or
*GitHub Downloads* for you Windows folks), just switch to it and clone
this repository there with the usual ``git clone`` command:

::
    git clone https://github.com/mounaiban/slowcomb
    
A few messages later, you should now have a copy of slowcomb in your
directory. It should be in a ``slowcomb`` subdirectory from the
directory you ran the above ``git clone`` command in.

Step 2: Run Tests and Familiarise Yourself With the Repo
========================================================
Slowcomb's project tree is extremely simple and nearly impossible to
get lost in, but it is worth saying that main modules live in the
``slowcomb`` subdirectory, and unit tests live in ``slowcomb/tests``.

To run the unit tests, stay in the slowcomb repo root (i.e. the same
folder as the ``README.rst`` and ``LICENSE`` files), and run this command:

::
    python3 -m unittest discover -s slowcomb/tests

  PROTIP: On many systems merely running ``python`` invokes a Python 2
  interpreter. However, the Python slowcomb was written is its largely
  incompatible successor, Python 3. This is why you have to run
  ``python3`` instead or the command will not succeed. Hopefully, by
  the time you read this, Python 3 would have become the default
  Python.

This runs the built-in ``unittest`` module, which is executable, and
tells it where the tests are.

Note that some of the tests have been skipped (there are about 18 of
them at this time for this official version), this is normal. A number
of the tests are that slow-running and take hours to complete have been
excluded from the test runner by default.

Step 3: Package
===============
In order to use slowcomb with your projects, you would have to either:

1. Install it with the other Python library modules on your system or 
   your Python Virtual Envrionment, or, heaven forbid,
    
2. Copy the library files into your project tree. Only do this if you
   know what you are doing, and/or just don't care...

The first option is recommended in most cases, as it is the smoothest
known workflow that allows the least effortful method of incorporating
the latest updates to the library into your project. But before you
can formally install it in your envrionment, you have to generate a
package using the setup script in the repo root, where the
``setup.py`` file is:

::
    python3 -m setup.py sdist

When all goes well, the ready-to-install package should appear in the
``dist`` subdirectory of the repo root. There may be multiple files
of the same prefix with a timestamp, like:

::
    ``slowcomb-0.x.dev.2019-09-09T09-09-09.999999.tar.gz

Note the path to the directory.

  PROTIP: If you are using ``bash``, or any other Unix shell, navigating
  to the directory and using the ``pwd`` command there will reveal the
  full path to that directory. As always, when in doubt, press Tab when
  composing your command.

What's In That Name?
********************
The first part of the filename tells you that it's a slowcomb package
and what version it is, while the ``dev`` means 'development', to
indicate that it's a package that you have generated on your system.
The last parts of the filename is the exact time ``setup.py`` was
invoked down to the microsecond (plus a few microseconds), and the
``.tar.gz`` suffix just tells you that the files are Unix Tape Archives
with gzip compression applied.

Each time you run ``setup.py``\*, a new file will be created. Unless you
are fixing a regression, you would use the archive with the latest
time stamp.

 \* A more accurate description would be 'each time you run ``setup.py``
 within the same microsecond'. I hope to live long enough to see computers 
 get so fast, that the entire package generation can finish in under a
 microsecond.

Step 4: Install
===============
With the full path to the ``dist`` subdirectory under the repo root in
mind, enter a virtual environment (venv) of your choice. If you are just
getting started with venv's, create one by first navigating to a directory
which you want to place the venv, and type:

::
    python3 -m venv my-first-venv

Substitute ``my-first-venv`` for a name you find to be more useful. A
directory with the name you chose will be created. Find out more about
venv's in the Python Tutorial, Chapter 12, *Virtual Environments and
Packages*.

 PROTIP: Note that virtual environments are started in a clean state
 with no packages, and installing slowcomb in the venv will only make it
 available in that particular venv. This is intentional, as it prevents
 an amateur-made library from messing up with your system-wide copy of
 Python.

If you have everything already started, you may get on with it and 
activate your venv. Either run ``source bin/activate`` from the venv
directory, or use your preferred alternative method.

 Note: The above steps may be skipped if you want to install slowcomb
 system-wide. This is not recommended for beginners, but experts are
 welcome to face the risks of doing it this way.

Once inside your venv, install slowcomb by issuing the pip command with
the path to the package generated in Step 3 above. On a ``bash`` terminal 
on a Unix-compatible system, the command may look like:

::
    pip3 install /home/mrtooliteral/downloads-github/slowcomb/dist/\
    slowcomb-0.x.dev.2019-09-09T09-09-09.999999.tar.gz

With the exact path before ``/dist/`` altered to suit your filesystem,
and the exact name of the archive changed to match the one that's
actually on your filesystem.

 Note that the backslash (\) character is only present to allow the
 example to be shown in two lines and still be correct. It may be removed.

A successful installation will be indicated by a message that looks like:

::
    Successfully installed slowcomb-0.x.dev.2019-09-09T09-09-09.999999

Pause to smell the victory. It's good for your soul.

Step 5: Hack
============
Slowcomb is now installed and ready for use. Either import it in your
own code to start using it, or mess with it in the Python interactive
shell.

Using It in Your Code
*********************
Import from the following modules:

* ``slowcomb.slowcomb`` for the main combinatorics classes,

* ``slowcomb.slowseq`` for the supporting sequence classes.

Look inside the ``slowcomb.py`` and ``slowseq.py`` modules in the
``slowcomb`` directory to find out the names of the classes you can use.

Playing Around With It in the Python Shell
******************************************
Once you have started the Python shell, type this to get started:

::
    from slowcomb.slowcomb import *
    from slowcomb.slowseq import *

Alternatively, the Manual Testing Environment has some mini-examples
set up during the course of the development of slowcomb. To get started,
just type:

::
    from slowcomb.tests.manual import *

If you see a welcome message, you are all set! For your convenience
most of the test objects have a prefix of ``test_``, so that you can
use the Tab key autocomplete feature to find them.

