import time

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
        total = mem_values["MemTotal:"]
        # used = mem_values["MemTotal:"] - mem_values["MemAvailable:"]
        used = mem_values["MemTotal:"] - (mem_values['MemFree:'] + mem_values['Buffers:'] + mem_values['Cached:'])
        percentage = used / total * 1e8
        return [round(i / 1e6, 2) for i in [total, used, percentage]]

    def main(self):
        return self._calc_mem_values(self._get_meminfo())

    def get_memusage(self):
        result_mem = self.main()
        # used = make_correct(str(result_mem[1]), 4, suffix="GB")
        used = str(result_mem[1])
        mem_percentage = make_correct(str(int(result_mem[2])), 2, suffix="%")
        return " MEM: {} {}".format(used, mem_percentage)


mem = MemData()


def test():
    with open('/proc/meminfo', 'rt') as f:
        vals = {}
        for i in f.read().splitlines():
            try:
                name, val = i.split(':')
                vals[name.strip()] = int(val.split()[0])
            except:
                pass
    memfree = vals['MemFree'] + vals['Buffers'] + vals['Cached']
    return float(vals['MemTotal'] - memfree) / 1e6

while True:
    a = mem.get_memusage()
    # a = test()
    print(a)
    time.sleep(1)
