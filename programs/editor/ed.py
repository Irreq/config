import curses
import sys



def handle_key(key):
    if key == "q":
        sys.exit(0)

def main(stdscr):
    
    file = sys.argv[1]

    with open(file) as f:
        buffer = f.readlines()



    while True:
        stdscr.erase()
        for row, line in enumerate(buffer):
            stdscr.addstr(row, 0, line)


        handle_key(stdscr.getkey())

        #k = stdscr.getkey()
        #if k == "q":
        #    sys.exit(0)

if __name__ == "__main__":
    curses.wrapper(main)
