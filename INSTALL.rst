Installing and Using Slowcomb for Virgins
-----------------------------------------

Slowcomb should be easy to import into your project using industry-standard
procedures, due to its minimal dependency footprint; only Python built-in
libraries are linked). Importing the library from repository to project, in
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

2. Optionally, run unit tests by invoking from the repo root:
   
   ::

      ``python3 -m unittest discover -s slowcomb/tests``

   This will ensure that you are not importing a build with known
   issues.

3. Optionally, prepare the virtual environment.

4. Generate a package by running ``python setup.py`` from the repo root.
   The installation package file should appear in the ``dist`` directory
   from here.

   * PROTIP: The packages are generated using ``setuptools`` and should 
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

* *repo root*, or Repository Root, the topmost level of the Slowcomb
  library repository's file system. In the simplest terms, the same
  directory you find ``README.rst`` and ``setup.py`` in.

* *source root*, the topmost level in which you may find Slowcomb-related
  material. In the simplest terms, it's the same directory that you
  may find ``slowcomb.py`` and ``slowseq.py`` in. Relative to the
  *repo root*, it is in the ``slowcomb/`` directory.

* *VE*, or *Virtual Environment*. An optional feature that allows you to
  create and maintain multiple copies of a Python environment, each
  with its own packages and modifications, and to prevent early updates
  or accidental uninstallations from causing software to stop working.
  
   VEs are used for maintaining continuity on enterprise systems or
   web servers, when running software certified to run only on specific
   versions of Python, or other modules, earlier than the latest, without
   holding back the rest of the system from potentially important updates.

Why am I doing this?
********************
Cloning from GitHub with Git is the preferred way of downloading source
code. Minor changes on the repository be applied without having to download
a newer version of an archive, eliminating the need to manage an entire
history of archive files. Changes may be reviewed using the ``git log``
command.

These are just two of the many features exclusive to using Git. If you
dive deeper, you might find out how to revert any file on your personal
copy of the repo to an older version while keeping the other files
intact. You could use the *bisect* feature to quickly find changes that
introduced a bug you are diagnosing. There are hundreds of features, one
for practically almost every possible situation a hacker could be in.

Do I have to do this?
*********************
No. Alternative installation methods exist. Read on...

How else can I do this?
***********************
* **ZIP dumps.** You can download the entire repo in a ZIP archive.
  From the repo root on the GitHub website, press the green 'Clone
  or Download' button. In the pop-up box that appears, use the Download
  ZIP link that appears. Save the ZIP file in your file system, and
  unpack the contents to a subfolder under your downloads or source code
  directory.
  Everything will work the same way like in the good 'ole days before 
  Git, but you may be missing out on the change tracking features such
  as the log and incremental updates.

* **Git front ends.** GitHub has its own original front end, the GitHub
  Desktop, downloadable from https://desktop.github.com. A much older
  version of this app (you're going back to a time when Electron was
  probably just a few bullet points on a napkin somewhere) was pretty
  much all the author has used in the way of Git front ends before he
  decided take the command line path, so you are pretty much on your
  own if you go down this way. Godspeed!


Step 2: Run Tests and Familiarise Yourself With the Repo
========================================================
Slowcomb's project tree is extremely simple and nearly impossible to
get lost in, but it is worth saying that main modules live in the
``slowcomb`` subdirectory, and unit tests live in ``slowcomb/tests``.

To run the unit tests, stay in the slowcomb repo root (i.e. the same
folder as the ``README.rst`` and ``LICENSE`` files), and run this command:

::

    python3 -m unittest discover -s slowcomb/tests

The ``python3`` explicitly invokes the default Python 3 interpreter on 
systems that have both Python 2 and 3 interpreters installed.

  PROTIP: On many systems merely running ``python`` invokes a Python 2
  interpreter. However, the Python slowcomb was written is its largely
  incompatible successor, Python 3. This is why you have to run
  ``python3`` instead or the command will not succeed. Hopefully, by
  the time you read this, Python 3 would have become the default
  Python.

This runs the built-in ``unittest`` module, which is executable, and
tells it where the tests are.

Note that some of the tests have been skipped (there are about 18 of
them at this time for the master branch). This is normal. A number
of the tests are slow-running and can take hours to complete. These
tests have been excluded from the test runner by default.

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

 Note that the backslash (\\) character is only present to allow the
 example to be shown in two lines and still be correct. It may be safely
 removed, as long as you mend the command back into a single line.

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

