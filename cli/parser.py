import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="mypm")

    subparsers = parser.add_subparsers(dest="command")

    # project
    subparsers.add_parser("init")
    subparsers.add_parser("info")
    subparsers.add_parser("doctor")

    # dependency
    add = subparsers.add_parser("add")
    add.add_argument("package")
    add.add_argument("constraint")

    remove = subparsers.add_parser("remove")
    remove.add_argument("package")

    subparsers.add_parser("show")

    # resolution
    subparsers.add_parser("resolve")
    subparsers.add_parser("conflicts")
    subparsers.add_parser("explain")

    # environment
    subparsers.add_parser("install")
    subparsers.add_parser("clean")

    # debug
    subparsers.add_parser("graph")

    return parser.parse_args()