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

### Search by Username

```py
result = await client.search(username="Erai-raws")
print(result)
```

### Search with Filter

```py
from nyaascraper import Filter

# No Filter. (Default)
result = await client.search(filter_=Filter.NO_FILTER)
print(result)

# Trusted only.
result = await client.search(filter_=Filter.TRUSTED_ONLY)
print(result)

# No Remakes.
result = await client.search(filter_=Filter.NO_REMAKES)
print(result)
```

### Search with Category

```py
from nyaascraper.enums import FunCategory, FapCategory

# Work-safe category.
result = await client.search(category=FunCategory.ANIME)
print(result)

# Work-safe subcategory search.
result = await client.search(category=FunCategory.ANIME__ENGLISH_TRANSLATED)
print(result)

# Non-work-safe category.
result = await client.search(category=FapCategory.ART)
print(result)

# Non-work-safe subcategory search.
result = await client.search(category=FunCategory.ART__MANGA)
print(result)
```

### Search with Sorting

```py
from nyaascraper.enums import SortBy, SortOrder

# Sort by comments.
result = await client.search(sort_by=SortBy.COMMENTS)
print(result)

# Sort by size.
result = await client.search(sort_by=SortBy.SIZE)
print(result)

# Sort by date.
result = await client.search(sort_by=SortBy.DATE)
print(result)

# Sort by seeders.
result = await client.search(sort_by=SortBy.SEEDERS)
print(result)

# Sort by leechers.
result = await client.search(sort_by=SortBy.LEECHERS)
print(result)

# Sort by downloads.
result = await client.search(sort_by=SortBy.DOWNLOADS)
print(result)

# Sort order: Ascending.
result = await client.search(sort_order=SortOrder.ASCENDING)
print(result)

# Sort order: Descending.
result = await client.search(sort_order=SortOrder.DESCENDING)
print(result)
```

### Search by Page

```py
result = await client.search(page=2)
print(result)
```

## Getting Torrent Information

```py
from nyaascraper.models import TorrentInfo

result = await client.search()

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
from nyaascraper.models import NyaaRSSFeed

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