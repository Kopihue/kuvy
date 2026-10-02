from kuvy.args import Args
from kuvy.actions import (
    ActionsPip,
    ActionsKuvy,
    help,
    new,
)

from kopilogs import log, Log
from kopilogs import paint
Log.text = True

import sys

def main() -> int:
    args = Args()
    args.read()

    if args.unknown:
        log("Not a valid option: try \"help\"").warning()
        return 1

    elif args.help:
        print("help")
        return 0

    elif args.new:
        try:
            new(args.new)
        except FileExistsError as e:
            log(e).error()
            return 1

        log(
            f"Successfully created:",
            paint(args.new).bold().green(),
        ).success()
        return 0

    try:
        actions_kuvy = ActionsKuvy()
        actions_pip = ActionsPip()
    except RuntimeError as e:
        log(e).error()
        return 1
    except FileNotFoundError as e:
        log(e).error()
        return 1

    if args.run:
        try:
            actions_kuvy.run(args.run, args=args.run_args)
        except ValueError as e:
            log(e).error()

    elif args.install:
        actions_pip.install(args.install)

    elif args.uninstall:
        actions_pip.uninstall(args.uninstall)

    elif args.upgrade:
        actions_pip.upgrade(args.upgrade)

    return 0

if __name__ == "__main__":
    sys.exit(main())
