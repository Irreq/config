"""This is a file containing functions and classes which monitors
the system, without doing anything afterwards"""

from . import vars

from datetime import datetime
from fnmatch import fnmatch

try:
    import shutil
except Exception as e:
    vars.log(str(e))
    shutil = False

def get_batusage(dev="BAT0"):
    current_stat = "Error"
    charge_state = "E"

    try:
        current_stat=open("/sys/class/power_supply/"+dev+"/capacity","r").readline().strip()
        charge_state=open("/sys/class/power_supply/"+dev+"/status","r").readline().strip()
    except Exception:
        pass

    return " BAT: {} {}%".format(charge_state, current_stat)

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
        speed = vars.make_correct(str(result_cpu[1]), 4)
        cpu_percentage = str(int(sum(result_cpu[3])/len(result_cpu[3])))
        temperature = result_cpu[4]
        # Do we seriously need the CPU-frequency?
        return " CPU: {}°C {}%".format(temperature, cpu_percentage)



cpu = SysData()



def get_cpuusage():
    return "CPU: {}"


def get_netusage():
    return " NET: 532MB/s 99.2%"

def get_hddusage(disk="/"):
    total, used, free = shutil.disk_usage("/")
    return " HDD: {}GB {}%".format(int(used/(2**30)*100)/100, int(used/total*100))

def get_datetime():
    return " {date:%Y-%m-%d %H:%M:%S}".format(date=datetime.now())

def get_everything(*args):
    return get_batusage() + get_hddusage() + cpu.get_cpuusage() + get_datetime()

def test():
    print(__file__)
    print(get_everything())
