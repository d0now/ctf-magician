from __future__ import annotations
from pathlib import Path
from shutil import copyfile

from .exceptions import CMagInvalidItemPath
from .config import itemconfig
from .manager import register as item_manager_register
from .item import Item
from .defaults import ItemTypes, FILE_ITEM_ORIGINAL_FILENAME


@itemconfig
class FileConfig:
    type: int = ItemTypes.FILE


@item_manager_register
class File(Item):

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
    def makeat(cls, _file: str | Path, _path: str | Path, exist_ok=False, symlink=False, **_config):
        
        super().makeat(_path, exist_ok=exist_ok, **_config)

        if not (path := Path(_path)).is_dir():
            raise CMagInvalidItemPath(path)
        if not (file := Path(_file)).is_file():
            raise FileNotFoundError(file)

        if symlink:
            file.link_to(path / FILE_ITEM_ORIGINAL_FILENAME)
        else:
            copyfile(file, path / FILE_ITEM_ORIGINAL_FILENAME)

    def open(self, *args, **kwargs):
        return self.filepath.open(*args, **kwargs)

    def link_to(self, *args, **kwargs):
        return self.filepath.link_to(*args, **kwargs)

    def copy_to(self, *args, **kwargs):
        return copyfile(self.filepath, *args, **kwargs)
