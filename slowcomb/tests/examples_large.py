"""
Shared Large Specimens for Manual and Automated Tests

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

# NOTE: This is a separate module for large Combinatorial Units that may
# take a long time to initialise.

# NOTE: Preliminary testing has shown that the Combination and
# CombinationWithRepeats classes are able to handle a much larger number
# of terms than 2000C128, but term derivations were found to be rather
# slow (taking 10 seconds or more on a test system).

from slowcomb.slowcomb import CatCombination, Combination, \
    CombinationWithRepeats, Permutation, PermutationWithRepeats

# Large Combinatorial Units
#
cc_large_100000_128 = CatCombination( (('🌒','🌓','🌔','🌕'),)*100000, r=10000)
    # Large Catenating Combination with 100 thousand sub-source sequences
    # selecting from all 100 sources
comb_large_2000_128 = Combination([x for x in range(2000)], r=128)
    # Large Combination with a 2000-element source, selecting 128 items
comb_pkmn = Combination([x for x in range(809)], r=6)
    # Large Combination with 809-element source, selecting 6 items
comr_large_2000_128 = CombinationWithRepeats([x for x in range(2000)], r=128)
    # Large Repeats-Permitted Combination with 2000-element source,
    # selecting 128 items
perm_large_100000_128 = Permutation([x for x in range(100000)], r=128)
    # Large Permutation with 100 thousand-element source, selecting
    # 128 items
prmr_large_100000_128 = PermutationWithRepeats(
    [x for x in range(100000)], r=128)
    # Large Repeats-Permitted Permutation with 100 thousand-element source,
    # selecting 128 items

