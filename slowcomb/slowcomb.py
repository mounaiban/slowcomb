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
    the Slow Combinatorics Library.
 
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
        """Get the number of subsets the CombinatorialUnit. 
        is able to return. Returns the count as an int.

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

    Thus the following properties apply:

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
    terms of the same length. 
 
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
    A sequence of all possible combinations of items from multiple
    position-dependent sequences, where items from the first sequence
    only appears on the first element of the combination, and items 
    from the second appear second, and so on...

    NOTE: It is possible to make the CatCombination class function like
    a permutator, but position-dependent combinations are the main
    intended use of this class, hence its name.

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

    >>> catcomb = CatCombination ( (('I',), ('need', 'want'), \
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

    A CatCombination whose r=0 only returns empty tuples. 
    This is in aligment with the behaviour of the ``combinations`` class
    from Python's itertools.

    >>> catcomb = CatCombination(seqs, r=0)
    >>> len(catcomb)
    1

    >>> catcomb[0]
    ()

    Fun activity: what output does a CatCombinator with r=None produce?
    Enter it and find out for yourself. Hint: see the class docstring for
    PBTreeCombinatorialUnit.

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
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        * x - The term to be searched for. Accepts any Python iterator
          type.

        """
        temp_ii = 0
        temp_src = self._seq_src[1:]
            # Strip the leading second-level sequence representing 
            # Level 0 (root with origin node) of the combinatorial tree
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

        Treatment of Tree Path
        ----------------------
        Each element in the addresses tuple returned by
        _get_comb_tree_path() is regarded as the index of an element of
        one of the sub-sequences of _seq_src.

        The i'th element of the path references an item on the i'th
        sequence.

        Example
        =======
        Referring to our example combinatorial unit:

        >>> from slowcomb.slowcomb import CatCombination
        >>> catcomb = CatCombination ( (('I',), ('need', 'want'), \
        ... ('sugar', 'spice', 'scissors')), r=3)

        And its corresponding tree:

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
        CatCombinator trees branch from a normally hidden origin node
        on Level zero, which counts as 1 node.

        Level n has the same number of nodes as elements in _seq_src[n].
        Each node on that level has as many child nodes as _seq_src[n+1].

        The PBTree of a CatCombinator has the same number of levels
        of the number of sub-sequences in _seq_src, which includes
        the origin node.

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
        creation of combinatorial units. 
        
        For details on creating the CU, consult the documentation of
        the combinatorial unit class above.

        """
        # Construction Routine
        seq_init = [ (None,) ] # Place the root node
        seq_init.extend(seqs)
        seq_src = tuple(seq_init)

        self._func_len_siblings = lambda lvl : len(self._seq_src[lvl])
        super().__init__(self._get_comb,self._func_len_siblings,seq_src, r)


class Permutation(PBTreeCombinatorialUnit):
    """Addressable Permutator

    A sequence of all possible re-arranged versions a source sequence,
    or all possible arrangements of a subset of the source sequence given
    a specific subset length.

    Uses PBTreeCombinatorialUnit to generate its combinations.

    Examples
    --------
    Full Re-arrangement
    ===================
    What are possible (re-)arrangements of this list of words: 'heads,
    shoulders, knees, toes'?

    i   Permutation
    ==  =======================================
    0   ('heads', 'shoulders', 'knees', 'toes')
    1   ('heads', 'shoulders', 'toes', 'knees')
    2   ('heads', 'knees', 'shoulders', 'toes')
    3   ('heads', 'knees', 'toes', 'shoulders')
    4   ('heads', 'toes', 'shoulders', 'knees')
    5   ('heads', 'toes', 'knees', 'shoulders')
    6   ('shoulders', 'heads', 'knees', 'toes')
    7   ('shoulders', 'heads', 'toes', 'knees')
    8   ('shoulders', 'knees', 'heads', 'toes')
    9   ('shoulders', 'knees', 'toes', 'heads')
    10  ('shoulders', 'toes', 'heads', 'knees')
    11  ('shoulders', 'toes', 'knees', 'heads')
    12  ('knees', 'heads', 'shoulders', 'toes')
    13  ('knees', 'heads', 'toes', 'shoulders')
    14  ('knees', 'shoulders', 'heads', 'toes')
    15  ('knees', 'shoulders', 'toes', 'heads')
    16  ('knees', 'toes', 'heads', 'shoulders')
    17  ('knees', 'toes', 'shoulders', 'heads')
    18  ('toes', 'heads', 'shoulders', 'knees')
    19  ('toes', 'heads', 'knees', 'shoulders')
    20  ('toes', 'shoulders', 'heads', 'knees')
    21  ('toes', 'shoulders', 'knees', 'heads')
    22  ('toes', 'knees', 'heads', 'shoulders')
    23  ('toes', 'knees', 'shoulders', 'heads')

    Subsets
    =======
    If you were to pick just two words from the list, how many
    arrangements can you make from those two words?

    i   Permutation (r=2)
    ==  ======================
    0   ('heads', 'shoulders')
    1   ('heads', 'knees')
    2   ('heads', 'toes')
    3   ('shoulders', 'heads')
    4   ('shoulders', 'knees')
    5   ('shoulders', 'totes')
    6   ('knees', 'heads')
    7   ('knees', 'shoulders')
    8   ('knees', 'toes')
    9   ('toes', 'heads')
    10  ('toes', 'shoulders')
    11  ('toes', 'knees')

    The resulting combinatorics tree can be visualised as:

    ::
        t k  t s  k s  t k  t h  k h  t s  t h  s h  k s  k h  s h
        | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |
        k t  s t  s k  k t  h t  h k  s t  h t  h s  s k  h k  h s
        \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/
         |    |    |    |    |    |    |    |    |    |    |    |
         s.   k.   t.   h.   k.   t.   h.   s.   t.   h.   s.   k.
          \____\___/     \___|___/      \___|___/      \___/____/
                \            |              |             /
                 h.          s.             k.           t.
                  \___________\____________/____________/
                                     |
                                     0

        legend: h.-heads, s.-shoulders, k.-knees, t.-toes

    The permutations are ordered as they appear on the tree from
    left to right. The algorithm used to determine the node counts is
    described in the _set_node_counts() method in this class.

    Please note that the last level always has one node per parent,
    and therefore the same number nodes as the second-last level.
    This is due to the element elimination of the permutation process.

    """
    def _get_index(self, x):
        """
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        x - The term to be searched for. Accepts any Python iterator type.

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
        """Changes the source sequence.

        Arguments
        ---------
        seq - Sequence to be permutated. Accepts any Python sequence.

        """
        self._seq_src=tuple(seq)
        self._set_thresholds()

    def _set_node_counts(self):
        """Sets up the node count embedded sequence, _node_counts, to
        enable the combinatorics tree's addressing method to function.

        Node Counts for Permutation
        ---------------------------
        * Level 0 always has one node, the root node.
        * All levels have the number of nodes in the previous Level
        multiplied by the number of branches per node in the previous
        Level (as with all PBTrees).
        * The number of branches per node in Level 0 is the number of
        items in the source sequence.
        * All Levels thereafter have one less branch per node than the
        previous Level. This is due to the elimination process during 
        permutation to prevent items from repeating.

        Example
        =======
        With reference to our example in the documentation of the
        Permutation class, suppose we have a four-long source sequence:

        ('heads', 'shoulders', 'knees', 'toes')

        * 1 node for Level 0 (the root node)
        * 4*1 == 4 nodes for Level 1
        * 3*4 == 12 for Level 2
        * 2*12 == 24 for Level 3
        * 1*24 == 24 for Level 4

        The two last Levels will always have the same number of nodes.

        The _node_counts for our example permutator will be equivalent
        to (1, 4, 12, 24, 24)

        """
        self._node_counts = CacheableSequence(
            lambda_int_npr(len(self._seq_src)),
            length = len(self._seq_src)+1
        )
        self._node_counts.enable_cache()

    def _get_perm(self, ii):
        """Return the first+ii'th permutation of the source sequence

        Arguments
        ---------
        ii - Internal Index of the permutation. Accepts int, 
            0 ≤ i < self._ii_stop

        Treatment of Combinatorial Tree Path
        ------------------------------------
        The path returned by _get_comb_tree_path() is a tuple which is
        regarded as a navigation route through the permutation tree.
        Each element of the path is coincidentially a reference to
        an interim list of indices to the source sequence. In resolving
        each of these interim indices, each index is removed (popped) 
        from the list once it is used, and the corresponding data item
        copied to to output list.

        The result of accessing the source sequence this way is
        the creation of a re-arranged version of it.

        Example
        =======
        With reference to our class documentation, here is a permutator
        set up to output four-word permutations, with a source sequence
        containing four words:

        ('heads', 'shoulders', 'knees', 'toes')
        
        In maths textbook-ese, this is a 4P4 permutation.

        And here's a reprint of the original permutation tree:

        ::
            1                                       *               24
            t k  t s  k s  t k  t h  k h  t s  t h  s h  k s  k h  s h
            | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |
            k t  s t  s k  k t  h t  h k  s t  h t  h s  s k  h k  h s
            \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/
             |    |    |    |    |    |    |    |    |    |    |    |
             s.   k.   t.   h.   k.   t.   h.   s.   t.   h.   s.   k.
              \____\___/     \___|___/      \___|___/      \___/____/
                    \            |              |             /
                     h.          s.             k.           t.
                      \___________\____________/____________/
                                         |
                                         0

        legend: h.-heads, s.-shoulders, k.-knees, t.-toes, *-17th 4P4 perm.

        We will now derive the seventeenth four-word permutation, marked
        on the diagram above with an asterisk. The route generated by
        _get_comb_tree_path will be (0, 2, 2, 0, 0). Each number in
        the tuple means a navigation to the first+n'th node. This
        tuple will be called ``addrs``.

        With the address at hand, let's derive the permutation!

        A temporary list, herein called ``out`` is first created to
        collect the permuted data for output.

        To reduce memory consumption, a list of references is generated
        to represent the source sequence, ``_seq_src``. The references
        are simply a series of integers from -1 to the last index of the
        source sequence. In our example it is (-1, 0, 1, 2, 3). This tuple
        will be called ``idxs``.

        The address tuple will then be read from left to right, and its
        corresponding item on the source references list:

        1. The first+zeroth element in addrs, addrs[0] will always be 0,
        as per PBTreeCombinatorialUnit conventions. This corresponds to the 
        first element in idxs, -1, the reference to the origin node
        at Level 0. The origin node is not included in output, so 
        this index will be discarded. This item is removed from idxs.

        End Result: addrs==(0, 2, 2, 0, 0), idxs==[0, 1, 2, 3],
        out==[]

        NOTE: the -1 was chosen out of convenience to simplify code,
        and has no reference to any data on the source sequence.

        2. Next, the first+1st element in addrs (addrs[1]) is read,
        this resolves to 2. This number is used to index idxs, resulting
        in idxs[2], which is coincidentially also 2. This item is popped,
        removed as it is read. The item to add to ``out`` is _seq_src[2],
        the first+2nd word in ('heads', 'shoulders', 'knees', 'toes').
        
        End Result: addrs==(0, 2, 2, 0, 0), idxs==[0, 1, 3], 
        out==['knees']

        3. The process is repeated for the addrs[2], which returns 2.
        This is used to resolve idxs[2], resolving to 3. In using that
        to resolve _seq_src[3], the word returned is 'toes', which is
        copied to the end of ``out``.

        End Result: addrs==(0, 2, 2, 0, 0), idxs==[0, 1], 
        out==['knees', 'toes']

        4. The process is yet repeated, this time for addrs[3], returning
        another 0. That is used to resolve and pop idxs[0], returning
        a 0. This number is then used to resolve _seq_src[0], returning
        the word 'heads'.

        End Result: addrs==(0, 2, 2, 0, 0), idxs==[1,], 
        out==['knees', 'toes', 'heads']

        5. Finally, to complete the process, addrs[4], which is 0 is used
        in resolving the last remaining idxs item, idxs[0], returning 1.
        Note that the last element of addrs is always 0. At this point,
        idxs has no more elements. Using this to resolve _seq_src[1],
        the word 'shoulders' is returned, and added to ``out``.
        
        End Result: addrs==(0, 2, 2, 0, 0), idxs==[], 
        out==['knees', 'toes', 'heads', 'shoulders']

        The sequence out may now be converted to a tuple and returned
        to the method or function that requested it.
        
        """
        addrs = self._get_comb_tree_path(ii)
        out = []
        seq_src_idxs = [x for x in range(-1, len(self._seq_src))]
            # Create a list of indices to the source sequences
            #  instead of deep copying the actual data
            # The -1 only refers to the root node, it will be
            #  discarded
        for iii in addrs:
            # Resolve the indices in seq_sec_refs to the actual
            #  data in _seq_src. Ignore the -1 reference to the
            #  root node.
            ir = seq_src_idxs.pop(iii)
            if(ir >= 0):
                out.append(self._seq_src[ir])
        return tuple(out)

    def __init__(self, seq, r=None):
        """Create an addressable Permutation sequence

        Arguments
        ---------
        seq - a sequence to be used as the source sequence of the
            permutator.

        Optional Arguments
        ==================
        r - the r-value, or the size of the subsets output by the
            permutation. Accepts int, 0 ≤ r ≤ len(seq).

            * Setting r to None causes the permutator to include
                permutations for all possible sizes in the sequence.

            * Setting r to 0 causes it to output only empty
                tuples, effectively disabling it.
        
        Examples
        --------
        Let's create the permutators from the documentation of the
        Permuation class.

        Full Permutation
        ================
        We will start with the full-length permutator which reorders
        the entire four word phrase:

        >>> from slowcomb.slowcomb import Permutation
        >>> words = ('heads','shoulders','knees','toes')
        >>> perm = Permutation(words, r=4)
        >>>     # Easy Mode
        >>> perm = Permutation(('heads','shoulders','knees','toes'),r=4)
        >>>     # Hardcore Mode
        
        And here's yet another reprint of the original permutation
        tree, with a slightly different numbering:

        ::
            0                A         B            C               23
            t k  t s  k s  t k  t h  k h  t s  t h  s h  k s  k h  s h
            | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |  | |
            k t  s t  s k  k t  h t  h k  s t  h t  h s  s k  h k  h s
            \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/
             |    |    |    |    |    |    |    |    |    |    |    |
             s.   k.   t.   h.   k.   t.   h.   s.   t.   h.   s.   k.
              \____\___/     \___|___/      \___|___/      \___/____/
                    \            |              |             /
                     h.          s.             k.           t.
                      \___________\____________/____________/
                                         |
                                         0


        legend: h.-heads, s.-shoulders, k.-knees, t.-toes 

        The nodes all start with an index of zero on the left.

        Let's try the different permutations:
        >>> perm[0]
        ('heads', 'shoulders', 'knees', 'toes')

        >>> perm[7] # Node A
        ('shoulders', 'heads', 'toes', 'knees')

        >>> perm  [11] # Node B, the space was left here on purpose
        ('shoulders', 'toes', 'knees', 'heads')

        >>> perm[16] # Node C
        ('knees', 'toes', 'heads', 'shoulders')

        Partial Permutation
        ===================
        We will now try two-word permutations. The permutation tree
        will now be like this:

        ::

           0              D                   E              F    11
           s.   k.   t.   h.   k.   t.   h.   s.   t.   h.   s.   k.
            \____\___/     \___|___/      \___|___/      \___/____/
                  \            |              |             /
                   h.          s.             k.           t.
                    \___________\____________/____________/
                                       |
                                       0

        legend: h.-heads, s.-shoulders, k.-knees, t.-toes 

        Let's create the permutator:

        >>> words = ('heads','shoulders','knees','toes')
        >>> perm = Permutation(words,r=2)

        Then, let's get the permutations...

        >>> perm[0] 
        ('heads', 'shoulders')

        >>> perm[3] # Node D
        ('shoulders', 'heads')

        >>> perm[7] # Node E
        ('knees', 'shoulders')

        >>> perm[10] # Node F
        ('toes', 'shoulders')

        Fun Activity: Create a nine-word permutator and a ten-word
        permutator with the same ten-word source sequence. Use len()
        on the permutator to find the number of permutations in either
        sequence. What do you observe?

        """
        # Construction Routine
        self._func = self._get_perm
        self._seq_src = seq
        self._func_len_siblings = lambda lvl: len(self._seq_src) - (lvl-1)

        super().__init__(self._get_perm, self._func_len_siblings, seq, r)
        self._set_thresholds()


