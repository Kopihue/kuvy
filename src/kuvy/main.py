from kuvy.args import Args
from kuvy.actions import (
    Actions,
    help,
    new,
)

import sys

def main() -> int:
    args = Args()
    args.read()

    if args.help:
        print("help")
        return 0

    elif args.new:
        try:
            new(args.new)
        except FileExistsError as e:
            print(e)
            return 1

        if args.new == "project":
            print("Project name not specified, falling back to \"project\"")

        print(f"Succesfully created \"{args.new}\"!")
        return 0

    try:
        actions = Actions()
    except FileNotFoundError as e:
        print(e)
        return 1

    if args.run:
        try:
            actions.run(args.run, args=args.run_args)
        except ValueError as e:
            print(e)

    return 0

if __name__ == "__main__":
    sys.exit(main())
