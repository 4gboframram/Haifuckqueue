from ctypes import c_int16


class Stack(list):
    def __init__(self, size):
        self.size = size
        super().__init__([c_int16()] * size)

    def print(self, num, do_output=True):
        for i in range(num.value):
            c = self.pop(0)
            if do_output:
                print(chr(c.value), end='')
            self.__iadd__([c_int16()])

    def plus(self):
        self[2] = c_int16(self[0].value + self[1].value)

    def sub(self):
        self[2] = c_int16(self[0].value - self[1].value)

    def mul(self):
        self[2] = c_int16(self[0].value * self[1].value)

    def div(self):
        self[2] = c_int16(self[0].value // self[1].value)

    def or_(self):
        self[2] = c_int16(self[0].value | self[1].value)

    def and_(self):
        self[2] = c_int16(self[0].value & self[1].value)

    def xor(self):
        self[2] = c_int16(self[0].value ^ self[1].value)

    def not_(self):
        self[0] = c_int16(~self[0].value)

    def swap(self, pos):
        self[0], self[pos - 1] = self[pos - 1], self[0]

    def inc(self):
        self[0] = c_int16(self[0].value + 1)

    def dec(self):
        self[0] = c_int16(self[0].value - 1)

    def push(self, value):
        self.insert(0, c_int16(value))
        self.pop(-1)
