"""
slowcomb — Slow Addressable Combinatorics Library main module. Supports
the use of Combinations, Catenation Combinations and Permutations with
individually-addressable terms (subsets).
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
from slowcomb.slowseq import lambda_int_npr, lambda_int_ncr, int_ncr,\
    AccumulateSequence, NumberSequence, CacheableSequence, SNOBSequence

# Classes
#
class Combinatorics(CacheableSequence):
    """
    Superclass which contains essential methods for implementing
    the first-party Combinatorics sequences in the Slow Combinatorics
    Library.

    Combinatorics sequences may be NumberSequences, or any of its
    Cacheable variants.
    """

    def is_valid(self):
        """
        Check if a Combinatroics sequence is ready to return any
        results.
        
        Returns True if ready, False otherwise.

        If a Combinatorics sequence is not ready, it should return
        a length of ``1``, and a default output, which in most cases
        is an empty tuple.

        This mechanism is intended to prevent a problematic sequence
        from locking up a complex chain of sequences should an invalid
        configuration be made by accident, or should the source
        sequence become unexpectedly unavailable.
        """
        # Return False if the sequence is set to work on itself
        if self._seq_src is self:
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

    def _prescreen_index_search_term(self, x):
        """Rejects search terms unsuitable for use with the index()
        method on various combinatorial sequence classes.

        Raises ValueError when a search term is rejected.

        Arguments
        ---------
        x - search term to be used with index()

        """
        if x is None:
            raise ValueError('Search term cannot be None')
        if self._r is not None:
            if len(x) != self._r:
                msg = "term must have a length of {0}".format(self._r)
                raise ValueError(msg)

    def _get_args(self):
        """Attempt to rebuild a probable equivalent of the arguments
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
        """Get the number of subsets the Combinatorics sequence. 
        is able to return. Returns the count as an int.

        This is simply the distance between the first internal
        index and the last internal index, whose method for setting
        these values depends on the type of combinatorics operation
        involved.
        """
        return self._ii_max - self._ii_start

    def __getitem__(self, key):
        """
        Supports direct lookups of terms in a Combinatorics sequence.

        Both integer and slices are accepted as keys.
        """
        if self.is_valid() is False:
            return self._default
        else:
            return super().__getitem__(key)

    def __len__(self):
        """
        The length of a Combinator as returned by len() is equal
        to the total possible number of outcomes it can return.
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
        """Supports the creation of a combinatorics sequence
        implemented using the Combinatorics class.

        This method is intended to be called from a subclass of
        the Combinatorics class.

        Arguments
        ---------
        
        Required Arguments
        ==================
        A Combinatorics class should have the following parameters:
        
        func - function or method to derive the subset.
        seq - a sequence to be set as a source of data to derive
            data subsets from. For examples, please check the subclasses,
            especially Combination and Permutation.

        Optional Arguments
        ==================
        r - the size of the subset to be derived in this sequence.
            Accepts zero and positive integers or None.
            The behaviour of a Combinatroics sequence when r is set to
            None is currently undefined.
        ii_start - the starting internal index of the sequence.

        Examples
        --------
        See Combination, CombinationWithRepeats, CatCombination,
        PBTreeCombinatorics and its subclasses (Permutation and
        PermutationWithRepeats).

        """
        # Validate Arguments 
        if r is not None:
            if(r < 0):
                raise ValueError('r, if present, must be zero or more')

        # Instance Attributes
        self._seq_src = seq
            # The source sequence from which to generate combinations
            #  (or permutations). The simplest examples use strings,
            #  but any sequence may be used. Map it to blobs, 
            #  database records, anything that has a sequence identifier.
            #  Even other Combinatorics sequences may be used. Think big!
        self._r = r
            # The length of a single term returned by the combinator.
            # Named after the r-arguments used in various classes in
            # Python's itertools, which is in turn named after the
            # r-argument (sometimes k) in partial combinations (nCr)
            # and permutations (nPr).
        #  Other Stat Keepers
        self._exceptions = None
            # Reserved attribute
            # To be set to true if exceptions have been encountered
            # during the operation of this Combinator

        # Construction Routine
        super().__init__(func, length=len(seq),
                ii_start=ii_start, default=() )
            # The _n value of a combinatorics sequence is the number of
            #  items in the set being selected or permutated from.
            # This meaning of _n overrides that of NumberSequence.


class PBTreeCombinatorics(Combinatorics):
    """Perfect Balanced Tree Combinatorics Sequence Class
    
    A superclass for supporting the implementations of combinatorial
    algorithms which derive results from a perfectly-balanced tree,
    which is simply a B-tree where the number of sub-nodes can be
    figured out algorithmically for each and every node ahead of time.

    Properties of the Slowcomb PBTree
    ---------------------------------
    Several traits are assumed to be true of the perfectly-balanced
    tree:

    1. The number of nodes per level is a whole-number multiple of
        nodes on the previous level.

    2. Every node on the same level has the same number of child nodes.
        Therefore, every node on the same level has the same number of
        sibling nodes

    3. Any node is allowed to have an arbitrary number of child nodes,
        as long as traits 1 and 2 above ``is True``.
    

    Getting Subsets from a PBTree
    -----------------------------
    Terms
    =====
    The each node, along with all the nodes on the path to that
    particular node, in order of navigation, represents one term in
    the sequence.

    Selecting Terms By Length (r-value)
    ===================================
    All siblings (nodes of the same depth or height) on the tree are
    terms of the same length. Therefore, terms of the same r-value 
    may be derived by selecting paths to nodes of a particular depth.
    
    Indexing
    --------
    A PBTreeCombinatorics sequence may be accessed with an integer index,
    and each node is numbered breadth first; from 'left to right,
    bottom to top', like in this example:

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

    Levels begin at zero and count upwards:
    * Level 0 comprises node 0
    * Level 1 comprises nodes 1, 2 and 3
    * Level 2 comprises nodes 4, 5, 6, 7, 8 and 9
    * Level 3 comprises nodes 10 thru 21

    Therefore, for example, term 5 will be (0,1,5), while term 18 will
    be (0,3,8,18).

    Note: The tree in this example is drawn from the bottom. Just imagine
    it upside-down if you like your trees that way.

    Use of Internal and External Indices
    ====================================
    With a PBTreeCombinatorics sequence, the internal index can be
    locked to indices of nodes of a particular depth. In our example
    above, to allow only the selection of subsets of three elements,
    simply set the internal index starting point, _ii_start, to 4 and
    the highest interal index, _ii_max, to 9.

    The external index (i=0) is therefore mapped to the node 4.
    There will be six nodes, making the last index of the sequence
    (i=5) map to node 9.

    Use of Node and Level 0
    =======================
    The use of Node 0 and Level 0 is defined by the type of combinatorics
    operation. Some types of operations make use of it, while some others
    will hide it from the consumer during normal operation.

    Examples
    --------
    Please see Permutation and PermutationWithRepeats below.

    """
    def _get_ii_level(self, ii):
        """Find out on which level in the combinatorics tree a node 
        is on by its internal index number. Returns the level number
        as an int.

        In a perfectly balanced tree, the level which a node rests on
        can be determined from its index. The PBTreeCombinatorics
        sequence keeps track of these levels, in an embedded sequence,
        _thresholds. 

        The root of the tree is regarded as Level 0.
        
        This method regards the thresholds as a barrier or stop for
        a particular level. This makes the internal index right 
        before the threshold the upper bound of a particular level.
        For example, _thresholds[0] is always one. Therefore, the
        zero'th level ends at ii=0.

        Thus, a level is determined by the n'th threshold which
        it first fails to meets or exceed. For more information on
        thresholds, see _set_thresholds.

        Arguments
        ---------
        ii - The internal index of the term of the sequence. Accepts int,
            0 ≤ i < self._ii_max

        Example
        -------
        In the example depicted in the docstring of the 
        PBTreeCombinatorics class, the thresholds would have been
        (1, 4, 10).

        """
        # TODO: Is _ii_max actually confusing, as ii cannot actually
        #  reach it? It might be wiser to call it ii_stop, to emphasise
        #  its similarity in purpose to the stop value of a slice.

        for t in range(len(self._thresholds)):
            if(ii < self._thresholds[t]):
                return t
        # If ii is larger than the last threshold, it is
        #  out of range
        raise IndexError('internal index is past the last level')

    def _get_comb_tree_path(self, ii):
        """
        Find out the tree path required to re-construct the i'th term
        of the combinatorics sequence. Returns a tuple of int internal
        indices.

        The indices are navigation routes in the combinatorics tree.
        The exact method of resolving the path to a term of the
        sequence is to be defined in the subclass inheriting from
        this class.

        How The Addressing Works
        ------------------------
        Referring to the example tree depicted in the documentation of
        the PBTreeCombinato class, which has been replicated here for
        your pleasure: 

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
        
        In order to reconstruct term 16, and trace its path back to
        the origin node 0, this method attempts to find out the level
        the term sits on, and its distance from the left of the tree.

        The path is presented as a tuple of ``int`` indices, each
        ``int`` corresponding to the index of an item on the source
        sequence, _seq_src, and also the sub nodes to navigate into.
        The index of these paths begin at zero. The algorithm used in
        this method gets elements, from the furthest to the closest
        to the root.

        Deriving the First Element of the Path
        ======================================
        The 16th term is on Level 3 (recalling that the 0th term is
        on Level 0). The distance from the left of the level can be
        determined from the distance of the term from the previous
        level's threshold (10), which is also the start of Level 3.

        In our example, the distance from the left works out to be 6.

        Recalling trait 2 in the PBTreeCombinatorics class 
        documentation, we can find out which sibling branch it is by
        finding the remainder of the division by the number of
        siblings it has. In this example, there are two siblings per
        node at Level 3. Therefore, 16 (16%2 == 0) is the first
        sibling.
        
        This actually the last element of the path, 0. Recall that
        we are resolving the path from the furthest to the closest.

        Deriving the Next Elements of the Path
        ======================================
        To navigate from Node 16 back to Node 7, simply select the
        corresponding node in the next lower level, which is Level 2.
        To find this node, keep in mind the left distance of Node 16
        in the last level, and divide it by the number of siblings in
        the last level.

        * In Level 3, we found that the Node 16 had distance of six
        nodes from the left. Each node had 2 siblings on this Level,
        and Node 16 had path value of zero.

        * In Level 2, the parent of Node 16 will have a distance of three
        (i.e. 6/2) from the left. Keeping in mind that node indices on
        the level start from zero, the node with a left distance of three
        on Level 2 is the parent, Node 7. 

        * In Level 2, nodes have two siblings. Therefore, Node 7 is the 
        second sibling because (a distance of 3) % (2 siblings per node)
        is equal to 1, the second sibling from zero. This is also the
        second-last element of our path. Therefore, our path so far
        is (1,0).

        * In Level 1, the parent of Node 7 will have a distance of one,
        1%3==1 from the left, as each node has three siblings on this Level.
        Therefore the parent is Node 2.
        
        * In Level 1, Node 2 is the the second sibling because (a distance
        of 1) % (3 siblings per node) is equal to 1, making it the second
        sibling, recalling that sibling indices start from zero. Therefore,
        we find the third-last element of the path: 1. This makes our
        path so far (1,1,0).

        * Finally in Level 0, all left distances resolve to zero. This
        makes the path at Level 0 always zero, consistent with the
        properties of a traditional tree structure. Our path becomes
        (0,1,1,0).

        See Also
        --------
        Permutation, PermutationWithRepeats and CatCombination on applications
        of the PBTree combinatorics.

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
        possible r's for a PBTreeCombinatorics seqence.

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
        ii - integer index of the internal index of a node on the
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
        """Placeholder method for setting node counts per level
        on the combinatorics tree.
        """
        raise NotImplementedError

    def _set_thresholds(self):
        """Prepares the internal sequence of thresholds, or guard
        indices indicating the barrier after the last index on the
        combinatorics tree.

        This method triggers the node counting method, _set_node_counts().

        ::
                4   5    6   7     8   9  
                 \__|    \___/    /___/
                     \     |     /
                      1    2    3
                       \___|___/
                           | 
                           0
        
        Referring once again to a truncated version of our example 
        from the documentation of the PBTreeCombinatorics class:

        * The threshold of Level 0 is 1.
        * The threshold of Level 1 is 4.
        * The threshold of Level 2 is 10, which is beyond the last Level.

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
        """Sets appropriate limits for the internal index, so that it may
        report the length of the combinatorics sequence correctly.

        The length is based both on the r-value (_r) of the sequence, and
        the length of the source sequence.

        Both minimum and maximum bounds are set.

        This method triggers the threshold setting method, _set_thresholds(),
        which in turn triggers _set_node_counts().

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
        
        Referring to our example tree from the PBTreeCombinatorics class
        documentation yet again, the bounds are as follows:

        If _r = 0, 0 ≤ ii ≤ 0 (iow ii == 0)
        If _r = 1, 1 ≤ ii ≤ 3
        If _r = 2, 4 ≤ ii ≤ 9
        If _r = 3, 10 ≤ ii ≤ 21

        """
        self._set_thresholds()
            # Must set thresholds first
        if isinstance(self._r, int):
            if self._r <= 0:
                self._ii_start = 1
                self._ii_max = 1
            else:
                self._ii_start = self._thresholds[self._r-1]
                self._ii_max = self._thresholds[self._r]
        else:
            i_last_threshold = len(self._thresholds) - 1
            self._ii_max = self._thresholds[i_last_threshold]
            self._ii_start = 1

    def __init__(self, func, func_len_siblings, seq, r=None):
        """Creates a PBTreeCombinatorics sequence.

        Please refer to the subclasses CatCombination, Permutation and 
        PermutationWithRepeats in order to make use of this class.
        If you are implementing your own subclass, read on to the next
        section.
    
        Required Parameters for Subclasses of PBTreeCombinatorics
        ---------------------------------------------------------
        func - The function to derive the subset or term in the sequence.
            The function must have only one argument (excluding self
            when a method is used), which accepts the external index of
            the term to be derived.

        func_len_siblings - The function to measure the number of nodes
            on the tree with a common parent. All nodes on the same level
            are assumed to have the same number of parent nodes.
            This function must have only one argument (excluding self
            when a method is used), which is the value on the tree to
            calculate the the sibling count for.

        seq - The source sequence to run combinatorics operations on.
            Accepts any sequence types, including Python iterators and 
            sequences.

        Optional Arguments
        ------------------
        r - The r-value of the combinatorics operations to be run by
            the combinatorics class. This is intended to refer to the 
            length or size of the output of the terms derived.
            If r is not specified, the PBTreeCombinatorics steps through
            every node, returning results for every possible value of r.

        """
        self._func_len_siblings = func_len_siblings
            # Function to find the number of nodes with a common parent
            #  on a given level. This function should take one argument
            #  (excluding self, if a method is used instead), and return
            #  and int representing the number of sibling nodes.
        self._node_counts = []
        self._thresholds = []
        super().__init__(func, seq, r, ii_start=0)
 

class CatCombination(PBTreeCombinatorics):
    """Addressable Concatenating Combinator

    A sequence of all possible combinations of items from multiple
    position-dependent sequences, where items from the first sequence
    only appears on the first element of the combination, and items 
    from the second appear second, and so on...

    Uses PBTreeCombinatorics to generate its combinations.
    
    Note: It is possible to make the CatCombination class function like
    a permutator, but position-dependent combinations are the main
    intended use of this class, hence its name.

    Example
    -------
    In a hypothetical English language lesson we have four lists:

    Pronoun  Verb     Determiner  Noun
    =======  =======  ==========  ====
    You      kicked   my          dog
    She      punted               anaconda
    He
    It

    The CatCombinator will generate all possible Pronoun-Verb-Determiner-
    Noun combinations:

    r=1    r=2           r=3              r=4
    ===    ==========    =============    ======================
    You    You kicked    You kicked my    You kicked my dog
    She    You punted    You punted my    You kicked my anaconda
    He     She kicked    She kicked my    You punted my dog
    It     She punted    She punted my    You punted my anaconda
           He kicked     He kicked my     She kicked my dog
           He punted     He punted my     She kicked my anaconda
           It kicked     It kicked my     She punted my dog
           It punted     It punted my     She punted my anaconda
                                          He kicked my dog
                                          He kicked my anaconda
                                          He punted my dog
                                          He punted my anaconda
                                          It kicked my dog
                                          It kicked my anaconda


    The resulting combinatorics tree can be visualised as:

    ::
    
       d. a. d. a. d. a. d. a.  d. a. d. a. d. a. d. a.
        \_/   \_/   \_/   \_/   \_/   \_/    \_/   \_/
         \     \     |     |     |     |     /     /
          my    my   my    my   my    my   my    my
           |    |    |     |    |     |    |     | 
           k.   p.   k.    p.   k.    p.   k.    p.
            \___/     \___/      \___/      \___/
              |         |          |          |
              You       She        He        It
               \_________\________/__________/
                             |
                             0
    
        legend: k.-'kicked', p.-'punted', d.-'dog', a.-'anaconda'

    The combinations are ordered as they appear on the tree from
    left to right. The algorithm used to determine the node counts is
    described in the _set_node_counts() method in this class.

    """
    def add_sequence(self, seq, t=1):
        """Add another sequence to the sequence of source sequences
        
        Arguments
        ---------
        seq - Source sequence. Accepts any Python sequence (a.k.a.
            finite collection of items with integer-addressable
            indices)
            
        t - Number of times to repeat the sequence. Accepts int,
            t ≥ 1

        """
        temp = list(self._seq_src)
        temp.extend([seq]*t)
        self._seq_src = tuple(temp)
        self._set_ii_bounds()

    def index(self, x):
        """
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        x - The term to be searched for. Accepts any Python iterator type.

        """
        self._prescreen_index_search_term(x)
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
        """Attempt to rebuild a probable equivalent of the arguments
        used in initialising a CatCombination sequence
        """
        seq_shown = self._seq_src[1:]
            # Strip leading None from the outer sequence
        re_arg_fmt = "seq={0}, r={1}"
        return re_arg_fmt.format(seq_shown, self._r)

    def _get_comb(self, ii):
        """Returns the first+i'th subset or term of a Catenation
        Combination sequence

        Arguments
        ---------
        ii - Internal Index of the term. Accepts int, 0 ≤ i < _ii_max

        Treatment of Addresses
        ----------------------
        Each element in the addresses tuple returned by _get_comb_tree_path
        refers to an item on one of the lists attached to the combinator:
        The i'th element of the list references an item on the i'th
        sequence.

        Example
        =======
        Referring to our example in the documentation for this class,
        let's recreate the combinator, and configure it to return the 
        full four-word sentences as terms:

        >>> from slowcomb.slowcomb import CatCombination
        >>> s_a = ('You','He','She','It')
        >>> s_b = ('kicked','punted')
        >>> s_c = ('my',) #  Remember the comma after a lone element 
        >>> s_d = ('dog','cat','anaconda')
        >>> seqs = (s_a, s_b, s_c, s_d)
        >>> comb = CatCombination(seqs,r=4)

        Note that the root node is already included in the sequence source.

        We find that there are twenty-four different sentences we can
        get from this combinator.

        >>> len(comb)
        24

        Let's try to get the address of the 13th combination.

        Remember that the PBTreeCombinator's address generation takes
        internal indices, so let's resolve our external index to an
        internal one:

        >>> ii = comb._resolve_i(14)

        Now, get the combinatorics tree path with the resolved internal
        index:

        >>> comb._get_comb_tree_path(ii)
        (0, 2, 0, 0, 2)

        That's the route from the root node to the thirteenth node on
        Level 4. The leftmost element represents Level 0, and the rightmost
        represents the topmost Level. Also, Level 0 references the first
        source sequence, each successive Level on the tree references
        a corresponding sequence. The CatCombinator does not output
        the empty subset represented by the root node in Level 0 under
        normal operation.
        
        Having known that, let's resolve it to a concrete term:
        
        Sequence 0 -> can be safely ignored, no output
        Sequence 1 -> get element 2 -> 'She'
        Seqeunce 2 -> get element 0 -> 'kicked'
        Sequence 3 -> get element 0 -> 'my'
        Sequence 4 -> get element 2 -> 'anaconda'

        Let's confirm our findings:
        
        >>> comb[14]
        ('She', 'kicked', 'my', 'anaconda')

        Well done! You have resolved a CatCombinator tree path!

        """
        addrs = self._get_comb_tree_path(ii)
        out = []
        for i in range(len(addrs)):
            out_data = self._seq_src[i][addrs[i]]
            if out_data is not None:
                out.append(out_data)
        return(tuple(out))
    
    def _set_node_counts(self):
        """Sets up the node count embedded sequence, _node_counts to
        enable the combinatorics tree's addressing method to function.
        
        Node Counts for PBTreeCombinatorics
        -----------------------------------
        * Level 0 always has 1 node, the root node.
        * The number of nodes for any Level thereafter is the node count
        of the previous Level multiplied by the number of items in the
        current level.

        Example
        =======
        Referring to our example in the documentation for the 
        CatCombination class, a combinator set up with the following
        sequences:
        
        I : ('You','She','He','It')
        II : ('kicked','punted')
        III : ('my')
        IV : ('dog','cat')

        Will have a node count of:
        
        * 1 for Level 0 (representing the root node)
        * 4*1 == 4 for Level 1
        * 2*4 == 8 for Level 2
        * 1*8 == 8 for Level 3
        * 2*8 == 16 for Level 4

        Thus, _node_counts will therefore be equivalent to (1,4,8,8,16).

        """
        func_node_counts = lambda i : len(self._seq_src[i])
        func_product_seq = lambda i,a : i*a
            # This basically makes the AccumulateSequence 
            #  a product sequence.
        self._node_counts = AccumulateSequence(func_node_counts,
            func_product_seq, length=len(self._seq_src))
        self._node_counts.enable_cache()
    
    def __init__(self, seqs, r=None):
        """Create a Catenating Combinator Sequence
        
        Arguments
        ---------
        seqs - Sequence source to derive combinations from. Accepts a 
            sequence of sub-sequences.

        Optional Arguments
        ==================
        r - The length of the terms derived from the combinator. On the
            CatCombinator, setting r smaller than the number of 
            sub-sequences in seqs causes it to use only the first r
            sub-sequences. Accepts int, 0 ≤ r < len(seqs).

        Examples
        --------
        To re-create the combinator in the documentation for the 
        CatCombinator class:

        First, prepare the source sequences. The CatCombintion accepts
        a 'sequence of sequences' as the source. This can be done the
        readable way:

        >>> from slowcomb.slowcomb import CatCombination
        >>> s_a = ('You','She','He','It')
        >>> s_b = ('kicked','punted')
        >>> s_c = ('my',) #  Remember comma after a lone element 
        >>> s_d = ('dog','anaconda')
        >>> seqs = (s_a, s_b, s_c, s_d)

        Or the hardcore, one-liner way:

        >>> seqs = ( ('You','She','He','It'),('kicked','punted'), ('my',),
        ... ('dog','anaconda') )

        Create the combinator as such, set r to four to generate full
        sentences:

        >>> comb = CatCombination(seqs,r=4)
        >>> comb[7]
        ('She', 'punted', 'my', 'anaconda')

        >>> comb[12]
        ('It', 'kicked', 'my', 'dog')

        To output only the first three words, reduce the r-value to 3:
        >>> comb = CatCombination(seqs, r=3)
        >>> comb[0]
        ('You', 'kicked', 'my')

        >>> comb [6]  # The space was placed on purpose
        ('It', 'kicked', 'my')

        Likewise for even shorter output:
        >>> comb = CatCombination(seqs, r=2)
        >>> comb[4]
        ('He', 'kicked')

        >>> comb = CatCombination(seqs, r=1)
        >>> len(comb)
        4

        >>> comb[0]
        ('You',)

        A CatCombination whose r=0 only returns empty tuples. 
        This is in aligment with the behaviour of the ``combinations`` class
        from Python's itertools.

        >>> comb = CatCombination(seqs, r=0)
        >>> len(comb)
        1

        >>> comb[0]
        ()

        Fun activity: what output does a CatCombinator with r=None produce?

        >>> seqs = ( ('You','She','He','It'),('kicked','punted'), ('my',),
        ... ('dog','anaconda') )
        >>> comb_myst = CatCombination(seqs,r=None)

        """
        # Construction Routine
        seq_init = [ (None,) ] # Place the root node
        seq_init.extend(seqs)
        seq_src = tuple(seq_init)

        self._func_len_siblings = lambda lvl : len(self._seq_src[lvl])
        super().__init__(self._get_comb,self._func_len_siblings,seq_src, r)


class Permutation(PBTreeCombinatorics):
    """Addressable Permutator

    A sequence of all possible re-arranged versions a source sequence,
    or all possible arrangements of a subset of the source sequence given
    a specific subset length.

    Uses PBTreeCombinatorics to generate its combinations.

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
    def index(self, x):
        """
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        x - The term to be searched for. Accepts any Python iterator type.

        """
        self._prescreen_index_search_term(x)
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
            0 ≤ i < self._ii_max

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
        as per PBTreeCombinatorics conventions. This corresponds to the 
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
    
    Uses PBTreeCombinatorics to generate its combinations.

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
    def index(self, x):
        """
        Return the first index of a term, if it is a member of this 
        combinatorial sequence.

        Arguments
        ---------
        x - The term to be searched for. Accepts any Python iterator type.

        """
        self._prescreen_index_search_term(x)
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
            0 ≤ i < self._ii_max

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


class Combination(Combinatorics):
    """Addressable Combination Sequence
    
    An addressable sequence of all possible selections from a source
    sequence. Multiple permutations of the same selections are regarded
    as the same selection.
    
    This class is an addressable analogue to the combination class
    from Python's itertools.

    """
    def _set_ii_bounds(self):
        """Sets appropriate limits for the internal index, so that it
        may report the length of the sequence correctly.

        """
        self._set_bitmap_src()
        self._ii_max = len(self._bitmap_src)

    def _get_comb(self, ii):
        """
        Return the first+ii'th term of the Combination sequence.

        Arguments
        ---------
        ii - The internal index of the term. Accepts int,
        0 ≤ ii ≤ _ii_max.

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
    def _get_comb(self, ii):
        """
        Return the first+ii'th term of the Repeats-Permitted
        Combination sequence.

        Arguments
        ---------
        ii - The internal index of the term. Accepts int,
        0 ≤ ii ≤ _ii_max.

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

