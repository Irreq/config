import os
from random import choice

path = "/home/irreq/Pictures/Wallpapers/"


class Py3status:
    format = "{pic_id}"

    def ok(self):
        (_, _, filenames) = next(os.walk(path))
        try:
            file = choice(filenames)
            status = file
            status = ""
            query = "feh --no-fehbg --bg-scale '{}'".format(path + file)
            os.system(query)
        except IndexError:
            status = "Empty directory"



        status = self.py3.safe_format(self.format, {'pic_id': status})

        return {
            'full_text': status,
            'cached_until': self.py3.time_in(600)
        }

        def on_click(self, event):
            # by defining on_click pressing any mouse button will refresh the
            # module.
            pass
