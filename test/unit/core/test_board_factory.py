"""Tests for board factory"""

import pytest

from tilematch_tools.core import BoardFactory
from tilematch_tools.model.board import GameBoard

class TestBoardFactory:
    width = 10
    height = 24

    def test_factory_creates_an_instance_of_board(self):
        assert isinstance(
                BoardFactory.create_board(
                    '',
                    TestBoardFactory.width,
                    TestBoardFactory.height),
                GameBoard
        )

    def test_subsequent_calls_produce_different_boards(self):
        board1 = BoardFactory.create_board(
                '',
                TestBoardFactory.width,
                TestBoardFactory.height)
        board2 = BoardFactory.create_board(
                '',
                TestBoardFactory.width,
                TestBoardFactory.height)
        assert not board1 is board2
