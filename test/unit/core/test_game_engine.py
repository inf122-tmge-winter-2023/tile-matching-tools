import pytest
from tilematch_tools.core import GameEngine
from tilematch_tools.core import BoardFactory
from tilematch_tools.core.tile_builder import TileBuilder
from tilematch_tools.model import GameBoard
from tilematch_tools.model import Scoring
from tilematch_tools.model import MovementRule
from tilematch_tools.model.match import MatchCondition
from tilematch_tools.model.tile_color import TileColor

@pytest.fixture
def simple_down_movement():
    class MoveDown(MovementRule):
        def exec(self, x, y):
            return (x + self._dx, y + self._dy)

    return MoveDown(0, 1)

@pytest.fixture
def simple_match():
    class SimpleMatch(MatchCondition):
        def __init__(self):
            super().__init__((1, 0), 4)

        def check_match(self, board, start_x, start_y):
            return super().MatchFound(4, matching_tiles=[])
    
    return SimpleMatch()

@pytest.fixture
def simple_score():
    class SimpleScore(Scoring):
        def award_for_match(self, match):
            super().award_for_match(match)

    return SimpleScore()

class TestGameEngine:
    def test_move_tile(self, simple_score, simple_down_movement):
        """
            Testing tile movement
        """
        game_engine = GameEngine(BoardFactory.create_board('default', 10, 24), simple_score)

        test_tile = TileBuilder().add_position(1,3).add_color(TileColor.RED).construct()
        game_engine.game_state.game_board.place_tile(test_tile)
        game_engine.move_tile(test_tile, simple_down_movement)
        assert game_engine.tile_at(1,4) == test_tile
    
    def test_match_tiles(self, simple_score, simple_match):
        """
            Testing match tile updates score
        """
        game_engine = GameEngine(BoardFactory.create_board('default', 10, 24), simple_score)
        tile_1 = TileBuilder().add_position(1,3).add_color(TileColor.RED).construct()
        tile_2 = TileBuilder().add_position(1,2).add_color(TileColor.RED).construct()
        game_engine.place_tile(tile_1)
        game_engine.place_tile(tile_2)
        game_engine.match_tiles(1,2,simple_match)
        assert game_engine.score == 4
