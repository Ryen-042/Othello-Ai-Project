from OthelloPvP import startPvPMatch
from OthelloPvC import startAiMatch
from configs import WINDOW_SIZE
import pygame
import ctypes
from os import path, chdir

chdir(path.dirname(__file__))

def EnableDPI_Awareness():
    """Enables `DPI Awareness` for the current thread to allow for accurate dimensions reporting."""
    
    # Creator note: behavior on later OSes is undefined, although when I run it on my Windows 10 machine, it seems to work with effects identical to SetProcessDpiAwareness(1)
    # Source: https://stackoverflow.com/questions/44398075/can-dpi-scaling-be-enabled-disabled-programmatically-on-a-per-session-basis/44422362#44422362
    # Source: https://stackoverflow.com/questions/32541475/win32api-is-not-giving-the-correct-coordinates-with-getcursorpos-in-python
    
    # Query DPI Awareness (Windows 10 and 8)
    awareness = ctypes.c_int()
    errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
    print("Current awareness value:", awareness.value, end=" -> ")
    
    if awareness.value != 0:
        return errorCode
    
    # Set DPI Awareness  (Windows 10 and 8). The argument is the awareness level. Check the link below for all valid values.
    # https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/ne-shellscalingapi-process_dpi_awareness
    # Further reading: https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2) # 1 seems to work fine
    
    # Printing the updated value.
    ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
    print(awareness.value)
    
    # Set DPI Awareness (Windows 7 and Vista). Also seems to work fine for windows 10.
    # success = ctypes.windll.user32.SetProcessDPIAware()
    return errorCode


