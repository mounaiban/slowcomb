"""
Test Method Name Generator and Planner

"""

# Copyright © 2019 Moses Chong
#
# This file is part of the Slow Addressable Combinatorics Library (slowcomb)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# Imports
#
import itertools
from slowcomb.slowcomb import CatCombination

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ModuleNotFoundError:
    print("PyGObject doesn't seem to be installed on this system")
    print("or virtual environment (VE). This demonstration needs it")
    print("to run. Please install it on your system or VE.\n")

# Utility Classes
#
class TestNameCombinator(CatCombination):
    """
    Template class for systematically generating names for tests.

    Arguments
    ---------
    * tags - a sequence of sequences containing test tags that will
      become part of the generated test names. Every tag combination
      from all sequences will be used. Tags will appear in the order
      as specified in the output format.

    * out_format - the output format which becomes the full name of
      the test. The format should be like:
      
      ::

        "test_cond_a_{0[x]}_cond_b_{0[x+1]}_cond_c_{0[x+2]}"

      and so on...
      
      The {0} replacement fields references the tag combination,
      while the subscripts after the 0 indicates which tag
      of the combination to use. For a more detailed explanation,
      see the Example below.

    Optional Arguments
    ------------------
    * include - Set to False to output nothing. This is just a means
      of excluding a test name combinator from a combinatorial chain
      without changing the list. Accepts True or False.
      True by default.

    Example
    -------
    Let's create a test name combinator for our role-playing-game:
    
    >>> from slowcomb.demos.test_planner import TestNameCombinator
    >>> tags_m = ('good', 'neutral', 'evil')
    >>>     # adapted from Dungeons and Dragons Morality
    >>> tags_a = ('chaotic', 'neutral', 'lawful')
    >>>     # adapted from D&D Adherence
    >>> tags_c = ('scientist', 'architect', 'hacker')
    >>>     # Our original classes
    >>> tags_all = (tags_m, tags_a, tags_c)
    >>> out_format = "test_ending_select_{0[2]}_{0[1]}_{0[0]}"
    >>> comb = TestNameCombinator(tags_all, out_format)

    Access the combinator as an iterator to see all the names:

    >>> for t in comb:
    ...     print(t)
    test_ending_select_scientist_chaotic_good
    test_ending_select_architect_chaotic_good
    test_ending_select_hacker_chaotic_good
    test_ending_select_scientist_neutral_good
    test_ending_select_architect_neutral_good
    test_ending_select_hacker_neutral_good
    test_ending_select_scientist_lawful_good
    test_ending_select_architect_lawful_good
    test_ending_select_hacker_lawful_good
    test_ending_select_scientist_chaotic_neutral
    test_ending_select_architect_chaotic_neutral
    test_ending_select_hacker_chaotic_neutral
    test_ending_select_scientist_neutral_neutral
    test_ending_select_architect_neutral_neutral
    test_ending_select_hacker_neutral_neutral
    test_ending_select_scientist_lawful_neutral
    test_ending_select_architect_lawful_neutral
    test_ending_select_hacker_lawful_neutral
    test_ending_select_scientist_chaotic_evil
    test_ending_select_architect_chaotic_evil
    test_ending_select_hacker_chaotic_evil
    test_ending_select_scientist_neutral_evil
    test_ending_select_architect_neutral_evil
    test_ending_select_hacker_neutral_evil
    test_ending_select_scientist_lawful_evil
    test_ending_select_architect_lawful_evil
    test_ending_select_hacker_lawful_evil

    Notice how the tags get inserted into the {0[x]} fields, and how
    the tags appear in reverse order. Observe in the format:

    ::

      out_format = "test_ending_select_{0[2]}_{0[1]}_{0[0]}"

    That the subscripts are in reverse order: 2, 1 and 0.

    This is merely a fraction of our possible endings, and there are
    already so many tests! Our game will miss Christmas at least twice
    at this rate!

    """
    def index():
        # TODO: Implement index()
        raise NotImplementedError('index() reverse-lookup not yet available')

    def _get_args(self):
        """
        Returns a string representation of a probable expression
        which may re-create this combinatorial unit.

        """
        out = "tags={0},include={1}".format(self._tags, self._r>0)
        return out

    def _get_comb(self, i):
        """
        Gets a tag combination of index i, formats it into a test
        name and outputs it as a string.
        """
        comb_data = super()._get_comb(i)
        return self._out_format.format(comb_data)

    def __init__(self, tags, out_format, **kwargs):
        """
        Create an instance of the TestNameCombinator. For instructions
        on using this class, please refer to the class-scope
        documentation for TestNameCombinator.

        """
        super().__init__(tags,len(tags))
        self._out_format = out_format
        self._tags = self._seq_src
        if kwargs.get('include',True) is False:
            self._r = 0

