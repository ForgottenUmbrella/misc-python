"""Handle input and output cleanly."""
import sys
import platform

try:
    from msvcrt import getwch as getch
except ImportError:
    import tty
    import termios

    def getwch():
        """Return a single character from user input without echoing.

        ActiveState code, adapted from
        <http://code.activestate.com/recipes/134892> by Danny Yoo under
        the Python Software Foundation license.

        """
        file_descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_descriptor)
        try:
            tty.setraw(file_descriptor)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
        return char


if platform.system() == 'Windows':
    try:
        import colorama
    except ImportError:
        import ctypes
        KERNEL32 = ctypes.windll.kernel32
        # Enable ANSI support (for Windows 10 >= v1511)
        KERNEL32.SetConsoleMode(KERNEL32.GetStdHandle(-11), 7)
    else:
        colorama.init()
else:
    import readline


class TempHistory:
    """Record one line from the terminal.

    Note: I use the term 'echo' to refer to when text is
    shown on the terminal but might not be written to 'sys.stdout'.

    """

    def __init__(self):
        """Initialise 'line' and save the 'print' and 'input' functions.

        'line' is initially set to '\n' so that the 'record' method
        doesn't raise an error about the string index being out of range.

        """
        self.line = '\n'
        self.builtin_print = print
        self.builtin_input = input

    def _record(self, text):
        """Append to 'line' or overwrite it if it has ended."""
        if text == '':
            return
        lines = text.split('\n')
        if text[-1] == '\n':
            last_line = lines[-2] + '\n'
        else:
            last_line = lines[-1]
        last_line = last_line.split('\r')[-1]
        if self.line[-1] == '\n':
            self.line = last_line
        else:
            self.line += last_line

    def _undo_newline(self):
        """Move text cursor back to its position before echoing newline.

        ANSI escape sequence: '\x1b[{count}{command}'
        '\x1b' is the escape code, and commands 'A', 'B', 'C' and 'D' are
        for moving the text cursor up, down, forward and backward {count}
        times respectively.

        Thus, after having echoed a newline, the final statement tells
        the terminal to move the text cursor forward to be inline with
        the end of the previous line, and then move up into said line
        (making it the current line again).

        """
        line_length = len(self.line)
        for i, char in enumerate(self.line[1:]):
            if char == '\b' and self.line[i-1] != '\b':
                line_length -= 2
        self.print('\x1b[{}C\x1b[1A'.format(line_length),
                   end='', flush=True, record=False)

    def print(self, *args, sep=' ', end='\n', file=sys.stdout, flush=False,
              record=True):
        """Print to 'file' and record the printed text.

        Other than recording the printed text, it behaves exactly like
        the built-in 'print' function.

        """
        self.builtin_print(*args, sep=sep, end=end, file=file, flush=flush)
        if record:
            text = sep.join([str(arg) for arg in args]) + end
            self._record(text)

    def input(self, prompt='', newline=True, record=True):
        """Return one line of user input and record the echoed text.

        Other than storing the echoed text and optionally stripping the
        echoed newline, it behaves exactly like the built-in 'input'
        function.

        """
        if prompt == '':
            prompt = ' \b'
        response = self.builtin_input(prompt)
        if record:
            self._record(prompt)
            self._record(response)
        if not newline:
            self._undo_newline()
        return response


class TerminalHistory(TempHistory):
    """Record ALL the lines from the terminal (from instantiation onwards)."""

    def __init__(self):
        """Initialise the list of terminal lines."""
        self.lines = ['']
        super().__init__()
        self.line = ''

    @property
    def line(self):
        """Return the last line."""
        return self.lines[-1]

    @line.setter
    def line(self, text):
        """Set the last line."""
        self.lines[-1] = text

    def _record(self, text):
        """Append to 'text' to 'line' or 'lines'.

        Overrides TempHistory's 'record' method, preventing overwriting when
        the line is finished and instead simply creating another line.

        """
        if text == '' or text == ' \b':
            return
        lines = [line.split('\r')[-1] + '\n' for line in text.split('\n') if line]
        if text[-1] != '\n':
            lines[-1] = lines[-1][:-1]
        for line in lines:
            if self.line == '':
                self.line = line
            elif self.line[-1] == '\n':
                self.lines.append(line)
            else:
                self.line += line


def valid_input(prompt='', valids=None, default=None):
    """Return values from input only if they are considered valid."""
    if valids is None:
        valids = {
            False: ['n', 'false', '0'],
            True: ['y', 'true', '1']
        }
    try:
        valids[True]
    except KeyError:
        valids[True] = ['y', 'true', '1']
    try:
        valids[False]
    except KeyError:
        valids[False] = ['n', 'false', '0']
    if default is None:
        default = valids[True][0]

    while True:
        print('{} {}'.format(prompt, default), end='\b' * len(default))
        answer = input().lower()
        if not answer:
            answer = default
        for key in valids:
            for subval in valids[key]:
                if subval in answer:
                    return key
        print('Invalid input: {}'.format(answer))


def gram_join(string, splitter=' ', joiner=', ', final_joiner=', and '):
    """Join a string as specified."""
    string_as_list = string.split(splitter)
    first_section = joiner.join(string_as_list[:-1])
    return final_joiner.join([first_section, string_as_list[-1]])


def pluralise(count, single, plural=None):
    """Return the plural form of a word if count is not 1."""
    if plural is None:
        if single[-1] == 's':
            if single == 'is':
                plural = 'are'
            else:
                plural = single + 'ses'
        else:
            plural = single + 's'

    if count == 1:
        return single
    else:
        return plural
