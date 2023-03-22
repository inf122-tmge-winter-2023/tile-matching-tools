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

    game_view.bind_key('<KeyRelease-w>', move_up)
    game_view.bind_key('<KeyRelease-s>', move_dn)
    game_view.bind_key('<KeyRelease-a>', move_left)
    game_view.bind_key('<KeyRelease-d>', move_right)

    def update():
        game_view.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

@pytest.mark.integration
def test_independent_game_view_bindings(move_rule_up, move_rule_down, move_rule_left, move_rule_right):
    gs1 = GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )
    gs2 = GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )
    moving_tile1 = TileBuilder() \
            .add_position(random.randint(1, gs1.board.num_cols), random.randint(1, gs1.board.num_rows)) \
            .add_color(random.choice(list(TileColor))) \
            .construct()
    moving_tile2 = TileBuilder() \
            .add_position(random.randint(1, gs2.board.num_cols), random.randint(1, gs2.board.num_rows)) \
            .add_color(random.choice(list(TileColor))) \
            .construct()

    gs1.board.place_tile(moving_tile1)
    gs2.board.place_tile(moving_tile2)


    root = tk.Tk()
    gv1 = GameView(root, gs1)
    gv2 = GameView(root, gs2)
    gv1.grid(row=0, column=0)
    gv2.grid(row=0, column=1)
    
    def move_up1(event):
        move_rule_up.move(gs1.board, moving_tile1)
        gs1.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_dn1(event):
        move_rule_down.move(gs1.board, moving_tile1)
        gs1.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_left1(event):
        move_rule_left.move(gs1.board, moving_tile1)
        gs1.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_right1(event):
        move_rule_right.move(gs1.board, moving_tile1)
        gs1.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    gv1.bind_key('<KeyRelease-w>', move_up1)
    gv1.bind_key('<KeyRelease-s>', move_dn1)
    gv1.bind_key('<KeyRelease-a>', move_left1)
    gv1.bind_key('<KeyRelease-d>', move_right1)

    def move_up2(event):
        move_rule_up.move(gs2.board, moving_tile2)
        gs2.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_dn2(event):
        move_rule_down.move(gs2.board, moving_tile2)
        gs2.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_left2(event):
        move_rule_left.move(gs2.board, moving_tile2)
        gs2.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    def move_right2(event):
        move_rule_right.move(gs2.board, moving_tile2)
        gs2.adjust_score(MatchCondition.MatchFound(random.randint(10, 50), []))

    gv2.bind_key('<KeyRelease-i>', move_up2)
    gv2.bind_key('<KeyRelease-k>', move_dn2)
    gv2.bind_key('<KeyRelease-j>', move_left2)
    gv2.bind_key('<KeyRelease-l>', move_right2)

    def update():
        gv1.update()
        gv2.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

