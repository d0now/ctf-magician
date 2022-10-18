from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pathlib import Path

if TYPE_CHECKING:
    from cmag.project import CMagProject
    from cmag.challenge import CMagChallenge

from .model import CMagFileModel

class CMagFile:
    
    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def challenge(self) -> CMagChallenge:
        return self._challenge

    @property
    def id(self) -> int:
        return self._id

    @property
    def record(self) -> CMagFileModel:
        return CMagFileModel.get_by_id(self.id)

    @property
    def path(self) -> Path:
        return Path(self.record.path)

    @property
    def abspath(self) -> Path:
        return self.challenge.files_dir / self.path

    @property
    def root(self) -> int:
        ...

    @property
    def type(self) -> int:
        ...

    def __init__(self, project: CMagProject, challenge: CMagChallenge, id: int):
        self._project = project
        self._challenge = challenge
        self._id = id

    def __repr__(self):
        if self.is_valid():
            return f"<CMagFile id={self.id}>"
        else:
            return f"<CMagFile id={self.id} invalid>"

    def get_record(self) -> Optional[CMagFileModel]:
        return CMagFileModel.get_or_none(id=self.id)

    def is_valid(self):
        return self.get_record() != None and self.exists()

    def exists(self):
        return self.abspath.exists()

    def open(self, *args, **kwargs):
        return self.abspath.open(*args, **kwargs)

    def delete(self):
        if self.exists():
            self.abspath.unlink(missing_ok=True)
        if self.get_record() != None:
            self.record.delete_instance()
