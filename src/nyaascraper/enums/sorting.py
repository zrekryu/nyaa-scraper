from enum import Enum

class SortBy(Enum):
    COMMENTS = "comments"
    SIZE = "size"
    DATE = "id"
    SEEDERS = "seeders"
    LEECHERS = "leechers"
    COMPLETED = "downloads"

class SortOrder(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"