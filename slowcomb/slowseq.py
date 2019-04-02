"""
Number Sequence classes for supporting Combinatorial Units
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
    * n - Number of items in the set. Accepts int.

    * r - Number of selections from the set. Accepts int.

    """
    return int(factorial(n)/( factorial(r)*factorial(n-r) ))

# Classes
#
class NumberSequence:
    """
    Subscriptable Lazily-Evaluated Numerical Sequence

    A class for creating a numerical sequence where individual terms
    of the sequence may be requested in any order with numbered indices,
    or slices.

    This class is the basis for most of the main classes of slowcomb, 
    including the CombinatorialUnit classes.

    For examples on how to use the NumberSequence, see the section
    More Examples on Using NumberSequence below.
            

    Required Arguments
    ------------------
    * func - The function to derive a term of the sequence. Both 
      block and lambda functions are accepted.

      * If func is defined at module or method scope, the
          arguments should be like:

        ::

          func(ii)

        The internal index value will be used as the value of ii.

      * If func is defined at class scope, please use the following
        argument format instead:
      
        ::
        
          func(self, ii)
       
      Please note that the NumberSequence uses the internal index
      to derive its terms. Please see the section Term Indexing
      below.

    * length - Number of terms in the sequence. Accepts int,
      where length ≥ 0.


    Optional Arguments
    ------------------
    * ii_start - The first position of the internal index. Accepts int,
      where ii_start ≥ 0. Default is 0. For details on its use, see
      the section Term Indexing below.

    * default - The default value or object returned in the event the
      sequence has a zero length, or is unable to otherwise derive
      a term from a valid index. Any object is accepted. The default
      default is None.


    Term Indexing
    -------------
    NumberSequence uses a two-level addressing system to map integer
    indices supplied by the consumer to a term of the sequence.

    *External Indices* are supplied to the NumberSequence by consumer
    code, by way of subscripting as seen in expressions like
    ``seq[1]``; the number 1 is the external index.

    *Internal Indices* are the indices used by only the NumberSequence
    to keep track of the terms. Internal Indices are resolved from
    external indices with the ``_resolve_i()`` method.
    
    By default, the Internal Index points to the same term as the
    External Index, but this can be altered with the ``ii_start``
    keyword argument when creating a new NumberSequence.

    At time of writing, the relationship between external and internal
    indices is a constant. The external index is always a fixed number
    ahead or behind the internal index. In maths speak:

    ::
       
       ii = i + ii_start,

    Where ``_ii_start`` is an integer.

    Example
    =======
    Consider the following sequence:

      "All powers of two from zero to 100."

    In code, you could express it like:

    >>> from slowcomb.slowseq import NumberSequence
    >>> pow_twos = NumberSequence(lambda x:2**x, length=101)
    >>> # PROTIP: There are a hundred *and one* numbers
    >>> # between zero to 100 *inclusive*.

    To get the fifth power of two, you would call

    >>> pow_twos[5]
    32

    But what if the sequence was defined like this instead:

      "All powers of two -50 to 50."

    You have two options, either rewrite the equation as:

    >>> pow_twos_nfa = NumberSequence(lambda x:2**(x-50), length=101)

    Or use internal index mapping:

    >>> pow_twos_nfb = NumberSequence(lambda x:2**x, length=101,
    ... ii_start=-50)

    When you want to recall two to the power of minus 5, which works
    out to be the term behind the 45th external index (as ``2**0`` is
    mapped to the 50th) do this:
    
    >>> pow_twos_nfa[45]
    0.03125

    >>> pow_twos_nfb[45]
    0.03125

    You may encounter non-trivial examples where using internal index
    remapping is more advantageous than rewriting the equation.


    More Examples of Using NumberSequence
    -------------------------------------
    Quadratic Curve 
    ===============
    This example uses ``ii_start``.

    Consider this sequence -- all positive values of y in:

        y = -(x/40)**2 + 100 

    Where x is an integer.

    After working it out, we come to the conclusion that -40 ≤ x ≤ 40.
    This also means we have eighty-one terms, when we include x=0.

    >>> from slowcomb.slowseq import NumberSequence
    >>> func_funk = lambda x: -(x/4)**2 + 100
    >>> seq_quadr = NumberSequence(func_funk, ii_start=-40, length=81)

    The result of x=-40 is thus mapped to:

    >>> seq_quadr[0]
    0.0

    As the external index of 0 is mapped to internal index -40, which
    the NumberSequence uses as the x-value.

    We can recall the maximum value of y:

    >>> seq_quadr[40]
    100.0

    The value x=0 is mapped to the 40th External Index, which resolves
    to Internal Index zero, which in turn is used as the x-value of
    func_funk to derive the term.

    Try other indices, like:

    >>> seq_quadr[80]
    0.0

    >>> seq_quadr[20]
    75.0

    >>> seq_quadr[60]
    75.0

    >>> seq_quadr[10]
    43.75

    >>> seq_quadr[70]
    43.75

    Powers of Two, Part II
    ======================
    This example demonstrates slice addressing to request multiple
    terms in a single call

    The sequence is expressed as:
    
      "All powers of two from 0 to 10"

    This can be coded as:

    >>> from slowcomb.slowseq import NumberSequence
    >>> func_pow2 = lambda x:2**x
    >>> seq_pow2 = NumberSequence(func_pow2,length=11)

    The 10th term of the sequence, 2**10, can be addressed as such:

    >>> seq_pow2[10]
    1024

    The 2nd to 5th terms inclusive can be addressed with a slice like:

    >>> seq_pow2[2:6] 
    (4, 8, 16, 32)

    You can also get all even powers of two from the sequence:

    >>> seq_pow2[2:11:2]
    (4, 16, 64, 256, 1024)

    Python sequence slicing conventions are also in use here, with
    respect to how the stop value is interpreted: [2:5] means
    '2nd to before the 5th'. Likewise, [5:2:-1] means '5th back to
    after the 2nd'.

    Powers of Two, Part III
    =======================
    This example demonstrates the use of negative indices for getting
    multiple terms in reverse order, or for addressing terms by position
    relative to the end (right side) of the sequence.

    While we're still with our power-of-two sequence:
    >>> from slowcomb.slowseq import NumberSequence
    >>> seq_pow2 = NumberSequence(lambda x:2**x,length=11)

    Multiple terms in reverse order with negative step values:
    
    >>> seq_pow2[5:1:-1]
    (32, 16, 8, 4)
        
    Negative addressing to get a term by its position from the
    right end, as seen with Python's built-in sequence types:

    Get the first item from the right:

    >>> seq_pow2[-1]
    1024

    Or the second from the right:

    >>> seq_pow2[-2]
    512

    To get the second to second-last (9th) term in reverse order:

    >>> seq_pow2[-2:1:-2]
    (512, 128, 32, 8)

    To get the first to the fifth term in reverse order:

    >>> seq_pow2[5:0:-1]
    (32, 16, 8, 4, 2)

    NOTE: Due to limitations, it is not possible to include the
    zeroth term of a sequence in a slice when a negative step value
    is used.

    Warm and Cool Colours
    =====================
    This example demonstrates the use of block functions with the
    NumberSequence, and a possiblitiy of using non-decimal output.

    Consider a sequence 100 colours. Every other colour is an 
    opposite colour of the last. The first colour is a warm colour,
    and second a cool colour, and so on.

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

    Note the omission of the ``length`` keyword.

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

    Guess what these colours are:

    >>> seq_hue[80]
    '#9900BF'

    >>> seq_hue[83]
    '#03BF00'

    >>> seq_hue[90]
    '#BF0072'

    Use As An Iterator
    ------------------
    As with all sequence types, you can use a NumberSequence, and
    all of its subclasses, as an iterator:

    >>> from slowcomb.slowseq import NumberSequence
    >>> seq_sq = NumberSequence(lambda x:x**2, length=10, ii_start=1)
    >>> for i in seq_sq:
    ...     print(i,end=',')
    1,4,9,16,25,36,49,64,81,100,

    """
    # Private Methods
    # 
    def _check_i(self, i):
        """
        Checks if an external index is out of bounds.
        
        Raises an IndexError when index is deemed to be out of range.

        Arguments
        ---------
        * i - external index, as an int

        Exceptions
        ----------
        * IndexError - if i is deemed out of range.

        """
        len_self = len(self)
        if i >= len_self or i < -len_self:
            raise IndexError('Sequence index out of bounds')
    
    def _clamp_i(self, i, i_min, i_max):
        """
        Limits a value to a set range.

        If a value i is found to exceed a nominated maximum, the
        maximum is returned. Likewise, if i is lower than a minimum
        value, the minimum value is returned.

        Arguments
        ---------
        * i - the value to be checked

        * i_min - minimum value to be returned

        * i_max - maximum value which may be returned

        All arguments may be of any type which supports comparisons by
        the less than (<) and greater than (>) operators.

        """
        if i >= i_max:
            return i_max
        elif i <= i_min:
            return i_min
        else:
            return i

    def _get_args(self):
        """
        Attempt to rebuild a probable equivalent of the arguments
        used in constructing this sequence, as a ``str``.

        """
        re_arg_fmt = "func={0}, length={1}, ii_start={2}, default={3}"
        re_args = re_arg_fmt.format(
            self._func.__code__.co_name,
            self._len, self._ii_start,
            self._default
        )
        return re_args
 
    def _get_term(self, i):
        """
        Return the first+n'th member of this sequence.
        See the class documentation on how to get members from the
        sequence.

        Arguments
        ---------
        * i - External index of the member. Accepts int, i ≥ 0.

        """
        # TODO: Write up on how term derivation function ``_func``
        #       is called, and why this pattern is used.
        #       
        self._check_i(i)
        return self._func(self._resolve_i(i))

    def _get_terms(self, s):
        """
        Routine to return multiple members in response to a slice
        
        Arguments
        ---------
        * s - Python ``slice`` containing external indices for start,
          stop and step values.

        """ 
        out = []
        s = self._resolve_slice(s)
        for ii in range(s.start, s.stop, s.step):
            out.append(self._func(ii))
        return tuple(out)

    def _resolve_i(self, i):
        """
        Remaps external indices to internal indices, and supports
        the use of negative indices. See the class documentation for
        NumberSequence for details on how it works, and why it is
        in use.

        Arguments
        ---------
        * i - External index, accepts int, i ≥ 0.

        """
        if i < 0:
            return self._ii_stop + i
            # PROTIP: Add with a negative to subtract from
            #  its magnitude
        else:
            return self._ii_start + i

    def _resolve_slice(self, s):
        """
        Resolves a slice containing external indices to a slice 
        of internal indices. Calls _clamp_i() and _resolve_i().

        Arguments
        ---------
        * s - Python ``slice`` containing external indices.

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
        """
        Sets the upper limit of the internal index.

        Always returns None.
        """
        self._ii_stop = self._ii_start + self._len
        

    # Special Methods and Constructor
    #
    def __getitem__(self, key):
        """
        Supports getting single or multiple individual terms from 
        a NumberSequence using Python's subscript notation.

        For details on how this works on this class, please refer
        to the class documentation above.

        Exceptions
        ----------
        * TypeError - when an object that is not an ``int``or a
          ``slice`` is used in place of ``key``.

        """
        if isinstance(key, int) is True:
            return self._get_term_method(key)
        elif isinstance(key, slice) is True:
            return self._get_multi_term_method(key)
        else:
            raise TypeError('indices must be int or slice')


    def __iter__(self):
        """
        Special method just to enable use of this class as an iterator.
        See the class documentation above for details.

        """
        return self


    def __len__(self):
        """
        Return the number of terms available, as an ``int``.
        """

        # NOTE: This works also when _ii_start is negative
        return self._len

    def __next__(self):
        """
        Supports the use of this class as an iterator.
        """
        if (self._ii_stop is None) or (self._i >= len(self)):
            raise StopIteration
        out = self[self._i]
        self._i += 1
        return out

    def __repr__(self):
        """
        Supports the reporting of information that can be used to 
        reconstruct this sequence. The information is returned as a
        string when the name an instance is referenced, without any
        reference to its members or without any parentheses.

        """
        out = "{0}({1})".format(self.__class__.__name__, self._get_args())
        return out
        # TODO: Implement Slowcomb Reporting Tools

    def __init__(self, func, length, **kwargs):
        """
        This is the constructor for creating an instance of this class.

        For details on using this class, please refer to the class
        documentation above.

        """
        # Class Constructor
        # 
        # Set Instance Attributes
        #
        self._default = kwargs.get('default', None)
            # The default value returned if the member cannot be derived
        self._func = func
            # The function to get the value of a term in a sequence.
        self._get_term_method = self._get_term
            # Intermediate method to call _func.
            #  May be swapped out with an alternate method to enable 
            #  caching, or alternative lookup methods.
        self._get_multi_term_method = self._get_terms
            # Intermediate method to call _func for multiple terms,
            #  and return them in an appropriate data type.
            #  May be swapped out with an alternate method to enable 
            #  caching, or alternative lookup methods.
        self._ii_start = int(kwargs.get('ii_start', 0))
            # First internal index. May be referred to as the ii 
            #  start offset.
        self._i = 0
            # Index when used as iterator.
        self._ii_stop = 0
            # Last internal index.
        self._len = int(length)
            # Expected number of external addresses including the zeroth
            #  index
        self._name = ''
            # TODO: Reserved attribute for reporting tools

        # Perform Init Routine
        #
        if self._len < 0:
            raise ValueError('sequence length must be zero or more')
        self._set_ii_bounds()


class CacheableSequence(NumberSequence):
    """
    Cacheable alternative to NumberSequence, the Subscriptable
    Lazily-Evaluated Numerical Sequence

    The CacheableSequence for use with number sequences whose terms
    may be slow or memory-intensive to derive. The dictionary caches
    every member lookup in its dictionary until it is cleared.

    The CacheableSequence is used exactly the same way as
    NumberSequence, with the added option of switching on and off
    the cache, as well as clearing it.


    Required Arguments
    ------------------
    Operation of CacheableSequence exactly the same as with
    NumberSequence. For full details, please refer to NumberSequence's
    class documentation.
    
    * func - The function to derive a term of the sequence. Both 
      block and lambda functions are accepted.

      * Example function defined at module or method scope:
        ``func(ii)``.

      * Example function defined at class scope:
        ``func(self, ii)``.
       
    * length - Number of terms in the sequence. Accepts int,
      where length ≥ 0.


    Optional Arguments
    ------------------
    * ii_start - The first position of the internal index. Accepts int,
      where ii_start ≥ 0. Default is 0. 

    * default - The default value or object returned in the event the
      sequence has a zero length, or is unable to otherwise derive
      a term from a valid index. Any object is accepted. The default
      default is None.
    
         
    Caching
    -------
    The cache is disbled by default. Call enable_cache() to start
    using it, and call disable_cache() to stop using the cache and
    to clear it. When enabled, caching is automatic and performed
    for every term, requested by a single index, that has not been
    previously requested or cached.

    Call clear_cache() to clear the cache without disabling it.

    For more details on how the cache is enabled or disabled,
    see enable_cache() and disable_cache() below.

    Limitations
    ===========
    Caching is not available for multiple lookups using slices.
    When getting terms using slices, the cache is bypassed and the
    terms not cached.

    Considerations
    --------------
    When to Use It
    ==============
    Speed advantages are achieveable if the time taken to derive a 
    term is significantly longer than entering an exception block
    and performing a Python ``dict`` lookup.
    
    The method of caching used herein is recommended for scenarios
    where the same terms from the sequence will be looked up very
    frequently, yet the terms are not easy to predict ahead of time.

    In compsci parlance, we would refer to this as a read pattern
    with strong temporal locality.
    
    When Not to Use It
    ==================
    As with many conventional methods of caching, scenarios with 
    frequent reads that are unpredictable, random lookups (having
    weak temporal locality) and within a wide range (weak spatial
    locality) are not likely to benefit from the dictionary cache.


    Examples
    --------
    This is a demonstration on a sequence of the first 999,999,999
    prime numbers or so. An extermely slow method of deriving the prime
    numbers is in use, in order to increase casual observability of
    the cache's action:

    ::

      # Please increase the numbers until the uncached lookups are
      # noticeably slow if you find no observable difference between
      # cached and uncached lookups.

      from slowcomb.tests.slowprime import slow_prime
      from slowcomb.slowseq import CacheableSequence
      cache_d = CacheableSeqeuence(slow_prime, length=999999999)

      # This term lookup should be noticeably slow even on
      # a high-performance machine. 
      print("First time lookup")
      cache_d[1500]

      # Enable the cache
      print("Cache enabled")
      cache_d.enable_cache()

      # This term lookup should be much faster
      print("Second-time lookup")
      cached[1500]

      # First-time lookups should be slow
      print("First time lookup")
      cached[1520]

      # Second-time lookups should be fast again
      print("Second time lookup")
      cached[1520]
        
      # Multiple lookups are not cached. This request will be
      # always slow
      print("First time multiple lookup")
      cached[500:504]
      print("Second time multiple lookup")
      cached[500:504]

      # This could not even finish in an hour on a 2016-vintage
      # system, but the second lookup onwards should be faster :P
      print("First time lookup")
      cached[-1]

      print("Second time lookup")
      cached[-1]

      print("Third time lookup")
      cached[-1]


    References
    ----------
    * Wikipedia. Locality of Reference.
      https://en.wikipedia.org/wiki/Locality_of_reference

    """
    # Public Methods
    #
    def disable_cache(self):
        """
        Disable the dictionary cache.
        
        The cache will be re-enabled when enable_cache() called.
        Disabling the cache also clears it.

        The default method for requesting single terms, ``_get_term()``
        is switched back in and bound to ``_get_term_method``.

        """
        self._cache = None
        self._get_term_method = self._get_term

    def enable_cache(self):
        """
        Set up and enable the dictionary cache.

        The default method for requesting single terms is switched
        out for ``_get_term_with_cache()``, by binding said method
        to ``_get_term_method``.
        
        """
        self._cache = {} 
        self._get_term_method = self._get_term_with_cache
        self._cache_multi_method = self._add_term_to_cache
    
    # Private Methods
    #
    def clear_cache(self):
        """
        Removes all saved results from cache to free up memory
        
        """
        self._cache.clear()

    def _add_term_to_cache(self, data, i, **kwargs):
        """
        Save a term into the dictionary cache.

        This method always returns None.


        Arguments
        ---------
        * data - a term of this sequence to save to cache.
          Accepts any Python object.

        * i - index to recall a data item with.
          Accepts int, i ≥ 0


        Notes
        -----
        The **kwargs argument is for compatibility purposes, to
        allow for implementions of new features in the
        CacheableSequence.
        
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
    
    def _get_term_with_cache(self, i):
        """
        Return the term of external index i of the sequence from the
        dictionary cache.

        If the term cannot be found in the cache, the cache is
        bypassed for the lookup. When the term has been derived, it
        is added to the cache.

        Arguments
        ---------
        * i - The index of the term of the sequence. Accepts int, i ≥ 0.
        
        """
        cache_enabled = self._cache is not None
        try:
            return self._cache[i]
        except KeyError:
            # On cache miss, fallback to normal path...
            out = self._get_term(i)
            # And save the result
            self._add_term_to_cache(out, i)
            return out

    # Special Methods and Constructor
    # 
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self._cache = None

