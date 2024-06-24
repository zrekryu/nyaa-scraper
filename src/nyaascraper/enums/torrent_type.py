from enum import Enum

class TorrentType(Enum):
    NORMAL = "normal"
    TRUSTED = "trusted"
    REMAKES = "remakes"
    
    @classmethod
    def from_color(cls, color: str) -> "TorrentType":
        if color == "default":
            return cls.NORMAL
        elif color == "success":
            return cls.TRUSTED
        elif color == "danger":
            return cls.REMAKES
        else:
            raise ValueError(f"Unknown color: {color}")