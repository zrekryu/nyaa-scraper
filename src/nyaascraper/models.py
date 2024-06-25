from typing import List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

from .enums import FunCategory, FapCategory, TorrentType

@dataclass
class SearchResultTorrent:
    """
    Represents a search result torrent.
    
    Attributes:
        - torrent_type (TorrentType): The type of the torrent.
        - view_id (int): View-ID of the torrent.
        - category (Union[FunCategory, FapCategory]): The category of the torrent.
        - category_icon_url (str): The URL of the icon of category.
        - torrent_url (str): The URL of the torrent file.
        - magnet_link (str): The Magnet Link of the torrent.
        - size (str): The size of the torrent.
        - timestamp (datetime): The timestamp of when the torrent was uploaded.
        - seeders (int): The number of seeders of the torrent.
        - leechers (int): The number of leechers of the torrent.
        - completed (int): The number of times the torrent has been completed.
        - total_comments (int): The number of total comments.
    """
    torrent_type: TorrentType
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
    """
    Search result.
    
    Attributes:
        - torrents (List[SearchResultTorrent]): A list of SearchResultTorrent objects.
        - displaying_from (int): The number of results displaying from.
        - displaying_to (int): The number of results displaying to.
        - total_results (int): The number of total results.
        - current_page (int): The number of current result page.
        - previous_page (int, optional): The number of previous result page. Defaults to None.
        - next_page (int, optional): The number of next result page. Defaults to None.
        - available_pages (int, optional): The number of currently avaiable result pages. If exceeded, there might be more result pages. Defaults to None.
    """
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
    """
    An User.
    
    Attributes:
        - username (str): The username of the user.
        - profile_url (str): The URL of the user.
        - photo_url (str, optional): The URL of the photo of the user. Defaults to None.
    """
    username: str
    profile_url: str
    photo_url: Optional[str] = None

@dataclass
class File:
    """
    A File.
    
    Attributes:
        - name (str): The name of the file.
        - size (str): The size of the file.
    """
    name: str
    size: str

@dataclass
class Folder:
    """
    A Folder.
    
    Attributes:
        - name (str): The name of the folder.
        - files (List[Union[File, "Folder"]]): A list of File or Folder objects.
    """
    name: str
    files: List[Union[File, "Folder"]]

@dataclass
class Comment:
    """
    A Comment.
    
    Attributes:
        - id (int): The ID of the comment.
        - user (User): The user who commented.
        - is_uploader (int): Indicates if the user is uploader of the torrent.
        - is_banned (int): Indicates if the user is banned.
        - timestamp (int): The timestamp of when the comment was made.
        - text (str): The text of the comment.
    """
    id: int
    user: User
    is_uploader: bool
    is_banned: bool
    timestamp: datetime
    text: str

@dataclass
class TorrentInfo:
    """
    Torrent information.
    
    Attributes:
        - name (str): The name of the torrent.
        - category (Union[FunCategory, FapCategory]): The category of the torrent.
        - torrent_url (str): The URL of the torrent file.
        - magnet_link (str): The Magnet Link of the torrent.
        - size (str): The size of the torrent.
        - timestamp (datetime): The timestamp of when the torrent was uploaded.
        - seeders (str): The number of seeders of the torrent.
        - leechers (str): The number of leechers of the torrent.
        - completed (str): The number of times the torrent has been completed.
        - info_hash (str): The info hash of the torrent.
        - submitter (Optional[User]): The user who uploaded this torrent. If anonymous, the value is None.
        - information (str): The information of the torrent.
        - description (str): The description of the torrent.
        - files (List[Union[File, Folder]]): A list of torrent files.
        - total_comments (int): The number of total comments on the torrent.
        - comments (List[Comment]): A list of comments on the torrent.
    """
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
    submitter: Optional[User]
    information: str
    description: str
    files: List[Union[File, Folder]]
    total_comments: int
    comments: List[Comment]