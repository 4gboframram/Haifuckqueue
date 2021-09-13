import string
import sys
import time
from ctypes import c_int16

from .stack import Stack


class FuckingError(Exception):
    def __init__(self, line, line_num, char, stack):
        super().__init__(f"Oops! Something went fucking wrong on line {line_num + 1}: "
                         f"\n\nTraceback (most fucking call last):\n{line!r}\n\n"
                         f"Something went wrong when executing {char!r}.\n\n"
                         f'The most recent stack state before the error was the following:'
                         f'\n{" ".join([str(i.value) for i in stack])}')


class Interpreter:
    followed_by_number = '.|$sdc'  # <>
    single_char_ops = '+-*/&^o!)(#~pan'
    number_chars = string.digits + '@A'

    def __init__(self, instructions, stack_size, debug=False, sleep=None, do_output=True, args=[],
                 do_real_traceback=False, test_mode=False):
        self.stack = Stack(stack_size)
        self.code = instructions.strip()
        self.line_index = 0
        self.line_num = 0

        self.lines = self.code.splitlines()
        self.debug = debug
        self.sleep = sleep
        self.do_output = do_output
        self.do_traceback = do_real_traceback

        def _gen():
            for byte in b'\x00'.join(args):
                yield byte

        self._args = b'\x00'.join(args)
        self.args = _gen()
        self.test_mode = test_mode
        self.check_char_cnt()
        self.check_string_syntax()
        # self.advance()

    @property
    def non_zero_stack(self):
        return c_int16(len([i for i in self.stack if i]))

    @property
    def current_line(self):
        return self.lines[self.line_num]

    @property
    def current_char(self):
        return self.current_line[self.line_index]

    @property
    def arg_len(self):
        return c_int16(len(self._args))

    def check_char_cnt(self):
        *line_lens, = map(len, self.lines)

        *filtered, = filter(lambda x: x not in (0, 5, 7), line_lens)
        if filtered:
            raise SyntaxError(
                f"Line {line_lens.index(filtered[0]) + 1} has {filtered[0]} "
                "characters when it should only have 5 or 7")

        for i in range(0, len(line_lens), 3):
            if line_lens[i:i + 3] != [5, 7, 5]:
                raise SyntaxError(f"Lines {i + 1}-{i + 4} do not follow the 5-7-5 pattern")

    def check_string_syntax(self):
        for line_num, line in enumerate(self.lines):
            for char in line:
                if line.find('}') < line.find('{'):
                    raise SyntaxError(f"Syntax Error on line {line_num}")

                elif '{' in line and '}' not in line:
                    raise SyntaxError("Strings must be terminated on the same line")

    def advance(self, i=1):
        if self.sleep:
            time.sleep(self.sleep)
        for _ in [0] * i:
            self.line_index += 1
            if self.line_index > (p := len(self.current_line) - 1):
                self.line_num += 1
                self.line_index = 0
                if self.debug:
                    print()

            return self.current_char

    def create_string(self):
        i = 0
        while (c := self.current_char) != '}':
            self.stack[i] = c_int16(ord(c))
            i += 1
            self.advance()
        self.advance()

    def create_number(self):
        if self.current_char == '@':
            self.advance()
            return self.non_zero_stack
        elif self.current_char == 'A':
            self.advance()
            return self.arg_len

        digits = ''
        while (c := self.current_char) in string.digits:
            self.advance()
            digits += c

        return c_int16(int(digits))

    def run(self):
        while c := self.current_char:
            try:
                if self.debug:
                    print(c, ' '.join([str(i.value) for i in self.stack]))

                if c == '{':
                    self.advance()
                    self.create_string()
                    # self.advance()
                elif c in Interpreter.followed_by_number:
                    self.advance()
                    num = self.create_number()
                    if c == '$':
                        self.stack.print(num, do_output=self.do_output)
                    elif c == '|':
                        self.stack[0] = num
                    elif c == 's':
                        self.stack.swap(num.value)
                    elif c == '.':
                        if self.stack[0]:
                            self.line_num = num.value - 1
                            self.line_index = 0
                    elif c == 'd':
                        if self.do_output:
                            print(self.stack[num.value].value, end='')
                    elif c == 'c':
                        if self.do_output:
                            print(chr(self.stack[num.value].value), end='')

                elif c in Interpreter.single_char_ops:
                    if c == '+':
                        self.stack.plus()
                    elif c == '-':
                        self.stack.sub()
                    elif c == '*':
                        self.stack.mul()
                    elif c == '/':
                        self.stack.div()
                    elif c == '~':
                        self.stack.not_()
                    elif c == '&':
                        self.stack.and_()
                    elif c == '^':
                        self.stack.xor()
                    elif c == 'o':
                        self.stack.or_()
                    elif c == '(':
                        self.stack.dec()
                    elif c == ')':
                        self.stack.inc()
                    elif c == '#':
                        self.stack.pop(0)
                        self.stack += [c_int16()]
                    elif c == 'p':
                        self.stack.push(0)
                    elif c == '!':
                        self.stack.clear()
                    elif c == 'a':
                        self.stack[0] = c_int16(next(self.args))
                    if self.test_mode:
                        if c == 'n':
                            pass
                    try:
                        self.advance()
                    except IndexError:
                        return self.stack

                else:
                    raise SyntaxError(f"Invalid Operation {c!r}")

            except Exception:
                if self.do_traceback:
                    raise FuckingError(self.current_line, self.line_num, c, self.stack).with_traceback(
                        sys.exc_info()[2])

                def excepthook(t, value, traceback):
                    print('\n' + t.__name__ + ':', value)

                sys.excepthook = excepthook
                raise FuckingError(self.current_line, self.line_num, c, self.stack)