class ExampleTestNameCombinator(TestNameCombinator):
    """
    Generate test names for tropical/sidereal Zodiac-type astrological
    relationship compatibility tests.

    This is a hopefully more effective way of describing and documenting
    how the TestNameCombinator class works.

    The ExampleTestNameCombinator demonstrates how TestCombinators
    may be used as subclasses, in situtations where this is more
    advantageous than using instances.

    """
    def __init__(self, **kwargs):
        out_format = "test_{0[0]}_relationship_{0[1]}_with_{0[2]}"
        rel_type = ('erot','plat')
        zod_sign_greg_ord = ('aqu','pis','ari','tau','gem','can','leo',
            'vir','lbr','sco','sag','cap')
                # Zodiac signs with ordered by start date appearance
                # in Gregorian Calendar
        tags = (rel_type, zod_sign_greg_ord, zod_sign_greg_ord)
            # Group the tags to be combined into separate tuples,
            # then wrap the tag tuples in an outer tuple for the
            # the TestNameCombinator. 
            # Abbreviate the tags as much as readability is preserved,
            # to keep the name from getting to long.
            # Note that the Zodiac signs are used twice, to represent
            # the two parties in the relationship.
            #
            # NOTE: The Zodiac actually begins with Aries, although
            # newspapers like to begin with Aquarius or the star sign
            # of the month or something like that...

        super().__init__(tags, out_format, **kwargs)
            # Please always pass on the **kwargs!

# Shared Tags
#
tags_pnz = ('pos','neg','zero')
tags_ii_start_stop = ('pos','neg','neg_zero_x')

# Slice Start, Stop and Step Cases Suffixes
#
tags_slice_cases = (tags_pnz, tags_pnz, tags_pnz)
format_slice_cases = "{0[0]}_start_{0[1]}_stop_{0[2]}_step"
names_slice_cases = TestNameCombinator(tags_slice_cases, format_slice_cases)

# Slowcomb Sequences Integer Subscription Test Names
#
tags_intkey_cases = (tags_pnz, tags_ii_start_stop)
format_intkey_cases = "test_intkey_{0[0]}_i_{0[1]}_ii_start"
names_intkey_cases = TestNameCombinator(tags_intkey_cases,format_intkey_cases)

# Slowcomb Sequences Slice Subscription Test Names
# 
tags_slicekey_cases = (names_slice_cases, tags_ii_start_stop)
format_slicekey_cases = "test_slicekey_{0[0]}_{0[1]}_ii_start"
names_slicekey_cases = TestNameCombinator(tags_slicekey_cases,
    format_slicekey_cases)


# The Test Planner GTK+3 GUI!!!1!
#
# TODO: Use Gettext?
# TODO: Adapted from sebp's Python GTK+3 tutorialA (mostly from chapter 6)
# https://python-gtk-3-tutorial.readthedocs.io/
# TODO: Revision 0f23aed8