class BlockCacheableSequence(CacheableSequence):
    """
    Cacheable alternative to NumberSequence, the Subscriptable
    Lazily-Evaluated Numerical Sequence

    The BlockCacheableSequence for use with number sequences whose
    terms may be slow or memory-intensive to derive. A tuple is used
    as a cache, which stores blocks of either equidistant or adjacent 
    terms requested with a slice lookup.

    The BlockCacheableSequence is used exactly the same way as
    NumberSequence, with the added options of switching on and off
    the cache and saving terms to the cache.


    Required Arguments
    ------------------
    Operation of CacheableSequence exactly the same as with
    NumberSequence. For full details, please refer to NumberSequence's
    class documentation.
    
    * func - The function to derive a term of the sequence. Both 
      block and lambda functions are accepted.

      * Example function defined at module or method scope:
        ``func(ii)``.

      * Example function defined at class scope:
        ``func(self, ii)``.
       
    * length - Number of terms in the sequence. Accepts int,
      where length ≥ 0.


    Optional Arguments
    ------------------
    * ii_start - The first position of the internal index. Accepts int,
      where ii_start ≥ 0. Default is 0. 

    * default - The default value or object returned in the event the
      sequence has a zero length, or is unable to otherwise derive
      a term from a valid index. Any object is accepted. The default
      default is None.
         
    Members are only cached when they are looked or derived up as part
    of a multiple-item operation using slices.


    Caching
    -------
    The cache is disbled by default. Call enable_cache() to start
    using it, and call disable_cache() to stop using the cache and
    to clear it.
    
    When enabled, caching is manual and performed each time multiple
    terms are requested using a slice.

    To clear the cache, without disabling it, perform a dummy lookup
    using a zero-length slice, like [0:0]. This forces caching of a
    negligibly small slice.

    For more details on how the cache is enabled or disabled,
    see enable_cache() and disable_cache() below.

    Limitations
    ===========
    Caching is not available for multiple lookups using slices. While
    slice lookups saves terms into the cache, the cache is effective
    for for single lookups.
    
    Only one slice may be cached at any given time.

    Considerations
    --------------
    When To Use It
    ==============
    Where there are frequent lookups that are invariably or mostly
    within a small, contiguous range of indices, or where they are
    consistently equidistant, the benefits of the block cache will be
    the most apparent. In compsci parlance, this would be described as
    having a read pattern with strong spatial or strong equidistant
    locality.

    When Not To Use It
    ==================
    The BlockCacheableSequence is not able to provide any performance
    benefit where lookups are frequently random, non-equidistant and
    over a large range of indices.


    Examples
    --------
    This is a demonstration on a sequence of the first 999,999,999
    prime numbers or so. An extermely slow method of deriving the prime
    numbers is used, to increase casual observability of the cache's
    action:

    ::

      # Please increase the numbers until the uncached lookups are
      # noticeably slow if you find no observable difference between
      # cached and uncached lookups.

      from slowcomb.tests.slowprime import slow_prime
      from slowcomb.slowseq import CacheableSequence
      cache_b = BlockCacheableSeqeuence(slow_prime, length=999999999)

      # This lookup should be slow
      print("Uncached lookup")
      cache_b[500]

      # Enable the cache to start using it
      cache_b.enable_cache()

      # The next couple of lookups should still be slow
      print("Second lookup not cached")
      cache_b[500]
      print("Subsequent lookup still not cached")
      cache_b[500]

      # Caching Contiguous Lookups 
      # --------------------------
      # Prime the cache by performing a slice lookup
      # Set up the cache for adjacent lookups
      print("Caching adjacent lookups")
      cache_b[495:505]

      # These lookups will be fast
      print("Cached lookups")
      cache_b[495]
      cache_b[500]
      cache_b[497]
      cache_b[493]
      cache_b[500]

      # This lookup will be slow
      print("Uncached lookup")
      cache_b[460]

      # Caching Equidistant Non-Contiguous Lookups
      # ------------------------------------------
      # Re-prime the cache for equidistant lookups
      # This multi-lookup requests even-index terms between
      # 482 and 500 in reverse order.
      print("Caching equidistant non-contiguous lookups)
      cache_b[498:480:-2]

      # These lookups will be fast
      print("Cached lookups")
      cache[482]
      cache[484]
      cache[486]
      cache[488]
      cache[490]
      cache[498]

      # These lookups will be slow
      cache[479] # Out of range of cache
      cache[480] # Unreachable by negative step slicing
      cache[481] # Odd index not included in cache
      cache[483]
      cache[485]
      cache[487]
      cache[500] # Deleted from cache, out of range
      cache[501] # Out of range of cache

    
    References
    ----------
    * Wikipedia. Locality of Reference.
      https://en.wikipedia.org/wiki/Locality_of_reference

    """

    def disable_cache(self):
        """Disable the block cache and clear it"""
        self._cache = None
        self._get_term_method = self._get_term

    def enable_cache(self):
        """Set up the block cache"""
        self._cache = []
        self._cache_start_i = 0
        self._cache_step_i = 1
        self._cache_stop_i = 0
        self._get_term_method = self._get_term_with_cache
        self._cache_method = self._add_terms_to_cache

    def _add_terms_to_cache(self, data, **kwargs):
        """
        Save data to the BlockCacheableSequence.

        This is a simple operation in which the results of a slice
        multi-lookup is copied to cache, along with the details of the
        slice.  This operation also deletes all existing content in
        the cache.

        """
        self._cache_start_i = kwargs.get('start',0)
        self._cache_step_i = kwargs.get('step',1)
        self._cache_stop_i = kwargs.get('stop',0)
        self._cache = data

    def _get_terms(self, s):
        """
        Routine to return multiple terms in response to a slice.
        The terms are returned in a tuple.
        
        Arguments
        ---------
        * s - start, stop and step external indices, in a slice.

        """ 
        out = []
        s = self._resolve_slice(s)
        for ii in range(s.start, s.stop, s.step):
            out.append(self._func(ii))
        self._add_terms_to_cache(out,start=s.start,stop=s.stop,step=s.step)
        return tuple(out)

    def _get_term_with_cache(self, i):
        """
        Get the first+i'th term of the sequence from the block cache.

        In the event that the term cannot be found in the cache (cache
        miss), the method will resort to looking up the term without
        the cache. The cache is effective for any term that was part
        of a cached multi-item slice lookup.

        Arguments
        ---------
        * i - External index of the term being requested. Accepts int,
          0 ≤ i ≤ len(self).

        Further Reading
        ---------------
        For more information on how this cache works, see the class
        documentation above, and also _add_terms_to_cache().

        """
        cache_i = None
        on_step = (i % self._cache_step_i) == 0
        if self._cache_start_i > self._cache_stop_i and self._cache_step_i<0:
            # Cache is in reverse order
            in_range=(i <= self._cache_start_i and i > self._cache_stop_i)
            if in_range and on_step:
                cache_i = (self._cache_start_i - i) // abs(self._cache_step_i)
        elif self._cache_start_i < self._cache_stop_i and self._cache_step_i>0:
            # Cache is in forward order
            in_range=(i >= self._cache_start_i and i < self._cache_stop_i)
            if in_range and on_step:
                cache_i = (i - self._cache_start_i) // self._cache_step_i
        if cache_i is None:
            # On cache miss, fallback to normal path
            out = self._get_term(i)
        else:
            out = self._cache[cache_i]
        return out

    def __init__(self, func, **kwargs):
        """
        This is the constructor for creating an instance of this class.

        For details on using this class, please refer to the class
        documentation above.

        """
        # Instance Attributes

        self._cache = None
        self._cache_start_i = 0 
            # Index of first term to be cached
        self._cache_step_i = 1
            # Distance between cached terms
        self._cache_stop_i = 0
            # Index of last term to be cached
        super().__init__(func, **kwargs)


