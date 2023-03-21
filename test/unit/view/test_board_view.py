"""Tests for board view"""

import tkinter as tk
import random
import time

import pytest

from tilematch_tools import BoardFactory, GameBoard, BoardView, TileBuilder
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

