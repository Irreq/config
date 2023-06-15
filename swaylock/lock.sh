#!/bin/bash

if pgrep -x swaylock; then
    swaylock 
    hyprctl dispatch dpms off
else;
    hyprctl dispatch dpms on
fi