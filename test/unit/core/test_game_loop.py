"""Test for game_loop"""

import pytest
import time
from unittest.mock import Mock

from tilematch_tools.model import Scoring, GameBoard
from tilematch_tools.core import GameLoop, GameState, BoardFactory
from tilematch_tools.core.exceptions import GameEndedException
from tilematch_tools.view import View

@pytest.fixture
def simple_game_state():
    class SimpleScore(Scoring):
        def __init__(self):
            super().__init__()

        def award_for_match(self, match):
            self._points += 4

    return GameState(
            BoardFactory.create_board(GameBoard, 3, 3),
            SimpleScore()
            )


@pytest.fixture
def simple_game_loop(simple_game_state):
    class SimpleGameLoop(GameLoop):
        def handle_input(self):
            super().handle_input()

        def find_matches(self, match_conditions):
            super().find_matches(match_conditions)

        def clear_matches(self, matches_found):
            super().clear_matches(matches_found)

        def update_view(self):
            pass

        def gameover(self):
            super().gameover()

    return SimpleGameLoop(simple_game_state, 'View', 2_000_000_000)

def test_game_loop_subclass_implements_template():
    class InvalidGameLoop(GameLoop):
        def __init__(self):
            pass

    with pytest.raises(TypeError):
        InvalidGameLoop()

def test_delay_between_loop_interations(simple_game_loop):
    start = time.time_ns()
    simple_game_loop()
    end = time.time_ns()
    assert end - start > 1_000_000_000

def test_game_loop_is_callable(simple_game_loop):
    loop = simple_game_loop
    loop()

def test_game_loop_cannot_be_run_if_game_is_over(simple_game_loop):
    loop = simple_game_loop
    loop.gameover = Mock(return_value=True)
    with pytest.raises(GameEndedException):
        loop()
