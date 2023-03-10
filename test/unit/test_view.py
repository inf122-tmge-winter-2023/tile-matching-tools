import queue
import time
import pytest

from tilematch_tools.core.board_factory import BoardFactory
from tilematch_tools.core.game_state import GameState
from tilematch_tools.core.tile_builder import TileBuilder
from tilematch_tools.model.score import Scoring
from tilematch_tools.view.view import View
from tilematch_tools import LOG_HANDLER
from tilematch_tools import LOGGER


@pytest.mark.integration
def setup_function():
    # Disable logger for Integration Tests
    LOG_HANDLER.setLevel(51)
    LOGGER.setLevel(51)

@pytest.mark.integration
@pytest.fixture
def simple_score():
    class SimpleScore(Scoring):
        def award_for_match(self, match):
            super().award_for_match(match)

    return SimpleScore()


@pytest.mark.integration
def test_user_input(simple_score):
    """Manual integration testing a user input"""
    game_board = BoardFactory.create_board('default', 10, 24)
    game_score = simple_score
    game_state = GameState(game_board, game_score)
    view = View(game_state) 
    moving_tile = TileBuilder().add_position(5,1).add_color('red').construct()
    game_state.game_board.place_tile(moving_tile)

    view.add_event_listener('KeyRelease')
    def move_down():
        clear_tile = TileBuilder().add_position(moving_tile.position.x, moving_tile.position.y).add_color('#D3D3D3').construct()
        game_board.place_tile(clear_tile)
        moving_tile.position.y += 1
        game_board.place_tile(moving_tile)

    def gameloop():
        while not view.quit:
            try:
                if view.key_event == 'w':
                    move_down()
            except queue.Empty:
                pass
            view.update(game_state)
            time.sleep(.0165)

    view.launch_view(gameloop)


@pytest.mark.integration
def test_mouse_input(simple_score):
    """Manual integration testing a user input"""
    game_board = BoardFactory.create_board('default', 12, 12)
    game_score = simple_score
    game_state = GameState(game_board, game_score)

    view = View(game_state) 

    def flip_tile(row, col):
        if(game_board.tile_at(row, col).color == 'red'):
            color = '#D3D3D3'
        else:
            color = 'red'
        tile_to_flip = TileBuilder().add_position(row,col).add_color(color).construct()
        game_board.place_tile(tile_to_flip)

    view.add_event_listener('ButtonRelease')
    
    
    def gameloop():
        while not view.quit:
            try:
                clicked_on = view.mouse_event
                flip_tile(clicked_on[0], clicked_on[1])
            except queue.Empty:
                pass
            view.update(game_state)
            time.sleep(.0165)

    view.launch_view(gameloop)