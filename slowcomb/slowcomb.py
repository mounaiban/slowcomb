"""
Slow Addressable Combinatorics Library main module. 

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

from math import factorial
from slowcomb.slowseq import int_ncr, int_npr,\
    AccumulateSequence, NumberSequence, CacheableSequence, SNOBSequence

# Classes
#
class CustomBaseNumberF(object):
    """
    Number with a custom base, with radix determined by a function.
    The radix may be either uniform or non-uniform.

    Numbers handled by this class are of a fixed length, and digits are
    handled as individual integers in a list. Currently, only positive
    integers are supported.

    Required Arguments
    ------------------
    * length - the length of the number. Accepts int, where length >= 0.
    
    * func_radix - function to determine the radix of a digit. Lambdas
      and methods are accepted. The definition should be like:
    
      ::

      func(i)

      Where i is the position of the digit, 0 < i < length, and i == 0
      determines the radix of the leftmost or most significant digit.

    Optional Arguments
    ------------------
    * digits - the digits of the number, if the number is to have an
      initial state.
    
    Exceptions
    ----------
    * TypeError is raised when an attempt is made to specify the length
      using a non-integer.

    * ValueError is raised when a negative integer is specified as the
      length of the number.
      

    Notes
    -----
    This class is being investigated for performance issues. Preliminary
    tests with the CPython interpreter suggest that calls to
    func_radix() to determine the radix of a digit incur a significant
    performance penalty. For the time being, the use of this class is only
    recommended for problems where it is unreasonable to specify the radices
    of the digits ahead of time.
 
    """
    # TODO: Tests for supporting zero-length numbers
    __slots__ = ('_digits', '_length', '_func_radix')

    def get_int_from_digits(self):
        """
        Get the decimal integer equivalent value of the number

        """
        out = 0
        mul = 1
        for i in range(len(self._digits)-1, -1, -1):
            # Recover the integer value of the number by
            # multiplying the numerical values of the digits
            # from right to left
            out += self._digits[i] * mul
            mul *= self._func_radix(i)
        return out

    def incr(self):
        """
        Increase the value of the number by one.

        If this method is invoked when the number is at its maximum value,
        it wraps around to zero.

        Note
        ----
        This method is intended as a means of bypassing the potentially
        slow operation of recalculating the number from an integer, when
        performing the relatively trivial operation of adding one to the
        number.

        """
        if len(self) == 0:
            # Do not do anything if number has zero length
            return None
        iii = self._length-1 # Start from right hand side of number
        carry = self._digits[iii]+1 >= self._func_radix(iii)
        while carry is True:
            try:
                self._digits[iii] = 0
                iii -= 1
                carry = self._digits[iii]+1 >= self._func_radix(iii)
            except IndexError:
                # If iii runs past the right side of self._digits,
                # it means that the number has overflowed.
                self.set_zero()
                return None
                    # Guard against infinite loops when running this
                    # method on zero-value numbers of radix 1.
        self._digits[iii] += 1
        return None
            
    def set_digits(self, digits):
        """
        Sets the digits of this number directly.

        Required Argument
        -----------------
        * digits - The digits of the number in a sequence, where
          1 < len(digits) < len(self), where len(self) is the number
          of digits in this number, as declared when it was created.

        Exceptions
        ----------
        * ValueError is raised when the following inputs are received:

          - The number of digits specified does not match the declared
            length of the number. For example the Mayan number (uniform
            base-20) input (17, 18, 15, 11) will not be accepted for a
            five-digit number. Numbers will have to be truncated or padded
            before input.

          - The result of self._func_radix returns a negative number.

          - A number with a digits that exceed the radix of the number
            or a particular digit. For example, a Mayan number cannot be
            (11, 8, 20, 12) because valid digits are from 0 to 19.
            Likewise, a non-uniform base number of base (10, 9, 8, 7)
            cannot take (11, 10, 9, 8) as an input.

          - Any digit is negative.

        """
        if len(digits) != self._length:
            # Number of digits must match length
            raise ValueError("Number of digits does not match length")
        for i in range(len(digits)):
            if self._func_radix(i) < 0:
                # Reject negative radices 
                msg_format = "Digit {0} from left has negative radix"
                msg = msg_format.format(i)
                raise ValueError(msg)
            elif digits[i] >= self._func_radix(i):
                # Reject digits that are too large for a position
                msg_format = "Digit {0} from left exceeds max of {1}"
                msg = msg_format.format(i, self._func_radix(i)-1)
                raise ValueError(msg)
            elif digits[i] < 0:
                # Reject negative digits
                msg_format = "Digit {0} from left is negative"
                msg = msg_format.format(i)
                raise ValueError(msg)
            i += 1
        self._digits = list(digits)

    def set_zero(self):
        """
        Sets the value of the number to zero

        """
        self._digits = [0,] * self._length

    def set_digits_from_int(self, i):
        """
        Sets the digits of the number from a decimal integer

        Argument
        --------
        * i - An integer to be converted to radix of this number.
          Accepts int, where i >= 0

        Exception
        ---------
        * OverflowError is raised when an integer has a value that
          exceeds the maximum value of the number

        """
        if len(self) == 0:
            # Do not do anything if length of number is zero
            return None
        self.set_zero()
        iii = self._length-1
        # Build the number in memory from smallest digit to
        # the largest
        while i > 0:
            if iii < 0:
                # If i is still not zero when the last digit has
                # been processed, it means that the number is too
                # large to be expressed.
                raise OverflowError("Value of int specified too large")
            radix_i = self._func_radix(iii)
            digit = i % radix_i
            self._digits[iii] = digit
            i //= radix_i
            iii -= 1

    def digits(self):
        """
        Return the digits of the number as a tuple of integers.

        """
        return tuple(self._digits)

    def __len__(self):
        """
        Supports the use of len() on this class.

        """
        return self._length
   
    def __init__(self, length, func_radix, digits=None, **kwargs):
        """
        Constructor method to support the creation of the Custom
        Base Number. Please refer to the class documentation on how
        to use this class.
        
        """
        if isinstance(length, int) is False:
            raise TypeError("Please specify length using int only")
        if length < 0:
            raise ValueError("Length of number cannot be negative")
        self._length = length
        self._digits = None
        self._func_radix = func_radix

        if digits is not None:
            self.set_digits(digits)
        else:
            self.set_zero()

class CustomBaseNumberP(CustomBaseNumberF):
    """
    Number with a custom base, with radices for each digit explicitly
    specified.

    The base of the number may be uniform or non-uniform

    Required Arguments
    ------------------
    * radices - A sequence of integers declaring the radix of each
      digit of this non-uniform base number. The length of this
      sequence determines the length of the number, or len(self).
      For example, a sexagesimal number representing a 24-hour clock 
      with a visible hour, minute and second signal could be represented
      by (24, 60, 60, 60).
      Accepts any sequence of integers.

    * digits - The digits of the number in a sequence, where
      1 < len(digits) < len(self), where len(self) is the number
      of digits in this number, as declared when it was created.
      The digits are specified as a sequence type containing only
      integers which represent an individual digit of the number.
      Accepts any sequence of integers.

    Exceptions
    ----------
    * TypeError is raised when any digit is not an integer.

    * ValueError is raised when the following inputs are received:

      - The number of digits specified does not match the declared
        length of the number. For example the Mayan number input
        (17, 18, 15, 11) will not be accepted for a five-digit
        number. Numbers will have to be truncated or padded before
        input.

      - A number with a digits that exceed the radix of the number
        or a particular digit. For example, Mayan number (uniform
        base-20) cannot be (11, 8, 20, 12) because valid digits 
        are from 0 to 19. Likewise, a non-uniform base number of 
        base (10, 9, 8, 7) cannot take (11, 10, 9, 8) as an input.

      - Any digit is negative.

    """
    # TODO: Document remaining exceptions.
    __slots__ = ('_digits', '_length', '_radices')

    def get_int_from_digits(self):
        out = 0
        mul = 1
        for i in range(self._length-1, -1, -1):
            # Recover integer value by multiplying the decimal values
            # of the digits from right to left
            out += self._digits[i] * mul
            mul *= self._radices[i]
        return out

    def incr(self):
        """
        Increase the value of the number by one. If this method is invoked
        when the number is at its maximum value, it wraps around to zero.

        This method is intended as a means of bypassing the potentially
        slow operation of recalculating the number from an integer, when
        performing the relatively trivial operation of adding one to the
        number.

        """
        if len(self) == 0:
            # Do nothing if length is zero
            return None

        iii = self._length-1 # Start from right hand side of number
        iii = self._length-1
        carry = self._digits[iii]+1 >= self._radices[iii]
        while carry is True:
            try:
                self._digits[iii] = 0
                iii -= 1
                carry = self._digits[iii]+1 >= self._radices[iii]
            except IndexError:
                # If iii runs past the right side of self._digits,
                # it means that the number has overflowed.
                self.set_zero()
                return None
                    # Guard against infinite loops for numbers that 
                    # just keep overflowing, such as zero-value numbers
                    # with a radix of all 1's
        self._digits[iii] += 1
            
    def set_digits(self, digits):
        # Verify input first
        if digits is None:
            raise TypeError("Only sequences of integers >= 0 accepted")
        elif len(digits) != len(self):
            # Reject numbers that are too long or short
            msg_format = "Number must be {0} digits long"
            msg = msg_format.format(len(self))
            raise ValueError(msg)
        for iii in range(len(digits)):
            if isinstance(digits[iii], int) is True:
                # Accept only integers
                if digits[iii] < 0:
                # Validate each digit
                    msg_format = "Digit {0} is negative"
                    msg = msg_format.format(iii)
                    raise ValueError(msg)
                elif digits[iii] >= self._radices[iii]:
                    msg_format = "Digit {0} exceeds its max value of {1}"
                    msg = msg_format.format(iii, self._radices[iii]-1)
                    raise ValueError(msg)
            else:
                msg_format = "Digit {0} is not an integer"
                msg = msg_format.format(iii)
                raise TypeError(msg)
        # Only assign digits after checks are complete and pass.
        self._digits = digits

    def set_digits_from_int(self, i):
        self.set_zero()
        iii = self._length-1
        # Build the number in memory from smallest digit to
        # the largest
        while i > 0:
            if iii < 0:
                # If there is still sme value left in i after dividing
                # by the last radix, it means that the number is too large
                # to be expressed.
                raise OverflowError("Radix too small to express int value")
            radix_i = self._radices[iii]
            digit = i % radix_i
            self._digits[iii] = digit
            i //= radix_i
            iii -= 1

    def __len__(self):
        return self._length

    def __init__(self, radices, digits=None, **kwargs):
        self._digits = None
        self._length = len(radices)
        self._radices = radices

        if digits is None:
            self.set_zero()
        else:
            self.set_digits(digits)

class CombinatorialUnit(object):
    """
    Superclass which supports implementations of Combinatorial Units
    the Slow Combinatorics Library. These Combinatorial Units, or
    CUs are sequences of combinatorial terms that are lazily evaluate
    combinatorial terms as they are requested.
 
    Required Arguments
    ------------------
    A combinatorial unit class should have the following:
    
    * seq - a sequence to be the data source from which to derive
      combinatorial terms. If seq supports a reverse-lookup method
      named index(), the CU becomes capable of finding out the index
      from raw combinatorial results.
      The simplest examples are strings, but any sequence may be used.
      Map it to blobs, database records, other CombinatorialUnit objects
      or anything that is subscriptable. Think big!

    * r - the size of the subset to be derived in this sequence.
      Named after r-value used in maths textbooks to describe the size
      of a combinatorial term which is a different size from the
      set being worked on (i.e. nPr, nCr), by way of the r-values in
      Python's combinatorial itertools classes.
 
    Examples
    --------
    See Combination, CombinationWithRepeats, CatCombination,
    PBTreeCombinatorialUnit and its subclasses (Permutation and
    PermutationWithRepeats).

    """
    # Slots
    #
    __slots__ = ('_default', '_i', '_r', '_seq_src', '_exceptions', 'name')

    # Class Attributes
    #

    # Methods
    #
    def index(self, x):
        """
        Get the index of a combinatorial result.

        This method merely initiates the reverse lookup process, and
        rejects invalid search terms.
        
        The actual lookup process is defined in _get_index() of the
        CombinatorialUnit subclass.

        Returns the index of the combinatorial result as an int.

        Arguments
        ---------
        * x - A sequence matching an output of the combinatorial unit 
          to be looked up.

        """
        # TODO: Document exceptions
        # TODO: Document use of CUs as Iterators

        # Reject obviously invalid terms
        if self.is_valid() is False:
            if x == self._default:
                return 0
        elif x is None:
            raise TypeError('Search term cannot be None')
        elif x == self._default:
            raise ValueError('default value is not a valid search term')
        elif x == ():
            raise ValueError('empty sequence is not a valid search term')

        # Reject otherwise valid terms of unacceptable length
        if self._r is not None:
            if len(x) != self._r:
                msg = "term must have a length of {0}".format(self._r)
                raise ValueError(msg)
        return self._get_index(x)
 
    def is_valid(self):
        """
        Check if a Combinatorial Unit is ready to return any results.
        
        Returns True if ready, False otherwise.

        If the Combinatorial Unit is not ready, it should return
        a length of 1, and a default output, which in most cases
        is an empty tuple.

        This mechanism is intended to prevent a problematic sequence
        from interfering with the operation of complex combinatorial
        unit setups, particularly with source sequences that are 
        liable to becoming unavailable at runtime, such as external
        databases.

        """
        # Return False if the sequence is set to work on itself
        if self._seq_src is self:
            return False

        # Zero-length sources invalidate the combinatorial unit
        if len(self._seq_src) <= 0:
            return False

        if self._r is not None:
            valid_r = self._r > 0
        else:
            valid_r = True
        no_excs = self._exceptions is None
        if(valid_r and no_excs):
            return True
        else:
            return False

    def supports_index(self, **kwargs):
        """
        Attempt to test if a Combinatoral Unit supports index()

        The index() method of a Combinatorial Unit returns the first
        index of a CU's term as an integer. If this CU supports index(),
        it will return True.

        Arguments
        ---------
        No arguments are required.

        Please disregard **kwargs, as it is used only as a means of
        tracking recursive calls.

        Exceptions
        ----------
        * RecursionError is raised if a recursion loop is detected or
          suspected. Recursion loops occur when any nested CU attempts
          to use any CU above it as a source sequence. This prevents any 
          navigation of the CU chain from terminating, causing a never-
          ending loop.

          - The error message will appear with a pair of numbers that
            look like

          ::

            [1] to [0]

           - In this example, a CU at level 1 is using a CU at level 0
             as a source sequence, but the aforementioned level 0
             sequence is already using the level 1 CU as a source sequence.

        """
        cu_path = kwargs.get('cu_path', [])
            # Path from the top level CU to the lowest level CU
            # used for detecting recursion loops. 
        if self in cu_path:
            # Abort operation if this CU is already in the path,
            # as it means there is a recursion loop. Report this
            # error and raise an exception.
            i_depth = len(cu_path)-1
            i_self = cu_path.index(self)
            out_format = 'loop in combinatorial unit chain: [{0}] to [{1}]'
            out = out_format.format(i_depth, i_self)
            raise RecursionError(out)

        if isinstance(self._seq_src, CombinatorialUnit) is True:
            # Register self into the path
            cu_path.append(self)
            # Descend into nested _seq_src if it is also another CU
            return self._seq_src.supports_index(cu_path = cu_path)
        else:
            # Check functionality of index() if CU is terminal (i.e.
            # has a non-CU as a source sequence).
            # This test works by checking the correctness of the
            # first and last indices returned by index().
            try:
               comb_count = len(self)
               first_term = self[0]
               last_term = self[comb_count-1]
               first_index_works = (self.index(first_term) == 0)
               last_index_works = (self.index(last_term) == comb_count-1)
               return (first_index_works & last_index_works)
            except AttributeError:
                # When a source sequence does not have an index() method,
                # attempting to call it regardless raises an AttributeError.
                # The lack of an index() method in a single part of the
                # CU tree is regarded as a lack of support for the
                # entire tree.
                return False

    def _get_args(self):
        """
        Attempt to rebuild a probable equivalent of the arguments
        used in initialising this sequence

        """
        if isinstance(self._seq_src, str) is True:
            # Add quotes back to str's used as sequences, so that the
            # repr string is actually accurate
            seq_shown = "'{0}'".format(self._seq_src)
        else:
            seq_shown = self._seq_src
        re_arg_fmt = "seq={0}, r={1}"
        re_args = re_arg_fmt.format(seq_shown, self._r)
        return re_args
 
    def _get_index(self):
        """
        Return the first index of a term, if it is a possible output 
        of this Combinatorial Unit. For details on usage, please refer
        to a subclass of this class.

        """
        raise NotImplementedError

    def get_term_count(self):
        """
        Returns the number of possible combinatorial terms with
        this Combinatorial Unit. For details on usage, please refer
        to a subclass of this class.

        """
        raise NotImplementedError

    def __getitem__(self, key):
        """
        Supports direct lookups of terms in a CombinatorialUnit.

        Both int and slice inputs are accepted as keys.

        """
        if self.is_valid() is False:
            return self._default
        elif isinstance(key, int) is True:
            # Single term lookup using integer index
            return self._get_term(key)
        elif isinstance(key, slice) is True:
            # Multiple term lookup using slice
            out = []
            for iii in range(s.start, s.stop, s.step):
                out.append(self._get_term(iii))
                return tuple(out)
        else:
            raise TypeError('indices must be int or slice')

    def __len__(self):
        """
        Gets the total possible number of terms of a combinatorial
        unit. Returns int.

        """
        if self.is_valid() is True:
            # The threshold of the last level is also the 
            # node count
            return self.get_term_count()
        else:
            # Non-valid combinatorics sequences always report a
            # length of one, to account for the default value.
            return 1

    def __iter__(self):
        """
        Supports the use of CombinatorialUnits as iterators

        """
        return self

    def __repr__(self):
        """
        Supports the reporting of information that can be used to reconstruct
        the CombinatorialUnit. The information is returned as a string that
        may be used as an expression in a Python interpreter.

        """
        class_name = self.__class__.__name__
        out_fmt = "{0}({1}, {2}, name={3})"
        if isinstance(self._seq_src, str) is True:
            # Output strings as tuples of characters
            seq_src_out = tuple(self._seq_src)
        else:
            seq_src_out = self._seq_src
        out = out_fmt.format(class_name, seq_src_out, self._r, self.name)
        return out
            
    def __init__(self, seq, r, name=None):
        """
        This is the special constructor method which supports 
        creation of combinatorial units. 
        
        For details on creating the CU, consult the documentation of
        the combinatorial unit class.

        """
        # Validate Arguments 
        if r is not None:
            if(r < 0):
                raise ValueError('r, if present, must be zero or more')

        # Instance Attributes
        #
        self._default = ()
        self.name = name
        self._seq_src = seq
            # The source sequence from which to derive combinatorial
            # terms
        self._i = 0
            # Index when CU is used as an iterator
        self._r = r
            # Sets a fixed length for terms returned by the
            # combinatorial unit.

        #  Other Stat Keepers
        #
        self._exceptions = None
            # Reserved attribute
            # To be set if exceptions have been encountered during 
            # the operation of this Combinator

class PBTreeCombinatorialUnit(CombinatorialUnit):
    """
    A superclass for supporting the implementations of combinatorial
    units that make use of Perfectly-Balanced Trees (PBTrees).

    PBTrees are B-Trees, so the number of child nodes for every node
    on the same level are the same. The node counts thus can be 
    figured out algorithmically for each and every node. The content,
    or more accurately, content referenced by the nodes is predictably
    repeated across the tree.
    
    Required Arguements
    -------------------
    * seq - a sequence to be set as the data source from which to derive
      combinatorial terms. If seq supports a reverse-lookup method
      named index(), the CU becomes capable of finding out the index
      from raw combinatorial results.
      
      - The simplest examples are strings, but any sequence, including
        database connections may be used.

      - Other CU's may be used as a source as well. CUs support reverse 
        index lookup using index() only if the CU's source sequence also
        fully supports index().

    * r - an integer determining the number of elements in the combinatoral
      terms output by the CU, in other words the number of items to be
      selected from seq. Accepts int, where r >= 0. Additional constraints
      on the value of r may apply depending on the Combinatorial Unit in
      use.

    * path_src - the path source, or any object which is able to derive
      paths to navigate the combinatorial tree of the CU. The path is a
      representation of a possible output of the CU.
      
      - The PBTree Combinatorial Unit assumes that a CustomBaseNumber
        is used to derive paths. However, any other object of a class
        that implements CustomBaseNumber methods may also work.

      - For more information on how to use a CustomBaseNumber, please
        see the CustomBaseNumberF and CustomBaseNumberP classes above.

    How It Works
    ------------

    Properties of the PBTree
    ========================
    The following properties apply to the PBTree:

    1. As a virtual tree, the actual tree is not present in memory,
       but its nodes are lazily evaluated as they are requested.

    2. The number of nodes per level is a multiple of the number of
       nodes on the previous level.

    3. Every node on the same level share the same exact number of
       sibling nodes.

    4. Any node is allowed to have an arbitrary number of child nodes,
       as long as traits 1 and 2 above apply.

    5. The path to a node can be determined from its index expressed
       as a numerical quantity, by a series of simple arithmetic
       operations.


    Using the PBTree to Represent Combinatorial Terms
    =================================================
    Here's a rather crude diagram of a three-level PBTree, with its
    nodes integer-indexed:

    ::

      10 11 12 13 14 15  16 17 18 19 20 21
        \_|   \_|  \_|   |_/   |_/   |_/
           \    |    |   |     |    /
            4   5    6   7     8   9  
             \__|    \___/    /___/
                 \     |     /
                  1    2    3
                   \___|___/
                       | 
                       0


    NOTE: The tree in this example is drawn from the bottom. For those
    who prefer their trees with the root on top, just imagine it
    upside-down.

    In this example, each node is numbered breadth first: from 'left
    to right, then bottom to top'.

    Paths
    =====
    The path to each node can be used to represent a combinatorial
    result, and the contents of each node could represent the elements
    of the combinatorial term. The exact content of the nodes depends
    on the subclass of PBTreeCombinatorics. Node zero is omitted from
    the path, as its purpose is simply to unify the tree's nodes in
    visualisations.

    The Paths to each of the nodes are as follows:

    Node    Path
    ----    -----------
    0       N/A
    1       (0,)
    2       (1,)
    3       (2,)
    4       (0, 0)
    5       (0, 1)
    6       (1, 0)
    7       (1, 1)
    8       (2, 0)
    9       (2, 1)
    10      (0, 0, 0)
    11      (0, 0, 1)
    12      (0, 1, 0)
    13      (0, 1, 1)
    14      (1, 0, 0)
    15      (1, 0, 1)
    16      (1, 1, 0)
    17      (1, 1, 1)
    18      (2, 0, 0)
    19      (2, 0, 1)
    20      (2, 1, 0)
    21      (2, 1, 1)

    The path can be regarded as a custom-base number with a non-uniform
    radix. The radix of the n'th digit is determined by the number of
    nodes on the n'th level.

    Selecting Terms By Length (r-value)
    ===================================
    The path to each node on a particluar level represents combinatorial
    terms of the same length. A combinatorial unit can be set up for
    returning terms of a set length by constraining the CU to selecting
    nodes of a particular level.
    
    For example, a CU with a source of ten items has a ten-level
    combinatorial tree. Limiting the path to a length of three restricts
    access to the first three levels of the tree, creating a CU that
    selects only three items out of a source of ten.

    Setting the r-value to zero causes the combinatorial unit to return
    empty terms.
 
    See Also
    --------
    CatCombination, Permutation, PermutationWithRepeats 

    """
    # Slots
    #
    __slots__ = ('_path_src')

    def _get_path(self, i):
        self._path_src.set_digits_from_int(i)
        return self._path_src.digits()

    def __init__(self, seq, r, path_src, name=None):
        """
        This is the special constructor method which supports 
        creation of combinatorial units. 
        
        For details on creating the CU, consult the documentation of
        the combinatorial unit class.

        """
        super().__init__(seq, r, name=name)
        self._path_src = path_src
 

class CatCombination(PBTreeCombinatorialUnit):
    """
    A Catenating Combination, or a sequence of all possible combinations
    of items from multiple position-dependent sequences, where items
    from the first sequence only appears on the first element of the
    combination, and items from the second appear second, and so on...

    Required Arguments
    ------------------
    * seqs - Sequence source to derive combinations from. Accepts a 
      sequence of sub-sequences.

    * r - The length of the terms derived from the combinatorial
      unit. With the CatCombinator, setting r smaller than the
      number of sub-sequences in causes it to use only the first r
      sub-sequences. Accepts int, 0 ≤ r < len(seqs).

    Note
    ----
    * While it is possible to make the CatCombination class work
      like the Permutation class, position-dependent combinations
      are the intended use of this class.

    Example
    -------
    Let's re-create the three-word CatCombination from the exampes
    module (from slowcomb.tests.examples.cc). Here's a table of the
    words in the CU:

    Word 1  Word 2  Word 3
    ======  ======  ========
    I       need    sugar
            want    spice 
                    scissors

    This can be done the more beginner-friendly way:

    >>> from slowcomb.slowcomb import CatCombination
    >>> s_a = ('I',)
    >>> s_b = ('need','want')
    >>> s_c = ('sugar','spice','scissors') 
    >>> seqs = (s_a, s_b, s_c)
    >>> catcomb = CatCombination(seqs, r=3)

    Or the hardcore way:

    >>> catcomb = CatCombination ( (('I',), ('need', 'want'),
    ... ('sugar', 'spice', 'scissors')), r=3)

    This combinatorial unit is set up to output only full sentences,
    as it's r-value is set to 3.

    To access all full sentences, use the CU as an iterator:

    >>> for d in catcomb:
    ...     print(d)
    ('I', 'need', 'sugar')
    ('I', 'need', 'spice')
    ('I', 'need', 'scissors')
    ('I', 'want', 'sugar')
    ('I', 'want', 'spice')
    ('I', 'want', 'scissors')

    Reducing the r-value to less than three cuts the sentences
    short to r number of words:

    >>> catcomb = CatCombination(seqs, r=2)
    >>> for d in catcomb:
    ...     print(d)
    ('I', 'need')
    ('I', 'want')

    >>> catcomb = CatCombination ( (('I',), ('need', 'want'), \
    ... ('sugar', 'spice', 'scissors')))

    The resulting combinatorial tree can be visualised as:

    ::
                    
      su.  sp.  sc.              su.  sp.  sc.
        \___|___/                  \___|___/
             \                        /
             need                  want
               \                    /
                \__________________/
                         |
                         I
                         |
                         0
    
        legend: su.-sugar, sp.-spice, sc.-scissors


    """

    # Slots
    #
    __slots__ = ()

    def supports_index(self, **kwargs):
        """
        Attempt to test if a Catenation Combination Unit supports index()

        The index() method of a Combinatorial Unit returns the first
        index of a CU's term as an integer. If this CU supports index(),
        it will return True.

        A CatCombination unit has multiple source sequences in _seq_src,
        and is deemed to have index() support, if all of its sequences have
        support for an index() method that behaves identically.

        Arguments
        ---------
        No arguments are required.

        Please disregard **kwargs, as it is used only as a means of
        tracking recursive calls.

        Exceptions
        ----------
        * RecursionError is raised if a recursion loop is detected or
          suspected. Recursion loops occur when any nested CU attempts
          to use any CU above it as a source sequence. This prevents any 
          navigation of the CU chain from terminating, causing a never-
          ending loop.

          - The error message will appear with a pair of numbers that
            look like

          ::

            [1] to [0]

           - In this example, a CU at level 1 is using a CU at level 0
             as a source sequence, but the aforementioned level 0
             sequence is already using the level 1 CU as a source sequence.

        """
        # NOTE: This method is an overridden version of 
        # CombinatorialUnit.supports_index() to handle CatCombination's
        # slightly different _seq_src format.

        cu_path = kwargs.get('cu_path', [])
            # Nesting list of CUs in order of the shallowest to the
            # deepest. Every CU down the list is part of the _seq_src
            # of the next higher CU.
        if self in cu_path:
            # Abort operation if this CU is already in cu_path,
            # as it means there is an infinite recursion loop.
            i_depth = len(cu_path)-1
            i_self = cu_path.index(self)
            # Report location of loop in cu_path
            #
            # TODO: Implement a means of spatially locating loops, i.e.
            # finding the exact point where the loop begins down to the
            # nesting layer and its index in the offending CU's _seq_src.
            out_format = 'loop in combinatorial unit chain: [{0}] to [{1}]'
            out = out_format.format(i_depth, i_self)
            raise RecursionError(out)

        for s in self._seq_src:
            # Use breadth-first recursive check to search CUs.
            # Return False if at least one CU has a _seq_src 
            # with no index() method.
            if isinstance(s, CombinatorialUnit) is True:
                cu_path.append(self) # Register self into the path
                if s.supports_index(cu_path=cu_path) is False:
                    # Descend into nested CUs in _seq_src, bringing
                    # along the tree path.
                    return False

            else:
                try:
                    # Check functionality of index() if CU is terminal
                    # (i.e. has a non-CU as a source sequence)
                    comb_count = len(s)
                    first_term = s[0]
                    last_term = s[comb_count-1]
                    first_index_works = (s.index(first_term) == 0)
                    last_index_works = (s.index(last_term) == comb_count-1)
                    if (first_index_works & last_index_works) is False:
                        return False
                except AttributeError:
                    # If there is an AttributeError raised when index()
                    # is called on any _seq_src, then the CU is regarded
                    # as not having index() support
                    return False

        # Assume that index() is supported if every source sequence
        # found has been tested to support index()
        return True


    def get_term_count(self):
        if self.is_valid() is True:
            count = 1
            for iii in range(self._r):
                count *= len(self._seq_src[iii])
            return count

    def _get_index(self, x):
        """
        Return the first index of a term, if it is a possible output 
        of this Combinatorial Unit.

        Arguments
        ---------
        * x - The term whose index is being sought after. Accepts any
          Python iterator type.

        Exceptions
        ----------
        * ValueError - when x is not a possible output of this CU.

        """
        # TODO: Attempt to rebuild the original path
        path = [0] * self._r
        i = 0
        for el in x:
            path[i] = self._seq_src[i].index(el)
            i += 1
        self._path_src.set_digits(path)
        return self._path_src.get_int_from_digits()
        

    def _get_args(self):
        """
        Attempt to rebuild a probable equivalent of the arguments
        used in initialising a CatCombination sequence

        """
        seq_shown = self._seq_src[1:]
            # Strip leading None from the outer sequence
        re_arg_fmt = "seq={0}, r={1}"
        return re_arg_fmt.format(seq_shown, self._r)

    def _get_term(self, ii):
        """
        Returns the first+ii'th term of a CatCombinator

        Arguments
        ---------
        * ii - Internal Index of the term. Accepts int, where
          0 ≤ i < _ii_stop

        Term Construction Process for the CatCombination CU
        ---------------------------------------------------
        This CU uses the virtual tree in the PBTreeCombinatorics class
        to build its terms. Terms are represented by paths to nodes on
        the tree, and the path to each node is created using 
        PBTreeCombinatronics._get_comb_tree_path(). Each element on the
        tree path is regarded a direct index of an element of a 
        corresponding sub-sequence of _seq_src.

        The i'th element of the path references an item on the i'th
        sequence.

        Example
        =======
        Referring to our example combinatorial unit:

        >>> from slowcomb.slowcomb import CatCombination
        >>> catcomb = CatCombination ( (('I',), ('need', 'want'),
        ... ('sugar', 'spice', 'scissors')), r=3)

        And its tree:

        ::
                        
          su.  sp.  sc.              su.  sp.  sc.
            \___|___/                  \___|___/
                 \                        /
                 need                  want
                   \                    /
                    \__________________/
                             |
                             I
                             |
                             0
        
            legend: su.-sugar, sp.-spice, sc.-scissors

        Let's recall term 4 from the CU:

        >>> catcomb[3]
        ('I', 'want', 'sugar')

        As 'I' is element 0 in sequence one, 'want' is element 1
        in sequence two and 'sugar' is element 0 in sequence three,
        The tree path would have been (0, 0, 1, 0)

        """
        path = self._get_path(ii)
        out = []
        for iii in range(len(path)):
            out_data = self._seq_src[iii][path[iii]]
            if out_data is not None:
                out.append(out_data)
        return(tuple(out))

    def __next__(self):
        # TODO: Method to support use as an iterator, with
        # special optimised code path, with minimal function calls
        if self._i >= len(self):
            raise StopIteration

        self._path_src.set_digits_from_int(self._i)
        path = self._path_src._digits
        out = []
        for iii in range(self._r):
            out.append(self._seq_src[iii][path[iii]])
        self._i += 1
        return tuple(out)

    def __init__(self, seqs, r, name=None):
        """
        This is the special constructor method which supports 
        the creation of a CatCombination combinatorial unit. 
        
        For details on how to do this, please consult the documentation
        for the CatCombination class.

        """
        # Construction Routine
        seq_src = tuple(seqs)
        subcounts = []
        for i in range(r):
            subcounts.append(len(seq_src[i]))
        path_src = CustomBaseNumberP(subcounts)
            # Set the radices to the count of each sub-sequence from left
            # to right
        super().__init__(seq_src, r, path_src, name=name)


class Permutation(PBTreeCombinatorialUnit):
    """
    A sequence of every possible re-arrangement of a source sequence,
    or a subset thereof.

    This combinatorial unit may be regarded as a subscriptable
    analogue to Python's built-in itertools.permutations class.

    Arguments
    ---------
    * seq - sequence source to derive permutations from.

    Optional Arguments
    ------------------
    * r - The length of the terms derived from the combinatorial
      unit. Setting r smaller than the number of elements in seq
      in causes the combinatorial unit to return so-called 
      'partial permutations'. Accepts int, 0 ≤ r < len(seqs).

    Examples
    --------
    Here is a classic four-element permuator:

    >>> from slowcomb.slowcomb import Permutation
    >>> words = ('heads','shoulders','knees','toes')
    >>> perm = Permutation(words, r=4)
    >>>     # Easy Mode

    And here is the one-liner equivalent:

    >>> perm = Permutation(('heads','shoulders','knees','toes'),r=4)
    >>>     # Hardcore Mode

    The twenty-four rearrangements can be listed by accessing the CU
    as an iterator:

    >>> for d in perm:
    ...     print(d)
    ('heads', 'shoulders', 'knees', 'toes')
    ('heads', 'shoulders', 'toes', 'knees')
    ('heads', 'knees', 'shoulders', 'toes')
    ('heads', 'knees', 'toes', 'shoulders')
    ('heads', 'toes', 'shoulders', 'knees')
    ('heads', 'toes', 'knees', 'shoulders')
    ('shoulders', 'heads', 'knees', 'toes')
    ('shoulders', 'heads', 'toes', 'knees')
    ('shoulders', 'knees', 'heads', 'toes')
    ('shoulders', 'knees', 'toes', 'heads')
    ('shoulders', 'toes', 'heads', 'knees')
    ('shoulders', 'toes', 'knees', 'heads')
    ('knees', 'heads', 'shoulders', 'toes')
    ('knees', 'heads', 'toes', 'shoulders')
    ('knees', 'shoulders', 'heads', 'toes')
    ('knees', 'shoulders', 'toes', 'heads')
    ('knees', 'toes', 'heads', 'shoulders')
    ('knees', 'toes', 'shoulders', 'heads')
    ('toes', 'heads', 'shoulders', 'knees')
    ('toes', 'heads', 'knees', 'shoulders')
    ('toes', 'shoulders', 'heads', 'knees')
    ('toes', 'shoulders', 'knees', 'heads')
    ('toes', 'knees', 'heads', 'shoulders')
    ('toes', 'knees', 'shoulders', 'heads')

    The permutations may also be individually requested:

    >>> perm[11]
    ('shoulders', 'toes', 'knees', 'heads')

    >>> perm[23]
    ('toes', 'knees', 'shoulders', 'heads')
    
    The full combintorial tree may be visualised as:

    ::
        
        t k  t s  k s  t k  t h  k h  t s  t h  s h  k s  k h  s h
        | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |
        k t  s t  s k  k t  h t  h k  s t  h t  h s  s k  h k  h s
        ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥
         |    |    |    |    |    |    |    |    |    |    |    |
         s.   k.   t.   h.   k.   t.   h.   s.   t.   h.   s.   k.
         ⸤____|____⸥    ⸤____|____⸥    ⸤____|____⸥    ⸤____|____⸥
              |              |              |              |
              h.             s.             k.             t.
              ⸤______________|______________|______________⸥
                                     |
                                     0

        legend: h.-heads, s.-shoulders, k.-knees, t.-toes 

        Nodes indices start from zero, and on the left.

    Notice that the last level always has one node per parent, and
    therefore the same number nodes as the second-last level. This is
    due to the element elimination of the permutation process.

    To derive partial permutations, simply set the r-argument to a
    smaller value to the term size of your choice:

    >>> perm = Permutation(('heads', 'shoulders', 'knees', 'toes'), r=2)
    >>> for d in perm:
    ...     print(d)
    ('heads', 'shoulders')
    ('heads', 'knees')
    ('heads', 'toes')
    ('shoulders', 'heads')
    ('shoulders', 'knees')
    ('shoulders', 'toes')
    ('knees', 'heads')
    ('knees', 'shoulders')
    ('knees', 'toes')
    ('toes', 'heads')
    ('toes', 'shoulders')
    ('toes', 'knees')

    Slicing of the permutator is supported too:

    >>> perm[0:12:3]
    (('heads', 'shoulders'), ('shoulders', 'heads'), ('knees', 'heads'), ('toes', 'heads'))

    This is how the partial permutation tree may be visualised:

    ::

         s.   k.   t.   h.   k.   t.   h.   s.   t.   h.   s.   k.
         ⸤____|____⸥    ⸤____|____⸥    ⸤____|____⸥    ⸤____|____⸥
              |              |              |              |
              h.             s.             k.             t.
              ⸤______________|______________|______________⸥
                                     |
                                     0

        legend: h.-heads, s.-shoulders, k.-knees, t.-toes 

    """

    def _get_index(self, x):
        """
        Return the first index of a term, if it is a possible output
        of this Combinatorial Unit.

        Arguments
        ---------
        * x - The term whose index is being sought after. Accepts any 
          Python iterator type.

        Exceptions
        ----------
        * ValueError - when x is not a possible output of this CU.

        """
        path = [0] * self._r
        temp_src = list(self._seq_src)
        i = 0
        for el in x:
            index_el = temp_src.index(el)
            path[i] = index_el
            temp_src.pop(index_el)
            i += 1
        self._path_src.set_digits(path)
        return self._path_src.get_int_from_digits()

    def set_src(self, seq):
        """
        Change the source sequence.

        Arguments
        ---------
        * seq - Sequence to be permutated. Accepts any Python sequence.

        """
        self._seq_src=tuple(seq)
        self._set_thresholds()

    def _get_term(self, ii):
        """
        Return the results of the permutation of internal index ii.

        Arguments
        ---------
        * ii - Internal Index of the permutation. Accepts int, 
          0 ≤ i < self._ii_stop

        Term Construction Process for the Permutation CU
        ------------------------------------------------
        Terms are derived based on the use of a tree path, which decides
        the read order of the source sequence, _seq_src. The path is,
        for the purposes of this method, equivalent to non-uniform
        base number in which:
        
        1. The highest digit has a radix equal to the number of
           elements in _seq_src.

        2. Each successive digit has a radix of the previous minus
           one.

        The root node is not used, and is ignored by the path
        construction algorithm.

        The elements of the tree path is then used as indices to a
        temporary copy of _seq_src. Every item referenced in this
        copy is moved from this temporary copy to a final output
        sequence, out, which it then returned to the caller.


        Example
        =======
        Here is our four-word example permutation:

        ::

          Permutation(('heads', 'shoulders', 'knees', 'toes'), r=4)
        
        In maths textbook-ese, this is a 4P4 permutation.

        And here's a reprint of the permutation tree:

        ::
                                                 * 
         t k  t s  k s  t k  t h  k h  t s  t h  s h  k s  k h  s h
         | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |
         k t  s t  s k  k t  h t  h k  s t  h t  h s  s k  h k  h s
         ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥  ⸤_⸥
          |    |    |    |    |    |    |    |    |    |    |    |
          s.   k.   t.   h.   k.   t.   h.   s.   t.   h.   s.   k.
          ⸤____|____⸥    ⸤____|____⸥    ⸤____|____⸥    ⸤____|____⸥
               |              |              |              |
               h.             s.             k.             t.
               ⸤______________|______________|______________⸥
                                      |
                                      X

        legend: h.-heads, s.-shoulders, k.-knees, t.-toes, X-root
                *-17th 4P4 perm.

        We will now derive the seventeenth four-word permutation, marked
        on the diagram above with an asterisk. The path generated herein
        will therefore be (2, 2, 0, 0). The path does not change during
        thie process of constructing the permutation.

        With the address at hand, let's derive the permutation!

        Tree path is (2, 2, 0, 0) throughout the process.
        Temporary seq. 'temp' is ('heads', 'shoulders', 'knees', 'toes')

        Element zero in path: 2
        Curr. temp: ('heads', 'shoulders', 'knees', 'toes')
        Pop temp[2] to end of out
        Current out: ['knees',]

        Element one in path: 2
        Curr. temp: ('heads', 'shoulders', 'toes')
        Pop temp[3] to end of out
        Current out: ['knees', 'toes']

        Element two in path: 0
        Curr. temp: ('heads', 'shoulders')
        Pop temp[0] to end of out
        Current out: ['knees', 'toes', 'heads']

        Element three in path: 0
        Curr. temp: ('shoulders',)
        Pop temp[0] to end of out

        Final out: ['knees', 'toes', 'heads', 'shoulders']
 
        The sequence out may now be converted to a tuple and returned
        to the method or function that requested it.
        
        """
        if self._r is None:
            raise NotImplementedError('r=None no longer supported')
        self._path_src.set_digits_from_int(ii)
        path = self._path_src.digits()

        # Build the actual term
        temp = []
        temp.extend(self._seq_src)
        out = []
        for i in tuple(path):
            out.append(temp.pop(i))
        return tuple(out)

    def get_term_count(self):
        n = len(self._seq_src)
        return int_npr(n, self._r)

    def __next__(self):
        if self._i >= self._len_iter:
            raise StopIteration

        path = self._path_src_iter._digits
        temp = []
        temp.extend(self._seq_src)
        out = []
        for i in path:
            out.append(temp.pop(i))
        self._i += 1
        self._path_src_iter.incr()
        return tuple(out)
            

    def __init__(self, seq, r, name=None):
        """
        This is the special constructor method which supports 
        creation of a Permutation combinatorial unit. 
        
        For details on creating the CU, consult the documentation
        for the Permutation class.

        """
        # Construction Routine
        func_radix = lambda x:len(self._seq_src)-x
        path_src = CustomBaseNumberF(r, func_radix)
        super().__init__(seq, r, path_src, name=name)
        
        # Instance Attributes
        # TODO: Iterator access stuff
        radices = tuple([x for x in range(len(seq), len(seq)-r, -1)])
        self._path_src_iter = CustomBaseNumberP(radices)
        self._len_iter = int_npr(len(self._seq_src), self._r)

class PermutationWithRepeats(PBTreeCombinatorialUnit):
    """
    A Repeats-Permitted Permutator, or a sequence of all possible
    uses of elements from a source sequence, given a set fixed number
    of elements, while allowing for multiple uses of the same element.
    
    Arguments
    ---------
    * seq - sequence source to derive permutations from.

    * r - The length of the terms derived from the combinatorial
      unit. Accepts int, 0 ≤ r < len(seq).

    There are probably many other names for such a combinatorial
    operation, but this name was chosen as it was observed to pretty
    much identical to allowing permutations to have repeating elements.

    Example
    -------
    A three-element repeats-permitted permutator (RPP) may be created
    like this:

    >>> from slowcomb.slowcomb import PermutationWithRepeats
    >>> permwr = PermutationWithRepeats(('🍇', '🍈', '🍉'),r=3)

    Note that r must be set, as without it the permutation will
    have an infinite length and will just keep going on and on...

    Here is every possible output of the RPP:

    >>> for d in permwr:
    ...     print(d)
    ('🍇', '🍇', '🍇')
    ('🍇', '🍇', '🍈')
    ('🍇', '🍇', '🍉')
    ('🍇', '🍈', '🍇')
    ('🍇', '🍈', '🍈')
    ('🍇', '🍈', '🍉')
    ('🍇', '🍉', '🍇')
    ('🍇', '🍉', '🍈')
    ('🍇', '🍉', '🍉')
    ('🍈', '🍇', '🍇')
    ('🍈', '🍇', '🍈')
    ('🍈', '🍇', '🍉')
    ('🍈', '🍈', '🍇')
    ('🍈', '🍈', '🍈')
    ('🍈', '🍈', '🍉')
    ('🍈', '🍉', '🍇')
    ('🍈', '🍉', '🍈')
    ('🍈', '🍉', '🍉')
    ('🍉', '🍇', '🍇')
    ('🍉', '🍇', '🍈')
    ('🍉', '🍇', '🍉')
    ('🍉', '🍈', '🍇')
    ('🍉', '🍈', '🍈')
    ('🍉', '🍈', '🍉')
    ('🍉', '🍉', '🍇')
    ('🍉', '🍉', '🍈')
    ('🍉', '🍉', '🍉')
        
    The resulting combinatorics tree can be visualised as:

    ::
      
       g h w  g h w  g h w  g h w  g h w  g h w  g h w  g h w  g h w
       ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥
         |      |      |      |      |      |      |      |      |
         g.     h.     w.     g.     h.     w.     g.     h.     w.
         ⸤______|______⸥      ⸤______|______⸥      ⸤______|______⸥
                |                    |                    |
                g.                   h.                   w.
                ⸤____________________|____________________⸥
                                     |
                                     0

        legend: g.-grapes🍇, h.-honeydew🍈, w.-watermelon🍉
    
    The PermutatorWithRepeats combinatorial unit is capable of terms
    where r (far) exceeds n.

    This creates an effectively 3P9 RPP:

    >>> permwr = PermutationWithRepeats(('🍇', '🍈', '🍉'),r=9)

    There are too many permutations to list here, but slices may
    be taken:

    >>> len(permwr)
    19683

    >>> for d in permwr[-16862:-16872:-2]:
    ...     print(d)
    ('🍇', '🍈', '🍇', '🍉', '🍈', '🍉', '🍈', '🍈', '🍈')
    ('🍇', '🍈', '🍇', '🍉', '🍈', '🍉', '🍈', '🍇', '🍉')
    ('🍇', '🍈', '🍇', '🍉', '🍈', '🍉', '🍈', '🍇', '🍇')
    ('🍇', '🍈', '🍇', '🍉', '🍈', '🍉', '🍇', '🍉', '🍈')
    ('🍇', '🍈', '🍇', '🍉', '🍈', '🍉', '🍇', '🍈', '🍉')


    Fun Facts
    ---------
    * You can achieve an identical sequence using a CatCombinator,
      by using multiple copies of the same source sub-sequence.
      However, using this CU may be easier.

    * This permutator was almost called PokiesPermutator, due to the
      similarity to its output to payline readouts on certain types of
      gambling machines.

    """
    # Slots
    #
    __slots__ = ('_len_iter', '_path_iter', '_out_iter', '_seq_src',)

    def _get_index(self, x):
        """
        Return the first index of a term, if it is a possible output
        of this Combinatorial Unit.

        Arguments
        ---------
        * x - The term whose index is being sought after. Accepts any 
          Python iterator type.

        Exceptions
        ----------
        * ValueError - when x is not a possible output of this CU.

        """
        # TODO: Attempt to rebuild paths
        path = [0] * self._r
        i = 0
        for el in x:
            path[i] = self._seq_src.index(el)
            i += 1
        self._path_src.set_digits(path)
        # TODO: Return the integer value of the path
        return self._path_src.get_int_from_digits()

    def _get_term(self, ii):
        """
        Return the permutation of internal index number ii.

        Arguments
        ---------
        * ii - Internal Index of the permutation. Accepts int, 
          0 ≤ i < self._ii_stop

        Term Construction Process for the PermutationWithRepeats CU
        -----------------------------------------------------------
        The paths of the combinatorial tree of a repeats-permitted
        permutation is, within the scope of this method, identical to
        a base-n. Each digit represents a reference to an element
        of _seq_src, and the n in this case is the number of elements
        in _seq_src.

        In the current implementation, a CustomBaseNumberP object
        configured to behave like a number with uniform base n, where
        n == len(self._seq_src), with length equal to self._r.

        Example
        =======
        Referring to our example permutator:
        
        >>> permwr = PermutationWithRepeats(('🍇', '🍈', '🍉'),r=3)

        The combinatorial tree can be visualised as:

        ::

           0 1 2  0 1 2  0 1 2  0 1 2  0 1 2  0 1 2  0 1 2  0 1 2  0 1 2
           ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥  ⸤_|_⸥
             |      |      |      |      |      |      |      |      |
             0      1      2      0      1      2      0      1      2 
             ⸤______|______⸥      ⸤______|______⸥      ⸤______|______⸥
                    |                    |                    |
                    0                    1                    2
                    ⸤____________________|____________________⸥
                                         |
                                         X

        Where 0 == 🍇, 1 == 🍈, 2 == 🍉 and X == Root node

        This CU is equivalent to a base-3 number. To create a CU which
        selects only three items, the path will have three elements.
        Therefore, we use a three-digit base-3 number as the path.
        Here are the paths for the first nine terms:

        Term (r=3)  Path       Term
        ==========  =========  ==========
        0           (0,0,0)    (🍇,🍇,🍇)
        1           (0,0,1)    (🍇,🍇,🍈)
        2           (0,0,2)    (🍇,🍇,🍉)
        3           (0,1,0)    (🍇,🍈,🍇)
        4           (0,1,1)    (🍇,🍈,🍈)
        5           (0,1,2)    (🍇,🍈,🍉)
        6           (0,2,0)    (🍇,🍉,🍇)
        7           (0,2,1)    (🍇,🍉,🍈)
        8           (0,2,2)    (🍇,🍉,🍉)

        The root node is ignored during path and term derivation.

        """
        self._path_src.set_digits_from_int(ii)
        path = self._path_src._digits
        out = [self._seq_src[0],] * self._r
        for iii in range(self._r):
            out[iii] = self._seq_src[path[iii]]
        return tuple(out)

    def get_term_count(self):
        return len(self._seq_src)**self._r

    def __next__(self):
        if self._i >= self._len_iter:
            raise StopIteration

        # NOTE: Experiment with CustomBaseNumber class to generate tree paths
        path = self._path_iter._digits
        for iii in range(self._r):
            self._out_iter[iii] = self._seq_src[path[iii]]
        self._path_iter.incr()
        self._i += 1
        return tuple(self._out_iter)
            
    def __init__(self, seq, r, name=None):
        """
        This is the special constructor method which supports 
        creation of a PermutationWithRepeats combinatorial unit. 
        
        For details on creating the CU, consult the documentation for 
        the PermutationWithRepeats class.

        """
        # Construction Routine
        self._path_iter = CustomBaseNumberP(radices=(len(seq), ) * r)
            # NOTE: Experiment using CustomBaseNumber to generate tree paths
        self._seq_src = seq
        super().__init__(seq, r, self._path_iter, name=name)

        # Instance Attributes
        self._len_iter = self.get_term_count()
        self._out_iter = [self._seq_src[0],] * self._r

class Combination(CombinatorialUnit):
    """
    A sequence of all possible selections of items from another source
    sequence. Selections of the same elements in a different order are
    regarded as the same selection. Elements may only be selected once.
    
    This class can be regarded as a subscriptable analogue Python's
    itertools.combinations class.
        
    Arguments
    ---------
    * seq - The source sequence to derive combinations from.

    * r - The number of items to select from seq. Accepts int,
      0 ≤ r ≤ len(seq).

    Example
    -------
    The combinatorial unit may be created like this:
    
    >>> from slowcomb.slowcomb import Combination
    >>> comb = Combination('ABCDEF',r=6)

    The full list of combinations may be dumped by using the CU it as
    an iterator:
    
    >>> for d in comb:
    ...     print(d)
    ('A', 'B', 'C', 'D', 'E', 'F')
    
    Surprise! There is only one distinct way to select all elements
    from a sequence.

    Let's try something different:

    >>> comb = Combination('ABCDEF',r=4)
    >>> for d in comb:
    ...     print(d)
    ('A', 'B', 'C', 'D')
    ('A', 'B', 'C', 'E')
    ('A', 'B', 'C', 'F')
    ('A', 'B', 'D', 'E')
    ('A', 'B', 'D', 'F')
    ('A', 'B', 'E', 'F')
    ('A', 'C', 'D', 'E')
    ('A', 'C', 'D', 'F')
    ('A', 'C', 'E', 'F')
    ('A', 'D', 'E', 'F')
    ('B', 'C', 'D', 'E')
    ('B', 'C', 'D', 'F')
    ('B', 'C', 'E', 'F')
    ('B', 'D', 'E', 'F')
    ('C', 'D', 'E', 'F')

    There are fifteen ways three elements can be selected from six.

    Individual selections may be selected:

    >>> comb[5]
    ('A', 'B', 'E', 'F')

    >>> comb[-5]
    ('B', 'C', 'D', 'E')

    How It Works
    ------------
    For details on how selections are made in this CU, please refer to
    the code and documentation for _get_comb.

    """
    # Slots
    #
    __slots__ = ('_bitmap_src')
    # Methods
    #
    def _get_index(self, x):
        """
        Return the first index of a term, if it is a possible output
        of this Combinatorial Unit.

        Arguments
        ---------
        * x - The term whose index is being sought after. Accepts any 
          Python iterator type.

        Exceptions
        ----------
        * ValueError - when x is not a possible output of this CU.

        """

        # Reconstruct the bitmap from the sequence
        #
        i_last = 0
        bitmap = 0
        for e in x:
            try:
                # Expect element e in x to be found in source...
                i_current = self._seq_src.index(e, i_last)
                bitmap <<= (i_current-i_last)
                    # A jump in the index by more than one
                    # means that there are items that have
                    # not been selected in the combination.
                    # In this case, zeroes will be added to
                    # the bitmap.
                bitmap <<= 1
                bitmap |= 1
                    # Add a raised bit to to mark presence
                    # of a copy the current item in x
                i_last = i_current+1
                    # Advance last source index to prevent
                    # lookups from reaching touched items in
                    # the source sequence. This has a side-effect
                    # of rejecting combinations in which the items
                    # are in a different order from the source
                    # sequence.
                
            except ValueError:
                # Expected exception when item is not found in source
                # sequence
                msg = '{0} is not a member of this sequence'.format(x)
                raise ValueError(msg)

        bitmap <<= (len(self._seq_src) - i_last)
            # Pad the bitmap with zeroes if combination does not include
            # the last item in the source sequence
        return self._bitmap_src.index(bitmap)
 
    def _get_term(self, ii):
        """
        Return the first+ii'th term of the Combination sequence.

        Arguments
        ---------
        * ii - The internal index of the term. Accepts int,
          0 ≤ ii ≤ _ii_stop.

        Term Construction Process of the Combination CU
        -----------------------------------------------
        Combinations are derived from a bitmap. Each bit from
        highest to the lowest (left to right) determines which
        corresponding item in the source sequence, _seq_src,
        will be selected.

        A raised (set to 1) leftmost bit on the bitmap selects
        the leftmost item in _seq_src, and each subsequent bit
        selects a corresponding subsequent item.

        This CU uses the Same Number of Bits Sequence (SNOBSequence)
        in order to construct its bitmaps, which are basically
        binary numbers of a fixed length with a fixed number of
        raised bits.

        Example
        -------
        Here's a list of all the possible 4-element selections 
        from the six-element source ('A','B','C','D','E','F'),
        right next to their bitmaps:

        ABCDEF  Combination
        ======  ====================
        111100	('A', 'B', 'C', 'D')
        111010	('A', 'B', 'C', 'E')
        111001	('A', 'B', 'C', 'F')
        110110	('A', 'B', 'D', 'E')
        110101	('A', 'B', 'D', 'F')
        110011	('A', 'B', 'E', 'F')
        101110	('A', 'C', 'D', 'E')
        101101	('A', 'C', 'D', 'F')
        101011	('A', 'C', 'E', 'F')
        100111	('A', 'D', 'E', 'F')
        011110	('B', 'C', 'D', 'E')
        011101	('B', 'C', 'D', 'F')
        011011	('B', 'C', 'E', 'F')
        010111	('B', 'D', 'E', 'F')
        001111	('C', 'D', 'E', 'F')

        See Also
        --------
        * slowcomb.slowseq.SNOBSequence (in the slowseq.py module)

        """
        out = []
        bitmap = (self._bitmap_src[ii])
            # The ii'th bitmap from the bitmap source should
            #  contain the correct bitmap to derive the
            #  first+ii'th combination
        probe = 1 << len(self._seq_src)-1
        for i in range(len(self._seq_src)):
            if probe & bitmap != 0:
                out.append(self._seq_src[i])
            probe >>= 1 
        return tuple(out)

    def get_term_count(self):
        return int_ncr(len(self._seq_src), self._r)

    def _set_bitmap_src(self):
        self._bitmap_src = SNOBSequence(len(self._seq_src), self._r)
        
    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self):
            raise StopIteration

        out = self[self._i]
        self._i += 1
        return out

    def __init__(self, seq, r, name=None):
        """
        This is the special constructor method which supports 
        creation of a Combination combinatorial unit. 
        
        For details on creating the CU, consult the documentation for
        the Combination class.

        """
        super().__init__(seq, r, name=name)
        self._i = 0
        self._set_bitmap_src()


class CombinationWithRepeats(Combination):
    """
    A sequence of all possible selections, of a predefined size,
    from another source sequence, where elements may be repeated
    Multiple arrangements of the same selection are regarded as the
    same selection.

    This class is an subscriptable analogue to the
    Python's built-in itertools.permutations_with_replacement class

    Arguments
    ---------
    * seq - The source sequence to derive combinations from.

    * r - The number of items to select from seq. Accepts int,
      0 ≤ r ≤ len(seq).
        
    Example
    -------
    The combinatorial unit may be created like this:
    
    >>> from slowcomb.slowcomb import CombinationWithRepeats
    >>> combr = CombinationWithRepeats('ABC',r=3)

    To dump every possible term, the CU may be accessed as an
    iterator:

    >>> for d in combr:
    ...     print(d)
    ('A', 'A', 'A')
    ('A', 'A', 'B')
    ('A', 'A', 'C')
    ('A', 'B', 'B')
    ('A', 'B', 'C')
    ('A', 'C', 'C')
    ('B', 'B', 'B')
    ('B', 'B', 'C')
    ('B', 'C', 'C')
    ('C', 'C', 'C')

    Individual terms may be selected:

    >>> combr[6]
    ('B', 'B', 'B')

    Slicing is also supported:

    >>> combr[1:-2:2]
    (('A', 'A', 'B'), ('A', 'B', 'B'), ('A', 'C', 'C'), ('B', 'B', 'C'))

    How It Works
    ------------
    For details on how selections are made in this CU, please refer to
    the code and documentation for _get_comb.

    """
    def _get_index(self, x):
        """
        Return the first index of a term, if it is a possible output
        of this Combinatorial Unit.

        Arguments
        ---------
        * x - The term whose index is being sought after. Accepts any 
          Python iterator type.

        Exceptions
        ----------
        * ValueError - when x is not a possible output of this CU.

        """
        # Reconstruct the bitmap from the sequence
        #
        elem_last = x[0]
        i_last = self._seq_src.index(x[0])
        bitmap = 0
        for e in x:
            try:
                # Expect element e in x to be in the source...
                if elem_last != e:
                    # Add a zero bit for each change of item in x
                    elem_last = e
                    i_current = self._seq_src.index(e, i_last)
                    bitmap <<= (i_current - i_last)
                    i_last = i_current
                # Add a raised bit for every item of a particular
                # type found
                bitmap <<= 1
                bitmap |= 1
                
            except ValueError:
                # Exception expected when an element in x is not found
                # in the source sequence
                msg = '{0} is not a member of this sequence'.format(x)
                raise ValueError(msg)

        bitmap <<= (len(self._seq_src)-1 - i_last)
            # Add remaining zero bits if there are no items in x
            # of the same type as the last element in the source
        return self._bitmap_src.index(bitmap)
 

    def _get_term(self, ii):
        """
        Return the first+ii'th term of the Repeats-Permitted
        Combination sequence.

        Arguments
        ---------
        * ii - The internal index of the term. Accepts int,
          0 ≤ ii ≤ _ii_stop.

        Term Construction in the CombinationWithRepeats CU
        --------------------------------------------------
        Elements are selected for the terms of the CU based on
        bitmaps. A '1' (raised) bit indicates the presence of an
        item, while a zero (lowered) bit indicates a change to the
        next item in the source sequence, _seq_src.

        The length of the bitmap would be equal to the number of
        selections (r-value), plus the number of items in _seq_src,
        minus one. The number of raised bits is equal to the r-value
        (in _r) of the CU.

        This CU uses the Same Number of Bits Sequence (SNOBSequence)
        in order to construct its bitmaps, which are basically
        binary numbers of a fixed length with a fixed number of
        raised bits.

        This technique was taken from Chapter 1 "The Sample Space",
        of Volume 1 of the 1959 edition of "An Introduction to
        Probability Theory and its Applications" by William Feller.
        Feller describes the use of 'stars' and 'bars' (p12) to
        select and partition items to systematically include and
        exclude them. They are, perhaps counterintuitively,
        represented here by 1's for stars and zeroes for bars.

        Example
        -------
        Here's a list of all the possible 3-element selections 
        from the six-element source ('A','B','C'), right next to
        their bitmaps:

        Bitmap  Term
        ======  ===============
        11100	('A', 'A', 'A')
        11010	('A', 'A', 'B')
        11001	('A', 'A', 'C')
        10110	('A', 'B', 'B')
        10101	('A', 'B', 'C')
        10011	('A', 'C', 'C')
        01110	('B', 'B', 'B')
        01101	('B', 'B', 'C')
        01011	('B', 'C', 'C')
        00111	('C', 'C', 'C')

        The bitmap is 3+3-1 == 5 bits long, and has 3 bits raised.

        References
        ----------
        * Wikipedia. Stars and bars (combinatorics).
          https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)

        """
        out = []
        iii_seq = 0
        mask_width = len(self._seq_src)-1 + self._r
        bitmap = self._bitmap_src[ii]
        probe = 1 << mask_width - 1
        while (probe > 0):
            if probe & bitmap == 0:
                iii_seq += 1
            else:
                out.append(self._seq_src[iii_seq])
            probe >>= 1 
        return tuple(out)

    def get_term_count(self):
        seq_len = len(self._seq_src)
        return int_ncr(seq_len-1 + self._r, self._r)

    def _set_bitmap_src(self):
        """
        Set up the selection bitmap source in order to map out items
        to be selected from the source sequence in order to perform
        the combinations.

        """
        seq_len = len(self._seq_src)
        self._bitmap_src = SNOBSequence(seq_len-1 + self._r, self._r)

    def __init__(self, seq, r, name=None):
        """
        This is the special constructor method which supports 
        creation of a CombinationWithRepeats combinatorial unit. 
        
        For details on creating the CU, consult the documentation for
        the CombinationWithRepeats class.

        """
        super().__init__(seq, r, name=name)

