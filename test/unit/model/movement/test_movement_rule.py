"""Tests for movement rule"""

from unittest.mock import Mock
import pytest

from tilematch_tools.model.board import GameBoard
from tilematch_tools.model.tiles import Tile, NullTile
from tilematch_tools.model.movement import MovementRule

def test_cannot_instantiate_movement_rule():
    with pytest.raises(TypeError):
        m = MovementRule(-1, -1)

def test_movements_must_implement_apply_interface():
    class TestMovement(MovementRule):
        def i_dont_implement_apply(self):
            pass

    with pytest.raises(TypeError):
        m = TestMovement(-1, 1)

@pytest.fixture
def simple_down():
    class SimpleDown(MovementRule):
        def apply(self, board, tile):
            tile.position = (tile.position.x, tile.position.y - 1)
            board.place_tile(tile)

    return SimpleDown()

class TestMovementRule:
    def setup_method(self):
        self.board = GameBoard(3, 3)
        self.tile = Tile(**{'position': (2, 3)})

    def test_movement_rule_updates_tile_position(self, simple_down):
        simple_down.move(self.board, self.tile)
        assert self.tile.position.x == 2
        assert self.tile.position.y == 2
        assert self.board.tile_at(2, 2) is self.tile
        assert isinstance(self.board.tile_at(2, 3), NullTile)

    def test_movement_rule_is_repeateable(self, simple_down):
        simple_down.move(self.board, self.tile)
        simple_down.move(self.board, self.tile)
        assert self.tile.position.x == 2
        assert self.tile.position.y == 1
        assert self.board.tile_at(2, 1) is self.tile
        assert isinstance(self.board.tile_at(2, 2), NullTile)
        assert isinstance(self.board.tile_at(2, 3), NullTile)

    def test_movement_reverted_on_failure(self, simple_down):
        simple_down.move(self.board, self.tile)
        simple_down.move(self.board, self.tile)
        simple_down.move(self.board, self.tile) #Illegal, would fall beyond board, should be reverted
        assert self.tile.position.x == 2
        assert self.tile.position.y == 1
        assert self.board.tile_at(2, 1) is self.tile
        assert isinstance(self.board.tile_at(2, 2), NullTile)
        assert isinstance(self.board.tile_at(2, 3), NullTile)

    def test_callback_called_after_movement_applied(self, simple_down):
        simple_down._after = Mock()
        simple_down.move(self.board, self.tile, 1, 2, 3)
        simple_down._after.assert_called_once_with(1, 2, 3)
