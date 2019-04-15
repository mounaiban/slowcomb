Installing and Using Slowcomb for Virgins
-----------------------------------------

Slowcomb should be easy to import into your project using industry-standard
procedures, due to its minimal dependency footprint; only Python built-in
libraries are linked. Importing the library from repository to project, in
the simplest of terms, is merely a matter of cloning, packaging and deploying.

  For information on contributing to the slowcomb project, please see
  ``CONTRIBUTING.rst``

If you are already fairly experienced with Python software development
in a Git-managed environment, and you use virtual environments regularly,
you can stop reading this file and start coding, as you probably already
know what you're doing, unless you want to join in the fun.

  Note for Windows Users: The advice given herein is rather Unix-focused,
  as the author used this library mostly on GNU/Linux and macOS systems.
  The procedures should not be too different on Windows, apart from
  fundamental differences such as path formats (e.g. ``/home``, as opposed
  to ``C:\Users``) and command line interfaces (e.g. ``ls`` vs ``dir``).

  PROTIP: Windows 10 users have the rather compelling *Windows Subsystem
  for Linux* option, which supports a legit GNU/Linux system.

Summary
-------
The installation and usage process endorsed here is basically:

1. Clone slowcomb using the ``git clone`` command.

2. Optionally, prepare the virtual environment.

3. Optionally, run unit tests by invoking from the repo root:
   
   ::

      python -m unittest

   This will ensure that you are not importing a build with known
   issues.

4. Generate a package by running ``python setup.py`` from the repo root.
   The installation package file should appear in the ``dist`` directory
   from here.

   PROTIP: The packages are generated using ``setuptools`` and should 
   end with ``.tar.gz``.
   
5. Install Slowcomb to your system or virtual environment, using
   ``pip $YOUR_SLOWCOMB_REPO/dist/$YOUR_ARCHIVE``, substituting:
   
   * ``$YOUR_SLOWCOMB_REPO`` for the path to the repo root,

   * ``$YOUR_ARCHIVE`` for the actual name of the package file.

6. Import the ``slowcomb.slowcomb`` module, or parts of it, into the 
   modules of your project.

   * Alternatively, import ``slowcomb.slowcomb`` while in the
     interactive Python shell, or ``slowcomb.tests.manual`` if you
     want to mess around...

7. When changes are made to Slowcomb, pull them into your local repo
   with ``git pull`` from any directory on or under the repo root, then
   repeat the process from Step 2.

Installation In More Detail
---------------------------

Step 1: Clone This Thing
========================
Prepare a directory on the file system you are working on.

If you have a special directory set aside for Git repositories (or 
'checkouts' other source control systems), just switch to it and clone
this repository there with the ``git clone`` command:

::

   git clone https://github.com/mounaiban/slowcomb
 
A few messages later, you should now have a copy of slowcomb in your
directory. It should be in a ``slowcomb`` subdirectory from the
directory you ran the above ``git clone`` command in.

A Word on Words: a Mini Glossary
********************************
From this point on, the following terms are going to be used liberally:
  
* *file system*, the storage space on the system you are working on, when
  organised into files and directories. This is to avoid using language-
  and implementation-specific terms such as *hard disk*, *SSD*, 
  *virtual machine*, *laptop* or even *computer*, and stuff like that.

* *pull*, to apply changes from a copy, or branch, of a repository to
  another. 

* *repo root*, or Repository Root, the area in the file system that 
  contains the first level of the Slowcomb library repository's 
  directory . In the simplest terms, the same directory you find
  ``README.rst`` and ``setup.py`` in.

* *source root*, the area of the file system in which you may find
  Slowcomb-related material. In the simplest terms, it's the same
  directory that you may find ``slowcomb.py`` and ``slowseq.py`` in.
  Relative to the *repo root*, it is in the ``slowcomb/`` directory.

* *VE*, or *Virtual Environment*. An optional feature that allows you to
  create and maintain multiple copies of a Python environment, each
  with its own packages and modifications, and to prevent early updates
  or accidental uninstallations from causing software to stop working.
  
   VEs are used for maintaining continuity on enterprise systems or
   web servers, when running software certified to run only on specific
   versions of Python, or other modules, earlier than the latest, without
   holding back the rest of the system from potentially important updates.

* *VE root*, the first level of the area in the file system which
  contains the files for supporting a VE. In the simplest terms, it's
  the directory where you find the ``bin``, ``include`` and ``lib``
  sub-directories.

