from typing import Type
from enum import Enum

class UserLevel(Enum):
    """
    User levels.
    
    Members:
        REGULAR (str): A regular user.
        TRUSTED (str): A trusted user.
        MODERATOR (str): A moderator.
        ADMINISTRATOR (str): An Administrator.
    """
    REGULAR = "User"
    TRUSTED = "Trusted"
    MODERATOR = "Moderator"
    ADMINISTRATOR = "Administrator"
    
    @classmethod
    def from_level_str(cls: Type["UserLevel"], level_str: str) -> "UserLevel":
        """
        Get UserLevel enum member from a corresponding level.
        
        Parameters:
            level_str (str): The level string of the user.
        """
        if level_str == "user":
            return cls.REGULAR
        elif level_str == "trusted":
            return cls.TRUSTED
        elif level_str == "moderator":
            return cls.MODERATOR
        elif level_str == "administrator":
            return cls.ADMINISTRATOR
        else:
            raise ValueError(f"Unknown user level string: {level_str}")