"""This module contains the core logic of the Othello game that is used by other modules."""

from configs import SQUARE_LENGTH, ROW_COL, DIAGONAL_MARGIN

class GameBoard:
    """A class that represents the game board."""
    
    def __init__(self):
        self.squareLength = SQUARE_LENGTH
        """The length of each square on the game board."""
        
        self.row = self.col = ROW_COL # The number of rows and columns on the game board.
        
        self.diagonalMargin = DIAGONAL_MARGIN
        """The margin between the board and the top left of the game window."""
        
        self.player = 1
        """The current plyer turn. `1` for black, `2` for white. Black always starts first."""
        
        self.disks: list[list[int]] = [[0] * self.col for _ in range(self.row)]
        """A 2D array that represents the game board."""
        
        # Initialize the board with 4 disks in the center of the board (2 black and 2 white).
        self.disks[self.row // 2 - 1][self.col // 2] = self.disks[self.row // 2][self.col // 2 - 1] = 1
        self.disks[self.row // 2 - 1][self.col // 2 - 1] = self.disks[self.row // 2][self.col // 2] = 2
        
        self.blackCount = 2
        """The number of black disks on the board."""
        
        self.whiteCount = 2
        """The number of white disks on the board."""
        
        self._legelSteps = ((0, 1), (0,  -1), (1,  0), (-1, 0),
                            (1, 1), (-1, -1), (1, -1), (-1, 1))
        """The eight directions in which a player can move a disk."""
        
        self.possibleMoves: set[tuple[int, int]] = set()
        """A list of possible moves for the current player."""
        
        self.evaluatePossibleMoves()

    def evaluatePossibleMoves(self):
        """Update the list of possible moves for the current player."""
        
        # Resetting the list of possible moves.
        self.possibleMoves = set()
        
        # Clearing any empty positions marked as possible moves (-1) that have been found in a previous call to this function.
        for row_i in range(self.row):
            for col_i in range(self.col):
                if self.disks[row_i][col_i] == -1:
                    self.disks[row_i][col_i] = 0
        
        opponent = 3 - self.player # (3 - 1 = 2), (3 - 2 = 1)
        
        # Checking for possible moves that the current player can make by iterating over each
        # position on the board and checking if it contains a dicks belonging to the current player.
        # If a dick is found, then we check in all eight directions to see if there are any opposing
        # dicks that can be captured by moving in that direction. If a sequence of opposing dicks is
        # found, and the next position in that direction is empty, then that empty position is considered
        # a valid move and added to the list of available positions.
        for row_i in range(self.row):
            for col_i in range(self.col):
                if self.disks[row_i][col_i] == self.player:
                    for rowStep, colStep in self._legelSteps:
                        row, col = row_i + rowStep, col_i + colStep
                        if 0 <= row < self.row and 0 <= col < self.col and self.disks[row][col] == opponent:
                            while 0 <= row < self.row and 0 <= col < self.col and self.disks[row][col] == opponent:
                                row += rowStep
                                col += colStep
                            if 0 <= row < self.row and 0 <= col < self.col and self.disks[row][col] == 0:
                                self.disks[row][col] = -1 # Marking the empty position as a possible move.
                                self.possibleMoves.add((row, col))

    def captureDisks(self, pos: tuple[int, int]):
        """Capture (flip) the disks of the opponent that are in the line of sight of the disk at the given position."""
        
        opponent = 3 - self.player
        for rowStep, colStep in self._legelSteps:
            row, col = pos[0] + rowStep, pos[1] + colStep
            if 0 <= row < self.row and 0 <= col < self.col and self.disks[row][col] == opponent:
                while 0 <= row < self.row and 0 <= col < self.col and self.disks[row][col] == opponent:
                    row += rowStep
                    col += colStep
                
                # After the while loop, if the current position contains a disk belonging to the current player, then capture the opponent's disks.
                # Else if the position has no disks, then do not capture the opponent's disks.
                if 0 <= row < self.row and 0 <= col < self.col and self.disks[row][col] == self.player:
                    while (row, col) != (pos[0], pos[1]):
                        row -= rowStep
                        col -= colStep
                        self.disks[row][col] = self.player

    def updateCount(self):
        """Update some of the GameBoard counters."""
        
        self.blackCount = self.whiteCount = 0
        
        for row in range(self.row):
            for col in range(self.col):
                if self.disks[row][col] == 1:
                    self.blackCount += 1
                
                elif self.disks[row][col] == 2:
                    self.whiteCount += 1

if __name__ == "__main__":
    print(GameBoard().possibleMoves)
