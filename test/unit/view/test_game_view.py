"""Tests for game view"""

import tkinter as tk
import random
from unittest.mock import Mock

import pytest

from tilematch_tools.core import GameState, BoardFactory, TileBuilder
from tilematch_tools.model import Scoring, GameBoard, MovementRule, Tile, TileColor, MatchCondition
from tilematch_tools.view import GameView, GameEvent, MouseEvent

@pytest.fixture
def simple_game_state():
    return GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )

@pytest.mark.integration
def test_simple_game_view(simple_game_state):
    root = tk.Tk()
    game_view = GameView(root, simple_game_state)
    game_view.pack()
    root.mainloop()

@pytest.fixture
def move_rule_up():
    class MoveUp(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x, tile_to_move.position.y + 1)
            board.place_tile(tile_to_move)

    return MoveUp()

@pytest.fixture
def move_rule_down():
    class MoveDown(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x, tile_to_move.position.y - 1)
            board.place_tile(tile_to_move)
    
    return MoveDown()

@pytest.fixture
def move_rule_left():
    class MoveLeft(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x - 1, tile_to_move.position.y)
            board.place_tile(tile_to_move)

    return MoveLeft()

@pytest.fixture
def move_rule_right():
    class MoveRight(MovementRule):
        def apply(self, board: GameBoard, tile_to_move: Tile) -> None:
            tile_to_move.position = (tile_to_move.position.x + 1, tile_to_move.position.y)
            board.place_tile(tile_to_move)
    
    return MoveRight()

@pytest.mark.integration
def test_game_view_update_cycle(simple_game_state, move_rule_up, move_rule_down, move_rule_left, move_rule_right):
    moving_tile = TileBuilder() \
            .add_position(random.randint(1, simple_game_state.board.num_cols), random.randint(1, simple_game_state.board.num_rows)) \
            .add_color(random.choice(list(TileColor))) \
            .construct()
    simple_game_state.board.place_tile(moving_tile)


    root = tk.Tk()
    game_view = GameView(root, simple_game_state)
    game_view.pack()

    class MoveUp(GameEvent):
        def __call__(self, event):
            move_rule_up.move(self.listener.board, moving_tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))
 
    class MoveDown(GameEvent):
        def __call__(self, event):
            move_rule_down.move(self.listener.board, moving_tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))

    class MoveLeft(GameEvent):
        def __call__(self, event):
            move_rule_left.move(self.listener.board, moving_tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))

    class MoveRight(GameEvent):
        def __call__(self, event):
            move_rule_right.move(self.listener.board, moving_tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))   
   
    game_view.bind_key('<KeyRelease-w>', MoveUp(simple_game_state))
    game_view.bind_key('<KeyRelease-s>', MoveDown(simple_game_state))
    game_view.bind_key('<KeyRelease-a>', MoveLeft(simple_game_state))
    game_view.bind_key('<KeyRelease-d>', MoveRight(simple_game_state))

    def update():
        game_view.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

