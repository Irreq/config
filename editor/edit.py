"""Simple curses-based text editor."""
from argparse import ArgumentParser, RawDescriptionHelpFormatter, _StoreTrueAction
from contextlib import contextmanager
import curses
import os

__version__ = "0.1"
PROGRAM_NAME = "Editor"
FONT = 'bold'


class Buffer(object):
    """The basic data structure for editable text.
    The buffer is column and row oriented. Column and row numbers start with 0.
    A buffer always has at least one row. All positions within a buffer specify
    a position between characters.
    """

    def __init__(self, text=''):
        """Create a new Buffer, optionally initialized with text."""
        self._lines = text.split('\n')

    def get_lines(self):
        """Return list of lines in the buffer."""
        return list(self._lines) # return a copy

    def _check_point(self, row, col):
        """Raise ValueError if the given row and col are not a valid point."""
        if row < 0 or row > len(self._lines) - 1:
            raise ValueError("Invalid row: '{}'".format(row))
        cur_row = self._lines[row]
        if col < 0 or col > len(cur_row):
            raise ValueError("Invalid col: '{}'".format(col))

    def set_text(self, row1, col1, row2, col2, text):
        """Set the text in the given range.
        The end of the range is exclusive (to allow inserting text without
        removing a single character). Column numbers are positions between
        characters.
        Raises ValueError if the range is invalid.
        """
        # TODO check that point2 is after or the same as point1
        self._check_point(row1, col1)
        self._check_point(row2, col2)

        line = self._lines[row1][:col1] + text + self._lines[row2][col2:]
        self._lines[row1:row2+1] = line.split('\n')


