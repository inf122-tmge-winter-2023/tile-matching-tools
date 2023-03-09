import pytest

from tilematch_tools.model.exceptions import InvalidBoardPositionError, IllegalBoardContentException
from tilematch_tools.model.board.game_board import GameBoard
from tilematch_tools.model.tiles.tile import Tile

width = 10
height = 24

class TestGameBoard:

    def setup_method(self):
        self.board = GameBoard(width, height)

    def test_game_board_constructor(self):
        """Testing game_board's default constructor to ensure board is of proper height and width"""
        assert len(self.board.board) == width
        assert all(len(row) == height for row in self.board.board)
        assert all(isinstance(tile, Tile) for row in self.board.board for tile in row)
    
    @pytest.mark.parametrize("x, y", [
        (x, y) 
        for x in range(1, width + 1) 
        for y in range(1, height + 1)
        ]
    )
    def test_tile_at(self, x, y):
        tile = self.board.tile_at(x, y)
        assert isinstance(tile, Tile)
        assert tile.position.x == x
        assert tile.position.y == y

    @pytest.mark.parametrize("x, y", [
            (0, 0),
            (width + 5, height + 10),
            (1, height + 5), 
            (0, height)
        ]
    )
    def test_tile_retrieval_at_invalid_positions(self, x, y):
        with pytest.raises(InvalidBoardPositionError):
            tile = self.board.tile_at(x, y)

    def test_tile_placement_with_tile_like_object(self):
        class SomeTile(Tile):
            pass
        self.board.place_tile(SomeTile(**{'position': (2, 2)}))
        assert type(self.board.tile_at(2, 2)) == SomeTile

    @pytest.mark.parametrize("o", [int, str, list, tuple, dict, set])
    def test_tile_placement_with_non_tile_object(self, o):
        with pytest.raises(IllegalBoardContentException):
            self.board.place_tile(o())

    @pytest.mark.parametrize("x, y", [
            (0, 0),
            (width + 5, height + 10),
            (1, height + 5),
            (0, height)
        ]
    )
    def test_tile_placement_with_invalid_position(self, x, y):
        class SomeTile(Tile):
            pass
        with pytest.raises(InvalidBoardPositionError):
            self.board.place_tile(SomeTile(**{'position': (x, y)}))
