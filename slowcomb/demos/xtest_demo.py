"""
Combinatorial Unit Introductory Demo self-test module

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

# A Note from Moses
# -----------------
# Some error or warning messages about "widget[s] already existing inside
# containers" are to be expected. At time of writing, these tests remain
# accurate. Nevertheless, I will have to eventually find a less dodgy way
# to perform these tests.
#

import csv
import io
import unittest
import os.path
from slowcomb.demos.demo import CUEditorModelSpec, MainUI
from slowcomb.demos.demo import csv_to_model, traverse_treemodel

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ModuleNotFoundError:
    msg_no_gi_gtk3 = \
        'PyGObject does\'t seem to be installed on this system'\
        'or virtual environment (VE).'\
        'To be able to run this test, please ensure that the'\
        'Following are installed and working correctly:'\
        '* PyGObject (check Python package manager)'\
        '* GTK+3 (check operating system)'
    print(msg_no_gi_gtk3)

class CSVToModelTests(unittest.TestCase):
    """Verifies the operation of the CSV-to-GTK TreeModel data import routine
    csv_to_model()

    """
    format_version = '1.1'

    def setUp(self):
        self.cm_spec = CUEditorModelSpec()
        self.fn_dummy = lambda tm,ti: 0
        self.csv_str_single = '"0","zulu","test",1,"Z"'
        self.csv_str_flat =  \
            '"0","whiskey","test",1,"W"\n'\
            '"1","yankee","test",1,"Y"\n'\
            '"2","zulu","test",1,"Z"\n'     
            # PROTIP: 'a' 'b' == 'ab'
        self.csv_str_deep_multi_lvl_return = \
            '"0","whiskey","test",1,"W"\n'\
            '"0:0","x-ray","test",1,"X"\n'\
            '"0:0:0","yankee","test",1,"Y"\n'\
            '"1","zulu","test",1,"Z"\n'    
        self.csv_str_deep_single_lvl_return = \
            '"0","whiskey","test",1,"W"\n'\
            '"0:0","x-ray","test",1,"X"\n'\
            '"1","yankee","test",1,"Y"\n'\
            '"2","zulu","test",1,"Z"\n'   
        self.csv_str_deep_no_return = \
            '"0","whiskey","test",1,"W"\n'\
            '"0:0","x-ray","test",1,"X"\n'\
            '"0:0:0","yankee","test",1,"Y"\n'
        self.csv_str_init = \
            '"0","alfa","test","1","A"\n'\
            '"0:0","bravo","test","1","B"\n'\
            '"1","charlie","test","1","C"\n'\
            '"2","delta","test","1","D"\n'  

    def _str_to_csv_reader(self, string):
        # Creates a CSV reader from a CSV-formatted string.
        # This function expects columns to be comma-separated,
        # values to be in either single or double quotes ONLY,
        # and rows to be terminated with any sequence, as long
        # it is the only one in use in the string.
        rows_raw = string.split('\n')
        dialect = csv.Sniffer().sniff(rows_raw[0])
        reader = csv.reader(rows_raw, dialect)
        return reader

    def test_self_test(self):
        """Verify that test data is correct. Test results from this
        test case shall only be accepted if this test passes.

        """
        model = Gtk.TreeStore(*self.cm_spec.column_types) 
        csvr_init = self._str_to_csv_reader(self.csv_str_init)
        csv_to_model(csvr_init, model, self.cm_spec)
        out_expected = (
            ['0','alfa','test',1,'A'],
            ['0:0','bravo','test',1,'B'],
            ['1','charlie','test',1,'C'],
            ['2','delta','test',1,'D'],
        )
            # PROTIP: The reference rows in out_expected are in lists, to
            # match the format which TreeModel rows are returned.
        out = get_path_stamped_rows(model)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_deep_no_return_top_level_mid_insert(self):
        model = Gtk.TreeStore(*self.cm_spec.column_types) 
        # Arrangement - Start with the default test model
        csvr_init = self._str_to_csv_reader(self.csv_str_init)
        csv_to_model(csvr_init, model, self.cm_spec)
        # Actions - Insert multiple rows after charlie at top level
        path = Gtk.TreePath.new_from_string('1')
        treeiter_1 = model.get_iter(path)
        csvr_dnr = self._str_to_csv_reader(self.csv_str_deep_no_return)
        csv_to_model(csvr_dnr, model, self.cm_spec, treeiter=treeiter_1)
        # Assertion
        out_expected = (
            ['0','alfa','test',1,'A'],
            ['0:0','bravo','test',1,'B'],
            ['1','charlie','test',1,'C'],
            ['2','whiskey','test',1,'W'],
            ['2:0','x-ray','test',1,'X'],
            ['2:0:0','yankee','test',1,'Y'],
            ['3','delta','test',1,'D'],
        )
        out = get_path_stamped_rows(model)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])
    
    def test_single_top_level_top_insert(self):
        model = Gtk.TreeStore(*self.cm_spec.column_types) 
        # Arrangement - Start with the default test model
        csvr_init = self._str_to_csv_reader(self.csv_str_init)
        csv_to_model(csvr_init, model, self.cm_spec)
        # Actions = Insert single row at start of top level
        csvr_single = self._str_to_csv_reader(self.csv_str_single)
        csv_to_model(csvr_single, model, self.cm_spec, mode='before')
        # Assertion
        out_expected = (
            ['0','zulu','test',1,'Z'],
            ['1','alfa','test',1,'A'],
            ['1:0','bravo','test',1,'B'],
            ['2','charlie','test',1,'C'],
            ['3','delta','test',1,'D'],
        )
        out = get_path_stamped_rows(model)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_single_top_level_mid_insert(self):
        model = Gtk.TreeStore(*self.cm_spec.column_types) 
        # Arrangement - Start with default test model
        csvr_init = self._str_to_csv_reader(self.csv_str_init)
        csv_to_model(csvr_init, model, self.cm_spec)
        # Actions - Insert single row after charlie
        csvr_single = self._str_to_csv_reader(self.csv_str_single)
        path = Gtk.TreePath.new_from_string('1')
        treeiter_1 = model.get_iter(path)
        csv_to_model(csvr_single, model, self.cm_spec, treeiter=treeiter_1)
        # Assertion
        out_expected = (
            ['0','alfa','test',1,'A'],
            ['0:0','bravo','test',1,'B'],
            ['1','charlie','test',1,'C'],
            ['2','zulu','test',1,'Z'],
            ['3','delta','test',1,'D'],
        )
        out = get_path_stamped_rows(model)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

class TraverseTreeModelTests(unittest.TestCase):
    """Verifies the operation of the generalised GTK TreeModel traversal
    routine, traverse_treemodel().

    Currently, this test also happens to be able to verify the functionality
    of the helper functions get_stamped_rows() and insert_into_model()
    of this test module.

    """
    format_version = '1.1'

    def setUp(self):
        self.cm_spec = CUEditorModelSpec()

    def test_flat(self):
        rows_src = (
            ['0','alfa','test',4,'A,B,C,D'],
            ['1','bravo','test',4,'E,F,G,H'],
            ['2','charlie','test',4,'I,J,K,L'],
        )
        treestore = Gtk.TreeStore(*self.cm_spec.column_types)
        insert_into_model(treestore, rows_src)

        out = get_path_stamped_rows(treestore)
        self.assertEqual(len(out), len(rows_src))
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], rows_src[i])

    def test_two_levels_no_return(self):
        rows_src_lvl_0 = (
            ('0','alfa','test',4,'A,B,C,D'),
            ('1','bravo','test',4,'E,F,G,H'),
        )
        row_src_1_0 = (('1:0','charlie','test',4,'I,J,K,L'),)
        out_expected = (
            ['0','alfa','test',4,'A,B,C,D'],
            ['1','bravo','test',4,'E,F,G,H'],
            ['1:0','charlie','test',4,'I,J,K,L'],
        )
        treestore = Gtk.TreeStore(*self.cm_spec.column_types)
        insert_into_model(treestore, rows_src_lvl_0)
        insert_into_model(treestore, row_src_1_0, parent_path_str='1')
        out = get_path_stamped_rows(treestore)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_two_levels_one_level_return(self):
        rows_src_lvl_0 = (
            ('0','alfa','test',4,'A,B,C,D'),
            ('1','bravo','test',4,'E,F,G,H'),
        )
        row_src_0_0 = (('0:0','charlie','test',4,'I,J,K,L'),)
        out_expected = (
            ['0','alfa','test',4,'A,B,C,D'],
            ['0:0','charlie','test',4,'I,J,K,L'],
            ['1','bravo','test',4,'E,F,G,H'],
        )
        out = []
        treestore = Gtk.TreeStore(*self.cm_spec.column_types)
        insert_into_model(treestore, rows_src_lvl_0)
        insert_into_model(treestore, row_src_0_0, parent_path_str='0')
        out = get_path_stamped_rows(treestore)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_four_levels_no_return(self):
        row_src_0 = ( ('0','alfa','test',4,'A,B,C'), )
        row_src_0_0 = ( ('0:0','bravo','test',4,'1,2,3'), )
        row_src_0_0_0 = ( ('0:0:0','charlie','test',4,'do,re,mi'), )
        row_src_0_0_0_0 = ( ('0:0:0:0','delta','test',4,'u,n,me'), )
        out_expected = (
            ['0','alfa','test',4,'A,B,C'],
            ['0:0','bravo','test',4,'1,2,3'],
            ['0:0:0','charlie','test',4,'do,re,mi'],
            ['0:0:0:0','delta','test',4,'u,n,me'],
        )
        treestore = Gtk.TreeStore(*self.cm_spec.column_types)
        insert_into_model(treestore, row_src_0)
        insert_into_model(treestore, row_src_0_0, parent_path_str='0')
        insert_into_model(treestore, row_src_0_0_0, parent_path_str='0:0')
        insert_into_model(treestore, row_src_0_0_0_0, parent_path_str='0:0:0')
        
        out = get_path_stamped_rows(treestore)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_four_levels_multi_level_return(self):
        row_src_0 = ( ('0','alfa','test',1,'A'), )
        row_src_0_0 = ( ('0:0','bravo','test',1,'B'), )
        row_src_0_0_0 = ( ('0:0:0','charlie','test',1,'C'), )
        row_src_0_0_0_0 = ( ('0:0:0:0','delta','test',1,'D'), )
        row_src_1 = ( ('1','echo','test',1,'E'), )
        out_expected = (
            ['0','alfa','test',1,'A'], 
            ['0:0','bravo','test',1,'B'], 
            ['0:0:0','charlie','test',1,'C'],
            ['0:0:0:0','delta','test',1,'D'], 
            ['1','echo','test',1,'E'], 
        )
        treestore = Gtk.TreeStore(*self.cm_spec.column_types)
        insert_into_model(treestore, row_src_0)
        insert_into_model(treestore, row_src_0_0, parent_path_str='0')
        insert_into_model(treestore, row_src_0_0_0, parent_path_str='0:0')
        insert_into_model(treestore, row_src_0_0_0_0, parent_path_str='0:0:0')
        insert_into_model(treestore, row_src_1)
        out = get_path_stamped_rows(treestore)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_four_levels_one_level_return(self):
        row_src_0 = ( ('0','alfa','test',4,'A,B,C'), )
        row_src_0_0 = ( ('0:0','bravo','test',4,'1,2,3'), )
        row_src_0_0_0 = ( ('0:0:0','charlie','test',4,'D,E,F'), )
        row_src_0_0_0_0 = ( ('0:0:0:0','delta','test',4,'iv,v,vi'), )
        row_src_0_0_1 = ( ('0:0:1','echo','test',4,'G,H,I'), )
        row_src_0_1 = ( ('0:1','foxtrot','test',4,'7,8,9'), )
        row_src_1 = ( ('1','golf','test',4,'J,K,L'), )
        out_expected = (
            ['0','alfa','test',4,'A,B,C'], 
            ['0:0','bravo','test',4,'1,2,3'], 
            ['0:0:0','charlie','test',4,'D,E,F'],
            ['0:0:0:0','delta','test',4,'iv,v,vi'], 
            ['0:0:1','echo','test',4,'G,H,I'], 
            ['0:1','foxtrot','test',4,'7,8,9'], 
            ['1','golf','test',4,'J,K,L'], 
        )
        treestore = Gtk.TreeStore(*self.cm_spec.column_types)
        insert_into_model(treestore, row_src_0)
        insert_into_model(treestore, row_src_0_0, parent_path_str='0')
        insert_into_model(treestore, row_src_0_0_0, parent_path_str='0:0')
        insert_into_model(treestore, row_src_0_0_0_0, parent_path_str='0:0:0')
        insert_into_model(treestore, row_src_0_0_1, parent_path_str='0:0')
        insert_into_model(treestore, row_src_0_1, parent_path_str='0')
        insert_into_model(treestore, row_src_1)
        out = get_path_stamped_rows(treestore)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

class TraverseTreeModelWithLimitsTests(unittest.TestCase):
    format_version = '1.1'

    def setUp(self):
        self.cm_spec = CUEditorModelSpec()
        rows_src_lvl_0 = (
            ('0','alfa','test',4,'A,B,C,D'),
            ('1','bravo','test',4,'A,B,C,D'),
            ('2','charlie','test',4,'A,B,C,D'),
            ('3','delta','test',4,'A,B,C,D'),
        )
        rows_src_0_0 = (
            ('0:0','alfa-0','test',3,'A,A,A'),
            ('0:1','alfa-1','test',3,'A,A,A'),
            ('0:2','alfa-2','test',3,'A,A,A'),
        ) 
        self.treestore = Gtk.TreeStore(*self.cm_spec.column_types)
        insert_into_model(self.treestore, rows_src_lvl_0)
        insert_into_model(self.treestore, rows_src_0_0, parent_path_str='0')

    def test_check_test_data(self):
        out_expected = (
            ['0','alfa','test',4,'A,B,C,D'],
            ['0:0','alfa-0','test',3,'A,A,A'],
            ['0:1','alfa-1','test',3,'A,A,A'],
            ['0:2','alfa-2','test',3,'A,A,A'],
            ['1','bravo','test',4,'A,B,C,D'],
            ['2','charlie','test',4,'A,B,C,D'],
            ['3','delta','test',4,'A,B,C,D'],
        )
        out = get_path_stamped_rows(self.treestore)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_zero_limit(self):
        path = Gtk.TreePath.new_from_string('0')
        treeiter = self.treestore.get_iter(path)
        limits = (0,)
        out_expected = []
        out = get_path_stamped_rows(self.treestore, limits=limits)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_one_top_level_deep_row(self):
        path = Gtk.TreePath.new_from_string('0')
        treeiter = self.treestore.get_iter(path)
        limits = (1,)
        out_expected = (
            ['0','alfa','test',4,'A,B,C,D'],
            ['0:0','alfa-0','test',3,'A,A,A'],
            ['0:1','alfa-1','test',3,'A,A,A'],
            ['0:2','alfa-2','test',3,'A,A,A'],
        )
        out = get_path_stamped_rows(self.treestore, limits=limits)
        self.assertEqual(len(out), len(out_expected))
        for i in range(len(out_expected)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

class EditorControlPageTests(unittest.TestCase):
    """Tests to verify correct operation of the CU Tree Editor in the
    Intro Demo

    """
    format_version = '1.1-SE'
    demos_dir = 'slowcomb/demos/'
    str_src_dir = os.path.join(os.path.abspath(os.path.curdir), demos_dir)
    str_src_file = MainUI.default_str_file_name
    str_src_path = os.path.join(str_src_dir, str_src_file)
        # TODO: Find a more resilient method of specifying the demos
        # directory (instead of the project root) as the working directory
        # during tests.
    dw = MainUI(str_src_path=str_src_path)
        # PROTIP: The Demo Main Window UI Window is in class scope, as it
        # only wants to be created once. GTK stuff appear to persist across
        # tests. Generally, only one instance of most widgets may be created
        # at any given time, making it rather unsafe to run these tests
        # conurrently.

    def setUp(self):
        # PROTIP: setUp() is run once for each test before it begins
        self.ctrlpage_ed = self.dw._control_pages['EDIT']
        self.string_dict = self.ctrlpage_ed._strings
        self.cu_marker_one = self.string_dict['editor-model-cu-marker-one']
        self.cu_marker_other = self.string_dict['editor-model-cu-marker-other']
            # PROTIP: The term 'other' is jargon from Android i18n libraries 
            # that is defined as any quantity other than one. English
            # is defined as only having a 'other' plural, while the singular
            # is defined as a 'one' plural.
            # See: Android Developers. String Resources. Quantity Strings.
        self.ed_file_test_default = \
            '{"app":"slowcomb-demo","version":"1.1-SE"}\n'\
            '"0","cu","CatCombination","2",""\n'\
            '"0:0","cu-src-perm","Permutation","4",""\n'
        # Action - Reset Editor and load test data 
        stream = str_to_string_io(self.ed_file_test_default)
        self.ctrlpage_ed._clear_and_reset()
        self.ctrlpage_ed._open(stream)

    def test_self_test(self):
        """Verify that test data is correctly set up. Do not accept results
        from this test case unless this test passes.

        """
        model = self.ctrlpage_ed.model
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-perm','Permutation',4,self.cu_marker_one],
        )
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_clear(self):
        model = self.ctrlpage_ed.model
        # Actions - Reset the Editor
        self.ctrlpage_ed._clear_and_reset()
        out_expected = (
            ['0','cu','Permutation',3,self.cu_marker_one],
            ['0:0','cu-src','tuple',1,'A,B,C,D'],
        )
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_single_add_single_src_cu(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-perm','Permutation',4,self.cu_marker_one],
            ['0:0:0','cu-src-perm-src','tuple',1,'I,J,K,L'],
        )
        # Actions - Select the Permutation by Path, add one source
        parent_path_str = '0:0'
        path = Gtk.TreePath.new_from_string(parent_path_str)
        selection.select_path(path)
        self.ctrlpage_ed._on_clicked_request_add(None)
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_multi_add_single_src_cu(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-perm','Permutation',4,self.cu_marker_one],
            ['0:0:0','cu-src-perm-src','tuple',1,'I,J,K,L'],
        )
        # Actions - Select the Permutation by Path, add three sources
        parent_path_str = '0:0'
        path = Gtk.TreePath.new_from_string(parent_path_str)
        selection.select_path(path)
        #  Attempt to add three sources to the single-source Permutation
        self.ctrlpage_ed._on_clicked_request_add(None)
        self.ctrlpage_ed._on_clicked_request_add(None)
        self.ctrlpage_ed._on_clicked_request_add(None)
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_single_add_multi_src_cu(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-perm','Permutation',4,self.cu_marker_one],
            ['0:1','cu-src-1','tuple',1,'I,J,K,L'],
        )
        # Actions - Select the CatCombination by Path, add one source
        parent_path_str = '0'
        path = Gtk.TreePath.new_from_string(parent_path_str)
        selection.select_path(path)
        self.ctrlpage_ed._on_clicked_request_add(None)
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_multi_add_multi_src_cu(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-perm','Permutation',4,self.cu_marker_one],
            ['0:1','cu-src-1','tuple',1,'I,J,K,L'],
            ['0:2','cu-src-2','tuple',1,'M,N,O,P'],
            ['0:3','cu-src-3','tuple',1,'Q,R,S,T'],
        )
        # Actions - Select the CatCombination by Path, add three sources
        parent_path_str = '0'
        path = Gtk.TreePath.new_from_string(parent_path_str)
        selection.select_path(path)
        #  Attempt to add three sources to multi-source CatCombination
        self.ctrlpage_ed._on_clicked_request_add(None)
        self.ctrlpage_ed._on_clicked_request_add(None)
        self.ctrlpage_ed._on_clicked_request_add(None)
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_delete_cu(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
        )
        # Actions - Select the Permutation by Path, delete it
        parent_path_str = '0:0'
        path = Gtk.TreePath.new_from_string(parent_path_str)
        selection.select_path(path)
        self.ctrlpage_ed._on_clicked_request_delete(None)
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_delete_cu_root(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-perm','Permutation',4,self.cu_marker_one],
        )
        # Actions - Select the Permutation by Path, delete it
        parent_path_str = '0'
        path = Gtk.TreePath.new_from_string(parent_path_str)
        selection.select_path(path)
        self.ctrlpage_ed._on_clicked_request_delete(None)
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_change_name(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        out_expected = (
            ['0','outer','CatCombination',2,self.cu_marker_other],
            ['0:0','inner','Permutation',4,self.cu_marker_one],
        )
        # Actions - Rename the CUs
        path_0 = Gtk.TreePath.new_from_string('0')
        path_0_0 = Gtk.TreePath.new_from_string('0:0')
        self.ctrlpage_ed._on_edited_apply_name_change(None, path_0, 'outer')
        self.ctrlpage_ed._on_edited_apply_name_change(None, path_0_0, 'inner')
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_change_type_cu_multi_src_to_single_src(self):
        model = self.ctrlpage_ed.model
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-0','CatCombination',2,self.cu_marker_other],
            ['0:0:0','cu-src-0-src-0','tuple',4,'A,B,C,D'],
            ['0:0:1','cu-src-0-src-1','tuple',4,'E,F,G,H'],
            ['0:1','cu-src-1','Permutation',1,self.cu_marker_one],  
            ['0:1:0','cu-src-1-src-0','tuple',4,'W,X,Y,Z'],
        )
        ed_file_test_init = \
            '{"app":"slowcomb-demo","version":"1.1-SE"}\n'\
            '"0","cu","CatCombination","2",""\n'\
            '"0:0","cu-src-0","CatCombination","2",""\n'\
            '"0:0:0","cu-src-0-src-0","tuple","4","A,B,C,D"\n'\
            '"0:0:1","cu-src-0-src-1","tuple","4","E,F,G,H"\n'\
            '"0:1","cu-src-1","CatCombination","1",""\n'\
            '"0:1:0","cu-src-1-src-0","tuple","4","W,X,Y,Z"\n'
        # Action - Reset Editor and load test data
        stream = str_to_string_io(ed_file_test_init)
        self.ctrlpage_ed._open(stream)
        # Action - Attempt to change CatCombination's to Permutation's
        class_name = 'Permutation'
        path_0_0 = Gtk.TreePath.new_from_string('0:0')
        path_0_1 = Gtk.TreePath.new_from_string('0:1')
        self.ctrlpage_ed._on_edited_apply_type_change(
            None, path_0_0, class_name
        )
        self.ctrlpage_ed._on_edited_apply_type_change(
            None, path_0_1, class_name
        )
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_change_type_cu_single_src_to_multi_src(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        # Action - Load test data into Editor 
        ed_file_init = \
            '{"app":"slowcomb-demo","version":"1.1-SE"}\n'\
            '"0","cu","CatCombination","2",""\n'\
            '"0:0","cu-src-1","Permutation","4",""\n'\
            '"0:0:0","cu-src-1-src","tuple","1","A,B,C,D"\n'\
            '"0:1","cu-src-2","Permutation","4",""\n'
        stream = str_to_string_io(ed_file_init)
        self.ctrlpage_ed._open(stream)
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-1','CatCombination',4,self.cu_marker_other],
            ['0:0:0','cu-src-1-src','tuple',1,'A,B,C,D'],
            ['0:1','cu-src-2','CatCombination',4,self.cu_marker_other],
        )
        # Action - Attempt changing both Permutation's into CatCombination's
        # PROTIP: CatCombinations are a multi-source Combinatorial Unit
        class_name = 'CatCombination'
        path_0_0 = Gtk.TreePath.new_from_string('0:0')
        path_0_1 = Gtk.TreePath.new_from_string('0:1')
        self.ctrlpage_ed._on_edited_apply_type_change(
            None, path_0_0, class_name
        )
        self.ctrlpage_ed._on_edited_apply_type_change(
            None, path_0_1, class_name
        )
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_change_type_cu_multi_src_to_src(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        # Action - Load test data into Editor 
        ed_file_init = \
            '{"app":"slowcomb-demo","version":"1.1-SE"}\n'\
            '"0","cu","CatCombination","2",""\n'\
            '"0:0","cu-src-1","CatCombination","4",""\n'\
            '"0:0:0","cu-src-1-src","tuple","1","A,B,C,D"\n'\
            '"0:1","cu-src-2","CatCombination","4",""\n'
        stream = str_to_string_io(ed_file_init)
        self.ctrlpage_ed._clear_and_reset()
        self.ctrlpage_ed._open(stream)
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-1','CatCombination',4,self.cu_marker_other],
            ['0:0:0','cu-src-1-src','tuple',1,'A,B,C,D'],
            ['0:1','cu-src-2','tuple',4,'I,J,K,L'],
        )
        # Action - Attempt to change the third CatCombination to a
        # terminal source
        class_name = 'tuple'
        path_0_1 = Gtk.TreePath.new_from_string('0:1')
        self.ctrlpage_ed._on_edited_apply_type_change(
            None, path_0_1, class_name
        )

        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_change_type_cu_single_src_to_src(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        # Action - Load test data into Editor 
        ed_file_init = \
            '{"app":"slowcomb-demo","version":"1.1-SE"}\n'\
            '"0","cu","CatCombination","2",""\n'\
            '"0:0","cu-src-1","Permutation","4",""\n'\
            '"0:0:0","cu-src-1-src","tuple","1","A,B,C,D"\n'\
            '"0:1","cu-src-2","Permutation","4",""\n'
        stream = str_to_string_io(ed_file_init)
        self.ctrlpage_ed._clear_and_reset()
        self.ctrlpage_ed._open(stream)
        out_expected = (
            ['0','cu','CatCombination',2,self.cu_marker_other],
            ['0:0','cu-src-1','Permutation',4,self.cu_marker_one],
            ['0:0:0','cu-src-1-src','tuple',1,'A,B,C,D'],
            ['0:1','cu-src-2','tuple',1,'I,J,K,L'],
        )
        # Action - Attempt to change the third CatCombination to a
        # terminal source
        class_name = 'tuple'
        path_0_1 = Gtk.TreePath.new_from_string('0:1')
        self.ctrlpage_ed._on_edited_apply_type_change(
            None, path_0_1, class_name
        )

        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_change_r_cu(self):
        model = self.ctrlpage_ed.model
        out_expected = (
            ['0','cu','CatCombination',42,self.cu_marker_other],
            ['0:0','cu-src-perm','Permutation',9001,self.cu_marker_one],
        )
        # Actions - Change the r-values on the CUs
        path_0 = Gtk.TreePath.new_from_string('0')
        path_0_0 = Gtk.TreePath.new_from_string('0:0')
        self.ctrlpage_ed._on_edited_apply_r_change(None, path_0, '42')
        self.ctrlpage_ed._on_edited_apply_r_change(None, path_0_0, '9001') 
        # Assertions
        out = get_path_stamped_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_editor_change_r_non_cu(self):
        model = self.ctrlpage_ed.model
        selection = self.ctrlpage_ed.selection
        ed_file_init = \
            '{"app":"slowcomb-demo","version":"1.1-SE"}\n'\
            '"0","lone-tuple","tuple","1","A,C,E"\n'
        stream = str_to_string_io(ed_file_init)
        self.ctrlpage_ed._open(stream)
        out_expected = ['0','lone-tuple','tuple',1,'A,C,E']
        # Action: Attempt to set a false r-value on a non-CU
        path_0 = Gtk.TreePath.new_from_string('0')
        self.ctrlpage_ed._on_edited_apply_r_change(None, path_0, '9001')
        out = get_path_stamped_rows(model)
        # Assertion
        self.assertEqual(out[0], out_expected)
            # PROTIP: get_path_stamped_rows only return rows in iter's,
            # even if there is only one row to return.

class TermViewerTests(unittest.TestCase):
    """Integration Tests to verify the operation of the Combinatorial Unit
    Term Viewer of the Intro Demo

    """
    format_version = '1.1-SE'
    demos_dir = 'slowcomb/demos'
    str_src_dir = os.path.join(os.path.abspath(os.path.curdir), demos_dir)
    str_src_file = MainUI.default_str_file_name
    str_src_path = os.path.join(str_src_dir, str_src_file)
    dw = MainUI(str_src_path=str_src_path)

    def setUp(self):
        self.ctrlpage_ed = self.dw._control_pages['EDIT']
        self.ctrlpage_vw = self.dw._view_page
        self.ed_file_test_default = \
            '{"app":"slowcomb-demo","version":"1.1-SE"}\n'\
            '"0","cu","Permutation","2",""\n'\
            '"0:0","cu-src","list","1","A,B,C,D"\n'
        # Action - Reset Editor and load test data, then display terms
        stream = str_to_string_io(self.ed_file_test_default)
        self.ctrlpage_ed._clear_and_reset()
        self.ctrlpage_ed._open(stream)
        self.ctrlpage_vw.page_settings.settings["output_json"] = False
        self.ctrlpage_vw._refresh()

    def test_self_test(self):
        """Verify that the initial contents of the test CU Term View Model is
        correct. This test must pass for all other tests to be considered
        valid.

        """
        model = self.ctrlpage_vw.model
        out_expected = (
            ['0', 'AB'],
            ['1', 'AC'],
            ['2', 'AD'],
            ['3', 'BA'],
            ['4', 'BC'],
            ['5', 'BD'],
            ['6', 'CA'],
            ['7', 'CB'],
            ['8', 'CD'],
            ['9', 'DA'],
            ['10', 'DB'],
            ['11', 'DC'],
        )
        # Assertions
        out = get_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_term_ranges(self):
        """Verify that the range setting works and causes the CU Term Viewer
        to only display the requested terms

        """
        model = self.ctrlpage_vw.model
        out_expected = (
            ['0', 'AB'],
            ['1', 'AC'],
            ['2', 'AD'],
            ['4', 'BA'],
            ['6', 'CA'],
            ['9', 'DA'],
            ['10', 'DB'],
            ['11', 'DC'],
        )
        # Action - set range limits and refresh
        range_str = "0-2,4,6,9-11"
        self.ctrlpage_vw.page_settings.settings["output_ranges"] = range_str
        self.ctrlpage_vw._refresh()
        # Assertions
        out = get_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_term_ranges_with_limit(self):
        """Verify that the term limit in the CU Term Viewer works and
        has priority over the range setting

        """
        model = self.ctrlpage_vw.model
        out_expected = (
            ['0', 'AB'],
            ['1', 'AC'],
            ['2', 'AD'],
            ['4', 'BA'],
            ['6', 'CA'],
        )
        # Action - set range and term limits, then refresh
        range_str = "0-2,4,6,9-11"
        limit = 3
        self.ctrlpage_vw.page_settings.settings["output_ranges"] = range_str
        self.ctrlpage_vw.page_settings.settings["term_limit"] = limit
        self.ctrlpage_vw._refresh()
        # Assertions
        out = get_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

    def test_term_limit(self):
        """Verify that the term limit in the CU Term Viewer works"""
        model = self.ctrlpage_vw.model
        out_expected = (
            ['0', 'AB'],
            ['1', 'AC'],
            ['2', 'AD'],
        )
        # Action - set range limits and refresh
        self.ctrlpage_vw.page_settings.settings["term_limit"] = 3
        self.ctrlpage_vw._refresh()
        # Assertions
        out = get_rows(model)
        for i in range(len(out)):
            with self.subTest(i=i):
                self.assertEqual(out[i], out_expected[i])

def get_rows(treemodel, **kwargs):
    """Convert the contents of a GTK TreeModel into a list of iter's
    containing data from the TreeModel, while leaving the contents intact.

    """
    def fn_get(model, treeiter, rows):
        rows = model[treeiter][:]
    rows = []
    args = (rows,)
    fn_dummy = lambda m,ti:0
    traverse_treemodel(
        treemodel,
        fn_get,
        fn_dummy,
        f_1_args=args,
        **kwargs
    )
    return rows

def get_path_stamped_rows(treemodel, **kwargs):
    """Convert the contents of a GTK TreeModel into a list of iter's
    containing data from the TreeModel, with the first column containing
    the address of the row in the TreeModel.

    """
    rows = []
    args = (rows,)
    fn_dummy = lambda m,ti:0
    traverse_treemodel(
        treemodel,
        trav_get_path_stamped_row,
        fn_dummy,
        f_1_args=args,
        **kwargs
    )
    return rows

def insert_into_model(model, rows, parent_path_str=None, position=-1):
    """Insert one or more rows into a GTK TreeModel.

    Arguments
    =========
    * model - GTK TreeModel to get data from

    * rows - An iter containing iters that represent a row in a GTK TreeModel

    * parent_path_str - A string representation of the path to a parent row in
      the TreeModel ``model`` where the rows will be inserted as sub-rows
      of the aforementioned row. This argument will only work with TreeModel's
      that support multiple levels of rows.

    * position - The number of rows under the parent row at which to insert
      the rows in ``rows``.

    """
    if parent_path_str is not None:
        path = Gtk.TreePath.new_from_string(parent_path_str)
        parent_ti = model.get_iter(path)
    else:
        parent_ti = None
    for r in rows:
        model.insert(parent_ti, position, r)

def str_to_string_io(string):
    """Creates an in-memory text stream (specifically, a StringIO object)
    from a string

    """
    out = io.StringIO()
    out.write(string)
    out.seek(0)
    return out

def trav_get_path_stamped_row(model, treeiter, out):
    """Function for use with traverse_treemodel which retrieves a traversed 
    row from a GTK TreeModel in the form of a list.

    Arguments
    =========
    * model - GTK TreeModel to get data from

    * treeiter - GTK TreeIter pointing to the target row in ``model`` to
        get the data from

    * out - Python list (or similar collection) to collect the output

    """
    row = model[treeiter][:]
    path = model.get_path(treeiter)
    row[0] = path.to_string()
    out.append(row)

