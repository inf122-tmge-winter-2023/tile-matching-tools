"""Tests for game view"""

import tkinter as tk

import pytest

from tilematch_tools.core import GameState, BoardFactory
from tilematch_tools.model import Scoring, GameBoard
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
