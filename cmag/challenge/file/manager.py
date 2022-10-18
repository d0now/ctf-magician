from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Iterator
from abc import ABC, abstractproperty
from enum import IntEnum
from pathlib import Path
from shutil import copyfile

import peewee

if TYPE_CHECKING:
    from cmag.project import CMagProject
    from cmag.database import CMagDatabase
    from cmag.challenge.model import CMagChallengeModel

from .file import CMagFile
from .model import CMagFileModel
from .exceptions import *

class CMagFileTypes(IntEnum):
    REGULAR = 1
    DIRECTORY = 2
    ARCHIVE = 3

class CMagFileManagerMixin(ABC):
    
    @property
    @abstractproperty
    def path(self) -> Path:
        ...

    @property
    @abstractproperty
    def project(self) -> CMagProject:
        ...

    @property
    @abstractproperty
    def record(self) -> CMagChallengeModel:
        ...

    @property
    def files_dir(self) -> Path:
        path = self.path / 'files'
        if not path.is_dir():
            path.mkdir(exist_ok=True)
        return path

    def init_files(self):
        CMagFileModel.create_table()

    def add_file(self, src: str | Path, dest: str | Path = '', copy=True, link=False) -> Optional[CMagFile]:
        
        src = Path(src)
        if not src.exists():
            raise CMagFileNotFoundError(f"{src} not found.")

        if not dest:
            dest = Path(src.name)

        if (copy or link) and dest.is_absolute():
            if not dest.is_relative_to(self.files_dir):
                raise CMagFileBadPathError(f"'{dest}' is out of '{self.files_dir}'")
            dest = dest.relative_to(self.files_dir)
        
        try:
            if copy:
                copyfile(src, self.files_dir / dest)
            elif link:
                src.symlink_to(self.files_dir / dest)
        except OSError as exc:
            raise CMagFileCreateError from exc

        if self.get_file_by_path(dest):
            raise CMagFileExistsError(f"'{dest}' already exists.")

        try:
            record = CMagFileModel.create(path=str(dest), root=0, type=CMagFileTypes.REGULAR, challenge=self.record)
        except peewee.IntegrityError as exc:
            raise CMagFileExistsError(f"'{dest}' already exists.")

        return self.get_file_with_check(record.id)

    def get_file(self, id: int) -> Optional[CMagFile]:
        if (record := CMagFileModel.get_or_none(id=id)):
            return CMagFile(self.project, self, record.id)

    def get_file_by_path(self, path: str | Path) -> Optional[CMagFile]:
        if (record := CMagFileModel.get_or_none(path=str(path))):
            return CMagFile(self.project, self, record.id)

    def get_file_with_check(self, id: int) -> CMagFile:
        if not (file := self.get_file(id)):
            raise CMagFileRecordNotFoundError(f"'{id}' record not found.")
        if not file.is_valid():
            raise CMagFileInvalidError(f"'{file.path}' is invalid.")
        return file

    def del_file(self, id: int):

        if (record := CMagFileModel.get_by_id(id)):
            
            if (path := self.files_dir / record.path).exists():
                path.unlink()

            CMagFileModel.delete_by_id(id)

    def del_files(self):
        for record in CMagFileModel.select(CMagFileModel.id):
            self.del_file(record.id)

    def files(self) -> Iterator[Optional[CMagFile]]:
        for record in self.record.files:
            if (file := self.get_file(record.id)):
                yield file
