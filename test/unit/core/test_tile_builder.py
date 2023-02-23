"""Tests for tile builder"""

import pytest

from inf122_tmge.core import TileBuilder
from inf122_tmge.model.tiles import Tile
from inf122_tmge.model.exceptions import MissingTilePropertyException

class TestTileBuilder:

    def setup_method(self):
        self._builder = TileBuilder()

    def test_default_tile_fails_with_no_position(self):
        with pytest.raises(MissingTilePropertyException):
            self._builder.construct()

    @pytest.mark.parametrize("x, y", [
            (x, y) for x in range(1, 6) for y in range(1, 6)
        ]
    )
    def test_default_tile_succeeds_with_required_position(self, x, y):
        the_tile = self._builder.add_position(x, y).construct()
        assert isinstance(the_tile, Tile)
        assert the_tile.position.x == x
        assert the_tile.position.y == y