Why am I doing this?
********************
Cloning from GitHub with Git is the preferred way of downloading source
code. Minor changes on the repository may be applied without having to
download a newer version of an archive, eliminating the need to manage
an entire history of archive files. Changes may be reviewed using the
``git log`` command.

These are just two of the many features exclusive to using Git. If you
dive deeper, you might find out how to revert any file on your personal
copy of the repo to an older version while keeping the other files
intact. You could use the *bisect* feature to quickly find changes that
introduced a bug you are diagnosing.

There are hundreds of features, one for practically almost every possible
situation a hacker could be in.

Do I have to do this?
*********************
No. Alternative installation methods exist. Read on...

What else can I use ?
*********************
* **ZIP dumps.** You can download the entire repo in a ZIP archive.
  From the repo root on the GitHub website, press the green 'Clone
  or Download' button. In the pop-up box that appears, use the Download
  ZIP link that appears. Save the ZIP file to a safe place on you file
  system, and unpack the contents into the subdirectory there.

  Everything will work same way like in the good 'ole days, but you may
  be missing out on features such as the log and incremental updates.

* **Git front ends.** GitHub has its own original front end, the GitHub
  Desktop, downloadable from https://desktop.github.com. A 2012 release 
  of this app was all the author has used in the way of Git front
  ends before he decided take the command line path, so you are pretty
  much on your own if you go down this way. Godspeed!

* **Subversion**, or SVN. If you are even thinking about using it,
  I am going to assume that you are a veteran who is far more qualified
  to talk about it than I am.
  
  PROTIP: For those who missed out the crazy MySpace days of the Internet,
  SVN is a centralised source control system that had the level of
  influence of Git at time of writing. GitHub maintains SVN support,
  and there are long-running projects out there still using it, such as
  the Apache HTTP Server.


Step 2: Prepare the VE (Optional)
=================================
As mentioned earlier, Virtual Environments (VEs) are a means of managing
multiple Python runtime envrionments, usually to avoid the need to modify
the system-level runtime and the risks associated with doing so.

To create a virtual environment, find a suitable location on your file
system. The VE will be hosted in a subdirectory at this location.

  Windows Users: please refer to the Python Documentation, under
  the section `venv - Creation of Virtual Environments <https://docs.python3.org/3/library/venv.html>`_
  for Windows-equivalent instructions.

If you are using a UNIX shell, use the following command to create a VE
in the working directory:

::

  python3 -m venv $ENVY

Substituting ``$ENVY`` for the name of the VE, which is also the name of
the subdirectory.

  PROTIP: use under_scores, instead of hy-phens or ``s p a c e s``, in the
  name of the VE. You will be glad you did, as the latter two punctuations
  are not allowed in names in Python (see part 2.3 of the Python Language
  Reference).
  
Once you have created a VE, you will have to activate it to use it, by
invoking:

::

   source bin/activate

from the VE root. The ``activate`` part of the command is actually a
shell script, but written in a format which is only runnable using the
``source`` command.

  NOTE: You can actually activate the VE from outside the VE root,
  just make adjustments to the path, and be aware which VE you
  are activating!

When successfully activated, the prompt will look like:

::

   (venvy) [urname@urhost venvy]$

Where ``venvy`` is replaced by the actual name you used for your VE.

Once the VE is activated, you will be using the VE's embedded runtime
instead of your system-wide runtime. The following rules will apply:

* Packages installed on the system-level Python runtime will not be
  available to the VE. They must be installed again.
  
* Packages installed in the VE are not available to other VEs and
  the system.

* Updates applied in the VE will not apply anywhere else.

* The default Python will be independent from any other VE and the
  system. If using the numberless ``python`` command activates
  Python 2.7 on your system-level runtime, you can configure your
  VE to run the latest Python 3 runtime from the same command without
  affecting anything else outside the VE.

To leave the VE, just invoke the ``deactivate`` command.

Do I Have to do this?
*********************
No. VEs are completely optional. However, it is a good habit to maintain
separate VEs for playing around with random bits of code.

While Slowcomb is hardly able to make system-wide changes (unless you are
running a top-secret Python app that is also named ``slowcomb``), the same
cannot be said for other software that *do* make such changes.

