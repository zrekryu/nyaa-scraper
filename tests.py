import asyncio

from nyaascraper.enums import SITE, QualityFilter, FunCategory
from nyaascraper.models import NyaaRSSFeed, NyaaRSSTorrent
from nyaascraper import NyaaRSSClient

client = NyaaRSSClient(site=SITE.FUN)

async def main() -> None:
    # All parameters passed are optional.
    feed: NyaaRSSFeed = await client.get_feed(
        username="Erai-raws",
        filter_=QualityFilter.TRUSTED_ONLY,
        category=FunCategory.ANIME__ENGLISH_TRANSLATED
        )

    print("Title:", feed.title)
    print("Description:", feed.description)
    
    # Iterate over torrents.
    for torrent in feed.torrents:
        print(torrent)


asyncio.run(main())