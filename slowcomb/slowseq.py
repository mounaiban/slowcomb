"""
slowseq — Slow Combinatorics supporting sequence classes
and more.
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

from math import factorial, floor

# Functions
# 
def lambda_int_npr(n):
    """
    Return an nPr lambda function, with a fixed n, that returns results
    as integers.

    The nPr function determines the number of outcomes for a partial
    permutation, when taking r items from a set of n items, and taking
    each item exactly once. It is usually written like:

        n! / (n-r)!
    
    Where ! means factorial, the product of an integer and all smaller
    positive integers.

    """
    return lambda r: int(factorial(n)/factorial(n-r))

def lambda_int_ncr(n):
    """Return an nCr lambda function, with a fixed value for n, that
    returns results as integers.
    """

    # TODO: Remove this function if found to be unneeded in future
    # versions
    return lambda r: int(factorial(n)/( factorial(r)*factorial(n-r) ))

def int_ncr(n,r):
    """
    Evaluate nCr, the number of possible combinations given r selections
    from a set of n members.

    The nCr function is commonly written as:

      n! / ( r! * (n-r)! )

    Where ! means factorial, the product of an integer and all smaller
    positive integers.
    
    Arguments
    ---------
    n - Number of items in the set. Accepts int.
    r - Number of selections from the set. Accepts int.
    """

    return int(factorial(n)/( factorial(r)*factorial(n-r) ))

# Classes
#
class NumberSequence:
    """Addressable finite number sequence.

    A class for a numeric sequence with a finite number of terms,
    which supports slicing in order to directly address members of the 
    sequence. This class may also be used as an iterator.

    For further instructions on its use, see __init__() and
    __getitem__() below.
    """

    # Private Methods
    # 
    def _check_i(self, i):
        """Checks if an external index is out of bounds.
        
        Raise an IndexError if the external index requested is deemed
        to be out of range.

        Arguments:
        i - External index, as requested by square-bracket addressing
        """

        len_self = len(self)
        if i >= len_self or i < -len_self:
            raise IndexError('Sequence index out of bounds')
    
    def _clamp_i(self, i, i_min, i_max):
        """Limits a value to a set range.

        If a value i is found to exceed a nominated maximum, the
        maximum is returned. Likewise, if i is lower than a minimum
        value, the minimum value is returned.

        Arguments:
        i - the value to be checked
        i_min - minimum value to be returned
        i_max - maximum value which may be returned

        All arguments may be of any type which supports comparisons by
        the less than (<) and greater than (>) operators.
        """
        if i >= i_max:
            return i_max
        elif i <= i_min:
            return i_min
        else:
            return i

    def _get_member(self, i):
        """Routine to return the first+n'th member of the sequence

        Arguments:
        i - External index of the member
        """

        self._check_i(i)
        return self._func(self._resolve_i(i))

    def _get_members(self, s):
        """Routine to return multiple members in response to a slice
        
        Arguments:
        s - External start, stop and step indices in a Python ``slice``
        """ 

        out = []
        s = self._resolve_slice(s)
        for ii in range(s.start, s.stop, s.step):
            out.append(self._func(ii))
        return tuple(out)

    def _resolve_i(self, i):
        """Remaps external indices to internal indices, and supports
        the use of negative indices.

        This dual index system in use by NumberSequence is intended to
        reconcile the nature of numerical sequences, which may not 
        begin at zero or one, with the nature of Python's data sequences,
        which always begin at index zero for the first item and end at
        the number of items in the sequence. For further information,
        refer to the usage notes in __init__().

        Arguments:
        i - External index, as requested by square-bracket addressing
        """

        if i < 0:
            return self._ii_max + i
            # PROTIP: Add with a negative to subtract from
            #  its magnitude
        else:
            return self._ii_start + i

    def _resolve_slice(self, s):
        """
        Resolves a slice of external indices to a slice of internal
        indices.

        Arguments:
        s - External indices, as requested by a Python ``slice``

        """

        len_self = len(self)
        stop = self._clamp_i(s.stop, -len_self+1, len_self)
        stop_res = self._resolve_i(stop)
        start = 0
        step = 1
        if s.start is not None:
            start = self._clamp_i(s.start, -len_self+1, len_self-1)
            start_res = self._resolve_i(start)
        if s.step is not None:
            step = s.step
        return slice(start_res, stop_res, step)

    def _set_ii_bounds(self):
        """Sets the upper limit of the internal index.

        Always returns None.
        """
        self._ii_max = self._ii_start + self._len
        

    # Special Methods and Constructor
    #
    def __getitem__(self, key):
        """Supports addressing of single or multiple individual terms
        of a NumberSequence using Python's square-bracket notation.

        As with Python's built-in sequence types, both integer and 
        slice addressing may be used. Negative indices to address terms
        from the farthest end of the sequence are also supported.

        As with Python's sequences, Indices address the _first+n'th_
        sequence, and thus begin at zero. The zero'th index therefore
        references the first term of the sequence.
        
        Returns numeric types for single terms, and tuples for multiple
        terms.

        Examples:
        ---------
        Given a NumberSequence of powers of two from 0 to 10:

        >>> from slowcomb.slowseq import NumberSequence
        >>> func_pow2 = lambda x:2**x
        >>> seq_pow2 = NumberSequence(func_pow2,length=11)

        Please remember that there are eleven terms from i=0 to ii=10
        inclusive. By default, sequences start from zero.

        Single Term Addressing
        ======================
        The 10th term of the sequence, 2**10, can be addressed as such:

        >>> seq_pow2[10]
        1024

        Slicing
        =======
        Get all terms from the 2nd to 5th inclusive of the sequence 
        like this:

        >>> seq_pow2[2:6] 
        (4, 8, 16, 32)

        You can also get all even powers of two from the sequence:

        >>> seq_pow2[2:11:2]
        (4, 16, 64, 256, 1024)

        Or get multiple terms in reverse order with negative step values:
        
        >>> seq_pow2[5:1:-1]
        (32, 16, 8, 4)
        
        Recall that by Python slicing conventions: 2nd to 5th must be
        written as '2nd to before the 6th', while reverse order slices
        such as 5th to 2nd must be written as '5th to after the 1st'.

        Negative Addressing
        ===================
        Negative addressing to get a term by its position from the farthest
        end, as seen with Python's own sequences, are also supported:

        Get the first item from the farthest end:

        >>> seq_pow2[-1]
        1024

        Or the second from the farthest end:

        >>> seq_pow2[-2]
        512

        And so on...

        Mixed Slicing
        =============
        Feel free to mix negative and positive indices and steps!

        To get the second to second-last (9th) term in reverse order:

        >>> seq_pow2[-2:1:-2]
        (512, 128, 32, 8)

        To get the first to the fifth term in reverse order:

        >>> seq_pow2[5:0:-1]
        (32, 16, 8, 4, 2)

        Sorry, due to limitations, it is not possible to include the
        zeroth term of a sequence in a slice when a negative step value
        is used.
        """

        if isinstance(key, int) is True:
            return self._get_member_method(key)
        elif isinstance(key, slice) is True:
            return self._get_multi_member_method(key)
        else:
            raise TypeError('indices must be int or slice')


    def __iter__(self):
        """Special method just to enable use as an iterator.
        
        Example
        -------
        This iterator yields all values for the sequence containing
        all squares from 1 to 10:

        >>> from slowcomb.slowseq import NumberSequence
        >>> seq_sq = NumberSequence(lambda x:x**2, length=10, ii_start=1)
        
        You can print all the terms from 1 to 10 like this:

        >>> for i in seq_sq:
        ...     print(i,end=',')
        1,4,9,16,25,36,49,64,81,100,

        """
        return self


    def __len__(self):
        """Returns the number of terms available in a NumberSequence"""

        # NOTE: This works also when _ii_start is negative
        return self._len

    def __next__(self):
        """Supports the use of this class as an iterator.
        See __iter___().
        """
        if (self._ii_max is None) or (self._i >= len(self)):
            raise StopIteration
        out = self[self._i]
        self._i += 1
        return out

    def __repr__(self):
        """Reserved method for the Reporting Tools, which may be
        implemented when Moses feels like it.
        """
        pass
        # TODO: Implement Slowcomb Reporting Tools

    def __init__(self, func, length, **kwargs):
        """Method to create a NumberSequence instance
        
        Options for creating a NumberSequence
        -------------------------------------

        Arguments
        =========
        func - The function to derive a term of the sequence. Accepts
            'full-bodied' functions or lambdas.

            * If the function is defined outside a class or inside
            a method then it must only have one argument for the 
            internal index of the term. For more info on internal
            and external indices, see NumberSequence.__init__().

            * If the function is defined inside a class, it is 
            classified as a method by Python conventions, and must
            have two arguments, one for ``self`` and another for
            the index of the term.

        n - The number of terms in the sequence. Accepts int.

        Optional Arguments
        ==================
        ii_start - The first position of the internal index. For 
            more information about them, please see the section
            on Internal Indices below. Accepts int.

        default - The default value or object returned in the event the
            sequence has a zero length, or is unable to otherwise derive
            a term from a valid index. May be of any class.

        Examples
        --------

        Trivial Example: Power of Two Sequence
        ======================================
        This sequence has 101 terms, and thus contains all powers
        of two from zero to 100.
        >>> from slowcomb.slowseq import NumberSequence
        >>> seq_pow2 = NumberSequence(lambda x:2**x,101)

        Get the result of 2**0

        >>> seq_pow2[0]
        1

        Get the result of 2*100
        
        >>> seq_pow2[100]
        1267650600228229401496703205376

        Slightly More Complex Example: Warm and Cool Colours
        ====================================================
        This sequence has 100 terms, and alternates between opposite
        HSV hues, stepping around the hue circle in increments of
        one percent.

        Also, Python does American spelling, but I don't :P

        >>> import colorsys  
        >>> from slowcomb.slowseq import NumberSequence
        >>> def get_hue(i):
        ...     # Step between warm and cool colours
        ...     # In Python HSV, H values start from 0.0
        ...     # representing red, then to 1/3 representing
        ...     # green, then to 2/3 representing blue, then
        ...     # back to red at 1.0.
        ...     hue = 0
        ...     if i%2==0 :
        ...         hue += (0.01*i)%1
        ...     else:
        ...         hue += (0.5 + 0.01*i)%1
        ...     rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.75)
        ...     # Convert relative values to 8-bit hex absolute values
        ...     rgb_hex = ['{0:02X}'.format(int(255*i)) for i in rgb]
        ...     # Convert RGB 8-bit hexadecimal to W3C 24-bit spec
        ...     out = '#'
        ...     for i in rgb_hex:
        ...         out+=i
        ...     return out
        >>> seq_hue = NumberSequence(get_hue,100)

        Get the first colour (a passionate red)!
        All colours are in W3C 24-bit format, seen in HTML, CSS, SVG...

        >>> seq_hue[0]
        '#BF0000'
        
        Get the second (first+1'th) colour (a calming aqua)!

        >>> seq_hue[1]
        '#00B3BF'

        Get the 34th colour (an alluring violet)!
        
        >>> seq_hue[33]
        '#BB00BF'

        Get the 66th colour (some olive oil-like colour)!
        
        >>> seq_hue[67]
        '#BBBF00'

        Fun Activity: Guess what these colours are:

        >>> seq_hue[80]
        '#9900BF'

        >>> seq_hue[83]
        '#03BF00'

        >>> seq_hue[90]
        '#BF0072'


        Internal Indices
        ----------------
        Internal Indices are an important part of the NumericSequence
        class, which is intended to map suitable mathematical numeric
        sequences into a class which resemble Python's data sequences,
        allowing numerical sequences to be used like tuples, lists,
        arrays and the like.

        External Indices are the values given to a NumericSequence
        to retrieve the first+n'th term from a sequence. These are mapped
        to Internal Indices (ii's), the actual key of the term in the
        sequence, by the method `_resolve_i()`.

        An Example of Internal Indices
        ==============================
        Consider the following sequence:
        
        All values of y in

            y = -(x/40)**2 + 100 

        where -40 ≤ x ≤ 40 and x is an integer.

        This sequence is based on a problem in which one is to find all
        values of x in a quadratic equation that would yield a positive
        integer value as a result. It can be visualised on a 2D graph
        as a selection of the x-axis (representing values of x) where 
        the curve (representing values of y) are above the x-axis.

        Our equation here may be expressed as a Python lambda like:

        >>> func_funk = lambda x: -(x/4)**2 + 100

        Luckily for us, the values of x are integers, and thus may be
        directly used as indices for values of y. However, let's 
        assume in our situation that only positive integers can be used
        as indices, as they have to be addressed ordinally (i.e. 1st for
        x=-40, 2nd for x=-39...), and we are not allowed to rewrite our
        equation.

        We can use a NumberSequence to express this:

        >>> from slowcomb.slowseq import NumberSequence
        >>> seq_quadr = NumberSequence(func_funk, ii_start=-40, length=81)

        This sequence will have 81 terms, yielded by indices -40 to 40
        inclusive, not forgetting about the zero. The first term may
        be returned by accessing the zeroth (short for "first+zeroth")
        index:

        >>> seq_quadr[0]
        0.0

        This first term in turn will reference internal index -40, as
        indicated by the ``ii_start=-40`` argument in the original
        statement to create the NumberSequence.

        Each time we use index 0 on the NumberSequence, it will map it
        to index -40 internally and fetch the corresponding value of y.

        Likewise, we can find the median y-value, which is the 40th value,
        with:

        >>> seq_quadr[40]
        100.0

        This 40th "external" index was mapped to the internal index 0
        corresponding to x=0 of our quadratic equation.

        The index at the other end of the sequence can be referenced
        by the last external index:

        >>> seq_quadr[80]
        0.0

        Try other indices, like:

        >>> seq_quadr[20]
        75.0

        >>> seq_quadr[60]
        75.0

        >>> seq_quadr[10]
        43.75

        >>> seq_quadr[70]
        43.75

        Fun Activity: Think of some other equations worthy of being used 
        as a basis for a NumberSequence, preferably one involving both
        negative and positive input values.
        """

        # Instance Attributes
        #
        self._default = kwargs.get('default', None)
            # The default value returned if the member cannot be derived
        self._func = func
            # The function to get the value of a term in a sequence.
        self._get_member_method = self._get_member
            # Intermediate method to call _func.
            #  May be swapped out with an alternate method to enable 
            #  caching, or alternative lookup methods.
        self._get_multi_member_method = self._get_members
            # Intermediate method to call _func for multiple terms,
            #  and return them in an appropriate data type.
            #  May be swapped out with an alternate method to enable 
            #  caching, or alternative lookup methods.
        self._ii_start = int(kwargs.get('ii_start', 0))
            # First internal index. May be referred to as the ii 
            #  start offset.
        self._i = 0
            # Index when used as iterator.
        self._ii_max = 0
            # Last internal index.
        self._len = int(length)
            # Expected number of external addresses including the zeroth
            #  index
        self._name = ''
            # TODO: Reserved attribute for reporting tools

        # Init Routine
        #
        if self._len < 0:
            raise ValueError('sequence length must be zero or more')
        self._set_ii_bounds()


class CacheableSequence(NumberSequence):
    """Cacheable alternative to NumberSequence using a dictionary cache.

    The CacheableSequence is intended as an alternative class for 
    number sequences whose members may take a long time to derive. The
    dictionary cache remembers every member lookup in its dictionary
    until it is cleared.

    How to Use It
    -------------
    The CacheableSequence is used exactly like a NumberSequence. Caching
    is automatic and performed during every time a member that is not 
    previously cached is derived (this includes multi-lookups by slicing).

    The cache is disbled by default.
    
    Call enable_cache() to start caching members.
    Call disable_cache() to disable the cache. This also clears the cache.
    Call clear_cache to clear the cache without disabling it.

    When to Use It
    --------------
    Speed advantages are achieveable if the time taken to derive the
    terms is significantly longer than entering an exception block
    and performing a Python ``dict`` lookup.
    
    The method of caching used herein is recommended for scenarios
    where the same terms from the sequence will be looked up very
    frequently, but the terms are not part of a contiguous block,
    and are subject to infrequent, random change during the course of
    a program running.

    When Not to Use It
    ------------------
    As with many conventional methods of caching, scenarios with 
    random lookups within a wide range are likely to cause excessive
    memory usage while greatly reducing any speed advantage, especially
    with sequences with a large number of terms.
    How It Works
    ------------
    Please see _get_member_with_cache() and _add_member_to_cache() below.
    """
    # Public Methods
    #
    def disable_cache(self):
        """Disable the dictionary cache.
        
        The CacheableSequence will function like a normal sequence
        until the enable_cache() method is called. Disabling the cache
        also clears it.
        """
        self._cache = None
        self._get_member_method = self._get_member
        self._cache_method = self._skip_caching

    def enable_cache(self):
        """Set up and enable the dictionary cache."""
        self._cache = {} 
        self._get_member_method = self._get_member_with_cache
        self._cache_multi_method = self._add_member_to_cache
    
    # Private Methods
    #
    def clear_cache(self):
        """Removes all saved results from cache to free up memory"""
        self._cache.clear()

    def _add_member_to_cache(self, data, i, **kwargs):
        """Save an item into the dictionary cache.

        Arguments
        ---------
        data - result of the member lookup to save to cache.
            Accepts any object, even None.
        i - index to recall a data item with. Accepts int, i ≥ 0

        The **kwargs argument is for compatibility purposes, to
        allow for implementions of new features in the
        CacheableSequence.
        
        This method always returns None.
        """
        if self._cache is None:
            # TODO: Is an AttributeError appropriate here?
            raise AttributeError('Cache not enabled')
        if isinstance(i,int) is True:
            if i < 0:
                raise ValueError('i must be ≥ 0')
            self._cache[i] = data
        else:
            raise TypeError('Only int may be used as cache dict key')
    
    def _get_member_with_cache(self, i):
        """Return the first+i'th member of the sequence from the
        dictionary cache.

        If the member cannot be found in the cache, the full routine
        to get the member will be run. The member will then be
        saved to the cache for subsequent requests of the same
        member.

        Arguments
        ---------
        i - The index of the member of the sequence. Accepts int, i ≥ 0.
        
        """
        cache_enabled = self._cache is not None
        try:
            return self._cache[i]
        except KeyError:
            # On cache miss, fallback to normal path...
            out = self._get_member(i)
            # And save the result
            self._add_member_to_cache(out, i)
            return out

    def _skip_caching(self, data, **kwargs):
        """Dummy method to skip the caching process
        
        In order to avoid excessive checks, the CacheableSequence will
        always run the caching method for every member lookup. When the
        cache is disabled, this dummy method is run in place of the
        usual cache check.

        This method, along with the use of switchable methods was used
        in anticipation that some caching schemes would involve an
        expensive operation to check if the cache is in use.

        Please see disable_cache() method above and the design of the
        NumberSequence class (which the CacheableSequence derives from)
        for specific details on how this method is switched in.
        """
        pass

    # Special Methods and Constructor
    # 
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self._cache = None
        self._cache_method = self._skip_caching

class BlockCacheableSequence(CacheableSequence):
    """Cacheable alternative to NumberSequence using a block cache.

    The BlockCacheableSequence is intended as an alternative class for 
    number sequences whose members may take a long time to derive.
    This sequence remembers members that fall within a contiguous block,
    which by definition includes both adjacent members (e.g. [2],[3],[4]
    [5]), or members with a constant step between them (e.g. '[1],[4],[7],
    [10]...'). The cache is a implemented as a list.
    
    How To Use It
    -------------
    The BlockCacheableSequence is used exactly like a normal NumberSequence.
    Members are only cached when they are looked or derived up as part
    of a multiple-item operation using slices.

    The cache is disbled by default.
    
    Call enable_cache() to enable the cache.
    Call disable_cache() to disable the cache. This also clears the cache.
    There is no separate method to clear the cache. Instead, perform a 
    dummy lookup with a zero-length slice (e.g. [0:0]) to force caching of
    a negligbly small slice.

    When To Use It
    --------------
    Sequences with frequent lookups exclusively within a small, contiguous
    range of indices, or consistently equidistant lookups within any range,
    will benefit most from this cache. In compsci parlance, this would be
    described as a read pattern with _strong spatial or strong equidistant
    locality_*.

    *Wikipedia. Locality of Reference.
    en.wikipedia.org/wiki/Locality_of_reference

    When Not To Use It
    ------------------
    The BlockCacheableSequence is not able to provide any performance benefit
    to sequences that frequently service lookups within a wide range of
    non-equidistant indices.
    
    How It Works
    ------------
    For more information, see __init__(), __getitem__() and
    _add_members_to_cache() below.
    """

    def disable_cache(self):
        """Disable the block cache and clear it"""
        self._cache = None
        self._get_member_method = self._get_member
        self._cache_method = self._skip_caching

    def enable_cache(self):
        """Set up the block cache"""
        self._cache = []
        self._cache_start_i = 0
        self._cache_step_i = 1
        self._cache_stop_i = 0
        self._get_member_method = self._get_member_with_cache
        self._cache_method = self._add_members_to_cache

    def _add_members_to_cache(self, data, **kwargs):
        """Save looked up members to the BlockCacheableSequence.

        This is a simple operation in which the results of a multi-lookup
        are kept in cache, along with the details of the that was used for
        the lookup. This operation also deletes all existing content in
        the cache.

        The cache will be effective for any member that was part of 
        a cached multi-item lookup using a slice.

        Examples
        --------
        seq[1:11] -> all members 1 thru 10 are cached
        seq[0:21:2] -> all even members 0 thru 20 are cached
        seq[20:0:-1] -> all members 0 thru 20 are cached, albeit in
            reverse order. This does not affect operation of the cache.

        The sequence ``seq`` in the following examples has a length of 101
        (with indices 0 to 100):
        
        seq[-1:-51:-1] -> the last fifty members are cached
        seq[-2:-51:-2] -> the last fifty odd members are cached
        """
        self._cache_start_i = kwargs.get('start',0)
        self._cache_step_i = kwargs.get('step',1)
        self._cache_stop_i = kwargs.get('stop',0)
        self._cache = data

    def _get_members(self, s):
        """Routine to return multiple members in response to a slice
        
        Arguments:
        s - External start, stop and step indices in a Python ``slice``
        """ 
        out = []
        s = self._resolve_slice(s)
        for ii in range(s.start, s.stop, s.step):
            out.append(self._func(ii))
        self._add_members_to_cache(out,
            start=s.start, stop=s.stop, step=s.step)
        return tuple(out)

    def _get_member_with_cache(self, i):
        """Get the first+i'th member of the sequence from the cache.

        In the event that the member cannot be found in the cache (cache
        miss), the method will resort to looking up the member without
        the cache. The cache is effective for any member that was part
        of a cached multi-item lookup using a slice.

        For more information on how this cache works, see
        _add_members_to_cache().
        """
        out = None
        if self._cache is None:
            self.enable_cache()
        in_range = (i >= self._cache_start_i) and (i < self._cache_stop_i)
        on_step_single = (i % self._cache_step_i) == 0
            # Should only be true when cache_step_i is 1
        on_step_multi = (i % self._cache_step_i) == 1
            # Remainder of i and step should be one if i is
            # on the step of the sequence
        if in_range and (on_step_single or on_step_multi):
            cache_i = (i - self._cache_start_i) // self._cache_step_i
            out = self._cache[cache_i]
        if out is None:
            # On cache miss, fallback to normal path
            out = self._get_member(i)
        return out

    def __init__(self, func, **kwargs):
        self._cache = None
        self._cache_start_i = 0 
            # Index of first member to be cached
        self._cache_step_i = 1
            # Distance between cached members
        self._cache_stop_i = 0
            # Index of last member to be cached
        super().__init__(func, **kwargs)


class SNOBSequence(NumberSequence):
    """Same Number Of Bits Number Sequence Class

    This class is a NumberSequence that address all possible binary
    numbers of a given length and a set number of bits.

    Numbers are arranged from the largest to the smallest, with the
    first+zero'th index returning the largest number.

    The SNOBSequence only returns int's.

    Example Sequences
    -----------------
    A 4-bit number with 2 bits set:

    i  Binary  Decimal
    =  ======  =======
    1  1100    12
    2  1010    10
    3  1001    9
    4  0110    6
    5  0101    5
    6  0011    3

    A 6-bit number with 3 bits set:

    i  Binary  Decimal        i   Binary  Decimal
    =  ======  =======        ==  ======  =======
    0  111000  56             10  011100  28
    1  110100  52             11  011010  26
    2  110010  50             12  011001  25
    3  110001  49             13  010110  22
    4  101100  44             14  010101  21
    5  101010  42             15  010011  19
    6  101001  41             16  001110  14
    7  100110  38             17  001101  13
    8  100101  37             18  001011  11
    9  100011  35             19  000111  7

    For more usage information, see __init__() below for instructions on
    creating an instance of this class, and for generating the numbers.

    """
    def _get_leading_z_with_i(self, n, r, i):
        """Get the binary number of leading zeroes on the i'th number
        of length n, with r bits raised, along with the ordinality of
        the number among numbers with the same leading zeroes.

        Arguments
        ---------
        n-Total bits in the number. Accepts int. n > 0.
        r-Number of raised bits in the number. Accepts int, 0 < r ≤ n.
        i-The i'th number given n and r above. Accepts int, 0< r ≤ nCr(n,r)
            [where nCr(n,r) = n! / r! * (n-r)!]

        Output
        ------
        Returns a tuple t, where
        t[0] - The number of zeroes given any value of n, r and i above.
        t[1] - The ordinality/rank of the number among numbers with the
            same leading zeroes

        Examples
        --------
        Given a SNOBSequence as follows:
        >>> from slowcomb.slowcomb import SNOBSequence
        >>> snob_seq = SNOBSequence(1,1)

        Note that the n and r of the SNOBSequence is not relevant in
        these examples, and was done only to initialise the SNOBSequence
        just to be able to use this method.

        For all 6-bit numbers with 3 raised bits,

        The highest number has nil leading zeroes, and is the first
        such number:

        >>> snob_seq._get_leading_z_with_i(6,3,1)
        (0, 1)

        The 10th highest number also has nil leading zeroes, and is
        the tenth such number:
        
        >>> snob_seq._get_leading_z_with_i(6,3,10)
        (0, 10)

        The 11th number has one leading zero, and is the first
        such number: 

        >>> snob_seq._get_leading_z_with_i(6,3,11)
        (1, 1)

        The 12th number has one leading zero, and is the second
        such number:

        >>> snob_seq._get_leading_z_with_i(6,3,12)
        (1, 2)

        Moreover, the 17th number has two leading zeroes, and is the
        first such number:
        >>> snob_seq._get_leading_z_with_i(6,3,17)
        (2, 1)

        Finally, the 20th (also the smallest) number has three leading
        zeroes, and is the first and only such number:
        >>> snob_seq._get_leading_z_with_i(6,3,20)
        (3, 1)

        """
        i_temp = i
        n_temp = n-1
        r_temp = r-1 # NOTE: This stays the same
        zeroes = 0
        ncr_temp = int_ncr(n_temp,r_temp) # Initial nCr
        while(i_temp > ncr_temp):
            zeroes += 1
            n_temp -= 1
            i_temp -= ncr_temp
            ncr_temp = int_ncr(n_temp,r_temp)
        return (zeroes, i_temp)

    def _get_bits(self, ii):
        """Get the ii'th highest n-bit number with r raised bits.
        
        The n and r settings for the SNOBSequence are kept as the _n
        and _r attributes respectively.

        Argument
        --------
        ii - The i'th highest number. Accepts int, 0 < ii ≤ nCr(n,r)
            [where nCr(n,r) = n! / r! * (n-r)!]

        """
        if self._r > self._n:
            raise ValueError('n must be greater than r')
        out_bin = 0
        temp_i = ii
        temp_n = self._n
        temp_r = self._r

        # The current method works from the highest bit to the lowest,
        # using the nCr function to determine between adding a single 
        # raised bit or the correct number of zeroes.
        # This method is non-recursive and therefore stack-saving.
        #
        # Illustrated Explanation of the Algorithm
        # ----------------------------------------
        # 
        # Example A
        # =========
        # Say that we want to find the fourth highest 8-bit number with
        # three raised bits. Therefore n=8, r=3 and ii=4. Our number
        # thus far is unknown:
        # 
        # ????????
        #
        # First, we find out the number of leading zeroes. Using the
        # method defined in _get_leading_z_with_i(), which we will call
        # the Leading Z method, the fourth 8-bit number with three raised
        # bits has no leading zeroes, therefore we add a raised bit:
        # 
        # 1???????
        # 
        # As we have no leading zeroes we repeat the process on a number
        # with one less bit, one less raised bit and the same ordinality.
        # In other words, we look for the fourth highest 7-bit number with
        # two raised bits. Using the Leading Z, we get no leading zeroes.
        # 
        # 11??????
        #
        # Continuing with the process the fourth 6-bit number with one raised
        # bit, we find that, using the Leading Z, there are three leading
        # zeroes, so we add the three zeroes
        #
        # 11000???
        #
        # We also find that it is the first and only number with that
        # number of leading zeroes.
        #
        # This time, we continue with the process with the largest number
        # with three less (i.e. three) and the same number of raised bits
        # (i.e. one).
        # 
        # The Leading Z confirms that the largest binary number of any bit
        # size with one raised bit is the first, which always has no leading
        # zeroes, thus bringing our number to:
        #
        # 110001??
        # 
        # At this point, we have run out of bits to raise, so we fill the
        # rest of the number with zeroes.
        # 
        # 11000100
        #
        # Congratulations, we have successfully found our number!
        # This is the fourth-highest 8-bit number with 3 raised bits, better
        # known as 196 in decimal.
        #
        #
        # Example B
        # =========
        # Now let's try the same process on an 8-bit number with five raised
        # bits, looking for the 10th largest number.
        #
        # 10th largest 8-bit number with 5 raised bits has no leading zeroes
        # 
        # 1???????
        #
        # 10th largest 7-bit number with 4 raised bits has no leading zeroes
        #
        # 11??????
        #
        # 10th largest 6-bit number, 3 raised bits, no leading zeroes
        #
        # 111?????
        #
        # 10th largest 5-bit number, 2 raised bits, three leading zeroes.
        # This number is also the largest such number.
        #
        # 111000??
        # 
        # Largest 2-bit number with 2 raised bits, no zeroes at all.
        # Therefore, we will raise the remaining bits.
        #
        # 11100011 (dec: 227)
        # 
        # Well Done! We have found our number!
        #


        # Add the first and middle bits
        #  Start from the highest bit of the given number
        while (temp_n != temp_r) & (temp_r > 0):
            z = self._get_leading_z_with_i(temp_n, temp_r, temp_i)
            if z[0] > 0:
                # Add zeroes 
                out_bin <<= z[0]
                # Repeat this operation with the next raised bit
                #  after the run of zeroes
                temp_n -= z[0]
                temp_i = z[1] 
            else:
                # Add raised bit 
                out_bin <<= 1
                out_bin |= 1
                # Repeat this operation with the next bit
                temp_n -= 1
                temp_r -= 1

        # Add the final bits
        if temp_n == temp_r:
            # This happens with numbers with a single or several
            # contiguous raised bits at the lower end
            for b in range(temp_n):
                out_bin <<= 1
                out_bin |= 1
        else:
            for b in range(temp_n):
                out_bin <<= 1
        return out_bin

    def _set_ii_bounds(self):
        self._ii_max = int_ncr(self._n,self._r)+1

    def __len__(self):
        return self._ii_max - self._ii_start

    def __init__(self, n, r):
        """Method to create a SNOBSequence instance
    
	A SNOBSequence (Same Number Of Bits Sequence) is a NumberSequence
	of binary numbers of a fixed length (n) and set number of set 
	bits (r), ordered from largest to smallest.
    
        Arguments
	---------
	n - the total number of bits. Accepts int, n > 0
        s - the number of bits that are set. Accepts int, 0 < n ≤ r

        Examples
        --------
        >>> from slowcomb.slowseq import SNOBSequence
        >>> seq_snob42 = SNOBSequence(4,2)

        Let's look at the largest (first+zeroth) 4-bit number with two
        set bits:

        >>> seq_snob42[0]
        12
        >>> "{0:b}".format(seq_snob42[0])
        '1100'

        What about the second (first+first)-largest 4-bit number with two
        set bits?

        >>> seq_snob42[1]
        10
        >>> "{0:b}".format(seq_snob42[1])
        '1010'
        
        Then, what about the tenth-largest 6-bit number with three
        bits set?

        >>> seq_snob63 = SNOBSequence(6,3)
        >>> seq_snob63[9]
        35
        >>> "{0:b}".format(seq_snob63[9])
        '100011'

	"""
        if r > n:
            raise ValueError('n must be ≥ r')
        self._n = n
        self._r = r
            # Sticky internal index
        super().__init__(self._get_bits, length=int_ncr(n,r), ii_start=1)

class AccumulateSequence(CacheableSequence):
    """A number sequence in which each term is the result of running
    a function on the requested term and all previous terms.

    The AccumulateSequence is intended to be an addressable analogue
    to the ``accumulate`` iterator from Python's itertools.
    """
    def _get_acc(self, i):
        """Get the accumulation of the first+i'th term, and all
        terms before it.

        The accumulative function is defined by the function or
        method referenced by the func_a argument when the
        AccumulateSeqence is created.

        """
        self._a = self._func_ii(self._ii_start)
        for i in range(self._ii_start+1, i+1):
            self._a = self._func_a(self._func_ii(i), self._a)
        return self._a 

    def __init__(self, func_ii, func_a, **kwargs):
        """Create an AccumulateSequence
        
        Options for Creating an AccumulateSequence
        ------------------------------------------

        Arguments
        =========
        func_ii - The function to derive a term of the sequence. Accepts
            'full-bodied' functions or lambdas. The function has either
            one or two arguments depending where it is defined:

            * If the function is defined outside a class or inside
            a method then it must only have one argument for the 
            internal index of the term. For more info on internal
            and external indices, see NumberSequence.__init__().

            * If the function is defined inside a class, it is 
            classified as a method by Python conventions, and must
            have two arguments, one for ``self`` and another for
            the index of the term.

        func_a - Function to run on all previous terms of the sequence.
            The result of func_ii for the requested term is then combined
            into the total result with this function.

            Accepts 'full-bodied' functions or lambdas. The function
            has either two or three arguments depending on where it is
            defined:

            * If the function is defined outside a class: Two arguments.
            First argument: index of the current term.
            Second argument: total result of all previous terms.
            Indices begin from zero for the first term.
            * If the function is defined inside a class:
            First argument: the ``self`` argument[1].
            Second argument: index of the current term.
            Third argument: total result of all previous terms.

        [1] According to the Python specs, the ``self`` argument does not
         have to be the first, but this is preferred in nearly all projects.
.
        Optional Arguments
        ==================
        
        init_val - Initial value of the accumulator in the sequence.

        Other Optional arguments are passed back to superclasses
        CacheableSequence and NumberSequence as **kwargs.
        For these options, please see __init__() in these superclasses
        above.

        See Also
        --------
        SumSequence, a sequence where each term is the result of all
        terms added together.
        """
        # Instance Attributes
        self._a = kwargs.get('init_val',0)
            # Accumulator
        self._func_ii = func_ii
        self._func_a = func_a
        super().__init__(self._get_acc, **kwargs)

class SumSequence(AccumulateSequence):
    """An accumulative sequence in which each term is the result of
    adding the requested term with all previous terms.
    
    The SumSequence is intended to be an addressable analogue
    to the ``accumulate`` iterator from Python's itertools, when left
    to run with the default ``func``, which is a sum function,
    functionally equivalent to ``lambda a,b : a+b``.
    """

    def __init__(self, func_ii, **kwargs):
        """
        Options for Creating an AccumulateSequence
        ------------------------------------------

        Arguments
        =========
        func_ii - The function to derive a term of the sequence. Accepts
            'full-bodied' functions or lambdas. The function has either
            one or two arguments depending where it is defined:

            * If the function is defined outside a class or inside
            a method then it must only have one argument for the 
            internal index of the term. For more info on internal
            and external indices, see NumberSequence.__init__().

            * If the function is defined inside a class, it is 
            classified as a method by Python conventions, and must
            have two arguments, one for ``self`` and another for
            the index of the term.

        """
        super().__init__(func_ii, lambda a,b:a+b, **kwargs)

