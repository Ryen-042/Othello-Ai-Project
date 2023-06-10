"""This module is used to start an AI match of Othello."""

from OthelloCore import GameBoard

class AiGameBoard(GameBoard):
    
    def __init__(self):
        super(AiGameBoard, self).__init__()
        
        self.stableDisks = [[0] * self.col for _ in range(self.row)]
        """
        A 2D array that represents the stable/safe disks on the game board.
        A disk is considered stable if it cannot be captured by the opponent from any position.
        """
        
        self.blackStableDisksCount = 0
        """Counts the number of stable/safe black disks on the board."""
        
        self.whiteStableDisksCount = 0
        """Counts the number of stable/safe white disks on the board."""
        
        # Next two variables are used for calculating a score/heuristic for the current game board.
        self.blackSemiStableDirections = 0
        """
        Counts the number of directions in which the black disks cannot be captured.
        Does not count the fully stable disks, so the maximum value for each disk is only 3.
        """
        
        self.whiteSemiStableDirections = 0
        """
        Counts the number of directions in which the white disks cannot be captured.
        Does not count the fully stable disks, so the maximum value for each disk is only 3.
        """

    def updateCount(self):
        """Updates the GameBoard counters."""
        
        self.blackCount = self.whiteCount = 0
        self.blackStableDisksCount = self.whiteStableDisksCount = 0
        
        # We need to check all the `8` directions to determine if a disk is stable. The other directions are also checked when `isStable` is called.
        steps = ((-1, -1), (-1, 0), (-1, 1), (0, 1))
        self.blackSemiStableDirections = self.whiteSemiStableDirections = 0
        
        # Resetting the list of possible moves.
        self.possibleMoves = set()
        
        # Clearing any empty positions marked as possible moves (-1) that have been found in a previous call to this function.
        for row_i in range(self.row):
            for col_i in range(self.col):
                if self.disks[row_i][col_i] == -1:
                    self.disks[row_i][col_i] = 0
        
        opponent = 3 - self.player # (3 - 1 = 2), (3 - 2 = 1)
        
        for row_i in range(self.row):
            for col_i in range(self.col):
                ## Updating some counters.
                if self.disks[row_i][col_i] == 1:
                    self.blackCount += 1
                    
                    if self.stableDisks[row_i][col_i]:
                        self.blackStableDisksCount += 1
                
                elif self.disks[row_i][col_i] == 2:
                    self.whiteCount += 1
                    
                    if self.stableDisks[row_i][col_i]:
                        self.whiteStableDisksCount += 1
                
                ## Checking the stability of the disks.
                # If a piece is not stable and is either black or white, check if it is stable in all directions.
                if self.disks[row_i][col_i] in (1, 2) and not self.stableDisks[row_i][col_i]:
                    # Counts the number of directions (e.g., (top, down), (left, right), and both diagonals) in which the disk is stable. Max is 4.
                    stabilityCounter = 0
                    
                    for step in steps:
                        if not self.isStable((row_i, col_i), step):
                            break
                        
                        stabilityCounter += 1
                    
                    # If the disk is stable in all directions, then it is considered stable.
                    if stabilityCounter == 4:
                        self.stableDisks[row_i][col_i] = self.disks[row_i][col_i]
                    
                    # Otherwise, update the heuristics of the current player.
                    else:
                        if self.disks[row_i][col_i] == 1:
                            self.blackSemiStableDirections += stabilityCounter
                        
                        elif self.disks[row_i][col_i] == 2:
                            self.whiteSemiStableDirections += stabilityCounter
                
                # Updating the list of possible moves:
                # Checking for possible moves that the current player can make by iterating over each
                # position on the board and checking if it contains a dicks belonging to the current player.
                # If a dick is found, then we check in all eight directions to see if there are any opposing
                # dicks that can be captured by moving in that direction. If a sequence of opposing dicks is
                # found, and the next position in that direction is empty, then that empty position is considered
                # a valid move and added to the list of available positions.
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

    def isStable(self, pos: tuple[int, int], step: tuple[int, int]):
        """Checks if the specified disk is stable/safe at the given position and its opposite."""
        
        opponent = 3 - self.disks[pos[0]][pos[1]]
        stabilityCounter = 0
        
        # Check if the specified disk is stable in the given and opposite directions.
        for rowStep, colStep in (step, (-step[0], -step[1])):
            row, col = pos[0] + rowStep, pos[1] + colStep
            
            # Set when we continue searching in the same direction.
            keepSearching = False
            
            while True:
                # If the position is out of bounds (reached the edge of the board), this means that the disk is stable in this direction.
                if not (0 <= row < self.row and 0 <= col < self.col):
                    # If we were still searching in the same direction, then break the loop.
                    if keepSearching:
                        stabilityCounter += 1
                        break
                    
                    # Otherwise, the specified disk is stable in the specified direction.
                    return True
                
                # If the disk we are checking (i.e., the disk at (row, col)) belongs to the current player:
                if self.disks[row][col] == self.disks[pos[0]][pos[1]]:
                    # If this disk is marked stable, then the specified disk is also stable and cannot be captured from the specified direction.
                    if self.stableDisks[row][col]:
                        return True
                    
                    # Otherwise, the disk may be unstable so we need to keep checking the same direction to find if an opponent disk is present.
                    row, col = row + rowStep, col + colStep
                    keepSearching = True
                
                # If the disk we are checking belongs to the opponent:
                elif self.disks[row][col] == opponent:
                    # If this disk is marked stable, then the specified disk is also stable and cannot be captured from this direction.
                    # However, it may still be captured from the opposite direction.
                    # For example: [2, 2, 1, 0]. The black disk is stable from the left side but can be captured from the right side.
                    if self.stableDisks[row][col]:
                        stabilityCounter += 1
                        break
                    
                    # The opponent disk may be unstable from this direction, for example: [0, 0, 2, 1, 2, 0]
                    # If a black disk is placed at position 1, another white disk can be placed at position 0,
                    # and the black disk we are interested in (at position 3) will be captured.
                    row, col = row + rowStep, col + colStep
                    keepSearching = True
                else:
                    break
        
        if stabilityCounter == 2: # Stable in both directions.
            return True
        
        return False
    
    def shallowCopy(self):
        """Returns a shallow copy of the current game board."""
        
        newBoard = AiGameBoard()
        newBoard.player = self.player
        newBoard.disks = [row[:] for row in self.disks]
        newBoard.blackCount = self.blackCount
        newBoard.whiteCount = self.whiteCount
        newBoard.possibleMoves = set(item[:] for item in self.possibleMoves)
        
        newBoard.stableDisks = [row[:] for row in self.stableDisks]
        newBoard.blackStableDisksCount = self.blackStableDisksCount
        newBoard.whiteStableDisksCount = self.whiteStableDisksCount
        newBoard.blackSemiStableDirections = self.blackSemiStableDirections
        newBoard.whiteSemiStableDirections = self.whiteSemiStableDirections
        return newBoard

