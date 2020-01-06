"""
General Unit tests for slowcomb.slowcomb (Slow Cominatorics Library
Main Module)

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

import unittest
from slowcomb.slowcomb import CustomBaseNumberF, CustomBaseNumberP

"""
NOTE: As seen on many other tests in this project, the results of
the methods herein are tested against multiple values produced by
a range generator. This way of testing is called "informal proof",
which attempts to prove that a method works for inputs deemed highly
likely to be used during normal operation.

An informal proof, despite being far easier to implement, is not as
thorough as a "formal" proof as seen in mathematics theses. However,
for the time being, they are sufficient to verify correctness during
normal use.

"""

class CustomBaseNumberFTests(unittest.TestCase):
    """
    Tests for Function-defined Radix Custom Base Number Class

    """
    DIGITS_MAX = 1000
    DIGITS_STEP = 249

    def test_get_int_from_digits(self):
        """
        Conversion to integer

        Verify that an integer value can be recovered from the
        Custom-Base Number by informal proof

        """
        length = 12 # Test for all values from 0 until (2**length)-1
        func = lambda x:2 # Dummy binary number
        cbn = CustomBaseNumberF(length, func)
        for i in range(2 ** length):
            with self.subTest(i = i):
                cbn.set_digits_from_int(i)
                ref_i = i 
                test_i = cbn.get_int_from_digits()
                self.assertEqual(test_i, ref_i)

    def test_len(self):
        """
        Output of len()

        Verify that len() returns the number of digits in the
        Custom-Base Number correctly, by informal proof.

        """
        func = lambda x:1 # Dummy zero-value number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            cbn = CustomBaseNumberF(length, func)
            with self.subTest(length=length):
                self.assertEqual(len(cbn), length)
     
    def test_new_number_default_value(self):
        """
        Creation of a new number with default values

        Verify that a Custom-Base Number created with no initial
        digits has exactly zero value, by informal proof.

        """
        func = lambda x:1 # Dummy number always has zero value
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            cbn = CustomBaseNumberF(length, func)
            digits = cbn._digits
            for iii in range(len(digits)):
                with self.subTest(length=length, iii=iii):
                    self.assertEqual(digits[iii], 0)
                    
    def test_get_digits(self):
        """
        Retrieval of digits

        Verify that the method to return the digits of the number,
        get_digits(), does this correctly, by informal proof.

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            test_int = 1
            for iii in range(length-1):
                # Create an integer which when expressed as binary
                # is made entirely of 1's
                test_int <<= 1
                test_int += 1
            cbn = CustomBaseNumberF(length, func)
            cbn.set_digits_from_int(test_int)
            digits = cbn.digits()
            ref = (1,) * length
            with self.subTest(length=length):
                self.assertEqual(digits, ref)

    def test_incr_zero_decimal(self):
        """
        Increment by one from zero

        Verify that increment by one from zero produces exactly one,
        by informal proof

        """
        func = lambda x:10 # Simulated decimal number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            test_int = 0
            cbn = CustomBaseNumberF(length, func)
            cbn.incr() # Increment the number from 0 to 1
            digits = cbn.digits()
            for iii in range(len(digits)-2):
                # Verify that all digits except the least significant
                #  are zeroes
                with self.subTest(length=length, iii=iii):
                    self.assertEqual(digits[iii], 0,
                        'Digits before least significant must be zero')
                self.assertEqual(digits[len(digits)-1], 1,
                    'First digit must be one')
                
    def test_incr_overflow_decimal(self):
        """
        Increment overflow

        Verify that incrementing a number at its maximum value by one
        wraps it back to zero, by informal proof

        """
        func = lambda x:10 # Simulated decimal number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            test_int = 9
            for iii in range(length-1):
                # Create an integer of all 9's
                test_int *= 10
                test_int += 9
            cbn = CustomBaseNumberF(length, func)
            cbn.set_digits_from_int(test_int)
            cbn.incr() # Increment the number past max value
            digits = cbn._digits
            for jjj in range(len(digits)-1):
                # Verify that every digit is zero 
                with self.subTest(length=length):
                    self.assertEqual(digits[jjj],0,'All digits must be zero')
                
    def test_set_digits_binary(self):
        """
        Setting of digits (using simulated binary number)

        Verify that method to set the digits of a number directly
        works correctly by informal proof

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            digits_test = (1,)*length
            cbn = CustomBaseNumberF(length, func, digits_test)
            digits = cbn._digits
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    self.assertEqual(digits[iii], digits_test[iii])

    def test_set_digits_binary_digit_negative(self):
        """
        Setting of digits to negative values

        Verify that any attempt to set a negative value on any
        digit of a number raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            digits_test = (-1,)*length
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberF(length, func, digits_test)

    def test_set_digits_binary_digit_exceed_max(self):
        """
        Setting of digits to exceed radix

        Verify that any attempt to set any digit past the maximum
        value defined by its radix raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            digits_test = (2,)*length
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberF(length, func, digits_test)

    def test_set_digits_binary_too_many(self):
        """
        Specifying too many digits during number creation

        Verify that any attempt to create a number with more
        digits than the declared digit length of the number
        raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            digits_test = (0,) * (length+1)
                # PROTIP: You need the parentheses around length+1,
                # because OPERATOR PRECEDENCE
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberF(length, func, digits_test)

    def test_set_digits_binary_too_few(self):
        """
        Specifying too few digits during number creation

        Verify that any attempt to create a number with less
        digits than the declared digit length of the number
        raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(2, self.DIGITS_MAX+1, self.DIGITS_STEP):
            digits_test = (-1,) * (length-1)
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberF(length, func, digits_test)

    def test_set_digits_binary_zero_length(self):
        """
        Specifying empty sequence as digits during number creation

        Verify that any attempt to create a number by specifying
        an empty sequence in place of actual digits raises a
        ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            digits_test = ()
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberF(length, func, digits_test)

    def test_set_digits_from_int_decimal(self):
        """
        Setting value from int (using simulated decimal number)

        Verify that the value of a number can be converted from
        an integer, by informal proof.

        """
        func = lambda x:10 # Simulate decimal number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            test_int = 9
            for iii in range(length-1):
                # Extend test_int with more 9's until it
                # has the same number of digits as length
                test_int *= 10
                test_int += 9
            cbn = CustomBaseNumberF(length, func)
            cbn.set_digits_from_int(test_int)
            digits = cbn._digits
            for iii in range(len(digits)):
                with self.subTest(length=length, iii=iii):
                    self.assertEqual(digits[iii], 9)
 
    def test_set_digits_from_int_decimal_too_large(self):
        """
        Setting excessively large value from int (simulated decimal)
        
        Verify that any attempt to set a value beyond the maximum
        range of the number raises an OverflowError

        """
        func = lambda x:10 # Simulated decimal number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            test_int = 10 ** length
                # The value of test_int should be always
                # one ahead of the max value
            cbn = CustomBaseNumberF(length, func)
            with self.subTest(length=length):
                with self.assertRaises(OverflowError):
                    cbn.set_digits_from_int(test_int)


