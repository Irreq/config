#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: main.py
# Description: Main Module For My Desktop Environment
# Author: irreq (irreq@protonmail.com)
# Date: 02/11/2021
#
# I wanted to create an desktop environment with as little dependencies as
# necessary.
# Many of programs like 'dmenu' and 'amixer' has been implented in python to
# use a smaller number of packages.
#
# Benefits from this config file:
# + VIM-keybinds (Arrow keys aren't needed)
# + CPU and memory usage are part of a class which can easily be obtained by
# another function
# + Easy update on a time interval for any function
# + A static program launcher, as a simple version of dmenu_run
#
# Bad stuff from this config file:
# - Little to no automation, you must specifically edit the programs in 'programs'
# - No mouse (But if you are reading this, you probably know how to navigate
# using a keyboard)
# - Not following the UNIX philosophy of only doing one thing, this file is
# more of a: "Do everything"
# Which might not be ideal, but i haven't got around to implement it yet...


# TODO:
# * Current playing Audio | Hard
# * Current Volume Level | Easy
# * Network status and speed | Medium
# * Auto detection of hardware (Start programs) | Medium
# * Dynamic Program selection | Easy
# * Notifications? | Easy
# * MORE AI | -
"""Documentation"""

# Imports

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
    sr_mode = "Working"
except Exception:
    sr = False
    sr_mode = "not_Working"

things_to_display = ["",]

functions_to_display = ["battery", "storage_test", "memory", "cpu", "datetime"]

