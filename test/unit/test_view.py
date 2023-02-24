import pytest

from inf122_tmge.core.board_factory import BoardFactory
from inf122_tmge.model.tiles.tile import Tile
from inf122_tmge.view.view import View

# Mark test as integration to avoid executing with test suite
@pytest.mark.integration
def test_launch_view():
    """Manual integration test to visually inspect the board"""
    game_board = BoardFactory.create_board('default', 10, 24)
    view = View(game_board) 
    view.launch_view()


# @pytest.mark.integration
# def test_update_tile():
#     """Manual integration test to see if a tile is drawn"""
#     game_board = BoardFactory.create_board('default', 10, 24)
#     game_board.update_tile(3, 3, Tile(3,3,'red'))
#     view = View(game_board) 

#     view.launch_view()