class CustomBaseNumberPTests(unittest.TestCase):
    """
    Tests for Explicitly-defined Radix Custom-Base Numbers

    """
    DIGITS_MAX = 1000
    DIGITS_STEP = 249

    def test_len(self):
        """
        Output of len()

        Verify that len() returns the number of digits in the
        Custom-Base Number correctly, by informal proof.

        """
        func = lambda x:1 # Dummy zero-value number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (1,) * length # Dummy always-zero number
            cbn = CustomBaseNumberP(radxs)
            with self.subTest(length=length):
                self.assertEqual(len(cbn), length)

    def test_new_number_default_value(self):
        """
        Creation of a new number with default values

        Verify that a Custom-Base Number created with no initial
        digits has exactly zero value, by informal proof

        """
        func = lambda x:1 # Dummy number always has zero value
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (1,) * length # Dummy always-zero number
            cbn = CustomBaseNumberP(radxs)
            digits = cbn._digits
            for iii in range(len(digits)):
                with self.subTest(length=length, iii=iii):
                    self.assertEqual(digits[iii], 0)
                    
    def test_get_digits(self):
        """
        Retrieval of digits

        Verify that the method to return the digits of the number,
        get_digits(), does this correctly, by informal proof.

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (2,) * length # Simulated binary number
            test_int = 1
            for iii in range(length-1):
                # create an integer which is all 1's expressed in
                # binary
                test_int <<= 1
                test_int += 1
            cbn = CustomBaseNumberP(radxs)
            cbn.set_digits_from_int(test_int)
            digits = cbn.digits()
            ref = (1,) * length
            with self.subTest(length=length):
                self.assertEqual(digits, ref)

    def test_incr_zero_decimal(self):
        """
        Increment from zero 

        Verify that incrementing a zero-value number by one produces
        a value of exactly one, by informal proof.

        """
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (10,) * length # Simulated decimal number
            test_int = 0
            cbn = CustomBaseNumberP(radxs)
            cbn.incr() # Increment the number from 0 to 1
            digits = cbn.digits()
            for iii in range(len(digits)-2):
                # Verify that all digits except the least significant
                # are zeroes
                with self.subTest(length=length, iii=iii):
                    self.assertEqual(digits[iii], 0,
                        'Digits before least significant must be zero')
                self.assertEqual(digits[len(digits)-1], 1,
                    'First digit must be one')
 
    def test_incr_overflow_decimal(self):
        """
        Increment overflow

        Verify that incrementing a number at its maximum value by one
        wraps it back to zero, by informal proof.

        """
        func = lambda x:10 # Simulated decimal number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (10,) * length # Simulated decimal number
            test_int = 9
            for iii in range(length-1):
                # Create an integer of all 9's
                test_int *= 10
                test_int += 9
            cbn = CustomBaseNumberP(radxs)
            cbn.set_digits_from_int(test_int)
            cbn.incr() # Increment the number past max value
            digits = cbn._digits
            for jjj in range(len(digits)-1):
                # Verify that every digit is zero 
                with self.subTest(length=length):
                    self.assertEqual(digits[jjj],0,'All digits must be zero')
                
    def test_set_digits_binary(self):
        """
        Setting of digits (using simulated binary number)

        Verify that method to set the digits of a number directly
        works correctly by informal proof

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (2,) * length # Simulated binary number
            digits_test = (1,)*length
            cbn = CustomBaseNumberP(radxs, digits_test)
            digits = cbn._digits
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    self.assertEqual(digits[iii], digits_test[iii])

    def test_set_digits_binary_digit_negative(self):
        """
        Setting of digits to negative values

        Verify that any attempt to set a negative value on any
        digit of a number raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (2,) * length # Simulated binary number
            digits_test = (-1,)*length
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberP(radxs, digits_test)

    def test_set_digits_binary_digit_exceed_max(self):
        """
        Setting of digits to exceed radix

        Verify that any attempt to set any digit past the maximum
        value defined by its radix raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (2,) * length # Simulated binary number
            digits_test = (2,)*length
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberP(radxs, digits_test)

    def test_set_digits_binary_too_many(self):
        """
        Specifying too many digits during number creation

        Verify that any attempt to create a number with more
        digits than the declared digit length of the number
        raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (2,) * length # Simulated binary number
            digits_test = (0,) * (length+1)
                # PROTIP: You need the parentheses around length+1,
                # because OPERATOR PRECEDENCE
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberP(radxs, digits_test)

    def test_set_digits_binary_too_few(self):
        """
        Specifying too few digits during number creation

        Verify that any attempt to create a number with less
        digits than the declared digit length of the number
        raises a ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(2, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (2,) * length # Simulated binary number
            digits_test = (-1,) * (length-1)
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberP(radxs, digits_test)

    def test_set_digits_binary_zero_length(self):
        """
        Specifying empty sequence as digits during number creation

        Verify that any attempt to create a number by specifying
        an empty sequence in place of actual digits raises a
        ValueError

        """
        func = lambda x:2 # Simulated binary number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (2,) * length # Simulated binary number
            digits_test = ()
            for iii in range(len(digits_test)):
                with self.subTest(length=length,iii=iii):
                    with self.assertRaises(ValueError):
                        cbn = CustomBaseNumberP(radxs, digits_test)

    def test_set_digits_from_int_decimal(self):
        """
        Setting value from int (using simulated decimal number)

        Verify that the value of a number can be converted from
        an integer, by informal proof.

        """
        func = lambda x:10 # Simulate decimal number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (10,) * length # Simulated decimal number
            test_int = 9
            for iii in range(length-1):
                # Extend test_int with more 9's until it has
                # as many digits as defined in length
                test_int *= 10
                test_int += 9
            cbn = CustomBaseNumberP(radxs)
            cbn.set_digits_from_int(test_int)
            digits = cbn._digits
            for iii in range(len(digits)):
                with self.subTest(length=length, iii=iii):
                    self.assertEqual(digits[iii], 9)
 
    def test_set_digits_from_int_decimal_too_large(self):
        """
        Setting excessively large value from int (simulated decimal)
        
        Verify that any attempt to set a value beyond the maximum
        range of the number, from an integer, raises an OverflowError

        """
        func = lambda x:10 # Simulated decimal number
        for length in range(1, self.DIGITS_MAX+1, self.DIGITS_STEP):
            radxs = (10,) * length # Simulated decimal number
            test_int = 10 ** length
                # Value of test_int should be always one ahead of its max
            cbn = CustomBaseNumberP(radxs)
            with self.subTest(length=length):
                with self.assertRaises(OverflowError):
                    cbn.set_digits_from_int(test_int)

