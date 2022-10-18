class CMagFileException(Exception):
    pass

class CMagFileBadPathError(CMagFileException):
    pass

class CMagFileCreateError(CMagFileException):
    pass

class CMagFileRecordNotFoundError(CMagFileException):
    pass

class CMagFileNotFoundError(CMagFileException, FileNotFoundError):
    pass

class CMagFileExistsError(CMagFileException, FileExistsError):
    pass

class CMagFileInvalidError(CMagFileException):
    pass