from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterator
from pathlib import Path
from shutil import copyfile, rmtree

from .exceptions import CMagInvalidItemPath
from .config import itemconfig
from .manager import register_item, ItemManager
from .item import Item
from .defaults import ItemTypes, FILE_ITEM_ORIGINAL_FILENAME


@itemconfig
class FileConfig:
    type: int = ItemTypes.FILE
    name: str = ''


@register_item
class File(Item):

    cfgbase = FileConfig

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def filepath(self) -> Path:
        return Path(self.path) / FILE_ITEM_ORIGINAL_FILENAME

    @classmethod
    def validate(cls, _path: str | Path):
        super().validate(_path)
        if not (filepath := Path(_path) / FILE_ITEM_ORIGINAL_FILENAME).exists():
            raise CMagInvalidItemPath(f"'{filepath}' not found.")

    @classmethod
    def makeat(cls, _file: str | Path, _path: str | Path, exist_ok=False, symlink=False, link_parent=False, **_config) -> Path:

        if not (file := Path(_file)).is_file():
            raise FileNotFoundError(file)

        if link_parent:
            path = Path(_path) / ('.' + file.name)
        else:
            path = Path(_path) / file.name

        if 'name' not in _config or not _config['name']:
            _config['name'] = file.name

        super().makeat(path, exist_ok=exist_ok, **_config)

        if not path.is_dir():
            raise CMagInvalidItemPath(path)

        original_filepath = Path(path / FILE_ITEM_ORIGINAL_FILENAME)

        if symlink:
            if file.exists() and exist_ok:
                file.unlink()
            file.link_to(original_filepath)
        else:
            copyfile(file, original_filepath)

        if link_parent:
            ItemManager.validate_item_type(path.parent)
            original_filepath.link_to(path.parent / file.name)

        return path

    def open(self, *args, **kwargs):
        return self.filepath.open(*args, **kwargs)

    def link_to(self, *args, **kwargs):
        return self.filepath.link_to(*args, **kwargs)

    def copy_to(self, *args, **kwargs):
        return copyfile(self.filepath, *args, **kwargs)

    def dump(self):
        return '\n'.join([
            self.dump_config()
        ])

    def dump_config(self):
        return '\n'.join([
            f"type : File",
            f"name: {self.name}"
        ])


class ParentOfFileMixin(ABC):

    @abstractmethod
    def iter_childs(self) -> Iterator[Item]:
        ...

    def iter_files(self) -> Iterator[File]:
        for child in self.iter_childs():
            if child.type == ItemTypes.FILE:
                yield child

    def has_files(self) -> bool:
        for _ in self.iter_files():
            return True
        return False

    def get_file(self, name: str) -> File | None:
        for file in self.iter_files():
            if file.name == name:
                return file

    def remove_file(self, name: str) -> Path | None:
        for file in self.iter_files():
            if file.name == name:
                rmtree(file.path)
                return file.path

    def dump_files(self) -> str:
        return '\n'.join([
            f"count : {len(list(self.iter_files()))}"
        ])
