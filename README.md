# nyaasi-scraper

nyaasi-scraper is an asynchronous Python library for scraping [nyaa.si](https://nyaa.si) and [sukebei.nyaa.si](https://sukebei.nyaa.si).

# Installation

Installing through pip.

```bash
pip install nyaasi-scraper
```

# Usage

## Initializing Client with Site

By default, the site is nyaa.si (work-safe site).

```py
from nyaascraper import NyaaClient, SITE

# Work-safe site.
client = NyaaClient(SITE.FUN)

# Non-work-safe site.
client = NyaaClient(SITE.FAP)
```

## Changing Site

You can change the site of the client dynamically.

```py
from nyaascraper import SITE

client.site = SITE.FUN
```

## Searching Torrents

### Search with Query

```py
from nyaascraper.models import SearchResult

result: SearchResult = await client.search(query="your query...")
print(result)

# Iterate over torrents.
for torrent in result.torrents:
    print(torrent)
```

### Search with Filter

```py
from nyaascraper.models import SearchResult
from nyaascraper import Filter

result: SearchResult = await client.search(filter_=Filter.TRUSTED_ONLY)
print(result)
```

Refer to the documentation for Filter for more details.

### Search with Category

```py
from nyaascraper.enums import FunCategory, FapCategory
from nyaascraper.models import SearchResult

# Work-safe category.
result: SearchResult = await client.search(category=FunCategory.ANIME)
print(result)

# Work-safe subcategory search.
result: SearchResult = await client.search(category=FunCategory.ANIME__ENGLISH_TRANSLATED)
print(result)

# Non-work-safe category.
result: SearchResult = await client.search(category=FapCategory.ART)
print(result)

# Non-work-safe subcategory search.
result: SearchResult = await client.search(category=FunCategory.ART__MANGA)
print(result)
```

Explore FunCategory and FapCategory for more options.

### Search Sorting

```py
from nyaascraper.enums import SortBy, SortOrder
from nyaascraper.models import SearchResult

result: SearchResult = await client.search(sort_by=SortBy.DATE, sort_order=SortOrder.DESCENDING)
print(result)
```

Check SortBy and SortOrder for additional sorting methods.

### Search by Page

```py
from nyaascraper.models import SearchResult

result: SearchResult = await client.search(page=2)
print(result)
```

## Getting Torrent Information

```py
from nyaascraper.models import SearchResult, TorrentInfo

result: SearchResult = await client.search()

# Select View-ID of first torrent from the search result.
view_id: int = result.torrents[0].view_id

torrent_info: TorrentInfo = await client.get_torrent_info(view_id)
print(torrent_info)
```

## RSS Feed

### Initializing Client with Site

By default, the site is nyaa.si (work-safe site).

```py
from nyaascraper import NyaaRSSClient, SITE

# Work-safe site.
client = NyaaRSSClient(SITE.FUN)

# Non-work-safe site.
client = NyaaRSSClient(SITE.FAP)
```

### Changing Site

You can change the site of the client dynamically.

```py
from nyaascraper import SITE

client.site = SITE.FUN
```

### Get RSS feed

```py
from nyaascraper.enums import Filter, FunCategory
from nyaascraper.models import NyaaRSSFeed, NyaaRSSTorrent

# All parameters passed are optional.
feed: NyaaRSSFeed = await client.get_feed(
    query="your query...",
    username="Erai-raws",
    filter_=Filter.TRUSTED_ONLY,
    category=FunCategory.ANIME__ENGLISH_TRANSLATED
    )

print("Title:", feed.title)
print("Description:", feed.description)

# Iterate over torrents.
for torrent in feed.torrents:
    print(torrent)
```

# License

Licensed under MIT License. See the LICENSE file for details.