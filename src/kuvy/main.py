from kuvy.args import Args
from kuvy.actions import (
    ActionsPip,
    ActionsKuvy,
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

        print(f"Succesfully created \"{args.new}\"!")
        return 0

    try:
        actions_kuvy = ActionsKuvy()
        actions_pip = ActionsPip()
    except FileNotFoundError as e:
        print(e)
        return 1

    if args.run:
        try:
            actions_kuvy.run(args.run, args=args.run_args)
        except ValueError as e:
            print(e)

    elif args.install:
        actions_pip.install(args.install)

    elif args.uninstall:
        actions_pip.uninstall(args.uninstall)

    elif args.upgrade:
        actions_pip.upgrade(args.upgrade)

    return 0

if __name__ == "__main__":
    sys.exit(main())
