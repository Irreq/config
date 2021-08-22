# -*- coding: utf-8 -*-
#
# Author: Irreq
#
# I wanted to create an desktop environment with as little dependencies as necessary.
# Many of programs like 'dmenu' and 'amixer' has been implented in python to use a
# smaller number of packages.
#
# Benefits from this config file:
# + VIM-keybinds (Arrow keys aren't needed)
# + CPU and memory usage are indivudual classes and should work for broader architecture
# + Easy update on a time interval for any function
# + A static program launcher, as a simple version of dmenu_run
#
# Bad stuff from this config file:
# - Little to no automation, you must specifically edit the programs in 'programs'
# - No mouse (But if you are reading this, you probably know how to navigate using a keyboard)
# - Not following the UNIX philosophy of only doing one thing, this file is more of a: "Do everything"
# Which might not be ideal, but i haven't got around to implement it yet...

import subprocess
try:
    import nltk
except Exception:
    nltk = False

import shutil

from datetime import datetime
from fnmatch import fnmatch

try:
    import speech_recognition as sr
except Exception:
    sr = False

from libqtile import bar, hook, pangocffi, layout, widget
from libqtile.command import lazy
from libqtile.config import Group, Key, Screen
from libqtile.widget.base import ORIENTATION_HORIZONTAL
from libqtile.widget.base import _TextBox as BaseTextBox

MOD = "mod4"
FONT = "PxPlus HP 100LX 10x11"
FONTSIZE = 12

programs = {
    # Programs
    "alacritty": "alacritty",
    "discord": "Discord",

    # Programming
    "atom": "atom",
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
    "tts": "sam",  # requires 'SAM' as /bin/sam
    "searchbrowser": "firefox",
    "search": "firefox https://duckduckgo.com/?q=QUERY&ia=web", # QUERY is what you type after search
    "terminal": "alacritty",
    "keyboard": "setxkbmap se",
    "wifi": "sudo wpa_supplicant -B -iwlo1 -c/etc/wpa_supplicant/wpa_supplicant-wlo1.conf",
    "screen_hdmi": "xrandr --output VGA-0 --off --output LVDS --off --output HDMI-0 --mode 1920x1200 --pos 0x0 --rotate normal",
    "screen_vga": "xrandr --output HDMI-0 --off --output LVDS --off --output VGA-0 --mode 1920x1200 --pos 0x0 --rotate normal",
    "screen_vga_thinkpad": "xrandr --output HDMI-0 --off --output LVDS1 --off --output VGA1 --mode 1920x1200 --pos 0x0 --rotate normal",
}

class Colors:
    bg = "#282828"
    highlight_bg = "#2596be"
    urgent_bg = "#ff0000"
    text = "#ffffff"
    inactive_text = "#555753"
    border_focus = "#354ae8"
    highlight_text = "#d3d7cf"


def make_correct(string, length, suffix="", filler="0"):
    difference = length-len(string)
    return string[:length] + filler*difference*(difference >= 0) + suffix

class MemData():
    def __init__(self):
        self.path = "/proc/meminfo"

    def _get_meminfo(self, head=40):
            with open(self.path, "r") as f:
                info = [next(f).split() for _ in range(head)]
                return {fields[0]: float(fields[1]) for fields in info}

    def _calc_mem_values(self, mem_values):
        """Calculate: total memory, used memory and percentage"""

        # From 'htop'
        # Total used memory = MemTotal - MemFree
        # Non cache/buffer memory (green) = Total used memory - (Buffers + Cached memory)
        # Buffers (blue) = Buffers
        # Cached memory (yellow) = Cached + SReclaimable - Shmem
        # Swap = SwapTotal - SwapFree
        total = mem_values["MemTotal:"]

        used = total - mem_values['MemFree:'] - (mem_values['Buffers:'] + (mem_values['Cached:'] + mem_values['SReclaimable:'] - mem_values['Shmem:']))

        # 2^20 = 1048576
        result = [int(i/1048576*100)/100 for i in (total, used)]

        result.append(int(used / total * 100))

        return result

    def main(self):
        return self._calc_mem_values(self._get_meminfo())

    def get_memusage(self):
        result_mem = self.main()
        used = str(result_mem[1])
        percentage = str(result_mem[2])
        return " RAM: {}GB {}%".format(used, percentage)


