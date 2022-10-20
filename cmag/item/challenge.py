from .config import itemconfig
from .item import Item
from .manager import register as item_manager_register
from .defaults import ItemTypes


@itemconfig
class ChallengeConfig:
    type: int = ItemTypes.CHALLENGE
    name: str = ''
    description: str = ''
    category: str = ''


@item_manager_register
class Challenge(Item):

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