class SNOBSequence(NumberSequence):
    """
    A Sequence of Numbers With the Same Number Of Bits (SNOB).

    This class is a NumberSequence that lazily evaluates all possible
    binary numbers of a given length and a set number of bits.

    Numbers are ordered by their value when expressed as a quantity,
    with the numbers with the highest such value to the smallest.

    SNOBSequence returns all numbers as an int.


    Required Arguments
    ------------------
    * n - The number of bits the number will have. Accepts int,
      where n > 0.

    * r - The number of bits which will be raised (set to high/1/
      active...). Accepts int, where r ≤ n. 


    Examples
    --------
    Here are all the 4-bit numbers with two bits set.

    ::
      
      >>> from slowcomb.slowseq import SNOBSequence
      >>> ["{:04b}".format(x) for x in SNOBSequence(4,2)]
      ['1100', '1010', '1001', '0110', '0101', '0011']

    Tell me that you comprehend the above list comprehension.

    These are the equivalent decimal values for 4-bit numbers
    with two bits set:

    ::

      >>> [x for x in SNOBSequence(4,2)]
      [12, 10, 9, 6, 5, 3]

    Here are the 6-bit numbers with three bits set, along
    with their equivalent decimal forms.

    ::
      
      >>> snob6_3 = SNOBSequence(6,3)
      >>> for x in snob6_3:
      ...   print("{0:06b} == {0}".format(x))
      111000 == 56
      110100 == 52
      110010 == 50
      110001 == 49
      101100 == 44
      101010 == 42
      101001 == 41
      100110 == 38
      100101 == 37
      100011 == 35
      011100 == 28
      011010 == 26
      011001 == 25
      010110 == 22
      010101 == 21
      010011 == 19
      001110 == 14
      001101 == 13
      001011 == 11
      000111 == 7

    You can still request each bitmask individually:
    
    ::
      
      >>> snob6_3[0]
      56

      >>> snob6_3[4]
      44
    
    Or slice them any which way!

    Further Reading
    ---------------
    Please see _get_leading_z_with_i() and _get_bits() below for
    details on how numbers are derived.

    """
    def index(self, x):
        """
        Look up the index of a number if it belongs in this SNOBSequence.

        This method is made possible by the fact that the numbers, when
        expressed as decimal or binary numbers, are ordered in the 
        sequence by value from highest to the lowest.
        
        Arguments
        ---------
        * x - SNOB number in decimal form. Accepts int, x > 0

        Exceptions
        ----------
        * ValueError - when the number is not found in the sequence

        """
        i_last = len(self)-1

        # Reject out-of-range bitmaps
        if x > self[0] or x < self[i_last]:
            msg = 'number: {0} is not part of this sequence'.format(x)
            raise ValueError(msg)
        
        # Perform a binary search for the bitmap
        i_peg_a = 0
        i_peg_b = i_last
        while i_peg_b - i_peg_a > 1:
            i_target = (i_peg_b + i_peg_a)//2
            val = self[i_target]
            if val < x:
                i_peg_b = i_target
            elif val > x:
                i_peg_a = i_target
            elif val == x:
                return i_target
        
        # FIXME: This is a workaround for a problem with the binary
        #  search algorithm above in which it routinely misses the
        #  bitmaps at the very beginning (i == 0) or end (i == len(self)-1).
        #  The pegs are sometimes unable to close in and become the same
        #  value to allow i_target to lock onto the bitmap being sought.
        #
        #  The current (hopefully temporary) fix is to perform a linear
        #  search on the space between the two pegs before calling off 
        #  the search.
        for iii in range(i_peg_a, i_peg_b+1):
            if self[iii] == x:
                return iii

        # Finally call off the search when all attempts fail
        msg = 'bitmap {0} not in sequence'.format(x)
        raise ValueError(msg)


    def _get_leading_z_with_i(self, n, r, i):
        """
        Get the number of leading zero bits of i when expressed
        in binary, along with its ordinality among fellow numbers
        numbers with:
        
        * The same number of leading zero bits,

        * The same number of raised bits, and

        * The same total number of bits 

        Returns a tuple t, where: 

        * t[0] - The number of zeroes given any value of n, r and i
          above.

        * t[1] - The ordinality/rank of the number among numbers with
          the same leading zeroes


        Arguments
        ---------
        * n - Total bits in the number. Accepts int. n > 0.

        * r - Number of raised bits in the number. Accepts int,
          0 < r ≤ n.

        * i - The subject of this method. Accepts int,
          0 < r ≤ nCr(n,r), where  nCr(n,r) = n! / r! * (n-r)! 


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

    def _get_args(self):
        """
        Attempt to rebuild a probable equivalent of the arguments
        used in constructing this sequence

        """
        re_arg_fmt = "n={0}, r={1}"
        re_args = re_arg_fmt.format(self._n, self._r)
        return re_args
    
    def _get_bits(self, ii):
        """
        Construct the first+ii'th binary number with a length specified
        in self._n, with self._r number of bits raised. This is the
        default _get_term() function of the SNOBSequence.
        
        Argument
        --------
        * ii - The i'th highest number. Accepts int, 0 < ii ≤ nCr(n,r)
          [where nCr(n,r) = n! / r! * (n-r)!]

        Exceptions
        ----------
        * ValueError - when self._n ≤ self._r. This should not happen
          during normal operation.

        How It Works
        ------------
        The current method takes advantage of the fact that the number
        of binary numbers with the same number of leading zeroes,
        raised bits and total bits can be determined ahead of time.
        
        The exact algorithm to determine this can be found in 
        _get_leading_z_with_i() above. For brevity's sake, the method
        would be called (somewhat less accurately) the Leading-Z.

        This method used herein is non-recursive and therefore
        stack-saving.

        Example A
        =========
        Find the fourth highest 8-bit number with three raised bits.
        The short notation n=8, r=3, ii=4 will be used.
        
        We start out not knowing a single bit. The number will be
        constructed from the most significant side (left).

        ????????
       
        By Leading-Z, n=8,r=3,ii=4 has no leading zeroes. A raised bit
        is added to the leftmost bit.
        
        1???????
        
        Having given up a single raised bit, the process is repeated
        on the remaining seven bits. The cardinality remains the same,
        but the number of bits are reduced by one.
        
        There are seven bits left to go, with two raised bits left.

        Our number is n=7,r=2,ii=4. By Leading-Z, there are no leading
        zeroes for this number, the cardinality remains the same.

        11??????
       
        The process is repeated with the remaining six bits, with
        n=6,r=1,ii=4. Leading-Z says that there's three leading zeroes,
        and the cardinality has changed, as the six-bit number at hand
        is the first of its kind.
       
        11000???

        The process continues with n=3,r=1,ii=1, to which the Leading-Z
        confirms a suspicion you may have: there are no leading zeroes!
        Our number is now:
        
        110001??
        
        Having run out of bits to raise, so we fill the rest of the
        number with zeroes.
        
        11000100
       
        Congratulations, we have successfully found our number!
        This is the fourth-highest 8-bit number with 3 raised bits, better
        known as 196 in decimal.
       
       
        Example B
        =========
        Find the 10th Highest 8-bit number with 5 raised bits.

        10th largest 8-bit number with 5 raised bits has no leading zeroes
        n=8,r=5,ii=10: Leading-Z reports no leading zeroes. Retain the
        cardinality and proceed.
        
        1???????
       
        The 10th largest 7-bit number with 4 raised bits has no leading
        zeroes n=7,r=4,ii=10. Leading-Z reports no leading zeroes...
       
        11??????
       
        With n=6,r=3,ii=10, No leading zeroes.
       
        111?????
       
        With n=5,r=2,ii=10, Three leading zeroes, with the number being
        the largest/first of its kind.
       
        111000??
        
        With n=2,r=2,ii=1, there is only one choice. This number is all
        raised bits, so the number is padded with the remaining raised
        bits.

        11100011 (dec: 227)
        
        Well Done! We have found our number!

        """
        if self._r > self._n:
            raise ValueError('n must be greater than r')
        out_bin = 0
        temp_i = ii
        temp_n = self._n
        temp_r = self._r

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
        """Sets the last internal index of this sequence"""
        self._ii_stop = int_ncr(self._n,self._r)+1

    def __len__(self):
        """Get the number of terms in this sequence"""

        return self._ii_stop - self._ii_start
    
    def __init__(self, n, r):
        """
        This is the constructor for creating an instance of this class.

        For details on using this class, please refer to the class
        documentation above.

        """
        # Instance Attributes
        if r > n:
            raise ValueError('n must be ≥ r')
        self._n = n
        self._r = r
            # Sticky internal index
        super().__init__(self._get_bits, length=int_ncr(n,r), ii_start=1)

class AccumulateSequence(CacheableSequence):
    """
    A NumberSequence in which each term is the result of running
    a function on the requested term with a cumulative result of 
    all previous terms.

    The AccumulateSequence is intended to be a subscriptable analogue
    to Python's built-in itertools.accumulate class.
    
    Required Arguments
    ------------------
    * func_ii - The function which derives a single term of the
      sequence. Accepts 'full-bodied' functions or lambdas. 

      * If the function is defined at module or method scope,
        the function should have one argument like:

        ::
          
          func(ii)
        
        The function will be called to derive the first+ii'th term.

      * If the function is defined at class scope, the function
        should have two arguments including ``self``:

        ::

          func(self, ii)

    * func_a - The function which derives the cumulative result of
      every term before the requested term. Accepts 'full-bodied'
      functions or lambdas.


      * If the function is defined at module or method scope,
        the function should have two arguments like:

        ::
          
          func(x_ii, a)
        
        After func_ii() is called to derive the result, func_a()
        evaluates x_ii into the accumulator.

      * If the function is defined at class scope, the function
        should have three arguments including ``self``:

        ::

          func(self, x_ii, a)
