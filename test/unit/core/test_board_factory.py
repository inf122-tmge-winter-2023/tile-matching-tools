"""Tests for board factory"""

import pytest

from tilematch_tools.core import BoardFactory
from tilematch_tools.model.board import GameBoard
from tilematch_tools import TileBuilder

class TestBoardFactory:
    width = 10
    height = 24

    def test_factory_creates_an_instance_of_board(self):
        assert isinstance(
                BoardFactory.create_board(
                    GameBoard,
                    TestBoardFactory.width,
                    TestBoardFactory.height),
                GameBoard
        )

    def test_subsequent_calls_produce_different_boards(self):
        board1 = BoardFactory.create_board(
                GameBoard,
                TestBoardFactory.width,
                TestBoardFactory.height)
        board2 = BoardFactory.create_board(
                GameBoard,
                TestBoardFactory.width,
                TestBoardFactory.height)
        assert not board1 is board2

    def test_factory_with_tiles_methods_places_tiles_on_board(self):
        tiles = [
            TileBuilder() \
                    .add_position(x + 1, y + 1) \
                    .construct() 
                    for x in range(TestBoardFactory.width)
                    for y in range(TestBoardFactory.height)
        ]

        board = BoardFactory.create_board_with_tiles(
                GameBoard,
                TestBoardFactory.width,
                TestBoardFactory.height,
                tiles
                )
        for x in range(TestBoardFactory.width):
            for y in range(TestBoardFactory.height):
                assert board.tile_at(x + 1, y + 1) in tiles
