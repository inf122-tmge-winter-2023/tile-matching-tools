"""
    :module_name: exceptions
    :module_summary: exceptions related to core tilematching functionality
    :module_author: Nathan Mendoze (nathancm@uci.edu)
"""

class BaseTileMatchCoreException(Exception):
    """
        Base exception for core tilematch functionality
    """

class GameEndedException(BaseTileMatchCoreException):
    """
        Raised when a game loop is executed with a gamestate that has ended
    """
