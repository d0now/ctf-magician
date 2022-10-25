from __future__ import annotations
from pathlib import Path
from shutil import rmtree
from typing import Iterator
from termcolor import colored

from .exceptions import CMagInvalidItemConfig
from .config import itemconfig
from .item import Item
from .challenge import ParentOfChallengeMixin
from .file import ParentOfFileMixin
from .manager import register_item
from .defaults import ItemTypes


@itemconfig
class CTFConfig:
    name: str
    type: int = ItemTypes.CTF
    homepage: str = ''


@register_item
class CTF(Item,
          ParentOfFileMixin,
          ParentOfChallengeMixin):
    
    cfgbase = CTFConfig

    @property
    def config(self) -> CTFConfig:
        return super().config

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def homepage(self) -> str:
        return self.config.homepage

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
            self.dump_challenges(),
        ])

    def dump_config(self):
        return '\n'.join([
            f"type     : CTF",
            f"name     : {self.name}",
            f"homepage : {self.homepage if self.homepage else colored('[empty]', color='grey')}",
        ])
