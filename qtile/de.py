#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: config.py
# Description: Desktop environment
# Author: irreq (irreq@protonmail.com)
# Date: 03/10/2021
# Version: 3.2.0


def launch(command):
    """Launch a program as it would have been launched in terminal"""
    commands = command.split()
    subprocess.Popen(commands)


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

        p_1 = self.values["storage"][2]

        p_2 = self.values["battery"][2]

        pleasantness = int((p_1 + 100-p_2)/2 // 10)

        return "I'm feeling " + self.moods[9-energy][9-pleasantness] + " " + result



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


class SuggestionPrompt():
    """Retrieve a choice by the user
    from a set of choices or what the user has
    typed
    """

    def __init__(self, *args, **kwargs):
        """Cache"""
        self.cache = self._load_cache() or {}

    def _initiate_cache(self, path):
        """initiate an archive of executables"""
        return

    def _load_cache(self, path):
        """load an archive of executables"""
        return

    def _update_cache(self, programs: dict()):
        """update an archive of executables
        Example:
        >>>self._update_cache({"terminal": "alacritty"})
        """
        return

    def startInput(self, *choices: list()):
        """Start the input from the user"""
        return
