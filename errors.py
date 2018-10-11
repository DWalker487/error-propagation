from __future__ import division, print_function
try:
    import numpy as math
except ImportError:
    import math


class Value(object):
    """ Basic class intended for e.g. ipython use defining a value
    with associated error for easy error propagation with constants
    and/or other Values. Floor division is not defined. Bitwise addition
    (& operator) gives the weighted mean of two values, equivalent to
    combining two measurements.

    Initialisation:
          x = Value(value, error)

    Example use:
          x = Value(1,3)         # Initialises value 1 +/- 2
          y = Value(2,4)         # Initialises value 2 +/- 4
          z = Value(1,3)         # Initialises value 1 +/- 2

          Expression -> Output
          -------------------------------------
          2*x        -> Value(2,6)
          x**2       -> Value(1,6)
          x + y      -> Value(3,5)
          x - y      -> Value(-1,5)
          x + 4      -> Value(5,3)
          x - 4      -> Value(-3,3)
          x*y        -> Value(2,7.21110255093)
          x/y        -> Value(0.5,1.80277563773)
          x == z     -> True
          x == y     -> False
          x == x     -> True
          x & y      -> Value(1.36, 2.4)

          >> x.percent_error
               300.0

    It is also possible to use the functionality for numpy arrays. If numpy
    is not available this functionality is not loaded.
    For example:
       x = Value(np.array([1,2]),np.array([3,2]))   # Initialises Values [1,2]
                                                    # Initialises Errors [3,2]
       x*2 -> Value([2,4],[6,4])
    and so on.
    """
    def __init__(self, value, error):
        try:  # Will not work if numpy is not loaded
            if isinstance(value, math.ndarray):
                assert len(value) == len(error)
                self._is_array = True
            else:
                raise AttributeError
        except AttributeError:
            self._is_array = False
        except (AssertionError, TypeError):
            txt = "Incompatible values and errors in {0}. "
            txt += "Check dimensions/types!"
            raise Exception(txt.format((value, error)))
        self._value = value
        self._error = error
        self._percent_error = self.__do_percent(error, value)

    # Set up properties
    @property
    def value(self):
        return self._value

    @property
    def error(self):
        return self._error

    @property
    def percent_error(self):
        """The percent property"""
        return self._percent_error

    # Aliases for easy use
    @property
    def err(self):
        return self._error

    @property
    def val(self):
        return self._val

    @property
    def percent(self):
        """Alias for the percent property"""
        return self._percent_error

    @property
    def pc(self):
        """Alias for the percent property"""
        return self._percent_error

    # Set up setters for self consistency, particularly with errors
    @value.setter
    def value(self, new_value):
        if self._is_array:
            assert len(new_value) == len(self.error)
        self._value = new_value
        self._percent_error = self.__do_percent(self.error, self._value)

    @error.setter
    def error(self, new_error):
        if self._is_array:
            assert len(new_error) == len(self.value)
        self._error = new_error
        self._percent_error = self.__do_percent(self._error, self.value)

    def __do_percent(self, error, value):
        return error/value*100

    def __add__(self, other):
        """ Addition operator. Errors propagate with other Values.
        Considers floats/ints as constants with error == 0
        """
        try:
            new_value = self.value + other.value
            new_error = math.sqrt(self.error**2 + other.error**2)
        except AttributeError:
            new_value = other + self.value
            new_error = self.error
        return Value(new_value, new_error)

    def __radd__(self, other):
        """ Addition operator. Errors propagate with other Values.
        Considers floats/ints as constants with error == 0
        """
        try:
            new_value = self.value + other.value
            new_error = math.sqrt(self.error**2 + other.error**2)
        except AttributeError:
            new_value = other + self.value
            new_error = self.error
        return Value(new_value, new_error)

    def __sub__(self, other):
        """ Subtraction operator. Errors propagate with other Values.
        Considers floats/ints as constants with error == 0
        """
        try:
            new_value = self.value - other.value
            new_error = math.sqrt(self.error**2 + other.error**2)
        except AttributeError:
            new_value = self.value - other
            new_error = self.error
        return Value(new_value, new_error)

    def __mul__(self, other):
        """ Multiplication operator. Errors propagate with other Values.
        Considers floats/ints as constants with error == 0
        """
        try:
            # Value*Value case
            new_value = self.value*other.value
            new_error = new_value*math.sqrt((self.error/self.value)**2 +
                                            (other.error/other.value)**2)
        except AttributeError:
            # Value*constant case
            new_value = self.value*other
            new_error = self.error*other
        return Value(new_value, new_error)

    def __rmul__(self, other):
        """ Multiplication operator. Errors propagate with other Values.
        Considers floats/ints as constants with error == 0
        """
        try:
            # Value*Value case
            new_value = self.value*other.value
            new_error = new_value*math.sqrt((self.error/self.value)**2 +
                                            (other.error/other.value)**2)
        except AttributeError:
            # Value*constant case
            new_value = self.value*other
            new_error = self.error*other
        return Value(new_value, new_error)

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        """ Division operator. Errors propagate with other Values.
        Considers floats/ints as constants with error == 0
        """
        try:
            # Value/Value case
            new_value = self.value/other.value
            new_error = new_value*math.sqrt((self.error/self.value)**2 +
                                            (other.error/other.value)**2)
        except AttributeError:
            # Value/constant case
            new_value = self.value/other
            new_error = self.error/other
        return Value(new_value, new_error)

    def __neg__(self):
        return Value(-self.value, self.error)

    def __pos__(self):
        return Value(self.value, self.error)

    def __abs__(self):
        if self.value < 0:
            return Value(-self.value, self.error)
        return Value(self.value, self.error)

    def __pow__(self, other):
        """ Power operator. Errors propagate with other Values.
        Considers floats/ints as constants with error == 0

        Not supported - float/int**Value type operations
        """
        try:
            # Value**Value case
            new_value = self.value**other.value
            new_error = math.sqrt((other.value*self.value**(other.value-1)*self.error)**2
                                  +(new_value*math.log(self.value)*other.error)**2)
        except AttributeError:
            # Value**constant case
            new_value = self.value**other
            new_error = new_value*self.error*other/self.value
        return Value(new_value, new_error)

    def __eq__(self, other):
        """ Equality operator. Checks that BOTH the value and the error are
        the same in both objects.
        """
        return (self.value == other.value and self.error == other.error)

    def __str__(self):
        return "{0} +/- {1}".format(self.value, self.error)

    def __repr__(self):
        return "({0},{1})".format(self.value, self.error)

    def __and__(self, other):
        """ Weighted mean operator. Equivalent to combining two measurements
        of the same thing with associated errors"""
        self_wgt = 1/self.error**2
        other_wgt = 1/other.error**2
        wgt_sum = self_wgt + other_wgt
        new_value = (self_wgt*self.value+other_wgt*other.value)/wgt_sum
        new_error = math.sqrt(1/wgt_sum)
        return Value(new_value, new_error)


