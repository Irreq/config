#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: main.py
# Description: Irreq's Qtile Config File
# Author: irreq (irreq@protonmail.com)
# Date: 02/11/2021

"""
USER NOTICE

This is only the config for the 'window-manager' settings, eg. keybinds.
All other stuff like statusbar are located in a different file. See down below.

"""

from libqtile import bar, hook, pangocffi, layout, widget

from libqtile.command import lazy

from libqtile.config import Group, Key, Screen

# For macros on Logitech M570
from libqtile.config import EzClick as Click

from libqtile.widget.base import ORIENTATION_HORIZONTAL
from libqtile.widget.base import _TextBox as BaseTextBox


# For every other function
import os, sys
path = os.path.expanduser("~/github/programs/de")
sys.path.append(path)

try:
    from main import programs, update_status_wrapper, launch, test_tts
except ModuleNotFoundError:
    print("[USER] module 'main' could not be found, does it exist?")

try:
    from main import program_ul as program
except Exception as e:
    print(e)
    def program(p):
        if p in programs:
            return programs[p]

# CONFIG

MOD = "mod4"  # The 'Super' key, aka Windows-key
FONT = "PxPlus HP 100LX 10x11"
FONTSIZE = 11


class Colors:
    bg = "#282828"
    highlight_bg = "#2596be"
    urgent_bg = "#ff0000"
    text = "#ffffff"
    inactive_text = "#555753"
    border_focus = "#354ae8"
    highlight_text = "#d3d7cf"



# Qtile specifics

class CustomBaseTextBox(BaseTextBox):
    defaults = [
        ("text_shift", 0, "Shift text vertically"),
    ]

    def __init__(self, text=" ", width=bar.CALCULATED, **config):
        super().__init__(text, width, **config)
        self.add_defaults(CustomBaseTextBox.defaults)

    # exact copy of original code, with Y adjustment
    def draw(self):
        # if the bar hasn't placed us yet
        if self.offsetx is None:
            return
        self.drawer.clear(self.background or self.bar.background)
        self.layout.draw(
            self.actual_padding or 0,
            int(self.bar.height / 2.0 - self.layout.height / 2.0) + 1 + self.text_shift,  # here
        )
        self.drawer.draw(offsetx=self.offsetx, width=self.width)


class DisplayOutputFromFunctionEverySecond(CustomBaseTextBox):
    orientations = ORIENTATION_HORIZONTAL
    defaults = [
        ("active_color", "ff4000", "Color of active indicator"),
        ("inactive_color", "888888", "Color of inactive indicator"),
        ("update_interval", 1, "Update interval in seconds"),
    ]

    def __init__(self, *func_args, function: "name of function", **config):
        # text is set to '' as there is no initial output
        super().__init__(text='', **config)
        self.add_defaults(DisplayOutputFromFunctionEverySecond.defaults)
        self.func_args = func_args
        self.function = function
        # This function will be called every "1" second but change to fit your needs
        self.update()
        if self.padding is None:
            self.padding = 4

    def update(self):
        output = str(self.function(self.func_args))

        output_color = self.active_color

        redraw = True
        redraw_bar = False

        old_width = None
        if self.layout:
            old_width = self.layout.width

        # Checks that color haven't changed
        if output_color != self.foreground:
            redraw = True
            self.foreground = output_color

        # No need to update if nothing changed
        if output != self.text:
            redraw = True
            self.text = output

        if not self.configured:
            return

        if self.layout.width != old_width:
            redraw_bar = True

        if redraw_bar:
            self.bar.draw()
        elif redraw:
            self.draw()

    def timer_setup(self):
        self.timeout_add(self.update_interval, self._auto_update)

    def _auto_update(self):
        self.update()
        self.timeout_add(self.update_interval, self._auto_update)


hook.subscribe.hooks.add("prompt_focus")
hook.subscribe.hooks.add("prompt_unfocus")


# Two 'programs' here:

