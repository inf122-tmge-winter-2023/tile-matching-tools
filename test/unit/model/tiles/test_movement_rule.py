"""Tests for movement rule"""

import pytest

from inf122_tmge.model.tiles import MovementRule

def test_cannot_instantiate_movement_rule():
    with pytest.raises(TypeError):
        m = MovementRule(-1, -1)

def test_movements_must_implement_exec_interface():
    class TestMovement(MovementRule):
        def i_dont_implement_exec(self):
            pass

    with pytest.raises(TypeError):
        m = TestMovement(-1, 1)
