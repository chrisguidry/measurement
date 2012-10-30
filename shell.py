#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import atexit
import code
import os.path
import readline
import sys

class MeasurementConsole(code.InteractiveConsole):
    def __init__(self, shell_locals=None):
        shell_locals = shell_locals or {}

        import measurement
        classes = []
        for attribute in dir(measurement):
            value = getattr(measurement, attribute)
            if isinstance(value, type):
                shell_locals[attribute] = value
                classes.append(value)

        classes = tuple(classes)
        for attribute in dir(measurement):
            value = getattr(measurement, attribute)
            if isinstance(value, classes):
                shell_locals[attribute] = value

        self.init_history(os.path.expanduser("~/.measurement_history"))

        code.InteractiveConsole.__init__(self, shell_locals)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)

def shell():
    shell_locals = {}
    console = MeasurementConsole(shell_locals)
    console.interact("Welcome to measurement's interactive Python shell.")

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "..")))
    shell()
