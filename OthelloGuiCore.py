from OthelloCore import GameBoard
from configs import WINDOW_SIZE, ICON_SIZE, COLOR_STYLE
from pygame import image, draw, font
from os import path
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    
    return path.join(base_path, relative_path)

class GameIcons:
    def __init__(self):
        styleDir = resource_path("iconsDarkStyle1") if COLOR_STYLE == (1,1) else resource_path("iconsDarkStyle2") if COLOR_STYLE == (1,2) \
             else resource_path("iconsLightStyle1") # if style == (2,1) else "iconsLightStyle2"
        
        self.size = ICON_SIZE
        self.background = image.load(path.join(styleDir, "background.png"))
        self.blackDisk = image.load(path.join(styleDir, "black.png"))
        self.whiteDisk = image.load(path.join(styleDir, "white.png"))
        self.possibleMoveDisk = image.load(path.join(styleDir, "available.png"))
        self.empty = image.load(path.join(styleDir, "blank.png"))
    
    def getDiskIconByValue(self, player: int):
        """Return the icon of the given player."""
        
        if player == 1:
            return self.blackDisk
        elif player == 2:
            return self.whiteDisk
        elif player == -1:
            return self.possibleMoveDisk
        return self.empty


def displayGameboardHStyle(screen, gameBoard: GameBoard, icons: GameIcons):
    """Display the gameboard on the given screen."""

    # Drawing the gameboard background.
    screen.blit(icons.background, (0, 0))

    # Drawing the gameboard grid. `+ 1` is for the right and bottom borders.
    for row in range(gameBoard.row + 1):
        for col in range(gameBoard.col + 1):
            draw.line(screen, (0, 0, 0),
                      (gameBoard.diagonalMargin + row * gameBoard.squareLength, gameBoard.diagonalMargin),
                      (gameBoard.diagonalMargin + row * gameBoard.squareLength, gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength))

            draw.line(screen, (0, 0, 0),
                      (gameBoard.diagonalMargin, gameBoard.diagonalMargin + col * gameBoard.squareLength),
                      (gameBoard.diagonalMargin + gameBoard.row * gameBoard.squareLength, gameBoard.diagonalMargin + col * gameBoard.squareLength))

    # Drawing the disks.
    imageMargin = gameBoard.diagonalMargin + gameBoard.squareLength // 2 - icons.size // 2
    for row in range(gameBoard.row):
        for col in range(gameBoard.col):
            screen.blit(icons.getDiskIconByValue(gameBoard.disks[row][col]), (col * gameBoard.squareLength + imageMargin, row * gameBoard.squareLength + imageMargin))

    # Drawing the players icons.
    playerIconPosX = gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength + gameBoard.squareLength // 2
    BlackIconPosY = playerIconPosX // 2 - icons.size * 1.5
    WhiteIconPosY = playerIconPosX // 2 - icons.size * 0.25

    if gameBoard.player == 1:
        screen.blit(icons.blackDisk, (playerIconPosX, BlackIconPosY))
        screen.blit(icons.possibleMoveDisk, (playerIconPosX, WhiteIconPosY))
    else:
        screen.blit(icons.possibleMoveDisk, (playerIconPosX, BlackIconPosY))
        screen.blit(icons.whiteDisk, (playerIconPosX, WhiteIconPosY))

    # Drawing the disk counters of the players.
    fontObj = font.Font(None, icons.size)

    # The black player.
    textSurfaceObj = fontObj.render(str(gameBoard.blackCount), True, (0, 0, 0))
    textRectangleObj = textSurfaceObj.get_rect()
    textRectangleObj.center = (playerIconPosX + icons.size * 2, int(BlackIconPosY + icons.size // 2))
    screen.blit(textSurfaceObj, textRectangleObj)

    # The white player.
    textSurfaceObj = fontObj.render(str(gameBoard.whiteCount), True, (0, 0, 0))
    textRectangleObj = textSurfaceObj.get_rect()
    textRectangleObj.center = (playerIconPosX + icons.size * 2, int(WhiteIconPosY + icons.size // 2))
    screen.blit(textSurfaceObj, textRectangleObj)

    # Printing Game Over if there is no possible moves for both players.
    if not gameBoard.possibleMoves:
        msg = "Game Over."
        textSurfaceObj = fontObj.render(msg, True, (100, 20, 40))
        textRectangleObj = textSurfaceObj.get_rect()
        textRectangleObj.center = (playerIconPosX + icons.size * 2, int(WhiteIconPosY + icons.size * 2))
        screen.blit(textSurfaceObj, textRectangleObj)

        msg = "Black wins!" if gameBoard.blackCount > gameBoard.whiteCount else "White wins!" if gameBoard.blackCount < gameBoard.whiteCount else "Tie!"
        textSurfaceObj = fontObj.render(msg, True, (20, 100, 40))
        textRectangleObj = textSurfaceObj.get_rect()
        textRectangleObj.center = (playerIconPosX + icons.size * 2, int(WhiteIconPosY + icons.size * 3))
        screen.blit(textSurfaceObj, textRectangleObj)

        msg = "Press the 'Space' key to start a new game."
        textSurfaceObj = fontObj.render(msg, True, (0, 0, 0))
        textRectangleObj = textSurfaceObj.get_rect()
        textRectangleObj.center = textRectangleObj.bottomleft = (gameBoard.diagonalMargin, gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength + icons.size * 4 // 3)
        screen.blit(textSurfaceObj, textRectangleObj)

        
   # Mypart
def displayGameboardVStyle(screen, gameBoard: GameBoard, icons: GameIcons):
    """Display the gameboard on the given screen."""

    # Drawing the gameboard background.
    screen.blit(icons.background, (0, 0))

    extraMargin = 13

    # Drawing the gameboard grid. `+ 1` is for the right and bottom borders.
    for row in range(gameBoard.row + 1):
        for col in range(gameBoard.col + 1):
            draw.line(screen, (0, 0, 0),
                      (gameBoard.diagonalMargin + row * gameBoard.squareLength, gameBoard.diagonalMargin + extraMargin),
                      (gameBoard.diagonalMargin + row * gameBoard.squareLength, gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength + extraMargin))

            draw.line(screen, (0, 0, 0),
                      (gameBoard.diagonalMargin, gameBoard.diagonalMargin + col * gameBoard.squareLength + extraMargin),
                      (gameBoard.diagonalMargin + gameBoard.row * gameBoard.squareLength, gameBoard.diagonalMargin + col * gameBoard.squareLength + extraMargin))

    # Drawing the disks.
    imageMargin = gameBoard.diagonalMargin + gameBoard.squareLength // 2 - icons.size // 2
    for row in range(gameBoard.row):
        for col in range(gameBoard.col):
            screen.blit(icons.getDiskIconByValue(gameBoard.disks[row][col]), (col * gameBoard.squareLength + imageMargin, row * gameBoard.squareLength + imageMargin + extraMargin))

    BlackIconPosX = gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength // 8
    WhiteIconPosX = gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength * 5 // 8
    PlayerIconPosY = gameBoard.diagonalMargin // 2 - icons.size // 2 + extraMargin // 2

    # Drawing the players icons.
    if gameBoard.player == 1:
        screen.blit(icons.blackDisk, (BlackIconPosX, PlayerIconPosY))
        screen.blit(icons.possibleMoveDisk, (WhiteIconPosX, PlayerIconPosY))
    else:
        screen.blit(icons.possibleMoveDisk, (BlackIconPosX, PlayerIconPosY))
        screen.blit(icons.whiteDisk, (WhiteIconPosX, PlayerIconPosY))

    # Drawing the disk counters of the players.
    fontObj = font.Font(None, icons.size)

    # The black player.
    textSurfaceObj = fontObj.render(str(gameBoard.blackCount), True, (0, 0, 0))
    textRectangleObj = textSurfaceObj.get_rect()
    textRectangleObj.center = (BlackIconPosX + icons.size * 2, int(PlayerIconPosY + icons.size // 2))
    screen.blit(textSurfaceObj, textRectangleObj)

    # The white player.
    textSurfaceObj = fontObj.render(str(gameBoard.whiteCount), True, (0, 0, 0))
    textRectangleObj = textSurfaceObj.get_rect()
    textRectangleObj.center = (WhiteIconPosX + icons.size * 2, int(PlayerIconPosY + icons.size // 2))
    screen.blit(textSurfaceObj, textRectangleObj)

    # Printing Game Over if there is no possible moves for both players.
    if not gameBoard.possibleMoves:
        fontObj = font.Font(None, icons.size * 3 // 4)

        msg = "Game Over. " + ("Black wins!" if gameBoard.blackCount > gameBoard.whiteCount else "White wins!" if gameBoard.blackCount < gameBoard.whiteCount else "Tie!")
        textSurfaceObj = fontObj.render(msg, True, (100, 20, 40))
        textRectangleObj = textSurfaceObj.get_rect()
        textRectangleObj.bottomleft = (gameBoard.diagonalMargin, gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength + icons.size + extraMargin - 5)
        screen.blit(textSurfaceObj, textRectangleObj)

        msg = "Press the 'Space' key to start a new game."
        textSurfaceObj = fontObj.render(msg, True, (0, 0, 0))
        textRectangleObj = textSurfaceObj.get_rect()
        textRectangleObj.bottomleft = (gameBoard.diagonalMargin, gameBoard.diagonalMargin + gameBoard.col * gameBoard.squareLength + icons.size * 5 // 3 + extraMargin - 5)
        screen.blit(textSurfaceObj, textRectangleObj)
