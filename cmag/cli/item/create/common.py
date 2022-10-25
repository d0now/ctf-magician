import argparse
import os
from pathlib import Path

from ..common import handlers_parser

def main(args: argparse.Namespace) -> int:
    raise NotImplementedError

handler_parser = handlers_parser.add_parser('create')
handler_parser.set_defaults(func=main)
handler_parser.add_argument("-p", "--path", type=Path, default=Path.cwd())
handler_parser.add_argument("--exist-ok", action='store_true')

items_parser = handler_parser.add_subparsers(dest='item', required=True)
