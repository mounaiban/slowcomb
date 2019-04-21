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
from slowcomb.slowseq import lambda_int_npr, int_ncr,\
    AccumulateSequence, NumberSequence, CacheableSequence, SNOBSequence

# Classes
#
class CombinatorialUnit(CacheableSequence):
    """
    Superclass which supports implementations of Combinatorial Units
    the Slow Combinatorics Library. These Combinatorial Units, or
    CUs are sequences of combinatorial terms that are lazily evaluate
    combinatorial terms as they are requested.
 
    Required Arguments
    ------------------
    A combinatorial unit class should have the following:
    
    * func - function or method to derive the combinatorial subset.
      Accepts a lambda or block function or method.

    * seq - a sequence to be the data source from which to derive
      combinatorial terms. If seq supports a reverse-lookup method
      named index(), the CU becomes capable of finding out the index
      from raw combinatorial results.
      The simplest examples are strings, but any sequence may be used.
      Map it to blobs, database records, other CombinatorialUnit objects
      or anything that is subscriptable. Think big!

    * r - the size of the subset to be derived in this sequence.
      Optional for some combinatorial units.
      Named after r-value used in maths textbooks to describe the size
      of a combinatorial term which is a different size from the
      set being worked on (i.e. nPr, nCr), by way of the r-values in
      Python's combinatorial itertools classes.
 
    Optional Arguments
    ------------------
    * ii_start - the starting internal index of the sequence.

    Examples
    --------
    See Combination, CombinationWithRepeats, CatCombination,
    PBTreeCombinatorialUnit and its subclasses (Permutation and
    PermutationWithRepeats).

    """
    # Slots
    #
    __slots__ = ('_r', '_seq_src', '_exceptions')

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
 
    def _get_subset_count(self):
        """
        Get the number of subsets the CombinatorialUnit is able to
        return. Returns the count as an int.

        This is simply the distance between the first internal
        index and the last internal index. These depend on the
        type of combinatorial unit involved.

        """
        return self._ii_stop - self._ii_start

    def __getitem__(self, key):
        """
        Supports direct lookups of terms in a CombinatorialUnit.

        Both int and slice inputs are accepted as keys.

        """
        if self.is_valid() is False:
            return self._default
        else:
            return super().__getitem__(key)

    def __len__(self):
        """
        Gets the total possible number of terms of a combinatorial
        unit. Returns int.

        """
        if self.is_valid() is True:
            # The threshold of the last level is also the 
            # node count
            return self._get_subset_count()
        else:
            # Non-valid combinatorics sequences always report a
            # length of one, to account for the default value.
            return 1

    def __init__(self, func, seq, r=None, ii_start=1):
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
        self._seq_src = seq
            # The source sequence from which to derive combinatorial
            # terms
        self._r = r
            # Sets a fixed length for terms returned by the
            # combinatorial unit.

        #  Other Stat Keepers
        #
        self._exceptions = None
            # Reserved attribute
            # To be set to true if exceptions have been encountered
            # during the operation of this Combinator

        # Construction Routine
        super().__init__(func, length=len(seq),
                ii_start=ii_start, default=() )


