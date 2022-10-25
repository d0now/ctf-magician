from argparse import Namespace
from .common import items_parser
from cmag.item.ctf import CTF, CTFConfig

def main(args: Namespace):

    ctf_path = CTF.makeat(
        args.path, args.exist_ok,
        **CTFConfig(
            name=args.name,
            homepage=args.homepage
        ).to_dict()
    )

    print(CTF(ctf_path).path)
    return 0


ctf_parser = items_parser.add_parser('ctf')
ctf_parser.set_defaults(func=main)
ctf_parser.add_argument("name", type=str)
ctf_parser.add_argument("-H", "--homepage", type=str, default='')