from enum import IntEnum

class Filter(IntEnum):
    NO_FILTER: int = 0
    NO_REMAKES: int = 1
    TRUSTED_ONLY: int = 2