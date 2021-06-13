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

m = moods[0][-1]

print(m)
