from datetime import datetime
from fnmatch import fnmatch

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.widget.base import ORIENTATION_HORIZONTAL
from libqtile.widget.base import _TextBox as BaseTextBox

MOD = "mod4"
FONT = "PxPlus HP 100LX 10x11"
SYSTEM_PATH = "/home/irreq/github/config/"
FONTSIZE = 12

class Commands:
    search = "firefox"
    terminal = "alacritty"
    volume_up = "amixer -q -c 0 sset Headset 5dB+"
    volume_down = "amixer -q -c 0 sset Headset 5dB-"
    audio_toggle = "python3 -q {}audio.py toggle".format(SYSTEM_PATH)
    menu = "python3 -q {}kisspy_menu.py".format(SYSTEM_PATH)

command = Commands()

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
        used = mem_values["MemTotal:"] - mem_values["MemAvailable:"]
        percentage = used / total * 1e8
        return [round(i / 1e6, 2) for i in [total, used, percentage]]

    def main(self):
        return self._calc_mem_values(self._get_meminfo())


class SysData():
    def __init__(self):
        self.path = "/proc/cpuinfo"
        self.stat = "/proc/stat"

        self.cpus = dict()

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

        return [low, mean, high, core_usage]


cpu = SysData()
mem = MemData()

def make_correct(string, length, suffix="", filler="0"):
    difference = length-len(string)
    return string[:length] + filler*difference*(difference >= 0) + suffix

def get_everything(*args):

    result_mem = mem.main()
    result_cpu = cpu.main()
    a = make_correct
    # total = a(str(result_mem[0]), 4, suffix="GB")
    used = a(str(result_mem[1]), 4, suffix="GB")
    mem_percentage = a(str(result_mem[2]), 2, suffix="%")

    # low = a(str(result_cpu[0]), 4, suffix="GHz")
    mean = a(str(result_cpu[1]), 4, suffix="GHz")
    # high = a(str(result_cpu[2]), 4, suffix="GHz")

    # cpu_percentage = ""
    # for i in result_cpu[3]:
    #     cpu_percentage += a(str(i), 2, suffix="%")+ " "

    cpu_percentage = str(int(sum(result_cpu[3])/len(result_cpu[3])))+"%"

    # return f"RAM: {total} {used} {mem_percentage} CPU: {low} {mean} {high} {cpu_percentage}"
    return f"RAM: {used} {mem_percentage} CPU: {mean} {cpu_percentage}"


class Logger():
    """Replacement for qtile logger"""
    def __init__(self):
        pass
    def error(self, string):
        with open(SYSTEM_PATH+"qtile/log.txt", "a") as f:
            f.write("\n"+string)

logger = Logger()


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


class CustomPrompt(widget.Prompt):
    def startInput(self, *a, **kw):  # noqa: N802
        hook.fire('prompt_focus')
        return super().startInput(*a, **kw)

    def _unfocus(self):
        hook.fire('prompt_unfocus')
        return super()._unfocus()


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


groups = []
for gname in "asdfg":
    groups.append(Group(gname, label=gname.upper()))

def user_keymap(mod, shift, control, alt):
    for g in groups:
        yield mod + g.name, lazy.group[g.name].toscreen()
        yield mod + shift + g.name, lazy.window.togroup(g.name)

    # VIM keybinds
    yield mod + "h", lazy.layout.left()
    yield mod + "j", lazy.layout.down()
    yield mod + "k", lazy.layout.up()
    yield mod + "l", lazy.layout.right()

    yield mod + shift + "h", lazy.layout.shuffle_left()
    yield mod + shift + "j", lazy.layout.shuffle_down()
    yield mod + shift + "k", lazy.layout.shuffle_up()
    yield mod + shift + "l", lazy.layout.shuffle_right()

    yield mod + control + "h", lazy.layout.grow_left()
    yield mod + control + "j", lazy.layout.grow_down()
    yield mod + control + "k", lazy.layout.grow_up()
    yield mod + control + "l", lazy.layout.grow_right()

    yield mod + alt + "h", lazy.layout.flip_left()
    yield mod + alt + "j", lazy.layout.flip_down()
    yield mod + alt + "k", lazy.layout.flip_up()
    yield mod + alt + "l", lazy.layout.flip_right()

    yield mod + "n", lazy.layout.normalize()

    yield alt + "F4", lazy.window.kill()
    yield mod + shift + "r", lazy.restart()
    yield control + alt + "q", lazy.shutdown()
    yield mod + "r", lazy.spawncmd()

    yield mod + "F11", lazy.window.toggle_fullscreen()
    yield mod + "F12", lazy.spawn(command.audio_toggle)

    yield mod + "Return", lazy.spawn(command.terminal)
    yield mod + "y", lazy.spawn(command.search)
    yield mod + "o", lazy.spawn(command.menu)


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
            logger.error('Bad key %s', k)
            continue

        if 'lock' in mods:
            logger.error('You must not use "lock" modifier yourself')
            continue

        result.append(Key(list(mods), k, cmd))

    return result


keys = make_keymap(user_keymap)


class ColorScheme:
    bg = "#282828"
    highlight_bg = "#888888"
    urgent_bg = "#fe8964"

    text = "#ffffff"
    inactive_text = "#534353"

    border = "#333333"
    border_focus = urgent_bg
    highlight_text = urgent_bg


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
    foreground=ColorScheme.text,
    center_aligned=True,
    markup=False,
)


def create_widgets():
    yield CustomPrompt(
        prompt="$ ",
        padding=10,
        foreground=ColorScheme.highlight_text,
        cursor_color=ColorScheme.highlight_text,
    )
    yield widget.GroupBox(
        disable_drag=True,
        use_mouse_wheel=False,
        padding_x=4,
        padding_y=0,
        margin_y=4,
        spacing=0,
        borderwidth=0,
        highlight_method="block",
        urgent_alert_method="block",
        rounded=False,
        active=ColorScheme.text,
        inactive=ColorScheme.inactive_text,
        urgent_border=ColorScheme.urgent_bg,
        this_current_screen_border=ColorScheme.highlight_bg,
        fontsize=FONTSIZE,
        font=FONT,
    )
    yield CustomWindowName(
        padding=20
    )
    yield DisplayOutputFromFunctionEverySecond(
        function=get_everything,
        active_color=ColorScheme.highlight_text,
        inactive_color=ColorScheme.inactive_text,
    )
    yield widget.Clock(
        format="%e %a",
        foreground=ColorScheme.inactive_text,
        font=FONT,
        update_interval=60,
        padding=2,
    )
    yield widget.Clock(
        format="%H:%M:%S",
        foreground=ColorScheme.text,
        font=FONT,
        padding=2,
    )


screens = [
    Screen(
        bottom=bar.Bar(
            list(create_widgets()),
            20,
            background=ColorScheme.bg,
        ),
    ),
]


dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "urgent"
wmname = "LG3D"