class PBTreeCombinatorialUnit(CombinatorialUnit):
    """
    A superclass for supporting the implementations of combinatorial
    units that make use of Perfectly-Balanced Trees, B-Trees whose
    node counts and content can be figured out algorithmically for
    each and every node ahead of time.

    Required Arguements
    -------------------
    * func - function or method to derive combinatorial terms.
      Accepts a lambda or block function or method. The definition
      should look like:

      * In module or method scope: func(i), where i is the external
        index of the term.

      * In class scope: func(self, i), where i is the external
        index of the term.

    * seq - a sequence to be set as the data source from which to derive
      combinatorial terms. If seq supports a reverse-lookup method
      named index(), the CU becomes capable of finding out the index
      from raw combinatorial results. The simplest examples are strings,
      but any sequence, including database records or even other
      combinatorial units, may be used.

    * func_len_siblings - function to determine the number of nodes
      on the tree with a common parent. All nodes on the same level
      are assumed to have the same number of parent nodes. Accepts
      methods, block function or lambda functions with the following
      definition:

      * In module or method scope: f(lvl), where lvl is an int
        representing the level the node is on in the tree.

      * In class scope: f(self, lvl) where lvl is an int
        representing the level the node is on in the tree.


    Optional Arguments
    ------------------
    * r - the size of the subset to be derived in this sequence.
      Optional for some combinatorial units. Accepts None, or int
      where r ≥ 0.
      If r is None, the PBTreeCombinatorialUnit steps through
      every term of every possible size, from smallest to largest.


    How It Works
    ------------

    About the PBTree
    ================
    The Perfectly-Balanced Tree (PBTree) is a virtual tree data
    structure in which the number of children per node is exactly
    the same for each node on the same level of the tree, and the
    content of the nodes are predictably repeated across the tree.

    As a virtual tree, the actual tree is not present in memory,
    but its nodes are lazily evaluated as they are requested.

    The following properties apply to the PBTree:

    1. The number of nodes per level is a multiple of nodes on the
    previous level.

    2. Every node on the same level share the same exact number of
    sibling nodes.

    3. Any node is allowed to have an arbitrary number of child nodes,
    as long as traits 1 and 2 above apply.

    4. The path to a node can be determined from its index expressed
    as a numerical quantity, by a series of simple arithmetic
    operations.


    Illustration and Indexing
    =========================
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

    Each node is numbered breadth first, from 'left to right, then
    bottom to top'.

    Levels begin at zero and count upwards:

    * Level 0 comprises node 0

    * Level 1 comprises nodes 1, 2 and 3
    
    * Level 2 comprises nodes 4, 5, 6, 7, 8 and 9

    * Level 3 comprises nodes 10 thru 21

    The levels are tracked internally using an embedded sequence,
    _thresholds, which keeps track of the next node after the last
    node of a particular level. In this example:

    * Level 0's threshold is 1

    * Level 1's threshold is 4

    * Level 2's threshold is 10

    * Level 3's threshold is 22 (not shown in tree)


    Using the PBTree for Combinatorial Operations
    ---------------------------------------------

    Paths
    =====
    The path to each node can be used to represent a combinatorial
    result, and the contents of each node could represent the elements
    of the combinatorial term. The exact content of the nodes depends
    on the subclass of PBTreeCombinatorics.

    Paths are sequences of child node numbers, which begin from zero for
    the leftmost child.
   
    In our example, the path to node 5 will be (0,0,1), while term 18
    will be (0,2,0,0).

    Selecting Terms By Length (r-value)
    ===================================
    The path to each node on a particluar level represents combinatorial
    terms of the same length. A combinatorial unit can be set up for
    returning terms of a set length by constraining the CU to selecting
    nodes of a particular level.
    
    For example, in a massive, ten-level combinatorial tree, allowing
    only Level 3 nodes to be selected causes the CU to only return
    three-element terms. Likewise, allowing only Level 10 elements
    to be selected by the CU causes the CU to only return ten-element
    terms.

    Setting the r-value to zero constrains the CU to only selecting
    the normally-hidden root node. This causes the CU to only output
    the default value, an empty tuple ().
 
    Use of Internal Indices
    =======================
    The indices of nodes in the PBTree are internal indices.

    Internal indices can be constrained to begin on the first node
    of a particular level, and end on the last node of the same level,
    to create a CU which returns terms of a specific length.

    In our example, setting _ii_start to 10 and _ii_stop to 22 constrains
    our CU to three (or four, depending on the CU) -element terms.
    External index 0 will map to node ten, and index 11 will map to
    node 21.
   
    See Also
    --------
    * CatCombination

    * Permutation 

    * PermutationWithRepeats 

    """
    # Slots
    #
    __slots__ = ('_func_len_siblings', '_node_counts', '_thresholds')

    # Methods
    #
    def _get_ii_level(self, ii):
        """
        Returns the level of a node in the combinatorics tree as an
        int.

        In the PBTree, the level which a node rests on is determined
        from its index, and a sequence of indices of the next node
        after the last node of each level. These indices are kept
        in an embedded sequence, _thresholds. 

        The root of the tree is regarded as Level 0.
        
        Arguments
        ---------
        * ii - The internal index of the term of the sequence. Accepts int,
          0 ≤ i < self._ii_stop

        See Also
        --------
        * _set_thresholds

        """

        for t in range(len(self._thresholds)):
            if(ii < self._thresholds[t]):
                return t
        # If ii is larger than the last threshold, it is
        #  out of range
        raise IndexError('internal index is past the last level')

    def _get_comb_tree_path(self, ii):
        """
        Find out the path to a particular node of index ii on the
        PBTree, returns a tuple representing a path to the node.

        Each element of the path represents the number of the child
        node to navigate into, with the first child on the left
        as number zero.

        How The Path Discovery Works
        ----------------------------
        The path to a PBTree node can be discovered from its node number
        using a series of simple arithmetic operations.

        The tree from the class documentation above has been replicated
        here for your pleasure: 

        ::
                             * 
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
        
        In this example, we will find the path to node 16, marked with
        an asterisk. The discovery process herein begins from the 
        right-hand end of the path.

        There are several facts we have to find out from various
        metadata to discover the rightmost path index:

        * Is on Level three (from _thresholds)

        * Is on a level with twelve nodes (from _node_counts)

        * Is node number six on this level (subtract 16 from
          _thresholds), remembering that the the first node is given
          the number zero. In code, this is referred to as 'distance
          from left'.
        
        * Has two siblings, (from _func_len_siblings)

        * Is a child of node 7 (from dividing its position on this
          level by the number of siblings, then adding it back
          to index of the first node of Level one).

        In shorthand, we could write this as ii=16,lvl=3,n=12,d=6,
        sibs=2.

        However, the most important number is node 16's sibling number,
        which is determined by n % sibs (the remainder of n divided by
        sibs). From this, we find that node 16 is sibling zero of 
        node 7.
        
        We save this in a sequence, and our path so far is [,0].
        
        Repeating the process on node 7, we find that lvl=2,n=6,d=3,
        sibs=2, and that it is *sibling one* (from d%n) of node 2 
        (from d//sibs + 1)

        We add this fact to the left side of our sequence, making it
        [,1,0].

        Continue with node 2, finding out that lvl=1,n=3,d=1,sibs=3,
        and that this node is *sibling one* of node 0.

        Add this fact to the left of our sequence, resulting in
        [,1,1,0].

        The process ends with node 0, where lvl=0,n=1,d=0,sibs=0.
        This node has no siblings, thus assuming the default path
        0.

        We complete the path by adding this fact to the left of the
        route, ending up with [0,1,1,0].

        """
        ii_lvl = self._get_ii_level(ii)
        if ii_lvl == 0:
            # Special case for looking up level zero
            # This is to prevent negative level lookups, which
            # don't work due to how things are implemented.
            d_lvl = 0
        else:
            d_lvl = ii - self._thresholds[ii_lvl-1]
            # Distance of the last component of the
            # i'th term from the left of the combinator tree.
        addrs = []
        for level in range(ii_lvl,-1,-1):
            # Resolve relative distance to an index
            j = d_lvl % self._func_len_siblings(level)
            addrs.insert(0,j)
            # Scale down distance for the next shallower level 
            d_lvl //= self._func_len_siblings(level)
        return tuple(addrs)

    def _get_full_subset_count(self):
        """
        Return the total possible number of subsets with all
        possible r's for a PBTreeCombinatorialUnit.

        The number of total subsets is also the number of nodes
        in the combinatorics tree, which in turn coincides with
        the last node index level threshold.
        """
        return self._thresholds[len(self._thresholds)-1]

    def _get_child_iidxs(self, ii):
        """
        Return a slice covering the internal index range for the
        immediate child nodes of a particular node

        Arguments
        ---------
        * ii - integer index of the internal index of a node on the
          combinatorial tree.

        """
        lvl = self._get_ii_level(ii)
        lvl_start = self._thresholds[lvl]
        lvl_d = ii - lvl_start
            # Distance from beginning of current tree level
        lvl_siblings = self._func_len_siblings(lvl)
        next_lvl = lvl+1
        next_lvl_start = self._thresholds[next_lvl]
        next_lvl_siblings = self._func_len_siblings(next_lvl)
        sub_start = next_lvl_start + lvl_d*next_lvl_siblings
        sub_stop = sub_start + next_lvl_siblings
        return slice(sub_start, sub_stop)
    
    def _set_node_counts(self):
        """
        Placeholder method for setting node counts per level
        on the combinatorics tree.

        """
        raise NotImplementedError

    def _set_thresholds(self):
        """
        Sets the threshold indices of the combinatorial tree.
        This method triggers the node counting method, _set_node_counts().

        See Also
        --------
        * The class documentation above, under the heading Illustration
          and Indexing, for the definition of thresholds.

        """
        self._set_node_counts()
            # Need to count the nodes first
        total = 0
        counts = []
        for i in self._node_counts:
            total += i
            counts.append(total)
        self._thresholds = tuple(counts)

    def _set_ii_bounds(self):
        """
        Sets start (_ii_start) and stop (_ii_stop) bounds for the
        internal index, so that only terms of a specific length
        are accessible, and so that the correct number of terms
        in this combinatorial unit is reported by len() correctly.

        This method triggers the threshold setting method,
        _set_thresholds(), which in turn triggers _set_node_counts().

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
        
        Referring to our illustration from the class documentation yet
        again, the bounds are as follows:

        * If _r = 0, 0 ≤ ii ≤ 0 (or, ii == 0)

        * If _r = 1, 1 ≤ ii ≤ 3

        * If _r = 2, 4 ≤ ii ≤ 9

        * If _r = 3, 10 ≤ ii ≤ 21

        """
        self._set_thresholds()
            # Must set thresholds first
        if isinstance(self._r, int):
            if self._r <= 0:
                self._ii_start = 1
                self._ii_stop = 1
            else:
                self._ii_start = self._thresholds[self._r-1]
                self._ii_stop = self._thresholds[self._r]
        else:
            i_last_threshold = len(self._thresholds) - 1
            self._ii_stop = self._thresholds[i_last_threshold]
            self._ii_start = 1

    def __init__(self, func, func_len_siblings, seq, r=None):
        """
        This is the special constructor method which supports 
        creation of combinatorial units. 
        
        For details on creating the CU, consult the documentation of
        the combinatorial unit class.

        """
        self._func_len_siblings = func_len_siblings
            # Function to find the number of nodes with a common parent
            #  on a given level. This function should take one argument
            #  (excluding self, if a method is used instead), and return
            #  and int representing the number of sibling nodes.
        self._node_counts = []
        self._thresholds = []
        super().__init__(func, seq, r, ii_start=0)
 

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

    Optional Arguments
    ------------------
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

    Fun activity: what output does a CatCombinator with r=None produce?
    Enter it and find out for yourself. Hint: see PBTreeCombinatorialUnit,
    under the section Optional Arguments.

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
    def add_sequence(self, seq, t=1):
        """
        Add another sequence to the sequence of source sequences
        
        Arguments
        ---------
        * seq - Source sequence. Accepts any Python sequence.
            
        * t - Number of times to repeat the sequence. Accepts int,
          t ≥ 1

        """
        temp = list(self._seq_src)
        temp.extend([seq]*t)
        self._seq_src = tuple(temp)
        self._set_ii_bounds()

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
        temp_ii = 0
        temp_src = self._seq_src[1:]
            # Strip the leading sub-sequence representing Level 0
            # (root) of the combinatorial tree
        levels = len(x)
        for lvl in range(levels):
            # Traverse the combinatorial tree
            try:
                iii_elem = temp_src[lvl].index(x[lvl])
            except ValueError:
                msg = '{0} not an output of this sequence'.format(x)
                raise ValueError(msg)
            child_nodes = self._get_child_iidxs(temp_ii)
            temp_ii = child_nodes.start + iii_elem
                # Advance the temp_ii index further into the subtree
        return temp_ii - self._ii_start
            # Return the external index resolved from internal index

    def _get_args(self):
        """
        Attempt to rebuild a probable equivalent of the arguments
        used in initialising a CatCombination sequence

        """
        seq_shown = self._seq_src[1:]
            # Strip leading None from the outer sequence
        re_arg_fmt = "seq={0}, r={1}"
        return re_arg_fmt.format(seq_shown, self._r)

    def _get_comb(self, ii):
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
        addrs = self._get_comb_tree_path(ii)
        out = []
        for i in range(len(addrs)):
            out_data = self._seq_src[i][addrs[i]]
            if out_data is not None:
                out.append(out_data)
        return(tuple(out))
    
    def _set_node_counts(self):
        """
        Counts the number of tree nodes, and keeps them in the embedded
        sequence _node_counts. This information is necessary in creating
        paths to nodes on the tree. For more information on when and how
        this information is used, refer to the class documentation for 
        PBTreeCombinatorialUnit._get_comb_tree_path().

        Node Counts of a CatCombinator
        ------------------------------
        The normally-hidden root node in Level 0 counts as 1 node.

        Level x has the same number of nodes as elements in _seq_src[x].
        Each node on that level has as many child nodes as _seq_src[x+1].

        The PBTree of a CatCombinator has the same number of levels
        of the number of sub-sequences in _seq_src, which includes
        the root node.

        In our example CatCombinator:

        ::

          s_a = ('I',)
          s_b = ('need','want')
          s_c = ('sugar','spice','scissors') 
          seqs = (s_a, s_b, s_c)
          catcomb = CatCombination(seqs, r=3)

        There would have been 3 levels (0 to 2).

        Level zero would have 1 node; Level one, 1 node; Level two, 2
        nodes and Level three, 6 nodes.

        This makes a total of 10 nodes.

        See Also
        --------
        * PBTreeCombinatorialUnit

        * PBTreeCombinatorialUnit._get_comb_tree_path()

        """
        func_node_counts = lambda i : len(self._seq_src[i])
        func_product_seq = lambda i,a : i*a
            # This basically makes the AccumulateSequence 
            #  a product sequence.
        self._node_counts = AccumulateSequence(func_node_counts,
            func_product_seq, length=len(self._seq_src))
        self._node_counts.enable_cache()
    
    def __init__(self, seqs, r=None):
        """
        This is the special constructor method which supports 
        the creation of a CatCombination combinatorial unit. 
        
        For details on how to do this, please consult the documentation
        for the CatCombination class.

        """
        # Construction Routine
        seq_init = [ (None,) ] # Place the root node
        seq_init.extend(seqs)
        seq_src = tuple(seq_init)

        self._func_len_siblings = lambda lvl : len(self._seq_src[lvl])
        super().__init__(self._get_comb,self._func_len_siblings,seq_src, r)


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
        temp_x = list(x)
        temp_src = list(self._seq_src)
        temp_ii = 0
        levels = len(temp_x)
        for lvl in range(levels):
            elem = temp_x.pop(0)
            try:
                iii_elem = temp_src.index(elem)
            except ValueError:
                msg = '{0} not an output of this sequence'.format(x)
                raise ValueError(msg)
            temp_src.pop(temp_src.index(elem))
                # Exclude elements that have been found from next search
            subtree_slice = self._get_child_iidxs(temp_ii)
            temp_ii = subtree_slice.start + iii_elem
        return temp_ii - self._ii_start
            # Return the external index resolved from internal index

    def set_src(self, seq):
        """
        Change the source sequence.

        Arguments
        ---------
        * seq - Sequence to be permutated. Accepts any Python sequence.

        """
        self._seq_src=tuple(seq)
        self._set_thresholds()

    def _set_node_counts(self):
        """
        Counts the number of tree nodes, and keeps them in the embedded
        sequence _node_counts. This information is necessary in creating
        paths to nodes on the tree. For more information on when and how
        this information is used, refer to the class documentation for 
        PBTreeCombinatorialUnit._get_comb_tree_path().

        Node Counts of a Permutation
        ----------------------------
        The normally-hidden root node in Level zero counts as 1 node.

        The number of nodes per level from Level one onwards is equal to:

        ::
        
          (n - (x-1)) * n[x-1]

        Where:

        * n means the number of elements in _seq_src

        * x is the level number

        * n[x] means the number of nodes on level x

        All successive levels after Level one have one less branch
        per node than the previous Level. This is due to the elimination
        process during permutation to prevent items from repeating.

        Example
        =======
        With reference to our example above, the node counts for a
        permuataion on ('heads', 'shoulders', 'knees', 'toes')
        would be:

        * 1 node for Level 0 (the root node)

        * 4*1 == 4 nodes for Level 1

        * 3*4 == 12 for Level 2

        * 2*12 == 24 for Level 3

        * 1*24 == 24 for Level 4

        The two last Levels will always have the same number of nodes.

        """
        self._node_counts = CacheableSequence(
            lambda_int_npr(len(self._seq_src)),
            length = len(self._seq_src)+1
        )
        self._node_counts.enable_cache()

    def _get_perm(self, ii):
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
        i = ii - self._ii_start 
            # FIXME: This undoes the internal index (ii) mapping for
            # the time being. The use of ii mapping will be removed
            # from Permutation CUs in the future.
            #

        path = [0,] * self._r
            # Start with an all-zero path, as only the rightmost
            # elements will change for lower indices.
        iii = self._r - 1
        n = len(self._seq_src)
        sibs = n - self._r + 1
        # Build the path in memory
        while sibs <= n:
            path_elem = i % sibs
            path[iii] = path_elem
            i //= sibs
            sibs += 1
            iii -= 1

        # Build the actual term
        temp = []
        temp.extend(self._seq_src)
        out = []
        for i in tuple(path):
            out.append(temp.pop(i))
        return tuple(out)


    def __init__(self, seq, r=None):
        """
        This is the special constructor method which supports 
        creation of a Permutation combinatorial unit. 
        
        For details on creating the CU, consult the documentation
        for the Permutation class.

        """
        # Construction Routine
        self._func = self._get_perm
        self._seq_src = seq
        self._func_len_siblings = lambda lvl: len(self._seq_src) - (lvl-1)

        super().__init__(self._get_perm, self._func_len_siblings, seq, r)
        self._set_thresholds()


