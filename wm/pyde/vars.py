test = True

def make_correct(string, length, suffix="", filler="0"):
    difference = length-len(string)
    return string[:length] + filler*difference*(difference >= 0) + suffix

def log(event):
    print(event)
