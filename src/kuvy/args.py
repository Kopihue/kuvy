import sys

class Args:
    def __init__(self):
        self.help: bool = False
        self.new: None | str = None
        self.run: None | str = None
        self.run_args: list[str] = []

    def read(self):
        args = iter(sys.argv[1:])

