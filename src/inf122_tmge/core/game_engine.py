"""
    :module_name: game_engine
    :module_summary: representation of a runtime environment capable of running tile-matching games
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC

from inf122_tmge.core.game_state import GameState

from inf122_tmge.model.board.game_board import GameBoard
from inf122_tmge.model.score import Scoring
from inf122_tmge.model.match import MatchCondition

from inf122_tmge.model.tiles.movement_rule import MovementRule
from inf122_tmge.model.tiles.tile import Tile

class GameEngine(ABC):
    def __init__(self, board: GameBoard, score : Scoring):
        self.game_state = GameState(game_board=board, game_score=score)

    # TODO: Replace with updated place_tile
    # TODO: Handle exceptions, possibly chain exceptions
    def move_tile(self, row: int, col: int, rule: MovementRule):
        tile_to_move: Tile = self.game_state.game_board.tile_at(row, col).move(rule)
        self.game_state.game_board.place_tile(tile_to_move, tile_to_move.position.x, tile_to_move.position.y)

    # TODO Implement aftermath of a match
    def match_tiles(self, start_x: int, start_y: int, match_condition: MatchCondition):
        if match_condition.check_match(self.game_state.game_board,start_x, start_y):
            self.game_state.game_score.award_for_match(match_condition)
