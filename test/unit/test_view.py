import copy
from threading import Thread
import time
import pytest

from inf122_tmge.core.board_factory import BoardFactory
from inf122_tmge.core.tile_builder import TileBuilder
from inf122_tmge.model.tiles.tile import Tile
from inf122_tmge.view.view import View

# Mark test as integration to avoid executing with test suite
@pytest.mark.integration
def test_launch_view():
    """Manual integration test to visually inspect the board"""
    game_board = BoardFactory.create_board('default', 10, 24)
    view = View(game_board) 
    view.launch_view()


@pytest.mark.integration
def test_update_tile():
    """Manual integration test to see if a tile is drawn"""
    game_board = BoardFactory.create_board('default', 10, 24)
    tile_to_place = TileBuilder().add_position(3,3).add_color('red').construct()
    game_board.place_tile(tile_to_place, 3, 3)
    view = View(game_board) 

    view.launch_view()

@pytest.mark.integration
def test_threading_fill_board():
    """Manual integration test to see board is filled"""
    game_board = BoardFactory.create_board('default', 10, 24)
    view = View(game_board) 

    def place_thread():
        t1=Thread(target=place_tiles, daemon=True)
        t1.start()
  
    def place_tiles():
        for i in range(1,11):

            for j in range(1,25):
                tile_to_place = TileBuilder().add_position(i,j).add_color('red').construct()
                board2 = copy.deepcopy(game_board)

                board2.place_tile(tile_to_place, i, j)
                view.update_board(board2)
                time.sleep(.01667)
    
    # After 1000 ms execute the thread
    view.root.after(1000, place_thread)
    view.launch_view()