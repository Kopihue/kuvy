from kuvy.args import Args

import sys

def main() -> int:
    args = Args()
    args.read()

    return 0

if __name__ == "__main__":
    sys.exit(main())
