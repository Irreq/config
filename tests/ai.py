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


class thresholds:
    # Good -> Bad
    battery = [100, 0]
    temperature = [20, 80]

ENERGY = 3
PLEASANTNESS = 7

mood = moods[ENERGY][PLEASANTNESS]
print(mood)
