import argparse
from pathlib import Path
from termcolor import colored

from .common import handlers_parser
from cmag.item import ItemManager, CTF, Challenge, File
from cmag.item.defaults import ItemTypes

def main(args: argparse.Namespace) -> int:
    
    item = ItemManager.from_path(args.path)
    print(colored(item.path.absolute(), attrs=['bold']))
    
    if hasattr(item, 'dump'):
        print(item.dump())

handler_parser = handlers_parser.add_parser('print')
handler_parser.set_defaults(func=main)
handler_parser.add_argument("-p", "--path", type=Path, default=Path.cwd())
