"""
    :module_name: game_engine
    :module_summary: representation of a runtime environment capable of running tile-matching games
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from abc import ABC

from ..core.game_state import GameState

from ..model import GameBoard
from ..model import Scoring
from ..model import MatchCondition

from ..model import MovementRule
from ..model import Tile

LOGGER=logging.getLogger(__name__)

class GameEngine(ABC):
    def __init__(self, board: GameBoard, score : Scoring):
        self.game_state = GameState(game_board=board, game_score=score)

    # TODO: Replace with updated place_tile
    # TODO: Handle exceptions, possibly chain exceptions
    def move_tile(self, row: int, col: int, rule: MovementRule):
        """Applies movement rule to tile at (row, col)

        Args:
            row (int): row of tile
            col (int): col of tile
            rule (MovementRule): Concrete MovementRule
        """
        tile_to_move = self.tile_at(row, col)
        tile_to_move.move(rule)
        self.place_tile(tile_to_move, tile_to_move.position.x, tile_to_move.position.y)

    # TODO Implement aftermath of a match
    def match_tiles(self, start_x: int, start_y: int, match_condition: MatchCondition):
        """Checks if tiles match, then awards for match accordingly

        Args:
            start_x (int): the x position the match scans for
            start_y (int): the y position the match scans for
            match_condition (MatchCondition): the match condition that awards points
        """
        if match_condition.check_match(self.game_state.game_board,start_x, start_y):
            self.game_state.game_score.award_for_match(match_condition)
    
    # TODO: Replace with updated place_tile
    def place_tile(self, tile: Tile, row: int, col: int):
        """Propogated place_tile from game_board 

        Args:
            tile (Tile): tile to place
            row (int): row of the tile
            col (int): col of the tile
        """
        self.game_state.game_board.place_tile(tile, row, col)

    def tile_at(self, row: int, col: int) -> Tile:
        """Propogated tile_at from game_board 

        Args:
            row (int): row of the tile
            col (int): col of the tile

        Returns:
            Tile: Tile at (row, col) position

        Raises:
            InvalidBoardPosition for invalid tile positions
        """
        return self.game_state.game_board.tile_at(row, col)
    
    @property
    def score(self) -> int:
        """Propogated score property from game_score

        Returns:
            int: score
        """
        return self.game_state.game_score.score
    
