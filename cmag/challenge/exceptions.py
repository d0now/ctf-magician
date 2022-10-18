class CMagChallengeException(Exception):
    pass

class CMagChallengeExistsError(CMagChallengeException):
    pass

class CMagChallengeNotFoundError(CMagChallengeException):
    pass