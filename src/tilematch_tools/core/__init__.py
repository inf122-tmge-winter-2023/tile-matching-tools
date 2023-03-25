"""
    :module_name: core
    :module_summary: a collection of classes for creating and running tile-matching games
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from .tile_builder import TileBuilder
from .board_factory import BoardFactory
from .game_state import GameState
from .game_loop import GameLoop
from .game_engine import GameEngine
from .game_factory import GameFactory, Game