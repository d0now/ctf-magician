from typing import TYPE_CHECKING, Iterator, Optional
from abc import ABC, abstractproperty

import peewee
from pathlib import Path
from logging import Logger

if TYPE_CHECKING:
    from cmag.project import CMagProject
    from cmag.database import CMagDatabase

from .challenge import CMagChallenge
from .model import CMagChallengeModel
from. exceptions import *

class CMagChallengeManagerMixin(ABC):

    def add_challenge(self, fields: dict = {}) -> Optional[CMagChallenge]:
        
        try:
            record = CMagChallengeModel.create(**fields)
        except peewee.IntegrityError as exc:
            raise CMagChallengeExistsError from exc

        return CMagChallenge(self, record.id)

    def get_challenge(self, id: int) -> Optional[CMagChallenge]:
        if (record := CMagChallengeModel.get_or_none(id=id)):
            return CMagChallenge(self, record.id)

    def get_challenge_by_name(self, name: str) -> Optional[CMagChallenge]:
        if (record := CMagChallengeModel.get_or_none(name=name)):
            return CMagChallenge(self, record.id)

    def get_challenge_with_check(self, id: int) -> CMagChallenge:
        if not (challenge := self.get_challenge(id)):
            raise CMagChallengeNotFoundError(f"'{id}' not found.")
        return challenge

    def del_challenge(self, id: int) -> bool:
        if (challenge := self.get_challenge(id)):
            challenge.del_files()
            CMagChallengeModel.delete_by_id(id)

    def challenges(self) -> Iterator[Optional[CMagChallenge]]:
        for record in CMagChallengeModel.select(CMagChallengeModel.id):
            if (challenge := self.get_challenge(record.id)):
                yield challenge
