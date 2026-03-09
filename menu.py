from tkinter import *
import random
BLACK = "#596070"
class Menu:
    def __init__(self, root):

        # window formatting
        self.root = root
        self.root.configure(background = BLACK)
        self.root.title(".・。.・゜✭・.・✫・゜ checkers ・゜・。.・゜✭・.・✫・゜・。.")
        self.root.geometry("800x800")        

        # title label that says 'welcome to checkers'
        self.root.titleLabel = Label(self.root, bg = BLACK, text = ("welcome to checkers!!"), fg = "white", font = ("Fixedsys",25), anchor = CENTER)
        self.root.titleLabel.pack()

        # one player and two player buttons the user can press
        self.one_player_button = Button(self.root, bg = BLACK, text = ("one player"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = lambda mode = "one":self.clearFirstScreen(mode))
        self.one_player_button.pack(pady = 10)
        self.two_player_button = Button(self.root, bg = BLACK, text = ("two player"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = lambda mode = "two":self.clearFirstScreen(mode))
        self.two_player_button.pack(pady = 10)

        self.poem = self.pickPoem()       
        self.root.poemLabel = Label(self.root, bg = BLACK, text = self.poem, fg = "white", font = ("Fixedsys",15),padx=5, pady=5, anchor = CENTER)
        self.root.poemLabel.pack()

    # clears the one and two player buttons to make space to diplay the option buttons
    def clearFirstScreen(self, mode):
        self.root.titleLabel.destroy()
        self.one_player_button.destroy()
        self.two_player_button.destroy()
        self.root.poemLabel.destroy()
        self.options(mode)

    # clears the options buttons to allow the user to play the one or two player game
    def clearSecondScreen(self, mode):
        self.root.titleLabel.destroy()
        self.turnLabel.destroy()
        self.turnButton.destroy()
        self.jumpLabel.destroy()
        self.jumpButton.destroy()
        self.confirmButton.destroy()

        if mode == "one":
            self.difficultyLabel.destroy()
            self.difficultyButton.destroy()
        
    def options(self,mode):
        
        # displays appropriate labels and buttons and defines the relevant variables - each option has a label, button and variable
        self.root.titleLabel = Label(self.root, bg = BLACK, text = ("select your preferences..."), fg = "white", font = ("Fixedsys",25), anchor = CENTER)
        self.root.titleLabel.pack()        
        self.turnLabel = Label(self.root, bg = BLACK, text = ("which colour goes first?"), fg = "white", font = ("Fixedsys",15), anchor = CENTER)
        self.turnLabel.pack()
        self.turn = "black"
        self.turnButton = Button(self.root, bg = BLACK, text = ("black"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = self.changeTurn)
        self.turnButton.pack(pady = 10)
        self.jumpLabel = Label(self.root, bg = BLACK, text = ("force jumps?"), fg = "white", font = ("Fixedsys",15), anchor = CENTER)
        self.jumpLabel.pack()
        self.enforceJump = True
        self.jumpButton = Button(self.root, bg = BLACK, text = ("yes"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = self.changeJump)
        self.jumpButton.pack(pady = 10)        

        # if it is a one player game, the user can select a difficulty level
        if mode == "one":
            self.difficultyLabel = Label(self.root, bg = BLACK, text = ("choose a difficulty level:"), fg = "white", font = ("Fixedsys",15), anchor = CENTER)
            self.difficultyLabel.pack()
            self.difficulty = "easy"
            self.difficultyButton = Button(self.root, bg = BLACK, text = ("easy"), fg = "white", font = ("Fixedsys",20), anchor = CENTER,  command = self.changeDifficulty)
            self.difficultyButton.pack(pady = 10)
            self.confirmButton = Button(self.root, bg = BLACK, text = ("confirm"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = lambda mode=mode: self.startGame(self.difficulty, self.turn, self.enforceJump, mode))
            self.confirmButton.pack(pady = 10)
        else:
            self.confirmButton = Button(self.root, bg = BLACK, text = ("confirm"), fg = "white", font = ("Fixedsys",20), anchor = CENTER, command = lambda mode=mode: self.startGame(None, self.turn, self.enforceJump, mode))
            self.confirmButton.pack(pady = 10)

    # allows the options button to change when the user clicks them to select their preferences
    def changeTurn(self):
        if self.turn == "black":
            self.turnButton.configure(text="white")
            self.turn = "white"
        elif self.turn == "white":
            self.turnButton.configure(text="black")
            self.turn = "black"
    # allows the options button to change when the user clicks them to select their preferences
    def changeJump(self):
        if self.enforceJump == True:
            self.jumpButton.configure(text="no")
            self.enforceJump = False
        elif self.enforceJump == False:
            self.jumpButton.configure(text="yes")
            self.enforceJump = True

    # allows the options button to change when the user clicks them to select their preferences
    def changeDifficulty(self):
        if self.difficulty == "easy":
            self.difficultyButton.configure(text="medium")
            self.difficulty = "medium"
        elif self.difficulty == "medium":
            self.difficultyButton.configure(text="hard")
            self.difficulty = "hard"
        elif self.difficulty == "hard":
            self.difficultyButton.configure(text="easy")
            self.difficulty = "easy"
            
    # runs the one or two player game - this only happens after the options have been selected
    def startGame(self,difficulty, turn, enforceJump, mode):
        self.clearSecondScreen(mode)
        if mode == "two": # if its a two player game
            import twoPlayerFromMenu
            twoPlayerFromMenu.Game(self.root, turn, enforceJump)
        else:
            import onePlayerFromMenuFinal
            onePlayerFromMenuFinal.Game(self.root, difficulty, turn, enforceJump)
            
    def pickPoem(self):
        poems = [
    """Checkers ain't chess, but don't be fooled,
You gotta think, you gotta move.
Hop that piece, stack that crown,
One wrong step? You're going down.

Double jump, yeah, that’s the flex,
Dodge the traps, what comes next?
Life’s a board, black and red,
Win or lose? It’s in your head.

King me up, now I’m free,
Moving how I wanna be.
Play it smart, take your time,
Just like life—it's all a climb.""",

    """Life’s a board of black and red,
A game of choices, move ahead.
Step too quick, you risk the fall,
Step too slow, you lose it all.

Some start forward, some stay back,
Some get lucky, dodge attack.
Pieces move, but not too free—
Rules decide what they can be.

A single step, a careful wait,
A daring jump—defying fate.
A king is made, but at a cost,
For every win, a piece is lost.

We chase the crown, we plot, we scheme,
We learn the game, we build the dream.
But in the end, when play is through,
The board resets—the same for you.""",

    """The Battle of the Squares

Upon the board, the kingdom’s might,
Two armies clash in fierce delight.
The black and white, both bold and true,
In silent war, the pieces flew.

The pawns advance with careful grace,
Across the board, they seek their place.
The kings arise with crowns of gold,
Their battle fierce, a knight’s bold dream.

The royal court, the knights and lords,
By fate’s own hand, they’re moved by swords.
The colors clash, the pieces fall,
And in the end, one reigns, the call."""
]

        poem = random.choice(poems)
        return poem
 
if __name__ == "__main__":
    root = Tk()
    Menu(root)
    root.mainloop()
