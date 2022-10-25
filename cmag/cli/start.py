from .common import parser
from .item import *

def start():
    args = parser.parse_args()
    exit_code = args.func(args)
    exit(exit_code)
