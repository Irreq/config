#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: config.py
# Description: Irreq's Qtile Config File
# Author: irreq (irreq@protonmail.com)
# Date: 02/11/2021



# For every other function
import os
import sys

import socket  # To connect to pymetricsd.py daemon

from libqtile import bar, hook, pangocffi, layout, widget

from libqtile.command import lazy

from libqtile.config import Group, Key, Screen
from libqtile.config import EzClick as Click  # For macros on Logitech M570
from libqtile.config import EzKey  # To rebind keys on Deltaco DK440R

from libqtile.widget.base import _TextBox, ThreadPoolText
from libqtile.widget import KeyboardLayout

path = os.path.expanduser("~/github/programs/de")
sys.path.append(path)
from main import programs, program, launch

GROUPS = "asdfgzxcvbnm"

# Cosmetics
FONT = "PxPlus HP 100LX 10x11"
FONTSIZE = 11

# Keyboard
mod = "mod4"  # The 'Super' key
shift = "shift"
control = "control"
left, down, up, right = ("h", "j", "k", "l")  # Movement keys

def test():
    import time
    return str(time.time())

class Colors:
    bg = "#282828"
    highlight_bg = "#2596be"
    urgent_bg = "#ff0000"
    text = "#ffffff"
    inactive_text = "#555753"
    border_focus = "#354ae8"
    highlight_text = "#d3d7cf"


class MetricsListener(ThreadPoolText):
    def __init__(self, udp_ip="localhost", udp_port=28441, **kwargs):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.config = kwargs
        self.sock = False
        self.timeout_count = 0

        self.connect()

        if self.is_socket_closed(self.sock):
            self.sock = False

        super().__init__("Booting...".format(self.udp_ip, self.udp_port), **self.config)
        self.update_interval = 1


    def is_socket_closed(self, sock):
        try:
            # Will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # Socket is open and reading from it would block
        except ConnectionResetError:
            return True  # Socket was closed for some other reason
        except Exception as e:
            logger.exception("unexpected exception when checking if a socket is closed")
            return False
        return False


    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # [Errno 98] Address already in use, https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.udp_ip, self.udp_port))
        except Exception as e:
            print(e)
            self.sock = False

    def poll(self):
        if not self.is_socket_closed(self.sock):
            data = "Nothing received for %ds. Is pymetricsd.py running?" % (self.timeout_count * 5)
            self.sock.settimeout(5)
            try:
                # buffer size is 1024 bytes
                data, addr = self.sock.recvfrom(1024)
                data = data.decode("utf8")
                self.timeout_count = 0
            except:
                self.timeout_count += 1
            self.sock.settimeout(None)
            return data
        else:
            return "Socket Error"


class CustomBaseTextBox(_TextBox):
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
            int(self.bar.height / 2.0 - self.layout.height / 2.0) + 1 + self.text_shift,
        )
        self.drawer.draw(offsetx=self.offsetx, width=self.width)


hook.subscribe.hooks.add("prompt_focus")
hook.subscribe.hooks.add("prompt_unfocus")


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


def home_or_end(qtile, kk):
    from pynput.keyboard import Key, Controller
    import time

    keyboard = Controller()

    # Press and release  delay
    time.sleep(0.2)

    k = getattr(Key, kk)
    keyboard.press(k)
    keyboard.release(k)

keys = [
    # Move
    Key([mod], left, lazy.layout.left()),
    Key([mod], down, lazy.layout.down()),
    Key([mod], up, lazy.layout.up()),
    Key([mod], right, lazy.layout.right()),

    # Shuffle
    Key([mod, shift], left, lazy.layout.shuffle_left()),
    Key([mod, shift], down, lazy.layout.shuffle_down()),
    Key([mod, shift], up, lazy.layout.shuffle_up()),
    Key([mod, shift], right, lazy.layout.shuffle_right()),

    # Size
    Key([mod, control], left, lazy.layout.grow_left()),
    Key([mod, control], down, lazy.layout.grow_down()),
    Key([mod, control], up, lazy.layout.grow_up()),
    Key([mod, control], right, lazy.layout.grow_right()),

    # Audio
    Key([mod], "comma", lazy.spawn(program("vol_down"))),
    Key([mod], "period", lazy.spawn(program("vol_up"))),
    Key([mod], "minus", lazy.spawn(program("pause"))),

    # Start stuff
    Key([mod], "o", lazy.spawncmd()),  # Open menu
    Key([mod], "Return", lazy.spawn(program("terminal"))),

    # Stop stuff
    Key([mod, shift], "q", lazy.window.kill()),
    Key([mod, shift], "r", lazy.restart()),

    # Shortcuts to rebind 'home' & 'end' for Deltaco DK440R
    Key([mod], "Left", lazy.function(home_or_end, "home")),
    Key([mod], "Right", lazy.function(home_or_end, "end"))
]

groups = [Group(gname, label=gname.upper()) for gname in GROUPS]

# Handle groups, `mod` + key -> go to that group.
# `mod` & shift + key -> move window to group.
for g in groups:
    keys.extend([Key([mod], g.name, lazy.group[g.name].toscreen()),
                 Key([mod, shift], g.name, lazy.window.togroup(g.name))])

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

screens = [
    Screen(
        bottom=bar.Bar(
            [SuggestionPrompt(
                prompt=" > ",
                padding=2,
                foreground=Colors.highlight_text,
                cursor_color=Colors.highlight_text,
            ),
            widget.GroupBox(
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
            ),
            CustomWindowName(
                padding=20
            ),
            KeyboardLayout(
                font=FONT,
                fontsize=FONTSIZE,
                foreground=Colors.highlight_text,
                # func=test,
                configured_keyboards=["se", "se svdvorak"],
                update_interval=1,
                padding=20,
                ),
            MetricsListener(
                font=FONT,
                fontsize=FONTSIZE,
                foreground=Colors.highlight_text,
            ),
            ],
            FONTSIZE+0, # Bar height
            background=Colors.bg,
        ),
    ),
]

# Emulate function keys as 'super' + f*
fk = "python3 ~/github/programs/presskey ctrl+alt+f"
keys.extend([EzKey("M-" + str(i), lazy.spawn(fk+str(i))) for i in range(1,9)])

# For Logitech M570
mouse = [
    Click("8", lazy.spawn(program("terminal"))),  # Macro 2 = Open terminal
    Click("9", lazy.spawn(program("pause"))),  # Macro 1 = Open menu
    Click("M-9", lazy.window.kill()),  # 'Super' + Macro 1 = Kill window
    Click("M-4", lazy.spawn(program("vol_up"))),  # 'Super' + Wheel = increase volume
    Click("M-5", lazy.spawn(program("vol_down")))  # 'Super' + Wheel = derease volume
]

@hook.subscribe.client_new
def client_new(client):
    # Rules for new programs
    if client.name == 'Discord':
        client.togroup('d')
    elif client.name == 'Mozilla Firefox':
        client.togroup('s')
    elif client.name == 'Atom Dev':
        client.togroup('a')
    elif client.name == 'Volume Control':
        client.togroup('g')

@hook.subscribe.startup_once
def autostart():
    # Processes to start during boot:
    for p in ["keyboard", "terminal", "firefox", "pavucontrol"]:
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
