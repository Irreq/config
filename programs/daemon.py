#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A versatile Dmenu clone written in Python3
# It grabs user input until any non-acceped key has been pressed
#
# Author: Irreq

import subprocess, time

def launch(command):
    """Launch a program as it would have been launched in terminal"""
    commands = command.split()
    subprocess.Popen(commands)
    return True


class Status:

    def __init__(self):
        


print("Daemon has started")

exit(0)
