from argparse import Namespace
from pathlib import Path
from secrets import token_hex
from cmag.item.challenge import Challenge, ChallengeConfig

def main(args: Namespace):

    challenge_path = Challenge.makeat(
        args.path, exist_ok=args.exist_ok,
        **ChallengeConfig(
            name=args.name,
            description=args.description,
            category=args.category
        ).to_dict()
    )

    print(Challenge(challenge_path).path)
    return 0

from .common import items_parser
challenge_parser = items_parser.add_parser('challenge')
challenge_parser.set_defaults(func=main)
challenge_parser.add_argument("name", type=str)
challenge_parser.add_argument("-d", "--description", type=str, default='')
challenge_parser.add_argument("-c", "--category", type=str, default='')