def StartGame():
    """Starts the main game loop where the user can select the game mode and the Ai difficulty."""
    
    # Initialize pygame.
    pygame.init()

    # Defining the window size.
    SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_SIZE

    # Defining colors
    BG = (255, 255, 255)
    GREEN = (0, 200, 0)

    # Defining table row and column sizes.
    rowSize = 45
    colSize = 150
    RowPadding = 20
    colPadding = 30
    
    # Define table coordinates and sizes.
    xTablePos = 50
    yTablePos = 50
    tableWidth = colSize * 3
    tableHeight = rowSize * 4
    cellPadding = 10

    # Defining a font object.
    font = pygame.font.SysFont('Arial', 18)

    # Defining text surfaces.
    gameModeText = font.render('Game Mode', True, (0, 0, 0))
    pvpText = font.render('Player vs Player', True, (0, 0, 0))
    pvcText = font.render('Player vs AI', True, (0, 0, 0))
    cvcText = font.render('AI vs AI', True, (0, 0, 0))

    blackAiDiffText = font.render('Black Agent Difficulty', True, (0, 0, 0))
    whiteAiDiffText = font.render('White Agent Difficulty', True, (0, 0, 0))
    easyText = font.render('Easy', True, (0, 0, 0))
    normalText = font.render('Normal', True, (0, 0, 0))
    hardText = font.render('Hard', True, (0, 0, 0))
    vHardText = font.render('Very Hard', True, (0, 0, 0))
    beginText = font.render('Begin', True, (0, 0, 0))

    # Defining table cells.
    gameModeCell  = pygame.Rect(xTablePos, yTablePos, colSize, rowSize)
    pvpCell       = pygame.Rect(xTablePos, (yTablePos + rowSize + RowPadding), colSize, rowSize)
    pvcCell       = pygame.Rect(xTablePos, (yTablePos + rowSize * 2 + RowPadding * 2), colSize, rowSize)
    cvcCell       = pygame.Rect(xTablePos, (yTablePos + rowSize * 3 + RowPadding * 3), colSize, rowSize)

    aiOneDiffCell = pygame.Rect((xTablePos + colPadding + colSize), yTablePos, colSize, rowSize)
    easyCell      = pygame.Rect((xTablePos + colPadding + colSize), (yTablePos + rowSize + RowPadding), colSize, rowSize)
    normalCell    = pygame.Rect((xTablePos + colPadding + colSize), (yTablePos + rowSize * 2 + RowPadding * 2), colSize, rowSize)
    hardCell      = pygame.Rect((xTablePos + colPadding + colSize), (yTablePos + rowSize * 3 + RowPadding * 3), colSize, rowSize)
    vHardCell     = pygame.Rect((xTablePos + colPadding + colSize), (yTablePos + rowSize * 4 + RowPadding * 4), colSize, rowSize)

    aiTwoDiffCell = pygame.Rect((xTablePos + colPadding * 2 + colSize * 2), yTablePos, colSize, rowSize)
    easyCell2     = pygame.Rect((xTablePos + colPadding * 2 + colSize * 2), (yTablePos + rowSize + RowPadding), colSize, rowSize)
    normalCell2   = pygame.Rect((xTablePos + colPadding * 2 + colSize * 2), (yTablePos + rowSize * 2 + RowPadding * 2), colSize, rowSize)
    hardCell2     = pygame.Rect((xTablePos + colPadding * 2 + colSize * 2), (yTablePos + rowSize * 3 + RowPadding * 3), colSize, rowSize)
    vHardCell2    = pygame.Rect((xTablePos + colPadding * 2 + colSize * 2), (yTablePos + rowSize * 4 + RowPadding * 4), colSize, rowSize)

    # Two rects centered in the window, one for the background and another for the text.
    beginBgCell   = pygame.Rect(xTablePos, (yTablePos + rowSize * 6 + RowPadding * 5), tableWidth, rowSize)
    beginTextCell = beginText.get_rect(left=(xTablePos + tableWidth // 2 - 10), top=(yTablePos + rowSize * 6 + RowPadding * 5 + 10))

    terminate = False
    while not terminate:
        # Define done variable for the game loop
        gameMode = 1
        aiOneDiff = 0
        aiTwoDiff = 0
        done = False
        
        # Starting the game loop
        while not done:
            # Clearing the screen
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.fill(BG)
            
            # Handle events
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    terminate = True
                    done = True
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pvpCell.collidepoint(event.pos):
                        gameMode = 1
                        aiOneDiff = 0
                        aiTwoDiff = 0
                    
                    elif pvcCell.collidepoint(event.pos):
                        gameMode = 2
                        aiOneDiff = 1
                        aiTwoDiff = 0
                    
                    elif cvcCell.collidepoint(event.pos):
                        gameMode = 3
                        aiOneDiff = 1
                        aiTwoDiff = 1
                    
                    elif beginBgCell.collidepoint(event.pos):
                        pygame.draw.rect(screen, GREEN, beginBgCell, 0)
                        done = True
                    
                    elif gameMode in (2, 3):
                        # White
                        if easyCell.collidepoint(event.pos):
                            aiOneDiff = 1
                    
                        elif normalCell.collidepoint(event.pos):
                            aiOneDiff = 2
                        
                        elif hardCell.collidepoint(event.pos):
                            aiOneDiff = 3
                        
                        elif vHardCell.collidepoint(event.pos):
                            aiOneDiff = 4
                        
                        if gameMode == 3: # Black
                            if easyCell2.collidepoint(event.pos):
                                aiTwoDiff = 1
                            
                            elif normalCell2.collidepoint(event.pos):
                                aiTwoDiff = 2
                            
                            elif hardCell2.collidepoint(event.pos):
                                aiTwoDiff = 3
                            
                            elif vHardCell2.collidepoint(event.pos):
                                aiTwoDiff = 4

            # Drawing the table cells
            pygame.draw.rect(screen, (50, 200, 20), pvpCell, 1)
            pygame.draw.rect(screen, (50, 200, 20), pvcCell, 1)
            pygame.draw.rect(screen, (50, 200, 20), cvcCell, 1)
            pygame.draw.rect(screen, (50, 200, 20), beginBgCell, 1)
            
            # Highlighting the selected cells
            if gameMode == 1:
                pygame.draw.rect(screen, GREEN, pvpCell)
            elif gameMode == 2:
                pygame.draw.rect(screen, GREEN, pvcCell)
            elif gameMode == 3:
                pygame.draw.rect(screen, GREEN, cvcCell)
            
            if aiOneDiff:
                pygame.draw.rect(screen, (50, 200, 20), easyCell, 1)
                pygame.draw.rect(screen, (50, 200, 20), normalCell, 1)
                pygame.draw.rect(screen, (50, 200, 20), hardCell, 1)
                pygame.draw.rect(screen, (50, 200, 20), vHardCell, 1)
                
                if aiOneDiff == 1:
                    pygame.draw.rect(screen, GREEN, easyCell)
                elif aiOneDiff == 2:
                    pygame.draw.rect(screen, GREEN, normalCell)
                elif aiOneDiff == 3:
                    pygame.draw.rect(screen, GREEN, hardCell)
                elif aiOneDiff == 4:
                    pygame.draw.rect(screen, GREEN, vHardCell)
            
            if aiTwoDiff:
                pygame.draw.rect(screen, (50, 200, 20), easyCell2, 1)
                pygame.draw.rect(screen, (50, 200, 20), normalCell2, 1)
                pygame.draw.rect(screen, (50, 200, 20), hardCell2, 1)
                pygame.draw.rect(screen, (50, 200, 20), vHardCell2, 1)
                
                if aiTwoDiff == 1:
                    pygame.draw.rect(screen, GREEN, easyCell2)
                elif aiTwoDiff == 2:
                    pygame.draw.rect(screen, GREEN, normalCell2)
                elif aiTwoDiff == 3:
                    pygame.draw.rect(screen, GREEN, hardCell2)
                elif aiTwoDiff == 4:
                    pygame.draw.rect(screen, GREEN, vHardCell2)
            
            # Draw the texts in the table cells
            screen.blit(gameModeText, (gameModeCell.left + cellPadding, gameModeCell.top + cellPadding))
            screen.blit(pvpText, (pvpCell.left + cellPadding, pvpCell.top + cellPadding))
            screen.blit(pvcText, (pvcCell.left + cellPadding, pvcCell.top + cellPadding))
            screen.blit(cvcText, (cvcCell.left + cellPadding, cvcCell.top + cellPadding))
            
            if gameMode in (2, 3):
                screen.blit(whiteAiDiffText, (aiOneDiffCell.left + cellPadding, aiOneDiffCell.top + cellPadding))
                screen.blit(easyText, (easyCell.left + cellPadding, easyCell.top + cellPadding))
                screen.blit(normalText, (normalCell.left + cellPadding, normalCell.top + cellPadding))
                screen.blit(hardText, (hardCell.left + cellPadding, hardCell.top + cellPadding))
                screen.blit(vHardText, (vHardCell.left + cellPadding, vHardCell.top + cellPadding))
            
            if gameMode == 3:
                screen.blit(blackAiDiffText, (aiTwoDiffCell.left + cellPadding, aiTwoDiffCell.top + cellPadding))
                screen.blit(easyText, (easyCell2.left + cellPadding, easyCell2.top + cellPadding))
                screen.blit(normalText, (normalCell2.left + cellPadding, normalCell2.top + cellPadding))
                screen.blit(hardText, (hardCell2.left + cellPadding, hardCell2.top + cellPadding))
                screen.blit(vHardText, (vHardCell2.left + cellPadding, vHardCell2.top + cellPadding))
            
            if (gameMode == 1) or (gameMode == 2 and aiOneDiff) or (gameMode == 3 and aiOneDiff and aiTwoDiff):
                pygame.draw.rect(screen, (50, 200, 50), beginBgCell, 2) # Border
                screen.blit(beginText, beginTextCell)
            
            # Update the display
            pygame.display.flip()
        
        # Starting the game.
        if not terminate:
            print(f"Starting a game with the following options:\nGame mode: {gameMode}\nAI difficulty for the first agent: {aiOneDiff}\nAI difficulty for the second agent: {aiTwoDiff}")
            if gameMode == 1:
                startPvPMatch(asPlugin=True)
            
            elif gameMode == 2:
                startAiMatch(1, aiOneDiff, asPlugin=True)
            
            elif gameMode == 3:
                startAiMatch(2, aiOneDiff, aiTwoDiff, asPlugin=True)
            print("="*50)

    # Quit pygame
    pygame.quit()

    # Print the selected options
    # print('Game mode:', gameMode)
    # print('AI difficulty for the first agent:', aiOneDiff)
    # print('AI difficulty for the second agent:', aiTwoDiff)


if __name__ == "__main__":
    # EnableDPI_Awareness()
    #testing editing
    StartGame()
