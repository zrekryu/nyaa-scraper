from enum import Enum

class TorrentType(Enum):
    """
    Types of torrents.
    
    Members:
        NORMAL (str): Represents a normal torrent.
        TRUSTED (str): Represents a trusted torrent.
        REMAKES (str): Represents a remakes torrent.
    """
    NORMAL = "normal"
    TRUSTED = "trusted"
    REMAKES = "remakes"
    
    @classmethod
    def from_color(cls, color: str) -> "TorrentType":
        """
        Get TorrentType enum member from a corresponding color.
        
        Parameters:
            color (str): The color of the torrent.
        
        Raises:
            ValueError: If the color string is not known by the TorrentType enum.
        
        Returns:
            TorrentType: Enum member of the TorrentType corresponding to the color.
        """
        if color == "default":
            return cls.NORMAL
        elif color == "success":
            return cls.TRUSTED
        elif color == "danger":
            return cls.REMAKES
        else:
            raise ValueError(f"Unknown color: {color}")