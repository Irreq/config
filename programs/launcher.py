import sys, os

"""This is a program launcher written in Python

Usage:
    % python3 launcher.py <program_name> <flags>
"""

programs = {
    # Programs
    "alacritty": "alacritty",
    "discord": "discord",
    #"discord": "flatpak run com.discordapp.Discord",
    "teams": r"flatpak run com.microsoft.Teams",

    # Programming
    "atom": "flatpak run io.atom.Atom",
    "nvim": "nvim",
    "vim": "vim",
    "python3": "python3",

    # Web
    "firefox": "firefox",
    "github": "firefox https://github.com/Irreq",
    "youtube": "https://www.youtube.com/results?search_query=QUERY",

    # System (be careful, some stuff might break)
    "update": "sudo xbps-install -Su",
    "reboot": "sudo reboot now",
    "shutdown": "sudo shutdown -h now",

    "tester": "(alacritty &)",

    # Audio
    #"vol_up": "amixer -q -c 0 sset Headset 5dB+",
    #"vol_down": "amixer -q -c 0 sset Headset 5dB-",
    "vol_up": "amixer -q sset Master 10%+",
    "vol_down": "amixer -q sset Master 10%-",
    "pause": "python3 -q /home/irreq/github/config/programs/audio.py toggle",
    "pavucontrol": "pavucontrol",
    "spotify": "spotify -no-zygote",

    # Meta
    "open": "atom",
    "filebrowser": "thunar",
    "searchbrowser": "firefox",
    "search": "firefox https://duckduckgo.com/?q=QUERY&ia=web", # QUERY is what you type after search
    "terminal": "alacritty",
    "keyboard": "setxkbmap se",
    "wifi": "sudo wpa_supplicant -B -iwlo1 -c/etc/wpa_supplicant/wpa_supplicant-wlo1.conf",
    "screen_hdmi": "xrandr --output VGA-0 --off --output LVDS --off --output HDMI-0 --mode 1920x1200 --pos 0x0 --rotate normal",
    "screen_vga": "xrandr --output HDMI-0 --off --output LVDS --off --output VGA-0 --mode 1920x1200 --pos 0x0 --rotate normal",
}

if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        print(__doc__)
        exit(0)
    try:
        os.system(programs[sys.argv[1:][0]])
        exit(0)
    except Exception:
        pass
    #print(len(sys.argv[1:]))

