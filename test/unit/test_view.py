from copy import deepcopy
import queue
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
from tilematch_tools.model.tiles.tile import NullTile
from tilematch_tools.model.board import GameBoard
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
        def __init__(self):
                super().__init__()

        def award_for_match(self, match):
            self._points += len(match.matching_tiles)

    return SimpleScore()

@pytest.mark.integration
@pytest.fixture
def row_match():
    class RowMatch(MatchCondition):
        def check_match(self, board, start_x, start_y):
            matching_tiles = []
            try:
                for x in range(start_x, start_x - 9, -1):
                    if not isinstance(board.tile_at(x + self._scan_delta[0], start_y  + self._scan_delta[1]), NullTile) and \
                        not isinstance(board.tile_at(x , start_y), NullTile):
                        if board.tile_at(x, start_y) == board.tile_at(start_x + self._scan_delta[0], start_y + self._scan_delta[1]):
                            matching_tiles.append(board.tile_at(x, start_y))
                            matching_tiles.append(board.tile_at(x + self._scan_delta[0], start_y  + self._scan_delta[1]))
                    else:
                        matching_tiles = []
                        break
                if len(matching_tiles) == 0:
                    return None
                return self.MatchFound(self.point_value, 
                    matching_tiles
                )
            except InvalidBoardPositionError:
                return None
    return RowMatch((-1, 0), 4)

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
def test_demo(simple_up_movement, simple_down_movement, simple_score : Scoring, row_match : MatchCondition):
    """Demo test"""
    ex_env = ExecutionEnviornment()
    game_board = BoardFactory.create_board(GameBoard, 10, 24)
    game_score = simple_score
    game_state = GameState(game_board, game_score)
    view = View(game_state, ex_env.root) 
    view2 = View(game_state, ex_env.root)

    view.add_event_listener("KeyRelease")
    game_engine = GameEngine(game_board,game_score)

    # Places some tiles
    for x in range(1,11):
        if x == 5:
            pass
        else:
            game_engine.place_tile(TileBuilder().add_position(x,1).add_color('red').construct())


    def gameloop():
        fps = 30
        moving_tile = TileBuilder().add_position(5,10).add_color('red').construct()
        game_engine.place_tile(moving_tile)
        while not ex_env.quit:
            
            try:
                matched = game_engine.match_tiles(game_board.num_cols,1, row_match)
                if matched or moving_tile.position.y == 1:
                    moving_tile = TileBuilder().add_position(5,4).add_color('red').construct()
                    game_engine.place_tile(moving_tile)
                user_event = view.key_event
                if user_event == "w":
                    game_engine.move_tile(moving_tile, simple_up_movement)
                elif user_event == "s":
                    game_engine.move_tile(moving_tile, simple_down_movement)
          
            except queue.Empty:
                pass
            except Exception as e:
                print(e)
            view.update_game_state(game_state)
            view2.update_game_state(game_state)

            time.sleep(1/fps)

    ex_env.set_view(view)
    ex_env.set_view2(view2)

    ex_env.launch(gameloop)

@pytest.mark.integration
def test_swap( simple_score : Scoring, row_match : MatchCondition):
    """Demo test"""
    ex_env = ExecutionEnviornment()
    game_board = BoardFactory.create_board(GameBoard, 10, 24)
    game_score = simple_score
    game_state = GameState(game_board, game_score)
    view = View(game_state, ex_env.root) 
    view2 = View(game_state, ex_env.root)

    view.add_event_listener("ButtonRelease")
    view2.add_event_listener("ButtonRelease")
    game_engine = GameEngine(game_board,game_score)

    # Places some tiles
    for x in range(1,11):
        if x == 5:
            pass
        else:
            game_engine.place_tile(TileBuilder().add_position(x,1).add_color('red').construct())


    def gameloop():
        fps = 30
        moving_tile = TileBuilder().add_position(5,10).add_color('red').construct()
        game_engine.place_tile(moving_tile)
        first_click = None
        while not ex_env.quit:  
            try:
                matched = game_engine.match_tiles(game_board.num_cols,1, row_match)
                if matched or moving_tile.position.y == 1:
                    moving_tile = TileBuilder().add_position(5,4).add_color('red').construct()
                    game_engine.place_tile(moving_tile)
                if first_click is not None:
                    second_click = view.mouse_event
                    if second_click is not None:
                        game_engine.swap_tiles(game_engine.tile_at(first_click[0], first_click[1]),
                                               game_engine.tile_at(second_click[0], second_click[1])) 
                        first_click = None
                else:
                    first_click = view.mouse_event 
                
            except queue.Empty:
                pass
            except Exception as e:
                print(e)
            view.update_game_state(game_state)
            view2.update_game_state(game_state)

            time.sleep(1/fps)

    ex_env.set_view(view)
    ex_env.set_view2(view2)

    ex_env.launch(gameloop)