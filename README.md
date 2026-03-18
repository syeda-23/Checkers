# Checkers

## Overview
This is a game of checkers (or draughts!) I built using Python, with the GUI implemented using Tkinter. It is playable against either a human or computer opponent. The computer moves are determined using the minimax algorithm

## Features

1. **Main menu and settings:** The user is presented with the option to play a one player or two player game. The main menu also displays one of three poems to the user
2. **Settings and customisation:** The user can choose which coloured player makes the first move: black or white. They can also decide whether or not the program will force the user to make a 'jump' move, wherever one is possible. If playing against the computer, the user can select a difficulty level to play againts (easy, medium, hard).
3. **Gameplay** The game alternates players' turns accordingly and displays a message indicating whose turn it currently is. To play, the user clicks a piece they wish to move, which will then highlight on the board valid moves they can make. After clicking one of the highlighted moves, they will have made their turn. The game ends when there is no more of the opponent's pieces left on the board.
The board is represented using a dictionary where keys represent the coordinates in the form (row, column) and values store information about which piece is stored at each position on the board.

## Minimax algorithm and the one player mode
The computer opponent in the one player mode generates its moves using the minimax algorithm. It assumes the computer player wants to maximise their score, and the human player wants to minimise their score. The heuristic score is calculated using the following formula which prioritises kinging by weighting king pieces by 3, and also maximises the number of pieces on the board. There are other strategies and heuristic measures that also weight pieces at the edge of the board more heavily:

        score = (#computer pieces - #user pieces) + ((3 * #comp kings) - (3 * #user kings))

**Easy Mode:** This mode does not utilise the minimax algorithm. Instead, moves are randomly selected<br>
**Medium Mode:** Whereas Medium mode evaluates moves up to a depth of 2, considering the opponent’s immediate response<br>
**Hard Mode:** Hard mode extends to a depth of 4, allowing it to anticipate multiple moves ahead and make more strategic decisions. 
