from datetime import datetime
from urllib.parse import urlparse, parse_qs
import re

from bs4 import BeautifulSoup
import bs4.element
import httpx

from .exceptions import TorrentNotFoundError
from .enums import (
    SITE,
    QualityFilter,
    FunCategory, FapCategory,
    SortBy, SortOrder,
    TorrentType,
    UserLevel
    )
from .utils.categories import get_category_by_id

from .models import (
    SearchResult,
    SearchResultTorrent,
    TorrentInfo,
    User,
    File, Folder,
    Comment
    )

class NyaaClient:
    """
    Scraper client.
    """
    DEFAULT_SITE: SITE = SITE.FUN
    TIMEOUT: int = 30
    
    def __init__(self: "NyaaClient", site: SITE = DEFAULT_SITE, timeout: int = TIMEOUT) -> None:
        """
        Initialize scraper client.
        
        Parameters:
            site (SITE, optional): The site to scrape from. Defaults to DEFAULT_SITE.
            timeout (int, optional): The timeout for HTTP requests. Defaults to TIMEOUT.
        """
        self._site = site
        self.base_url = site.value
        self.timeout = timeout
        
        self._http_client: httpx.AsyncClient = httpx.AsyncClient(timeout=self.timeout)
    
    @property
    def site(self: "NyaaClient") -> SITE:
        """
        Getter property for the current site of the client.
        
        Returns:
            SITE: The current site used by the client.
        """
        return self._site
    
    @site.setter
    def site(self: "NyaaClient", new_site: SITE) -> None:
        """
        Set the site to scrape from.
        
        Parameters:
            new_site (SITE): The new site to set.
        """
        self._site = new_site
        self.base_url = new_site.value
    
    async def search(
        self: "NyaaClient",
        term: str | None = None,
        username: str | None = None,
        quality_filter: QualityFilter = QualityFilter.NO_FILTER,
        category: FunCategory | FapCategory | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        page: int = 1
        ) -> SearchResult:
        """
        Search torrents.
        
        Parameters:
            term (str | None, optional): Search term. Defaults to None.
            username (str | None, optional): Search torrents of a user. Defaults to None.
            quality_filter (QualityFilter | None, optional): Filter torrents by quality. If not specified, defaults to QualityFilter.NO_FILTER.
            category (FunCategory | FapCategory | None, optional): Filter torrents by category. If not specified, a default category is used. Defaults to None.
            sort_by (SortBy | None, optional): Sort results by. Defaults to None.
            sort_order (SortOrder | None, optional): Sort order of search. Defaults to None.
            page (int, optional): Page number of search result. Defaults to 1.
        
        Raises:
            httpx.HTTPError: If an HTTP-related error occurs during the request.
        
        Returns:
            SearchResult: Result of the search.
        """
        if category is None:
            category = get_category_by_id(self.site, "0_0")
        
        if username:
            url = f"{self.base_url}/user/{username}"
        else:
            url = self.base_url
        
        params = {
            "q": term,
            "f": quality_filter.value,
            "c": category.value,
            **({"s": sort_by.value} if sort_by else {}),
            **({"o": sort_order.value} if sort_order else {}),
            "p": page
        }
        response: httpx.Response = await self._http_client.get(url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        torrents: list[SearchResultTorrent] = []
        rows = soup.select("table.torrent-list tbody tr")
        for row in rows:
            category_ = get_category_by_id(
                site=self.site,
                category_id=row.select_one("a[href^='/?c=']")["href"][4:]
                )
            category_icon_url = self.base_url + row.find("img", class_="category-icon")["src"]
            
            total_comments, view_id, name = 0, None, None
            for tag in row.select("td[colspan='2'] a"):
                if "comments" in tag.get("class", []):
                    total_comments = int(tag.text)
                elif tag.get("href", "").startswith("/view/"):
                    view_id = int(tag["href"][6:])
                    name = tag["title"]
            
            tds = row.find_all("td", class_="text-center")
            torrent_url = self.base_url + tds[0].select_one("a[href^='/download/']")["href"]
            magnet_link = tds[0].select_one("a[href^='magnet:?xt=']")["href"]
            
            size = tds[1].text
            timestamp = datetime.utcfromtimestamp(int(tds[2]["data-timestamp"]))
            seeders = int(tds[3].text)
            leechers = int(tds[4].text)
            completed = int(tds[5].text)
            
            torrents.append(
                SearchResultTorrent(
                    torrent_type=TorrentType.from_color(row["class"][0]),
                    view_id=view_id,
                    name=name,
                    category=category_,
                    category_icon_url=category_icon_url,
                    torrent_url=torrent_url,
                    magnet_link=magnet_link,
                    size=size,
                    timestamp=timestamp,
                    seeders=seeders,
                    leechers=leechers,
                    completed=completed,
                    total_comments=total_comments
                    )
                )
        
        # Extract pagination results.
        displaying_from, displaying_to, total_results = 0, 0, 0
        pagination_page_info = soup.select_one("div.pagination-page-info")
        if pagination_page_info:
            matches = re.match(
                r"^Displaying results (\d+)-(\d+) out of (\d+) results\.",
                pagination_page_info.text
                )
            displaying_from, displaying_to, total_results = int(matches.group(1)), int(matches.group(2)), int(matches.group(3))
        
        # Extract pagination pages.
        previous_page, current_page, next_page, available_pages = None, None, None, None
        if (pagination := soup.find("ul", class_="pagination")):
            if (
                previous_tag := (
                    pagination.select_one("li.previous:not(.disabled):not(.unavailable) a[href]") or
                    pagination.select_one("li a[rel='prev']")
                    )
                ):
                query_params = parse_qs(urlparse(previous_tag["href"]).query)
                previous_page = int(query_params.get("p", [1])[0])
            
            
            if (active_tag := pagination.select_one("li.active a")):
                current_page = int(re.search("(\d+)", active_tag.text).group())
            
            if (
                next_tag := (
                    pagination.select_one("li.next:not(.disabled):not(.unavailable) a[href]") or
                    pagination.select_one("li a[rel='next']")
                    )
                ):
                query_params = parse_qs(urlparse(next_tag["href"]).query)
                next_page = int(query_params.get("p")[0])
            
            available_pages = int(pagination.find_all("li")[-2].find("a").text)
        elif torrents:
            # Pagination won't be available if there is only one page of results.
            # Therefore, if at least one torrent exists, it indicates that there is one page.
            # This also applies to current page.
            current_page = 1
            available_pages = 1
        
        return SearchResult(
            torrents=torrents,
            displaying_from=displaying_from,
            displaying_to=displaying_to,
            total_results=total_results,
            current_page=current_page,
            previous_page=previous_page,
            next_page=next_page,
            available_pages=available_pages
            )
    
    async def get_torrent_info(self: "NyaaClient", view_id: int) -> TorrentInfo:
        """
        Get torrent information.
        
        Parameters:
            view_id (int): View-ID of the torrent.
        
        Raises:
            httpx.HTTPError: If an HTTP-related error occurs during the request.
            TorrentNotFoundError: If the torrent of view id not found.
        
        Returns:
            TorrentInfo: Information of the torrent.
        """
        url = self.base_url + f"/view/{view_id}"
        response: httpx.Response = await self._http_client.get(url)
        response.raise_for_status()
        
        if response.status_code == 404:
            raise TorrentNotFoundError(f"Torrent '{view_id}' not found")
        
        soup = BeautifulSoup(response, "html.parser")
        
        name = soup.select_one("div.panel-heading h3.panel-title").get_text(strip=True)
        
        rows = soup.select("div.panel-body div.row")
        
        category = get_category_by_id(
            site=self.site,
            category_id=rows[0].select_one("a[href^='/?c=']")["href"][4:]
            )
        timestamp = datetime.utcfromtimestamp(int(rows[0].find("div", attrs={"data-timestamp": True})["data-timestamp"]))
        
        submitter_link = rows[1].select_one("a[href^='/user/']")
        if submitter_link:
            submitter = User(
                username=submitter_link["href"][6:],
                profile_url=self.base_url + submitter_link["href"]
                )
        else:
            # Submitter was an anonymous.
            submitter = None
        
        seeders = int(rows[1].select_one("span[style='color: green;']").text)
        
        information = rows[2].select_one("div.col-md-5").get_text(strip=True)
        leechers = int(rows[2].select_one("span[style='color: red;']").text)
        
        divs = rows[3].select("div.col-md-5")
        size, completed = divs[0].text, int(divs[1].text)
        
        info_hash = rows[4].find("kbd").text
        
        torrent_url = self.base_url + soup.select_one("div.panel-footer a[href^='/download/']")["href"]
        magnet_link = soup.select_one("div.panel-footer a[href^='magnet:?xt=']")["href"]
        
        description = soup.find("div", id="torrent-description").text
        files: list[File | Folder] = self.__extract_files_and_folders(soup.find("div", class_="torrent-file-list"))
        
        total_comments = int(soup.select_one("div#comments div.panel-heading h3.panel-title").text.split("-")[1])
        comments: list[Comment] = []
        for comment in soup.select("div#comments div.comment-panel"):
            user_tag = comment.select_one("a[href^='/user/']")
            image_src = comment.find("img", class_="avatar")["src"]
            user = User(
                username=user_tag["href"][6:],
                profile_url=self.base_url + user_tag["href"],
                photo_url=self.base_url + image_src if image_src.startswith("/") else image_src,
                is_banned="BANNED" in user_tag["title"]
                )
            
            comments.append(
                Comment(
                    id=int(comment["id"].split("-")[1]),
                    user=user,
                    user_level=UserLevel.from_level_str(level_str=user_tag["title"].split()[0].lower()),
                    is_uploader="(uploader)" in comment.select_one("div.col-md-2 p").text,
                    timestamp=datetime.utcfromtimestamp(int(comment.find("small", attrs={"data-timestamp": True})["data-timestamp"])),
                    text=comment.find("div", class_="comment-content").text
                    )
                )
        
        return TorrentInfo(
            name=name,
            category=category,
            torrent_url=torrent_url,
            magnet_link=magnet_link,
            size=size,
            timestamp=timestamp,
            seeders=seeders,
            leechers=leechers,
            completed=completed,
            info_hash=info_hash,
            submitter=submitter,
            information=information,
            description=description,
            files=files,
            total_comments=total_comments,
            comments=comments
            )
    
    def __extract_files_and_folders(self: "NyaaClient", tag: bs4.element.Tag) -> list[File | Folder]:
        """
        Extract files and folders from a BeautifulSoup element tag containing <ul> tag.
        
        Parameters:
            tag (bs4.element.Tag): A BeautifulSoup element tag containing <ul> tag.
        
        Returns:
            list[File | Folder]: A list File or Folder objects.
        """
        files_and_folders: list[File | Folder] = []
        for li in tag.select("ul li"):
            if (folder_tag := li.find("a", class_="folder")):
                files_and_folders.append(
                    Folder(
                        name=folder_tag.get_text(strip=True),
                        files=self.__extract_files_and_folders(li)
                        )
                    )
            elif li.find("i", class_="fa-file"):
                files_and_folders.append(
                    File(
                        name="".join((elem.get_text(strip=True) for elem in li.find_all(string=True, recursive=False))),
                        size=li.find("span", class_="file-size").get_text(strip=True).strip("()")
                        )
                    )
        return files_and_folders