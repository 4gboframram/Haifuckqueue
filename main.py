# A stack-based esoteric programming language which has more arbitrary  formatting than pep8
# Lines must be length 5,7,5 #
# +-*/&^o: perform the operation on the top 2 items of the stack #
# and set the third item on the stack to the result.
# Division is floor division, o is or
# .[number] Go to that line number if tos is not 0 #
# |[number] set tos to that value #
# $[number] Print the top [number] items on the stack as their character and pop them from the stack. No newline.
# d [number] Print value of [number]th item of the stack #
# s[number] Swap tos and the [number]th item on the stack #
# ~ Convert tos to binary not of tos #

# >< [number] Go forward/back [number] instructions

# {string} Set the top len(string) items on the stack to be the values of the characters of the string.
# Has to be terminated on the same line. #
# @ represents the number of non-zero items on the stack. Can be used in place of [number] #
# ! Set the entire stack to 0 #
# # Pop tos #
# )( Increment/Decrement tos #

# a Set tos to be the next byte in args. If there are no more bytes, raise an exception.
# A Total byte count of sys.argv, including null bytes

# p Push a 0 onto the tos
# c [number] Print the [number]th item on the stack as a string
# Arguments will separated by null bytes
# All numbers and strings must be terminated on the same line

import sys

from src.interpreter.interpreter import Interpreter
import argparse
parser = argparse.ArgumentParser(description='The cmdline arg parser for haifuckyou')
parser.add_argument('file', metavar='file', type=str, nargs=1,
                    help='The file to run.')
parser.add_argument('--stacksize', metavar='[size]', type=int, nargs=1, default=[256],
                    help='The size of stack to use. The default size is 256')
parser.add_argument('--args', type=str, nargs='+',
                    help='Arguments for input', default=[])
parser.add_argument('--debug', help='Print stack before every stack operation',
                    action='store_true')
parser.add_argument('--sleep', metavar='[time]', type=float,
                    help='Amount of time to sleep between operations. Useful for debugging')
parser.add_argument('--noout', action='store_true',
                    help="Don't do console output")
parser.add_argument('--traceback', action='store_true',
                    help="Whether to use Python's actual exception traceback. "
                         "Should not be used unless you think you've found a bug with the interpreter")
if __name__ == "__main__":

    args = parser.parse_args()

    with open(args.file[0]) as f:
        inst = f.read()

        i = Interpreter(inst, args.stacksize[0], args.debug, args.sleep,
                        not args.noout, [i.encode() for i in args.args], args.traceback)
        i.run()
    hello_world = """
{Hel}
$3{lo }
$3{W}
$1{o}
$1{rld}
$3{!}
$1|10
$1ooooo
ooooo 
"""

