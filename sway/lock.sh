#!/bin/bash
swayidle -w \
        timeout 60 'swaylock -f -c 000000' \
        timeout 60 'hyprctl dispatch dpms off' \
                resume 'hyprctl dispatch dpms on' \
        before-sleep 'swaylock -f -c 000000'
