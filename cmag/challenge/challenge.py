from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pathlib import Path

if TYPE_CHECKING:
    from cmag.project import CMagProject

from .model import CMagChallengeModel
from .file import CMagFileManagerMixin
from .file.model import CMagFileModel

class CMagChallenge(CMagFileManagerMixin):

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def id(self) -> int:
        return self._id

    @property
    def record(self) -> CMagChallengeModel:
        return CMagChallengeModel.get_by_id(self.id)

    @property
    def name(self) -> str:
        return self.record.name

    @property
    def desc(self) -> str:
        return self.record.desc

    @property
    def path(self) -> Path:
        path = self.project.path / 'challenges' / str(self.id)
        return path

    def __init__(self, project: CMagProject, id: int):
        self._project = project
        self._id = id
        self.path.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return f"<CMagChallenge id={self.id}>"

    def set(self, **update) -> Any:
        query = CMagChallengeModel.update(**update).where(id=self.id)
        return query.execute()

    def get_record(self) -> Optional[CMagFileModel]:
        return CMagFileModel.get_or_none(id=self.id)

    def is_valid(self):
        return self.get_record() != None

    def delete(self):
        if self.get_record() != None:
            self.record.delete_instance()
