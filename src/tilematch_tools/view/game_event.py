"""
    :module_name: game_event
    :module_summary: interface for tilmatching game events
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import tkinter as tk


from ..core import GameState
from .board_view import BoardView

class GameEvent:
    """
        Class represent an abstract game event
    """

    def __init__(self, listener: GameState):
        self._listener = listener

    @property
    def listener(self) -> GameState:
        """
            Reference to the object that knows how to respond to this event
            :returns: object awaiting this event
            :rtype: GameState
        """
        return self._listener

    def __call__(self, event: tk.Event) -> None:
        """
            Logic for responding to this event. AKA the "event handler"
            :arg event: event triggering this response
            :arg type: tk.Event
            :returns: nothing
            :rtype: None
        """
        pass

class MouseEvent(GameEvent):
    def __init__(self, listener: GameState, board_clicked_on: BoardView):
        super().__init__(listener)
        self.board_display = board_clicked_on

    def __call__(self, event):
        object_clicked_on = event.widget.find_closest(event.x, event.y)
        if object_clicked_on:
            for tile, drawing in self.board_display.tiles_map.items():
                if drawing == object_clicked_on[0]:
                    return tile
             
