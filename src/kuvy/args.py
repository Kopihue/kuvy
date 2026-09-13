from typing import Iterator
import sys

class KuvyArgs:
    def __init__(self):
        self.new: None | bool = None
        self.new_name: None | str = None

    def read(self):
        def get_arg(args: Iterator) -> str | None:
            try:
                return next(args)
            except StopIteration:
                return None

        args = iter(sys.argv[1:])

        while arg := get_arg(args):
            match arg:
                case "new":
                    self.new = True

                    if arg := get_arg(args):
                        self.new_name = arg
                    else:
                        raise ValueError("\"new\" requires the project name to create it!")
