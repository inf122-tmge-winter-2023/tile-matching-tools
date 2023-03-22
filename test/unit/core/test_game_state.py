import pytest
from tilematch_tools.core import GameState, BoardFactory, TileBuilder
from tilematch_tools.model import Scoring, MovementRule, MatchCondition, TileColor, GameBoard
from tilematch_tools.model.exceptions import IllegalTileMovementException, InvalidBoardPositionError
from tilematch_tools.model.tiles.tile import NullTile

@pytest.fixture
def simple_down_movement():
    class MoveDown(MovementRule):
        def apply(self, board, tile):
            tile.position = (tile.position.x, tile.position.y - 1)
            board.place_tile(tile)

    return MoveDown()

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


class SimpleScore(Scoring):
    def __init__(self):
        super().__init__()

    def award_for_match(self, match):
        self._points += 4


class TestGameState:
    
    def setup_method(self, simple_score):
        self.state = GameState(
                BoardFactory.create_board(GameBoard, 10, 24),
                SimpleScore()
                )

    def test_move_tile(self, simple_down_movement):
        """
            Testing tile movement
        """

        test_tile = TileBuilder().add_position(1,3).add_color(TileColor.RED).construct()
        self.state.board.place_tile(test_tile)
        self.state.move_tile(test_tile, simple_down_movement)
        assert self.state.board.tile_at(1,2) == test_tile
    
    def test_cant_move_immovable(self, simple_down_movement):
        test_tile = TileBuilder().add_position(1,3).add_color(TileColor.RED).construct()
        test_tile._movable = False
        self.state.board.place_tile(test_tile)
        self.state.move_tile(test_tile, simple_down_movement)
        assert test_tile.position.y == 3


    def test_find_match(self, two_match):
        tile_1 = TileBuilder().add_position(1,3).add_color(TileColor.RED).construct()
        tile_2 = TileBuilder().add_position(1,2).add_color(TileColor.RED).construct()
        self.state.board.place_tile(tile_1)
        self.state.board.place_tile(tile_2)
        assert self.state.find_match(1, 3, two_match)

    def test_handle_match(self, two_match):
        """
            Testing match tile updates score
        """
        tile_1 = TileBuilder().add_position(1,3).add_color(TileColor.RED).construct()
        tile_2 = TileBuilder().add_position(1,2).add_color(TileColor.RED).construct()
        self.state.board.place_tile(tile_1)
        self.state.board.place_tile(tile_2)
        match = self.state.find_match(1,3,two_match)
        self.state.clear_match(match)
        self.state.adjust_score(match)
        assert self.state.score.score == 4
        assert isinstance(self.state.board.tile_at(1, 3), NullTile)
        assert isinstance(self.state.board.tile_at(1, 2), NullTile)

    def test_tiles_dont_match(self, two_match):
        """
            Testing match tile updates score
        """
        tile_1 = TileBuilder().add_position(5,3).add_color(TileColor.RED).construct()
        tile_2 = TileBuilder().add_position(1,2).add_color(TileColor.RED).construct()
        self.state.board.place_tile(tile_1)
        self.state.board.place_tile(tile_2)
        
        assert self.state.find_match(1,3,two_match) is None

    def test_swap_tiles(self):
        tile_1 = TileBuilder().add_position(1,3).add_color(TileColor.BLUE).construct()
        tile_2 = TileBuilder().add_position(1,2).add_color(TileColor.RED).construct()
        self.state.board.place_tile(tile_1)
        self.state.board.place_tile(tile_2)
        self.state.swap_tiles(tile_1, tile_2)
        assert tile_1.position.y == 2
        assert tile_2.position.y == 3
        assert self.state.board.tile_at(1,3).color == TileColor.RED
        assert self.state.board.tile_at(1,2).color == TileColor.BLUE
