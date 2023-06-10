"""This module is used to start a PVP match of Othello."""

from OthelloCore import GameBoard
from OthelloGuiCore import GameIcons, displayGameboardHStyle, displayGameboardVStyle
from configs import WINDOW_SIZE, WINDOW_STYLE
import pygame, sys

def putDisk(gameBoard: GameBoard, x: int, y: int):
    """Maps the given coordinates to the corresponding position in the game board grid and places a disk at this position."""
    
    # Mapping the coordinates to the corresponding position in the game board grid.
    row, col = (y - gameBoard.diagonalMargin) // gameBoard.squareLength, (x - gameBoard.diagonalMargin) // gameBoard.squareLength
    
    # Clicked outside the board or on a position that is not a possible move.
    if not (0 <= row < gameBoard.row and 0 <= col < gameBoard.col and gameBoard.disks[row][col] == -1):
        return
    
    # Placing a disk at the clicked position.
    gameBoard.disks[row][col] = gameBoard.player
    gameBoard.captureDisks((row, col))
    gameBoard.updateCount()
    
    # Advancing the game to the next turn.
    gameBoard.player = 3 - gameBoard.player
    gameBoard.evaluatePossibleMoves()
    
    # if not gameBoard.possibleMoves:
    #     gameBoard.player = 3 - gameBoard.player
    #     gameBoard.evaluatePossibleMoves()
    #     gameBoard.updateCount()
    #     if not gameBoard.possibleMoves:
    #         gameBoard.player = 0 # Game over.

def startPvPMatch(asPlugin=False):
    """Start a match of Othello between two manual players."""
    
    gameBoard = GameBoard()
    icons = GameIcons()
    
    if not asPlugin:
        pygame.init()
    
    SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_SIZE
    
    if WINDOW_STYLE == 'H':
        displayGameboard = displayGameboardHStyle
    else:
        displayGameboard = displayGameboardVStyle
    
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Othello-PvpMatch')
    
    displayGameboard(screen, gameBoard, icons)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                px, py = pygame.mouse.get_pos()
                putDisk(gameBoard, px, py)
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if asPlugin:
                        return
                    
                    gameBoard = GameBoard()
            
            displayGameboard(screen, gameBoard, icons)
            pygame.display.update()

if __name__ == "__main__":
    startPvPMatch()
