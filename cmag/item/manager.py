from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Type, TypeVar
from pathlib import Path

from .defaults import ITEM_CONFIG_FILENAME
from .exceptions import *

if TYPE_CHECKING:
    from .item import Item


class ItemManager:

    _itemclasses: List[Type[Item]] = []

    @classmethod
    def register(cls, itemclass: Item) -> None:

        from .item import Item

        if not issubclass(itemclass, Item):
            raise CMagItemNotImplemented

        if cls.has_item_of_type(itemclass.type):
            raise CMagItemExists

        cls._itemclasses.append(itemclass)

    @classmethod
    def unregister(cls, type: int) -> None:
        if (item := cls.get_item_of_type(type)):
            cls._itemclasses.remove(item)

    @classmethod
    def get_item_of_type(cls, type: int) -> Type[Item] | None:
        for registered in cls._itemclasses:
            if registered.cfgbase.type == type:
                return registered

    @classmethod
    def has_item_of_type(cls, type: int) -> bool:
        return cls.get_item_of_type(type) != None

    @classmethod
    def get_item_type(cls, _path: str | Path) -> int:
        
        from json import load, JSONDecodeError

        path = Path(_path)
        if not path.is_dir():
            raise CMagInvalidItemPath

        if not (cfgpath := path / ITEM_CONFIG_FILENAME).is_file():
            raise CMagInvalidItemPath

        try:
            with cfgpath.open() as f:
                config = load(f)
        except OSError as exc:
            raise CMagInvalidItemPath from exc
        except JSONDecodeError as exc:
            raise CMagInvalidItemConfig from exc

        if 'type' not in config:
            raise CMagInvalidItemConfig

        return config['type']

    @classmethod
    def validate_item_type(cls, _path: str | Path) -> int:
        item_type = cls.get_item_type(_path)
        if not cls.has_item_of_type(item_type):
            raise CMagItemTypeNotFound
        return item_type

    @classmethod
    def check_item_type(cls, _path: str | Path) -> int | None:
        try:
            return cls.validate_item_type(_path)
        except CMagItemException:
            return None

    @classmethod
    def from_path(cls, _path: str | Path) -> Item:
        if not (item_type := cls.validate_item_type(_path)):
            raise RuntimeError
        if not (itemclass := cls.get_item_of_type(item_type)):
            raise RuntimeError
        return itemclass(_path)


T = TypeVar('T')

def register(itemclass: T) -> T:
    if not hasattr(itemclass, '__item_manager_registered'):
        ItemManager.register(itemclass)
        setattr(itemclass, '__item_manager_registered', True)
    return itemclass
