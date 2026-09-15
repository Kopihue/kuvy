import sys

from kopilogs.logs import Log
from kopilogs.paint import paint

from kuvy.static_actions import (
    create_project,
    help,
)
from kuvy.args import KuvyArgs
from kuvy.actions import Kuvy

def main() -> int:
    kuvy_args = KuvyArgs()

    try:
        kuvy_args.read()
    except Exception as e:
        Log(str(e)).error()

    if kuvy_args.static:
        return static_actions(kuvy_args)

    kuvy = Kuvy()

    if kuvy_args.run:
        try:
            kuvy.run(kuvy_args.run)
        except Exception as e:
            Log(str(e)).error()

    return 0

def static_actions(kuvy_args: KuvyArgs) -> int:
    if kuvy_args.new:
        try:
            create_project(kuvy_args.new)
        except Exception as e:
            Log(str(e)).error()
            return 1

        Log(f"Created project: {paint(kuvy_args.new).bold().green()}").success()

    elif kuvy_args.help:
        help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
