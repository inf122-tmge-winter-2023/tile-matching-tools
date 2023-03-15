"""
    :module_name: game_state
    :module_summary: an extensible class capable of representing the state of a tile-matching game
    :module_author: Nathan Mendoza (nathancm@uci.edu), Matthew Isayan
"""

import logging

from .tile_builder import TileBuilder
from ..model import GameBoard, Scoring, MatchCondition
from ..model.tiles import Tile, MovementRule, NullTile
from ..model.exceptions import IllegalTileMovementException, InvalidBoardPositionError

LOGGER = logging.getLogger(__name__)

class GameState:
    """
        Class responsible for holding the gameboard and score 
    """
    def __init__(self, board: GameBoard, score: Scoring):
        self._board = board
        self._score = score
        self._match_conditions = []

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
            LOGGER.info('Attempting to move tile at (%d, %d)', origin_x, origin_y)
            tile_to_move.move(rule)
            self.board.place_tile(tile_to_move)
        except (IllegalTileMovementException, InvalidBoardPositionError):
            # Handling both exceptions as the sequence of events in try would imply invalid move
            LOGGER.error('Could not apply movement rule %s. Reverting tile state', str(type(rule)))
            # Restore tile's original position so its board position is correctly reflected
            tile_to_move.position = (origin_x, origin_y)
            # Movement failed, so actual tile was never moved
        else:
            # Replace origin tile position with a null tile
            LOGGER.info(
                    'Movement successfully applied. Declaring (%d, %d) on the board to be null',
                    origin_x,
                    origin_y
                    )
            self.board.place_tile(
                    TileBuilder() \
                            .add_position(origin_x, origin_y) \
                            .add_color('#D3D3D3') \
                            .construct(tile_type=NullTile)
            )

    def find_match(
            self, 
            start_x: int, 
            start_y: int, 
            match_condition: MatchCondition
            ) -> MatchCondition.MatchFound or None:
        """Find a match that satisfies the given match condition

        Args:
            start_x (int): the x position the match scans for
            start_y (int): the y position the match scans for
            match_condition (MatchCondition): the match condition to satisfy
        Returns:
            An object decribing the match if one exists, None otherwise
        """
        LOGGER.info(
                'Checking for %s starting at (%d, %d)',
                str(type(match_condition)),
                start_x,
                start_y
                )
        return match_condition.check_match(self.board, start_x, start_y)
 
    def adjust_score(self, match: MatchCondition.MatchFound) -> None:
        """Update the score with the discovered match

        Args:
            match (MatchCondition.MatchFound): object describing the match found
        Returns:
            None
        """
        LOGGER.debug('Awarding %d points for discovered match', match.value)
        self._score.award_for_match(match)

    def clear_match(self, match: MatchCondition.MatchFound) -> None:
        """Update the tiles part of the given match with Null tiles

        Args:
            match (MatchCondition.MatchFound): object describing the match found
        Returns:
            None
        """
        for tile in match.matching_tiles:
            LOGGER.debug(
                    'Replacing tile at (%d, %d) with null as it is part of a match',
                    tile.position.x,
                    tile.position.y
                    )
            self.board.place_tile( TileBuilder() \
                         .add_position(tile.position.x, tile.position.y) \
                        .add_color('#D3D3D3') \
                        .construct(tile_type=NullTile)
            )

    def swap_tiles(self, tile1: Tile, tile2: Tile) -> None:
        """Swap two tiles
        Args:
            tile1 (Tile): first tile to swap
            tile2 (Tile): second tile to swap
        Returns:
            None
        """
        self.board.place_tile(TileBuilder() \
                            .add_position(tile1.position.x, tile1.position.y) \
                            .add_color(tile1.color) \
                            .construct(tile_type=NullTile))
        self.board.place_tile(TileBuilder() \
                            .add_position(tile2.position.x, tile2.position.y) \
                            .add_color(tile2.color) \
                            .construct(tile_type=NullTile))
        temp_x = tile1.position.x
        temp_y = tile1.position.y

        tile1.position = (tile2.position.x, tile2.position.y)
        tile2.position = (temp_x, temp_y)
        
        self.board.place_tile(tile1)
        self.board.place_tile(tile2)
    
 

    def add_match_condition(self, match_cond):
        """
            Adds a match conditions that can affect this game state
            :arg match_cond: the new match condition
            :arg type: MatchCondition
            :returns: nothing
            :rtype: None
        """
        LOGGER.debug('Adding matching condition: %s', str(type(match_cond)))
        self._match_conditions.append(match_cond)

    @property
    def match_rules(self):
        """
            Return a reference to the collection of match rules that can affect this game state
            :returns: list of match conditions
            :rtype: list
        """
        return self._match_conditions

    @property
    def board(self) -> GameBoard:
        """
            Return a reference to this game state's board
            :returns: game board
            :rtype: GameBoard
        """
        return self._board

    @property
    def score(self) -> int:
        """
            Return a snapshot of the score at the time of request
            :returns: the score
            :rtype: int
        """
        return self._score.score