class SuggestionPrompt(widget.Prompt):

    max_suggestions = 10
    available = []
    current_query = programs
    chosen = ""

    separator = " "

    def startInput(self, *a, **kw):  # noqa: N802
        hook.fire('prompt_focus')
        return super().startInput(*a, **kw)

    def flush(self):
        if self.chosen != "":
            self.user_input = self.chosen

        self.chosen = ""
        self.current_query = programs

    def _unfocus(self):
        hook.fire('prompt_unfocus')
        self.flush()
        return super()._unfocus()

    def _update(self):
        if self.active:

            self.text = self.archived_input or self.user_input

            self.available = [k for k in self.current_query.keys() if self.text in k]
            self.available.sort()

            cursor = pangocffi.markup_escape_text(" ")

            if self.cursor_position < len(self.text):
                self.chosen = ""

                txt1 = self.text[:self.cursor_position]
                txt2 = self.text[self.cursor_position]
                txt3 = self.text[self.cursor_position + 1:]
                for text in (txt1, txt2, txt3):
                    text = pangocffi.markup_escape_text(text)
                txt2 = self._highlight_text(txt2)
                self.text = "{0}{1}{2}{3}".format(txt1, txt2, txt3, cursor)

            # Will display the alternatives as suggestions
            elif len(self.text) + 1 <= self.cursor_position <= len(self.text) + len(self.available):
                self.chosen = self.available[int(self.cursor_position-len(self.text)-1)]

            else:
                self.text = pangocffi.markup_escape_text(self.text)
                self.text += self._highlight_text(cursor)

            if self.chosen != "":
                self.text = self.chosen


            self.text = self.display + self.text

            if self.available:
                self.text += " | " + f"{self.separator}".join(self.available[:self.max_suggestions]) + " | "

        else:
            self.text = ""
        self.bar.draw()

    def _send_cmd(self):
        """Parse the omitted query to find specific things"""
        self.flush()
        separate = self.user_input.split()
        if separate[0] in self.current_query:
            tmp = self.current_query[separate[0]]
            if len(separate) > 1:
                if "QUERY" in tmp:
                    tmp = tmp.replace("QUERY", "+".join(separate[1:]))
                else:
                    tmp += " "+" ".join(separate[1:])

                if "sudo" in tmp:
                    tmp = "{} | {}".format(self.current_query["terminal"], tmp)
            self.user_input = tmp

        self.callback = launch
        try:
            super()._send_cmd()

        except Exception:
            self._unfocus()

    def _cursor_to_left(self):
        # Move cursor to left, if possible
        if self.cursor_position:
            self.cursor_position -= 1
        else:
            self._alert()

    def _cursor_to_right(self):
        # move cursor to right, if possible
        command = self.archived_input or self.user_input

        if self.cursor_position < len(command) + len(self.available):
            self.cursor_position += 1
        else:
            self._alert()


class CustomWindowName(widget.WindowName):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.visible = True

    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)
        hook.subscribe._subscribe("prompt_focus", self.hide)
        hook.subscribe._subscribe("prompt_unfocus", self.show)

    def show(self):
        self.visible = True
        self.update()

    def hide(self):
        self.visible = False
        self.update()

    def update(self, *args):
        if self.visible:
            super().update(*args)
        else:
            self.text = ''
            self.bar.draw()


groups = [Group(gname, label=gname.upper()) for gname in "asdfgzxcvbnm"]

@hook.subscribe.client_new
def client_new(client):
    if client.name == 'discord':
        client.togroup('d')

    elif client.name == 'Mozilla Firefox':
        client.togroup('s')

    elif client.name == 'Atom Dev':
        client.togroup('a')


