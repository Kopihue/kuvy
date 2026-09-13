import sys

from kopilogs.logs import Log

from kuvy.static_actions import (
    create_project,
)
from kuvy.args import KuvyArgs

def main() -> int:
    kuvy_args = KuvyArgs()

    try:
        kuvy_args.read()
    except Exception as e:
        Log(str(e)).error()

    if kuvy_args.new and kuvy_args.new_name:
        try:
            create_project(kuvy_args.new_name)
        except Exception as e:
            Log(str(e)).error()

    return 0

if __name__ == "__main__":
    sys.exit(main())
