"""
    Module responsible for holding the constants for the view
"""

class ViewConstants:
    """
        Contains views constants

    """
    window_title = "TMGE GUI"
    tile_size = 30
    num_rows = 24
    num_cols = 10
    score_container_width = 200
    
    window_padding = 10
    board_padding = 5
    score_padding = 60
    
    @staticmethod
    def window_width() -> int:
        """Calculates Screen Width

        Returns:
            int: number of pixels in width
        """
        return  (ViewConstants.num_cols * ViewConstants.tile_size) \
              + ViewConstants.score_container_width + ViewConstants.window_padding

    @staticmethod
    def window_height() -> int:
        """Calculates Screen Height

        Returns:
            int: number of pixels in height
        """
        return (ViewConstants.num_rows * ViewConstants.tile_size) + ViewConstants.window_padding

    @staticmethod
    def board_width() -> int:
        """Calculates board width

        Returns:
            int: number of pixels in width
        """
        return ViewConstants.window_width() + ViewConstants.board_padding - ViewConstants.score_container_width
    
    @staticmethod
    def board_height() -> int:
        """Calculates board height

        Returns:
            int: number of pixels in height
        """
        return ViewConstants.window_height() + ViewConstants.board_padding