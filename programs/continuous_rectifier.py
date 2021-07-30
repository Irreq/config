#!/usr/bin/python3
# -*- coding: utf-8 -*-

e = 2.71828182846

def continuous_rectifier(x0, x, x1):
    """
    Theoretical Continuous Analog Rectifier For Artificial Neural Networks.

    NOTE:           The algorithm yields an input-value rectified
                    between two other values calculated by the relative
                    distance distance. This equation is defined as:
                    ______________________________________________________

                                            x1 - x0
                    f(x0, x, x1) = ------------------------ + x0
                                           -(2*x - x1 - x0)
                                            ---------------
                                   1 + (5e)     x1 - x0
                    ______________________________________________________
                    If x is not between x0 and x1, x will be valued
                    closest to that value. This will create.
                    If x0<x<x1, x will kind of keep its value apart
                    from minor changes. If not x0<x<x1, x will be
                    fit within boundaries. It is basically the
                    sigmoid function, but instead of: x -> 0<x<1
                    it is: x -> x0<x<x1

                    Having k = 16 gives equal deviation among numbers,
                    but falsely increases values within boundaries, but
                    fixes for smaller error.
                    Having k = 4\pi gives a smaller deviation
                    while having k = 8 gives smallest
    ARGUMENTS:
        - x0                float() The lower boundary (min).
        - x                 float() The value to rectify.
        - x1                float() The upper boundary (max).
    RETURNS:
        - float()           x0 <= x <= x1
    """

    return (x1 - x0) / (1 + (5*e) ** -((2*x - x1 - x0) / (x1 - x0))) + x0

if __name__ == "__main__":
    a = -10
    b = 10
    c = 14

    result = continuous_rectifier(a, c, b)
    print(result)
