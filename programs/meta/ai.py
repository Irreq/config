import numpy as np
import matplotlib.pyplot as plt

class Mood():
    # Pleasantness X Energy
    moods = """
    enraged panicked stressed jittery shocked surprised upbeat festive exhilarated ecstatic
    livid furious frustrated tense stunned hyper cheerful motivated inspired elated
    fuming frightened angry nervous restless energized lively enthusiastic optimistic excited
    anxious apprehensive worried irritated annoyed pleased happy focused proud thrilled
    repulsed troubled concerned uneasey peeved pleasant joyful hopeful playful blissful
    disgusted glum disappointed down apathetic easy easygoing content loving fulfilled
    pessimistic morose discouraged sad bored calm secure satsified grateful touched
    alienated miserable lonely disheartened tired relaxed chill restful blessed balanced
    despondent depressed sullen exhausted fatigued mellow thoughtful peaceful comfy carefree
    despair hopeless desolate spent drained sleepy complacent tranquil cozy serene
    """

    def __init__(self):
        pass

    def get_moods(self):
        # Return a 10x10 list containing all moods
        return [i.split() for i in self.moods.split("\n")[1:-1]]
M = Mood()
moods = M.get_moods()

e = 2.71828182846
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

                            having k = 16 gives equal deviation among numbers,
                            but falsely increases values within boundaries, but
                            fixes for smaller error.
                            having k = 4\pi gives a smaller deviation
                            while having k = 8 gives smallest
    ARGUMENTS:
        - x0                float() x0<x1
        - x                 float() The value to rectifiy.
        - x1                float() x0<x1
    RETURNS:
        - float()           x0<x<x1
    TODO:
    desmos.com:
    \frac{b-a}{1+e^{-e\cdot\frac{2x-\left(b+a\right)}{\left(b-a\right)}}}+a

    \frac{b-a}{1+\frac{1}{\left(4\pi\right)^{\frac{2x-b-a}{b-a}}}}+a
    """

    # 15.15426224^x - 1
    # -----------------
    # 15.15426224^x + 1


    return (x1-x0) / (1 + e**-(e*(2*x-(x1+x0))/(x1-x0))) + x0

def nonlinear_rectifier_anti_derivative(c, x, d):
    """x0 = -1, x1 = 1

    desmos.com:
    \frac{2\cdot\ln\left(\left|c^{dx}+1\right|\right)}{\ln\left(c\right)\cdot d}-x

    \frac{2\ln\left(\left|a^{bx}+1\right|\right)-\ln\left(\left|a^{bx}\right|\right)}{b\ln\left(a\right)}

    \frac{c^{dx}-1}{c^{dx}+1}
    """

    # return 2 * np.log(abs(c**(d*x)+1)) / (np.log(c) * d) - x
    return (2 * np.log(abs(c**(d*x)+1)) - np.log(abs(c**(d*x)))) / (d * np.log(c))

def my_func(x, k=e**e):
    return (k**x-1)/(k**x+1)


def original(x):
    if x >= 1.0:
        return 1.0

    else:
        return x
def f(k):

    # ks = np.linspace(6,36,100)
    # result = []
    #
    # for x in np.linspace(0,1,1000):
    #     penalty = abs(my_func(x, k=14) - original(x))
    #     result.append(penalty)
    #     # print(original(x))
    result = {}

    for c in np.linspace(9,17,80):
        lst = [abs(my_func(x, k=c) - original(x)) for x in np.linspace(0,2,6000)]
        ke = sum(lst)/len(lst)
        result[ke]=c

    # result = {sum([abs(my_func(x, k=c) - original(x)) for x in np.linspace(0,100,20000)]):c for c in np.linspace(14.59,14.61,200)}

    small = min(result.keys())
    value = result[small]
    print(value)
    # print(sum(result))
    # plt.plot(result)
    # plt.show()


def penalty():
    return

def test(a=-1, x=2, b=1):
    class thresholds:
        # Good -> Bad
        battery = [100, 0]
        temperature = [20, 80]

    ENERGY = 3
    PLEASANTNESS = 7

    mood = moods[ENERGY][PLEASANTNESS]
    print(mood)
    return
if __name__ == "__main__":
    c = 2
    d = 0.7
    x = 0
    # result = nonlinear_rectifier_anti_derivative(c, x, d)

    result = f(x)
    # print(result)
    c = 14.59321608040201
    c = 14.592405063291139
    c = 14.593243744041
    # c =

    # for c in (c, 14.59321608040201):
    #     lst = [abs(my_func(x, k=c) - original(x)) for x in np.linspace(0,10,20000)]
    #     ke = sum(lst)/len(lst)
    #     print(c, ke)
    # result = [abs(my_func(x, k=c) - original(x)) for x in np.linspace(0,200,40000)]
    # # result = []
    #
    # # for i, x in enumerate(np.linspace(0,100,20000)):
    # #     penalty = abs(my_func(x, k=c) - original(x))
    # #     result.append(penalty)
    # #     # if i%100==0:
    # #     #     print(penalty, x)
    # print(sum(result)/len(result))
