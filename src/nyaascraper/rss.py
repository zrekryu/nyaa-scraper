from typing import List, Optional, Union

import httpx
import feedparser

from .enums import SITE, Filter, FunCategory, FapCategory, TorrentType
from .utils.categories import get_category_by_id

from .models import NyaaRSSFeed, NyaaRSSTorrent

class NyaaRSSClient:
    DEFAULT_SITE: SITE = SITE.FUN
    TIMEOUT: int = 30
    
    def __init__(self: "NyaaRSSClient", site: SITE = DEFAULT_SITE, timeout: int = TIMEOUT) -> None:
        """
        Initialize rss client.
        
        Parameters:
            site (SITE, optional): The site to fetch from. Defaults to DEFAULT_SITE.
            timeout (int, optional): The timeout for HTTP requests. Defaults to TIMEOUT.
        """
        self._site = site
        self.base_url = site.value
        self.timeout = timeout
        
        self._http_client: httpx.AsyncClient = httpx.AsyncClient(timeout=self.timeout)
    
    @property
    def site(self: "NyaaRSSClient") -> SITE:
        """
        Getter property for the current site of the client.
        
        Returns:
            SITE: The current site used by the client.
        """
        return self._site
    
    @site.setter
    def site(self: "NyaaRSSClient", new_site: SITE) -> None:
        """
        Set the site to fetch from.
        
        Parameters:
            new_site (SITE): The new site to set.
        """
        self._site = new_site
        self.base_url = new_site.value
    
    async def get_feed(
        self: "NyaaRSSClient",
        query: Optional[str] = None,
        username: Optional[str] = None,
        filter_: Optional[Filter] = Filter.NO_FILTER,
        category: Optional[Union[FunCategory, FapCategory]] = None
        ) -> NyaaRSSFeed:
        """
        Parameters:
            query (Optional[str], optional): Search query. Defaults to None.
            username (Optional[str], optional): Search torrents of a user. Defaults to None.
            filter_ (Filter, optional): Search by filter. Defaults to Filter.NO_FILTER.
            category (Union[FunCategory, FapCategory], optional): Search by category. Defaults to None. If None, it'll be assigned to (FanCategory/FapCategory).ALL_CATEGORIES depending on site.
        
        Raises:
            httpx.HTTPError: If an HTTP-related error occurs during the request.
        
        Returns:
            NyaaRSSFeed: RSS feed.
        """
        if category is None:
            category = get_category_by_id(self.site, "0_0")
        
        params = {
            "page": "rss",
            "q": query,
            "u": username,
            "f": filter_.value,
            "c": category.value
        }
        response: httpx.Response = await self._http_client.get(self.base_url, params=params)
        response.raise_for_status()
        
        parsed_feed = feedparser.parse(response.text)
        
        torrents: List[NyaaRSSTorrent] = []
        for entry in parsed_feed.entries:
            torrent_type = TorrentType.NORMAL
            if entry.nyaa_trusted.lower() == "yes":
                torrent_type = TorrentType.TRUSTED
            elif entry.nyaa_remake.lower() == "yes":
                torrent_type = TorrentType.REMAKES
            
            view_id = int(entry.guid.split("/view/")[-1])
            category = get_category_by_id(site=self.site, id_=entry.nyaa_categoryid)
            
            torrents.append(
                NyaaRSSTorrent(
                    torrent_type=torrent_type,
                    view_id=view_id,
                    name=entry.title,
                    category=category,
                    size=entry.nyaa_size,
                    published=entry.published,
                    published_parsed=entry.published_parsed,
                    torrent_url=entry.link,
                    seeders=int(entry.nyaa_seeders),
                    leechers=int(entry.nyaa_leechers),
                    completed=int(entry.nyaa_downloads),
                    info_hash=entry.nyaa_infohash,
                    description=entry.description,
                    total_comments=int(entry.nyaa_comments)
                    )
                )
        
        return NyaaRSSFeed(
            title=parsed_feed.feed.title,
            description=parsed_feed.feed.description,
            torrents=torrents
            )