Many publicly-available apps out there are written to deal with changes
to the Python runtimes and dependencies. However, you may be using
software that may not be built with such cross-version compatibility
in mind that are particularly susceptible to problems when dependencies
and runtimes change.

VEs can help to mitigate such risks of breaking other software on the 
system due to changes to the runtimes and packages.


How else can I do this?
***********************
You can skip using VEs altogether, and install Slowcomb on your system-wide
Python runtime. Just remember to put a ``3`` where it's needed!

  PROTIP: On many systems merely running ``python`` invokes a Python 2
  interpreter. However, Slowcomb was written for its largely
  incompatible successor, Python 3, which is in at time of writing.
  This is when you have to run ``python3`` instead or the test or
  command will not succeed.

  The same applies to the pip package manager, run ``pip3`` to install
  pip packages on the Python 3 runtime. As running ``pip`` will only
  manage Python 2 packages on these systems.

  This problem is not expected on VEs created using Python 3.

  Hopefully, by the time you read this, the Pythonistas would have
  fulfilled their 2020-1-1 promise to drop Python 2, and make Python 3
  the default Python on all newer systems.

Other solutions for managing VEs exist:

* **pipenv**. A third-party VE manager which aims to address VE-related 
  usability and security issues by combining VE and package management
  into a single tool, and throwing in some added integrity and security
  measures.

* **virtualenv**. A more advanced version of the built-int ``venv``
  module.

* **Use your IDE.** Some Integrated Development Environments, such as
  JetBrains' PyCharm feature built-in VE management tools, and are able
  to create them and switch between them on the fly.


Step 3: Run the Unit Tests (Optional)
=====================================
To run the unit tests, navigate to the the repo root and simply run:

::

    python -m unittest 

This runs the executable built-in ``unittest`` module, which will home
in on all modules that begin with ``test_*`` and attempt to run anything
that looks like a unit test, and then report its result.

You should see something like this on your terminal:

::

   ......................................................................
   .................................................. 
   --------------------------------------------------------------
   Ran 120 tests in 0.0022s

   OK


When you see nothing but dots (save for an occassional ``s``), and an
``OK``, it means all tests that matter have passed. Each dot you see
represents a test that has passed. 

If you see a lowercase ``s``, it indicates a skipped test. These tests are
usually expected failures, usually due to an issue that is not expected to
affect normal operation, but is still important enough to warrant action in
the foreseeable future.

Anything else is trouble. Check the Issues section in the Slowcomb
repo on GitHub, and file a report if you cannot find any prior reported
cases of the same issue, especially if it affects you.
 
Do I have to do this?
*********************
Not at all, you can skip running the test, but why would you want to not
be sure that the build you have is working fine, and be sure that any issue
caused by Slowcomb bugs are not your fault?


Step 4: Package
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

    slowcomb-0.x.dev.2019-09-09T09-09-09.999999.tar.gz

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
The numbers after the ``dev`` is the date and time ``setup.py`` was
invoked (it is actually off by up to a few hundred microseconds), while
the ``.tar.gz`` suffix just tells you that the files are Unix Tape Archives
with gzip compression applied.

Each time you run ``setup.py``, a new file will be created\*. Unless you
are fixing or working around a regression, you would use the archive with
the latest time stamp.

  \* A more accurate description would be: 'a new file is created for every
  different microsecond that ``setup.py`` is invoked'. I hope to live long 
  enough to see computers get so fast, that the entire package generation 
  can finish in under a microsecond.


Step 5: Install
===============
Begin by activating the VE of your choice.

Once inside the VE, install slowcomb by issuing the pip command with
the path to the package generated in Step 3 above. On a ``bash`` terminal 
on a Unix-compatible system, the command may look like:

::

    pip3 install /home/mrtooliteral/downloads-github/slowcomb/dist/\
    slowcomb-0.x.dev.2019-09-09T09-09-09.999999.tar.gz

With the exact path before ``/dist/`` altered to suit your filesystem,
and the exact name of the archive changed to match the one that's
actually on your filesystem.

 Note that the backslash (\\) character is only present to allow the
 example to be shown in two lines and still be correct. It may be safely
 removed, as long as you mend the command back into a single line.

A successful installation will be indicated by a message that looks like:

::

    Successfully installed slowcomb-0.x.dev.2019-09-09T09-09-09.999999

Pause to smell the victory. It's good for your soul.


Step 6: Have Fun!
=================
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

