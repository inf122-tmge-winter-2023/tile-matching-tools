"""Tests for tile group"""

import pytest

from inf122_tmge.model import TileGroup
from inf122_tmge.model.exceptions import TileGroupPositionOccupiedError, \
                                         TileGroupDisbandedException
from inf122_tmge.core import TileBuilder

class TestTileGroup:
    def setup_method(self):
        self._builder = TileBuilder()
        self._group = TileGroup(self._builder.add_position(5, 5).construct())

    def test_default_group_has_size_one(self):
        assert self._group.size == 1

    def test_size_increases_when_tile_added_to_group(self):
        self._group.add_sibling_tile(
                self._builder.add_position(5, 5),
                0,
                -1
                )
        assert self._group.size == 2
    
    def test_cannot_add_tile_to_an_occupied_relative_position(self):
        with pytest.raises(TileGroupPositionOccupiedError):
            self._group.add_sibling_tile(
                    self._builder.add_position(5, 5),
                    0,
                    0
                    )
        assert self._group.size == 1
    
    def test_cannot_add_tile_when_group_is_disbanded(self):
        with pytest.raises(TileGroupDisbandedException):
            self._group.disband()
            self._group.add_sibling_tile(
                    self._builder.add_position(5, 5),
                    1,
                    1
                    )
