import os
import sys
arg = r"flatpak run io.atom.Atom"
arg = r"flatpak run com.microsoft.Teams"

# os.system(arg)

# with open("/home/irreq/github/config/qtile/log.txt", "w") as f:
#     f.write(" ".join(sys.argv[1:]))
#     f.close()
os.system(" ".join(sys.argv[1:]))

def open_terminal(command, hold=False, direct=False):
    """Open a terminal to run a command"""
    sh_command_file = os.path.expanduser("~/.dmenuEextended_shellCommand.sh");
    with open(sh_command_file, 'w') as f:
        f.write("#! /bin/bash\n")
        f.write(command + ";\n")

        if hold == True:
            f.write('echo "\n\nPress enter to exit";')
            f.write('read var;')

    os.chmod(os.path.expanduser(sh_command_file), 0o744)
    os.system(programs["terminal"] + ' -e ' + sh_command_file)

def test_lol(res):
    # global result
    try:
        # open_terminal(res)
        os.system("python3 -q /home/irreq/github/config/qtile/test.py {}".format(res))
        # os.system(res)
        # result = str(res)
    except Exception as e:
        pass
    return

class BrowseablePrompt():

    def __init__(self, *args, arguments={"Empty": "echo Empty"}, n_suggestions=42, **kwargs):
        self._args = args
        self._arguments = arguments
        self._n_suggestions = n_suggestions
        self._kwargs = kwargs

        self.clear()

    def clear(self):
        self.position = None
        self.cursor_position = 0
        self.available = ""
        self.user_input = ""
        self.archived_input = ""

    def main(self):
        pass

    def exec_cmd(self):
        pass

    def move_right(self):
        pass

    def move_left(self):
        pass
