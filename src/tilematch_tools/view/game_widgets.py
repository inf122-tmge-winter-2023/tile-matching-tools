"""
    :module_name: game_widgets
    :module_summary: abstract classes representing generalized game widgets
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import tkinter as tk
import tkinter.font as tkFont


class GameWidget(tk.Frame):
    """
        A base widget class for tilematching games
    """

    def __init__(self, parent, **options):
        super().__init__(parent, **options)
        self.create_widgets()
        self.place_widgets()

    def update(self):
        """
            Describes how the widget should update itself
        """
        raise NotImplementedError(f'No implementation for {self.update}')


    def create_widgets(self):
        """
            A place to initialize any necessary internal widgets
        """
        raise NotImplementedError(f'No implementation for {self.create_widgets}')

    def place_widgets(self):
        """
            A place to organize internal widgets into self
        """
        raise NotImplementedError(f'No implementation for {self.place_widgets}')

class GameInfo(GameWidget):
    """
        A base widget for displaying key: value game information
    """

    def __init__(self, parent, **options):
        super().__init__(parent, **options)
        
    @property
    def font(self):
        """
            Font to use in display
        """
        return tkFont.Font(family='Helvetica', size=16)

    @property
    def watching(self):
        """
            A getter for the value this widget is watching for changes
        """
        raise NotImplementedError(f'No implementation for {self.watching.fget}')

    @property
    def showing(self):
        """
            A getter for the value ths widget is currently displaying
        """
        raise NotImplementedError(f'No implementation for {self.showing.fget}')

   