class Engine(object):

    def __init__(self, current=None):
        """create a frame for all the files"""
        self._backend = {}
        self._clipboard = ""
        self._current = current
        self._mode = "normal"
        self._message = ""  # what to display
        self._query = ""  # if code needs to be executed

        if self._current == None:
            self.set_structure(self._current, "")

    def set_structure(self, name, data):
        self._backend[name] = {"file": None,
                               "buffer": Buffer(data),
                               "row": 0,
                               "column": 0,
                               "changes": False}

    def get_file(self, name):
        """get the file data and setup structure"""
        if name in self._backend.keys():
            return

        with open(name) as file:
            data = file.read()
            # file.close()

        self.set_structure(name, data)
        self._message = f"opened: {name}"

    def write_file(self, name):
        """write out to file"""
        if name not in self._backend.keys():
            return

        if name == None:
            self._message = "you cannot write to memory"
            return

        try:
            with open(name, 'w') as f:
                f.write("\n".join(self._backend[name]["buffer"].get_lines()))
                f.close()
            self._message = f"wrote to: {name}"
        except IOError:
            self._message = f"couldn't write to: {name}"

    # def exit_file(self, name):
    #     """remove file from memory"""
    #     if name not in self._backend.keys():
    #         return
    #
    #     self._backend[name]["file"].close()
    #     del self._backend[name]

    def touch_file(self, name):
        """create a file"""
        with open(name, 'a'):
            os.utime(name, None)

        self._message = f"touched: {name}"

    def kill_engine(self):
        """quit the program nicely"""
        # for i in list(self._backend.keys()).copy():
        #     self._backend[i]["file"].close()
        #     del self._backend[i]
        exit(0)


    def _handle_normal_keypress(self, name, char):
        """Handle a keypress in normal mode."""
        if name not in self._backend.keys():
            return

        if char == ord('q'):  # quit
            self._will_exit = True
        elif char == ord('j'):  # down
            self._backend[name]["row"] += 1
        elif char == ord('k'):  # up
            self._backend[name]["row"] -= 1
        elif char == ord('h'):  # left
            self._backend[name]["column"] -= 1
        elif char == ord('l'):  # right
            self._backend[name]["column"] += 1
        elif char == ord('9'):  # move to beginning of line
            self._backend[name]["column"] = 0
        elif char == ord('0'):  # move to end of line
            cur_line_len = len(self._backend[name]["buffer"].get_lines()[self._backend[name]["row"]])

            self._backend[name]["column"] = cur_line_len
            # self._backend[name]["row"] = cur_line_len
        elif char == ord('x'):  # delete a character
            self._backend[name]["buffer"].set_text(self._backend[name]["row"],
                                                   self._backend[name]["column"],
                                                   self._backend[name]["row"],
                                                   self._backend[name]["column"] + 1,
                                                   '')
        elif char == ord('i'):  # enter insert mode
            self._mode = "insert"
        elif char == ord('a'):  # enter insert mode after cursor
            self._mode = "insert"
            self._backend[name]["column"] += 1
        elif char == ord('o'):  # insert line after current
            cur_line_len = len(self._backend[name]["buffer"].get_lines()[self._backend[name]["row"]])

            self._backend[name]["buffer"].set_text(self._backend[name]["row"],
                                                   cur_line_len,
                                                   self._backend[name]["row"],
                                                   cur_line_len,
                                                   '\n')
            self._backend[name]["row"] += 1
            self._backend[name]["column"] = 0
            self._mode = "insert"
        elif char == ord('O'):  # insert line before current
            self._backend[name]["buffer"].set_text(self._backend[name]["row"],
                                                   0,
                                                   self._backend[name]["row"],
                                                   0,
                                                   '\n')
            self._backend[name]["column"] = 0
            self._mode = "insert"
        elif char == ord('w'):  # write file
            self.write_file(name)
        elif char == ord(":"):  # execute code
            self._mode = "execute"

        else:
            self._message = 'Unknown key: {}'.format(char)

    def _handle_code_keypress(self, name, char):
        """handle keypress in code mode"""
        if name not in self._backend.keys():
            return

        if char not in [10, 27, 127]:
            self._query += chr(char)
            self._message = ":"+self._query
            return

        if char == 127:  # backspace
            self._query = self._query[:-1]
            self._message = ":"+self._query
            return

        if not char == 10:  # enter
            return

        if self._query[:5] == "touch":
            for file in self._query[6:].split():
                self.engine.touch_file(file)

        if self._query[:4] == "open":
            for file in self._query[5:].split():
                try:
                    self.get_file(file)
                except FileNotFoundError:
                    self.touch_file(file)

        # if self._query[:2] == "q!":
        #     self._will_exit = True

        if self._query in self._backend.keys():
            self._current = self._query
            self._message = f"opened: '{self._current}'"


        self._mode = "normal"
        self._query = ""
        self._message = ""


    def _handle_insert_keypress(self, name, char):
        """Handle a keypress in insert mode."""
        if name not in self._backend.keys():
            return

        if char == 27:  # Esc
            self._mode = "normal"
        elif char == 127:  # backspace
            if self._backend[name]["column"] == 0 and self._backend[name]["row"] == 0:
                pass  # no effect
            elif self._backend[name]["column"] == 0:
                # join the current line with the previous one
                prev_line = self._backend[name]["buffer"].get_lines()[self._backend[name]["row"] - 1]

                cur_line = self._backend[name]["buffer"].get_lines()[self._backend[name]["row"]]

                self._backend[name]["buffer"].set_text(self._backend[name]["row"] - 1, 0, self._backend[name]["row"],
                                                                            len(cur_line), prev_line + cur_line)
                self._backend[name]["column"] = len(prev_line)
                self._backend[name]["row"] -= 1
            else:
                # remove the previous character
                self._backend[name]["buffer"].set_text(self._backend[name]["row"], self._backend[name]["column"] - 1, self._backend[name]["row"],
                                   self._backend[name]["column"], '')
                self._backend[name]["column"] -= 1
        else:
            # self._message = ('inserted {} at row {} col {}'
            #                  .format(char, self._backend[name]["row"] + 1, self._backend[name]["column"]))
            # self._message = f'"{self._current}"'
            self._backend[name]["buffer"].set_text(self._backend[name]["row"], self._backend[name]["column"], self._backend[name]["row"],
                               self._backend[name]["column"], chr(char))
            if chr(char) == '\n':
                self._backend[name]["row"] += 1
                self._backend[name]["column"] = 0
            else:
                self._backend[name]["column"] += 1


