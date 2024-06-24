from enum import Enum

class TorrentType(Enum):
    NORMAL = "normal"
    TRUSTED = "trusted"
    REMAKES = "remakes"
    BATCHES = "batches"
    HIDDEN = "hidden"
    
    @classmethod
    def from_color(cls, color: str) -> "TorrentType":
        if color == "default":
            return cls.NORMAL
        elif color == "success":
            return cls.TRUSTED
        elif color == "danger":
            return cls.REMAKES
        elif color == "batches":
            return cls.BATCHES
        elif color == "hidden":
            return cls.HIDDEN
        else:
            raise ValueError(f"Unknown color: {color}")