class PermutationWithRepeats(Permutation):
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
        temp_ii = 0
        levels = len(x)
        for i in range(levels):
            elem = x[i]
            try:
                iii_elem = self._seq_src.index(elem)
            except ValueError:
                msg = '{0} not an output of this sequence'.format(x)
                raise ValueError(msg)
            child_nodes = self._get_child_iidxs(temp_ii)
            temp_ii = child_nodes.start + iii_elem
                # Advance the temp_ii index further into the combinatorial
                # tree
        return temp_ii - self._ii_start
            # Return the external index resolved from internal index
            
    def _set_node_counts(self):
        """
        Sets up the node count embedded sequence, _node_counts, to
        enable tree paths to be constructed.

        Node Counts for PermutationsWithRepeats
        ----------------------------------------
        * Level 0 always has one node, the root node.

        * All subsequent Levels have the number of elements in _seq_src
          to the power of the Level number, as number of branches per
          node is constant and equal to the number of items in _seq_src
          throughout the entire permutation tree.

        Example
        =======
        Consider a three-element repeats-permitted permutation unit.
        The node counts per level would be as follows, when r=4:

        * 1 node for Level 0 

        * 3*1 == 3 nodes for Level 1

        * 3*3 == 9 nodes for Level 2

        * 9*3 == 27 nodes for Level 3

        """
        self._node_counts = NumberSequence(
            lambda x : len(self._seq_src) ** x,
            length = self._r+1
        )

    def _get_perm(self, ii):
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

        This also means that the tree path can be directly worked out
        using just the external decimal integer index of the term.
        The current method uses a double-division process: the index
        number is divided for the remainder to get the path element,
        then integer-divided again to distribute remaiing value over
        to the subsequent digits, if any.

        Example
        =======
        Referring to our example permutator:
        
        >>> permwr = PermutationWithRepeats(('🍇', '🍈', '🍉'),r=3)

        The combinatorial tree can be visualised as:

        ::
                                    *
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

        Where 0 == 🍇, 1 == 🍈, 2 == 🍉 and X == Origin
        Node 11 is marked with the *
        Tree levels start from Level 0.

        Tracing the paths of the tree, one ends up with base-3 numbers.
        Here are the first nine:

        Lv3 Node  Path       Term
        ========  =========  ==========
        0         (0,0,0)    (🍇,🍇,🍇)
        1         (0,0,1)    (🍇,🍇,🍈)
        2         (0,0,2)    (🍇,🍇,🍉)
        3         (0,1,0)    (🍇,🍈,🍇)
        4         (0,1,1)    (🍇,🍈,🍈)
        5         (0,1,2)    (🍇,🍈,🍉)
        6         (0,2,0)    (🍇,🍉,🍇)
        7         (0,2,1)    (🍇,🍉,🍈)
        8         (0,2,2)    (🍇,🍉,🍉)

        The root node X is ignored during term derivation and skipped
        over by the algorithm.

        """
        i = ii - self._ii_start 
            # FIXME : This hack undoes the internal address (ii) mapping.
            # The ii-mapping will be completely removed from all tree
            # combinatorial units in the near future.
            # 
        sibs = len(self._seq_src)
            # Node siblings
        out = [self._seq_src[0],] * self._r
            # Output, pre-filled with leftmost item from _seq_src
        iii = len(out)-1
        while i > 0:
            path_elem = i % sibs
            out[iii] = self._seq_src[path_elem]
                # Optimisation: Immediately resolve path_elem and
                # copy referenced element to out. Equivalent to
                # working out all path_elems into a distinct number,
                # then processing the number by using it to get
                # data from _seq_src to derive the term.
            iii -= 1
            i //= sibs
        else:
            return tuple(out)


    def __init__(self, seq, r):
        """
        This is the special constructor method which supports 
        creation of a PermutationWithRepeats combinatorial unit. 
        
        For details on creating the CU, consult the documentation for 
        the PermutationWithRepeats class.

        """
        # Construction Routine
        super().__init__(seq, r)

        # Construction Routine
        self._func_len_siblings = lambda x: len(self._seq_src) 
            # Override self._func_len_siblings
        self._seq_src = seq
        self._set_thresholds()


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
 
    def _set_ii_bounds(self):
        """
        Sets appropriate limits for the internal index, so that 
        len() reports the correct number of possible terms.

        """
        self._set_bitmap_src()
        self._ii_stop = len(self._bitmap_src)

    def _get_comb(self, ii):
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
    
    def _set_bitmap_src(self):
        """Set up the selection bitmap source in order to map out items
        to be selected from the source sequence in order to perform
        the combinations.

        """
        self._bitmap_src = SNOBSequence(len(self._seq_src), self._r)

    def __init__(self, seq, r):
        """
        This is the special constructor method which supports 
        creation of a Combination combinatorial unit. 
        
        For details on creating the CU, consult the documentation for
        the Combination class.

        """
        super().__init__(self._get_comb, seq, r, ii_start=0)


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
 

    def _get_comb(self, ii):
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

    def _set_bitmap_src(self):
        """
        Set up the selection bitmap source in order to map out items
        to be selected from the source sequence in order to perform
        the combinations.

        """
        seq_len = len(self._seq_src)
        self._bitmap_src = SNOBSequence(seq_len-1 + self._r, self._r)

    def __init__(self, seq, r):
        """
        This is the special constructor method which supports 
        creation of a CombinationWithRepeats combinatorial unit. 
        
        For details on creating the CU, consult the documentation for
        the CombinationWithRepeats class.

        """
        super().__init__(seq, r)

