"""
    :module_name: view
    :module_summary: a class that is responsible for displaying the Tile Game
    :module_author: Matthew Isayan
"""
from copy import deepcopy
import math
import queue
from threading import Thread
import tkinter
import types
import typing

from ..model import GameBoard

class View:
    """
        A class that represents the view of the TMGE
    """
    def __init__(self, game_board: GameBoard):
        self._game_board = deepcopy(game_board)
        # tile_width will need to be passed in as well as appearance
        self._tile_width = 30

        self._init_screen()
        self._draw_board()
        self._board_queue = queue.Queue()
        self._score_queue = queue.Queue()
        self._key_events = queue.Queue()
        self._mouse_events = queue.Queue()
        self._quit = False

    def launch_view(self, func_name: types.FunctionType=None):
        """
            Launches window and a thread of func_name 500 ms later
            :arg func_name: Name of the function to run side by side View
            :arg type: FunctionType
            :returns: nothing
            :rtype: None
        """
        thread = None  # Initialize thread variable

        if func_name:
            thread = Thread(target=func_name)
            self._root.after(500, thread.start())

        def on_close():
            self._quit = True
            if thread is not None:
                thread.join()  # Wait for thread to finish
            self._root.destroy()

        # Close on exit
        self._root.protocol("WM_DELETE_WINDOW", on_close)

        while not self._quit:
            self.update_board_view(self._board_queue.get())
            self.update_score(self._score_queue.get())
            self._root.update()
 
    def _init_screen(self):
        """
            Initializes screen, main container and canvas for the board 
            :returns: nothing
            :rtype: None
        """
        # Initialize empty window
        self._root = tkinter.Tk()
        score_container_width = 200
        padding = 10
        screen_width = self._game_board.num_cols * self._tile_width \
              + score_container_width + padding
        screen_height = self._game_board.num_rows * self._tile_width + padding

        # Setting window size: Needs to be in this format '600x800'
        self._root.geometry(f"{screen_width}x{screen_height}")
        self._root.title('TMGE GUI')
        self._root.resizable(False, False)

        # Init main container
        self._main_container = tkinter.Frame(self._root)
        self._main_container.pack(side="left", fill="both")
        # Init canvas for board
        canvas_padding = 5
        canvas_width = screen_width + canvas_padding - score_container_width
        canvas_height = screen_height + canvas_padding
        self._board_canvas = tkinter.Canvas(self._main_container, \
                                            width=canvas_width, height=canvas_height)
        self._board_canvas.pack(side="left", fill="y")
        # Init container for score
        score_container = tkinter.Frame(self._main_container, width=score_container_width,\
                                         height=screen_height,padx=60)
        score_container.pack(side="left", fill="both")

        # Add label to display score
        score_label = tkinter.Label(score_container, text="Score", font=("Roboto", 16))
        score_label.pack(side="top")

        # Add label to display score number
        self._score_label = tkinter.Label(score_container, text="0", font=("Roboto", 14))
        self._score_label.pack(side="top")

    def _draw_tile(self, row: int, col: int, color: str):
        """
            Draws a singular tile on the board
            :arg row: Row number on the board (1-based)
            :arg col: Column number on the board (1-based)
            :arg color: color
            :arg type: int
            :arg type: int
            :arg type: color
            :returns: nothing
            :rtype: None
        """
        row = row - 1
        col = col - 1
        padding = 5
        tile_start_x = row * self._tile_width + padding
        tile_end_x = row * self._tile_width + padding + self._tile_width

        tile_start_y = col * self._tile_width + padding
        tile_end_y = col * self._tile_width + padding + self._tile_width

        self._board_canvas.create_rectangle(tile_start_x, tile_start_y, tile_end_x, \
                                             tile_end_y, fill=color, outline='gray', width=2)

    def _draw_board(self):
        """
            Draws the entire board using the draw_tile method
            :returns: nothing
            :rtype: None
        """
        for row in range(1, self._game_board.num_cols + 1):
            for col in range(1, self._game_board.num_rows + 1):
                self._draw_tile(row, col, self._game_board.tile_at(row, col).color)

    def _set_board(self, board: GameBoard):
        """
            Sets the board
            :arg board: Board model to set to view
            :arg type: GameBoard 
            :returns: nothing
            :rtype: None
        """
        self._game_board = deepcopy(board)

    def update_board_view(self, updated_board:GameBoard):
        """
            Updates the board view and sets the updated board
            :arg updated_board: Board model to update the view
            :arg type: GameBoard 
            :returns: nothing
            :rtype: None
        """
        for row in range(1, self._game_board.num_cols + 1):
            for col in range(1, self._game_board.num_rows + 1):
                if self._game_board.tile_at(row, col) != updated_board.tile_at(row, col):
                    self._draw_tile(row, col, updated_board.tile_at(row, col).color)

        self._set_board(updated_board)

    def update(self, updated_board: GameBoard, updated_score: int):
        self._board_queue.put(updated_board)
        self._score_queue.put(updated_score)

    def add_event_listener(self, event_name: str):
        """
            Add's an event listener to the view
            :arg event_name: The name of the event ex: KeyPress, KeyRelease, Key 
            :arg type: str 
            :returns: nothing
            :rtype: None
        """
        if("Key" in event_name):
            self._root.bind(f"<{event_name}>", self._event_handler)
        else:
            self._board_canvas.bind(f"<{event_name}>", self._event_handler)

    def _event_handler(self, event: tkinter.Event):
        """
            Add's an event listener to the view
            :arg event_name: The name of the event ex: KeyPress, KeyRelease, Key 
            :arg type: tkinter.Event 
            :returns: nothing
            :rtype: None
        """
        if(event.type ==  tkinter.EventType.ButtonRelease):
            self._mouse_events.put(self._map_mouse(event.x, event.y))
        else:
            self._key_events.put(event.char)

    @property
    def key_events(self) -> queue.Queue:
        """
            Getter for the events queue
            :returns:  Returns the queue of events storing the latest event at the first position
            :rtype: queue.Queue
        """
        return self._key_events
    @property
    def mouse_events(self) -> queue.Queue:
        """
            Getter for the events queue
            :returns:  Returns the queue of events storing the latest event at the first position
            :rtype: queue.Queue
        """
        return self._mouse_events
    
    def update_score(self, score: int):
        """
            Updates the Score label
            :returns:  Returns the queue of events storing the latest event at the first position
            :rtype: queue.Queue
        """
        self._score_label.config(text=f"{score}")

    # TODO Implement via constants
    def _map_mouse(self, x_coord: int, y_coord: int) -> typing.Tuple:
        """Maps Event Coordinates to Board Coordinates"""

        row = math.floor(((x_coord - 5) / 30) + 1)
        col =  math.floor(((y_coord - 5) / 30) + 1)
        return (row, col)
    
    @property
    def quit(self):
        return self._quit