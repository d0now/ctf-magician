from enum import IntEnum

class ItemTypes(IntEnum):
    CTF = 1
    CHALLENGE = 2
    FILE = 3
    DIRECTORY = 4
    ARCHIVE = 5

ITEM_CONFIG_FILENAME = ".item.cmag"

FILE_ITEM_ORIGINAL_FILENAME = ".data.cmag"
