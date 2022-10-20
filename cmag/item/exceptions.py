class CMagItemException(Exception):
    pass

class CMagInvalidItemPath(CMagItemException):
    pass

class CMagInvalidItemConfig(CMagItemException):
    pass

class CMagItemNotImplemented(CMagItemException):
    pass

class CMagItemTypeNotFound(CMagItemException):
    pass

class CMagItemExists(CMagItemException):
    pass
