import os
import sys

class commands:

    def update(args):
        print(args)

cmds = commands


def update(args):
    print(args)


def main(arguments):
    #print(arguments)
    #result = getattr(commands, arguments[0], arguments[1:])
    try:
        globals()[arguments[0]](arguments[1:])

    except Exception:
        pass




if __name__ == "__main__":
    #main(sys.argv[1:])
    arguments = sys.argv[1:]
    try:
        globals()[arguments[0]](arguments[1:])
    except Exception:
        print("{}: command not found".format(arguments[0]))
