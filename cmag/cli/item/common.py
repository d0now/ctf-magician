import argparse

from ..common import commands_parser

def main(args: argparse.Namespace) -> int:
    raise NotImplementedError

command_parser = commands_parser.add_parser('item')
command_parser.set_defaults(func=main)

handlers_parser = command_parser.add_subparsers(dest='handler')
