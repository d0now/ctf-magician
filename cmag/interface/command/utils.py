from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Optional

import sys
from io import IOBase
from cmag.project import CMagProject
from cmag.interface.logger import CMagLogger

def open_project(args):

    log_level: int = getattr(CMagLogger, args.log_level.upper())

    if args.log_stream == 'null':
        log_stream: Optional[IOBase] = None
    else:
        log_stream: Optional[IOBase] = getattr(sys, args.log_stream)

    log_file = args.log_file

    return CMagProject(args.project, log_level=log_level, log_to_stream=log_stream, log_to_file=log_file)

def open_challenge(args):

    project = open_project(args)
    if not project:
        return None

    if args.id:
        return project.get_challenge(args.id)
    elif args.name:
        return project.get_challenge_by_name(args.name)