class Editor(Engine):

    def __init__(self, stdscr):
        """create the editor"""
        super().__init__()
        # print(self._mode)
        self._stdscr = stdscr
        self._will_exit = False
        self._scroll_top = 0  # the first line number in the window

    def _draw_gutter(self, num_start, num_rows, last_line_num):
        """Draw the gutter, and return the gutter width."""
        line_nums = range(num_start, num_start + num_rows)
        assert len(line_nums) == num_rows
        gutter_width = max(3, len(str(last_line_num))) + 1
        for y, line_num in enumerate(line_nums):
            if line_num > last_line_num:
                text = '~'.ljust(gutter_width)
            else:
                text = '{} '.format(line_num).rjust(gutter_width)
            self._stdscr.addstr(y, 0, text, curses.A_REVERSE)
        return gutter_width

    def _draw(self):
        """Draw the GUI."""
        self._stdscr.erase()
        height = self._stdscr.getmaxyx()[0]
        width = self._stdscr.getmaxyx()[1]
        self._draw_status_line(0, height - 1, width)
        self._draw_text(0, 0, width, height - 1)
        self._stdscr.refresh()

    def _draw_status_line(self, left, top, width):
        """Draw the status line."""
        # TODO: can't write to bottom right cell
        mode = '{} {}'.format(self._mode.upper(),
                              self._message).ljust(width - 1)
        self._stdscr.addstr(top, left, mode, curses.A_REVERSE)
        position = f'"{self._current}"' if self._current != None else ""
        position += ' LN {}:{} '.format(self._backend[self._current]["row"] + 1,
                                      self._backend[self._current]["column"] + 1)
        self._stdscr.addstr(top, left + width - 1 - len(position), position,
                            curses.A_REVERSE)

    def _get_num_wrapped_lines(self, line_num, width):
        """Return the number of lines the given line number wraps to."""
        return len(self._get_wrapped_lines(line_num, width))

    def _get_wrapped_lines(self, line_num, width, convert_nonprinting=True):
        """Return the wrapped lines for the given line number."""
        def wrap_text(text, width):
            """Wrap string text into list of strings."""
            if text == '':
                yield ''
            else:
                for i in range(0, len(text), width):
                    yield text[i:i + width]
        assert line_num >= 0, 'line_num must be > 0'

        line = self._backend[self._current]["buffer"].get_lines()[line_num]
        if convert_nonprinting:
            line = self._convert_nonprinting(line)
        return list(wrap_text(line, width))

    def _scroll_bottom_to_top(self, bottom, width, height):
        """Return the first visible line's number so bottom line is visible."""
        def verify(top):
            """Verify the result of the parent function is correct."""
            rows = [list(self._get_wrapped_lines(n, width))
                    for n in range(top, bottom + 1)]
            num_rows = sum(len(r) for r in rows)
            assert top <= bottom, ('top line {} may not be below bottom {}'
                                   .format(top, bottom))
            assert num_rows <= height, (
                '{} rows between {} and {}, but only {} remaining. rows are {}'
                .format(num_rows, top, bottom, height, rows))

        top, next_top = bottom, bottom
        # distance in number of lines between top and bottom
        distance = self._get_num_wrapped_lines(bottom, width)

        # move top upwards as far as possible
        while next_top >= 0 and distance <= height:
            top = next_top
            next_top -= 1
            distance += self._get_num_wrapped_lines(max(0, next_top), width)

        verify(top)
        return top

    def _scroll_to(self, line_num, width, row_height):
        """Scroll so the line with the given number is visible."""
        # lowest scroll top that would still keep line_num visible
        lowest_top = self._scroll_bottom_to_top(line_num, width, row_height)

        if line_num < self._scroll_top:
            # scroll up until line_num is visible
            self._scroll_top = line_num
        elif self._scroll_top < lowest_top:
            # scroll down to until line_num is visible
            self._scroll_top = lowest_top

    @staticmethod
    def _convert_nonprinting(text):
        """Replace nonprinting character in text."""
        # TODO: it would be nice if these could be highlighted when displayed
        res = []
        for char in text:
            i = ord(char)
            if char == '\t':
                res.append('->  ')
            elif i < 32 or i > 126:
                res.append('<{}>'.format(hex(i)[2:]))
            else:
                res.append(char)
        return ''.join(res)

    def _draw_text(self, left, top, width, height):
        """Draw the text area."""
        # TODO: handle single lines that occupy the entire window
        highest_line_num = len(self._backend[self._current]["buffer"].get_lines())
        gutter_width = max(3, len(str(highest_line_num))) + 1
        line_width = width - gutter_width  # width to which text is wrapped
        cursor_y, cursor_x = None, None  # where the cursor will be drawn

        # set scroll_top so the cursor is visible
        self._scroll_to(self._backend[self._current]["row"], line_width, height)

        line_nums = range(self._scroll_top, highest_line_num)
        cur_y = top
        trailing_char = '~'

        for line_num in line_nums:

            # if there are no more rows left, break
            num_remaining_rows = top + height - cur_y
            if num_remaining_rows == 0:
                break

            # if all the wrapped lines can't fit on screen, break
            wrapped_lines = self._get_wrapped_lines(line_num, line_width)
            if len(wrapped_lines) > num_remaining_rows:
                trailing_char = '@'
                break

            # calculate cursor position if cursor must be on this line
            if line_num == self._backend[self._current]["row"]:
                lines = self._get_wrapped_lines(line_num, line_width,
                                                convert_nonprinting=False)
                real_col = len(self._convert_nonprinting(
                    ''.join(lines)[:self._backend[self._current]["column"]])
                )
                cursor_y = cur_y + real_col / line_width
                cursor_x = left + gutter_width + real_col % line_width

            # draw all the wrapped lines
            for n, wrapped_line in enumerate(wrapped_lines):
                if n == 0:
                    gutter = '{} '.format(line_num + 1).rjust(gutter_width)
                else:
                    gutter = ' ' * gutter_width
                self._stdscr.addstr(cur_y, left, gutter, curses.A_REVERSE)
                self._stdscr.addstr(cur_y, left + len(gutter), wrapped_line)
                cur_y += 1

        # draw empty lines
        for cur_y in range(int(cur_y), int(top + height)):
            gutter = trailing_char.ljust(gutter_width)
            self._stdscr.addstr(cur_y, left, gutter)

        # position the cursor
        assert cursor_x != None and cursor_y != None
        self._stdscr.move(int(cursor_y + 0), int(cursor_x + 0))

    def main(self):
        """GUI main loop."""
        while not self._will_exit:
            self._draw()
            self._message = ''

            char = self._stdscr.getch()
            if self._mode == 'normal':
                self._handle_normal_keypress(self._current, char)
            elif self._mode == 'insert':
                self._handle_insert_keypress(self._current, char)
            elif self._mode == 'execute':
                self._handle_code_keypress(self._current, char)

            # TODO: get rid of this position clipping
            num_lines = len(self._backend[self._current]["buffer"].get_lines())
            self._backend[self._current]["row"] = min(num_lines - 1, max(0, self._backend[self._current]["row"]))
            # on empty lines, still allow col 1
            num_cols = max(1, len(self._backend[self._current]["buffer"].get_lines()[self._backend[self._current]["row"]]))
            # in insert mode, allow using append after the last char
            if self._mode == 'insert':
                num_cols += 1
            self._backend[self._current]["column"] = min(num_cols - 1, max(0, self._backend[self._current]["column"]))

        self.kill_engine()


