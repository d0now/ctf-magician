from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from io import IOBase
    from typing import Any

import sys
from cmag.interface.logger import CMagLogger
from .project_impl import CMagProjectImpl

class CMagProject(CMagProjectImpl):

    def __init__(self, project_dir:str,
                       log_level: int = CMagLogger.INFO,
                       log_to_stream: IOBase = sys.stderr,
                       log_to_file: str = '',
                       load_all: bool = True):

        super().__init__(project_dir, log_level=log_level, log_to_stream=log_to_stream, log_to_file=log_to_file)

    def __repr__(self) -> str:
        return f"<CMagProject path={self.dir}>"