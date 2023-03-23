from unittest.mock import Mock
import pytest
from tilematch_tools.core.board_factory import BoardFactory
from tilematch_tools.core.game_factory import Game, GameFactory
from tilematch_tools.core.game_state import GameState
from tilematch_tools.model.board.game_board import GameBoard
from tilematch_tools.model.tiles import Tile

def game_state(width, height):
    return GameState(BoardFactory.create_board(GameBoard, width, height), Mock())

@pytest.fixture
def my_game():
    class MyGame(Game):
        def setup(self):
            tile = Tile(**{'position': (3, 3)})
            self.state.board.place_tile(tile)
    return  MyGame(game_state(10, 10), Mock(), Mock(), 0)


class TestGame:
    def test_game_setup(self, my_game):
        my_game.setup()
        assert isinstance(my_game.state.board.tile_at(3, 3), Tile)



class TestGameFactory:
    def test_create_game(self):
        class TestGame(Game):
            def setup():
                return super().setup()

        class MyGameFactoryClass(GameFactory):
            @staticmethod
            def create_game() -> Game:
                return TestGame(game_state(10, 15), Mock(), Mock(), 200)

        test_game = MyGameFactoryClass.create_game()

        assert isinstance(test_game, TestGame)
        assert test_game.tick_speed == 200
        assert test_game.state.board.num_cols == 10
        assert test_game.state.board.num_rows == 15

