# Othello-Ai-Project

[About the game]

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

