"""
    :module_name: game_event
    :module_summary: interface for tilmatching game events
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import tkinter as tk


from ..core import GameState

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
