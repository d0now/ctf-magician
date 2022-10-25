from __future__ import annotations
from typing import List, Type, TypeVar
from abc import ABC, abstractmethod
from pathlib import Path
from .exceptions import *


class ItemBase(ABC):

    cfgbase = None

    @classmethod
    @abstractmethod
    def validate(cls, _path: str | Path):
        ...

    @classmethod
    @abstractmethod
    def makeat(cls, _path: str | Path, exist_ok=False, **_config) -> Path:
        ...

    def __new__(cls, *args, **kwargs):
        if cls.cfgbase == None:
            raise NotImplementedError(f"'{cls.__name__}.cfgbase' is 'None'")
        return super().__new__(cls)

    @property
    def path(self) -> Path:
        return Path(self._path)

    def __init__(self, path: str | Path):
        self.validate(path)
        self._path = path



class ItemManagerBase(ABC):

    _itemclasses: List[Type[ItemBase]] = []

    @classmethod
    def register(cls, itemclass: Type[ItemBase]) -> None:

        if not issubclass(itemclass, ItemBase):
            raise CMagItemNotImplemented

        if cls.has_item_of_type(itemclass.cfgbase.type):
            raise CMagItemExists

        cls._itemclasses.append(itemclass)

    @classmethod
    def unregister(cls, type: int) -> None:
        if (item := cls.get_item_of_type(type)):
            cls._itemclasses.remove(item)

    @classmethod
    def get_item_of_type(cls, type: int) -> Type[ItemBase] | None:
        for registered in cls._itemclasses:
            if registered.cfgbase.type == type:
                return registered

    @classmethod
    def has_item_of_type(cls, type: int) -> bool:
        return cls.get_item_of_type(type) != None


T = TypeVar('T')

def register_item_to(managerclass: ItemManagerBase):

    def register_item(itemclass: T) -> T:

        flagattr = f'__{managerclass.__name__.lower()}_registered'

        if not hasattr(itemclass, flagattr):
            managerclass.register(itemclass)
            setattr(managerclass, flagattr, True)

        return itemclass

    return register_item

