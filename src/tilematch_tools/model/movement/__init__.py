"""
    :module_name: movement
    :module_summary: a class the controls how a tile is allowed to move
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
from abc import ABC, abstractmethod

from ..tiles import Tile, NullTile
from ..board import GameBoard
from ..exceptions import IllegalTileMovementException, InvalidBoardPositionError

LOGGER = logging.getLogger(__name__)

class MovementRule(ABC):
    """
        Class that represents how a tile's position should adjust
        :arg callback: a callable object to be called after the movement is applied
    """

    def __init__(self, callback: callable = None):
        self._after = callback
        self._origin_x = None
        self._origin_y = None

    def move(self, board: GameBoard, tile_to_move: Tile, *callback_args) -> None:
        """
            Apply this movement rule to the given tile on the specific gameboard
            Then calls the callback if one exists
            :arg board: gameboard the move will be made on
            :arg tile_to_move: tile to be moved
            :arg *callback_args: additional arguments to be passed to the callback
            :arg type: GameBoard
            :arg type: Tile
            :arg type: tuple
        """
        if not tile_to_move.mobile:
            LOGGER.error(
                    'Attempting to move immovable tile at (%d, %d)',
                    tile_to_move.position.x,
                    tile_to_move.position.y
                    )
            return
        self._origin_x = tile_to_move.position.x
        self._origin_y = tile_to_move.position.y
        try:
            LOGGER.info(
                    'Attempting to move tile at (%d, %d)', 
                    tile_to_move.position.x,
                    tile_to_move.position.y
                    )
            self.apply(board, tile_to_move)
        except (IllegalTileMovementException, InvalidBoardPositionError):
            LOGGER.error('Could not apply movement rule %s. Reverting tile state', str(self))
            self.revert(board, tile_to_move)
        else:
            LOGGER.info(
                    'Tile successfully moved from (%d, %d) -> (%d, %d)',
                    self._origin_x,
                    self._origin_y,
                    tile_to_move.position.x,
                    tile_to_move.position.y
                    )
            self._mark_null(board)
        finally:
            if self._after:
                self._after(*callback_args)

    @abstractmethod
    def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
        """
            Logic for executing this tile movement. Should raise exception if cannot be completed
            :arg board: gameboard move will be executed on
            :arg tile_to_move: tile to be moved by this movement rule
            :arg type: GameBoard
            :arg type: Tile
            :raises: IllegalTileMovementException if the tile movement is illegal
            :raises: InvalidBoardPositionError if the tile's new position is invalid
        """
        LOGGER.warning('Using default implementation. This is meant to be overridden!')

    def revert(self, board: GameBoard, tile_to_move: Tile) -> None:
        """
            Reverts this movement rule by restoring tile_to_move original position
            :arg board: gameboard on which move will be reverted
            :arg tile_to_move: tile which will be un-moved
            :arg type: GameBoard
            :arg type: Tile
        """
        LOGGER.info('Reverting tile to position (%d, %d)', self._origin_x, self._origin_y)
        tile_to_move.position = (self._origin_x, self._origin_y)

    def _mark_null(self, board: GameBoard):
        LOGGER.info('Marking (%d, %d) with a null tile', self._origin_x, self._origin_y)
        board.place_tile(
                NullTile(
                    **{
                        'position': (self._origin_x, self._origin_y),
                        'color': '#D3D3D3'
                    }
                )
        )
