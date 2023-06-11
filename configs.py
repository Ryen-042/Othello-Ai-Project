"""Defines the constants used in the modules."""

DIAGONAL_MARGIN = 50
"""The diagonal margin between the left top of the window border and the gameboard grid."""

ICON_SIZE       = 50
"""The size of the disk icons in the gameboard."""

SQUARE_LENGTH   = 60
"""The length of a square cell in the gameboard."""

ROW_COL         = 8
"""The number of rows and columns in the gameboard."""

HSTYLE_WINDOW_WIDTH  = DIAGONAL_MARGIN * 2 + SQUARE_LENGTH * ROW_COL + (ICON_SIZE) * 4
HSTYLE_WINDOW_HEIGHT = DIAGONAL_MARGIN * 2 + SQUARE_LENGTH * ROW_COL + (ICON_SIZE)
VSTYLE_WINDOW_WIDTH  = DIAGONAL_MARGIN * 2 + SQUARE_LENGTH * ROW_COL
VSTYLE_WINDOW_HEIGHT = DIAGONAL_MARGIN * 2 + SQUARE_LENGTH * ROW_COL + (ICON_SIZE)


WINDOW_STYLE_OPTIONS = {"H": (HSTYLE_WINDOW_WIDTH, HSTYLE_WINDOW_HEIGHT), "V": (VSTYLE_WINDOW_WIDTH, VSTYLE_WINDOW_HEIGHT)}

# Change the one to select the window style.
WINDOW_STYLE = "V"

WINDOW_SIZE = WINDOW_STYLE_OPTIONS[WINDOW_STYLE]

# Change this to change the game window color style. Available options are (1, 1), (1, 2), (2, 1).
COLOR_STYLE = (1, 2) # [First number -> 1: Dark, 2: Light] | [Second number -> differnet colors].