class GameBoardNode:
    """A node in the game board tree."""
    
    def __init__(self, gameBoard: AiGameBoard):
        self.gameBoard = gameBoard
        self.parent: GameBoardNode = None # type: ignore
        self.children: dict[tuple[int, int], GameBoardNode] = {}
        
        if gameBoard.player == 1:
            self.score = 100 * (gameBoard.blackStableDisksCount - gameBoard.whiteStableDisksCount) + \
                                    (gameBoard.blackSemiStableDirections  - gameBoard.whiteSemiStableDirections)
        elif gameBoard.player == 2:
            self.score = 100 * (gameBoard.whiteStableDisksCount - gameBoard.blackStableDisksCount) + \
                                    (gameBoard.whiteSemiStableDirections  - gameBoard.blackSemiStableDirections)

class GameBoardTree:
    """A tree that represents the game board and its possible moves."""

    def __init__(self, node: GameBoardNode, depth = 2) -> None:
        self.root = node
        self.searchDepth = depth

    def expandTree(self) -> None:
        """Expands the tree by adding the possible moves from the root node."""
        
        BFS_Nodes: list[GameBoardNode] = [self.root]
        BFS_NodesNext: list[GameBoardNode] = []
        
        # Expanding the tree by adding the possible moves from the root node.
        for _ in range(self.searchDepth):
            for node in BFS_Nodes:
                # If the node has children, then it has already been expanded.
                if node.children:
                    for pos in node.children:
                        BFS_NodesNext.append(node.children[pos])
                
                # Otherwise, expand the node.
                else:
                    for pos in node.gameBoard.possibleMoves:
                        newGameBoard = putDisk(node.gameBoard, pos)
                        
                        if newGameBoard:
                            childNode = GameBoardNode(newGameBoard)
                            childNode.parent = node # type: ignore
                            node.children[pos] = childNode
                            BFS_NodesNext.append(childNode)
            
            BFS_Nodes = BFS_NodesNext
            BFS_NodesNext = []

    def minMax(self, node: GameBoardNode, player: bool, depthLimit: int) -> float:
        """Returns the score of the game board at the given node."""
        
        if not depthLimit or not node.children:
            return node.score
        
        scores: dict[tuple[int, int], float] = {}
        for pos in node.children:
            scores[pos] = self.minMax(node.children[pos], player, depthLimit - 1)
        
        if node.gameBoard.player == player:
            return min(scores.values())
        
        return max(scores.values())

    def getBestMove(self, player) -> tuple[int, int]:
        """Returns the best move for the current player."""
        
        scores: dict[tuple[int, int], float] = {}
        for pos in self.root.children:
            scores[pos] = self.minMax(self.root.children[pos], player, self.searchDepth - 1)
        
        if not scores:
            return (-1, -1)
        
        if self.root.gameBoard.player == player:
            return min(scores, key = scores.get) # type: ignore
        
        return max(scores, key = scores.get) # type: ignore

def putDisk(gameBoard: AiGameBoard, pos: tuple[int, int]) -> AiGameBoard | None:
    """Puts a disk at the specified position on the game board."""
    
    if not (0 <= pos[0] < gameBoard.row and 0 <= pos[1] < gameBoard.col and gameBoard.disks[pos[0]][pos[1]] == -1):
        return
    
    # If the position is within the boundaries and the location is empty, then put the disk.
    newGameBoard = gameBoard.shallowCopy()
    newGameBoard.disks[pos[0]][pos[1]] = gameBoard.player
    newGameBoard.captureDisks(pos)
    
    newGameBoard.player = 3 - gameBoard.player
    newGameBoard.updateCount()
    
    return newGameBoard
