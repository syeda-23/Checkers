import time
from tkinter import *
import copy
#from game_images import *
import random
from copy import deepcopy

moves = []

class Game():

    def __init__(self,root, difficulty, turn, enforceJump):
         
        # defining global variables
        self.turn = turn
        self.first = self.turn 
        self.selected_piece = [] # determines which piece has been clicked so only one piece can be clicked at a time
        self.board = {} # the state of the board is stored as a dictionary
        self.enforceJump = enforceJump # user can decide whether they want jumping to be mandatory
        self.mustJump = False
        self.level = difficulty
        self.gameOver = False
        self.nodesChecked = 0

        # defining variables relating to the computer player
        if self.turn == "black":
            self.computerColour = "white" # colour the computer is playing as
            self.playerColour = "black" # colour the user is playing as
        elif self.turn == "white":
            self.computerColour = "black"
            self.playerColour = "white"
        
        # defining colours 
        self.BEIGE = "#e7ead6"
        self.BLACK = "#596070"
        self.GREY = "#91949c"

        # window formatting
        self.root = root     
        self.frame2 = Frame(root)
        self.frame2.pack(padx=30, pady=30, expand=True, anchor="center")
      
        # defining the files and images to be used
        self.root.white_pawn = PhotoImage(file = "white_pawn.png").subsample(4, 4)
        self.root.black_pawn = PhotoImage(file = "black_pawn.png").subsample(4, 4)
        self.root.white_pawn_clicked = PhotoImage(file = "white_pawn_clicked.png").subsample(4,4)
        self.root.black_pawn_clicked = PhotoImage(file = "black_pawn_clicked.png").subsample(4,4)
        self.root.white_pawn_option = PhotoImage(file = "white_pawn_option.png").subsample(4,4)
        self.root.black_pawn_option = PhotoImage(file = "black_pawn_option.png").subsample(4,4)
        self.root.white_king = PhotoImage(file = "white_king.png").subsample(4,4)
        self.root.black_king = PhotoImage(file = "black_king.png").subsample(4,4)
        self.root.white_king_clicked = PhotoImage(file = "white_king_clicked.png").subsample(4,4)
        self.root.black_king_clicked = PhotoImage(file = "black_king_clicked.png").subsample(4,4)
        self.root.white_king_option = PhotoImage(file = "white_king_option.png").subsample(4,4)
        self.root.black_king_option = PhotoImage(file = "black_king_option.png").subsample(4,4)
     
        # initialising the game
        self.backEnd()
        print(self.board)
        self.DrawBoard()

        # defining the right hand side
        title = Label(self.frame2, bg = self.BLACK, text = ("❤ checkers ❤"), fg = "white", font = ("Fixedsys",25), anchor = CENTER)      
        title.grid(row = 2, column = 33, padx = 20, pady = 10)
        self.turnAlert = Label(self.frame2, bg = self.BLACK, text = (self.turn + "'s go"), fg = "white", font = ("Fixedsys",20), anchor = CENTER)      
        self.turnAlert.grid(row = 3, column = 33)
        restart = Button(self.frame2, bg = self.BLACK, text = ("restart ↻"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = lambda: self.restartGame())
        restart.grid(row = 6, column = 33)
        menu = Button(self.frame2, bg = self.BLACK, text = ("menu ☰"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = lambda: self.Menu())
        menu.grid(row = 7, column = 33)
        if self.enforceJump: # sets up the message that will indicate whether there is a mandatory jump to be made or not
            self.jumpAlert = Label(self.frame2, bg=self.BLACK, text="no jump", fg="white", font=("Fixedsys", 20), anchor=CENTER)
            self.jumpAlert.grid(row=5, column=33, padx=20, pady=10)
            
        # row 2: checkers title
        # row 3: whose turn
        # row 5: mandatory jump alert
        # row 4: winning notification
        # row 6: restart button
        # row 7: menu button

    def Menu(self): # takes the user back to the starting screen when 'menu' button is pressed
       import menu
       self.root.destroy()  # Destroy the current window to open the menu
       root = Tk()  # Create a new root window
       menu.Menu(root)  # Pass the new root window to the menu class
       root.mainloop()

################################################# MINIMAX SUBROUTINES ##################################################################

    def evaluateScore(self, board): # evaluates the state of the board and allocates it a score

        comp_pieces = 0
        comp_kings = 0
        user_pieces = 0
        user_kings = 0
  
        for coord in board: # iterates through each piece on the board
            piece = board[coord]
            if piece!= " ":
                if piece[0] == self.computerColour[0]:
                    comp_pieces = comp_pieces + 1
                    if len(piece) > 1 and piece[1] == "k":  # check for kings 
                        comp_kings += 1 # keeps a count of kings

                elif piece[0] == self.playerColour[0]:
                    user_pieces += 1
                    if len(piece) > 1 and piece[1] == "k": # check for kings 
                        user_kings += 1

        score = (comp_pieces - user_pieces) + ((3*comp_kings) - (3*user_kings)) # final score calculation
        return score

    def computerMove(self): # subroutine called when it is the computer's turn to make a move - handles calculating which move to make and updating the front and back end board accordingly

        self.mustJump = False
        
        # for easy mode, moves are randomly generated
        if self.level == "easy":
            bestMoves = self.generateAllMoves(self.computerColour, self.board)
            bestMove = random.choice(bestMoves)
 
            piece = bestMove['start']
            move = bestMove['moves']
            if len(move) > 1:
                move = random.choice(move)
            elif len(move) == 1:
                move = move[0]
            
        else: # for medium and hard modes, the minimax algorithm determines the move
            board_copy = copy.deepcopy(self.board) # minimax will simulate different moves using a copy of the board, so the current state of the board is not altered
            if self.level == "medium":
                bestScore, bestMoves = self.minimax(board_copy, 2, True)# medium mode will search to a depth of 2
                # when computer plays we want to maximise our score
            else:
                bestScore, bestMoves = self.minimax(board_copy, 4, True)# hard mode will search to a depth of 3 

            # since all moves returned by the minimax function are of equal value, pick a random move
            bestMove = random.choice(bestMoves)
            piece = bestMove['start']
            move = bestMove['moves']
        
        if len(move) > 1:
            Jump = True
        else:
            Jump = False

        # make the front and back end move
        self.board = self.makeMoveBackEnd(self.computerColour, move, int(move[-1][0]),int(move[-1][1]), int(piece[0]), int(piece[1]), Jump, self.board)
        self.updateBoardAndUI(move[-1][0], move[-1][1], piece[0], piece[1], self.computerColour, move, Jump)
        self.mustJump = False

    def minimax(self, state, depth, isMaximising): # state is the state of the board, depth is how far we are in the tree, gets decremented, isMaximising is a Boolean value

        # determine depth - position is only evaluated if we reach end of the tree or if we win
        if depth == 0 or self.checkWin(state) != " ": # if we've won the game, no need to keep searching
            score = self.evaluateScore(state) # if depth is 0, get the evaluation of that move, return the current state along with the score it generated
            return score, state

        bestMoves = [] # moves with the highest score stored in this list

        # computer's turn to maximise score
        if isMaximising:
            
            allMoves = self.generateAllMoves(self.computerColour, state) # retrieves all possible moves for the computer colour so we can loop through each
            bestScore = float('-inf') # initialise score to arbitrarily negative score
            
            for item in allMoves: # iterate through every possible move and simulate it to obtain a score
    
                piece = item['start']
                moves = item['moves']

                for m in moves:
                    if len(m) > 1:
                        Jump = True
                    else:
                        Jump = False
 
                    simulate_board = copy.deepcopy(state) # copy of current state of the board to simulate move
                    simulate_board = self.makeMoveBackEnd(self.computerColour, m, m[-1][0] , m[-1][1], piece[0], piece[1], Jump, simulate_board) # simulate making the move                    
                    score = self.minimax(simulate_board, depth-1, False)[0] # once base case is reached, we only need the score for that move

                    if score > bestScore:
                        bestScore = score
                        bestMoves = [{'start': piece, 'moves': m}]
                    elif score == bestScore:
                        bestMoves.append({'start': piece, 'moves': m})
                
            return bestScore, bestMoves
        
        else: # player's turn to minimise score
            
            allMoves = self.generateAllMoves(self.playerColour, state)
            bestScore = float('inf') # initialise score to arbitrarily large value
            
            for item in allMoves:
                piece = item['start']
                moves = item['moves']

                for m in moves:
                    if len(m) > 1:
                        Jump = True
                    else:
                        Jump = False
 
                    simulate_board = copy.deepcopy(state)
                    simulate_board = self.makeMoveBackEnd(self.playerColour, m, m[-1][0] , m[-1][1], piece[0], piece[1], Jump, simulate_board)                    
                    score = self.minimax(simulate_board, depth-1, True)[0]

                    if score < bestScore:
                        bestScore = score
                        bestMoves = [{'start': piece, 'moves': m}]
                    elif score == bestScore:
                        bestMoves.append({'start': piece, 'moves': m})

            return bestScore, bestMoves
        
    def generateAllMoves(self, colour, state): # get all possible moves from current state of board

        allMoves = [] 
        jumpMoves = []
        if self.enforceJump:
            mustJump = False

        for key in state:
            if state[key][0] == colour[0]: # iterates through each piece in the board dictionary looking for pieces of the same colour
                row = str(key)[0]
                column = str(key)[1]
                if state[key][1] == "k":
                    kinged = True
                else:
                    kinged = False

                moves, Jump = self.calculateMoves(int(row), int(column), colour, kinged, state) # calculates moves for each piece
 
                if moves!= []: # if there are possible moves to make for that piece, store it as a dictionary with the key as the start coordinate and value as end coordinate
                    move = {'start': (row+column),'moves': moves}
                    if Jump: # if its a jump move, append it to the jumpMoves list
                        jumpMoves.append(move)
                    else: # if its not a jump move, append it to normal moves list
                        allMoves.append(move)

        if self.enforceJump and jumpMoves!= []: # if mandatory jumping is being enforced and there are jump moves to be made, only return the jump moves 
            return jumpMoves

        else:
            return allMoves + jumpMoves

###########################################################################################################################################################
###########################################################################################################################################################
        
    def backEnd(self): # defining the back end board, stored as dictionary, only stores the grey coordinates the game is played on 

        for r in range(1,9):
            for c in range(1,9):
                # defining black pieces
                if (c in [2,4,6,8] and r in [1,3]) or (c in [1,3,5,7] and r == 2):
                    self.board[str(r) + str(c)] = "bp"

                # defining white pieces
                elif (c in [1,3,5,7] and r in [8,6]) or (c in [2,4,6,8] and r == 7):
                    self.board[str(r) + str(c)] = "wp"
                
                # defining blank grey pieces  
                elif (r + c)%2 != 0:
                    self.board[str(r) + str(c)] = " "

    def calculateMoves(self, row, column, colour, kinged, state):
        
        Jump = False # Boolean flag that indicates whether a jump move is possible for that piece, useful for detecting mandatory jumps
        moves = [] # initialises moves as an empty list

        # sets up the direction the selected piece can move in based on its status (pawn or king),stored as a list
        if kinged:
            direction = [1,-1]# kings can move up and down the board        
        elif colour == "black":
            direction = [1]
        else:
            direction = [-1]

        # checks for single moves
        for d in direction: # storing direction as a list allows us to iterate through the directions list      
            try:
                if 0 < (row + d) < 9 and 0 < (column + d) < 9 and state[str(row + d) + str(column + d)] == " ":
                    moves.append([str(row + d) + str(column + d)])          
                if 0 < (row + d) < 9 and 0 < (column - d) < 9 and state[str(row + d) + str(column - d)] == " ":
                    moves.append([str(row + d) + str(column - d)])
            except:
                pass

        # calls function that will check for jumps
        Jump, jump_moves = self.checkJump(row, column, colour, kinged, state)

        if self.enforceJump: # this part enforces mandatory jumping           
            if Jump: # if there is a jump move to be made and mandatory jumping is being enforced, the function should only return the jump move
                moves = jump_moves
            elif self.mustJump: # if there is a jump move that can be made by another piece of the same colour, enforce that jump move
                moves = []
        else: # if mandatory jumping is not being enforced, add any jump moves to current list of moves
            for m in jump_moves:
                moves.append(m)

        return moves, Jump
        
    def checkJump(self, row, column, colour, kinged, state, visited = None): # checks for jump moves and returns a list of jump moves a piece can make

        jump_moves = []
        further_jumps = []
        Jump = False
        JumpMore = False

        # for kinged pieces, having a list of visited nodes helps prevent infinite recursion as nodes that have already been explored won't be visited again
        if visited == None:
            visited = []
        visited.append(str(row) + str(column))# append the current piece to the 'visited' list

        # sets up the direction the selected piece can move in(stored as a list) and defines the opponent colour    
        if colour == "black":
            opponent = "w"
            if not kinged:
                direction = [1]
            else:
                direction = [1,-1]
                
        elif colour == "white":
            opponent = "b"
            if not kinged:
                direction = [-1]
            else:
                direction = [1,-1]

        for d in direction:
            
            # checks for jumps in one direction - in this case checks for jumps 'up' 
            if 0 < (row + 2*d) < 9 and 0 < (column + 2*d) < 9:            
                adjacent = state[str(row + d) + str(column + d)] # finds which piece is stored diagonally
                end = state[str(row + 2*d) + str(column + 2*d)] # find which piece is stored at the end of the jump move
                if adjacent[0] == opponent and end == " " and (str(row+2*d) + str(column + 2*d)) not in visited: # checks if the piece diagonally is an opponent piece, and the space diagonal to that is an empty space
                    current_move = [str(row + d) + str(column + d),str(row + 2*d) + str(column + 2*d)] # current valid jump moves stored in current_move
                    new_visited = visited.copy() # when checking if a compound jump can be made, call the checkJump subroutine and send it the list of pieces that have already been visited 
                    JumpMore, further_jumps = self.checkJump(row + 2*d, column + 2*d, colour, kinged,self.board,new_visited)# all these jump moves come from the move we've just made

                    if JumpMore: # checks if any further jumps can be made by calling the checkJump subroutine again
                        for jump in further_jumps: # if any further jumps can be made, append them to the list of jump moves that can be made
                            jump_moves.append(current_move + jump)
                    else:
                        jump_moves.append(current_move)# the end coordinate is stored last, and any pieces to be jumped over are stored at the front of the list

            # checks for jumps in the other direction - in this case 'down' the board
            if 0 < (row + 2*d) < 9 and 0 < (column - 2*d) < 9:               
                adjacent = state[str(row + d) + str(column - d)]
                end = state[str(row + 2*d) + str(column - 2*d)]
                if adjacent[0] == opponent and end == " " and (str(row+2*d)+ str(column-2*d)) not in visited:
                    new_visited = visited.copy()
                    current_move = [str(row + d) + str(column - d), str(row + 2*d) + str(column - 2*d)]
                    JumpMore, further_jumps = self.checkJump(row + 2*d, column - 2*d, colour, kinged,self.board, new_visited)

                    if JumpMore:
                        for jump in further_jumps:
                            jump_moves.append(current_move + jump)
                    else:
                        jump_moves.append(current_move)

        if jump_moves!=[]: 
            Jump = True # Jump is a Boolean value that indicates whether there are any jump moves for that piece
            
        return Jump, jump_moves

    def checkWin(self, state): # after every move, this function is called to see if a winning move has been made - player wins when there are no opponent pieces left on the board
        
        black = 0
        white = 0
        winner = " "
        
        # loops through each coordinate in the board dictionary and counts how many of each piece there are
        for key in state:
            piece = state[key]
            if piece[0] == "b":
                black = black + 1
            elif piece[0] == "w":
                white = white + 1
                
        if black == 0: 
            winner = "white"
        elif white == 0:
            winner = "black"

        if winner in ["black", "white"]:
            self.endGame(winner)

        return winner  # returns which colour has won (black or white if there has been a winning move, and " " if no one has won yet)

    def checkDraw(self, colour): # checks if the game has come to a draw (neither player can move)

        Draw = True
        for key in self.board: # loops through each piece on the board and checks if a move can be made for colour passed to it
            piece = self.board[key]            
            if piece[0] == colour[0]:
                if key in self.board and len(self.board[key]) > 1 and self.board[key][1] == "k":
                    kinged = True
                else:
                    kinged = False
                    
                moves, Jump = self.calculateMoves(int(key[0]), int(key[1]),colour, kinged, self.board)
                print("moves for", piece, key, "is", moves)
                
                if moves != []:# if any valid moves are possible, the game has not come to a draw
                    Draw = False
                    break

        if Draw:
            self.endGame("draw")
            return True # return Boolean value that indicates whether game has come to a draw
        else:
            return False

    def makeMoveBackEnd(self, colour, moves, newR, newC, oldR, oldC, Jump, state): # updates the dictionary whenever a move is made
        newR = int(newR)
        newC = int(newC)
        oldR = int(oldR)
        oldC = int(oldC)
        piece = state[str(oldR) + str(oldC)]
        # updates the dictionary so the piece is not stored at its new coordinates
        if colour == "black":
           if newR == 8 or piece == "bk":
                state[str(newR) + str(newC)] = "bk"                
           else:
                state[str(newR) + str(newC)] = "bp"

        if colour == "white":
            if newR == 1 or piece == "wk":
                state[str(newR) + str(newC)] = "wk"                
            else:
                state[str(newR) + str(newC)] = "wp"

        # removes piece from old coordinates and replaces old coordinates with a blank space
        state[str(oldR) + str(oldC)] = " "

        if Jump:
            # make jump move
            if type(moves[0])==list:
                for m in moves:
                    if (str(newR) + str(newC)) in m:
                        for i in range(len(m)-1):
                            state[str(m[i][0]) + str(m[i][1])] = " "
            else:
                for i in range(len(moves)-1):
                            state[str(moves[i][0]) + str(moves[i][1])] = " "

        return state
        
    def endGame(self, state): # game ends if there is a win or draw

        # display end state of the game (draw or win)
        if state == "draw":
            self.message = Label(self.frame2, bg = self.BLACK, text = ("draw"), fg = "white", font = ("Fixedsys",20))        
            self.message.grid(row = 4, column = 33)
        elif state == "black":
            self.message = Label(self.frame2, bg = self.BLACK, text = ("black won!!"), fg = "white", font = ("Fixedsys",20))        
            self.message.grid(row = 4, column = 33)
        elif state == "white":
            self.message = Label(self.frame2, bg = self.BLACK, text = ("white won!!"), fg = "white", font = ("Fixedsys",20))        
            self.message.grid(row = 4, column = 33)

        self.gameOver = True

        # remove any unnecessary labels    
        if self.enforceJump:
            self.jumpAlert.config(text = "")
        self.turnAlert.config(text = "")
        self.turnAlert.update()

################################################ FRONT END SUBROUTINES #########################################################################
        
    def DrawBoard(self): # drawing the state of the board so it matches the board dictionary - front end GUI board     

        self.root.configure(background=self.GREY)
        
        # ensuring the front end matches the contents of the back end board dictipnary
        for key in self.board:
            r = int(str(key)[0])
            c = int(str(key)[1])
            if self.board[key] == " ":
                button = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
            elif self.board[key] == "bp":
                button = Button(self.frame2, image = self.root.black_pawn, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r = r, c = c, colour = "black", clicked = False, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))
            elif self.board[key] == "wp":
                button = Button(self.frame2,image = self.root.white_pawn, width = 53, height = 65,compound="center", bg = self.BLACK , relief=FLAT, command = lambda r = r, c = c, colour = "white", clicked = False, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))

            button.grid(row = r, column = c)

        # adding the row and column numbers
        for r in range(1,9):
            for c in range(1,9):
                try:
                    if self.board[str(r) + str(c)]:
                        pass
                except:                    
                    button = Button(self.frame2, width = 7, height = 4, bg = self.BEIGE, relief=FLAT)
                    button.grid(row = r, column = c)
                    
        # labelling the rows and columns           
        for i in range(1,9):
            self.xcoords = Label(self.frame2, text = f"{i}")
            self.xcoords.grid(row = 0, column = i)

        for i in range(1,9):
            self.ycoords = Label(self.frame2, text = f"{i}")
            self.ycoords.grid(row = i, column = 0)

    def restartGame(self): # resets the board and the settings to start the game again

        self.mustJump = False
        self.backEnd()
        self.DrawBoard()
        self.turn = self.first
        
        self.turnAlert.config(text = self.turn + "'s turn")
        if self.enforceJump:
            self.jumpAlert.config(text = "no jump")

        if self.gameOver:
            self.gameOver = False
            self.message.config(text = " ")
            
    def deselectPieces(self, r, c, colour, clicked, kinged): # deselect pieces and any options for moves associated with that piece

        moves, Jump = self.calculateMoves(int(r),int(c),colour,kinged, self.board)
        if colour == self.turn == "black" and self.board[str(r)+str(c)][0] == "b": # makes sure only pieces that exist and are of the player's colour are being deselected
            if clicked: # if the piece is already clicked, unclick it, change the costume from a selected piece to deselected piece
                if kinged: 
                    button = Button(self.frame2, image = self.root.black_king, width = 53, height = 65,compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "black", clicked = False, kinged = True: self.pieceClicked(r, c, colour, clicked, kinged))
                else:
                    button = Button(self.frame2, image = self.root.black_pawn, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "black", clicked = False, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))                  
                button.grid(row = r, column = c)

                # stop displaying any moves that associated with the deselected piece
                if Jump: # handles deselecting any jump moves that are being displayed
                    self.pieceClickedJump(r, c, colour, clicked, kinged, moves)           
                else: # handles standard single moves
                    for i in moves:
                        optR = int(i[0][0])
                        optC = int(i[0][1])
                        blank = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
                        blank.grid(row = optR, column = optC)

        elif colour == self.turn == "white" and self.board[str(r)+str(c)][0] == "w":
            if clicked: # if the piece is already clicked, unclick it
                
                ## changing the costume from a selected piece to deselected piece
                if kinged: 
                    button = Button(self.frame2, image = self.root.white_king, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "white", clicked = False, kinged = True: self.pieceClicked(r, c, colour, clicked, kinged))
                else:
                    button = Button(self.frame2, image = self.root.white_pawn, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "white", clicked = False, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))                  
                button.grid(row = r, column = c)

                # stop displaying any moves that associated with the deselected piece
                if Jump: # handles jump moves
                    self.pieceClickedJump(r, c, colour, clicked, kinged, moves)           
                else: # handles standard single moves
                    for i in moves:
                        optR = int(i[0][0])
                        optC = int(i[0][1])
                        blank = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
                        blank.grid(row = optR, column = optC)       

    def pieceClicked(self, r, c, colour, clicked, kinged): # if piece clicked, change the piece appropriately

        if self.gameOver:
            return

        # displays coordinates of the piece that has been clicked
        print(r, c, " from pieceClicked")

        # calls calculateMoves at the beginning, 'moves' can be referred to throughout the rest of the function
        moves,Jump = self.calculateMoves(int(r),int(c),colour, kinged, self.board)

         # making sure you can only click a piece if it is your turn
        if colour != self.turn:
            return
        
        if clicked: # if a piece that has already been selected is clicked, call the deselectPiece function to unclick it
            self.deselectPieces(r, c, colour, clicked, kinged)

        elif not clicked: # if a piece that has not been selected is clicked, select it
            if len(self.selected_piece) > 0: # the selected_piece variable ensures any other selected pieces on the board are deselected before a new piece is selected
                self.deselectPieces(self.selected_piece[0][0], self.selected_piece[0][1], colour, True, kinged)

            self.selected_piece = []
            self.selected_piece.append(str(r) + str(c))
            
            if colour == self.turn == "black":
                if kinged: # changes the costume from an 'unclicked' to 'clicked' one
                    button = Button(self.frame2, image = self.root.black_king_clicked, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "black", clicked = True, kinged = True: self.pieceClicked(r, c, colour, clicked, kinged))
                else:
                    button = Button(self.frame2, image = self.root.black_pawn_clicked, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "black", clicked = True, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))
                button.grid(row = r, column = c)

                # displays potential moves
                if Jump:
                    self.pieceClickedJump(r, c, colour, clicked, kinged, moves)
                else:
                    self.displayOptions(moves, colour, r, c, kinged)

            elif colour == self.turn == "white": # same thing for black
                if kinged:              
                    button = Button(self.frame2, image = self.root.white_king_clicked, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "white", clicked = True, kinged = True: self.pieceClicked(r, c, colour, clicked, kinged))
                else:
                    button = Button(self.frame2, image = self.root.white_pawn_clicked, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, colour = "white", clicked = True, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))
                button.grid(row = r, column = c)

                if Jump:
                    self.pieceClickedJump(r, c, colour, clicked, kinged, moves)
                else:
                    self.displayOptions(moves, colour, r, c, kinged)

    def pieceClickedJump(self,r, c, colour, clicked, kinged, moves): # removes previously displayed jump move highlights if a piece is deselected or displays possible jump moves
        
        if clicked: # if a piece has already been selected, deselect it and stop displaying jump moves for that piece
            for m in moves:
                end = m[-1]           
                optR = int(end[0])
                optC = int(end[1])
                blank = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
                blank.grid(row = optR, column = optC)
                
        elif not clicked: # if a piece has not been clicked, highlight possible jump moves for that piece         
            for m in moves:                
                for i in range(0,len(m)):
                    if (i%2 != 0) or (i == len(m)-1): # makes sure we only consider odd indices (as jumps occur every two steps) or the last
                        end = m[i] # identifies the end location of each jump
                        optR = int(end[0])
                        optC = int(end[1])
                        
                        if colour == "white" and (i == len(m)-1): # ensures only the last position of the jump move is clickable and the user must complete a full jump move
                            button = Button(self.frame2,image = self.root.white_pawn_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda optR = optR, r=r, c=c, optC= optC, moves = moves: self.makeMove(colour,moves,optR,optC,r,c,True))
                        elif colour == "white":
                            button = Button(self.frame2,image = self.root.white_pawn_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT)
                        
                        elif colour == "black" and (i == len(m)-1):
                            button = Button(self.frame2,image = self.root.black_pawn_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda optR = optR, optC= optC,r=r, c=c, moves = moves: self.makeMove(colour,moves,optR,optC,r,c,True))
                        else:
                            button = Button(self.frame2,image = self.root.black_pawn_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT)
                        
                        button.grid(row = optR, column = optC)
    
    def makeJumpMove(self, colour, endR, endC, moves): # handles the graphics of making a jump move
        
        global board
        count = 0
        # remove the jumped over piece from GUI board and from dictionary
        if colour != self.computerColour: # slightly different functionality when computer makes jump move compared to when user makes one
            for m in moves:
                if m[-1] == str(endR) + str(endC):
                    count = count + 1
                    if count <= 1:                  
                        for i in range(len(m)-1):                   
                            jumped = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
                            jumped.grid(row = m[i][0], column = m[i][1])
                            self.board[str(m[i][0]) + str(m[i][1])] = " "

            # stop displaying all the other options
            for m in moves:           
                end = m[-1]
                optR = int(end[0])
                optC = int(end[1])
                if self.board[str(optR) + str(optC)] not in ["wp", "wk", "bp", "bk"]:
                    blank = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
                    blank.grid(row = optR, column = optC)

        elif colour == self.computerColour:
            
            endR = moves[-1][0]
            endC = moves[-1][1]
            
            piece = Button(self.frame2, image = self.root.white_pawn, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda endR=endR, endC=endC, colour = "white", clicked = False, kinged = False: self.pieceClicked(endR, endC, colour, clicked, kinged))
            piece.grid(row = endR, column = endC)

            # remove the jumped over piece(s)
            for i in range(0,len(moves)-1):
                blank = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
                blank.grid(row = int(moves[i][0]), column =  int(moves[i][1]))
                self.board[str(moves[i][0]) + str(moves[i][1])] = " "
                
    def displayOptions(self, moves, colour, oldR, oldC, kinged): # handles what happens when a piece is pressed and displays possible moves - single standard moves

        for i in moves: # iterates through the 'moves' list to display potential moves 
            r = int(i[0][0])
            c = int(i[0][1])
            if colour == self.turn == "black" and kinged:
                button = Button(self.frame2,image = self.root.black_king_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, oldR = oldR, oldC= oldC: self.makeMove(colour, moves,r,c,oldR,oldC, False))
            elif colour == self.turn == "black" and not kinged:
                button = Button(self.frame2,image = self.root.black_pawn_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, oldR = oldR, oldC= oldC: self.makeMove(colour, moves,r,c,oldR,oldC,False))
            elif colour == self.turn == "white" and kinged:
                button = Button(self.frame2,image = self.root.white_king_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, oldR = oldR, oldC= oldC: self.makeMove(colour, moves,r,c,oldR,oldC,False))
            elif colour == self.turn == "white" and not kinged:
                button = Button(self.frame2,image = self.root.white_pawn_option,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r=r, c=c, oldR = oldR, oldC= oldC : self.makeMove(colour, moves,r,c,oldR,oldC,False))
            button.grid(row = r, column = c)

    def updateBoardAndUI(self, newR, newC, oldR, oldC, colour, moves, Jump): # handles the graphics of moving a piece to a new coordinate

        global turn
        global board
        global mustJump
        
        # moving a piece to 'newCoord' and setting 'oldCoord' to be an blank piece
        oldCoord = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
        oldCoord.grid(row = oldR, column = oldC) 
        if colour == "black":          
            newCoord = Button(self.frame2, image = self.root.black_pawn,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda clicked = False, kinged= False: self.pieceClicked(newR, newC, colour, clicked, kinged))
            newCoord.grid(row = newR, column = newC)        
        if colour == "white":          
            newCoord = Button(self.frame2, image = self.root.white_pawn,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda clicked = False, kinged = False: self.pieceClicked(newR, newC, colour, clicked, kinged))
            newCoord.grid(row = newR, column = newC)

        # kings
        if colour == "black":
           if newR == 8 or self.board[str(oldR) + str(oldC)] == "bk":
                king = Button(self.frame2, image = self.root.black_king,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda clicked = False, kinged = True: self.pieceClicked(newR, newC, colour, clicked, kinged))
                king.grid(row = newR, column = newC)
        if colour == "white":
            if newR == 1 or self.board[str(oldR) + str(oldC)] == "wk":
                
                king = Button(self.frame2, image = self.root.white_king,  width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda clicked = False ,kinged = True: self.pieceClicked(newR, newC, colour, clicked, kinged))
                king.grid(row = newR, column = newC)

        # removing any alternate options that the user hasnt selected from the board once they make a move
        if Jump:
            self.makeJumpMove(colour, newR, newC, moves)
        else:
            if colour != self.computerColour:
                for i in moves:
                    if (i[0][0] + i[0][1]) != (str(newR) + str(newC)):
                        blank = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
                        blank.grid(row = int(i[0][0]), column = int(i[0][1]))

        # clear the board
        for piece in self.board:
            r = int(str(piece)[0])
            c = int(str(piece)[1])
            if self.board[piece] == " ":
                button = Button(self.frame2, width = 7, height = 4, bg = self.BLACK, relief=FLAT)
            elif self.board[piece] == "bp":
                button = Button(self.frame2, image = self.root.black_pawn, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r = r, c = c, colour = "black", clicked = False, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))
            elif self.board[piece] == "bk":
                button = Button(self.frame2, image = self.root.black_king, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r = r, c = c, colour = "black", clicked = False, kinged = True: self.pieceClicked(r, c, colour, clicked, kinged))
            elif self.board[piece] == "wp":
                button = Button(self.frame2, image = self.root.white_pawn, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r = r, c = c, colour = "white", clicked = False, kinged = False: self.pieceClicked(r, c, colour, clicked, kinged))
            elif self.board[piece] == "wk":
                button = Button(self.frame2, image = self.root.white_king, width = 53, height = 65, compound="center", bg = self.BLACK , relief=FLAT, command = lambda r = r, c = c, colour = "white", clicked = False, kinged = True: self.pieceClicked(r, c, colour, clicked, kinged))
            button.grid(row = r, column = c)


    def makeMove(self, colour, moves, newR, newC, oldR, oldC, Jump): # handles moving a piece to another position and capturing, updates dictionary when move is made

        if colour != self.turn: # makes sure you can only make a move if it is your turn i.e. user can't move a black piece if it is white's turn
            return

        if self.turn == self.computerColour:
            self.computerMove()
                    
        # makes the back and front end moves by updating both the board and the dictionary
        self.board = self.makeMoveBackEnd(colour, moves, newR, newC, oldR, oldC, Jump, self.board)
        self.updateBoardAndUI(newR, newC, oldR, oldC, colour, moves, Jump)

        # alternate colours
        if self.turn == "black":
            self.turn = "white"
        else:
            self.turn = "black"

        # if its computer's turn, let computer play
        if self.turn == self.computerColour:
            self.computerMove()
            
        # change turn accordingly
        if self.turn == "black":
            self.turn = "white"
            self.mustJump = False
        else:
            self.turn = "black"
            self.mustJump = False
            
        # display whose turn it is
        self.turnAlert.config(text = self.turn + "'s turn")   

        # check if a winning move has been made by calling the checkWin() function
        winner = self.checkWin(self.board)
        if winner!= " ":
            return
        draw = self.checkDraw(self.turn)
        if draw:
            return

        # check if there are mandatory jumps to be made 
        self.checkMandatoryJumps()
 
    def checkMandatoryJumps(self): # checks if there are any jump moves to be made and informs the player accordingly by displaying a message

        jump_moves = {} # jump_moves holds the list of all jump moves
        jump_pieces = [] # jump_pieces holds the coordinates of pieces that can make jump moves - this is what is displayed to the user
        self.mustJump = False
 
        for piece in self.board:
            if self.board[piece][0] == self.turn[0]: # make sure to only check for pieces whose turn it is
                if self.board[piece][1] == "k":
                    kinged = True
                else:
                    kinged = False
                Jump, moves = self.checkJump(int(piece[0]),int(piece[1]), self.turn, kinged, self.board)
                if Jump: # if a jump move is possible, add the piece to jump_pieces
                    self.mustJump = True
                    jump_moves[str(piece[0]) + str(piece[1])]= moves
                    
        # displaying the jump label if mandatory jumping is enforced          
        if self.enforceJump:
            if self.mustJump:
                for piece in jump_moves:
                    jump_pieces.append(piece)
                self.jumpAlert.config(text = (f"must jump at ({','.join(map(str, jump_pieces))})"))
            else:
                self.jumpAlert.config(text = "no jump")
    
if __name__ == "__main__":
    game = Tk()
    game.geometry("900x800") # defines window size
    game.title(".・。.・゜✭・.・✫・゜・。. .・。.・゜✭・.・✫・゜・。. play checkers .・。.・゜✭・.・✫・゜・。..・。.・゜✭・.・✫・゜・。.")
    Game(game)
    game.mainloop()
