# Othello-Ai-Project

Othello game with GUI, and you can play it against the computer or player vs player.

# The alghorithm

For the development of this project, we use a famouse algorithm for boardgames called "Minimax". This algorithm try to find the best move assuming that the oponent also play good.


# About the game

There are 2 players and the goal is to have the most disks of your own colour as soon as the opponent is unable to place any more of his colour.

At the start there are 4 disks, 2 for  each player lined up in the center with this pattern:

W B

B W

You can place a disk on the empty field if you have, looking from that position, at least one diagonal, horizontal or vertical line full of your opponents colour up to one of your own.

Then you make your move, the oponnent's disks which end up in between will switch to your colour.

Example: Here you are W and shown below is an extract of a possible alignment in a running game. To keep it simple only a horizontal line is shown here.

1 2 3 4 5 6 7 8 9

_ _ B B B W _ _ W

You can place your disk at the second position, because on the horizontal direction after the 3 Bs a disk of your colour (W) is located at position 6.

Following this move, every B in between will change colour

1 2 3 4 5 6 7 8 9

_ W W W W W _ _ W

This concept applies for horizontal, vertical and diagonal directions.



# How to Play

1. The game is played on an 8x8 board.

2. There are 64 disks, each one colored black on one side and white on the other.

3. At the start of the game, two black and two white pieces are placed in the center of the board, forming a square pattern.

4. Each player takes turns to place a disk of their color on the board.

5. A player can only place a disk on the board if it will result in the capture of at least one of their opponent's disks.

6. A disk is captured if it is surrounded on either side by a line of the opponent's disks, with one of the player's disks at each end of the line.

7. The game ends when the board is full or neither player can make a valid move.

8. The player with the most disks of their color on the board at the end of the game is the winner.


