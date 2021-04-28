# -*- coding: utf8 -*-
import sys
import os
import subprocess
import signal
import locale
import time

# It might be convenient to order alias by frequency
programs = {
    # Programs
    "atom": "flatpak run io.atom.Atom",
    "discord": "flatpak run com.discordapp.Discord",

    "pavucontrol": "pavucontrol",
    "spotify": "spotify -no-zygote",
    "teams": "flatpak run com.microsoft.Teams",
    "nvim": "nvim",
    "vim": "vim",
    "python3": "python3",


    # Web
    "firefox": "firefox",
    "github": "firefox https://github.com/Irreq",
    "youtube": "firefox https://youtube.com",

    # System
    "update": "sudo xbps-install -Su",
    "reboot": "sudo reboot now",
    "shutdown": "sudo shutdown -h now",
    "ls": "ls",
    "cat": "cat",

    # Meta
    "open": "atom",
    "browse": "thunar",
    "search": "firefox https://duckduckgo.com/?q=QUERY&ia=web", # QUERY is what you type after search
    "terminal": "alacritty",
    "keyboard": "setxkbmap se",
    "wifi": "sudo wpa_supplicant -B -iwlo1 -c/etc/wpa_supplicant/wpa_supplicant-wlo1.conf",
    "screen": "xrandr --auto --output VGA-1 --mode 1920x1200 --right-of LVDS-1",
}

meta = {
    "menu": "dmenu",
    "terminal": "alacritty",
    "fileopener": "atom",           # Program to handle opening files
    "filebrowser": "thunar",          # Program to handle opening paths
    "webbrowser": "firefox",           # Program to hangle opening urls
    "search": "firefox https://duckduckgo.com/?q=QUERY&ia=web",
    "sign": "</>",                        # The placeholder?
    "menu_arguments": [
        # "-b",                           # Place at bottom of screen
        "-i",                           # Case insensitive searching
        "-nf",                          # Element foreground colour
        "#888888",
        "-nb",                          # Element background colour
        "#282828",
        "-sf",                          # Selected element foreground colour
        "#ffffff",
        "-sb",                          # Selected element background colour
        "#111111",
        "-fn",                          # Font and size'
        # "-*-PxPlus-HP-100LX-8x8-*-*-*-14-*-*-*-*-*-*-*",
        "PxPlus-HP-100LX-8x8:pixelsize=14",
        # "-*-*-*-*-14-*-*-*-*-*-*-*",
        # "PxPlus HP 100LX 10x11 9"
    ],
    "path_shellCommand": "~/.dmenuEextended_shellCommand.sh",
    "timeout": 5,

}


class Menu(object):

    def __init__(self):
        self.system_encoding = locale.getpreferredencoding() # Retrieve the system's encoding
        self.plugins_loaded = False
        self.prefs = meta
        self.debug = False
        self.preCommand = False
        self.cache = self.load_cache()

    def load_cache(self):
        """Organize available programs"""
        cache = list(programs.keys())
        # cache.extend(simple_programs)
        # cache = list(q)
        return cache

    def command_output(self, command, split=True):
        """Retrieve system output from command"""
        if type(command) != list:
            command = command.split(" ")
        tmp = subprocess.check_output(command)
        out = tmp.decode(self.system_encoding)

        if split:
            return out.split("\n")
        else:
            return out

    def message_open(self, message):
        """Output message to user"""
        tmp = [*self.prefs['menu_arguments'], *["-l", "10"]] # make output verical
        self.message = subprocess.Popen([self.prefs['menu']] + tmp,
                                        stdin=subprocess.PIPE, preexec_fn=os.setsid)
        msg = str(message)
        msg = msg.encode(self.system_encoding)
        self.message.stdin.write(msg)
        self.message.stdin.close()

    def message_close(self):
        """Close message"""
        os.killpg(self.message.pid, signal.SIGTERM)

    def open_terminal(self, command, hold=False, direct=False):
        """Open a terminal to run a command"""
        sh_command_file = os.path.expanduser(self.prefs['path_shellCommand']);
        with open(sh_command_file, 'w') as f:
            f.write("#! /bin/bash\n")
            f.write(command + ";\n")

            if hold == True:
                f.write('echo "\n\nPress enter to exit";')
                f.write('read var;')

        os.chmod(os.path.expanduser(sh_command_file), 0o744)
        os.system(self.prefs['terminal'] + ' -e ' + sh_command_file)

    def menu(self, items, prompt=False):
        """Main wrapper"""
        if type(items) == list:
            items = "\n".join(items)

        p = subprocess.Popen([meta["menu"]] + self.prefs['menu_arguments'] + ['-p', prompt],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        out = p.communicate(items.encode(self.system_encoding))[0]

        if out.decode().strip() == '':
            sys.exit()
        else:
            return out.decode().strip('\n')

    def parse(self, query):
        """Pipe to correct program"""

        if query.startswith("youtube "):
            query = "+".join(query[len("youtube "):].split())
            os.system(f"{meta['webbrowser']} https://www.youtube.com/results?search_query={query}")
        elif query.startswith("github "):
            query = "+".join(query[len("github "):].split())
            os.system(f"{meta['webbrowser']} https://github.com/search?q={query}")
        elif query.startswith("wikipedia "):
            query = "+".join(query[len("wikipedia "):].split())
            os.system(f"{meta['webbrowser']} https://en.wikipedia.org/wiki/{query}")
        elif query.startswith("search "):
            query = "+".join(query[len("search "):].split())
            tmp = meta["search"]
            tmp = tmp.replace("QUERY", query)
            os.system(tmp)
        elif query.startswith("keyboard "):
            query = "setxkbmap "+query[len("keyboard "):]
            # os.system(query)
            self.open_terminal(query)
        elif query.startswith("vim"):
            self.open_terminal(query)
        elif query.startswith("teams"):
            self.open_terminal("alacritty | "+programs[query])
        elif query.startswith("top"):
            self.open_terminal(query)
        elif query.startswith("py"):
            self.open_terminal(query)
        elif query.startswith("test"):
            self.open_terminal("neofetch")

        else:
            # If query in executable programs
            if query in programs.keys():
                self.open_terminal(programs[query])

            # Run as a command in terminal without opening a window
            else:
                try:
                    result = self.command_output(query)
                    self.message_open("\n".join(result))
                    time.sleep(meta["timeout"])
                    self.message_close()
                except Exception as e:
                    pass


if __name__ == "__main__":
    m = Menu()
    result = m.menu(m.cache, m.prefs["sign"]).strip()
    m.parse(result)
