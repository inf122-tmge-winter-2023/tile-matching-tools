"""
    :module_name: view
    :module_summary: a class that is responsible for displaying the Tile Game
    :module_author: Matthew Isayan
"""

class View:
    def __init__(self, board):
        self.board = board
        self.score = 0