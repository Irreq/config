import os
from random import choice

path = "/home/irreq/Pictures/Wallpapers/"
(_, _, filenames) = next(os.walk(path))

try:
    wallpaper = choice(filenames)
    file = wallpapers + wallpaper

    status = wallpaper
    query = "feh --no-fehbg --bg-scale '{}'".format(file)
    os.system(query)
except IndexError:
    status = "Empty directory"

print(status)
