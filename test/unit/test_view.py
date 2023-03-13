from copy import deepcopy
from threading import Thread
import time
import tkinter
import pytest

from tilematch_tools.core.board_factory import BoardFactory
from tilematch_tools.core.game_engine import GameEngine
from tilematch_tools.core.game_state import GameState
from tilematch_tools.core.tile_builder import TileBuilder
from tilematch_tools.model.exceptions import InvalidBoardPositionError
from tilematch_tools.model.match import MatchCondition
from tilematch_tools.model.score import Scoring
from tilematch_tools.model.tiles.movement_rule import MovementRule
from tilematch_tools.view.view import View
from tilematch_tools import LOG_HANDLER
from tilematch_tools import LOGGER


class ExecutionEnviornment: 
    def __init__(self):
        self.root = tkinter.Tk()
        self.quit = False
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_view(self, view: View):
        self.view = view
        self.view.main_container.pack(side="left", fill="both")

    def set_view2(self, view: View):
        self.view2 = view
        self.view2.main_container.pack(side="left", fill="both")

    def launch(self, gameloop):
        self.thread = Thread(target=gameloop)
        self.root.after(200, self.thread.start())
        if self.view is not None and self.view2 is not None:
            while not self.quit:
                self.view.update_container()
                self.view2.update_container()
        else:
            print("Need to set views")
            self.on_close()

    def on_close(self):
        self.quit = True
        self.thread.join()  # Wait for thread to finish

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

# @pytest.mark.integration
# @pytest.fixture
# def two_match():
#     class TwoMatch(MatchCondition):
#         def check_match(self, board, start_x, start_y):
#             try:
#                 if self._eq(
#                     board.tile_at(start_x, start_y),
#                     board.tile_at(
#                         start_x + self._scan_delta[0],
#                         start_y + self._scan_delta[1]
#                             )
#                     ):
#                     return self.MatchFound(self.point_value, [
#                         board.tile_at(start_x, start_y),
#                         board.tile_at(
#                             start_x + self._scan_delta[0],
#                             start_y + self._scan_delta[1]
#                             )        
#                         ]
#                     )
#                 return None
#             except InvalidBoardPositionError:
#                 return None
#     return TwoMatch((0, -1), 4)

@pytest.fixture
def simple_up_movement():
    class MoveUp(MovementRule):
        def exec(self, x, y):
            return (x + self._dx, y + self._dy)

    return MoveUp(0, 1)

@pytest.fixture
def simple_down_movement():
    class MoveDown(MovementRule):
        def exec(self, x, y):
            return (x + self._dx, y + self._dy)

    return MoveDown(0, -1)

@pytest.mark.integration
def test_demo(simple_up_movement, simple_down_movement, simple_score):
    """Demo test"""
    ex_env = ExecutionEnviornment()
    game_board = BoardFactory.create_board('default', 10, 24)
    game_score = simple_score
    game_state = GameState(game_board, game_score)
    view = View(game_state, ex_env.root) 
    view2 = View(game_state, ex_env.root)

    view.add_event_listener("KeyRelease")
    game_engine = GameEngine(game_board,game_score)
    moving_tile = TileBuilder().add_position(5,1).add_color('red').construct()
    game_engine.place_tile(moving_tile)

    def gameloop():
        fps = 30
        while not ex_env.quit:
            try:
                user_event = view.key_event
                if user_event == "w":
                    game_engine.move_tile(moving_tile, simple_up_movement)
                elif user_event == "s":
                    game_engine.move_tile(moving_tile, simple_down_movement)
            except:
                pass
            view.update_game_state(game_state)
            view2.update_game_state(game_state)

            time.sleep(1/fps)

    ex_env.set_view(view)
    ex_env.set_view2(view2)

    ex_env.launch(gameloop)
