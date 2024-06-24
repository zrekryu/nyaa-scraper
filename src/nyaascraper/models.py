from typing import List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

from .enums.categories import FunCategory, FapCategory

@dataclass
class SearchResultTorrent:
    torrent_type: str
    view_id: int
    name: str
    category: Union[FunCategory, FapCategory]
    category_icon_url: str
    torrent_url: str
    magnet_link: str
    size: str
    timestamp: datetime
    seeders: int
    leechers: int
    completed: int
    total_comments: int

@dataclass
class SearchResult:
    torrents: List[SearchResultTorrent]
    displaying_from: int
    displaying_to: int
    total_results: int
    current_page: int
    previous_page: Optional[int] = None
    next_page: Optional[int] = None
    available_pages: Optional[int] = None

@dataclass
class User:
    username: str
    profile_url: str
    photo_url: Optional[str] = None

@dataclass
class File:
    name: str
    size: str

@dataclass
class Folder:
    name: str
    files: List[Union[File, "Folder"]]

@dataclass
class Comment:
    id: int
    user: User
    is_uploader: bool
    is_banned: bool
    timestamp: datetime
    text: str

@dataclass
class TorrentInfo:
    name: str
    category: Union[FunCategory, FapCategory]
    torrent_url: str
    magnet_link: str
    size: str
    timestamp: datetime
    seeders: int
    leechers: int
    completed: int
    info_hash: str
    submitter: User
    information: str
    description: str
    files: List[Union[File, Folder]] = field(default_factory=list)
    total_comments: int = field(default=0)
    comments: List[Comment] = field(default_factory=list)