def user_keymap(mod, shift, control, alt):
    """Generate keymap for operations"""
    for g in groups:
        yield mod + g.name, lazy.group[g.name].toscreen()
        yield mod + shift + g.name, lazy.window.togroup(g.name)

    # VIM keybinds
    yield mod + "h", lazy.layout.left()
    yield mod + "j", lazy.layout.down()
    yield mod + "k", lazy.layout.up()
    yield mod + "l", lazy.layout.right()

    # yield mod + "n", lazy.layout.normalize()

    yield mod + shift + "h", lazy.layout.shuffle_left()
    yield mod + shift + "j", lazy.layout.shuffle_down()
    yield mod + shift + "k", lazy.layout.shuffle_up()
    yield mod + shift + "l", lazy.layout.shuffle_right()

    yield mod + control + "h", lazy.layout.grow_left()
    yield mod + control + "j", lazy.layout.grow_down()
    yield mod + control + "k", lazy.layout.grow_up()
    yield mod + control + "l", lazy.layout.grow_right()

    # Audio
    yield mod + "comma", lazy.spawn(program("vol_down"))
    yield mod + "period", lazy.spawn(program("vol_up"))
    yield mod + "minus", lazy.spawn(program("pause"))

    # Start stuff
    yield mod + "o", lazy.spawncmd() # Open menu
    yield mod + "y", lazy.function(test_tts) # Launch SAM assistant
    yield mod + "u", lazy.spawn(program("gesture_audio"))
    yield mod + "Return", lazy.spawn(program("terminal"))
    yield mod + "p", lazy.window.toggle_fullscreen()

    # Stop stuff
    yield mod + shift + "q", lazy.window.kill()
    yield mod + shift + "r", lazy.restart()


def make_keymap(user_map):
    result = []

    class KeyCombo:
        def __init__(self, mods, key):
            self._mods = mods
            self._key = key

    class KeyMods:
        def __init__(self, mods):
            self._mods = set(mods)

        def __add__(self, other):
            if isinstance(other, KeyMods):
                return KeyMods(self._mods | other._mods)
            else:
                return KeyCombo(self._mods, other)

    for k, cmd in user_map(
        KeyMods({'mod4'}),
        KeyMods({'shift'}),
        KeyMods({'control'}),
        KeyMods({'mod1'}),
    ):
        if isinstance(k, str):
            mods = set()
        elif isinstance(k, KeyCombo):
            mods = k._mods
            k = k._key
        else:
            continue

        if 'lock' in mods:
            continue

        result.append(Key(list(mods), k, cmd))

    return result


keys = make_keymap(user_keymap)

layouts = [
    layout.Columns(border_focus_stack=0, border_width=0),
]

widget_defaults = dict(
    font=FONT,
    fontsize=FONTSIZE,
    padding=0,
    padding_x=0,
    padding_y=0,
    margin=0,
    margin_x=0,
    margin_y=0,
    foreground=Colors.text,
    center_aligned=True,
    markup=False,
)


def create_widgets():
    yield SuggestionPrompt(
        prompt=" > ",
        padding=2,
        foreground=Colors.highlight_text,
        cursor_color=Colors.highlight_text,
    )
    yield widget.GroupBox(
        disable_drag=True,
        hide_unused=True,
        use_mouse_wheel=False,
        padding_x=4,
        padding_y=0,
        margin_y=4,
        spacing=0,
        borderwidth=0,
        highlight_method="block",
        urgent_alert_method="block",
        rounded=True,
        active=Colors.text,
        inactive=Colors.inactive_text,
        urgent_border=Colors.urgent_bg,
        this_current_screen_border=Colors.highlight_bg,
        fontsize=FONTSIZE,
        font=FONT,
    )
    yield CustomWindowName(
        padding=20
    )
    yield DisplayOutputFromFunctionEverySecond(
        function=update_status_wrapper,
        active_color=Colors.highlight_text,
        inactive_color=Colors.inactive_text,
    )


screens = [
    Screen(
        bottom=bar.Bar(
            list(create_widgets()),
            FONTSIZE+0, # bar height
            background=Colors.bg,
        ),
    ),
]



# For Logitech M570
mouse = [
    Click("8", lazy.spawn(program("terminal"))),  # Macro 2 = Open terminal
    Click("9", lazy.spawn(program("pause"))),  # Macro 1 = Open menu
    Click("M-9", lazy.window.kill()),  # 'Super' + Macro 1 = Kill window
    Click("M-4", lazy.spawn(program("vol_up"))),
    Click("M-5", lazy.spawn(program("vol_down")))
]

@hook.subscribe.startup_once
def autostart():

    # Just add process to start on boot:
    for p in ["keyboard", "terminal", "firefox"]:
        launch(program(p))


dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
# bring_front_click = True
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = "urgent"
wmname = "Qtile"
