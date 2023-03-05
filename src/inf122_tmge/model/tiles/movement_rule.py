"""
    :module_name: movement_rule
    :module_summary: a class the controls how a tile is allowed to move
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

from abc import ABC, abstractmethod

class MovementRule(ABC):
    """
        Class that represents how a tile's position should adjust
    """

    def __init__(self, dx, dy):
        self._dx = dx
        self._dy = dy

    @abstractmethod
    def exec(self, x: int, y: int) -> (int, int):
        """
            Provide information required to apply this movement rule
            :arg x: current x position
            :arg y: current y position
            :arg type: int
            :arg type: int
            :returns: new position
            :rtype: (int, int)
        """
        pass