programs = {
    # Programs
    "alacritty": "alacritty",
    "discord": "Discord",

    # Programming
    "atom": "atom",
    "nvim": "nvim",
    "vim": "vim",
    "python3": "alacritty",

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
    "vol_up": "amixer -q sset Master 10%+",
    "vol_down": "amixer -q sset Master 10%-",
    "pause": "python3 -q /home/irreq/github/config/programs/audio.py toggle",
    "gesture_audio": "python3 -q /home/irreq/github/config/programs/handVolumeController.py",
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

def program_ul(p):
    if p in programs:
        return programs[p]

# #### TEST AREA ####

def initiate_cache():
    """This function is not finished but will create a dynamic program list"""
    return

make_and_model_path = "/sys/devices/virtual/dmi/id/product_version"

def get_from_file(path):
    content=open(path, "r").readline().strip()
    return content


def launch(command):
    """Launch a program as it would have been launched in terminal"""
    commands = command.split()
    subprocess.Popen(commands)
    return True


# #### STATUS BAR ####

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


class Status():

    def __init__(self, verbose=True, status_items=["cpu"]):
        self.verbose = verbose
        self.status_items = status_items
        self.values = {item:[str, *(int,)*3] for item in self.status_items}

        self.dynamic_cpu = SysData()

    def make_correct(self, string, length, suffix="", filler="0"):
        difference = length-len(string)
        return string[:length] + filler*difference*(difference >= 0) + suffix

    def cpu(self):
        cpu_info = self.dynamic_cpu._get_cpuinfo()
        low, mean, high = self.dynamic_cpu._calc_cpu_freqs(cpu_info)

        core_usage = self.dynamic_cpu._calc_cpu_percent_wrapper()

        temperature = int(self.dynamic_cpu._get_tempinfo())

        # speed = self.make_correct(str(mean), 4)
        cpu_percentage = int(sum(core_usage)/len(core_usage))

        if not self.verbose:
            HOT = 80
            COLD = 19
            temp = abs(continuous_rectifier(COLD, temperature, HOT)-COLD)/(HOT-COLD)*100

            avg = (cpu_percentage + temp) // 2
        else:
            avg = cpu_percentage

        # Do we seriously need the CPU-frequency?

        text = "CPU: {}°C {}%".format(temperature, cpu_percentage)

        return text, temperature, cpu_percentage

    def audio(self):
        percentage = 100
        # return "VOL: Master {}%".format(percentage), 0, 0
        return "VOL: <UNFINISHED>", 0, 0

    def network(self):
        return "NET: <UNFINISHED>", 0, 0

    def memory(self, path="/proc/meminfo", head=40):
        """Calculate: total memory, used memory and percentage

        From 'htop':

        Total used memory = MemTotal - MemFree
        Non cache/buffer memory (green) = Total used memory - (Buffers + Cached memory)
        Buffers (blue) = Buffers
        Cached memory (yellow) = Cached + SReclaimable - Shmem
        Swap = SwapTotal - SwapFree
        """

        with open(path, "r") as f:
            info = [next(f).split() for _ in range(head)]
            mem_values = {fields[0]: float(fields[1]) for fields in info}

        total = mem_values["MemTotal:"]

        used = total - mem_values['MemFree:'] - (mem_values['Buffers:'] + (mem_values['Cached:'] + mem_values['SReclaimable:'] - mem_values['Shmem:']))

        # 2^20 = 1048576
        total, used = [int(i/1048576*100)/100 for i in (total, used)]

        percentage = int(used / total * 100)

        text = "RAM: {}GB {}%".format(used, percentage)

        return text, used, percentage

    def storage(self, disk="/"):
        total, used, free = shutil.disk_usage("/")

        status = int(used/(2**30)*100)/100

        capacity = int(used/total*100)

        text = "SSD: {}GB {}%".format(status, capacity)

        return text, status, capacity

    def storage_test(self):
        return "SSD: <TESTING>", 0, 80

    def battery(self):
        capacity = "-"
        status = "Error"

        try:
            status = get_from_file("/sys/class/power_supply/BAT0/status")
            capacity = int(get_from_file("/sys/class/power_supply/BAT0/capacity"))
        except Exception:
            pass

        if not self.verbose:
            if status == "Error":
                return 0
            else:
                return int(status)

        text = "BAT: {} {}%".format(status, capacity)

        return text, status, capacity

    def datetime(self):
        current = datetime.now()
        # date = "{date:%Y-%m-%d}".format(date=current)
        # time = "{time:%H:%M:%S}".format(time=current)
        #
        # return str(type(current))
        return "{date:%Y-%m-%d %H:%M:%S}".format(date=datetime.now()), 0, 0


class AI(Status):

    # Pleasantness X Energy
    moods = """
    enraged     panicked     stressed     jittery      shocked   surprised upbeat     festive      exhilarated ecstatic
    livid       furious      frustrated   tense        stunned   hyper     cheerful   motivated    inspired    elated
    fuming      frightened   angry        nervous      restless  energized lively     enthusiastic optimistic  excited
    anxious     apprehensive worried      irritated    annoyed   pleased   happy      focused      proud       thrilled
    repulsed    troubled     concerned    uneasey      peeved    pleasant  joyful     hopeful      playful     blissful
    disgusted   glum         disappointed down         apathetic easy      easygoing  content      loving      fulfilled
    pessimistic morose       discouraged  sad          bored     calm      secure     satisfied    grateful    touched
    alienated   miserable    lonely       disheartened tired     relaxed   chill      restful      blessed     balanced
    despondent  depressed    sullen       exhausted    fatigued  mellow    thoughtful peaceful     comfy       carefree
    despair     hopeless     desolate     spent        drained   sleepy    complacent tranquil     cozy        serene
    """



    def __init__(self):
        self.count = 0
        super().__init__()
        self.status_items = functions_to_display

        self.values = {}

        self.moods = [i.split() for i in self.moods.split("\n")[1:-1]]

    def notifications(self):
        final = []

        for function in self.status_items:
            try:
                text, data, percentage = getattr(super(), function)()
                self.values[function] = [text, data, percentage]
                result = text
            except Exception as e:
                result = "{} {}".format(function, str(e))
            final.append(result)

        return " ".join(final)

    def update(self, *args):

        result = self.notifications()

        _, temperature, percentage = self.values["cpu"]

        HOT = 80
        COLD = 19
        temp = abs(self.continuous_rectifier(COLD, temperature, HOT)-COLD)/(HOT-COLD)*100

        avg = (int(percentage) + temp) // 2

        energy = int(avg // 10)

        p_1 = self.values["storage_test"][2]

        p_2 = self.values["battery"][2]

        pleasantness = int((p_1 + 100-p_2)/2 // 10)

        return " ".join(things_to_display) + " I'm feeling " + self.moods[9-energy][9-pleasantness] + " " + result



    def continuous_rectifier(self, x0, x, x1):
        """
        Theoretical Continuous Analog Rectifier For Artificial Neural Networks.

        NOTE:           The algorithm yields an input-value rectified
                        between two other values calculated by the relative
                        distance distance. This equation is defined as:
                        ______________________________________________________

                                                x1 - x0
                        f(x0, x, x1) = ------------------------ + x0
                                               -(2*x - x1 - x0)
                                                ---------------
                                       1 + (5e)     x1 - x0
                        ______________________________________________________
                        If x is not between x0 and x1, x will be valued
                        closest to that value. This will create.
                        If x0<x<x1, x will kind of keep its value apart
                        from minor changes. If not x0<x<x1, x will be
                        fit within boundaries. It is basically the
                        sigmoid function, but instead of: x -> 0<x<1
                        it is: x -> x0<x<x1

        ARGUMENTS:
            - x0                float() The lower boundary (min).
            - x                 float() The value to rectify.
            - x1                float() The upper boundary (max).
        RETURNS:
            - float()           x0 <= x <= x1
        """

        e = 2.71828182846

        return (x1 - x0) / (1 + (5*e) ** -((2*x - x1 - x0) / (x1 - x0))) + x0


ai = AI()

def update_status_wrapper(*args):

    return ai.update()

#### VOICE CONTROL ####

class Voice():

    def __init__(self):
        pass

    def notify(self, text):
        """Runs threaded and won't affect the calling function"""
        launch("{} {}".format(programs["tts"], text))


    def numToWords(self, num,join=True):
        # By 'Developer' https://stackoverflow.com/a/19193721

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


    def appendInt(self, num):
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


    def time_conversion_24(self, hours, minutes):
        """Convert time to words"""
        result = self.numToWords(hours)

        if minutes == 0:
            result += " o'clock"

        elif minutes == 15:
            result = "quarter past " + result

        elif minutes == 30:
            result = "half past " + result

        elif minutes == 45:
            result = "quarter to " + result

        elif minutes < 30:
            result = "{} minute{} past ".format(self.numToWords(minutes), "" if minutes == 1 else "s") + result

        else:
            result = "{} minute{} to ".format(self.numToWords(60-minutes), "" if 60 - minutes == 1 else "s") + result
        return result


    def parse_query(self, query):

        if query.startswith("hello"):
            self.notify("Hello, friend!")
        elif query.startswith("exit"):
            self.notify("Bye!")
            return

        elif query.startswith("time"):
            d_date = datetime.now()
            date = d_date.strftime("%A %d %B %Y %I %M %S")
            date = date.split()
            result = date[0] + " " + self.numToWords(int(date[1])) + self.appendInt(date[1]) + " " + date[2]
            result += self.numToWords(int(date[3])) + " " + self.time_conversion_24(int(date[4]), int(date[5]))
            result += " or " + self.numToWords(int(date[4])) + " and " + self.numToWords(int(date[5]))

            self.notify(result)

        elif query.startswith("rapport"):
            self.notify("Welcome back, all systems are online and working properly!")
        elif query.startswith("audio"):
            os.system("python3 -q /home/irreq/github/config/programs/audio.py toggle")
        else:
            tokenized = nltk.word_tokenize(query)
            nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if (pos[:2] == 'NN')]
            # notify(" ".join(nouns))
            try:
                subprocess.Popen([programs[query.lower()]])
                self.notify(programs[query])
            except Exception:
                pass

            #if len(nouns) != 0:
            #    lazy.spawn(programs[nouns[0]])

            #else:
            #    notify("What?")


    def recognize_speech_from_microphone(self, recognizer, microphone):
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


    def test_tts(self, qtile, *args, **kwargs):
        if not sr:
            self.notify("Speech recognition not installed")
            return

        self.notify("Working")
        # return

        recognizer = sr.Recognizer()

        # Error occurs here when PyAudio is not installed
        microphone = sr.Microphone()

        self.notify("Yes?")
        data = self.recognize_speech_from_microphone(recognizer, microphone)
        if data["error"] != "":
            self.notify(data["error"])
        else:
            self.parse_query(data["transcription"])


    def main(self):
        return






def notify(text):
    """Runs threaded and won't affect the calling function"""
    launch("{} {}".format(programs["tts"], text))


#### End ####


def test_tts(qtile, *args, **kwargs):
    # voice.test_tts(2, 3)
    return notify("Check Python Script")
