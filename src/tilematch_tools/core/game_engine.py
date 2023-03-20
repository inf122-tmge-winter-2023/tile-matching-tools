


from abc import ABC
from collections.abc import Iterable
import logging
from threading import Thread
from tilematch_tools.core.exceptions import GameEndedException

from tilematch_tools.core.game_loop import GameLoop

import tkinter as tk

LOGGER=logging.getLogger(__name__)

class GameEngine(ABC):
    def __init__(self, game_loops : Iterable[GameLoop]):
        self._game_loops = game_loops
        self._exit = False
        self._init_root()
        self._set_root()


    def run(self) -> None:
        """
            Executes game engine
            Runs on main thread
        """
        Thread(target=self._game_thread).start()
        while not self._exit:
            for game_loop in self._game_loops:
                if not game_loop.gameover():
                    # Render for games that are not over
                    game_loop.view.update_container()


    def _game_thread(self) -> None:
        """
            Runs on a worker thread
        """
        while not self._exit:
            for game_loop in self._game_loops:
                try:
                    if not game_loop.gameover():
                        # Iterate through game_loop for games that are not over
                        game_loop()
                except GameEndedException as err:
                    LOGGER.error('%s', str(err))
                    game_loop.await_delay()


    def _init_root(self):
        """
            Initializes Tkinter root
        """
        self._root = tk.Tk()
        self._root.protocol("WM_DELETE_WINDOW", self._on_exit)

    def _set_root(self):
        """
            Sets reference to root in views
        """
        for game_loop in self._game_loops:
            game_loop.view.set_root(self._root)
    
    def _on_exit(self):
        self._exit = True
