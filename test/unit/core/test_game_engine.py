import pytest
from tilematch_tools.core import GameEngine, BoardFactory, TileBuilder
from tilematch_tools.model import Scoring, MovementRule, MatchCondition, TileColor
from tilematch_tools.model.exceptions import InvalidBoardPositionError
from tilematch_tools.model.tiles.tile import NullTile

@pytest.fixture
def simple_down_movement():
    class MoveDown(MovementRule):
        def exec(self, x, y):
            return (x + self._dx, y + self._dy)

    return MoveDown(0, 1)

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


@pytest.fixture
def simple_score():
    class SimpleScore(Scoring):
        def __init__(self):
            super().__init__()

        def award_for_match(self, match):
            self._points += 4

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
    
    def test_match_tiles(self, simple_score, two_match):
        """
            Testing match tile updates score
        """
        game_engine = GameEngine(BoardFactory.create_board('default', 10, 24), simple_score)
        tile_1 = TileBuilder().add_position(1,3).add_color(TileColor.RED).construct()
        tile_2 = TileBuilder().add_position(1,2).add_color(TileColor.RED).construct()
        game_engine.place_tile(tile_1)
        game_engine.place_tile(tile_2)
        game_engine.match_tiles(1,3,two_match)
        assert game_engine.score == 4
        assert isinstance(game_engine.tile_at(1, 3), NullTile)
        assert isinstance(game_engine.tile_at(1, 2), NullTile)

    def test_swap_tiles(self, simple_score):
        game_engine = GameEngine(BoardFactory.create_board('default', 10, 24), simple_score)
        tile_1 = TileBuilder().add_position(1,3).add_color(TileColor.BLUE).construct()
        tile_2 = TileBuilder().add_position(1,2).add_color(TileColor.RED).construct()
        game_engine.place_tile(tile_1)
        game_engine.place_tile(tile_2)
        game_engine.swap_tiles(tile_1, tile_2)
        assert tile_1.position.y == 2
        assert tile_2.position.y == 3
        assert game_engine.tile_at(1,3).color == TileColor.RED
        assert game_engine.tile_at(1,2).color == TileColor.BLUE