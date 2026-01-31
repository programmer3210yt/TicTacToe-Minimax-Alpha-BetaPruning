import tkinter as tk
from tkinter import messagebox

board = [[" " for _ in range(3)] for _ in range(3)]
AI = "O"
HUMAN = "X"

minimax_calls = 0
alphabeta_calls = 0
minimax_total = 0
alphabeta_total = 0

current_turn = HUMAN
mode = "minimax"
ai_first = False

def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != " ":
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] != " ":
            return b[0][i]
    if b[0][0] == b[1][1] == b[2][2] != " ":
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != " ":
        return b[0][2]
    return None

def is_full(b):
    for row in b:
        for cell in row:
            if cell == " ":
                return False
    return True

def evaluate(b):
    winner = check_winner(b)
    if winner == AI:
        return +1
    elif winner == HUMAN:
        return -1
    else:
        return 0

def minimax(b, is_maximizing):
    global minimax_calls
    minimax_calls += 1
    score = evaluate(b)
    if score != 0:
        return score
    if is_full(b):
        return 0
    if is_maximizing:
        best = -999
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = AI
                    val = minimax(b, False)
                    b[i][j] = " "
                    if val > best:
                        best = val
        return best
    else:
        best = 999
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = HUMAN
                    val = minimax(b, True)
                    b[i][j] = " "
                    if val < best:
                        best = val
        return best

def best_move_minimax():
    global minimax_calls, minimax_total
    minimax_calls = 0
    best_val = -999
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = AI
                val = minimax(board, False)
                board[i][j] = " "
                if val > best_val:
                    best_val = val
                    move = (i, j)
    minimax_total += minimax_calls
    return move, minimax_calls

def alphabeta(b, is_maximizing, alpha, beta):
    global alphabeta_calls
    alphabeta_calls += 1
    score = evaluate(b)
    if score != 0:
        return score
    if is_full(b):
        return 0
    if is_maximizing:
        value = -999
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = AI
                    value = max(value, alphabeta(b, False, alpha, beta))
                    b[i][j] = " "
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        return value
        return value
    else:
        value = 999
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = HUMAN
                    value = min(value, alphabeta(b, True, alpha, beta))
                    b[i][j] = " "
                    beta = min(beta, value)
                    if alpha >= beta:
                        return value
        return value

def best_move_alphabeta():
    global alphabeta_calls, alphabeta_total
    alphabeta_calls = 0
    best_val = -999
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = AI
                val = alphabeta(board, False, -999, 999)
                board[i][j] = " "
                if val > best_val:
                    best_val = val
                    move = (i, j)
    alphabeta_total += alphabeta_calls
    return move, alphabeta_calls




# GUI




root = tk.Tk()
root.title("Tic-Tac-Toe: Minimax vs Alpha-Beta")

buttons = [[None for _ in range(3)] for _ in range(3)]
status_label = tk.Label(root, text="Mode: Human vs AI (Minimax). X to move", font=("Arial", 12))
status_label.grid(row=0, column=0, columnspan=3, pady=(6,0))
info_label = tk.Label(root, text="Nodes this move: 0    Total nodes (Minimax/Alpha-Beta): 0 / 0", font=("Arial", 10))
info_label.grid(row=1, column=0, columnspan=3, pady=(0,8))

def on_cell_click(r, c):
    global current_turn
    if board[r][c] != " ":
        return
    if mode == "hvh":
        board[r][c] = current_turn
        buttons[r][c]['text'] = current_turn
        winner = check_winner(board)
        if winner or is_full(board):
            end_game(winner)
            return
        current_turn = AI if current_turn == HUMAN else HUMAN
        status_label.config(text=f"Player {current_turn} to move")
    else:
        if current_turn != HUMAN:
            return
        board[r][c] = HUMAN
        buttons[r][c]['text'] = HUMAN
        winner = check_winner(board)
        if winner or is_full(board):
            end_game(winner)
            return
        current_turn = AI
        status_label.config(text="AI is thinking...")
        root.update_idletasks()
        ai_move()

