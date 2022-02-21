import time
import random
import socket
import pickle
import select
from tkinter import *
from functools import partial
from tkinter import messagebox
from time import sleep

sign = 0# sign variable to decide the turn of which player

my_socket = socket.socket()#הסוקט

player_shape = None#משתנה היחזיק את סוג השחקן


#יצירת לוח גלובלי,זה לוח המשחק
global board
board = [[" " for x in range(3)] for y in range(3)]

#צבעים לממשק המשתמש
backgroundcolor = "#201e20"
clicked = "#e0a96d"
textcolor = "#ddc3a5"

#פעולה מקבלת לוח של 3 על 3 וסוג משתמש איקס או עיגול
#הפעולה מחזירה אמת אם יש ניצחון ושקר אם לא
def winner(b, XorO):
    return ((b[0][0] == XorO and b[0][1] == XorO and b[0][2] == XorO) or
            (b[1][0] == XorO and b[1][1] == XorO and b[1][2] == XorO) or
            (b[2][0] == XorO and b[2][1] == XorO and b[2][2] == XorO) or
            (b[0][0] == XorO and b[1][0] == XorO and b[2][0] == XorO) or
            (b[0][1] == XorO and b[1][1] == XorO and b[2][1] == XorO) or
            (b[0][2] == XorO and b[1][2] == XorO and b[2][2] == XorO) or
            (b[0][0] == XorO and b[1][1] == XorO and b[2][2] == XorO) or
            (b[0][2] == XorO and b[1][1] == XorO and b[2][0] == XorO))

#הפעולה מקבלת לוח משחק
#הפעולה מתאימה את הטקסט של הכפתורים לטקסט שעל הלוח שהתקבל בנוסף משווה את לוח המשחק ללוח שהתקבל
def print_board( newBoard):
    for i in range(3):
        for j in range(3):
            button[i][j].config(text=newBoard[i][j])
            board[i][j] = newBoard[i][j]


#הפעולה אחראית לקבלת לוח מהמשתמש השני ולבדיקת מנצח או שיוויון
def update_board_recv(gb, l1, l2, myName, PS):
    newBoard = my_socket.recv(2048)
    newBoard = pickle.loads(newBoard)
    print('recv ',newBoard)

    print_board(newBoard)
    if winner(board, "X"):
        boardData = pickle.dumps([["e" for x in range(3)] for y in range(3)])
        my_socket.send(boardData)
        box = messagebox.showinfo("Winner", myName + ", won the match")
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



#הפעולה אחראית לשליחת לוח למשתמש השני ולבדיקת מנצח או שיוויון
def update_board_send(i, j, gb, l1, l2, myName, PS):
    global sign
    if board[i][j] == ' ':
        if PS == 'X':
            if sign % 2 == 0:
                l1.config(state=DISABLED)
                l2.config(state=ACTIVE)
                board[i][j] = "X"
            else:
                l2.config(state=DISABLED)
                l1.config(state=ACTIVE)
                board[i][j] = "X"
        if PS == 'O':
            if sign % 2 == 0:
                l1.config(state=DISABLED)
                l2.config(state=ACTIVE)
                board[i][j] = "O"
            else:
                l2.config(state=DISABLED)
                l1.config(state=ACTIVE)
                board[i][j] = "O"
        boardData = pickle.dumps(board)
        my_socket.send(boardData)
        sign += 1
        print("send ",board)
        print_board(board)
    if winner(board, "X"):
        boardData = pickle.dumps([["e" for x in range(3)] for y in range(3)])
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
    gb.after(500, lambda: update_board_recv(gb, l1, l2, myName, PS))



#בודק אם מקום בלוח חופשי
def isfree(i, j):
    return board[i][j] == " "

#בודק אם הלוח מלא
def isfull():
    flag = True
    for i in board:
        if(i.count(' ') > 0):
            flag = False
    return flag


#פעולה היוצרת את הלוח בצורה של כפתורים, הפעולה אחראית על סידור הכפתורים ושליחה לפעולה הבאה בהתאם לסוג השחקן
def gameboard(game_board, l1, l2, myName, PS):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(update_board_send, i, j, game_board, l1, l2, myName, PS)
            button[i][j] = Button(game_board, bd=5, command=get_t, height=4, width=8, activeforeground=backgroundcolor,
                                  activebackground=clicked, bg=backgroundcolor, fg=textcolor, font=20)
            button[i][j].grid(row=m, column=n)
    if PS == "O":
        demo = partial(update_board_recv, game_board, l1, l2, myName)
        game_board.after(500, lambda: update_board_recv(game_board, l1, l2, myName, PS))
    game_board.mainloop()



#הפעולה מחברת את השחקן לשרת ומקבלת מהשרת אינדיקציה לסוג השחקן איקס או עיגול
def setup(game_board, myName):
    game_board.destroy()
    game_board = Tk()
    game_board.configure(bg=backgroundcolor)
    game_board.title("Tic Tac Toe")
    my_socket.connect(("127.0.0.1", 5555))
    data = my_socket.recv(2048).decode()
    data = int(data)
    if data % 2 == 0:
        player_shape = "O"
    else:
        player_shape = "X"
    game_board.after(10)
    print(player_shape)
    time.sleep(0.5)
    if player_shape == "X":
        l1 = Button(game_board, text=str(myName)+" : X", activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor, disabledforeground='gray')
        l1.grid(row=1, column=1)

        l2 = Button(game_board, text="opponent : O",  activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor,  disabledforeground='gray')
        l2.grid(row=2, column=1)
        gameboard(game_board, l1, l2, myName, player_shape)
    else:
        l1 = Button(game_board, text=str(myName) + " : O", activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor, disabledforeground='gray')
        l1.grid(row=1, column=1)

        l2 = Button(game_board, text="opponent : X", activeforeground=backgroundcolor,
                    activebackground=clicked, bg=backgroundcolor, fg=textcolor, disabledforeground='gray')
        l2.grid(row=2, column=1)
        gameboard(game_board, l1, l2, myName, player_shape)



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







