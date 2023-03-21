"""Tests for score view"""

import tkinter as tk

import pytest

from tilematch_tools import Scoring, ScoreView

@pytest.fixture
def simple_score():
    class MyScore(Scoring):
        def award_for_match(self, match):
            super().award_for_match(match)

@pytest.mark.integration
def simple_score_display(simple_score):
    root = tk.Tk()
    score_view = ScoreView(root, simple_score)
    score_view.pack()
