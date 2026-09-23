from kuvy.args import Args

import sys

def main() -> int:
    args = Args()
    args.read()

    print(args.help)
    print(args.new)

    return 0

if __name__ == "__main__":
    sys.exit(main())
