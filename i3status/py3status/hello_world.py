# # -*- coding: utf-8 -*-
# """
# Example module that uses colors.
#
# We generate a random number between and color it depending on its value.
# Clicking on the module will update it an a new number will be chosen.
#
# Configuration parameters:
#     format: Initial format to use
#         (default 'Number {number}')
#
# Format placeholders:
#     {number} Our random number
#
# Color options:
#     color_high: number is 5 or higher
#     color_low: number is less than 5
# """
#
# from random import randint
#
#
# class Py3status:
#     # format = 'Number {number}'
#     format = '{number}'
#
#     def random(self):
#         number = randint(0, 9)
#         full_text = self.py3.safe_format(self.format, {'number': number})
#
#         # if number < 5:
#         #     color = self.py3.COLOR_LOW
#         # else:
#         #     color = self.py3.COLOR_HIGH
#
#         return {
#             'full_text': full_text,
#             # 'color': color,
#             # 'cached_until': self.py3.CACHE_FOREVER
#             'cached_until': self.py3.time_in(1)
#         }
#
#     def on_click(self, event):
#         # by defining on_click pressing any mouse button will refresh the
#         # module.
#         pass
