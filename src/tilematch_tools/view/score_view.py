"""
    :module_name: score_view
    :module_summary: GUI widget for displaying a game score
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import tkinter as tk
import tkinter.font as tkFont

from ..model.score import Scoring


class ScoreView(tk.Frame):
    """
        GUI widget for displaying a game score
        :arg parent: GUI widget
        :arg score_to_watch: score to update this widget
        :arg **oprtions: configuration
    """
    
    def __init__(self, parent, score_to_watch, **options):
        super().__init__(parent, **options)
        self._watching = score_to_watch
        self._create_widgets()
        self._place_widgets()

    @property
    def font(self):
        return tkFont.Font(family='Helvetica', size=16)

    @property
    def watching(self):
        return self._watching.score

    @property
    def showing(self):
        if not hasattr(self, '_showing'):
            self._showing = tk.StringVar()
            self._showing.set('0')
            
        return self._showing

    def update_score_display(self):
        current_display = int(self.showing.get())
        if current_display < self.watching:
            self.showing.set(str(current_display + 1))
        elif current_display > self.watching:
            self.showing.set(str(current_display - 1))

    def _create_widgets(self):
        self._score_label = tk.Label(self, text='Score: ', font=self.font, width=10, anchor=tk.W)
        self._score_display = tk.Label(self, textvariable=self.showing, font=self.font, width=4, anchor=tk.E)

    def _place_widgets(self):
        self._score_label.grid(row=0, column=0)
        self._score_display.grid(row=0, column=1)
