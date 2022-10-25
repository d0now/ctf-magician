from argparse import Namespace
from pathlib import Path
from cmag.item.file import File, FileConfig

def main(args: Namespace):

    filepath = File.makeat(
        args.file, args.path,
        exist_ok=args.exist_ok,
        symlink=args.symlink,
        link_parent=args.link_parent,
        **FileConfig().to_dict()
    )

    file = File(filepath)

    if args.link_parent:
        print(f"{file.path.parent / args.file.name} -> {file.path}")
    else:
        print(file.path)

    return 0

from .common import items_parser
file_parser = items_parser.add_parser('file')
file_parser.set_defaults(func=main)
file_parser.add_argument("file", type=Path)
file_parser.add_argument("--link-parent", action='store_true')
file_parser.add_argument("--symlink", action='store_true')
