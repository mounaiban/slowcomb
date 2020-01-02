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

1. **Clear (Alt+L)** - Deletes the CU and Resets the tree to the default state,
   as seen each time app is started. Files and exported data are left intact.

2. **Add Source (Alt+A)** - Adds a new source to a CU. Some CUs are
   single-source, so only one source may be added to them. A multi-source
   CU can accomodate multiple sources. A terminal source can only serve as a
   source to a CU.

3. **Delete (Alt+D)** - Deletes a CU. The first CU in the view (or the root CU)
   should not be deleted.

4. **Copy (Alt+C)** - Copies a CU to the clipboard. The data may be pasted
   elsewhere on the CU tree, or in a text editor. 

5. **Paste (Alt+P)** - Adds a copy of the CU in the clipboard to the CU tree.
   The same limitations on Adding new CUs apply to pasted CUs. See also Add
   Source above.

6. **Open (Alt+O)** - Replaces the CU tree with another from a file in your file
   system.

7. **Save As (Alt+S)** - Copies the entire CU tree to a file in your file
   system. These trees may be accessed again with the Open operation.

8. **Quit (Alt+Q)** - Closes the app. Please note that there is not yet a prompt
   to save any changes that may have been made, and all unsaved changes will
   be discarded without warning.

Please note that for now buttons for some operations may be hidden behind a
pull-down menu to the right side of the Editor toolbar. Hovering the pointer
over a button may be necessary to reveal the button to reveal the menu.
Keyboard shortcuts will not work for options hidden in the menu.

CUs and Sources
^^^^^^^^^^^^^^^
A CU tree may contain one or more sources, or random and
individually-addressable collections of data on which to perform combinatorial
operations.

Sources may be *terminal sources* that embed data in their literal form.
Currently-suported examples are the Python collections ``tuples`` and
``lists``.  CUs may also be used as sources to other CUs.

Please note that ``tuples`` and ``lists`` have identical behaviour in this
demo. Both are featured in order to prove that either may be used as terminal
sources.

CUs that attach only terminal sources are *simple CUs*. Conversely, CUs that
use one or more other CUs as sources are *compound CUs*.

All except one of the supported CU types are able to work with only one source;
``Permutation``, ``PermutationWithRepeats``, ``Combination`` and
``CombinationWithRepeats`` are *single-source CUs*, while ``CatCombination``
is a *multi-source CU*.

Configuring CUs
^^^^^^^^^^^^^^^
Each item in the CU tree has five properties:

1. **Address (abbreviated to #)** - A numerical path to show where on the
   tree a CU or source is located. The *root CU* on top of the tree always
   has an address of zero (``0``). An address of ``0:1:0`` points to the
   source under the second CU of the root CU.

2. **Name** - A friendly name that may be used to help identify the role of
   a CU or sources more clearly.

3. **Type** - Use this property to set an item as a particular type of CU,
   or a terminal source. See the section *CUs and Sources* in this file for
   information on what is defined as a CU or terminal source.
   For details on the exact behaviour and usage of CUs, please refer to the
   embedded documentation and code in the ``slowcomb.py`` module file, located
   in the project root.

4. **r** - Controls the number of elements in a term. For terminal sources,
   this value is not used, but should always be shown as ``1`` in the Editor.

5. **Data** - Specifies the content of a terminal source. This property
   is not used for CUs. In this demo, only comma-separated string sequences
   are supported.
   Some characters may interfere with the way the demo works. These characters
   may prevent the demo from displaying, copying, pasting or exporting terms.
   Configurations may even fail to load from file.

   Here are suggestions for some problematic characters:

   * Comma (``,``) - use HTML escape codes ``&#44`` or ``&comma;``

   * Single quote mark (``'``) - ``&#39`` 

   * Double quote marks (``"``) - ``\&quot;`` (one backslash followed by the
     HTML escape sequence ``&quot;``) for JSON export, or ``&quot;`` without
     the backslash for tabular export.

   These workarounds may also be used to manually recover configuration
   files.

Combinatorial Unit Terms Viewer
===============================
Terms from a CU will be shown in the Term Viewer to the left.

Press the **Refresh (Alt+R)** button to view the output of the CU in the
editor. Please note that for CUs with a very large number of terms (these
are really common, especially with Permutations), only a tiny subset of the
terms will be shown. Use the Term Settings control panel to adjust the number
of terms shown.

The terms may be copied to the clipboard, simply by selecting them from the
list. Multiple terms may be selected for copying.

CU Terms: Term Settings
=======================
Use the **Term Settings (Alt+T)** mini control panel to adjust the number of 
terms to be displayed, how they will be displayed, and the format that they
will be exported. The following options are available:

1. **JSON Output (Alt+J)** - Causes the terms to appear in a condensed format
   pursuant to the JSON standard when exported to file or copied to the
   clipboard. The terms will be placed in a single unbroken line, separated
   by commas and placed inside parentheses.
   JSON output may be copy-pasted directly into JavaScript code, or any code
   of any other language that has support for data collections with similar
   syntax.

2. **Term Limit (Alt+T)** - Specifies the maximum number of terms that will
   appear in the Term Viewer.

3. **Output Ranges (Alt+G)** - Sets the range of terms that will be shown.
   Multiple ranges may be entered. Term indices are used, which means that
   the *first term is term zero*. The format is as follows:

   ::

       [X0-Y0],[S0],[Xn-Yn],[Sn]...

   Where X is the lower bound and Y is the upper bound of a range, and
   S is a index to a single term, short form for S-S. Multiple ranges may be
   specified, separated by commas with no spaces. Ranges must be ordered 
   from smallest to largest (or rather, first to last).

   Here are some examples:

   * ``300-399`` - show only 299th to 398th term
   
   * ``1-20,50,60-80`` - show only 2nd to 21st, 51st, 61st to 79th terms

   * ``45-55,144-378``- show only 44th to 55th, then 143rd to 377th terms

   * ``1,2,4,8`` - show only 2nd, 3rd, 5th, 9th terms

   Remember that *the first term is term zero*.

   Ranges will be rejected if they:

   * Are placed out of order (e.g. ``100-200,50-60``)

   * Overlap (e.g. ``80-90,77-101``)

   * Contain non-integer numbers. (e.g. ``0.375-1.0``)

   * Do not match the format specified above.

Note that shortcut keys are only usable when the control panel is open.

4. **Compressed Ranges** - This upcoming feature allows the use of alphanumeric
   integers as an alternative to very long decimal integers when working with 
   large combinatorial sets.

Export
======
Press **Alt+X** to save all terms appearing in the viewer to a file. Control
the range of terms using the **Output Ranges** setting in Term Settings.
Enable **JSON Output** if the file is to be used with any application that
use JSON arrays as input, or for direct use in source code, disable it to
obtain the output in tabular format for use with spreasheets.

Comments
========
Some demo files have embedded comments that will be shown in the Comments tab.

Message History
===============
Some messages reported by the application that are too lengthy to fit in the
status bar will be viewable from a list that can be opened using the **History
(Alt+Y)** button at the bottom of the window.

