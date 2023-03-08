"""
    :module_name: exceptions
    :module_summary: exception classes for tilematch_tools.model
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

class BaseInf122tmgeModelException(Exception):
    """Base exception for all other module related exceptions"""

class MissingTilePropertyException(BaseInf122tmgeModelException):
    """Exception raised when a tile cannot be constructed due to a missing property"""

class InvalidBoardPositionError(BaseInf122tmgeModelException):
    """Exception raised when a board operation is attempted with a bad position coordinate"""

class IllegalBoardContentException(BaseInf122tmgeModelException):
    """Exception raised when attempting to place something other than a subtype of Tile in a game board"""

class TileGroupDisbandedException(BaseInf122tmgeModelException):
    """Exception raised when performing actions on a tile group that has disbanded"""

class TileGroupPositionOccupiedError(BaseInf122tmgeModelException):
    """Exception raised when attempting to add a tile with invalid relative position"""

class IllegalTileMovementException(BaseInf122tmgeModelException):
    """Exception raised when a movement is not applicable to a tile"""