class PermutationWithRepeats(Permutation):
    """Addressable Permutation With Permitted Repetition Sequence

    A sequence of all possible uses of elements from a source sequence,
    including uses of the same elements in a different order.

    There are probably many other names for such a sequence, but this
    name was chosen as it was observed to have a very similar effect
    to allowing permutations to have repeating elements.
    
    Uses PBTreeCombinatorialUnit to generate its combinations.

    Example
    -------
    Permutation with Same Size as Source Sequence
    =============================================
    What can you have for breakfast, lunch, and dinner, from a selection
    of ('milk', 'beer', 'wine')?

    i   Permutation (r=3)
    ==  ========================
    0   ('milk', 'milk', 'milk')
    1   ('milk', 'milk', 'beer')
    2   ('milk', 'milk', 'wine')
    3   ('milk', 'beer', 'milk')
    4   ('milk', 'beer', 'beer')
    5   ('milk', 'beer', 'wine')
    6   ('milk', 'wine', 'milk')
    7   ('milk', 'wine', 'beer')
    8   ('milk', 'wine', 'wine')
    9   ('beer', 'milk', 'milk')
    10  ('beer', 'milk', 'beer')
    11  ('beer', 'milk', 'wine')
    12  ('beer', 'beer', 'milk')
    13  ('beer', 'beer', 'beer')
    14  ('beer', 'beer', 'wine')
    15  ('beer', 'wine', 'milk')
    16  ('beer', 'wine', 'beer')
    17  ('beer', 'wine', 'wine')
    18  ('wine', 'milk', 'milk')
    19  ('wine', 'milk', 'beer')
    20  ('wine', 'milk', 'wine')
    21  ('wine', 'beer', 'milk')
    22  ('wine', 'beer', 'beer')
    23  ('wine', 'beer', 'wine')
    24  ('wine', 'wine', 'milk')
    25  ('wine', 'wine', 'beer')
    26  ('wine', 'wine', 'wine')

    The resulting combinatorics tree can be visualised as:

    ::
      
       m b w  m b w  m b w  m b w  m b w  m b w  m b w  m b w  m b w
       \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/
         |      |      |      |      |      |      |      |      |
         m.     b.     w.     m.     b.     w.     m.     b.     w.
         \______|______/      \______|______/      \______|______/
                |                    |                    |
                m.                   b.                   w.
                \____________________|____________________/
                                     |
                                     0

        legend: m.-milk, b.-beer, w.-wine

    Fun Facts
    ---------
    * You can achieve a similar (or probably identical) sequence using
    a CatCombinator, and using multiple copies of the same source
    sub-sequence.
    * This permutator was almost called PokiesPermutator, due to the
    similarity to its output to payline readouts on certain types of
    gambling machines.

    """
    def _get_index(self, x):
        """
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        x - The term to be searched for. Accepts any Python iterator type.

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
        """Sets up the node count embedded sequence, _node_counts, to
        enable the combinatorics tree's addressing method to function.

        Node Counts for PermutationsWithRepeats
        ----------------------------------------
        * Level 0 always has one node, the origin node.
        * All subsequent Levels have the number of nodes to the power
        of the Level number. This is due to the number of branches
        per node being constant and equal to the number of items in the
        source sequence throughout the entire permutation tree.

        Example
        =======
        Consider a repeats-permitted permutation, with twelve-element
        source sequence. The node counts per level would be as follows,
        when r=4:

        * 1 node for Level 0 
        * 12*1 == 12 nodes for Level 1
        * 12*12 == 144 nodes for Level 2
        * 144*12 == 1728 nodes for Level 3
        * 1728*12 == 20736 nodes for Level 4

        """
        self._node_counts = NumberSequence(
            lambda x : len(self._seq_src) ** x,
            length = self._r+1
        )

    def _get_perm(self, ii):
        """Return the first+ii'th permutation of the source sequence

        Arguments
        ---------
        ii - Internal Index of the permutation. Accepts int, 
            0 ≤ i < self._ii_stop

        Treatment of Addresses
        ----------------------
        The address tuple returned by _get_comb_tree_path() is used
        to directly address items in the source sequence. This is
        possible with the repeats-permitted permutation, as the
        nodes on the permutation tree have the same number of child
        nodes, due to the lack of elimination. Thus, the navigation
        route in the address tuple directly maps to the source sequence
        data.

        Example
        =======
        Referring to our example in the documentation of the
        PermutationsWithRepeats class, we have a permutator with an
        r-value of 3, and a source sequence with three items
        ('milk', 'beer', 'wine').

        The permutation tree has been reprinted below:

        ::
      
           1                        *                                 27
           m b w  m b w  m b w  m b w  m b w  m b w  m b w  m b w  m b w
           \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/  \_|_/
             |      |      |      |      |      |      |      |      |
             m.     b.     w.     m.     b.     w.     m.     b.     w.
             \______|______/      \______|______/      \______|______/
                    |                    |                    |
                    m.                   b.                   w.
                    \____________________|____________________/
                                         |
                                         0

        legend: m.-milk, b.-beer, w.-wine

        We will address and derive the 12th sequence from the left, marked
        with an asterisk in the diagram. The address tuple, herein called
        ``addrs``, and returned by _get_comb_tree_path() should be 
        (0, 1, 0, 2).

        The output will be collected in a list ``out``.

        The first+zero'th element of addrs (addrs[0]) is always zero, as
        it references the origin node. This node is not present in any
        output and is thus discarded.

        The first+first element in the address tuple, addrs[1], resolves
        to 1. The same address is used on the source sequence, to get
        the element at _seq_src[1], which resolves to 'beer', which is in
        turn copied to out.

        Result: addrs==(0, 1, 0, 2), out==['beer',]

        Following up with addrs[2], which resolves to 0, this index is
        once again used directly on the source sequence to get the word 
        in _seq_src[0], 'milk', and copy it to out.

        Result: addrs==(0, 1, 0, 2), out==['beer', 'milk']

        Repeating the same process with addrs[3], we complete the
        permutation.

        Result: addrs=(0, 1, 0, 2), out==['beer', 'milk', 'wine']

        The output is ready to be converted to a tuple and returned
        to the caller.

        """
        addrs = self._get_comb_tree_path(ii)
        out = []
        for i_addr in range(1,len(addrs)):
            out_data = self._seq_src[addrs[i_addr]]
            if out_data is not None:
                out.append(out_data)
        return tuple(out)

    def __init__(self, seq, r):
        """
        Create an Addressable Repeats-Permitted Permutation Sequence

        Arguments
        ---------
        seq - The source sequence to derive permutations from. Any
            Python sequence may be used.

        r - The length of the terms derived by the permutation.
            This argument is mandatory. Accepts int, r ≥ 0.
            Note that the r value can exceed the number of elements
            in the source sequence.

        Example
        -------

        In a certain scratch-and-reveal lottery ticket, there are
        twelve panels. Any of the four icons may be hidden under those
        panels. The panels are divided into three groups. The first
        three are in the 1st group, the next three in the 2nd and
        so on.

        Prizes are awarded depending on the number of groups having
        the same icon in all three panels.
        
        Let's create a permutator that will find every possible
        way the icons may appear:

        >>> from slowcomb.slowcomb import PermutationWithRepeats
        >>> icons = ('B', 'R', 'N', 'S')
        >>> perm_st = PermutationWithRepeats(icons,r=12)
        >>>     # B-bracelet, R-ring, N-necklace, S-sunglasses
        >>>     # The items are abbreviated to save screen space.
        >>>     # As you can see, this is a high fashion-themed
        >>>     # scratchie.

        Now, let's try some interesting permutations:
        >>> perm_st[438564]
        ('B', 'B', 'R', 'N', 'N', 'S', 'B', 'R', 'B', 'N', 'R', 'B')

        >>> perm_st[9136497]
        ('N', 'B', 'N', 'S', 'R', 'N', 'N', 'R', 'R', 'S', 'B', 'R')

        And some boring ones:
        >>> perm_st[4194304]
        ('R', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B')
        
        Well, boring unless you bought the ticket...
        
        >>> perm_st[1864135]
        ('B', 'R', 'S', 'B', 'R', 'S', 'B', 'R', 'S', 'B', 'R', 'S')

        You'll be **really** lucky to find this ticket, yet the luck
        doesn't really get you anything...

        Look at the sheer number of possible permutations:
        >>> len(perm_st)
        16777216

        That's basically the number of 24-bit numbers!
        
        Fun Activity: How can you control or predict the appearance
        of the icons under the panels? Hint-it really helps when you
        are well-versed with binary arithetic...
        
        """
        super().__init__(seq, r)

        # Construction Routine
        self._func_len_siblings = lambda x: len(self._seq_src) 
            # Override self._func_len_siblings
        self._seq_src = seq
        self._set_thresholds()


class Combination(CombinatorialUnit):
    """Addressable Combination Sequence
    
    An addressable sequence of all possible selections from a source
    sequence. Multiple permutations of the same selections are regarded
    as the same selection.
    
    This class is an addressable analogue to the combination class
    from Python's itertools.

    """
    def _get_index(self, x):
        """
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        x - The term whose index is being sought after. Accepts any 
            Python iterator type.

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
        """Sets appropriate limits for the internal index, so that it
        may report the length of the sequence correctly.

        """
        self._set_bitmap_src()
        self._ii_stop = len(self._bitmap_src)

    def _get_comb(self, ii):
        """
        Return the first+ii'th term of the Combination sequence.

        Arguments
        ---------
        ii - The internal index of the term. Accepts int,
        0 ≤ ii ≤ _ii_stop.

        Treatment of Addresses by the Combination Sequence
        --------------------------------------------------
        Combinations are derived from a bitmask (or bitmap).
        In this class, the highest (or leftmost) bit deterines
        selection of the first item in the source sequence,
        the second-highest for the second item, and so on.

        A raised (set to 1) bit on the bitmask marks its
        corresponding item for selection.

        The ``Combination`` class uses the Same Number of Bits
        Sequence, the SNOBSequence, in order to count through
        successive numbers of the same length with the same 
        number of set bits when represented in binary. The bit
        length of the number is set to the number of items in
        the source sequence, and the number of those bits that
        are raised is set to the number of items to be selected.
        This has an effect of steppping through all possible
        selections.

        Example
        -------
        Out of a list of of seven secondary items to take on an
        adventure, you are only allowed to take five. What are
        the possible selections you can make?

        Your items are: boot polish, fan, flip-flops, lip balm,
        neck pillow, teddy bear and USB battery.

        To save screen space, they are herein abbreviated to
        ('bp', 'fan', 'ff', 'lb', 'np', 'tb', 'ub').

        i   Bitmask  Combination
        ==  =======  ================================
        0   1111100  ('bp', 'fan', 'ff', 'lb', 'np')
        1   1111010  ('bp', 'fan', 'ff', 'lb', 'tb')
        2   1111001  ('bp', 'fan', 'ff', 'lb', 'ub')
        3   1110110  ('bp', 'fan', 'ff', 'np', 'tb')
        4   1110101  ('bp', 'fan', 'ff', 'np', 'ub')
        5   1110011  ('bp', 'fan', 'ff', 'tb', 'ub')
        6   1101110  ('bp', 'fan', 'lb', 'np', 'tb')
        7   1101101  ('bp', 'fan', 'lb', 'np', 'ub')
        8   1101011  ('bp', 'fan', 'lb', 'tb', 'ub')
        9   1100111  ('bp', 'fan', 'np', 'tb', 'ub')
        10  1011110  ('bp', 'ff', 'lb', 'np', 'tb')
        11  1011101  ('bp', 'ff', 'lb', 'np', 'ub')
        12  1011011  ('bp', 'ff', 'lb', 'np', 'ub')
        13  1010111  ('bp', 'ff', 'np', 'tb', 'ub')
        14  1001111  ('bp', 'lb', 'np', 'tb', 'ub')
        15  0111110  ('fan', 'ff', 'lb', 'np', 'tb')
        16  0111101  ('fan', 'ff', 'lb', 'np', 'ub')
        17  0111011  ('fan', 'ff', 'lb', 'tb', 'ub') 
        18  0110111  ('fan', 'ff', 'np', 'tb', 'ub')
        19  0101111  ('fan', 'lb', 'np', 'tb', 'ub')
        20  0011111  ('ff', 'lb', 'np', 'tb', 'ub')

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
        """Create an Addressable Combination sequence
        
        Arguments
        ---------
        seq - The source sequence to derive combinations from.

        r - The number of items to select from seq. Accepts int,
            0 ≤ r ≤ len(seq).

        Example
        -------
        Let's recreate the example in the documentation of
        _get_comb and enumerate the combinations: there are seven
        items, and five items are to be selected.

        The items are abbreviations of 'boot polish', 
        'electric fan', 'flip-flops', 'lip balm', 'neck pillow',
        'teddy bear' and 'USB battery'.

        >>> from slowcomb.slowcomb import Combination
        >>> items = ('bp', 'fan', 'ff', 'lb', 'np', 'tb', 'ub')
        >>> comb = Combination(items, r=5)

        We can now recall the combinations at random:

        >>> comb[0]
        ('bp', 'fan', 'ff', 'lb', 'np')

        >>> comb[9]
        ('bp', 'fan', 'np', 'tb', 'ub')

        >>> comb[18]
        ('fan', 'ff', 'np', 'tb', 'ub')

        """
        super().__init__(self._get_comb, seq, r, ii_start=0)


class CombinationWithRepeats(Combination):
    """Addressable Repeats-Permitted Combination Sequence
    
    An addressable sequence of all possible selections from a source
    sequence, including multiple selections of the same element.
    Multiple permutations of the same selections are regarded as the
    same selection.

    To achieve multiple selections of the same element, for a 
    given size (r-value) of a combination, the combinations for
    all smaller r-values until 1 are evaluated. The smaller subsets
    resulting from such selections are then padded by repeating the
    first item until the selection reaches the target size.

    This class is an analogue to the permutations_with_replacement class
    from Python's itertools.

    """
           
    def _get_index(self, x):
        """
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        x - The term whose index is being sought after. Accepts any 
            Python iterator type.

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
        ii - The internal index of the term. Accepts int,
        0 ≤ ii ≤ _ii_stop.

        Treatment of Addresses
        ----------------------
        Addresses of the repeats-permitted combinations are derived
        from bitmasks with a set number of bits, with a set number
        of those bits raised (set to 1).

        A raised bit indicates the presence of an item, while a
        lowered (zero) bit indicates a change in the item to select.

        This means that the length of the bitmask would be equal
        to the number of selections (r-value), plus the number of
        items in the source sequence minus one.

        This technique was taken from Chapter 1 "The Sample Space",
        of Volume 1 of the 1959 edition of "An Introduction to
        Probability Theory and its Applications" by William Feller.
        Feller describes the use of 'stars' and 'bars' (p12) to
        select and partition items to systematically include and
        exclude them into subsets, which, perhaps counterintuitively,
        is represented here by 1's for stars and zeroes for bars.

        See Also: Wikipedia. Stars and bars (combinatorics).
        https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)

        Example
        -------
        At a certain pizza shop, you are allowed three topping
        serves to your pizza without any extra charge. You have three 
        choices, and are allowed to pick the same choice more than
        once, thus doubling, or tripling down the same thing.

        Your choices are ('tomatoes', 'mushroom', 'pineapple').

        In maths textbook-ese, this will be a 3C3 selection. However,
        the bitmask will be run with arguments n=(3+3-1), c=3

        i   Bitmask  Combination
        ==  =======  ======================================
        0   11100    ('tomato', 'tomato', 'tomato')
        1   11010    ('tomato', 'tomato', 'mushroom')
        2   11001    ('tomato', 'tomato', 'pineapple')
        3   10110    ('tomato', 'mushroom', 'mushroom')
        4   10101    ('tomato', 'mushroom', 'pineapple')
        5   10011    ('tomato', 'pineapple', 'pineapple')
        6   01110    ('mushroom', 'mushroom', 'mushroom')
        7   01101    ('mushroom', 'mushroom', 'pineapple')
        8   01011    ('mushroom', 'pineapple', 'pineapple')
        9   00111    ('pineapple', 'pineapple', 'pineapple')

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
        """Set up the selection bitmap source in order to map out items
        to be selected from the source sequence in order to perform
        the combinations.

        """
        seq_len = len(self._seq_src)
        self._bitmap_src = SNOBSequence(seq_len-1 + self._r, self._r)

    def __init__(self, seq, r):
        """Create an Addressable Repeats-Permitted Combination sequence

        Arguments
        ---------
        seq - The source sequence to derive combinations from.

        r - The number of items to select from seq. Accepts int,
            0 ≤ r ≤ len(seq).
        
        Example
        -------
        Let's re-create the example from the documentation of 
        _get_comb in code:

        >>> from slowcomb.slowcomb import CombinationWithRepeats
        >>> choices = ('tomato', 'mushroom', 'pineapple')
        >>> combr = CombinationWithRepeats(choices,r=3)

        The choices can be directly accessed and recalled at random:
        >>> combr[0]
        ('tomato', 'tomato', 'tomato')

        >>> combr[4]
        ('tomato', 'mushroom', 'pineapple')

        >>> combr[9]
        ('pineapple', 'pineapple', 'pineapple')
        
        Fun Activity
        ------------
        The restaurant began to offer more choices, expanding the 
        selection to a total of six choices: anchovies, artichokes,
        fetta, mushrooms, tomato and pineapple. The larger selection
        has been abbreviated to ('an', 'ar', 'fe', 'mu', 'to', 'pi').

        You are now able to choose up to four serves, with the option
        of selecting the same thing more than once.

        >>> from slowcomb.slowcomb import CombinationWithRepeats
        >>> choices_x = ('an', 'ar', 'fe', 'mu', 'to', 'pi')
        >>> combr_x = CombinationWithRepeats(choices_x, r=4)

        However, the number of possible combinations is huge!

        >>> len(combr_x)
        126

        Sure, it is now easy to pick a random selection, but what
        about control?

        Try to find a way of precisely controlling your selection
        and mapping your selection to an index number...

        """
        super().__init__(seq, r)

