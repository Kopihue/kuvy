from typing import (
    Iterator,
)
import sys

class Args:
    def __init__(self):
        self.help:      bool         = False
        self.new:       str          = ""
        self.run:       str          = ""
        self.run_args:  list[str]    = []
        self.install:   list[str]    = []
        self.uninstall: list[str]    = []
        self.update:    list[str]    = []
        self.build:     bool         = False
        self.upload:    bool         = False

        self.unknown:   bool         = False

    def read(self):
        def get_arg(args: Iterator) -> None | str:
            try:
                return next(args)
            except StopIteration:
                return None

        args = iter(sys.argv[1:])

        while arg := get_arg(args):
            match arg:
                case "help":
                    self.help = True
                    
                case "new":
                    if arg := get_arg(args):
                        self.new = arg

                case _:
                    self.unknown = True
