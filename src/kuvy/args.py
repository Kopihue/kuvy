from typing import Iterator
import sys

class KuvyArgs:
    def __init__(self):
        self.static: bool = False
        self.new: None | str = None
        self.help: None | bool = None
        self.run: None | str = None

    def read(self):
        def get_arg(args: Iterator) -> str | None:
            try:
                return next(args)
            except StopIteration:
                return None

        args = iter(sys.argv[1:])
        arg = get_arg(args)

        if not arg:
            self.static = True
            self.help = True
            return

        match arg:
            case "new":
                self.static = True

                if arg := get_arg(args):
                    self.new = arg
                else:
                    raise ValueError("\"new\" requires the project name to create it!")

            case "help":
                self.static = True
                self.help = True

            case "run":
                if arg := get_arg(args):
                    self.run = arg
                else:
                    self.run = "main"

            case _:
                self.static = True
                self.help = True
