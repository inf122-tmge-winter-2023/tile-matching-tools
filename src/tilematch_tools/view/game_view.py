"""
    :module_name: game_view
    :module_summary: GUI widget for displaying a game's widgets
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import tkinter as tk

from ..core import GameState
from .score_view import ScoreView
from .board_view import BoardView
from .game_widgets import GameWidget
from .game_event import GameEvent

class GameView(GameWidget):
    """
        GUI widget for displaying a game's widgets
    """

    def __init__(self, parent, game_to_watch: GameState):
        self._game = game_to_watch
        super().__init__(parent)

    def create_widgets(self):
        self._game_widgets  = {
                'score': ScoreView(self, self._game.score),
                'board': BoardView(self, self._game.board)
            }

    def place_widgets(self):
        self._game_widgets['board'].grid(column=1, row=1, columnspan=3, rowspan=4, padx=30, pady=30)
        self._game_widgets['score'].grid(column=6, row=4, padx=30)

    def update(self):
        for w in self._game_widgets.values():
            w.update()

    @property
    def board_view(self):
        return self._game_widgets['board']

    @property
    def score_view(self):
        return self._game_widgets['score']

    def bind_key(self, key_sequence: str, handler: GameEvent) -> None:
        self.bind_all(key_sequence, handler)

    def bind_click(self, mouse_button: str, handler: GameEvent) -> None:
        self._game_widgets['board'].showing.bind(mouse_button, handler)
        
