from __future__ import print_function
import signal,copy,sys,time
from random import randint

'''
This class gets input from the user
'''
class GetchUnix:
    def __init__(self):
        import tty

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
