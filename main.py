import customtkinter as ctk
import tkinter as tk
import numpy as np
from functools import partial

window = ctk.CTk()
window.geometry("600x668")
window.title("")


main_frame = ctk.CTkFrame(window)

# frame grid
for i in list(range(0, 9)):
    main_frame.rowconfigure(i, weight=1, uniform="a")

for i in list(range(0, 9)):
    main_frame.columnconfigure(i, weight=1, uniform="a")


def character_limit(v):
    if len(v.get()) > 0:
        v.set(v.get()[-1])


cells = []
data = np.zeros((9, 9), dtype=np.uint8)


def is_valid(board, row, col, num):
    # Check if 'num' is not in current row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check if 'num' is not in current 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True


def solve_sudoku(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty
    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False


def find_empty_cell(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i, j
    return None


def callback(i, j, ev):
    global data
    if len(ev.char) == 1 and str(ev.char).isdigit():
        data[i][j] = np.uint8(ev.char)
        for p in range(0, 9):
            for q in range(0, 9):
                for cell in data[p]:
                    pass
                    # print(cell)
    else:
        data[i][j] = np.uint8(0)


for i in range(0, 9):
    for j in range(0, 9):
        sv = tk.StringVar()
        entry = tk.Entry(main_frame, textvariable=sv, justify="center")
        callback_prepared = partial(callback, i, j)
        entry.bind('<KeyRelease>', callback_prepared)
        entry.grid(row=j, column=i, sticky="nsew")
        cells.append(entry)


main_frame.pack(expand=True, fill="both")


def solve():
    global data
    calc2 = data.copy()

    solve_sudoku(calc2)
    refresh(calc2)


def clear():
    global data
    refresh(data)



def clear_all():
    global data
    global cells
    data = np.zeros((9, 9), dtype=np.uint8)
    refresh(data)


def refresh(matrix):
    global cells
    for i in range(0, 9):
        for j in range(0, 9):
            e = cells[i * 9 + j]
            e.delete(0, tk.END)
            if matrix[i, j] > 0:
                e.insert(0, str(matrix[i, j]))


check_btn_0 = ctk.CTkButton(window, text="check for solution", command=solve)
check_btn_1 = ctk.CTkButton(window, text="undo", command=clear)
check_btn_2 = ctk.CTkButton(window, text="clear everything", command=clear_all)

check_btn_0.pack(side="left", pady=20, expand=True)
check_btn_2.pack(side="right", pady=20, expand=True)
check_btn_1.pack(side="right", pady=20, expand=True)


window.mainloop()
