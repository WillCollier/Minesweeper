import numpy as np
from tkinter import *
import random, time
from itertools import product


def placeBomb(grid, ngrid, nBombs):
    """
    Places nBombs of bombs onto the true board
    Use random.sample to randomly sample each coord on the grid, instead of randint and have
    to check if a position has been sampled multiple times
    :param grid: game board
    :param ngrid: length of a game board axis
    :param nBombs: number of bombs
    :return:
    """
    coord = list(product(range(ngrid), range(ngrid)))
    for bombs in random.sample(coord, nBombs):
        grid[bombs[0]][bombs[1]] += 9
    return grid


def get_val(x, y, grid):
    """
    Returns the value of a given square on the game board
    :param x: x coord on grid
    :param y: y coord on grid
    :param grid: game board
    :return:
    """
    return grid[x, y]


def updateValues(x, y, grid, ngrid):
    """
    Update the values in the game board surrounding a bomb to the nummber of bombs the square touches
    :param x: x coord on game_board
    :param y: y coord on game_board
    :param grid: the gameboard
    :param ngrid: the length of each axis
    :return: the ammended grid
    """
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (x + i >= 0) and (x + i <= ngrid - 1) and (y + j >= 0) and (y + j <= ngrid - 1):
                if grid[x + i, y + j] != 9:
                    grid[x + i, y + j] += 1

    return grid


def ZeroProcedure(r, c, grid, ngrid, btns):
    """
    Open squares surrounding a zero value
    """
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (r + i >= 0) and (r + i <= ngrid - 1) and (c + j >= 0) and (c + j <= ngrid - 1):
                val = get_val(i + r, j + c, grid)
                res = str(val)
                btns[(i + r) * ngrid + (j + c)].configure(text=res)
    return


def clicked(i, j, b, nBombs, ngrid, btns, lbl, startTime):
    """
    On a left click, replace button text with value on game value grid
    If a bomb, uncover the game board and state that the player lost
    """
    val = get_val(i, j, b)
    if val == 9:
        res = '⦻'
        btns[i * ngrid + j].configure(text=res)

        lbl.configure(text="You lost!")
        for i in range(ngrid):
            for j in range(ngrid):
                val = get_val(i, j, b)
                if val == 9:
                    res = '⦻'
                    btns[i * ngrid + j].configure(text=res)
                else:
                    res = str(val)
                    btns[i * ngrid + j].configure(text=res)

    res = str(val)
    btns[i * ngrid + j].configure(text=res)

    if val == 0:
        ZeroProcedure(i, j, b, ngrid, btns)

    counter = 0
    for k in range(len(btns)):
        if btns[k].cget('text') == " ":
            counter += 1
    if counter == nBombs:
        lbl.configure(text="You win! Time Taken: {} seconds".format(time.time()-startTime))
        for i in range(ngrid):
            for j in range(ngrid):
                val = get_val(i, j, b)
                if val == 9:
                    res = '⦻'
                    btns[i * ngrid + j].configure(text=res)
                else:
                    res = str(val)
                    btns[i * ngrid + j].configure(text=res)


def right_clicked(i, j, b, nBombs, ngrid, btns, lbl, startTime):
    """
    On a right click, replace button text with a flag to cover potential bombs
    If current value a flag, replace with blank
    """
    if btns[i * ngrid + j].cget('text') == " ":
        res = '⚐'
        btns[i * ngrid + j].configure(text=res)
    else:
        res = ' '
        btns[i * ngrid + j].configure(text=res)
    # button.configure(text=res)
    counter = 0
    for k in range(len(btns)):
        if (btns[k].cget('text') == " ") or ((btns[k].cget('text') == "⚐") and (get_val(i, j, b) == 9)):
            counter += 1
    if counter == nBombs:
        lbl.configure(text="You win! Time Taken: {} seconds".format(time.time()-startTime))




class grid_setup(object):
    """
    Using the defined number of bombs and the size of the grid
    Places the bombs into the game board (b)
    Maximise use of numpy arrays by utilising integers instead of strings
    """

    def __init__(self, ngrid, nBombs):
        self.ngrid = ngrid
        self.nBombs = nBombs

    def start_game(self):
        # The solution grid
        b = np.zeros((self.ngrid, self.ngrid), dtype=int)
        # print(b)
        # for n in range(0, nBombs):
        b = placeBomb(b, self.ngrid, self.nBombs)

        coords = np.where(b == 9)
        coord = np.vstack((coords[0], coords[1])).T
        for i in coord:
            b = updateValues(i[0], i[1], b, self.ngrid)

        self.game_board = b


class game_board(object):
    """
    Takes the premade game_board and creates the user interface

    """
    def __init__(self, board, nBombs, ngrid):
        self.game_board = board
        self.nBombs = nBombs
        self.ngrid = ngrid

    def make_window(self):
        """
        Create the game board, maybe make the gemoetry change dependent on gridsize?
        """
        window = Tk()
        window.title("Minesweeper")
        window.geometry('750x500')
        self.lbl = Label(window, text="Begin playing Minsweeper")
        self.lbl.grid(column=0, row=0)

        self.window = window

    def make_buttons(self):

        """
        Place buttons into the game window
        """
        self.start_time = time.time()
        self.btns = []
        for i in range(self.ngrid):
            for j in range(self.ngrid):
                frame = Frame(self.window, width=40, height=40)  # their units in pixels
                button = Button(frame, text=" ", command=lambda i=i, j=j, b=self.game_board,
                                                                nBombs=self.nBombs, ngrid=self.ngrid, btns=self.btns,
                                                                lbl=self.lbl, startTime=self.start_time:
                                                                clicked(i, j, b, nBombs, ngrid, btns, lbl, startTime))

                button.bind("<Button-3>", lambda e, i=i, j=j, b=self.game_board, nBombs=self.nBombs, ngrid=self.ngrid,
                                                 btns=self.btns, lbl=self.lbl, startTime = self.start_time:
                                                right_clicked(i, j, b, nBombs, ngrid, btns, lbl, startTime))
                self.btns.append(button)

                frame.grid_propagate(False)  # disables resizing of frame
                frame.columnconfigure(0, weight=1)  # enables button to fill frame
                frame.rowconfigure(0, weight=1)  # any positive number would do the trick

                frame.grid(row=i + 2, column=j + 1)  # put frame where the button should be
                button.grid(sticky="wens")  # makes the button expand


    def play(self):
        self.window.mainloop()


set_up_grid = grid_setup(ngrid=9, nBombs=10)
set_up_grid.start_game()

game = game_board(set_up_grid.game_board, set_up_grid.nBombs, set_up_grid.ngrid)
game.make_window()
game.make_buttons()
game.play()
