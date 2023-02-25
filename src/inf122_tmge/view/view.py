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
    def __init__(self, game_board: GameBoard):
        self.game_board = deepcopy(game_board)
        self.score = 0
        # tile_width will need to be passed in as well as appearance
        self.tile_width = 30

        self._init_screen()
        self._draw_board()
        self.events = queue.Queue()

    def launch_view(self, func_name: types.FunctionType=None):
        """Launches window and a thread of func_name 500 ms later"""
        if func_name:
            thread = Thread(target=func_name, daemon=True)
            self.root.after(500, thread.start())
        self.root.mainloop()
    
    def _init_screen(self):
        """Initializes screen, main container and canvas for the board """
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
    
    # Maybe pass in TileAppearance instead of color
    def _draw_tile(self, row, col, color):
        """
            Draws a singular tile with said board coordinates and color
            1-based indexing
        """
        row = row - 1
        col = col - 1 
        padding = 5
        tile_start_x = row * self.tile_width + padding
        tile_end_x = row * self.tile_width + padding + self.tile_width

        tile_start_y = col * self.tile_width + padding
        tile_end_y = col * self.tile_width + padding + self.tile_width

        self.board_canvas.create_rectangle(tile_start_x, tile_start_y, tile_end_x, tile_end_y, fill=color, outline='gray', width=2)

    def _draw_board(self):
        """Draws the entire board"""
        for row in range(1, self.game_board.num_cols + 1):
            for col in range(1, self.game_board.num_rows + 1):
                self._draw_tile(row, col, self.game_board.tile_at(row, col).color) # #D3D3D3 is light gray

    def _set_board(self, board: GameBoard):
        self.game_board = deepcopy(board)

    def update_board_view(self, updated_board:GameBoard):
        for row in range(1, self.game_board.num_cols + 1):
            for col in range(1, self.game_board.num_rows + 1):
                if self.game_board.tile_at(row, col).color != updated_board.tile_at(row, col).color:
                    # if the tile color has changed, redraw it
                    self._draw_tile(row, col, updated_board.tile_at(row, col).color)
                    
        self._set_board(updated_board)

    def add_keybind(self, event_name: str):
        self.root.bind('<%s>' % event_name, self.event_handler)

    def event_handler(self, event):
        self.events.put(event.char)
