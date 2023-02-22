import pytest

from inf122_tmge import gimme_five
from inf122_tmge.model.board.game_board import GameBoard
from inf122_tmge.model.tiles.tile import Tile

def test_vacuous():
    """A test the passes vacuously"""
    pass

@pytest.mark.parametrize("owed, final", [
    (0, 5),
    (1, 4),
    (2, 3),
    (3, 2),
    (4, 1),
    (5, 0)
])
def test_gimme_five(owed, final):
    """Test the gimme five sample function"""
    assert gimme_five() - owed == final

def test_exception_is_raised():
    """Test that an exception is raised"""
    with pytest.raises(ValueError):
        raise ValueError

def test_game_board_constructor():
    """Testing game_board's default constructor to ensure board is of proper height and width"""
    width = 10
    height = 24
    board = GameBoard(width, height).board

    assert len(board) == width
    assert all(len(row) == height for row in board)
    assert all(isinstance(tile, Tile) for row in board for tile in row)