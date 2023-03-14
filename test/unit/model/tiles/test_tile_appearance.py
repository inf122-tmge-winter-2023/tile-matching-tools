"""Tests for tile appearance"""

from itertools import product

import pytest

from tilematch_tools.model.tiles.tile_appearance import TileAppearance, TileShape, TileColor

@pytest.mark.parametrize("color, shape, border", product(TileColor, TileShape, TileColor))
def test_appearance_dataclass(color, shape, border):
    ta = TileAppearance(color, shape, border)
    assert ta.color == color
    assert ta.shape == shape
    assert ta.border == border
