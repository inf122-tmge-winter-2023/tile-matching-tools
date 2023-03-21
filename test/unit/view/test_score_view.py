"""Tests for score view"""

import tkinter as tk

import pytest

from tilematch_tools import MatchCondition, Scoring, ScoreView

@pytest.fixture
def simple_score():
    class MyScore(Scoring):
        def award_for_match(self, match):
            super().award_for_match(match)

@pytest.mark.integration
def test_simple_score_display(simple_score):
    root = tk.Tk()
    score_view = ScoreView(root, simple_score)
    score_view.pack()
    root.mainloop()

@pytest.mark.integration
def test_simple_score_update(simple_score):
    def add_score(event):
        simple_score.award_for_match(MatchCondition.MatchFound(10, []))

    def lose_score(event):
        simple_score.award_for_match(MatchCondition.MatchFound(-10, []))


    root = tk.Tk()
    score_view = ScoreView(root, simple_score)
    score_view.pack()
    score_view.bind_all('<KeyRelease-a>', add_score)
    score_view.bind_all('<KeyRelease-l>', lose_score)

    def update_score():
        score_view.update_score_display()
        score_view.after(100, update_score)

    score_view.after(100, update_score)
    root.mainloop()

