import os
from random import choice

path = "/home/irreq/Pictures/Wallpapers/"

def set_wallpaper():
    (_, _, filenames) = next(os.walk(path))
    try:
        name = choice(filenames)
        query = "feh --no-fehbg --bg-scale '{}'".format(path + name)
        os.system(query)
        return name
    except IndexError:
        return "Empty directory"
