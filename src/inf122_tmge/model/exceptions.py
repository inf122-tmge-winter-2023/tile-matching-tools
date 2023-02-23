"""
    :module_name: exceptions
    :module_summary: exception classes for inf122_tmge.model
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
