from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List
    from io import IOBase


import sys
from logging import Logger
from pathlib import Path
from peewee import SqliteDatabase

from cmag.database import CMagDatabaseProxy
from cmag.database.models import CMagChallengeModel, CMagFileModel

from cmag.interface.logger import CMagLogger

from cmag.challenge import CMagChallengeManagerMixin

class CMagProjectImpl(CMagChallengeManagerMixin):

    def __init__(self, project_dir:str, log_level: int = CMagLogger.INFO, log_to_stream: IOBase = sys.stderr, log_to_file: str = ''):
        
        self._dir = project_dir
        self.path.mkdir(exist_ok=True)

        self._logger = CMagLogger(log_level=log_level, log_to_stream=log_to_stream, log_to_file=log_to_file)
        self._log = self.logger.log
        self.log.debug("CMagLogger initialized.")

        self._database = SqliteDatabase(self.dbpath)
        self.database.connect(reuse_if_open=True)
        CMagDatabaseProxy.initialize(self.database)

        CMagChallengeModel.create_table()
        CMagFileModel.create_table()

    # properties

    @property
    def dir(self):
        return self._dir

    @property
    def path(self):
        return Path(self.dir)

    @property
    def dbpath(self):
        return self.path / 'project.db'

    @property
    def database(self):
        return self._database

    # logging methods

    @property
    def logger(self) -> CMagLogger:
        return self._logger

    @property
    def log(self) -> Logger:
        return self._log
