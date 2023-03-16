"""
    :module_name: game_engine
    :module_summary: representation of a runtime environment capable of running tile-matching games
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

########################
# Deprecrated!!!       #
########################

import logging
from abc import ABC
import time

from .game_state import GameState
from .tile_builder import TileBuilder
from ..model import GameBoard, Scoring, MatchCondition, MovementRule, Tile, NullTile
from ..model.exceptions import IllegalTileMovementException, InvalidBoardPositionError

LOGGER=logging.getLogger(__name__)

class GameEngine(ABC):
    def __init__(self, board: GameBoard, score : Scoring):
        self.game_state = GameState(game_board=board, game_score=score)

    def move_tile(self, tile_to_move: Tile, rule: MovementRule):
        """Applies movement rule to tile at (row, col)

        Args:
            row (int): row of tile
            col (int): col of tile
            rule (MovementRule): Concrete MovementRule
        """
        origin_x = tile_to_move.position.x
        origin_y = tile_to_move.position.y
        try:
            tile_to_move.move(rule)
            self.place_tile(tile_to_move)
        except (IllegalTileMovementException, InvalidBoardPositionError):
            # Handling both exceptions as the sequence of events in try would imply invalid move
            LOGGER.error('Could not apply movement rule %s. Reverting tile state', str(type(rule)))
            # Restore tile's original position so its board position is correctly reflected
            tile_to_move.position = (origin_x, origin_y)
            # Movement failed, so actual tile was never moved
        else:
            # Replace origin tile position with a null tile
            self.place_tile(
                    TileBuilder() \
                            .add_position(origin_x, origin_y) \
                            .add_color('#D3D3D3') \
                            .construct(tile_type=NullTile)
            )
                    


    # TODO Implement aftermath of a match
    def match_tiles(self, start_x: int, start_y: int, match_condition: MatchCondition) -> bool:
        """Checks if tiles match, then awards for match accordingly

        Args:
            start_x (int): the x position the match scans for
            start_y (int): the y position the match scans for
            match_condition (MatchCondition): the match condition that awards points
        Returns:
            True if match found, false otherwise
        """
        match_found = match_condition.check_match(self.game_state.game_board,start_x, start_y)
        if match_found is not None:
            self.game_state.game_score.award_for_match(match_found)
            time.sleep(.25)
            for tile in match_found.matching_tiles:
                self.place_tile( TileBuilder() \
                            .add_position(tile.position.x, tile.position.y) \
                            .add_color('#D3D3D3') \
                            .construct(tile_type=NullTile))
            return True
        return False
    
    def swap_tiles(self, tile1: Tile, tile2: Tile):
        self.place_tile(TileBuilder() \
                            .add_position(tile1.position.x, tile1.position.y) \
                            .add_color(tile1.color) \
                            .construct(tile_type=NullTile))
        self.place_tile(TileBuilder() \
                            .add_position(tile2.position.x, tile2.position.y) \
                            .add_color(tile2.color) \
                            .construct(tile_type=NullTile))
        temp_x = tile1.position.x
        temp_y = tile1.position.y

        tile1.position = (tile2.position.x, tile2.position.y)
        tile2.position = (temp_x, temp_y)
        
        self.place_tile(tile1)
        self.place_tile(tile2)
    
    def place_tile(self, tile: Tile):
        """Propogated place_tile from game_board 

        Args:
            tile (Tile): tile to place
            row (int): row of the tile
            col (int): col of the tile
        """
        self.game_state.game_board.place_tile(tile)

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
    
