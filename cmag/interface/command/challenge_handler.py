from argparse import ArgumentParser, _SubParsersAction, Namespace
from pathlib import Path
from .utils import open_project, open_challenge


# challenge ... {subcommand}

def challenge_handler(args):
    raise NotImplementedError

def challenge_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_handler)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--name", type=str)
    group.add_argument("-i", "--id", type=int)


# challenge ... add ...

def challenge_add_handler(args):
    project = open_project(args)
    challenge = project.add_challenge(dict(name=args.name))
    if not challenge:
        print("failed.")
    else:
        print("done.")

def challenge_add_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_add_handler)
    parser.add_argument("name")


# challenge ... list ...

def challenge_list_handler(args):
    
    from termcolor import colored
    
    project = open_project(args)
    if not project:
        print("failed.")
        return -1
    
    print(colored(f"{'id':4} | name", attrs=['bold']))
    for challenge in project.challenges():
        print(f"{str(challenge.id):4} | {challenge.name}")

    return 0

def challenge_list_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_list_handler)
    parser.add_argument("--with-files", action='store_true')


# challenge ... info ...

def challenge_info_handler(args):
    
    project = open_project(args)
    if not project:
        print("failed.")
        return -1

    if args.id:
        challenge = project.get_challenge(args.id)
    elif args.name:
        challenge = project.get_challenge_by_name(args.name)
    else:
        print("failed.")
        return -1

    if not challenge:
        print("failed.")
        return -1

    # TODO: improve this.
    print(challenge)

    return 0

def challenge_info_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_info_handler)

# challenge ... remove ...

def challenge_remove_handler(args):

    project = open_project(args)
    if not project:
        print("failed.")
        return -1

    if args.id:
        challenge = project.get_challenge(args.id)
    elif args.name:
        challenge = project.get_challenge_by_name(args.name)
    else:
        raise Exception

    if not challenge:
        print("failed.")
        return -1

    if not project.del_challenge(challenge.id):
        print("failed.")
        return -1

    print("done.")
    return 0

def challenge_remove_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_remove_handler)


# challenge ... file ... {subcommand}

def challenge_file_handler(args):
    raise NotImplementedError

def challenge_file_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_handler)

# challenge ... file ... create ...

def challenge_file_create_handler(args):
    
    if not (challenge := open_challenge(args)):
        print("failed.")
        return -1

    if not (file := challenge.add_file(args.path, args.destination, not args.dont_copy, args.link)):
        print("failed.")
        return -1

    print(file.path)
    return 0

def challenge_file_create_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_create_handler)
    parser.add_argument("path", type=Path)
    parser.add_argument("-d", "--destination", type=Path)
    parser.add_argument("-c", "--dont-copy", action='store_true')
    parser.add_argument("-l", "--link", action='store_true')


# challenge ... file ... add ...

def challenge_file_add_handler(args):
    
    if not (challenge := open_challenge(args)):
        print("failed.")
        return -1

    if not (file := challenge.add_file(args.path, args.dest)):
        print("failed.")
        return -1

    print(file.path)
    return 0

def challenge_file_add_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_add_handler)
    parser.add_argument("path", type=Path)
    parser.add_argument("-d", "--dest", type=Path)


# challenge ... file ... list ...

def challenge_file_list_handler(args):
    
    from termcolor import colored

    if not (challenge := open_challenge(args)):
        print("failed.")
        return -1

    print(colored(f"{'id':4} | name", attrs=['bold']))
    for file in challenge.files():
        print(f"{str(file.id):4} | {file.path}")

    return 0

def challenge_file_list_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_list_handler)


# challenge ... file ... remove ...

def challenge_file_remove_handler(args):
    
    if not (challenge := open_challenge(args)):
        print("failed.")
        return -1

    if (file := challenge.get_file_by_path(args.path)):
        file.delete()

def challenge_file_remove_argparse(parser: ArgumentParser):
    parser.set_defaults(func=challenge_file_remove_handler)
    parser.add_argument("path", type=Path)


# factory

def factory_challenge_subparsers(parser: ArgumentParser,
                                 interface_subparsers: _SubParsersAction,
                                 command_subparsers: _SubParsersAction):


    challenge_subparser = command_subparsers.add_parser("challenge")
    challenge_argparse(challenge_subparser)

    # challenge {subcommand}
    subcommand_subparsers = challenge_subparser.add_subparsers(title='subcommand', required=True)

    # challenge add ...
    add_subcommand_subparser = subcommand_subparsers.add_parser("add")
    challenge_add_argparse(add_subcommand_subparser)
    
    # challenge list ...
    list_subcommand_subparser = subcommand_subparsers.add_parser("list")
    challenge_list_argparse(list_subcommand_subparser)

    # challenge info ...
    info_subcommand_subparser = subcommand_subparsers.add_parser("info")
    challenge_info_argparse(info_subcommand_subparser)

    # challenge remove ...
    remove_subcommand_subparser = subcommand_subparsers.add_parser("remove")
    challenge_remove_argparse(remove_subcommand_subparser)


    # challenge file ...
    file_subparser = subcommand_subparsers.add_parser("file")
    challenge_file_argparse(file_subparser)

    # challenge file {file_subcommand}
    file_subcommand_subparsers = file_subparser.add_subparsers(title="file_subcommand", required=True)

    # challenge file create ...
    file_create_subcommand_subparser = file_subcommand_subparsers.add_parser("create")
    challenge_file_create_argparse(file_create_subcommand_subparser)

    # challenge file add ...
    file_add_subcommand_subparser = file_subcommand_subparsers.add_parser("add")
    challenge_file_add_argparse(file_add_subcommand_subparser)

    # challenge file path ...
    file_list_subcommand_subparser = file_subcommand_subparsers.add_parser("list")
    challenge_file_list_argparse(file_list_subcommand_subparser)

    # challenge file remove ...
    file_remove_subcommand_subparser = file_subcommand_subparsers.add_parser("remove")
    challenge_file_remove_argparse(file_remove_subcommand_subparser)
