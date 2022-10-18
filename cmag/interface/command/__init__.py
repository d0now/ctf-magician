from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from .project_handler import factory_project_subparsers
from .challenge_handler import factory_challenge_subparsers
from .plugin_handler import factory_plugin_subparsers

def factory_cli_subparsers(parser: ArgumentParser, interface_subparsers: _SubParsersAction):
    
    cli_subparser = interface_subparsers.add_parser("cli")
    cli_subparser.add_argument("-p", "--project", type=Path, default=Path("."), required=True)
    cli_subparser.add_argument("--log-level", choices=['debug', 'info', 'warning', 'error', 'critical'], default='info')
    cli_subparser.add_argument("--log-stream", choices=['stdout', 'stderr', 'null'], default='stdout')
    cli_subparser.add_argument("--log-file", type=Path)

    command_subparsers = cli_subparser.add_subparsers(title='command', required=True)
    factory_project_subparsers(parser, interface_subparsers, command_subparsers)
    factory_challenge_subparsers(parser, interface_subparsers, command_subparsers)
    factory_plugin_subparsers(parser, interface_subparsers, command_subparsers)
