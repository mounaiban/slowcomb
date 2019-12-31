Slowcomb Introductor Demo Instructions
--------------------------------------

Welcome to the Slowcomb Intro Demo!

This demo app is intended to be an introduction to the operation of Slowcomb's
Combinatorial Units (CUs), the building blocks of randomly-addressable
combinatorial operations. The app may be used to explore the capabilities,
limitations, strengths and weaknesses of Slowcomb's approach to combinatorics.

Editor
======

The demo allows users to visually create and manage a single CU. The view of
the CU is called the CU tree. The following operations are available, along
with their shortcut key combo:

1. Clear (Alt+L) - Deletes the CU and Resets the tree to the default state,
   as seen each time app is started. Files and exported data are left intact.

2. Add Source (Alt+A) - Adds a new source to a CU. Some CUs are single-source,
   so only one source may be added to them. A multi-source CU can accomodate
   multiple sources. A terminal source can only serve as a source to a CU.

3. Delete (Alt+D) - Deletes a CU. The first CU in the view (or the root CU)
   should not be deleted.

4. Copy (Alt+C) - Copies a CU to the clipboard. The data may be pasted
   elsewhere on the CU tree, or in a text editor. 

5. Paste (Alt+P) - Adds a copy of the CU in the clipboard to the CU tree.
   The same limitations on Adding new CUs apply to pasted CUs. See also Add
   Source above.

6. Open (Alt+O) - Replaces the CU tree with another from a file in your file
   system.

7. Save As (Alt+S) - Copies the entire CU tree to a file in your file system.
   These trees may be accessed again with the Open operation.

8. Quit (Alt+Q) - Closes the app. Please note that there is not yet a prompt
   to save any changes that may have been made, and all unsaved changes will
   be discarded without warning.

Please note that for now buttons for some operations may be hidden behind a
pull-down menu to the right side of the Editor toolbar. Hovering the pointer
over a button may be necessary to reveal the button to reveal the menu.
Keyboard shortcuts will not work for options hidden in the menu.

Editor: CUs and Sources
=======================
A CU tree may contain one or more sources, or random and
individually-addressable collections of data on which to perform combinatorial
operations.

Sources may be *terminal sources* that embed data in their literal form.
Currently-suported examples are the Python collections ``tuples`` and
``lists``.  CUs may also be used as sources to other CUs.

CUs that attach only terminal sources are *simple CUs*. Conversely, CUs that
use one or more other CUs as sources are *compound CUs*.

All except one of the supported CU types are able to work with only one source;
``Permutation``, ``PermutationWithRepeats``, ``Combination`` and
``CombinationWithRepeats`` are *single-source CUs*, while ``CatCombination``
is a *multi-source CU*.


