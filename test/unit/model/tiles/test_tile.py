"""Tests for the TMGE tile class"""

from itertools import product

import pytest

from tilematch_tools.model import Tile, MovementRule
from tilematch_tools.model.tiles.tile_appearance import TileAppearance, TileShape, TileColor
from tilematch_tools.model.exceptions import MissingTilePropertyException, IllegalTileMovementException

@pytest.fixture
def simple_down_movement():
    class MoveDown(MovementRule):
        def exec(self, x, y):
            return (x + self._dx, y + self._dy)

    return MoveDown(0, -1)

@pytest.fixture
def frozen_tile():
    class FrozenTile(Tile):
        def __init__(self, **properties):
            super().__init__(**properties)
            self._movable = False

    return FrozenTile(**{'position': (2, 2)})

class TestTiles:
    test_positions = [
            (1, 0),
            (5, 3),
            (3, 5),
            (2, 2)
            ]
    test_styles = product(TileColor, TileShape)

    @pytest.mark.parametrize("x, y", test_positions)
    def test_tile_constructor_sets_position_and_style(self, x, y):
        the_tile = Tile(**{'position': (x, y)})
        assert hasattr(the_tile, '_position')
        assert hasattr(the_tile, '_appearance')

    @pytest.mark.parametrize("x, y", test_positions)
    def test_tile_position_getter(self, x, y):
        the_tile = Tile(**{'position': (x, y)})
        assert the_tile.position.x == x
        assert the_tile.position.y == y

    @pytest.mark.parametrize("x, y", test_positions)
    def test_tile_position_setter(self, x, y):
        the_tile = Tile(**{'position': (x, y)})
        
        the_tile.position = (x - 1, y + 1)
        assert the_tile.position.x != x
        assert the_tile.position.y != y

    @pytest.mark.parametrize("x, y", test_positions)
    def test_position_property_cannot_be_missing(self, x, y):
        with pytest.raises(MissingTilePropertyException):
            the_tile = Tile(**{'definitely not a position': (x, y)})

    @pytest.mark.parametrize("x, y", test_positions)
    def test_default_shape_and_color(self, x, y):
        the_tile = Tile(**{'position': (x, y)})

        assert the_tile.color == TileColor.RED
        assert the_tile.shape == TileShape.SQUARE

    @pytest.mark.parametrize("pos, style", product(test_positions, test_styles))
    def test_non_default_styles(self, pos, style):
        the_tile = Tile(**{'position': pos, 'color': style[0], 'shape': style[1]})

        assert the_tile.color == style[0]
        assert the_tile.shape == style[1]

    @pytest.mark.parametrize("x, y", test_positions)
    def test_movement_rule_updates_tiles_position(self, x, y, simple_down_movement):
        the_tile = Tile(**{'position': (x, y)})

        assert the_tile.position.x == x and the_tile.position.y == y
        the_tile.move(simple_down_movement)
        assert the_tile.position.x == x and the_tile.position.y == y -1

    def test_immovable_tile_cannot_move(self, frozen_tile, simple_down_movement):
        with pytest.raises(IllegalTileMovementException):
            the_tile = frozen_tile
            the_tile.move(simple_down_movement)

    @pytest.mark.parametrize("x, y", test_positions)
    def test_border_getter_setter(self, x, y):
        the_tile = Tile(**{'position': (x, y)})
        the_tile.border = "blue"
        assert the_tile.border == "blue"