@pytest.mark.integration
def test_independent_game_view_bindings(move_rule_up, move_rule_down, move_rule_left, move_rule_right):
    gs1 = GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )
    gs2 = GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )
    moving_tile1 = TileBuilder() \
            .add_position(random.randint(1, gs1.board.num_cols), random.randint(1, gs1.board.num_rows)) \
            .add_color(random.choice(list(TileColor))) \
            .construct()
    moving_tile2 = TileBuilder() \
            .add_position(random.randint(1, gs2.board.num_cols), random.randint(1, gs2.board.num_rows)) \
            .add_color(random.choice(list(TileColor))) \
            .construct()

    gs1.board.place_tile(moving_tile1)
    gs2.board.place_tile(moving_tile2)


    root = tk.Tk()
    gv1 = GameView(root, gs1)
    gv2 = GameView(root, gs2)
    gv1.grid(row=0, column=0)
    gv2.grid(row=0, column=1)
    
    class MoveUp(GameEvent):
        def __init__(self, listener, tile):
            super().__init__(listener)
            self.tile = tile

        def __call__(self, event):
            move_rule_up.move(self.listener.board, self.tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))
 
    class MoveDown(GameEvent):
        def __init__(self, listener, tile):
            super().__init__(listener)
            self.tile = tile

        def __call__(self, event):
            move_rule_down.move(self.listener.board, self.tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))

    class MoveLeft(GameEvent):
        def __init__(self, listener, tile):
            super().__init__(listener)
            self.tile = tile

        def __call__(self, event):
            move_rule_left.move(self.listener.board, self.tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))

    class MoveRight(GameEvent):
        def __init__(self, listener, tile):
            super().__init__(listener)
            self.tile = tile

        def __call__(self, event):
            move_rule_right.move(self.listener.board, self.tile)
            self.listener.adjust_score(MatchCondition.MatchFound(random.randint(5, 10), []))   
    

    gv1.bind_key('<KeyRelease-w>', MoveUp(gs1, moving_tile1))
    gv1.bind_key('<KeyRelease-s>', MoveDown(gs1, moving_tile1))
    gv1.bind_key('<KeyRelease-a>', MoveLeft(gs1, moving_tile1))
    gv1.bind_key('<KeyRelease-d>', MoveRight(gs1, moving_tile1))

    gv2.bind_key('<KeyRelease-i>', MoveUp(gs2, moving_tile2))
    gv2.bind_key('<KeyRelease-k>', MoveDown(gs2, moving_tile2))
    gv2.bind_key('<KeyRelease-j>', MoveLeft(gs2, moving_tile2))
    gv2.bind_key('<KeyRelease-l>', MoveRight(gs2, moving_tile2))

    def update():
        gv1.update()
        gv2.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

@pytest.mark.integration
def test_mouse_click_events(simple_game_state):

    root = tk.Tk()
    game_view = GameView(root, simple_game_state)
    game_view.pack()

    class ClickDetector(MouseEvent):
        def __init__(self, listener, board_view):
            super().__init__(listener, board_view)
            self.board_display = board_view

        def __call__(self, event):
            clicked_on = super().__call__(event)
            new_tile = TileBuilder() \
                    .add_position(*clicked_on) \
                    .add_color(random.choice(list(TileColor))) \
                    .construct()
            self.listener.board.place_tile(new_tile)

    game_view.bind_click('<Button-1>', ClickDetector(simple_game_state, game_view.board_view))
    
    def update():
        game_view.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

@pytest.mark.integration
def test_independent_mouse_click_events():
    
    gs1 = GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )
    gs2 = GameState(
        BoardFactory.create_board(GameBoard, 10, 24),
        Scoring()
    )


    root = tk.Tk()
    gv1 = GameView(root, gs1)
    gv2 = GameView(root, gs2)
    gv1.grid(row=0, column=0)
    gv2.grid(row=0, column=1)


    class ClickDetector(MouseEvent):
        def __init__(self, listener, board_view):
            super().__init__(listener, board_view)
            self.board_display = board_view

        def __call__(self, event):
            clicked_on = super().__call__(event)
            new_tile = TileBuilder() \
                    .add_position(*clicked_on) \
                    .add_color(random.choice(list(TileColor))) \
                    .construct()
            self.listener.board.place_tile(new_tile)

    gv1.bind_click('<Button-1>', ClickDetector(gs1, gv1.board_view))
    gv2.bind_click('<Button-1>', ClickDetector(gs2, gv2.board_view))
    
    def update():
        gv1.update()
        gv2.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()

@pytest.mark.integration
def test_board_blocked_by_gameover_screen_when_game_ended(simple_game_state):
    root = tk.Tk()
    game_view = GameView(root, simple_game_state)
    game_view.pack()

    class EndGame(GameEvent):
        def __call__(self, event):
            self.listener.gameover = Mock(return_value=True)

    game_view.bind_key('<KeyRelease-q>', EndGame(simple_game_state))

    
    def update():
        game_view.update()
        root.after(100, update)

    root.after(100, update)
    root.mainloop()


