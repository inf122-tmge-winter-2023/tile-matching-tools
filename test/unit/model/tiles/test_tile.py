"""Tests for the TMGE tile class"""

import pytest

from inf122_tmge.model import Tile

class TestTiles:
    test_positions = [
            (1, 0),
            (5, 3),
            (3, 5),
            (2, 2)
            ]

    @pytest.mark.parametrize("x, y", test_positions)
    def test_tile_constructor_sets_position(self, x, y):
        the_tile = Tile(x, y)
        assert hasattr(the_tile, '_position')

    @pytest.mark.parametrize("x, y", test_positions)
    def test_tile_position_getter(self, x, y):
        the_tile = Tile(x, y)
        assert the_tile.position.x == x
        assert the_tile.position.y == y

    @pytest.mark.parametrize("x, y", test_positions)
    def test_tile_position_setter(self, x, y):
        the_tile = Tile(x, y)
        
        the_tile.position = (x - 1, y + 1)
        assert the_tile.position.x != x
        assert the_tile.position.y != y
