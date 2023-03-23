


from abc import ABC
from dataclasses import dataclass
from collections.abc import Iterable
import logging
import tkinter as tk

from .exceptions import GameEndedException
from .game_factory import Game


LOGGER=logging.getLogger(__name__)



class GameEngine(ABC):
    REFRESH_LATENCY = 100

    def __init__(self, games: Iterable[Game]):
        self._root = tk.Tk()
        self._games = games
        self._active = []


    def run(self) -> None:
        """
            Executes game engine
        """
        for slot, game in enumerate(self._games):
            loop = game.loop(game.state, game.view(self._root, game.state), game.tick_speed)
            self._active.append(loop)
            loop.view.grid(row=0, column=slot)
        self._root.after(self.REFRESH_LATENCY, self.update_games)
        self._root.mainloop()



    def update_games(self) -> None:
        """
            Update all the games
        """

        for game in self._active:
            try:
                if not game.state.gameover():
                    game()
                    game.view.update()
            #TODO: find simpler mechanic to handle gameover
            except GameEndedException as err:
                LOGGER.error('%s', str(err))
                game.view.update()


        self._root.after(self.REFRESH_LATENCY, self.update_games)



