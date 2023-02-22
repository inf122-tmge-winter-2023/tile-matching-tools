"""
    :module_name: board_factory
    :module_summary: a class capable of creating new boards of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC

from ..model.board.game_board import GameBoard

class BoardFactory(ABC):
    def create_board(type: str, width, height) -> GameBoard:
        return GameBoard(width, height)
