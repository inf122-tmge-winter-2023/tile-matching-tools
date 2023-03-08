"""
    :module_name: game_state
    :module_summary: an extensible class capable of representing the state of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu), Matthew Isayan
"""

from dataclasses import dataclass

from inf122_tmge.model.board.game_board import GameBoard
from inf122_tmge.model.score import Scoring

@dataclass
class GameState:
    """
        Class responsible for holding the gameboard and score 
    """
    game_board: GameBoard
    score: Scoring