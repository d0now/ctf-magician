from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path


class ItemBase(ABC):

    cfgbase = None

    @classmethod
    @abstractmethod
    def validate(cls, _path: str | Path):
        ...

    @classmethod
    @abstractmethod
    def makeat(cls, _path: str | Path, exist_ok=False, **_config):
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
