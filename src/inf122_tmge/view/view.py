"""
    :module_name: view
    :module_summary: a class that is responsible for displaying the Tile Game
    :module_author: Matthew Isayan
"""
from copy import deepcopy
import queue
from threading import Thread
import tkinter
import types

from ..model import GameBoard

class View:
    """
        A class that represents the view of the TMGE
    """
    def __init__(self, game_board: GameBoard):
        self.game_board = deepcopy(game_board)
        self.score = 0
        # tile_width will need to be passed in as well as appearance
        self.tile_width = 30

        self.__init_screen()
        self.__draw_board()
        self._events = queue.Queue()

    def launch_view(self, func_name: types.FunctionType=None):
        """
            Launches window and a thread of func_name 500 ms later
            :arg func_name: Name of the function to run side by side View
            :arg type: FunctionType
            :returns: nothing
            :rtype: None
        """
        if func_name:
            thread = Thread(target=func_name, daemon=True)
            self.root.after(500, thread.start())
        self.root.mainloop()
    
    def __init_screen(self):
        """
            Initializes screen, main container and canvas for the board 
            :returns: nothing
            :rtype: None
        """
        # Initialize empty window
        self.root = tkinter.Tk()
        score_container_width = 150
        padding = 10
        screen_width = self.game_board.num_cols * self.tile_width + score_container_width + padding
        screen_height = self.game_board.num_rows * self.tile_width + padding

        # Setting window size: Needs to be in this format '600x800'
        self.root.geometry('%dx%d' % (screen_width, screen_height))
        self.root.title('TMGE GUI')

        # Init main container
        self.main_container = tkinter.Frame(self.root)
        self.main_container.pack(side="left", fill="both")
        
        # Init canvas for board
        canvas_padding = 5
        canvas_width = screen_width+canvas_padding
        canvas_height = screen_height+canvas_padding
        self.board_canvas = tkinter.Canvas(self.main_container, width=canvas_width, height=canvas_height)
        self.board_canvas.pack()    
    
    def __draw_tile(self, row: int, col: int, color: str):
        """
            Draws a singular tile on the board by converting the row + col to x + y coords of the view
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
        tile_start_x = row * self.tile_width + padding
        tile_end_x = row * self.tile_width + padding + self.tile_width

        tile_start_y = col * self.tile_width + padding
        tile_end_y = col * self.tile_width + padding + self.tile_width

        self.board_canvas.create_rectangle(tile_start_x, tile_start_y, tile_end_x, tile_end_y, fill=color, outline='gray', width=2)

    def __draw_board(self):
        """
            Draws the entire board using the draw_tile method
            :returns: nothing
            :rtype: None
        """
        for row in range(1, self.game_board.num_cols + 1):
            for col in range(1, self.game_board.num_rows + 1):
                self.__draw_tile(row, col, self.game_board.tile_at(row, col).color) # #D3D3D3 is light gray

    def __set_board(self, board: GameBoard):
        """
            Sets the board
            :arg board: Board model to set to view
            :arg type: GameBoard 
            :returns: nothing
            :rtype: None
        """
        self.game_board = deepcopy(board)

    def update_board_view(self, updated_board:GameBoard):
        """
            Updates the board view and sets the updated board
            :arg updated_board: Board model to update the view
            :arg type: GameBoard 
            :returns: nothing
            :rtype: None
        """
        for row in range(1, self.game_board.num_cols + 1):
            for col in range(1, self.game_board.num_rows + 1):
                if self.game_board.tile_at(row, col).color != updated_board.tile_at(row, col).color:
                    self.__draw_tile(row, col, updated_board.tile_at(row, col).color)
                    
        self.__set_board(updated_board)


    def add_event_listener(self, event_name: str):
        """
            Add's an event listener to the view
            :arg event_name: The name of the event ex: KeyPress, KeyRelease, Key 
            :arg type: str 
            :returns: nothing
            :rtype: None
        """
        self.root.bind('<%s>' % event_name, self.__event_handler)

    def __event_handler(self, event: tkinter.Event):
        """
            Add's an event listener to the view
            :arg event_name: The name of the event ex: KeyPress, KeyRelease, Key 
            :arg type: tkinter.Event 
            :returns: nothing
            :rtype: None
        """
        self._events.put(event.char)

    @property
    def events(self) -> queue.Queue:
        """
            Getter for the events queue
            :returns:  Returns the queue of events storing the latest event at the first position
            :rtype: queue.Queue
        """
        return self._events