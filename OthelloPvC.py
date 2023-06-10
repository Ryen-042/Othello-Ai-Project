from OthelloGuiCore import GameIcons, displayGameboardHStyle, displayGameboardVStyle
from OthelloAiCore import AiGameBoard, GameBoardNode, GameBoardTree
from configs import WINDOW_SIZE, WINDOW_STYLE
import pygame, sys

def startAiMatch(mode=1, searchDepthBlack=3, searchDepthWhite=3, asPlugin=False):
    """Starts a match between one manual and one AI player (`mode=1`) or two AI players (`mode=2`)."""
    
    gameBoard = AiGameBoard()
    icons = GameIcons()
    if not asPlugin:
        pygame.init()
    
    SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_SIZE
    
    if WINDOW_STYLE == 'H':
        displayGameboard = displayGameboardHStyle
    else:
        displayGameboard = displayGameboardVStyle
    
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Othello-AiMatch')
    
    node = GameBoardNode(gameBoard)
    gameBoardTree = GameBoardTree(node)
    gameBoardTree.expandTree()
    
    displayGameboard(screen, gameBoard, icons)
    pygame.display.update()
    
    pos = (-1, -1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                elif event.key == pygame.K_SPACE:
                    if asPlugin:
                        return
                    
                    gameBoard = AiGameBoard()
                    node = GameBoardNode(gameBoard)
                    gameBoardTree = GameBoardTree(node)
                    gameBoardTree.expandTree()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONUP and gameBoard.player == 1 and mode == 1:
                px, py = pygame.mouse.get_pos()
                pos = (py - gameBoard.diagonalMargin) // gameBoard.squareLength, (px - gameBoard.diagonalMargin) // gameBoard.squareLength
                break
        
        if mode == 2 or gameBoard.player == 2:
            # TODO: It appears that the black player is not playing optimally.
            # I think it selects the moves that minimizes its values.
            if gameBoard.player == 1:
                gameBoardTree.searchDepth = searchDepthBlack
            else:
                gameBoardTree.searchDepth = searchDepthWhite
            
            pos = gameBoardTree.getBestMove(gameBoard.player)
        
        if pos in gameBoard.possibleMoves:
            gameBoardTree.root = gameBoardTree.root.children[pos]
            gameBoard = gameBoardTree.root.gameBoard
            gameBoardTree.expandTree()
        
        displayGameboard(screen, gameBoard, icons)
        pygame.display.update()

if __name__ == "__main__":
    # startAiMatch("V")
    from os import chdir, path
    
    # Changing the current working directory to the directory of this file.
    chdir(path.dirname(path.abspath(__file__)))
    
    startAiMatch(2, 2, 3)
