"""
Slowcomb Introductory Demo (and Micro-Framework for other demos)

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

# Objectives
# ----------
# The Slowcomb Introductory Demonstration is intended to show the basic
# operation of a Combinatorial Unit, a virtual list of terms of a combinatorial
# operation to allow terms to be addressed in a random manner. The strengths
# and weaknesses of such an approach to combinatorial operations will be
# explored, as well as its potential applications (and mis-applications).
#
# Prerequisites
# -------------
# This demonstration requires:
#  1. GTK+ 3 libraries (simply called 'GTK3' if you prefer), 
#     for the GUI widgets 
#  2. PyGObject to provide the necessary bindings to use GTK from Python.
#     The exact version targeted by this demo is 3.0.
#
# GTK is pretty much the lifeblood of a good number of GNU/Linux systems,
# especially when running GNOME as the desktop environment, so it is expected
# to be working properly on a vast majority of GNU/Linux systems out of
# the box. You may be required to install it if you are on other operating
# systems like the various BSDs, macOS or Windows.
#
# PyGObject may be installed via pip. If you are using virtual environments
# (VEs), many VE managers are set up to require manual installation for 
# each new VE created.
#
# Style and Miscellaneous Notes
# -----------------------------
# Methods in this file are meant to be arranged in this order:
#  1. By calling vector, or intended means of use. Event-called methods
#     (or callbacks) are placed first, followed by private functions, then
#     public functions, then first_run(), then _setup_ui(), then __repr__()
#     if applicable, and finally __init__().
#  2. Alphabetically, from a-z.
#
# Class-prefix naming (aka Hungarian notation) will be used for GTK 
# objects only, except for shared objects such as data models (e.g. TreeStore,
# ListStore), which may be used far beyond the scope of the original contexts
# in which they reside.
#
# Strings used in literal form in this file should be in single quotes,
# while double quotes are to be used for strings used as references and formats
# that resolve to something else. This is in spirit of conventions lifted from
# Unix shell programming.
#
# Programming experts may find some comments too verbose or even unnecessary.
# This file is intended as a beginner's guide to Python programming, or a
# refresher to those coming back to Python after a long period of time.
#
# CompSci veterans and Object Modelling architects note: the design patterns
# and algorithms used herein are highly likely to be sub-optimal.
#
# This demo is designed to be a single-executable, three-file application
# with minimal third-party dependencies. The only files required for full
# operation are this file, the string tables and the documentation file.
# The documentation file is completely optional.
#
# All code in this module is written to be reusable for other mini-demos
# that may be added to the Slowcomb Project.
#
# TODO: Error messages in exceptions are still hard coded strings. Is there
# a more efficient alternative to open up a means of using multi-lingual 
# error messages in exceptions?
#
# Acknowledgements
# ----------------
# This demo in essence a thoroughly modified version of an adaptation of sebp's
# Python GTK+3 Tutorial at https://python-gtk-3-tutorial.readthedocs.io/
#
# Additional help was consulted from Lazka's PGI Docs at
# https://lazka.github.io/pgi-docs/
#
# Special thanks to the creators and maintainers of Stack Overflow, and the
# contributors who wrote those valuable questions and responses. Yes, even if
# they were already a decade out of date at time of writing and could no
# longer be consulted in their original form.

import csv
import datetime
import itertools
import html
import io
import json
import os.path
from sys import argv
from slowcomb.slowcomb import Combination, CombinationWithRepeats, \
    CatCombination, Permutation, PermutationWithRepeats

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib
except ModuleNotFoundError:
    msg_no_gi_gtk3 = (
        'PyGObject does\'t seem to be installed on this system',
        'or virtual environment (VE).',
        'To be able to run this demo, please ensure that the',
        'Following are installed and working correctly:',
        '* PyGObject (see Python package manager)',
        '* GTK+3 (see operating system)',
    )
    for s in msg_no_gi_gtk3:
        print(s)

# 
# Helper Classes
#
class ProportionalPaned(Gtk.Paned):
    """A Gtk.Paned which retains the size proportion of its two paned areas
    (a.k.a. relative handle position) even after its parent has been resized.

    """
    def _on_draw_restore_proportion(self, widget, event):
        self._restore_proportion()

    def _on_position_change_save_proportion(self, widget, event):
        # Save the proportion of the paned areas when the handle is moved
        if self.hide2 is True or self._user_interaction is False:
            # Ignore requests to save proportion if position
            # changes are caused by resizing the parent widget by
            # means other than user interaction, such as the widget
            # expansions during the UI building process.
            return
        p = self.get_position()
        maxp = self.props.max_position
        self.proportion = p/maxp

    def _on_button_press(self, widget, event):
        self._user_interaction = True

    def _on_button_release(self, widget, event):
        self._user_interaction = False

    def show2(self):
        """Makes the second pane visible by bringing it out far enough
        to make it meaningfully visible and interactable.

        """
        # Push the second pane out a little more if the user has
        # dragged it too far to one side before hiding it. This is
        # intended to aid users with low-precision controls.
        if self._last_proportion > self.max_allowed_proportion:
            self.proportion = self.max_allowed_proportion - self.spring_factor
        elif self._last_proportion < self.min_allowed_proportion:
            self.proportion = self.spring_factor
        else:
            self.proportion = self._last_proportion
        self._restore_proportion()
    
    def hide2(self):
        """Makes the second pane invisible by moving the handle to the
        furthest position to the right or bottom, depending on the
        orientation

        """
        self._last_proportion = self.proportion
        self.proportion = 1.0
        self._restore_proportion()
 
    def toggle2(self):
        """Toggles hiding of the second pane. This is the bottom paned for 
        a paned areas that stack vertically, or the right pane horizontally-
        stacked areas.

        """
        if self.proportion < 1.0:
            self.hide2()
        else:
            self.show2()

    def _restore_proportion(self):
        self.set_position(self.proportion * self.props.max_position)

    def __init__(self, **kwargs):
        # Instance Properties
        self._default_proportion = 0.5
        self._user_interaction = False
        self.max_allowed_proportion = kwargs.pop('max_allowed_proportion',0.96)
        self.min_allowed_proportion = kwargs.pop('min_allowed_proportion',0.04)
        self.proportion = kwargs.pop('proportion', self._default_proportion)
        self.spring_factor = kwargs.pop('spring_factor', 0.13)
            # Proportion of smaller-to-larger pane to show
            # after exceeding min/max

            # PROTIP: The keyword arguments above are popped from kwargs 
            # to prevent them from being passed to the Gtk.Paned object
            # constructor, which refuses to initialise if unexpected keywords
            # are supplied.

        # Init Procedure
        self._last_proportion = self.proportion
        Gtk.Paned.__init__(self, **kwargs)
        self.connect(
            'notify::position', self._on_position_change_save_proportion
        )
        self.connect('button-press-event', self._on_button_press)
        self.connect('button-release-event', self._on_button_release)
            # PROTIP: The button-press-event and button-release-event
            # signals on the entire Paned are part of a hack to 
            # differentiate between user-initiated and system-initiated
            # changes to the handle position.
            # This is necessary as the mechanism used herein uses the
            # notify::position signal, which is emitted when the window is
            # resized without the user adjusting the handle, and when the
            # paned is hidden using hide2(), causing the paned to lose track
            # of the paned proportion.
            # See: StackOverflow Questions #1060039
            # "Detecting window resize from user"
            # https://stackoverflow.com/questions/1060039
        self.connect('draw', self._on_draw_restore_proportion)
            # PROTIP: The draw signal is emitted when a widget redraws,
            # which happens on pretty much any operation that changes
            # the appearance, size and position of the widget on the
            # screen.

class ModelSpec:
    """Model Specification, a Template class for aiding exchange of
    data betwen GTK TreeModel's and Python iter's, as well as constructing
    TreeModel's and their associated view widgets.
    This class is intended to contain methods for data insertion & retrieval,
    formatting, validation, and also GTK widget construction.

    There are five aspects to a ModelSpec:

    * column_names - Names for the columns in order from first to last

    * column_formatters - Methods that convert data to accepted formats.
        May be omitted by using a None in place. Arguments are
        (self, column_data, *args). The exact arguments are method-specific.

    * column_renderers - References to GTK CellRenderers

    * column_types - GTK TreeModel formats of the columns

    * column_validators - Methods to check if the data is acceptable for
        insertion into the TreeModel. Returns either True if the data is
        to be accepted, False otherwise.`May be omitted by using a None
        in place. Arguments are (self, column_data, *args). Exact arguments
        are method-specific.

    Formatters, renderers, types and validators are to be specified in 
    iters, in the same order as column names.

    For example, column 0 would be named by a string in column_names[0].
    Before inserting a row, the method referenced in column_formatters[0]
    will be called to convert the input into an acceptable format. Then,
    the method in column_validators[0] will be called to check the input,
    and so on...

    In order to create a TreeModel, column 0's data type will be contained
    in column_types[0]. To create an associated TreeView, column_renderers[0]
    could reference a GTK CellRenderer for use with the column.

    The same process is repeated for types and validators.

    Notes
    =====
    Column data validation is yet to be properly implemented at time
    of writing.

    """
    # Properties
    column_names = None
    column_formatters = []
    column_renderers = []
    column_types = []
    column_validators = [] 
    strings = {}
    # Generic functions
    fn_to_int = lambda self, x, *args: int(x) # Convert to int
    fn_zero = lambda self, x, *args: 0 # Always return zero

    def dict_to_row(self, spec_dict):
        """Create an iter containing appropriately-formatted rows for
        insertion into a GTK TreeModel from a Python dict, or similar
        string-addressable array. Values with keys that are not
        supported by this specification will be silently ignored.

        """
        row = []
        for n in self.column_names:
            value = spec_dict.get(n, None)
            if value is not None:
                row.append(spec_dict[n])
        return self.iter_to_row(row)

    def get_gtk_treeview_column(self, name, **kwargs):
        """Builds and returns a GTK TreeViewColumn for use with a
        TreeView.

        Optional Arguments
        ==================
        * string_dict - a dict to be used as a string lookup table, when
            string aliases instead of hardcoded string literals are used
            for column names. 

        * renderer_callbacks - a dict

        Format for the ``renderer_callbacks`` Argument
        ==============================================
        Any callback to be assigned to the ColumnRenderer of the TreeViewColumn
        should be passed in as a dict or similar string collection.
        The key of the callback specifier should be the same name as the GTK
        signal emitted by the ColumnRenderer.
        
        Example: a column triggers the function ``start_edit_help`` when it
        is edited, and the function ``save_data`` when the data in it changes.
        Its callback specification would look like:

        { 'edited' : self.start_edit_help, 'editing-started' : self.save_data }

        PROTIP: This example involves the use of this method from within a
            class, thus the ``self``.

        """
        string_dict = kwargs.get('string_dict', self._strings)
        renderer_callbacks = kwargs.get('renderer_callbacks', None)
        i = self.column_names.index(name)
        colrend = self.column_renderers[i]
        if renderer_callbacks is not None:
            signal_names = renderer_callbacks.keys()
            for sn in signal_names:
                colrend.connect(sn, renderer_callbacks[sn])
        if string_dict is not None:
            sdkey = self.column_names[i]
            column_name = string_dict[sdkey]
        else:
            column_name = self.column_names[i]
        tvcol = Gtk.TreeViewColumn(
            column_name,
            self.column_renderers[i],
            text=i
        )
        tvcol.set_resizable(True)
        return tvcol

    def iter_to_row(self, input_iter):
        """Format an iter in order to make it suitable for insertion into a
        GTK TreeModel.

        """
        n_cols = len(input_iter)
        out = []
        if n_cols != len(self.column_names):
            raise ValueError('Mismatched number of columns in input iter')
        for i in range(n_cols):
            fn_format = self.column_formatters[i]
            if fn_format is not None:
                formatted_data = fn_format(input_iter[i], input_iter)
                out.append(formatted_data)
            else:
                out.append(input_iter[i])
            fn_valid = self.column_validators[i]
            if fn_valid is not None:
                if fn_valid(out[i]) is not True:
                    raise ValueError
        return out 
    
    def get_column_index(self, name):
        if name in self.column_names:
            return self.column_names.index(name)
        else:
            return None

    def get_column_data(self, row_iter, col_name):
        i = self.get_column_index(col_name)
        if i is not None:
            return row_iter[i]
        else:
            raise NameError('Column name not in spec')

    def reformat_row(self, row_iter):
        """Reapply formatting on existing data in an iter. This is intended
        for use with GTK TreeModels, in order to keep data compliant to the 
        ModelSpec's format, particularly after editing.

        This method modifies ``row_iter`` in place.

        """
        for n in self.column_names:
            i = self.get_column_index(n)
            fn_format = self.column_formatters[i]
            if fn_format is not None:
                reformatted_data = fn_format(row_iter[i], row_iter)
                self.set_column_data(row_iter, n, reformatted_data)

    def set_column_data(self, row_iter, col_name, data):
        i = self.get_column_index(col_name)
        if i is not None:
            row_iter[i] = data
        else:
            raise NameError('Column name not in spec')

    def _text(self, name):
        # Retrieves text from the UI Page's string dict.
        return self._strings.get(name, '🤷')
            # PROTIP: The dict is intended to be an alternative to
            #  using deeply-embedded, hardcoded strings.

    def __init__(self, **kwargs):
        self._strings = kwargs.get("strings", None)

class CUEditorModelSpec(ModelSpec):
    """Combinatorial Unit Configuration Editor Model Specification. This model 
    spec governs the data format used in the Editor page in this demo.

    """
    multi_source_cu_classes = { CatCombination, }
    non_cu_classes = { tuple, list, }
    simple_cu_classes = {
        Combination,
        CombinationWithRepeats,
        Permutation,
        PermutationWithRepeats,
    }

    def _format_data_column(self, column_data, row):
        out = '' 
        cu_class_name = self.get_column_data(row, 'editor-model-type')
        cu_class = self.get_class_from_name(cu_class_name)
        if self.is_supported_multi_source_cu(cu_class):
            out = self._text('editor-model-cu-marker-other')
        elif self.is_supported_cu(cu_class):
            out = self._text('editor-model-cu-marker-one')
        else:
            out = column_data
        return out

    def _get_all_supported_classes(self):
        # Prepare an iter of supported CU classes
        chain = itertools.chain(
            self.multi_source_cu_classes,
            self.simple_cu_classes,
            self.non_cu_classes
        )
        classes = []
        for c in chain:
            classes.append(c)
        return classes

    def _get_class_choice_gtk_renderer(self):
        # Prepare a GTK CellRendererCombo that presents a choice of
        # supported CU classes (known as 'types' in the UI).
        # This method only works after supported_classes is set.
        listst_choices = Gtk.ListStore(str)
        for c in self.supported_classes:
            listst_choices.append( (c.__name__,) )
        colrend = Gtk.CellRendererCombo(
            model=listst_choices,
            text_column=0,
            editable=True,
            has_entry=False
        )
        return colrend 

    def _get_supported_classes_dict(self):
        # Prepare the dictionary of supported CU classes that allow class
        # objects to be referenced by a string name
        cdict = {}
        classes = self.supported_classes
        for c in classes:
            name = c.__name__
            cdict[name] = c
        return cdict

    def get_class_from_name(self, name):
        return self.supported_classes_dict.get(name, None)

    def is_supported_multi_source_cu(self, cu_class):
        """ Determine if a particular Combainatorial Unit is supported *and*
        uses multiple-sources

        """
        return cu_class in self.multi_source_cu_classes
            # PROTIP: Compound CUs are defined as CUs that use multiple
            # source sequences to derive terms, like CatCombination.

    def is_supported_cu(self, cu_class):
        """ Determine if the editor supports a particular type of Combinatorial
        Unit.

        """
        return cu_class in self.supported_cu_classes

    def is_supported_non_cu(self, seq_class):
        is_not_cu = seq_class not in self.supported_cu_classes
        is_seq = seq_class in self.non_cu_classes
        is_supported_non_cu = (is_not_cu and is_seq) is True
        return is_supported_non_cu

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.supported_classes = self._get_all_supported_classes()
        self.supported_classes_dict = self._get_supported_classes_dict()
        self.supported_cu_classes = self.simple_cu_classes.union(
            self.multi_source_cu_classes
        )

        # GTK TreeView Cell Renderers
        ren_t = Gtk.CellRendererText()
        ren_name = Gtk.CellRendererText(editable=True)
        ren_type = self._get_class_choice_gtk_renderer()
        ren_r = Gtk.CellRendererText(editable=True)
        ren_data = Gtk.CellRendererText(editable=True)
            # PROTIP: As of GTK+ 3.0, Reusing CellRenderers will cause
            #  event handlers assigned to one renderer to trigger for
            #  *all* instances of the same renderer. For example, a handler
            #  to register changes to a Name column would end up overwriting
            #  the data in a Description column with input into the former,
            #  if the two columns use the same CellRenderer.
 
        # Column Specs
        self.column_names = (
            'editor-model-address',
            'editor-model-name',
            'editor-model-type',
            'editor-model-r',
            'editor-model-data',
        )
            # PROTIP: As with all Slowcomb Demos, the first TreeModel
            #  column is for addressing, and the last one for data.
            # PROTIP: The column names herein are actually placeholder
            #  names. The actual names are in the text string file,
            #  use these names as keys to look up the actual name in the
            #  string file.
        self.column_formatters = (
            None, None, None, self.fn_to_int, self._format_data_column
        )
        self.column_renderers = (ren_t, ren_name, ren_type, ren_r, ren_data)
        self.column_types = (str, str, str, int, str)
        self.column_validators = (None, None, None, None, None) 

class CUTermViewModelSpec(ModelSpec):
    """Combinatorial Unit Term Viewer Model Specification. This model spec
    governs the format of the data presented on the Term output view in this
    demo.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            # PROTIP: Two ways of instantiating a subclass have been in use
            # in this demo. 
        rend = Gtk.CellRendererText() 
            # PROTIP: CellRenderers can be safely reused for every 
            # TreeView column in this model spec as the CU Term Viewer
            # is a read-only view.
        self.column_names = ('termview-model-i', 'termview-model-term')
        self.column_types = (int, str)
        self.column_formatters = (self.fn_to_int, None)
        self.column_renderers = (rend, rend)
        self.column_validators = (None, None)

class MessageAreaModelSpec(ModelSpec):

    def __init__(self, **kwargs):
        ModelSpec.__init__(self, **kwargs)

        rend = Gtk.CellRendererText()
        self.column_names = (
            'messagearea-code',
            'messagearea-time',
            'messagearea-message'
        )
        self.column_types = (str, str, str)
        self.column_formatters = (None, None, None)
        self.column_renderers = (rend, rend, rend)
        self.column_validators = (None, None, None)

class ControlsPage(Gtk.Box):
    """This is the Slowcomb Demo UI Control Panel Page Design
    Reference Class. It is intended to be a foundation for building
    user controls in Slowcomb demos.

    """
    def _get_message_code(self):
        fmt = "{0}{1}"
        out = fmt.format(self._message_code_prefix, self._message_count)
        return out
    
    def _get_error_message_code(self):
        fmt = "{0}ERR{1}"
        out = fmt.format(self._message_code_prefix, self._message_count)
        return out

    def _text(self, name):
        # Retrieves text from the UI Page's string dict.
        # PROTIP: The dict is intended to be an alternative to
        #  using deeply-embedded, hardcoded strings.
        return self._strings.get(name, '🤷')

    def spec_to_toolitem_dict(self, spec_dict):
        """Generate a dict of controls ready to use with GTK Toolbar's,
        based on a specification.

        Format of ``spec_dict``
        =======================
        Controls are specified in the form of a dictionary. Each control
        must have a prefixed name, which is also used as the key to the
        specification in ``spec_dict``. Currently, the only supported prefix
        is ``button``, which generates GTK Buttons. All names must be strings.

        The format is as follows:
        'widget-spec-name' : *arg_specs

        * widget-spec-name: name given to the specification

        * arg_specs: a tuple of arguments to define the control

        The arg_specs for ``button`` is as follows:

        'button-spec-name' : ('label-id','icon-name',callback,*callback_args)

        * widget-spec-name must begin with the prefix ``button``.

        * label-id: A string table identifier to identify the string
            to be used as the button's caption. Mnemonics are enabled.
            If the string lookup fails, the string is used literally
            as the label text.

         * icon-name: The name of the icon to be used on the button.
            Use standard icon names according to the GNOME Icon Naming
            Specification.

         * callback: The method or function to be called when the button
            is ``clicked``.

         * callback_args: A tuple containing arguments to be passed to 
            ``callback``. The tuple is expanded into multiple arguments.

        Names given to items in the specification are re-used for the
        returned control dict. A specification like this:
        
        {
            'button-play' : (
                'button-go', 'media-play', self._on_click_play, (self.pos,)
            ),
            'button-stop' : (
                'button-stop', 'media-play', self._on_click_play, (self.pos,)
            ),
        }

        Returns something like this:

        { 'button-play' : <Gtk.ToolButton>, 'button-stop' : <Gtk.ToolButton> }

        """
        def get_button(label_text, icon_name, callback_spec):
            text = self._text(label_text)
            if text == '🤷':
                use_text = label_text
            else:
                use_text = text
            image_icon = None
            if icon_name is not None:
                image_icon = Gtk.Image.new_from_icon_name(
                    icon_name,
                    8 
                )
            label = Gtk.Label.new_with_mnemonic(use_text)
            toolbutton = Gtk.ToolButton.new(image_icon, None)
            toolbutton.set_label_widget(label)
            toolbutton.connect("clicked", *callback_spec)
            toolbutton.set_homogeneous(False)
            return toolbutton
            
        handlers = {
            'button' : get_button,
        }
            # TODO: More handlers may be added in the future to 
            # support for more widgets.
            # The handler pattern used herein is loosely based on
            # R. Hettinger's (2010) example "Compute Memory Footprint
            # and Its Contents".
            # See: https://code.activesite.com/recipes/577504
        names = spec_dict.keys()
        toolbar_item_dict = {}
        for n in names:
            prefix = (n.split('-'))[0]
            handler = handlers[prefix]
            toolbar_item_new = handler(*spec_dict[n])
            toolbar_item_dict[n] = toolbar_item_new
        return toolbar_item_dict    

    def message(self, message, code=None, detail=None):
        """Leaves a message in the main window's message area"""
        if code is None:
            code = self._get_message_code()
        self._message_count += 1
        self.main_window.messages.append(code, message, detail)

    def first_run(self):
        raise NotImplementedError

    def _setup_ui(self):
        raise NotImplementedError

    def __init__(self, **kwargs):
        self._message_code_prefix = kwargs.pop(
            'message_code_prefix','UNDEF'
        )
        self._message_count = 0
        self._strings = kwargs.pop("strings", {})
        self._widgets = {}

        self.main_window = kwargs.pop('main_window', None)
            # PROTIP: This property allows control panels to
            # communicate with the main window.
        self.statusbar_context_id = None
        self.tab_label_text = kwargs.pop('tab_label_text', 'Unnamed')
        Gtk.Box.__init__(self, **kwargs)
        self._setup_ui()

class CUEditorControlsPage(ControlsPage):
    """Controls for visually creating and exploring Combinatorial Units, the
    building blocks of Slowcomb's randomly addressable combinatorics.

    """
    _new_cu_data = (
            'A,B,C,D', 'E,F,G,H', 'I,J,K,L', 'M,N,O,P',
            'Q,R,S,T', 'U,V,W,X', 'Y,Z,*,#',
        )
    _new_cu_src_spec = {
        'editor-model-address' : '0',
        'editor-model-name' : 'cu',
        'editor-model-type' : 'tuple',
        'editor-model-r' : 1,
    }
    em_spec = None 
    _insert_count = 0
    model = None
    selection = None
    treeview = None 

    def _on_clicked_request_add(self, widget):
        model, treeiter = self.selection.get_selected()
        if treeiter is None:
            # No CU or any item in editor selected
            self.message(self._text("editor-error-source-no-target"))
            return
        target_row = model[treeiter]
        src_count = model.iter_n_children(treeiter)
        class_name = self.em_spec.get_column_data(
            target_row, "editor-model-type"
        )
        target_cu_class = self.em_spec.get_class_from_name(class_name)
        new_cu_src_data = self._get_cycling_string(self._new_cu_data)
        cu_spec = self._new_cu_src_spec.copy()
        cu_spec["editor-model-data"] = new_cu_src_data
        if self.em_spec.is_supported_multi_source_cu(target_cu_class) is True:
            # Adding to multi-source CUs
            name_prefix = self.em_spec.get_column_data(
                target_row, "editor-model-name"
            )
            name = "{}-src-{}".format(name_prefix, src_count)
            cu_spec["editor-model-name"] = name
            self._add(
                cu_spec,
                self.model,
                treeiter=treeiter,
                add_mode='under'
            )
            path = model.get_path(treeiter)
            self.treeview.expand_row(path, False)
        elif self.em_spec.is_supported_cu(target_cu_class) is True:
            # Adding to single-source CUs
            if src_count >= 1:
                self.message(self._text("editor-error-source-add-limit"))
                return
            else:
                name_prefix = self.em_spec.get_column_data(
                    target_row, "editor-model-name"
                )
                name = "{}-src".format(name_prefix)
                cu_spec["editor-model-name"] = name
                self._add(
                    cu_spec,
                    self.model,
                    treeiter=treeiter,
                    add_mode='under'
                )
                path = model.get_path(treeiter)
                self.treeview.expand_row(path, False)
        else:
            self.message(self._text("editor-error-source-add-limit"))
            return

    def _on_clicked_request_clear(self, widget):
        self._clear_and_reset()

    def _on_clicked_request_delete(self, widget):
        model, treeiter = self.selection.get_selected()
        path = model.get_path(treeiter)
        path_str = path.to_string()
        if path_str == "0":
            # Prevent deletion of the root CU
            self.message(self._text("editor-error-delete-root"))
            return
        else:
            model.remove(treeiter)

    def _on_clicked_request_open(self, widget):
        buttons = (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
            # PROTIP: Use Gtk.STOCK_ buttons to make life easier, as they
            # return buttons that are matched to the specifications of the
            # underlying platform the application is running on.
            # PROTIP: Buttons are specified in a single iter, alternating
            # between button label and their response type.
            # PROTIP: Buttons will appear the order they are specified in
            # the iter. The agreed standard for file dialogs seems to be
            # cancellation before confirmation (e.g. Cancel, Save)
        filters = (
            get_non_file_filter(),
        )
        filepath = get_path_with_dialog(
            action=Gtk.FileChooserAction.OPEN,
            title=self._text("editor-open-dialog-title"),
            buttons=buttons,
            filters=filters
        )
        with open(filepath, 'r') as f_r:
            self._open(f_r)
        filename = os.path.basename(filepath)
        self.main_window.update_title(filename)

    def _open(self, stream_obj):
        # Load a CU configuration directly from a stream object.
        # This method should be invoked from within a Context Manager
        # (such as the section starting with ``with open()`` in 
        # ``_on_clicked_request_open()``.
        # The implementation style of this method is intended to allow
        # easier automated testing of the file loading routine.
        try:
            sig_raw = stream_obj.readline()
            json_dec = json.JSONDecoder()
            meta = json_dec.decode(sig_raw)
            # Verify metadata
            expected_app = 'slowcomb-demo'
            expected_version = '1.1-SE'
            if meta['app']==expected_app and meta['version']==expected_version:
                self.model.clear()
                self.model_termview.clear()
                csv_sample = stream_obj.readline()
                dialect = csv.Sniffer().sniff(csv_sample)
                stream_obj.seek(len(sig_raw), 0)
                reader = csv.reader(stream_obj, dialect)
                csv_to_model(reader, self.model, self.em_spec)
                treeiter = self.model.get_iter_first()
                self._reset_addresses(treeiter)
                self.treeview.expand_all()
                self.comment = meta.get('comment', self._text("comment-none"))
                self._show_comment_in_tab(self.comment)
            else:
                self.message(self._text("file-error-wrong-format"))
        except json.decoder.JSONDecodeError:
            self.message(self._text("file-error-wrong-format"))
                
    def _show_comment_in_tab(self, comment):
        txtbuf_c = self.main_window.shared_data['comments-text-buffer']
        txtbuf_c.set_text('')
        txtbuf_c.set_text(comment)

    def _on_clicked_request_save(self, widget):
        buttons = (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        filters = (
            get_non_file_filter(),
        )
        filepath = get_path_with_dialog(
            action=Gtk.FileChooserAction.SAVE,
            buttons=buttons,
            filters=filters,
            overwrite_confirmation=True,
            title=self._text('editor-save-dialog-title')
        )
        json_enc = json.JSONEncoder()
        meta_dict = {
            "app" : "slowcomb-demo",
            "version" : "1.1-SE",
        }
        sig = json_enc.encode(meta_dict)
        sig = ''.join( (sig, '\n') )
        with open(filepath, 'w') as f_w:
            f_w.write(sig)
            model_to_csv(self.model, f_w)

    def _on_edited_apply_name_change(self, widget, path, text):
        target_row = self.model[path]
        self.em_spec.set_column_data(target_row, 'editor-model-name', text)

    def _on_edited_apply_type_change(self, widget, path, text):
        target_row = self.model[path]
        treeiter = self.model.get_iter(path)
        src_count = self.model.iter_n_children(treeiter)
        current_class_name = self.em_spec.get_column_data(
            target_row,'editor-model-type'
        )
        current_class = self.em_spec.get_class_from_name(current_class_name)
        new_class = self.em_spec.get_class_from_name(text)
        if self.em_spec.is_supported_multi_source_cu(current_class) is True:
            if src_count > 1:
            # Prevent change from multi-source CU to non-multi-source CU
            # if there are multiple attached sources. This is to prevent
            # accidental loss of sources
                self.message(self._text("editor-error-multi-to-single"))
                return
        elif self.em_spec.is_supported_non_cu(new_class) is True:
            if src_count >= 1:
                self.message(self._text("editor-error-cu-to-terminal"))
                return
            self.em_spec.set_column_data(target_row, "editor-model-r", 1)
                # The r-value of a terminal source is always shown as one.
                # This is rather mathematically incorrect, as lists are
                # not combinatorial units. Non-CU sequences are given a
                # ficticious r-value for technical convenience. This is
                # rationalised by the fact that their output is similar
                # to Combinations where r=1.
        self.em_spec.set_column_data(target_row, "editor-model-type", text)
        self._apply_default_data(self.model, path)
    
    def _on_edited_apply_data_change(self, widget, path, text):
        target_row = self.model[path]
        i_type_col = self.em_spec.get_column_index('editor-model-type')
        i_data_col = self.em_spec.get_column_index('editor-model-data')
        iclass_name=self.em_spec.get_column_data(target_row,'editor-model-type')
        iclass = self.em_spec.get_class_from_name(iclass_name)
        target_row[i_data_col] = text
        self.em_spec.reformat_row(target_row)

    def _on_edited_apply_r_change(self, widget, path, text):
        target_row = self.model[path]
        i_r_col = self.em_spec.get_column_index('editor-model-r')
        i_type_col = self.em_spec.get_column_index('editor-model-type')
        cu_class_name = target_row[i_type_col]
        cu_class = self.em_spec.get_class_from_name(cu_class_name)
        if self.em_spec.is_supported_non_cu(cu_class) is True:
            target_row[i_r_col] = 1
        else:
            target_row[i_r_col] = int(text)
        # TODO: Implement early invalid r-value detection, using ModelSpec
        # column validator functions.

    def _add(self, row_spec, model, treeiter=None, add_mode='after'):
        # Add a source to the CU configuration
        row_data = self.em_spec.dict_to_row(row_spec)
        if treeiter is not None:
            # Automatically add to the containing multi-source CU
            # when a sub-CU is selected
            treeiter_parent = None
            if add_mode == 'after':
                treeiter_parent = model.iter_parent(treeiter)
                treeiter_sibling = treeiter
            if add_mode == 'under':
                treeiter_parent = treeiter
                treeiter_sibling = None
            treeiter = model.insert(treeiter_parent, -1, row_data)
        else:
            # Add a CU if the configuration is empty
            treeiter = model.insert(None, -1, row_data)
        new_row = model[treeiter]
        new_path = model.get_path(treeiter)
        path_str = new_path.to_string()
        self.em_spec.set_column_data(new_row, 'editor-model-address', path_str)
        self._insert_count += 1
        return treeiter
    
    def _apply_default_data(self, model, path):
        # Apply placeholder data to terminal sources converted from CUs
        treeiter = model.get_iter(path)
        target_row = model[path]
        cu_class_name = self.em_spec.get_column_data( 
            target_row,'editor-model-type'
        )
        cu_class = self.em_spec.get_class_from_name(cu_class_name)
        if self.em_spec.is_supported_cu(cu_class) is False:
            text = self._get_cycling_string(self._new_cu_data)
            self.em_spec.set_column_data(target_row, 'editor-model-data', text)
        self.em_spec.reformat_row(target_row)

    def _clear_and_reset(self):
        # Return the Editor to its default state
        self.model.clear()
        self._insert_count = 0
        new_cu_data = self._get_cycling_string(self._new_cu_data)
        new_cu_spec = {
            'editor-model-address' : '0',
            'editor-model-name' : 'cu',
            'editor-model-type' : 'Permutation',
            'editor-model-r' : 3,
            'editor-model-data' : ''
        }
        new_cu_src_spec = {
            'editor-model-address' : '0',
            'editor-model-name' : 'cu-src',
            'editor-model-type' : 'tuple',
            'editor-model-r' : 1,
            'editor-model-data' : new_cu_data
        }
        treeiter = self._add(new_cu_spec, self.model)
        self._add(
            new_cu_src_spec,
            self.model,
            treeiter=treeiter,
            add_mode='under'
        )
        self._show_comment_in_tab(self._text("comment-welcome"))
        self.treeview.expand_all()

    def _get_cycling_string(self, str_tuple, numbered=False):
        i = self._insert_count % len(str_tuple)
        output = str_tuple[i]
        if numbered is True:
            n_suffix = self._insert_count // len(str_tuple)
            if n_suffix >= 1:
                output = ''.join( (output, '-', str(n_suffix+1)) )
        return output

    def _on_row_i_reset_addresses(self, model, path, treeiter):
        startiter = model.get_iter(path)
        self._reset_addresses(startiter)

    def _on_row_d_reset_addresses(self, model, path):
        # Update CU addresses in a TreeModel after point of deletion
        try:
            treeiter = model.get_iter(path)
            self._reset_addresses(treeiter)
        except ValueError:
            treeiter = model.get_iter_first()
            self._reset_addresses(treeiter)

    def _on_clicked_request_copy(self, widget):
        model, treeiter = self.selection.get_selected()
        self._copy(model, treeiter)

    def _on_clicked_request_paste(self, widget):
        model, treeiter = self.selection.get_selected()
        if treeiter is None:
            self.message(self._text("editor-error-source-no-target"))
            return
        target_row = model[treeiter]
        src_count = model.iter_n_children(treeiter)
        cu_class_name = self.em_spec.get_column_data(
            target_row, 'editor-model-type'
        )
        cu_class = self.em_spec.get_class_from_name(cu_class_name)
        if self.em_spec.is_supported_multi_source_cu(cu_class) is False:
            if self.em_spec.is_supported_cu(cu_class) is True:
                if src_count >= 1:
                    self.message(self._text("editor-error-source-add-limit"))
                    return
            else:
                self.message(self._text("editor-error-source-add-terminal"))
                return
        self._paste(model, treeiter, self._clipboard, mode='under')
        path = model.get_path(treeiter)
        self.treeview.expand_row(path, False)

    def _copy(self, model, treeiter, **kwargs):
        model, treeiter = self.selection.get_selected()
        clipboard = kwargs.get("clipboard", self._clipboard)
        file_obj = io.StringIO()
        limits = (1,)
        model_to_csv(
            model, file_obj, limits=limits, treeiter_start=treeiter
        )
        clipboard.set_text(file_obj.getvalue(),-1)

    def _paste(self, model, treeiter, clipboard, mode=None):
        text = clipboard.wait_for_text()
        if text is not None:
            rows_raw = text.split('\n')
            dialect = csv.Sniffer().sniff(rows_raw[0])
            reader = csv.reader(rows_raw, dialect)
            csv_to_model(
                reader, model, self.em_spec, treeiter=treeiter, mode=mode
            )
        else:
            self.message(self._text("editor-error-clipboard-empty"))
            
    def _reset_addresses(self, treeiter_start, limits=None):
        dummy = lambda model,treeiter: 0

        def _stamp_path(model, treeiter):
            path = model.get_path(treeiter)
            pathstr = path.to_string()
            model[treeiter][0] = pathstr

        traverse_treemodel(
            self.model,
            _stamp_path,
            dummy,
            treeiter_start=treeiter_start,
            limits=limits
        )
            
    def first_run(self):
        self.model_termview = self.main_window.shared_data['term-view-model']
        self._clear_and_reset()
        statusbar = self.main_window.shared_data['statusbar']
        self.statusbar_context_id = statusbar.get_context_id(self.tab_label_text)
        self.model.connect('row-deleted', self._on_row_d_reset_addresses)
        self.model.connect('row-inserted', self._on_row_i_reset_addresses)

    def _setup_ui(self):
        # PROTIP: GTK widgets tend to be utilised at the class level.
        # Often, if two variations of the same widget is desired, one cannot
        # create two instances of the same widget class. Instead, the correct
        # way to do this in GTK is to use two classes, one for each variation.

        # Resources and Links
        self._clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.em_spec = CUEditorModelSpec(strings=self._strings)

        # Config Controls Box
        box_cu_config = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.pack_start(box_cu_config, True, True, 0)

        # Config Banner
        label = Gtk.Label()
        label.set_markup(self._text("editor-title"))
        box_cu_config.pack_start(label, False, False, 2)

        # Config Toolbar
        toolbar = Gtk.Toolbar.new()
        toolbar.set_style(Gtk.ToolbarStyle.TEXT)
        dummy_fn = lambda self,x:print(x)
        toolbar_button_spec = {
            "button-clear" : (
                "button-clear",
                "edit-clear",
                (self._on_clicked_request_clear,)
            ),
            "button-add-source" : (
                "button-add-source",
                "list-add",
                (self._on_clicked_request_add,)
            ),
            "button-remove-source" : (
                "button-remove-source",
                "list-remove",
                (self._on_clicked_request_delete,)
            ),
            "button-copy" : (
                "button-copy",
                "edit-copy",
                (self._on_clicked_request_copy,)
            ),
            "button-paste" : (
                "button-paste",
                "edit-paste",
                (self._on_clicked_request_paste,)
            ),
            "button-open" : (
                "button-open",
                "document-open",
                (self._on_clicked_request_open,)
            ),
            "button-save" : (
                "button-save",
                "document-save",
                (self._on_clicked_request_save,)
            ),
            "button-close-application" : (
                "button-close-application",
                "application-exit",
                (Gtk.main_quit,)
            ),
        }
        self.toolbar_items = self.spec_to_toolitem_dict(toolbar_button_spec)
        for ti in self.toolbar_items.values():
            toolbar.insert(ti, -1)
        box_cu_config.pack_start(toolbar, False, False, 0)

        # Config TreeView
        self.model= Gtk.TreeStore(*self.em_spec.column_types)
        self.treeview = Gtk.TreeView(model=self.model)
        self.selection = self.treeview.get_selection()
        string_dict = self._strings
        callback_spec = {
            'editor-model-data' : {'edited':self._on_edited_apply_data_change},
            'editor-model-name' : {'edited':self._on_edited_apply_name_change},
            'editor-model-type' : {'edited':self._on_edited_apply_type_change},
            'editor-model-r' : {'edited':self._on_edited_apply_r_change}
        }
        for n in self.em_spec.column_names:
            treeview_column = self.em_spec.get_gtk_treeview_column(
                n, 
                string_dict=string_dict,
                renderer_callbacks=callback_spec.get(n)
            )
            self.treeview.append_column(treeview_column)
        box_cu_config.pack_start(self.treeview, True, True, 0)


    def __init__(self, **kwargs):
        # Properties
        self.default_class_name = 'Combination'
        ControlsPage.__init__(
            self,
            orientation=Gtk.Orientation.VERTICAL,
            margin=4,
            tab_label_text='_Editor',
            message_code_prefix = 'EDIT',
            **kwargs
        )
        # Share model with main window
        self.main_window.shared_data['editor-selection'] = self.selection
        self.main_window.shared_data['editor-model'] = self.model

class CUTermViewSettingsPage(ControlsPage):
    """Control Panel for configuring the CU Term View Controls Page"""
    _safe_term_limit = 300
        # Intended to be the threshold at which a refresh is expected to take
        # too long to complete due to the sheer number of terms involved.
    _spacing_px = 4
    _strings = None
    comment = None
    message_code_prefix = 'TVSET'
    settings = {
        "output_json" : True,
        "output_ranges" : '',
        "term_limit" : 500,
        "compressed_ranges" : False,
    }

    def _on_changed_update_output_ranges(self, widget):
        text = widget.get_chars(0,-1)
        self.settings["output_ranges"] = text

    def _on_changed_update_term_limit(self, widget):
        text = widget.get_chars(0,-1)
        try:
            n = int(text)
        except ValueError:
            n = 0
        self.settings["term_limit"] = n
        if n <= self._safe_term_limit:
            # Auto-refresh if there is just a handful of terms to go through,
            # because why not?
            self.parent_page._refresh()

    def _on_toggled_set_compressed_ranges(self, widget):
        self.settings["compressed_ranges"] = widget.get_active()

    def _on_toggled_set_json(self, widget):
        self.settings["output_json"] = widget.get_active()
        self.parent_page._refresh()
            # PROTIP: This setting triggers an automatic refresh of
            # the term view, to prevent the outputs from looking too
            # different from the user's expectations

    def _setup_ui(self):
        # Output Format Settings
        frame_fm = Gtk.Frame(label=self._text("termsettings-out-format-title"))
        self.pack_start(frame_fm, True, True, self._spacing_px)
        box_fm= Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin=self._spacing_px
        )
        frame_fm.add(box_fm)
        checkb_json = Gtk.CheckButton.new_with_mnemonic(
            self._text("termsettings-out-json")
        )
        checkb_json.set_active(self.settings["output_json"])
        checkb_json.connect("toggled", self._on_toggled_set_json)
        box_fm.pack_start(checkb_json, True, True, self._spacing_px)

        # Output Range Settings 
        text_range = self._text("termsettings-out-range-title")
        frame_range = Gtk.Frame(label=text_range)
        self.pack_start(frame_range, True, True, self._spacing_px)
        box_outconf = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=4)
        frame_range.add(box_outconf)

        entry_limit = Gtk.Entry()
        entry_limit.set_text( str(self.settings["term_limit"]) )
        entry_limit.connect("changed", self._on_changed_update_term_limit)
        text_limit = self._text("termsettings-out-limit")
        label_limit = Gtk.Label().new_with_mnemonic(text_limit)
        label_limit.set_mnemonic_widget(entry_limit)
        box_outconf.pack_start(label_limit, True, True, self._spacing_px)
        box_outconf.pack_start(entry_limit, True, True, self._spacing_px)

        entry_outranges = Gtk.Entry()
        entry_outranges.connect(
            "changed", self._on_changed_update_output_ranges
        )
        text_outranges = self._text("termsettings-out-range-entry")
        label_outranges = Gtk.Label().new_with_mnemonic(text_outranges)
        label_outranges.set_mnemonic_widget(entry_outranges)
        box_outconf.pack_start(label_outranges, True, True, self._spacing_px)
        box_outconf.pack_start(entry_outranges, True, True, self._spacing_px)
        text_comp = self._text("termsettings-out-compressed-addr")
        checkb_comp = Gtk.CheckButton().new_with_mnemonic(text_comp)
        checkb_comp.set_active(self.settings["compressed_ranges"])
        checkb_comp.connect(
            "toggled",
            self._on_toggled_set_compressed_ranges
        )
        checkb_comp.set_sensitive(False)
        box_outconf.pack_start(checkb_comp, True, True, self._spacing_px)

    def __init__(self, **kwargs):
        self.parent_page = kwargs.pop("parent_page")
        ControlsPage.__init__(
            self,
            orientation=Gtk.Orientation.VERTICAL,
            **kwargs
        )

class CUTermViewPage(ControlsPage):
    """Controls for viewing the output of the Combinatorial Unit created
    using the Editor. Also supports exporting terms to files and the
    operating system's clipboards.

    """
    _target_scroll_path = None
    em_spec = None
    vm_spec = None
    model = None
    selection = None
    treeview = None

    def _on_button_press_mark_user_present(self, widget, event):
        self._user_interaction = True

    def _on_button_release_mark_user_absent(self, widget, event):
        self._user_interaction = False

    def _on_clicked_show_settings(self, widget):
        self.popover_settings.set_relative_to(widget)
        self.popover_settings.show_all()
        self.popover_settings.popup()

    def _on_selection_changed_copy_terms(self, selection):
        if self._user_interaction is False:
            # Do not copy terms if change in selection is caused by
            # by non-user events
            return
        out = ""
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        model, paths = selection.get_selected_rows()
        output_json = self.page_settings.settings["output_json"]
        if output_json is True:
            out = ''.join((out, '['))
            for p in paths:
                treeiter = model.get_iter(p)
                row = model[treeiter]
                term = self.vm_spec.get_column_data(row, "termview-model-term")
                out = ''.join((out, term, ','))
            out = out.rstrip(',')
            out = ''.join((out, ']'))
        else:
            for p in paths:
                treeiter = model.get_iter(p)
                row = model[treeiter]
                term = self.vm_spec.get_column_data(row, "termview-model-term")
                out = ''.join((out, term, '\n'))
        clipboard.set_text(out, -1)

    def _on_clicked_refresh(self, widget):
        self._refresh()

    def _on_clicked_request_export(self, widget):
        buttons = (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        filters = (
            get_non_file_filter(),
        )
        filepath = get_path_with_dialog(
            action=Gtk.FileChooserAction.SAVE,
            title=self._text("termview-export-dialog-title"),
            buttons=buttons,
            filters=filters,
            overwrite_confirmation=True
        )
        self._refresh()
        # Refresh the Term View model, because the terms are exported from the
        # model. This is done so that the user is able to confirm which terms
        # have been exported, using the visible list of terms.
        with open(filepath, mode='w') as f_w:
            if self.page_settings.settings["output_json"] is True:
                f_w.write('[')
                treeiter = self.model.get_iter_first()
                while treeiter is not None:
                    row = self.model[treeiter]
                    term = self.vm_spec.get_column_data(
                        row, "termview-model-term"
                    )
                    f_w.write(term)
                    treeiter = self.model.iter_next(treeiter)
                    if treeiter is not None:
                        f_w.write(',')
                f_w.write(']')
            else:
                treeiter = self.model.get_iter_first()
                while treeiter is not None:
                    row = self.model[treeiter]
                    term = self.vm_spec.get_column_data(
                        row, "termview-model-term"
                    )
                    out = "{}\n".format(term)
                    f_w.write(out)
                    treeiter = self.model.iter_next(treeiter)
            
    def _editor_model_to_cu(self, editor_model, treeiter):
        # Recursively navigate the CU config tree to build a CU
        if treeiter is None:
            # Handle attempts to get missing sources
            raise TypeError
        try:
            data = []
            cu_config_row = editor_model[treeiter]
            cu_address = self.em_spec.get_column_data(
                cu_config_row, "editor-model-address"
            )
            iclass_name = self.em_spec.get_column_data(
                cu_config_row, "editor-model-type"
            )
            iclass = self.em_spec.get_class_from_name(iclass_name)
            r = self.em_spec.get_column_data(
                cu_config_row, "editor-model-r"
            )
            name = self.em_spec.get_column_data(
                cu_config_row, "editor-model-name"
            )
            if self.em_spec.is_supported_multi_source_cu(iclass) is True:
                # Handle Multi-source CU - get CU with all attached sources
                sources = []
                treeiter_sub_cu = editor_model.iter_children(treeiter)
                while treeiter_sub_cu is not None:
                    src= self._editor_model_to_cu(
                        editor_model, treeiter_sub_cu
                    )
                    sources.append(src)
                    treeiter_sub_cu = editor_model.iter_next(treeiter_sub_cu)
                cu = iclass(sources, r, name=name)
                return cu 
            elif self.em_spec.is_supported_cu(iclass) is True:
                # Handle Single-source CU: get CU with first attached source
                treeiter_sub_cu = editor_model.iter_children(treeiter)
                source = self._editor_model_to_cu(editor_model, treeiter_sub_cu)
                cu = iclass(source, r, name=name)
                return cu
            elif self.em_spec.is_supported_non_cu(iclass) is True:
                # Handle Terminal Source: return data as tuple
                data_raw = self.em_spec.get_column_data(
                    cu_config_row, "editor-model-data"
                )
                fn_unescape = lambda x: html.unescape(x)
                seq = data_raw.split(',')
                m = map(fn_unescape, seq)
                out = tuple(m)
                return out
            else:
                text_fmt = self._text("termview-error-unsupported-source-fmt")
                self.message(self._text.format(cu_address))
                return ()
                    # PROTIP: This returns an empty tuple, this is not C ;)
        except ValueError:
            text_fmt = self._text("termview-error-r-fmt")
            self.message(text_fmt.format(cu_address))
            return ()
        except TypeError:
            text_fmt = self._text("termview-error-no-source-fmt")
            self.message(text_fmt.format(cu_address))
            return ()
        except IndexError:
            text_fmt = self._text("termview-error-r-fmt")
            self.message(text_fmt.format(cu_address))
            return ()

    def _get_ranges(self, range_str='', decoder_fn=None):
        # Convert value range strings into a list of tuples containing
        # two integers representing start and end indices.
        #
        # Range Format:
        # Valid ranges are pairs of integers separated by a dash ``-``, or
        # single integers. In pairs, the smaller integer is speficied first.
        # Ranges are separated by commas. Value ranges must be ordered from
        # smallest to largest, and must not intersect.
        # Invalid ranges are skipped over and reported to the user.
        #
        # Valid Examples:
        # '1-500,750-1000' => [(1, 500), (750, 100)]
        # '25-30,80,100-250' => [(25, 30), (80, 80), (100, 250)]
        #
        # Invalid Examples:
        # '20-1' (Descending ranges are not supported)
        # '8001-9001,12-42' (Specifying ranges out of order is not supported)
        # '1-5,3-10' (Intersecting ranges are not supported)
        #
        if range_str == '':
            return
        ranges = []
        ranges_invalid = []
        range_strs = range_str.split(',')
        i_highest = 0
        for s in range_strs:
            try:
                range_strs_L2 = s.split('-')
                if len(range_strs_L2) > 2:
                    ranges_invalid.append(s)
                elif len(range_strs_L2) == 1:
                    # Handle single values
                    n = int(range_strs_L2[0])
                    if n <= i_highest:
                        ranges_invalid.append(s)
                    else:
                        range_int = (n, n)
                        ranges.append(range_int)
                        i_highest = n
                else:
                    # Handle pairs of values
                    i_first = int(range_strs_L2[0])
                    i_last = int(range_strs_L2[1])
                    if i_first > i_last:
                        ranges_invalid.append(s)
                    elif i_last <= i_highest or i_first <= i_highest:
                        ranges_invalid.append(s)
                    else:
                        range_int = (i_first, i_last)
                        ranges.append(range_int)
                        i_highest = i_last
            except ValueError:
                ranges_invalid.append(s)
        if len(ranges_invalid) > 0:
            # Notify user of invalid ranges
            code = self._get_error_message_code()
            text = self._text("termview-invalid-range-text")
            detail_fmt = self._text("termview-invalid-range-details-fmt")
            detail = detail_fmt.format(ranges_invalid)
            self.message(text, code=code, detail=detail)
        return ranges

    def _refresh(self):
        # Refresh the Term View and outputs terms from the CU specified
        # in the editor
        self.model.clear()
        treeiter_ed = self.model_ed.get_iter_first()
        cu = self._editor_model_to_cu(self.model_ed, treeiter_ed)
        if cu is not None:
            term_count = len(cu)
        else:
            term_count = 0
        limit = self.page_settings.settings["term_limit"]
        ranges = self._get_ranges(
            self.page_settings.settings["output_ranges"]
        )
        if ranges is None:
            ranges = [(0, term_count), ]
        elif len(ranges) <= 0:
            ranges.append( (0, term_count) )
        output_json = self.page_settings.settings["output_json"]
        j = 0
        for r in ranges:
            i_last = min(term_count, r[1]+1)
            for ii in range(r[0], i_last):
                if j >= limit:
                    break
                term = self._term_to_str(cu[ii])
                if output_json is True:
                    term = "\"{}\"".format(term)
                term_row = (ii, str(term))
                self.model.append(self.vm_spec.iter_to_row(term_row))
                j += 1

    def _term_to_str(self, term):
        # Reformats a CU term as a continuous string with no separators
        # between combinatorial elements/components,
        # e.g. ('A','B','C') becomes 'ABC'
        out = ''
        for item in term:
            if isinstance(item, str):
                out = ''.join((out, item))
            elif isinstance(item, (list, tuple)):
                out = ''.join( (out, self._term_to_str(item)) )
        return out.strip()

    def first_run(self):
        self.model_ed = self.main_window.shared_data["editor-model"]

    def _setup_ui(self):
        # Model Specifications
        self.em_spec = CUEditorModelSpec()
        self.vm_spec = CUTermViewModelSpec()

        # Banner
        label = Gtk.Label()
        label.set_markup(self._text("termview-title"))
        self.pack_start(label, False, False, 0)

        # Navigation Toolbar
        dummy_fn = lambda self,x:print(x)
        toolbar = Gtk.Toolbar.new()
        toolbar.set_style(Gtk.ToolbarStyle.BOTH)
        toolbar_button_spec = {
            "button-refresh" : (
                "button-refresh",
                "view-refresh",
                (self._on_clicked_refresh,)
            ),
            "button-settings-term" : (
                "button-settings-term",
                "applications-utilities",
                (self._on_clicked_show_settings,)
            ),
            "button-export" : (
                "button-export",
                "document-save",
                (self._on_clicked_request_export,)
            )
        }
        self.toolbar_items = self.spec_to_toolitem_dict(toolbar_button_spec)
        for ti in self.toolbar_items.values():
            toolbar.insert(ti, -1)
        self.pack_start(toolbar, False, False, 0)

        # Term Settings Popover
        self.popover_settings = Gtk.Popover()
        self.page_settings = CUTermViewSettingsPage(
            strings=self._strings,
            parent_page=self
        )
        self.popover_settings.add(self.page_settings)

        # TreeView and Selection
        column_types = self.vm_spec.column_types
        self.model= Gtk.ListStore(*column_types)
        self.treeview = Gtk.TreeView(model=self.model)
        self.treeview.connect(  
            "button-press-event", self._on_button_press_mark_user_present
        )
        self.treeview.connect(  
            "button-release-event", self._on_button_release_mark_user_absent
        )
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.selection.connect("changed",self._on_selection_changed_copy_terms)
        for i, name in enumerate(self.vm_spec.column_names):
            renderer = self.vm_spec.column_renderers[i]
            column = self.vm_spec.get_gtk_treeview_column(
                name, string_dict=self._strings
            )
            self.treeview.append_column(column)
        scroll_cu_results = Gtk.ScrolledWindow()
        scroll_cu_results.add(self.treeview)
        self.pack_start(scroll_cu_results, True, True, 0)

    def __init__(self, **kwargs):
        ControlsPage.__init__(
            self,
            margin=4,
            message_code_prefix = 'TVIEW',
            orientation=Gtk.Orientation.VERTICAL,
            **kwargs
        )
        self.main_window.shared_data["term-view-model"] = self.model

class AboutPage(ControlsPage):
    """ControlsPage to show version information, instructions
    licensing, copyrights and all that jazz.

    """
    textar_text = Gtk.TextView(
            editable=False,
            hexpand=True,
            wrap_mode=Gtk.WrapMode.WORD
        )
    sppx = 4

    def first_run(self):
        text_fmt = self._text("help-text-fmt")
        filename = self._text("help-file-name")
        text = text_fmt.format(filename)
        txtbuf = self.textar_text.get_buffer()
        txtiter = txtbuf.get_end_iter()
        txtbuf.insert(txtiter, text, len(text))

    def _setup_ui(self):
        # App Title
        label_title = Gtk.Label()
        lbl_pango = "<big>{}</big>\n<b>Version {}</b>\n"
            # PROTIP: The markup language used in GTK+ 3 is Pango,
            # not HTML.
            # See: lazka.github.io/pgi-docs/Gtk-3.0/classes/Label.html
            # set_markup()
        title_text = lbl_pango.format(
            self._text("app-name"), self._text("version")
        )
        lbl_title = Gtk.Label()
        lbl_title.set_markup(title_text)

        # Scrollable Text Area
        scroll_text = Gtk.ScrolledWindow(margin=self.sppx)
        scroll_text.add(self.textar_text)

        # Outer Box surrounding App Title and TextView
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin=self.sppx
        )
        box.pack_start(lbl_title, False, True, self.sppx)
        box.pack_start(scroll_text, True, True, 0)
        self.add(box)

    def __init__(self, **kwargs):
        ControlsPage.__init__(
            self,
            message_code_prefix='HELP',
            **kwargs
        )
        self.tab_label_text=self._text("tab-help")

class CommentPage(AboutPage):
    """A ControlsPage set aside for displaying comments embedded in
    demo files

    """
    textar_text = Gtk.TextView(
        editable=False,
        hexpand=True,
        wrap_mode=Gtk.WrapMode.WORD,
        monospace=True
    )

    def first_run(self):
        pass

    def __init__(self, **kwargs):
        AboutPage.__init__(self, **kwargs)
        # Override some important properties, as we have inherited from
        # the AboutPage class.
        message_code_prefix = 'COMMENT'
        self.tab_label_text = self._text("tab-comments")
        self.text_buffer = self.textar_text.get_buffer()
        self.main_window.shared_data["comments-text-buffer"] = self.text_buffer

class DemoUserControlsModule:
    """Object for collecting ControlsPage's for use in a Demo Main UI Window

    """
    # These standard attributes are placed at class scope mainly so that they
    # appear in Python documentation generators, such as the help() command
    # in the interactive interpreter.
    pages = None
    init_view_widget = None

    def __init__(self, **kwargs):
        strings = kwargs.get("strings")
        main_window = kwargs.get("main_window", None)
        self.pages = (
            CUEditorControlsPage(
                main_window=main_window, strings=strings
            ),
            CommentPage(
                main_window=main_window, strings=strings
            ),
            AboutPage(strings=strings),
        )
        self.init_view_widget = CUTermViewPage(
            main_window=main_window, strings=strings
        )

class MessageArea(ProportionalPaned):
    """A user control widget for reviewing messages raised by a Demo
    App's ControlPages and the Main UI.

    """
    _details = {}
    _selection = None
    model_spec = None
    model = None
    _treeview = None

    def append(self, code, message, detail=None):
        descr = str(datetime.datetime.now().timestamp())
        statusbar = self.main_window.shared_data['statusbar']
        context_id = statusbar.get_context_id(descr)
        statusbar.push(context_id, message)
        GLib.timeout_add(5000, statusbar.remove_all, context_id)
        if detail is not None:
            # For now, only messages with details are stored in the log
            if 'ERR' in code:
                self.main_window.show_message_area()
            message_spec = {
                "messagearea-message" : message,
                "messagearea-code" : code,
                "messagearea-time" : str(datetime.datetime.now())
            }
            new_row = self.model_spec.dict_to_row(message_spec)
            self.model.insert(0, new_row)
            self._details[code] = detail
            iter_first = self.model.get_iter_first()
            self._selection.select_iter(iter_first)
            self._treeview.scroll_to_cell(self.model.get_path(iter_first))

    def _on_list_clicked_show_detail(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            row = model[treeiter]
            title = self.model_spec.get_column_data(row, 'messagearea-message')
            code = self.model_spec.get_column_data(row, 'messagearea-code')
            time = self.model_spec.get_column_data(row, 'messagearea-time')
            details = self._details[code]
            text_fmt = '{0}\n{1} ({2})\n\n'
            text = text_fmt.format(title, time, code)
            textbuffer = self._textview.get_buffer()
            textbuffer.set_text(text)
            textiter = textbuffer.get_end_iter()
            for t in details:
                textbuffer.insert(textiter, t, len(t))

    def _setup_ui(self):
        # Model Specification
        self.model_spec = MessageAreaModelSpec(strings=self._strings)

        ## Scrollable Message List View
        self.model = Gtk.ListStore(*self.model_spec.column_types)
            # PROTIP: Gtk.TreeView is reused for viewing contents
            # of Gtk.ListStores
        self._treeview = Gtk.TreeView(model=self.model)
        for n in self.model_spec.column_names:
            treeview_column = self.model_spec.get_gtk_treeview_column(n)
            self._treeview.append_column(treeview_column)
        scroll_tv = Gtk.ScrolledWindow()
        scroll_tv.add(self._treeview)
        scroll_tv.set_vexpand(True)
        self.add1(scroll_tv)
            # PROTIP: Add to Paned left side
        self._selection = self._treeview.get_selection()
        self._selection.connect("changed", self._on_list_clicked_show_detail)

        ## Scrollable full message text view
        self._textview = Gtk.TextView(
            margin=4, editable=False, wrap_mode=Gtk.WrapMode.WORD
        )
        self._textbuffer = self._textview.get_buffer()
        default_text = self._strings["messagearea-default"]
        self._textbuffer.set_text(default_text)
        scroll_textview = Gtk.ScrolledWindow()
        scroll_textview.add(self._textview)
        scroll_textview.set_vexpand(True)
        self.add2(scroll_textview)
            # PROTIP: Add to Paned right side
       
    def __init__(self, **kwargs):
        # Init Procedure - Message Area Widget Structure
        self.main_window = kwargs.pop("main_window")
        self._strings = kwargs.pop("strings")
        ProportionalPaned.__init__(
            self,
            orientation=Gtk.Orientation.HORIZONTAL,
            wide_handle=True,
        )
        self._setup_ui()

class MainUI(Gtk.Window):
    """Main Demo GUI Window to enable usage of Demo Control Pages and the
    interactive viewing and exchange of any data output.

    """
    _control_pages = {}  
        # PROTIP: this dictionary of references to attached ControlsPage's
        # is only used during testing
    _str_src_path = None
    _strings = {}
    _view_page = None
    control_module_class = None
    default_resource_dir = os.path.dirname(argv[0])
    default_str_file_name = 'demo.text-en-au.json'
    default_str_file_path = os.path.join(
        default_resource_dir, default_str_file_name
    )
    default_window_width = 900
    default_window_height = 480
    message_widget_class = None
    shared_data = {}
    shared_function_calls = {}
    statusbar = None
    subtitle = None

    def _load_strings(self, filepath):
        with open(filepath, mode='r') as f_r:
            json_decoder = json.JSONDecoder()
            dump = f_r.read()
            idict = json_decoder.decode(dump)
        return idict

    def _text(self, name):
        return self._strings.get(name, '🤷')

    def _toggle_message_area(self, widget):
        self.paned_mouter.toggle2()

    def set_control_module(self, module_class):
        # Insert control module pages into the Main UI
        path_ssrc = self._str_src_path
        self._control_pages.clear()
        new_module = module_class(main_window=self, strings=self._strings)
        for p in new_module.pages:
            scr_scroll_area = Gtk.ScrolledWindow()
            scr_scroll_area.add(p)
                ## Make all controls scrollable
            self.nbk_ctrls.append_page(
                scr_scroll_area,
                Gtk.Label.new_with_mnemonic(p.tab_label_text)
            )
            self._control_pages[p._message_code_prefix] = p
            p.first_run()
        new_module.init_view_widget.first_run()
        self._view_page = new_module.init_view_widget
        self.paned_maction.add1(self._view_page)

    def show_message_area(self):
        self.paned_mouter.show2()

    def update_title(self, subtitle=None):
        """Updates the visible title of the Main UI window"""
        if subtitle is not None:
            self.set_title(
                self._text("main-title-with-subtitle-fmt").format(subtitle)
            )
        else:
            self.set_title(self._text("main-title"))

    def first_run(self):
        self.update_title()
        self.set_control_module(self.control_module_class)
        # Add Welcome Message to Message Area
        welcome_code = self._text("welcome-code")
        welcome_text = self._text("welcome-text")
        welcome_details = self._text("welcome-details")
        self.messages.append(welcome_code, welcome_text, welcome_details)

    def _setup_ui(self):
        ## Main Grid Separating Action and Messaging areas
        self.gr_main = Gtk.Grid(column_homogeneous=True) 
            # NOTE: Setting column_homogeneous to true caused the grid
            # to automatically match the containing window size, but
            # I don't quite know why.
        self.add(self.gr_main)

        ### Paned separating Action and Message areas (Main Grid top)
        self.paned_mouter = ProportionalPaned(
            proportion=1.0,
            orientation=Gtk.Orientation.VERTICAL,
            wide_handle=True
        )
            # PROTIP: Gtk.Paned orientation is the orientation
            # which the paned areas line up.
        self.gr_main.attach(self.paned_mouter, 0, 0, 6, 1)
 
        ### Action Area (Top Side of paned_mouter)
        self.paned_maction = ProportionalPaned(
            proportion=0.4,
            orientation=Gtk.Orientation.HORIZONTAL,
            wide_handle=True
        )
        self.paned_mouter.pack1(self.paned_maction, True, True)

        ## Controls Notebook - Right Side of Main Action Area
        self.nbk_ctrls = Gtk.Notebook(scrollable=True)
        self.paned_maction.pack2(self.nbk_ctrls, True, True)

        ## Status Bar (Main Grid bottom)
        self.statusbar = Gtk.Statusbar()
        self.gr_main.attach(self.statusbar, 0, 1, 6, 1)

        ## Message Area Toggle Button (Main Grid bottom)
        bn_vis = Gtk.Button.new_with_mnemonic(self._text("button-history"))
        self.gr_main.attach(bn_vis, 5, 1, 1, 1)
        bn_vis.connect("clicked", self._toggle_message_area)

        ## Message Area Widget Setup
        self.messages = self.message_widget_class(
            main_window=self, strings=self._strings
        )
        self.paned_mouter.pack2(self.messages, True, True)

    def __init__(self, **kwargs):
        # Main Window Properties
        self.control_module_class = kwargs.pop(
            "control_module_class", DemoUserControlsModule
        )
        self.message_widget_class = kwargs.pop(
            "message_widget_class", MessageArea
        )
        self._str_src_path = kwargs.pop(
            "str_src_path", self.default_str_file_path
        )
        width = kwargs.pop("width", self.default_window_width)
        height = kwargs.pop("height", self.default_window_height)
        Gtk.Window.__init__(self, **kwargs)
        self.resize(width, height)
        self._strings = self._load_strings(self._str_src_path)
        self._setup_ui()
        self.shared_data["statusbar"] = self.statusbar
        self.first_run()

def csv_to_model(csv_reader, model, model_spec, **kwargs):
    """Reads CSV-encoded rows back into a TreeModel.
    This function uses ``traverse_treemodel``. Row depth and relationships
    are currently determined using the tree path in the first column of
    the CSV table data.

    Arguments
    =========
    * csv_reader - a CSV reader bound to an input stream, such as a file
        or a StringIO text buffer

    * model - the TreeModel to insert the data as rows into

    * model_spec - a model specification object that contains the necessary
        logic to format and validate data entry. For information on how
        to use model specs, please refer to the documentation of the
        ModelSpec class.

    Optional Arguments
    ==================
    * mode - either 'above', or 'before'

    * treeiter - a TreeIter pointing to the location in model where the row
        is to be inserted.

    """
    treeiter = kwargs.get('treeiter', model.get_iter_first())
    mode = kwargs.get('mode', None)
    stack_treeiter = []
    last_path = Gtk.TreePath.new_first()
    for row_raw in csv_reader:
        # Determine how to insert the next row
        if len(row_raw) != model.get_n_columns():
            # Skip rows with the wrong number of columns
            break
        path = Gtk.TreePath.new_from_string(row_raw[0])
        if path.get_indices()[:-1] == last_path.get_indices():
            # Handle entry into a lower level
            stack_treeiter.append(treeiter)
        elif len(path.get_indices()) < len(last_path.get_indices()):
            d = len(last_path.get_indices()) - len(path.get_indices())
            for i in range(d):
                # Handle return to a higher level from where we
                # branched off, after reaching the end of a lower level.
                treeiter = stack_treeiter.pop()
        row = model_spec.iter_to_row(row_raw)
        # Perform row data insertion
        if len(stack_treeiter) > 0:
            treeiter = model.insert(stack_treeiter[-1], -1, row)
        elif treeiter is None:
            treeiter = model.insert(None, -1, row)
        else:
            if mode == 'under':
                treeiter = model.insert(treeiter, 0, row)
            elif mode == 'before':
                parent = model.iter_parent(treeiter)
                treeiter = model.insert_before(parent, treeiter, row)
            else:
                parent = model.iter_parent(treeiter)
                treeiter = model.insert_after(parent, treeiter, row)
        last_path = path

def get_path_with_dialog(**kwargs):
    """Convenience function to open ready-to-use GTK FileDialogs with
    a single function call. Returns an absolute file path when a file
    is selected and all confirmations acknowledged.

    """
    # TODO: Document accepted keywords
    action = kwargs.get("action") 
    buttons = kwargs.get("buttons")
    filters = kwargs.get("filters")
    main_window = kwargs.get("main_window")
    overwrite_confirmation = kwargs.get("overwrite_confirmation", True)
    title = kwargs.get("title")
    dialog = Gtk.FileChooserDialog(
        title=title,
        parent=main_window,
        action=action,
    )
    dialog.add_buttons(*buttons)
        # PROTIP: The star in front of the buttons argument tells
        # Python to unpack any iter passed in its place into multiple
        # arguments
    for f in filters:
        dialog.add_filter(f)
    dialog.set_do_overwrite_confirmation(overwrite_confirmation)
    dialog.run()
    abs_path = dialog.get_filename()
    dialog.destroy()
    return abs_path

def get_non_file_filter():
    """Get a "filter" which causes a GTK FileDialog to display all files"""
    filter_dummy = Gtk.FileFilter()
    filter_dummy.set_name('All Files')
    filter_dummy.add_pattern('*')
    return filter_dummy

def model_to_csv(model, stream_obj, **kwargs):
    """Write a TreeModel out into a stream (such as a file) using Python's
    CSV writer. The unix dialect (double quote columns, CR newlines) is
    used in all CSV output on this demo.

    This function uses ``traverse_treemodel``.

    """
    addr_offset = kwargs.get("addr_offset", 0)
    fn_zero = lambda m,ti : 0 # Dummy function that only returns zero 
    limits = kwargs.get("limits", None)
    treeiter_start = kwargs.get("treeiter_start", model.get_iter_first())
    writer = csv.writer(stream_obj, dialect='unix')

    def _write_csv_row(model, treeiter, csv_writer):
        row = model[treeiter][:]
        row[-1] = html.escape(row[-1], quote=True)
        csv_writer.writerow(row)
    f_1_args = (writer,)

    traverse_treemodel(
        model,
        _write_csv_row,
        fn_zero,
        f_1_args=f_1_args,
        limits=limits,
        treeiter_start=treeiter_start
    )

def traverse_treemodel(model, f_1, f_2, **kwargs):
    """Reusable GTK TreeModel traversal function.
    This function non-recursively traverses a TreeModel, running two functions
    on every row in the tree it encounters:

    * f_1 - function which executes once before traversal, after limit check
    * f_2 - function which executes once after traversal
    
    Both functions have an argument format like f_1(model, treeiter, *args),
    where ``model`` is the TreeModel to be traversed and ``treeiter`` is the
    TreeIter that is navigating the TreeModel.

    Additional arguments may be passed onto f_1 or f_2 using the f_1_args
    and f_2_args keyword arguments. 

    Optional Keyword Arguments
    ==========================
    * f_1_args - an iter containing arguments to be passed to f_1

    * f_2_args - an iter containing arguments to be passed to f_2

    * limits - an iter of integers containing row counts that define
        the limits of the tree traversal operation. 
        Each count from the start of the iter represents the row limit,
        starting from the topmost level. For levels where no limit is
        defined, traversal is unrestricted.

    * treeiter_start - a treeiter pointing to a row other than the first
        row of the TreeModel, if the traversal is to be started from an
        arbitrary location in the TreeModel.

    Tree Traversal Limit Examples
    =============================
    * (0,) - Return immediately, do not traverse
    * (1,) - Deep Traverse only one top-level row, and all of its sub-rows,
        and their sub-rows.
    * (6,6,6) - Traverse only the first six rows in the first three levels.
        Does not restrict traversal of deeper rows.

    Currently, only row counts from the start of a tree level are
    supported. Only the first few levels of the traversal may be limited.
    There is also no way to limit the depth of the traversal yet.

    """
    counters = [0,]
    f_1_args = kwargs.get("f_1_args", ())
    f_2_args = kwargs.get("f_2_args", ())
    iter_stack = []
    limits = kwargs.get("limits", None)
    n = 0
    treeiter = kwargs.get("treeiter_start", model.get_iter_first())
    while treeiter is not None:
        level = len(iter_stack) - 1
        if limits is not None: 
            # Check if number of rows processed is within limits
            if level < len(limits):
                if counters[level] >= limits[level]:
                    if level > 0:
                        treeiter = iter_stack.pop()
                        treeiter = model.iter_next(treeiter)
                    else:
                        treeiter = None
                    counters[-1] += 1
                    break
        f_1(model, treeiter, *f_1_args)
        if model.iter_has_child(treeiter) is True:
            # One or more sub-rows found, navigate into sub-row
            treeiter_child = model.iter_children(treeiter)
            iter_stack.append(treeiter)
            treeiter = treeiter_child
            counters.append(0)
        elif model.iter_next(treeiter) is not None:
            # Sub-rows not found, not yet at end of branch of TreeModel
            treeiter = model.iter_next(treeiter)
        elif len(iter_stack) > 0:
            # End of TreeModel branch
            keep_returning = True
            while keep_returning is True:
                # Skip levels that have only one row, or levels where
                # we branched off from its end.
                treeiter = iter_stack.pop()
                no_more_rows = model.iter_next(treeiter) is None
                stack_not_empty = len(iter_stack) > 0
                keep_returning = no_more_rows and stack_not_empty
                treeiter = model.iter_next(treeiter)
        else:
            # End of the top level of TreeModel
            treeiter = None
        f_2(model, treeiter, *f_2_args)
        counters[-1] += 1
        n += 1
    return n

def _start_gui():
    win_main = MainUI()
    win_main.connect("destroy", Gtk.main_quit)
    win_main.show_all()
    Gtk.main()

# Open Desktop GUI when called from a CLI shell
if __name__=='__main__':
    _start_gui()

