"""Test for scoring class"""

import pytest

from inf122_tmge.model.score import Scoring
from inf122_tmge.model.match import MatchCondition

@pytest.fixture
def simple_match():
    class SimpleMatch(MatchCondition):
        def __init__(self):
            super().__init__((1, 0), 4)

        def check_match(self, board, start_x, start_y):
            return True
    
    return SimpleMatch()

@pytest.fixture
def simple_score():
    class SimpleScore(Scoring):
        def award_for_match(self, match):
            super().award_for_match(match)

    return SimpleScore()

def test_scores_must_implement_scoring_interface():
    class SomeScore(Scoring):
        def i_dont_implement_the_scoring_interface(self):
            pass

    with pytest.raises(TypeError):
        SomeScore()

class TestScoring:
    def test_score_is_initialized_to_zero(self, simple_score):
        assert simple_score.score == 0
        assert simple_score.multiplier == 1

    def test_award_on_match_adds_points_to_score(self, simple_score, simple_match):
        simple_score.award_for_match(simple_match)
        assert simple_score.score == 4
        assert simple_score.multiplier == 1
