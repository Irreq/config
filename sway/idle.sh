#!/bin/bash
swayidle \
        timeout 60 'swaylock -f -c 000000' \
        timeout 70 'hyprctl dispatch dpms off' \
                resume 'hyprctl dispatch dpms on' \
        before-sleep 'swaylock -f -c 000000'
