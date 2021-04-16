# -*- coding: utf-8 -*-
"""
Example module that uses colors.

We generate a random number between and color it depending on its value.
Clicking on the module will update it an a new number will be chosen.

Configuration parameters:
    format: Initial format to use
        (default 'Number {number}')

Format placeholders:
    {number} Our random number

Color options:
    color_high: number is 5 or higher
    color_low: number is less than 5
"""

# from random import randint
# import numpy as np
import time

EULER = 2.718281828459045235360287471352662497757

e = 2.718281828459045235360287471352662497757

# seed = e

seed = time.time()


def random(multiplier=69069, increment=1, modulus=2**16):
    """
    Linear Congruential Generator (LCG)

    NOTE:                   A linear congruential generator (LCG) is
                            an algorithm that yields a sequence of
                            pseudo-randomized numbers calculated with a
                            discontinuous piecewise linear equation.
                            This equation is defined as:
                            _________________________________________

                                     Xn+1 = (aXn + c) mod m
                            _________________________________________

                            Change the initial 'seed' if you want
                            something else. This program does not
                            require any secure randomness, that is
                            becuase the random values only determine
                            the behavior of the particles.

    ARGUMENTS:
        - multiplier        int() 0 < 'a' < 'm'

        - increment         int() 0 <= 'c' < 'm'

        - modulus           int() 0 < 'm'

    RETURNS:
        - float()           Random value between 0 and 1
    """

    global seed

    # Linear congruention
    seed = (multiplier * seed + increment) % modulus

    return seed / modulus


def uniform(low, high):
    """
    Generate a random value between low and high

    NOTE:                   low <= high

    ARGUMENTS:
        - low               float() Eg, '-0.89'

        - high              float() Eg, '8.23'

    RETURNS:
        - float()           low <= float() <= high
    """

    return abs(high-low) * random() + low


def ndistance(p1, p2):
    """
    Calculate eucleidian distance between two points in N-dimensional space

    NOTE:                   The two points must have the same number of
                            dimensions, thus having the same shape.
                            Points' dimension is the same as their index.
                            Eg, point a: (2, 4) has two dimensions.

    ARGUMENTS:
        - p1                list() Coordinates. Eg, [0.2, 4, ..., n-1, n]

        - p2                list() Coordinates. Eg, [2, -7, ..., n-1, n]

    RETURNS:
        - float()           Eucledidian distance between both points.
    """

    return sum([(p1[i] - p2[i])**2 for i in range(len(p1))])**0.5


def nonlinear_rectifier(x0, x, x1):
    """
    Non-Linear Rectifier (LCR)

    NOTE:                   A non-linear rectifier (LCR) is
                            an algorithm that yields a input-value
                            rectified between two other values calculated
                            by relative distance. This equation is defined as:
                            ________________________________________________

                                         x1 - x0
                               --------------------------- + x0
                                      -e*(2x - (x1 + x0))
                                1 + e     --------------
                                             (x1 - x0)

                            ________________________________________________

                            If x is not between x0 and x1, x will be valued
                            closest to that value. This will create.
                            If x0<x<x1, x will kind of keep its value apart
                            from minor changes. If not x0<x<x1, x will be
                            fit within boundaries. It is bascically the
                            sigmoid function, but instead of: x -> 0<x<1
                            it is: x -> x0<x<x1

    ARGUMENTS:
        - x0                float() x0<x1

        - x                 float() The value to rectifiy.

        - x1                float() x0<x1

    RETURNS:
        - float()           x0<x<x1

    TODO:
    desmos.com:
    \frac{b-a}{1+e^{-e\cdot\frac{2x-\left(b+a\right)}{\left(b-a\right)}}}+a
    """

    return (x1-x0) / (1 + e**-(e*(2*x-(x1+x0))/(x1-x0))) + x0


def sigmoid(x):
    "Returns a sigmoid value"
    try:
        return 1.0 / (1.0 + EULER**-x)
    except OverflowError:
        print(x)
        return 1.0


def chaos(x):
    "Returns a chaotic value"
    return 3.9 * x * (1-x)


def sub_call():
    with open('/home/irreq/.config/i3status/py3status/lol.txt', 'r') as f:
        data = f.readlines()
        # data = " ".join()
        f.close()

    return "lol"


def get_text():
    # " " = 32
    # for lowercase + 32
    # "A" = 65
    # "Z" = 90
    text = chr(int(uniform(65, 90)))

    for i in range(int(uniform(3,10))):
        text += chr(int(uniform(97, 122)))

    text = str(int(uniform(97, 122))) + " " + text
    return text

class Py3status:
    # format = 'Number {number}'
    format = '{number}'

    def ok(self):

        # foo()
        # number = randint(8, 19)
        # number = sub_call()+str(number)
        full_text = self.py3.safe_format(self.format, {'number': get_text()})

        # if number < 5:
        #     color = self.py3.COLOR_LOW
        # else:
        #     color = self.py3.COLOR_HIGH

        return {
            'full_text': full_text,
            # 'color': color,
            # 'cached_until': self.py3.CACHE_FOREVER
            'cached_until': self.py3.time_in(5)
        }

    def on_click(self, event):
        # by defining on_click pressing any mouse button will refresh the
        # module.
        pass
