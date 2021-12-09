import time
import random
import socket
import pickle
import select
from tkinter import *
from functools import partial
from tkinter import messagebox
from time import sleep

# sign variable to decide the turn of which player
sign = 0
my_socket = socket.socket()
done_turn = "need board"
give_turn = "dont know my turn"
player_shape = None

#XY = my_socket.recv(2048).decode()
#int(XY)
#print(XY)
# Creates an empty board
global board
board = [[" " for x in range(3)] for y in range(3)]

backgroundcolor = "#201e20"
clicked = "#e0a96d"
textcolor = "#ddc3a5"

# Check l(O/X) won the match or not
# according to the rules of the game
def winner(b, XorO):
    return ((b[0][0] == XorO and b[0][1] == XorO and b[0][2] == XorO) or
            (b[1][0] == XorO and b[1][1] == XorO and b[1][2] == XorO) or
            (b[2][0] == XorO and b[2][1] == XorO and b[2][2] == XorO) or
            (b[0][0] == XorO and b[1][0] == XorO and b[2][0] == XorO) or
            (b[0][1] == XorO and b[1][1] == XorO and b[2][1] == XorO) or
            (b[0][2] == XorO and b[1][2] == XorO and b[2][2] == XorO) or
            (b[0][0] == XorO and b[1][1] == XorO and b[2][2] == XorO) or
            (b[0][2] == XorO and b[1][1] == XorO and b[2][0] == XorO))


# Configure text on button while playing with another player
def update_board_for_X(i, j, gb, l1, l2, myName):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        #send the board to the server
        boardData=pickle.dumps(board)
        my_socket.send(boardData)
        #קבלה של מערך הלוח ועדכון הלוח
        newBoard = my_socket.recv(2048)
        newBoard = pickle.loads(newBoard)
        print(newBoard)
        sign += 1

        button[i][j].config(text=board[i][j])
    if winner(board, "X"):
        boardData=pickle.dumps([["e" for x in range(3)] for y in range(3)])
        my_socket.send(boardData)
        box = messagebox.showinfo("Winner", myName+", won the match")
        sleep(2)
        gb.destroy()
    elif winner(board, "O"):
        boardData = pickle.dumps([["e" for x in range(3)] for y in range(3)])
        my_socket.send(boardData)
        box = messagebox.showinfo("Winner", "O won the match")
        sleep(2)
        gb.destroy()
    elif (isfull()):
        boardData = pickle.dumps([["e" for x in range(3)] for y in range(3)])
        my_socket.send(boardData)
        box = messagebox.showinfo("Tie Game", "Tie Game")
        sleep(2)
        gb.destroy()



# Check if the player can push the button or not
def isfree(i, j):
    return board[i][j] == " "


# Check if the board is full or not
def isfull():
    flag = True
    for i in board:
        if(i.count(' ') > 0):
            flag = False
    return flag


# Create the GUI of game board for play along with another player
def gameboard(game_board, l1, l2, myName):
    global button
    global c

    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            #if c%2==0:
            get_t = partial(update_board, i, j, game_board, l1, l2, myName)
            #else:
               # get_t=partial(resieve)
            button[i][j] = Button(game_board, bd=5, command=get_t, height=4, width=8, activeforeground=backgroundcolor,
                                  activebackground=clicked, bg=backgroundcolor, fg=textcolor, font=20)
            button[i][j].grid(row=m, column=n)

    game_board.mainloop()



# Initialize the game board to play with another player
def setup(game_board, myName):
    game_board.destroy()
    game_board = Tk()
    game_board.configure(bg=backgroundcolor)
    game_board.title("Tic Tac Toe")
    my_socket.connect(("127.0.0.1", 5555))
    #my_socket.send(give_turn.encode())
    data = my_socket.recv(2048).decode()
    data = int(data)
    if data % 2 == 0:
        player_shape = "O"
    else:
        player_shape = "X"

    print(player_shape)
    time.sleep(0.5)
    if player_shape == "X":
        l1 = Button(game_board, text=str(myName)+" : X", activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor, disabledforeground='gray')
        l1.grid(row=1, column=1)

        l2 = Button(game_board, text="opponent : O",  activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor,  disabledforeground='gray')
        l2.grid(row=2, column=1)
        gameboard(game_board, l1, l2, myName)
    else:
        l1 = Button(game_board, text=str(myName) + " : O", activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor, disabledforeground='gray')
        l1.grid(row=1, column=1)

        l2 = Button(game_board, text="opponent : X", activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor, disabledforeground='gray')
        l2.grid(row=2, column=1)
        gameboard(game_board, l1, l2, myName)



menu = Tk()
menu.geometry("200x200")
menu.title("Tic Tac Toe")
menu.configure(bg=backgroundcolor)
myclick = input('enter name')
wpl = partial(setup, menu, myclick)
B2 = Button(menu, text="play", command=wpl , activeforeground=backgroundcolor,
            activebackground=clicked, bg=backgroundcolor, fg=textcolor,
            width=200, font='summer', bd=5)
B2.pack()
menu.mainloop()









