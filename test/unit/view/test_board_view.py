"""Tests for board view"""

import tkinter as tk
import random
import time

import pytest

from tilematch_tools import BoardFactory, GameBoard, BoardView, TileBuilder, MovementRule
from tilematch_tools.model.tiles import Tile, NullTile, TileColor

@pytest.fixture()
def simple_board():
    return BoardFactory.create_board(GameBoard, 10, 24)

@pytest.mark.integration
def test_simple_board_view(simple_board):
    root = tk.Tk()
    board_view = BoardView(root, simple_board)
    board_view.pack()
    root.mainloop()

@pytest.mark.integration
def test_tile_redraws(simple_board):
    root = tk.Tk()
    board_view = BoardView(root, simple_board)
    board_view.pack()

    def show_tile(event):
        flashing = TileBuilder() \
                .add_position(2, 2) \
                .add_color(TileColor.RED) \
                .construct(tile_type=NullTile)

        simple_board.place_tile(flashing)

    def hide_tile(event):
        nullify = TileBuilder() \
                .add_position(2, 2) \
                .add_color(TileColor.LIGHT_GRAY) \
                .construct(tile_type=NullTile)

        simple_board.place_tile(nullify)

    board_view.bind_all('<KeyRelease-f>', show_tile)
    board_view.bind_all('<KeyRelease-r>', hide_tile)

    def update_board_view():
        board_view.update()
        root.after(100, update_board_view)

    root.after(100, update_board_view)
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
def test_tile_movement(simple_board, move_rule_up, move_rule_down, move_rule_left, move_rule_right):
    root = tk.Tk()
    board_view = BoardView(root, simple_board)
    board_view.pack()
    moving_tile = TileBuilder() \
            .add_position(random.randint(1, simple_board.num_cols), random.randint(1, simple_board.num_rows)) \
            .add_color(random.choice(list(TileColor))) \
            .construct()
    simple_board.place_tile(moving_tile)

    def move_up(event):
        move_rule_up.move(simple_board, moving_tile)

    def move_dn(event):
        move_rule_down.move(simple_board, moving_tile)

    def move_left(event):
        move_rule_left.move(simple_board, moving_tile)

    def move_right(event):
        move_rule_right.move(simple_board, moving_tile)

    board_view.bind_all('<KeyRelease-w>', move_up)
    board_view.bind_all('<KeyRelease-s>', move_dn)
    board_view.bind_all('<KeyRelease-a>', move_left)
    board_view.bind_all('<KeyRelease-d>', move_right)

    def update_board_view():
        board_view.update()
        root.after(100, update_board_view)

    root.after(100, update_board_view)
    root.mainloop()
