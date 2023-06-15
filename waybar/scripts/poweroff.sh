#!/bin/bash
case $(wofi -d -L 9 -l 3 -W 100 -x -100 -y 10 \
    -D dynamic_lines=true << EOF | sed 's/^ *//'
Shutdown
Reboot
Log out
Sleep
Lock
Cancel
EOF
) in
    "Shutdown")
        systemctl poweroff
        ;;
    "Reboot")
        systemctl reboot
        ;;
    "Sleep")
        systemctl suspend
        ;;
    "Lock")
        swaylock
        ;;
    "Log out")
        hyprctl dispatch exit
        ;;
esac