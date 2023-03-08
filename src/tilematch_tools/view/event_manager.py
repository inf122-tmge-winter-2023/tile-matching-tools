"""event_manager Module
"""

import queue


class EventManager:
    """EventManager Class"""
    def __init__(self):
        self._board_queue = queue.Queue()
        self._score_queue = queue.Queue()
        self._key_events = queue.Queue()
        self._mouse_events = queue.Queue()

    def put_mouse_event(self, event):
        self._mouse_events.put(event)
    
    def put_key_event(self, event):
        self._key_events.put(event)
    
    def put_board(self, game_board):
        self._board_queue.put(game_board)
    
    def put_score(self, game_score):
        self._score_queue.put(game_score)

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
    
    def get_board(self):
        """_summary_

        Returns:
            game_board : returns updated_board
        
        Warning:
            Blocks thread
        """
        return self._board_queue.get()
    
    def get_score(self):
        """_summary_

        Returns:
            score : returns score
        
        Warning:
            Blocks thread
        """
        return self._score_queue.get()