def std_dev_difference(value1, value2):
    """ Returns difference in terms of standard deviations between the two
    input values."""
    diff = value1-value2
    return math.abs(diff.value/diff.error)


def chi_squared(value1, value2):
    """Returns chi squared between two Value objects"""
    ratio = value1/value2
    return sum((1-ratio.value)**2/ratio.error**2)


def chi_squared_dof(value1, value2):
    """Returns chi squared per degree of freedom between two Value objects"""
    chisq = chi_squared(value1, value2)
    dof = 1.
    if value1._is_array:
        dof = len(value1.value)
    return chisq/dof


if __name__ == "__main__":
    x = Value(1, 3)
    y = Value(2, 4)
    z = Value(1, 3)

    # Quick tests
    assert 2*x == Value(2, 6)
    assert x**2 == Value(1, 6)
    assert x + y == Value(3, 5)
    assert x - y == Value(-1, 5)
    assert x + 4 == Value(5, 3)
    assert x - 4 == Value(-3, 3)
    # .lt. for floating point error
    tolerance = 0.000000001
    assert abs((x*y - Value(2, 7.21110255093)).value) < tolerance
    assert abs((x*y).error - 7.21110255093) < tolerance
    assert abs((x/y - Value(0.5, 1.80277563773)).value) < tolerance
    assert abs((x/y).error - 1.80277563773) < tolerance
    assert (x & x).value == 1
    assert abs((x & x).error - 3./math.sqrt(2)) < tolerance
    # comparitors
    assert x == x
    assert x == z
    assert not x == y
    print("Basic tests complete")
