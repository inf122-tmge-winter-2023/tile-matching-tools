"""Tests for match condition"""

import pytest

from tilematch_tools.model.match import MatchCondition
from tilematch_tools.model import GameBoard
from tilematch_tools.model.exceptions import InvalidBoardPositionError
from tilematch_tools.model.tiles import Tile

@pytest.fixture
def two_match():
    class TwoMatch(MatchCondition):
        def check_match(self, board, start_x, start_y):
            try:
                if self._eq(
                    board.tile_at(start_x, start_y),
                    board.tile_at(
                        start_x + self._scan_delta[0],
                        start_y + self._scan_delta[1]
                            )
                    ):
                    return self.MatchFound(self.point_value, [
                        board.tile_at(start_x, start_y),
                        board.tile_at(
                            start_x + self._scan_delta[0],
                            start_y + self._scan_delta[1]
                            )        
                        ]
                    )
                return None
            except InvalidBoardPositionError:
                return None
    return TwoMatch((0, -1), 4)


def test_match_condition_must_implement_the_match_interface():
    with pytest.raises(TypeError):
        m = MatchCondition((0, 1), lambda: False)

    with pytest.raises(TypeError):
        class TestCondition(MatchCondition):
            def i_dont_implement_the_match_interface():
                pass
        m = TestCondition((0, 1), lambda: False)

class TestMatchOnBoard:
    def setup_method(self):
        self._board = GameBoard(3, 3)
        self._board.place_tile(Tile(**{'position': (1, 1)}))
        self._board.place_tile(Tile(**{'position': (1, 2)}))
        self._board.place_tile(Tile(**{'position': (2, 2)}))

    def test_can_detect_a_match(self, two_match):
        assert two_match.check_match(self._board, 1, 2)

    def test_can_detect_a_nonmatch(self, two_match):
        assert not two_match.check_match(self._board, 2, 2)

    def test_can_read_match_conditions_point_value_as_property(self, two_match):
        assert two_match.point_value == 4