class TestPlannerGUI(Gtk.Window):

    class MessageAreaGrid(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self, border_width=8)

            lbl_msg = Gtk.Label(label="Message Area")
            btn_open_msg = Gtk.Button(label="Messages")
            btn_clear_msg = Gtk.Button(label="Clear")
            self.attach(lbl_msg, 0, 0, 8, 1)
            self.attach_next_to(btn_open_msg, lbl_msg, Gtk.PositionType.RIGHT,
                1, 1)
            self.attach_next_to(btn_clear_msg, btn_open_msg,
                Gtk.PositionType.RIGHT, 1, 1)
            lbl_msg.set_size_request(600,-1)

    class TestNameViewFrame(Gtk.Frame):

        def __init__(self):
            Gtk.Frame.__init__(self, label='Tests',border_width=8)

            grid = Gtk.Grid(border_width=8)
            treev_tests = Gtk.TreeView()
            treev_combs = Gtk.TreeView()
            grid.attach(treev_tests, 0, 0, 2, 1)
            grid.attach(treev_combs, 0, 1, 1, 1)
            self.set_size_request(600,-1)
            self.add(grid)

    class DeleteControlsFrame(Gtk.Frame):

        def __init__(self):
            Gtk.Frame.__init__(self, label='Delete Tests', border_width=8)

            # Delete Test Controls
            box_delete_ctls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            lbl_delete = Gtk.Label(label="Select one or more combinators or tests on the left to delete")
            lbl_delete.set_line_wrap(True)
            btn_delete = Gtk.Button(label="Delete")
            box_delete_ctls.pack_start(lbl_delete, True, True, 2)
            box_delete_ctls.pack_start(btn_delete, True, True, 2)

            # Clear Tests Controls
            box_clear_ctls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            lbl_clear = Gtk.Label(label="Press the button to delete ALL tests")
            btn_clear = Gtk.Button(label="Clear")
            box_clear_ctls.pack_start(lbl_clear, True, True, 2)
            box_clear_ctls.pack_start(btn_clear, True, True, 2)

            # Attach Delete and Clear Controls to Stack
            stack_delctls = Gtk.Stack()
            stack_delctls.add_titled(box_delete_ctls, "delete_controls",
                "Delete")
            stack_delctls.add_titled(box_clear_ctls, "clear_controls","Clear")
            stacksw = Gtk.StackSwitcher()
            stacksw.set_stack(stack_delctls)

            # Attach Stack and Switcher to Box
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,border_width=8)
            box.pack_start(stacksw, True, True, 4)
            box.pack_start(stack_delctls, True, True, 4)

            # Attach Everything to Frame 
            self.add(box)
            
    class AddControlsGrid(Gtk.Frame):

        def __init__(self):
            Gtk.Frame.__init__(self, label='Add Tests', border_width=8)

            # Add Test With Combinator Controls
            box_addc_ctls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            btn_addc = Gtk.Button(label="Add Test Using Combinator...")
            box_addc_ctls.pack_start(btn_addc, True, True, 2)

            # Add Single Test Controls
            box_adds_ctls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            ent_adds = Gtk.Entry()
            ent_adds.set_placeholder_text("Enter Name of Test")
            btn_adds = Gtk.Button(label="Add Test")
            box_adds_ctls.pack_start(ent_adds, True, True, 2)
            box_adds_ctls.pack_start(btn_adds, True, True, 2)

            # Attach Delete and Clear Controls to Stack
            stack_addctls = Gtk.Stack()
            stack_addctls.add_titled(box_adds_ctls, "single_controls",
                "Single")
            stack_addctls.add_titled(box_addc_ctls, "multi_controls","Multi")
            stacksw = Gtk.StackSwitcher()
            stacksw.set_stack(stack_addctls)

            # Attach Stack and Switcher to Box
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,border_width=8)
            box.pack_start(stacksw, True, True, 4)
            box.pack_start(stack_addctls, True, True, 4)

            # Attach Everything to Frame 
            self.add(box)
            
    class ExportImportControlsGrid(Gtk.Frame):

        def __init__(self):
            Gtk.Frame.__init__(self, label='Export and Import', border_width=8)

            # Test Export Controls
            box_exp_ctls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            lbl_exp = Gtk.Label(label="Put\n\n\n\n\nExport Test Controls Here")
            box_exp_ctls.pack_start(lbl_exp, True, True, 2)

            # Test Import Controls
            box_imp_ctls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            lbl_imp = Gtk.Label(label="Put Import Test Controls Here")
            box_imp_ctls.pack_start(lbl_imp, True, True, 2)

            # Attach Export and Import Controls to Stack
            stack_addctls = Gtk.Stack()
            stack_addctls.add_titled(box_exp_ctls, "export_controls","Export")
            stack_addctls.add_titled(box_imp_ctls, "import_controls","Import")
            stacksw = Gtk.StackSwitcher()
            stacksw.set_stack(stack_addctls)

            # Attach Stack and Switcher to Box
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,border_width=8)
            box.pack_start(stacksw, True, True, 4)
            box.pack_start(stack_addctls, True, True, 4)

            # Attach Everything to Frame 
            self.add(box)

            
    def __init__(self):
        # Prepare main grid layout
        Gtk.Window.__init__(self, title='Slowcomb Test Planner')

        self.set_default_size(720,480)
        main_grid = Gtk.Grid()
        self.add(main_grid)
        self.connect("size-allocate",lambda x: print('YAY'))

        button4 = Gtk.Button(label="Export/Import Controls")

        main_grid.attach(self.TestNameViewFrame(), 0, 0, 4, 8)
        main_grid.attach(self.DeleteControlsFrame(), 4, 0, 2, 1)
        main_grid.attach(self.AddControlsGrid(), 4, 1, 1, 1)
        main_grid.attach(self.ExportImportControlsGrid(), 4, 2, 1, 1)
        main_grid.attach(self.MessageAreaGrid(), 0, 8, 4, 1)



def _start_gui():
    win_main = TestPlannerGUI()
    win_main.connect("destroy", Gtk.main_quit)
    win_main.show_all()
    Gtk.main()

# Preliminary Test Planner Output in CSV
# TODO: Re-implement this using the Python CSV API?
def get_csv():
    tests=itertools.chain(names_intkey_cases,names_slicekey_cases)
    test_list=[t for t in tests]
    classes=('NumberSequence', 'CacheableSequence', 'BlockCacheableSequence')
    # Output CSV Rows
    headings='Test name,Status'
    print(headings)
    count=0
    for c in classes:
        for t in test_list:
            print("{0}:{1}".format(c,t), end=',NOT_IMPLEMENTED\n')
            count+=1
    print("Tests In Total: {0}".format(count))

# Open desktop GUI when called from a CLI shell
if __name__=='__main__':
    _start_gui()

