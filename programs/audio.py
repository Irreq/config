#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Welcome to the simple audio controller

Maintainers:
- Irreq irreq@protonmail.com

Commands:
toggle   - Switch between play/pause
pause    - Pause playing audio
play     - Play paused audio
stop     - Stop playing audio
next     - Skip playing audio
previous - Play previous audio
mute     - Mute audio
unmute   - Unmute audio
up       - Increase volume by 5%
down     - Decrease volume by 5%
panic    - Mute and pause all streams

Example:
python3 audio.py next
"""

import os
import sys
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from subprocess import call, DEVNULL

DIRECTORY = "/tmp/AudioControl"

# Initial check
if not os.path.isdir(DIRECTORY):
    os.makedirs(DIRECTORY)
    if not os.path.isdir(DIRECTORY+'/players'):
        os.makedirs(DIRECTORY+'/players')
    if not os.path.isdir(DIRECTORY+'/paused-players'):
        os.makedirs(DIRECTORY+'/paused-players')
    if not os.path.isfile(DIRECTORY+'/driver'):
        with open(DIRECTORY+'/driver', 'a'):
            os.utime(DIRECTORY+'/driver', None)
        # with open(DIRECTORY+'/driver', 'w') as f:
        #     f.write("ALSA")
        #     f.close()


# Set this to match your sound card driver
DRIVER = "ALSA"

players = []
DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()


CONTROLS = {
    "ALSA": {
        "mute": "amixer set Master -q mute",
        "unmute": "amixer set Master -q unmute",
        "up": "amixer set Master -q 5%+",
        "down": "amixer set Master -q 5%-"
    },
}



def do_nothing(*args, **kwargs):
    pass


def get_player_name(i, player):
    if i.startswith("org.mpris.MediaPlayer2."):
        return i[len("org.mpris.MediaPlayer2."):]
    else:
        return player.Get('org.mpris.MediaPlayer2',
                          'DesktopEntry',
                          dbus_interface='org.freedesktop.DBus.Properties')


def mute():
    os.system(CONTROLS[DRIVER]["mute"])


def unmute():
    os.system(CONTROLS[DRIVER]["unmute"])


def up():
    os.system(CONTROLS[DRIVER]["up"])


def down():
    os.system(CONTROLS[DRIVER]["down"])


def panic():
    mute()
    pause()


def pause():
    player_names = []
    for i in players:
        player = bus.get_object(i, '/org/mpris/MediaPlayer2')
        player_status = player.Get('org.mpris.MediaPlayer2.Player',
                                   'PlaybackStatus',
                                   dbus_interface='org.freedesktop.DBus.Properties')
        if player_status == 'Playing':
            player_name = get_player_name(i, player)
            player_names.append(player_name)
            player.Pause(dbus_interface='org.mpris.MediaPlayer2.Player',
                         reply_handler=do_nothing, error_handler=do_nothing)
    if player_names != []:
        for i in os.listdir(DIRECTORY+'/paused-players/'):

            os.remove(DIRECTORY+'/paused-players/'+i)
        for player_name in player_names:
            player_status_file = open(DIRECTORY+'/paused-players/'+player_name,
                                      "w")
            player_status_file.close()


def play():
    for i in os.listdir(DIRECTORY+'/paused-players/'):
        try:
            player = bus.get_object('org.mpris.MediaPlayer2.'+i,
                                    '/org/mpris/MediaPlayer2')
        except Exception:
            if i in os.listdir(DIRECTORY+'/paused-players'):
                os.remove(DIRECTORY+'/paused-players/'+i)

        player_status = player.Get('org.mpris.MediaPlayer2.Player',
                                   'PlaybackStatus',
                                   dbus_interface='org.freedesktop.DBus.Properties')
        if player_status == 'Paused':
            player.Play(dbus_interface='org.mpris.MediaPlayer2.Player',
                        reply_handler=do_nothing, error_handler=do_nothing)
            if i in os.listdir(DIRECTORY+'/paused-players'):
                os.remove(DIRECTORY+'/paused-players/'+i)


def stop():
    for i in players:
        player = bus.get_object(i, '/org/mpris/MediaPlayer2')
        player_status = player.Get('org.mpris.MediaPlayer2.Player',
                                   'PlaybackStatus',
                                   dbus_interface='org.freedesktop.DBus.Properties')
        if player_status == 'Playing' or player_status == 'Stopped':
            player.Stop(dbus_interface='org.mpris.MediaPlayer2.Player',
                        reply_handler=do_nothing,
                        error_handler=do_nothing)


def toggle():
    playing = False
    for i in players:
        player = bus.get_object(i, '/org/mpris/MediaPlayer2')
        player_status = player.Get('org.mpris.MediaPlayer2.Player',
                                   'PlaybackStatus',
                                   dbus_interface='org.freedesktop.DBus.Properties')
        if player_status == 'Playing':
            playing = True
    if playing:
        pause()
    else:
        play()


def next():
    for i in players:
        player = bus.get_object(i, '/org/mpris/MediaPlayer2')
        player_status = player.Get('org.mpris.MediaPlayer2.Player',
                                   'PlaybackStatus',
                                   dbus_interface='org.freedesktop.DBus.Properties')
        if player_status == 'Playing':
            player.Next(dbus_interface='org.mpris.MediaPlayer2.Player',
                        reply_handler=do_nothing,
                        error_handler=do_nothing)


def previous():
    for i in players:
        player = bus.get_object(i, '/org/mpris/MediaPlayer2')
        player_status = player.Get('org.mpris.MediaPlayer2.Player',
                                   'PlaybackStatus',
                                   dbus_interface='org.freedesktop.DBus.Properties')
        if player_status == 'Playing':
            player.Previous(dbus_interface='org.mpris.MediaPlayer2.Player',
                            reply_handler=do_nothing,
                            error_handler=do_nothing)


def getPlayerList():
    for i in bus.list_names():
        if i.startswith("org.mpris.MediaPlayer2."):
            players.append(i)


if len(sys.argv) > 1:
    getPlayerList()
    if sys.argv[1] == 'pause':
        pause()
    elif sys.argv[1] == 'play':
        play()
    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'next':
        next()
    elif sys.argv[1] == 'previous':
        previous()
    elif sys.argv[1] == 'toggle':
        toggle()
    elif sys.argv[1] == 'mute':
        mute()
    elif sys.argv[1] == 'unmute':
        unmute()
    elif sys.argv[1] == 'up':
        up()
    elif sys.argv[1] == 'down':
        down()
    elif sys.argv[1] == 'panic':
        panic()
    else:
        print(__doc__)
else:
    print(__doc__)