@contextmanager
def use_curses():
    """Context manager to set up and tear down curses."""
    stdscr = curses.initscr()
    curses.noecho() # do not echo keys
    curses.cbreak() # don't wait for enter
    try:
        yield stdscr
    finally:
        # clean up and exit
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()


def curses_main(args=None):
    """Start the curses GUI."""
    parser = ArgumentParser(prog=f'{PROGRAM_NAME}', formatter_class=RawDescriptionHelpFormatter,
                            # description=__doc__.format(**main_display.keybindings)
                            )

    path = parser.add_argument('path', nargs='*', default=None,
                               help=("path to file, may include colon \
                                     separated line and col numbers, \
                                     eg '~/Desktop/index.html:10:42'"))

    class EitherOrAction(_StoreTrueAction):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, self.const)
            path.required = False

    parser.add_argument('--rc', action=EitherOrAction,
                        help="display run control file")
    parser.add_argument('--rc-edit', action=EitherOrAction,
                        help="open run control file")
    parser.add_argument('-v', '--version', action=EitherOrAction,
                        help="show version and exit")

    ns = parser.parse_args(args=args)
    if ns.version:
        print("{} v{}".format(f'{PROGRAM_NAME}', __version__))
        return

    with use_curses() as stdscr:
        gui = Editor(stdscr)
        path = ns.path
        if path is not None:
            for part in path:
                if not os.path.exists(part):
                    gui.touch_file(part)
                    gui.get_file(part)
                    gui._current = part

                elif os.path.isdir(part):
                    name, folders, files = next(os.walk(part))
                    for i in files:
                        gui.get_file(part+'/'+i)
                        gui._current = part+'/'+i
                else:
                    gui.get_file(part)
                    gui._current = part

        gui.main()


if __name__ == '__main__':
    curses_main()
