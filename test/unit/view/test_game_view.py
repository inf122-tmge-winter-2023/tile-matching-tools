"""Tests for game view"""

import tkinter as tk
import random

import pytest

from tilematch_tools.core import GameState, BoardFactory, TileBuilder
from tilematch_tools.model import Scoring, GameBoard, MovementRule, Tile, TileColor, MatchCondition
from tilematch_tools.view import GameView

@pytest.fixture
def simple_game_state():
    return GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )

@pytest.mark.integration
def test_simple_game_view(simple_game_state):
    root = tk.Tk()
    game_view = GameView(root, simple_game_state)
    game_view.pack()
    root.mainloop()

@pytest.fixture
def move_rule_up():
    class MoveUp(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x, tile_to_move.position.y + 1)
            board.place_tile(tile_to_move)

    return MoveUp()

@pytest.fixture
def move_rule_down():
    class MoveDown(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x, tile_to_move.position.y - 1)
            board.place_tile(tile_to_move)
    
    return MoveDown()

@pytest.fixture
def move_rule_left():
    class MoveLeft(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x - 1, tile_to_move.position.y)
            board.place_tile(tile_to_move)

    return MoveLeft()

@pytest.fixture
def move_rule_right():
    class MoveRight(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x + 1, tile_to_move.position.y)
            board.place_tile(tile_to_move)
    
    return MoveRight()

@pytest.mark.integration
def test_game_view_update_cycle(simple_game_state, move_rule_up, move_rule_down, move_rule_left, move_rule_right):
    moving_tile = TileBuilder() \
            .add_position(random.randint(1, simple_game_state.board.num_cols), random.randint(1, simple_game_state.board.num_rows)) \
            .add_color(random.choice(list(TileColor))) \
            .construct()
    simple_game_state.board.place_tile(moving_tile)


    root = tk.Tk()
    game_view = GameView(root, simple_game_state)
    game_view.pack()
    
    def move_up(event):
        move_rule_up.move(simple_game_state.board, moving_tile)
        simple_game_state.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_dn(event):
        move_rule_down.move(simple_game_state.board, moving_tile)
        simple_game_state.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_left(event):
        move_rule_left.move(simple_game_state.board, moving_tile)
        simple_game_state.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_right(event):
        move_rule_right.move(simple_game_state.board, moving_tile)
        simple_game_state.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    game_view.bind_all('<KeyRelease-w>', move_up)
    game_view.bind_all('<KeyRelease-s>', move_dn)
    game_view.bind_all('<KeyRelease-a>', move_left)
    game_view.bind_all('<KeyRelease-d>', move_right)

    def update():
        game_view.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