.
    Optional Arguments
    ------------------
    * init_val - Initial value of the accumulator in the sequence.

    See Also
    --------
    * itertools.accumulate, Python's built-in accumulate iterator
      class

    * SumSequence, a sequence where each term is the result of all
      terms added together.

    """
    def _get_args(self):
        """
        Attempt to rebuild a probable equivalent of the arguments
        used in constructing this sequence

        """
        re_arg_fmt_a = "func_ii={0}, func_a={1}, length={2}," 
        re_arg_fmt_b = "ii_start={0}, default={1}"
        re_args_a = re_arg_fmt_a.format(
            self._func_ii.__code__.co_name,
            self._func_a.__code__.co_name,
            self._len
        )
        re_args_b = re_arg_fmt_b.format(
            self._ii_start,
            self._default
        )
        return "{0} {1}".format(re_args_a, re_args_b)

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
        """
        This is the constructor for creating an instance of this class.

        For details on using this class, please refer to the class
        documentation above.

        """
        # Instance Attributes
        self._a = kwargs.get('init_val',0)
            # Accumulator
        self._func_ii = func_ii
        self._func_a = func_a
        super().__init__(self._get_acc, **kwargs)

class SumSequence(AccumulateSequence):
    """
    A NumberSequence in which each term is the result of adding
    up all terms before it.
    
    The SumSequence is intended to be an addressable analogue
    to Python's built-in itertools.accumulate class.

    It is pretty much equivalent to running AccumulateSequence
    with ``lambda x,a: x+a``.


    Required Arguments
    ------------------
    * func_ii - The function which derives a single term of the
      sequence. Accepts 'full-bodied' functions or lambdas. 

      * If the function is defined at module or method scope,
        the function should have one argument like:

        ::
          
          func(ii)
        
        The function will be called to derive the first+ii'th term.

      * If the function is defined at class scope, the function
        should have two arguments including self:

        ::

          func(self, ii)


    Optional Arguments
    ------------------
    * init_val - Initial value of the accumulator in the sequence.

    See Also
    --------
    * itertools.accumulate, Python's built-in accumulate iterator
      class

    * AccumulateSequence, a sequence which allows you to use your own
      accumulative function.

    """
    def __init__(self, func_ii, **kwargs):
        """
        This is the constructor for creating an instance of this class.

        For details on using this class, please refer to the class
        documentation above.

        """
        super().__init__(func_ii, lambda a,b:a+b, **kwargs)

