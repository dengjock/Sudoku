import pygame as pg, requests
from solver import solve, valid
import time # imports

#response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")


pg.init() #initate py.game

font = pg.font.SysFont('Comic Sans MS', 50) # font used for Sudoku


pg.display.set_caption("Sudoku")
userScreen_size = (640, 750)
userScreen = pg.display.set_mode(userScreen_size)
pg.display.flip() # displays the screen size and caption / screen settings for pygame

grid = [
    [0, 7, 0, 0, 0, 0, 0, 3, 2],
    [0, 0, 9, 2, 0, 8, 7, 0, 5],
    [2, 0, 0, 7, 0, 3, 1, 0, 0],
    [0, 0, 1, 0, 6, 0, 3, 7, 0],
    [0, 3, 0, 0, 0, 0, 4, 0, 0],
    [0, 8, 0, 3, 7, 0, 0, 6, 1],
    [6, 0, 0, 5, 0, 1, 0, 8, 0],
    [5, 9, 4, 0, 2, 0, 6, 0, 0],
    [8, 1, 0, 0, 4, 9, 2, 0, 7]
] # predetermined grid used to fill sudoku board

#grid = response.json()['board']

class Grid: # grid class

    # method to initalize the grid class
    def __init__(self, rows, columns, width, height): # method takes in the parameters self, rows, columns, width, and height
        self.rows = rows
        self.columns = columns
        self.squares = [[Square(grid[i][j], i, j, width, height) for j in range(columns)] for i in range(rows)]
        self.width = width
        self.height = height
        self.currentModel = None
        self.selected = None # using the values from the parameters set the variables to their corresponding variables

    def updateGrid(self):
        self.currentModel = [[self.squares[i][j].val for j in range(self.columns)] for i in range(self.rows)] # updates each grid spot

    def valid_num(self, val):
        row, columns = self.selected # set the row and columns of the selected user number
        if self.squares[row][columns].val == 0: # if the grid spot value is 0
            self.squares[row][columns].set_val(val) # set the square at the specific row and column to the user value
            self.updateGrid() # update the grid
            if valid(self.currentModel, val, (row, columns)) and solve(self.currentModel): 
                return True # if the user selected the right number at the specific row and column keep the number and return true since it was a valid number
            else:
                self.squares[row][columns].set_val(0)
                self.squares[row][columns].set_temp(0)
                self.updateGrid()
                return False # if the user value at the specific row and column was wrong reset the specific spot to 0 and rerutrn false since it was the wrong number

    # method to draw the lines of the sudoku board
    def draw(self, userScreen): # takes in parameters self and userScreen
        userScreen.fill(pg.Color("White")) # makes the background of the board white
        pg.draw.rect(userScreen, pg.Color("Black"), pg.Rect(5, 5, userScreen.get_width() - 10, userScreen.get_height() - 120), 5) # draw specific grid spot
        i = 1
        gap = self.width / 9
        xoffset = 5
        yoffset = 5
        while (i * gap) < self.width:
            line_thickness = 3 if i % 3 == 0 else 1
            pg.draw.line(userScreen, pg.Color("Black"), pg.Vector2((i * gap) + xoffset, yoffset), ((i * gap) + xoffset,(self.width + yoffset)), line_thickness)
            pg.draw.line(userScreen, pg.Color("Black"), pg.Vector2(xoffset, (i * gap) + yoffset), pg.Vector2((self.width + xoffset), (i * gap) + yoffset), line_thickness)
            i += 1 # sudoku board is made up of 9 3x3 grids so darken outline for each 3x3 grid
        
        for i in range(self.rows): # iterate through i
            for j in range (self.columns): #iterate through j
                self.squares[i][j].draw(userScreen) # at the specific spot put the updated values

    # method to put numbers in (not method for checking if valid)
    def pencil(self, val): # parameters are self and val
        row, columns = self.selected # gets the row and column that the user clicked
        self.squares[row][columns].set_temp(val) # set the grid spot to the number
    
    # method for selecting the sudoku square grid spot
    def select_square(self, row, columns): # parameters
        for i in range(self.rows): # iterate
            for j in range(self.columns): #iterate
                self.squares[i][j].selected = False # goes through columns and rows and if the sudoku square grid spot is not the selected user spot set to false
        self.squares[row][columns].selected = True # if the sudoku square grid spot is the selected user value set to true
        self.selected = (row, columns) # set the self.selected value to the set row and column spot

    def finished_check(self):
        for i in range(self.rows): # iterate thorugh row
            for j in range(self.columns): # iterate through column
                if self.squares[i][j].val == 0: # if a grid spot is still 0
                    return False # return false because grid is not solved yet
        return True # if no grid spot is still 0 then the grid is solved

    def mouse_click(self, position): # parameters 
        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9 # gap is gap in the board made by the width and the 9 square grids
            x = position[0] / gap # set x to the position at[0] and divide by the gap
            y = position[1] / gap # set y to the position at [1] and divide by the gap
            return (int(y), int(x)) # return the x and y coordinates the user clicked 
        else:
            return None # if the position is less then self at the value

