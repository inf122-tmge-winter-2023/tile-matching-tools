"""Tests for tile builder"""

from itertools import product

import pytest

from tilematch_tools.core import TileBuilder
from tilematch_tools.model.tiles import Tile, TileColor, TileShape
from tilematch_tools.model.exceptions import MissingTilePropertyException

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

    @pytest.mark.parametrize("x, y", [
            (x, y) for x in range(1, 6) for y in range(1, 6)
        ]
    )
    def test_default_styling_of_tile_when_not_specified(self, x, y):
        the_tile = self._builder.add_position(x, y).construct()
        assert the_tile.color == TileColor.RED
        assert the_tile.shape == TileShape.SQUARE

    @pytest.mark.parametrize("color, shape", product(TileColor, TileShape))
    def test_specified_styling_of_tile(self, color, shape):
        the_tile = self._builder \
                .add_position(1, 1) \
                .add_color(color) \
                .add_shape(shape) \
                .construct()

        assert the_tile.color == color
        assert the_tile.shape == shape

    def test_tile_border(self):
        the_tile = self._builder \
            .add_position(1, 1) \
            .add_border(TileColor.BLUE) \
            .construct()
        assert the_tile.border == TileColor.BLUE
