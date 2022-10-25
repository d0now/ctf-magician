from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from shutil import rmtree
from typing import Iterator
from termcolor import colored

from .config import itemconfig
from .item import Item
from .file import ParentOfFileMixin
from .manager import register_item
from .defaults import ItemTypes
from .exceptions import CMagInvalidItemConfig


@itemconfig
class ChallengeConfig:
    name: str
    type: int = ItemTypes.CHALLENGE
    description: str = ''
    category: str = ''


@register_item
class Challenge(Item, ParentOfFileMixin):

    cfgbase = ChallengeConfig

    @property
    def config(self) -> ChallengeConfig:
        return super().config

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def description(self) -> str:
        return self.config.description

    @property
    def category(self) -> str:
        return self.config.category

    @classmethod
    def makeat(cls, _path: str | Path, exist_ok=False, **config) -> Path:

        path = Path(_path)

        if 'name' not in config:
            raise CMagInvalidItemConfig

        if not path.is_dir():
            raise FileNotFoundError(path)

        return super().makeat(path / config['name'], exist_ok, **config)

    def dump(self):
        return '\n'.join([
            self.dump_config(),
            self.dump_files()
        ])

    def dump_config(self):
        return '\n'.join([
            f"type        : Challenge",
            f"name        : {self.name}",
            f"description : {self.description if self.description else colored('[empty]', color='grey')}",
            f"category    : {self.category    if self.category    else colored('[empty]', color='grey')}",
        ])
    

class ParentOfChallengeMixin(ABC):

    @abstractmethod
    def iter_childs(self) -> Iterator[Item]:
        ...

    def iter_challenges(self) -> Iterator[Challenge]:
        for child in self.iter_childs():
            if child.type == ItemTypes.CHALLENGE:
                yield child

    def has_challenge(self) -> bool:
        for _ in self.iter_challenges():
            return True
        return False

    def get_challenge(self, name: str) -> Challenge | None:
        for challenge in self.iter_challenges():
            if challenge.name == name:
                return challenge

    def remove_challenge(self, name: str) -> Path | None:
        for challenge in self.iter_challenges():
            if challenge.name == name:
                rmtree(challenge.path)
                return challenge.path

    def dump_challenges(self):
        ret = []
        ret.append(f"count : {len(list(self.iter_challenges()))}")
        return '\n'.join(ret)