class Square: # declare class
    rows = 9
    columns = 9 # create rows and columns

    def __init__(self, val, row, columns, width ,height):
        self.val = val
        self.temp = 0
        self.row = row
        self.columns = columns
        self.width = width
        self.height = height
        self.selected = False # set variables to the parameters
    
    def draw(self, userScreen):
        gap = self.width / 9
        x = self.columns * gap  
        y = self.row * gap  # create board and make gaps to seperate grid spots

        if self.val == 0 and self.temp != 0:
            text = font.render(str(self.temp), 1, pg.Color("Grey"))
            userScreen.blit(text, (x + 30, y + 20)) # display user number
        elif self.val != 0:
            num_text = font.render(str(self.val), True, pg.Color("Black"))
            userScreen.blit(num_text, (x + 27, y + 20)) # display already found number
        if self.selected: # if the specific grid spot is selected 
            pg.draw.rect(userScreen, pg.Color("Red"), (x + 5, y + 5, gap, gap), 4) # make red outline

    def set_val(self, val):
        self.val = val
   
    def set_temp(self, val):
        self.temp = val

def time_formatter(seconds): # parameter
    second = seconds % 60 # calculate the second
    minute = seconds // 60 # calculate the minutes
    formatted_time = "" + str(minute) + " : " + str(second) # set minutes and seconds to a variable
    return formatted_time # return the time


def redraw(userScreen, board, timePlayed): # parameters
    board.draw(userScreen) # redraw the board
    time_txt = font.render("Time: " + time_formatter(timePlayed), 1, pg.Color("Black")) # show user amount of time
    userScreen.blit(time_txt, ((userScreen.get_width() - 250), 670)) # display the time on the screen
    
def game_over(timeTaken):
    running = True # if true then the user won
    while running: # while game is happening
        pg.draw.rect(userScreen, (112, 128, 144), pg.Rect(120, 210, 400, 150))
        game_over_txt = font.render("GAME OVER", 1, pg.Color("Black")) # set the txt to game over and what color
        time_txt = font.render("You won in " + time_formatter(timeTaken), 1, pg.Color("Black")) # set the txt to how long it took the user to win
        instructions_txt = font.render("(Press 'Enter' to Exit)", 1, pg.Color("Black")) # set the txt to the exit instructions
        userScreen.blit(game_over_txt, (140, 220)) 
        userScreen.blit(time_txt, (210, 280))
        userScreen.blit(instructions_txt, (230, 320)) # draw the texts and display the texts
        pg.display.flip() # allow specific area to update
        for event in pg.event.get(): # iterate 
            if event.type == pg.KEYDOWN: # if event.type == keydown
                if event.key == pg.K_RETURN: # if event.key = k_return
                    running = False # stops displaying message
    return False # stops displaying texts

def main():
    running = True 
    key = None
    start_time = time.time()
    board = Grid(9, 9, 630, 630) 

    # game loop
    while running:
        # calc playing time
        timePlayed = round(time.time() - start_time)
        # handle external events
        for event in pg.event.get():
            # to quit program
            if event.type == pg.QUIT:
                running = False
            # test for key press events
            if event.type == pg.KEYDOWN:
                # each number key
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                # operations when enter key is pressed
                if event.key == pg.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        # if guess is incorrect, add to wrong
                        if not board.valid_num(board.squares[i][j].temp):
                            #wrong += 1
                            key = None
                        # check if board is complete after every entry
                        if board.finished_check():
                            running = game_over(timePlayed)
            # test for mouse clicks
            if event.type == pg.MOUSEBUTTONDOWN:
                position = pg.mouse.get_pos()
                clicked = board.mouse_click(position)
                if clicked != None:
                    board.select_square(clicked[0], clicked[1])
                    key = None
        # pencil in the desired number
        if board.selected and key != None:
            board.pencil(key)
        # redraw board after changes
        #redraw(userScreen, board, wrong, timePlayed)
        redraw(userScreen, board, timePlayed)
        pg.display.update()

# run the program
main()
pg.quit()
