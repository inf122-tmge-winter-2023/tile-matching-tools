"""event_manager Module
"""

import queue

from ..core.game_state import GameState


class EventManager:
    """EventManager Class"""
    def __init__(self):
        self._game_state_queue = queue.Queue()
        self._key_events = queue.Queue()
        self._mouse_events = queue.Queue()

    def put_mouse_event(self, event):
        self._mouse_events.put(event)
    
    def put_key_event(self, event):
        self._key_events.put(event)
    
    def put_game_state(self, game_state: GameState):
        self._game_state_queue.put(game_state)

    def get_mouse_event(self):
        """Gets mouse event

        Returns:
            tkitner.Event: first mouse_event in queue

        Raises:
            queue.Empty if no events
        """
        return self._mouse_events.get_nowait()
    
    def get_key_event(self):
        """Gets key event

        Returns:
            tkitner.Event: first mouse_event in queue

        Raises:
            queue.Empty if no events
        """
        return self._key_events.get_nowait()
    
    def get_game_state(self) -> GameState:
        """_summary_

        Returns:
            game_board : returns updated_board
        
        Warning:
            Blocks thread
        """
        return self._game_state_queue.get()
    
