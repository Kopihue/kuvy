from kuvy.args import Args
from kuvy.actions import (
    help,
    new,
)

import sys

def main() -> int:
    args = Args()
    args.read()

    if args.help:
        return 0

    elif args.new:
        try:
            new(args.new)
        except FileExistsError as e:
            print(e)
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())
