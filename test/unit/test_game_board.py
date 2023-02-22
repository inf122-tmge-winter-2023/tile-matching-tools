import pytest

from inf122_tmge.model.board.game_board import GameBoard
from inf122_tmge.core.board_factory import BoardFactory
from inf122_tmge.model.tiles.tile import Tile

def test_game_board_constructor():
    """Testing game_board's default constructor to ensure board is of proper height and width"""
    width = 10
    height = 24
    game_board = BoardFactory.create_board("default", width, height)
    board = game_board.board

    assert len(board) == width
    assert all(len(row) == height for row in board)
    assert all(isinstance(tile, Tile) for row in board for tile in row)