class SysData():
    def __init__(self):
        self.path = "/proc/cpuinfo"
        self.stat = "/proc/stat"
        # temperature = cat /sys/class/thermal/thermal_zone*/temp
        self.cpus = dict()
        self.temp = 0

        self.refresh()

    def refresh(self):
        self.cpus = ["cpu?*"]
        self.cpus = {"cpus": self.cpus, "last": {}, "list": []}

        for line in self._get_stat():
            fields = line.split()
            cpu_name = fields[0]

        for local_filter in self.cpus["cpus"]:
            if fnmatch(cpu_name, local_filter):
                self.cpus["list"].append(cpu_name)


    def _get_tempinfo(self):
        # Fix this as it is hardcoded to work only for thermal_zone0 and
        # that could be anything on a multisensor system.
        with open(r"/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = [i.split("\n")[0] for i in f][0]
            return str(int(float(temp) / 1e3))

    def _get_cpuinfo(self):
        with open(self.path, "r") as f:
            return [float(line.split()[-1]) for line in f if "cpu MHz" in line]

    def _calc_cpu_freqs(self, cpu_freqs):
        """Min, mean and max"""
        freqs = [min(cpu_freqs), sum(cpu_freqs) / len(cpu_freqs), max(cpu_freqs)]
        return [round(i / 1e3, 2) for i in freqs]

    def _calc_cpu_percent(self, cpu):
        name, idle, total = cpu
        last_idle = self.cpus["last"].get(name, {}).get("idle", 0)
        last_total = self.cpus["last"].get(name, {}).get("total", 0)
        used_percent = 0

        if total != last_total:
            used_percent = (1 - (idle - last_idle) / (total - last_total)) * 100

        self.cpus["last"].setdefault(name, {}).update(
            zip(["name", "idle", "total"], cpu)
        )
        return used_percent

    def _get_stat(self):
            # kernel/system statistics. man -P 'less +//proc/stat' procfs
            stat = []
            with open(self.stat, "r") as f:
                for line in f:
                    if "cpu" in line:
                        stat.append(line)
                    else:
                        return stat

    def _filter_stat(self, stat, avg=False):
            if avg:
                fields = stat[0].split()
                return "avg", int(fields[4]), sum(int(x) for x in fields[1:])

            new_stat = []
            for line in stat:
                fields = line.split()
                cpu_name = fields[0]
                if self.cpus["cpus"]:
                    for _filter in self.cpus["cpus"]:
                        if fnmatch(cpu_name, _filter):
                            if cpu_name not in self.cpus["list"]:
                                self.cpus["list"].append(cpu_name)
                    if cpu_name not in self.cpus["list"]:
                        continue

                new_stat.append((cpu_name, int(fields[4]), sum(int(x) for x in fields[1:])))
            return new_stat

    def _calc_cpu_percent_wrapper(self):

        stat = self._get_stat()

        cpu = self._filter_stat(stat, avg=False)
        return [self._calc_cpu_percent(i) for i in cpu]

    def main(self):
        cpu = self._get_cpuinfo()
        low, mean, high = self._calc_cpu_freqs(cpu)

        core_usage = self._calc_cpu_percent_wrapper()

        temperature = self._get_tempinfo()

        return [low, mean, high, core_usage, temperature]

    def get_cpuusage(self):
        result_cpu = self.main()
        speed = make_correct(str(result_cpu[1]), 4)
        cpu_percentage = str(int(sum(result_cpu[3])/len(result_cpu[3])))
        temperature = result_cpu[4]
        # Do we seriously need the CPU-frequency?
        return " CPU: {}°C {}%".format(temperature, cpu_percentage)


cpu = SysData()
mem = MemData()


def get_batusage():
    current_stat = "-"
    charge_state = "Error"

    try:
        current_stat=open("/sys/class/power_supply/BAT0/capacity","r").readline().strip()
        charge_state=open("/sys/class/power_supply/BAT0/status","r").readline().strip()
    except Exception:
        pass

    return " BAT: {} {}%".format(charge_state, current_stat)


def get_netusage():
    return " NET: 532MB/s 99.2%"


def get_hddusage(disk="/"):
    total, used, free = shutil.disk_usage("/")
    return " HDD: {}GB {}%".format(int(used/(2**30)*100)/100, int(used/total*100))


def get_datetime():
    return " {date:%Y-%m-%d %H:%M:%S}".format(date=datetime.now())


def get_everything(*args):
    return get_batusage() + get_hddusage() + mem.get_memusage() + cpu.get_cpuusage() + get_datetime()


def launch(command):
    """Launch a program as it would have been launched in terminal"""
    commands = command.split()
    subprocess.Popen(commands)
    return True


#### VOICE CONTROL ####

def notify(text):
    """Runs threaded and won't affect the calling function"""
    # subprocess.Popen([programs["tts"], text])
    launch("{} {}".format(programs["tts"], text))

#### By 'Developer' https://stackoverflow.com/a/19193721 ####
def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    units = ['','one','two','three','four','five','six','seven','eight','nine']
    teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
             'seventeen','eighteen','nineteen']
    tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
            'eighty','ninety']
    thousands = ['','thousand','million','billion','trillion','quadrillion', \
                 'quintillion','sextillion','septillion','octillion', \
                 'nonillion','decillion','undecillion','duodecillion', \
                 'tredecillion','quattuordecillion','sexdecillion', \
                 'septendecillion','octodecillion','novemdecillion', \
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = int((numStrLen+2)/3)
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = int(groups-(i/3+1))
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+',')
    if join: return ' '.join(words)
    return words
