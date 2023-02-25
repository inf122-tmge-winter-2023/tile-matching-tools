"""
    :module_name: view
    :module_summary: a class that is responsible for displaying the Tile Game
    :module_author: Matthew Isayan
"""
from copy import deepcopy
import tkinter

from ..model import GameBoard

class View:
    def __init__(self, game_board: GameBoard):
        self.game_board = deepcopy(game_board)
        self.score = 0
        # tile_width will need to be passed in as well as appearance
        self.tile_width = 30

        self._init_screen()
        self._draw_board()

    def launch_view(self):
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
    def _draw_tile(self, board_x, board_y, color):
        """Draws a singular tile with said board coordinates and color"""
        padding = 5
        tile_start_x = board_x * self.tile_width + padding
        tile_end_x = board_x * self.tile_width + padding + self.tile_width

        tile_start_y = board_y * self.tile_width + padding
        tile_end_y = board_y * self.tile_width + padding + self.tile_width

        self.board_canvas.create_rectangle(tile_start_x, tile_start_y, tile_end_x, tile_end_y, fill=color, outline='gray', width=2)

    def _draw_board(self):
        """Draws the entire board"""
        for i in range(self.game_board.num_cols):
            for j in range(self.game_board.num_rows):
                self._draw_tile(i, j, self.game_board.board[i][j].color) # #D3D3D3 is light gray

    def _set_board(self, board: GameBoard):
        self.game_board = deepcopy(board)

    def update_board_view(self, updated_board:GameBoard):
        for i in range(self.game_board.num_cols):
            for j in range(self.game_board.num_rows):
                if self.game_board.board[i][j].color != updated_board.board[i][j].color:
                    # if the tile color has changed, redraw it
                    self._draw_tile(i, j, updated_board.board[i][j].color)
                    
        self._set_board(updated_board)

        
