from __future__ import annotations
from abc import ABC
from pathlib import Path
from shutil import rmtree
from typing import Iterator, Type

from .base import ItemBase
from .config import DefaultConfig
from .manager import ItemManager
from .defaults import *
from .exceptions import *


class Item(ItemBase):

    cfgbase = None

    @property
    def type(self) -> int:
        return self.cfgbase.type

    @property
    def path(self) -> Path:
        return Path(self._path)

    @property
    def config(self) -> Type[DefaultConfig]:
        cfgdata = (self.path / ITEM_CONFIG_FILENAME).read_text()
        return self.cfgbase.from_json(cfgdata)

    @classmethod
    def validate(cls, _path: str | Path):

        if not cls.cfgbase:
            raise CMagItemNotImplemented

        if issubclass(cls.cfgbase, DefaultConfig):
            raise CMagItemNotImplemented

        if not (path := Path(_path)).is_dir():
            raise CMagInvalidItemPath

        if not (cfgpath := path / ITEM_CONFIG_FILENAME).exists():
            raise CMagInvalidItemPath

        if not (cfgdata := cfgpath.read_text()):
            raise CMagInvalidItemConfig

        if not (config := cls.cfgbase.from_json(cfgdata)):
            raise CMagInvalidItemConfig

        if cls.cfgbase.type != config.type:
            raise CMagInvalidItemConfig

    @classmethod
    def check(cls, path: str | Path) -> bool:
        try: 
            cls.validate(path)
            return True
        except CMagItemException:
            return False

    @classmethod
    def makeat(cls, _path: str | Path, exist_ok=False, **_config):
        
        path = Path(_path)
        path.mkdir(exist_ok=exist_ok)

        config = cls.cfgbase.from_dict(_config)
        if cls.cfgbase.type != config.type:
            raise CMagInvalidItemConfig

        (path / ITEM_CONFIG_FILENAME).write_text(config.to_json())

    def __gt__(self, target: str) -> Item:
        return ItemManager.from_path(self.path / target)

    def has_parent(self) -> bool:
        return ItemManager.check_item_type(self.path.parent) != None

    def get_parent(self) -> Item:
        return ItemManager.from_path(self.path.parent)

    def iter_childs(self) -> Iterator[Item]:
        for path in self.path.iterdir():
            if ItemManager.check_item_type(path):
                yield ItemManager.from_path(path)

    def has_child(self) -> bool:
        return len(self.iter_childs()) != 0

    def get_child(self, name: str = '') -> Item | None:
        for child in self.iter_childs():
            if child.path.name == name:
                return child

    def remove_child(self, name: str) -> Path | None:
        for child in self.iter_childs():
            if child.path.name == name:
                rmtree(child.path)
                return child.path
