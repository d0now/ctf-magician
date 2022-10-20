from .config import itemconfig
from .item import Item
from .manager import register as item_manager_register
from .defaults import ItemTypes


@itemconfig
class CTFConfig:
    type: int = ItemTypes.CTF
    name: str = ''
    description: str = ''
    homepage: str = ''


@item_manager_register
class CTF(Item):
    
    cfgbase = CTFConfig

    @property
    def config(self) -> CTFConfig:
        return super().config

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def description(self) -> str:
        return self.config.description

    @property
    def homepage(self) -> str:
        return self.config.homepage