#### End ####


def appendInt(num):
    num = int(num)
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == '1':
            return 'th'
    lastDigit = num % 10
    if (lastDigit == 1):
        return 'st'
    elif (lastDigit == 2):
        return 'nd'
    elif (lastDigit == 3):
        return 'rd'
    else:
        return 'th'

def time_conversion_24(hours, minutes):
    """Convert time to words"""
    result = numToWords(hours)

    if minutes == 0:
        result += " o'clock"

    elif minutes == 15:
        result = "quarter past " + result

    elif minutes == 30:
        result = "half past " + result

    elif minutes == 45:
        result = "quarter to " + result

    elif minutes < 30:
        result = "{} minute{} past ".format(numToWords(minutes), "" if minutes == 1 else "s") + result

    else:
        result = "{} minute{} to ".format(numToWords(60-minutes), "" if 60 - minutes == 1 else "s") + result
    return result



def parse_query(query):

    if query.startswith("hello"):
        notify("Hello, friend!")
    elif query.startswith("exit"):
        notify("Bye!")
        return

    elif query.startswith("time"):
        d_date = datetime.now()
        date = d_date.strftime("%A %d %B %Y %I %M %S")
        date = date.split()
        result = date[0] + " " + numToWords(int(date[1])) + appendInt(date[1]) + " " + date[2]
        result += numToWords(int(date[3])) + " " + time_conversion_24(int(date[4]), int(date[5]))
        result += " or " + numToWords(int(date[4])) + " and " + numToWords(int(date[5]))

        notify(result)

    elif query.startswith("rapport"):
        notify("Welcome back, all systems are online and working properly!")
    elif query.startswith("audio"):
        os.system("python3 -q /home/irreq/github/config/programs/audio.py toggle")
    else:
        tokenized = nltk.word_tokenize(query)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if (pos[:2] == 'NN')]
        # notify(" ".join(nouns))
        try:
            subprocess.Popen([programs[query.lower()]])
            notify(programs[query])
        except Exception:
            pass

        #if len(nouns) != 0:
        #    lazy.spawn(programs[nouns[0]])

        #else:
        #    notify("What?")


def recognize_speech_from_microphone(recognizer, microphone):
    response = {
            "success": True,
            "error": "",
            "transcription": ""
    }

    if not isinstance(recognizer, sr.Recognizer):
        response["error"] = "`recognizer` must be `Recognizer` instance"

    if not isinstance(microphone, sr.Microphone):
        response["error"] = "`microphone` must be `Microphone` instance"

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unintelligible"

    return response


def test_tts(qtile, *args, **kwargs):
    if not sr:
        notify("Speech recognition not installed")
        return

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    notify("Yes?")
    data = recognize_speech_from_microphone(recognizer, microphone)
    if data["error"] != "":
        notify(data["error"])
    else:
        parse_query(data["transcription"])


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

        #self.callback = run_program
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


groups = [Group(gname, label=gname.upper()) for gname in "asdfg"]

@hook.subscribe.client_new
def client_new(client):
    if client.name == 'discord':
        client.togroup('d')

    elif client.name == 'firefox':
        client.togroup('s')


def user_keymap(mod, shift, control, alt):
    for g in groups:
        yield mod + g.name, lazy.group[g.name].toscreen()
        yield mod + shift + g.name, lazy.window.togroup(g.name)

    # VIM keybinds
    yield mod + "h", lazy.layout.left()
    yield mod + "j", lazy.layout.down()
    yield mod + "k", lazy.layout.up()
    yield mod + "l", lazy.layout.right()

    yield mod + "n", lazy.layout.normalize()

    yield mod + shift + "h", lazy.layout.shuffle_left()
    yield mod + shift + "j", lazy.layout.shuffle_down()
    yield mod + shift + "k", lazy.layout.shuffle_up()
    yield mod + shift + "l", lazy.layout.shuffle_right()

    yield mod + control + "h", lazy.layout.grow_left()
    yield mod + control + "j", lazy.layout.grow_down()
    yield mod + control + "k", lazy.layout.grow_up()
    yield mod + control + "l", lazy.layout.grow_right()

    # Audio
    yield mod + "comma", lazy.spawn(programs["vol_down"])
    yield mod + "period", lazy.spawn(programs["vol_up"])
    yield mod + "minus", lazy.spawn(programs["pause"])

    # Start stuff
    yield mod + "o", lazy.spawncmd() # Open menu
    yield mod + "y", lazy.function(test_tts) # Launch SAM assistant
    yield mod + "Return", lazy.spawn(programs["terminal"])
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
        function=get_everything,
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


@hook.subscribe.startup_once
def autostart():
    # Just add process to start on boot:
    for p in ["keyboard", "alacritty"]:
        launch(programs[p])


dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
# bring_front_click = True
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = "urgent"
wmname = "Qtile"
