import random
import string
import unittest

from src.interpreter.interpreter import Interpreter


def int_list(lis):
    return [i.value for i in lis]


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class InterpreterTest(unittest.TestCase):

    @staticmethod
    def setup_interpreter(instructions):
        return Interpreter(instructions, stack_size=5, test_mode=True)

    def test_string(self):
        inst1 = """{bee}
nnnnnnn
nnnnn
        """
        i = self.setup_interpreter(inst1)
        self.assertEqual(int_list(i.run()), [98, 101, 101, 0, 0])
        inst2 = """nnnnn
{bruh!}
nnnnn
        """
        i = self.setup_interpreter(inst2)
        self.assertEqual(int_list(i.run()), [98, 114, 117, 104, 33])
        inst3 = """{123}
{45678}
{910}
        """
        for _ in range(100):
            word = random_word(3)
            instrand = "{" + word + "}\nnnnnnnn\nnnnnn"
            i = self.setup_interpreter(instrand)
            self.assertEquals(int_list(i.run()), [ord(i) for i in word] + [0, 0])

    def test_set_top(self):
        for _ in range(100):
            digits = str(random.randint(10, 20))
            inst = "|" + digits + 'nn\nnnnnnnn\nnnnnn'
            i = self.setup_interpreter(inst)
            self.assertEqual(int_list(i.run()), [int(digits)] + [0]*4)

    def test_print_pop(self):
        pass


if __name__ == '__main__':
    unittest.main()
