"""Tests for tile appearance"""

from itertools import product

import pytest

from tilematch_tools.model.tiles.tile_appearance import TileAppearance, TileShape, TileColor

@pytest.mark.parametrize("color, shape", product(TileColor, TileShape))
def test_appearance_dataclass(color, shape):
    ta = TileAppearance(color, shape)
    assert ta.color == color
    assert ta.shape == shape
