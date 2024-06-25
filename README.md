# Usage

## Initializing client with site

By default, the site is nyaa.si (work-safe site).
```py
from nyaascraper import NyaaClient, SITE

# Work-safe site.
client = NyaaClient(SITE.FUN)

# Non-work-safe site.
client = NyaaClient(SITE.FAP)
```

## Searching torrents

### Search with query

```py
from nyaascraper.models import SearchResult

result: SearchResult = await client.search(query="your query...")
print(result)
```
### Search with filter

```py
from nyaascraper.enums import Filter
from nyaascraper.models import SearchResult

result: SearchResult = await client.search(filter_=Filter.TRUSTED_ONLY)
print(result)
```
### Search with category

```py
from nyaascraper.enums import FunCategory, FapCategory
from nyaascraper.models import SearchResult

# Work-safe category.
result: SearchResult = await client.search(category=FunCategory.ANIME)
print(result)

# Non-work-safe category.
result: SearchResult = await client.search(category=FapCategory.ART)
print(result)
```

## Getting torrent information

```py
from nyaascraper.models import SearchResult, TorrentInfo

# Fetch torrents at homepage.
result: SearchResult = await client.search()

view_id: int = result.torrents[0].view_id

torrent_info: TorrentInfo = await client.get_torrent_info(view_id)
print(torrent_info)
```