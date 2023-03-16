"""
    :module_name: view
    :module_summary: a class that is responsible for displaying the Tile Game
    :module_author: Matthew Isayan
"""
from copy import deepcopy
import math
import tkinter
import typing

from ..model.tiles.tile_appearance import TileColor

from ..model.tiles.tile import Tile

from ..core.game_state import GameState

from ..model import GameBoard
from .view_constants import ViewConstants
from .event_manager import EventManager

class View:
    """
        A class that represents the view of the TMGE
    """
    def __init__(self, game_state: GameState, root: tkinter.Tk):
        self._game_board = deepcopy(game_state.board)
        self._root = root
        ViewConstants.num_rows = self._game_board.num_rows
        ViewConstants.num_cols = self._game_board.num_cols

        self._event_manager = EventManager()
        self._init_screen()
        self._draw_board()

    def update_container(self):
        updated_game_state = self._event_manager.get_game_state()
        self._update_board_view(updated_game_state.board)
        self._update_score_view(updated_game_state.score)
        self._board_canvas.update()

    def update_game_state(self, updated_game_state: GameState):
        """Puts gamestate to queues for the main_loop() to read

        Args:
            updated_game_state (GameBoard): altered_board
        """
        self._event_manager.put_game_state(updated_game_state)

    def _init_screen(self):
        """
            Initializes screen, main container and canvas for the board 
            :returns: nothing
            :rtype: None
        """


        # Init main container
        self.main_container = tkinter.Frame(self._root)

        # Init canvas for board
        self._board_canvas = tkinter.Canvas(self.main_container, \
                                            width=ViewConstants.board_width(), \
                                            height=ViewConstants.board_height())
        self._board_canvas.pack(side="left", fill="y")

        # Init container for score
        score_container = tkinter.Frame(self.main_container, \
                                        width=ViewConstants.score_container_width, \
                                        height=ViewConstants.window_height(), \
                                        padx=ViewConstants.score_padding)
        score_container.pack(side="left", fill="y")

        # Add label to display score
        score_label = tkinter.Label(score_container, text="Score", font=("Roboto", 16))
        score_label.pack(side="top")

        # Add label to display score number
        self._score_label = tkinter.Label(score_container, text="0", font=("Roboto", 14))
        self._score_label.pack(side="top")

    def _draw_tile(self,tile: Tile):
        """
            Draws a singular tile on the board
            Use for initial board render
            :arg row: Row number on the board (1-based)
            :arg col: Column number on the board (1-based)
            :arg color: color
            :arg type: int
            :arg type: int
            :arg type: color
            :returns: nothing
            :rtype: None
        """
        x =  tile.position.x -1
        y = self._game_board.num_rows - tile.position.y 
        tile_start_x = x * ViewConstants.tile_size + ViewConstants.board_padding - 1.5
        tile_end_x = tile_start_x + ViewConstants.tile_size - 1.5

        tile_start_y = y *  ViewConstants.tile_size + ViewConstants.board_padding - 1.5
        tile_end_y = tile_start_y + ViewConstants.tile_size - 1.5
        return self._board_canvas.create_rectangle(tile_start_x, tile_start_y, tile_end_x, \
                                             tile_end_y, fill=tile.color, outline=tile.border, width=1)
    
    def _update_tile(self, tile : Tile):
        """Used to update tile on view after being drawn

        Args:
            tile (Tile): tile to update on view
        """
        self._board_canvas.itemconfig(self._tiles[tile.position.x-1][tile.position.y-1], fill=tile.color, outline=tile.border,width=1)
        if(tile.border != TileColor.GRAY):
            self._board_canvas.itemconfig(self._tiles[tile.position.x-1][tile.position.y-1], width=2)

        
    def _draw_board(self):
        """
            Draws the entire board using the draw_tile method
            :returns: nothing
            :rtype: None
        """
        self._tiles = []
        for x in range(1, self._game_board.num_cols + 1):
            tile_cols = []
            for y in range(1,self._game_board.num_rows + 1):
                tile_cols.append(self._draw_tile(self._game_board.tile_at(x, y)))
            self._tiles.append(tile_cols)
        
    def _set_board(self, board: GameBoard):
        """
            Sets the board
            :arg board: Board model to set to view
            :arg type: GameBoard 
            :returns: nothing
            :rtype: None
        """
        self._game_board = deepcopy(board)

    def _update_board_view(self, updated_board:GameBoard):
        """
            Updates the board view and sets the updated board
            :arg updated_board: Board model to update the view
            :arg type: GameBoard 
            :returns: nothing
            :rtype: None
        """
        for row in range(1, self._game_board.num_cols + 1):
            for col in range(1, self._game_board.num_rows + 1):
                old_tile = self._game_board.tile_at(row, col)
                updated_tile = updated_board.tile_at(row, col)
                if  old_tile != updated_tile or old_tile.border != updated_tile.border:
                    self._update_tile(updated_tile)
        self._set_board(updated_board)

    def add_event_listener(self, event_name: str):
        """
            Add's an event listener to the view
            :arg event_name: The name of the event ex: KeyPress, KeyRelease, Key 
            :arg type: str 
            :returns: nothing
            :rtype: None
        """
        if "Key" in event_name:
            self.main_container.bind_all(f"<{event_name}>", self._event_handler)
        else:
            self._board_canvas.bind(f"<{event_name}>", self._event_handler)

    def _event_handler(self, event: tkinter.Event):
        """
            Add's an event to the _event_manager
            :arg event_name: The name of the event ex: KeyPress, KeyRelease, Key 
            :arg type: tkinter.Event 
        """
        if event.type ==  tkinter.EventType.ButtonRelease:
            self._event_manager.put_mouse_event(self._map_mouse(event.x, event.y))
        else:
            self._event_manager.put_key_event(event.char)

    @property
    def key_event(self) -> str:
        """
            Returns the earliest key event 
            rtype: char
        """
        return self._event_manager.get_key_event()
    @property
    def mouse_event(self) -> typing.Tuple:
        """
            Returns the earliest mouse event
            rtype: (x,y)
        """
        return self._event_manager.get_mouse_event()

    def _update_score_view(self, score: int):
        """
            Updates the Score label
            :returns:  Returns the queue of events storing the latest event at the first position
            :rtype: queue.Queue
        """
        self._score_label.config(text=f"{score}")

    def _map_mouse(self, x_coord: int, y_coord: int) -> typing.Tuple:
        """Maps Event Coordinates to Board Coordinates"""

        # + 1 is for one-based
        x = math.floor(((x_coord - ViewConstants.window_padding) / ViewConstants.tile_size) + 1)
        y = self._game_board.num_rows - math.floor(((y_coord - ViewConstants.window_padding) / ViewConstants.tile_size) )
        return (x, y)