def ai_move():
    global current_turn
    if mode == "minimax":
        (r, c), calls = best_move_minimax()
    else:
        (r, c), calls = best_move_alphabeta()
    if r == -1:
        return
    board[r][c] = AI
    buttons[r][c]['text'] = AI
    info_label.config(text=f"Nodes this move: {calls}    Total nodes (Minimax/Alpha-Beta): {minimax_total} / {alphabeta_total}")
    winner = check_winner(board)
    if winner or is_full(board):
        end_game(winner)
        return
    current_turn = HUMAN
    status_label.config(text="Your turn (X)")

def end_game(winner):
    if winner:
        msg = f"Winner: {winner}"
    else:
        msg = "It's a draw!"
    status_label.config(text=msg)
    messagebox.showinfo("Game Over", msg)
    info_label.config(text=f"Nodes this move: 0    Total nodes (Minimax/Alpha-Beta): {minimax_total} / {alphabeta_total}")

for i in range(3):
    for j in range(3):
        b = tk.Button(root, text=" ", width=6, height=3, font=("Helvetica", 20),
                      command=lambda r=i, c=j: on_cell_click(r, c))
        b.grid(row=2 + i, column=j, padx=2, pady=2)
        buttons[i][j] = b

control_frame = tk.Frame(root)
control_frame.grid(row=5, column=0, columnspan=3, pady=(10,6))

mode_var = tk.StringVar(value="minimax")

def set_mode():
    global mode
    mode = mode_var.get()
    if mode == "hvh":
        status_label.config(text="Mode: Human vs Human. X to move")
    elif mode == "minimax":
        status_label.config(text="Mode: Human vs AI (Minimax). X to move")
    else:
        status_label.config(text="Mode: Human vs AI (Alpha-Beta). X to move")
    reset_board()

tk.Radiobutton(control_frame, text="Human vs Human", variable=mode_var, value="hvh", command=set_mode).grid(row=0, column=0)
tk.Radiobutton(control_frame, text="Human vs AI (Minimax)", variable=mode_var, value="minimax", command=set_mode).grid(row=0, column=1)
tk.Radiobutton(control_frame, text="Human vs AI (Alpha-Beta)", variable=mode_var, value="alphabeta", command=set_mode).grid(row=0, column=2)

first_var = tk.StringVar(value="human")

def set_first():
    global ai_first
    ai_first = (first_var.get() == "ai")
    reset_board()

tk.Radiobutton(control_frame, text="Human first (X)", variable=first_var, value="human", command=set_first).grid(row=1, column=0)
tk.Radiobutton(control_frame, text="AI first (O)", variable=first_var, value="ai", command=set_first).grid(row=1, column=1)

def reset_board():
    global board, current_turn, minimax_calls, alphabeta_calls
    board = [[" " for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = " "
    current_turn = HUMAN
    minimax_calls = 0
    alphabeta_calls = 0
    mode_selected = mode_var.get()
    first_selected = first_var.get()
    if mode_selected == "hvh":
        status_label.config(text="Mode: Human vs Human. X to move")
    elif mode_selected == "minimax":
        status_label.config(text="Mode: Human vs AI (Minimax). X to move")
    else:
        status_label.config(text="Mode: Human vs AI (Alpha-Beta). X to move")
    if first_selected == "ai":
        current_turn = AI
        status_label.config(text="AI is thinking...")
        root.update_idletasks()
        if mode_var.get() == "minimax":
            (r, c), calls = best_move_minimax()
        elif mode_var.get() == "alphabeta":
            (r, c), calls = best_move_alphabeta()
        else:
            return
        if r != -1:
            board[r][c] = AI
            buttons[r][c]['text'] = AI
            info_label.config(text=f"Nodes this move: {calls}    Total nodes (Minimax/Alpha-Beta): {minimax_total} / {alphabeta_total}")
        current_turn = HUMAN
        status_label.config(text="Your turn (X)")

reset_btn = tk.Button(control_frame, text="New Game / Reset", command=reset_board)
reset_btn.grid(row=1, column=2, padx=8)

def clear_totals():
    global minimax_total, alphabeta_total
    minimax_total = 0
    alphabeta_total = 0
    info_label.config(text=f"Nodes this move: 0    Total nodes (Minimax/Alpha-Beta): {minimax_total} / {alphabeta_total}")

clear_btn = tk.Button(control_frame, text="Clear Totals", command=clear_totals)
clear_btn.grid(row=1, column=3, padx=8)

set_mode()
set_first()
root.mainloop()
