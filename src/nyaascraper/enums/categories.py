from enum import Enum

class FunCategory(Enum):
    """
    Categories for torrents used in SITE.FUN.
    
    Members:
        ALL_CATEGORIES (str): Represents all categories.
        
        ANIME (str): Anime category.
        ANIME_AMV (str): Anime Music Video (AMV) category.
        ANIME_ENGLISH_TRANSLATED (str): Anime - English Translated category.
        ANIME_NON_ENGLISH_TRANSLATED (str): Anime - Non-English Translated category.
        ANIME_RAW (str): Anime - Raw category.
        
        AUDIO (str): Audio category.
        AUDIO_LOSSLESS (str): Audio - Lossless category.
        AUDIO_LOSSY (str): Audio - Lossy category.
        
        LITERATURE (str): Literature category.
        LITERATURE_ENGLISH_TRANSLATED (str): Literature - English Translated category.
        LITERATURE_NON_ENGLISH_TRANSLATED (str): Literature - Non-English Translated category.
        LITERATURE_RAW (str): Literature - Raw category.
        
        LIVE_ACTION (str): Live Action category.
        LIVE_ACTION_ENGLISH_TRANSLATED (str): Live Action - English Translated category.
        LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO (str): Live Action - Idol Promotional Video category.
        LIVE_ACTION_NON_ENGLISH_TRANSLATED (str): Live Action - Non-English Translated category.
        LIVE_ACTION_RAW (str): Live Action - Raw category.
        
        PICTURES (str): Pictures category.
        PICTURES_GRAPHICS (str): Pictures - Graphics category.
        PICTURES_PHOTOS (str): Pictures - Photos category.
        
        SOFTWARE (str): Software category.
        SOFTWARE_APPLICATIONS (str): Software - Applications category.
        SOFTWARE_GAMES (str): Software - Games category.
    """
    ALL_CATEGORIES = "0_0"
    ANIME = "1_0"
    ANIME__AMV = "1_1"
    ANIME__ENGLISH_TRANSLATED = "1_2"
    ANIME__NON_ENGLISH_TRANSLATED = "1_3"
    ANIME__RAW = "1_4"
    
    AUDIO = "2_0"
    AUDIO__LOSSLESS = "2_1"
    AUDIO__LOSSY = "2_2"
    
    LITERATURE = "3_0"
    LITERATURE__ENGLISH_TRANSLATED = "3_1"
    LITERATURE__NON_ENGLISH_TRANSLATED = "3_2"
    LITERATURE__RAW = "3_3"
    
    LIVE_ACTION = "4_0"
    LIVE_ACTION__ENGLISH_TRANSLATED = "4_1"
    LIVE_ACTION__IDOL_PROMOTIONAL_VIDEO = "4_2"
    LIVE_ACTION__NON_ENGLISH_TRANSLATED = "4_3"
    LIVE_ACTION__RAW = "4_4"
    
    PICTURES = "5_0"
    PICTURES__GRAPHICS = "5_1"
    PICTURES__PHOTOS = "5_2"
    
    SOFTWARE = "6_0"
    SOFTWARE__APPLICATIONS = "6_1"
    SOFTWARE__GAMES = "6_2"

class FapCategory(Enum):
    """
    Categories for torrents used in SITE.FAP.
    
    Members:
        ALL_CATEGORIES (str): Represents all categories.
        
        ART (str): Art category.
        ART_ANIME (str): Art - Anime category.
        ART_DOUJINSHI (str): Art - Doujinshi category.
        ART_GAMES (str): Art - Games category.
        ART_MANGA (str): Art - Manga category.
        ART_PICTURES (str): Art - Pictures category.
        
        REAL_LIFE (str): Real Life category.
        REAL_LIFE_PHOTOBOOKS_AND_PICTURES (str): Real Life - Photobooks and Pictures category.
        REAL_LIFE_VIDEOS (str): Real Life - Videos category.
    """
    ALL_CATEGORIES = "0_0"
    
    ART = "1_0"
    ART__ANIME = "1_1"
    ART__DOUJINSHI = "1_2"
    ART__GAMES = "1_3"
    ART__MANGA = "1_4"
    ART__PICTURES = "1_5"
    
    REAL_LIFE = "2_0"
    REAL_LIFE__PHOTOBOOKS_AND_PICTURES = "2_1"
    REAL_LIFE__VIDEOS = "2_2"