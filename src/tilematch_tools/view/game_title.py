"""
    :module_name: game_title
    :module_summary: a GUI widget for displaying a game's title
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""
import tkinter as tk
import tkinter.font as tkFont

from .game_widgets import GameInfo

class GameTitle(GameInfo):
    
    def __init__(self, parent, game_title, **options):
        self._title = game_title
        super().__init__(parent, **options)

    def create_widgets(self):
        self._title_container = tk.Label(self, text=self.showing, anchor=tk.W, font=self.font)

    def place_widgets(self):
        self._title_container.pack()

    @property
    def showing(self):
        return self._title

    @property
    def font(self):
        return tkFont.Font(family='Helvetica', size=48)

    def update(self):
        pass
