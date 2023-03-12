import queue
import time
import pytest

from tilematch_tools.core.board_factory import BoardFactory
from tilematch_tools.core.tile_builder import TileBuilder
from tilematch_tools.view.view import View
from tilematch_tools import LOG_HANDLER
from tilematch_tools import LOGGER

@pytest.mark.integration
def setup_function():
    # Disable logger for Integration Tests
    LOG_HANDLER.setLevel(51)
    LOGGER.setLevel(51)

# Mark test as integration to avoid executing with test suite
@pytest.mark.skip
def test_launch_view():
    """Manual integration test to visually inspect the board"""
    game_board = BoardFactory.create_board('default', 10, 24)
    view = View(game_board) 
    view.launch_view()


@pytest.mark.skip
def test_update_tile():
    """Manual integration test to see if a tile is drawn"""
    game_board = BoardFactory.create_board('default', 10, 24)
    tile_to_place = TileBuilder().add_position(3,3).add_color('red').construct()
    game_board.place_tile(tile_to_place)
    view = View(game_board) 
    view.launch_view()

@pytest.mark.skip
def test_threading_fill_board():
    """Manual integration test to see board is filled one by one"""
    game_board = BoardFactory.create_board('default', 10, 24)
    view = View(game_board) 

    def place_tiles():
        for i in range(1,11):
            for j in range(1,25):
                tile_to_place = TileBuilder().add_position(i,j).add_color('red').construct()

                game_board.place_tile(tile_to_place)
                view._update_board_view(game_board)
                time.sleep(.0165)

    view.launch_view(place_tiles)

@pytest.mark.integration
def test_user_input():
    """Manual integration testing a user input"""
    game_board = BoardFactory.create_board('default', 10, 24)
    view = View(game_board) 

    moving_tile = TileBuilder().add_position(5,1).add_color('red').construct()
    game_board.place_tile(moving_tile)

    view.add_event_listener('KeyRelease')
    def move_down():
        clear_tile = TileBuilder().add_position(moving_tile.position.x, moving_tile.position.y).add_color('#D3D3D3').construct()
        game_board.place_tile(clear_tile)
        moving_tile.position.y += 1
        game_board.place_tile(moving_tile)

    def gameloop():
        score = 0
        while not view.quit:
            try:
                if view.key_event == 'w':
                    move_down()
            except queue.Empty:
                pass
            view.update(game_board,score)
            score += 1
            time.sleep(.0165)

    view.launch_view(gameloop)


@pytest.mark.integration
def test_mouse_input():
    """Manual integration testing a user input"""
    game_board = BoardFactory.create_board('default', 12, 12)
    view = View(game_board) 

    def flip_tile(row, col):
        if(game_board.tile_at(row, col).color == 'red'):
            color = '#D3D3D3'
        else:
            color = 'red'
        tile_to_flip = TileBuilder().add_position(row,col).add_color(color).construct()
        game_board.place_tile(tile_to_flip)

    view.add_event_listener('ButtonRelease')
    
    
    def gameloop():
        score = 0
        while not view.quit:
            score += 1
            try:
                clicked_on = view.mouse_event
                flip_tile(clicked_on[0], clicked_on[1])
            except queue.Empty:
                pass
            view.update(game_board,score)
            time.sleep(.0165)

    view.launch_view(gameloop)