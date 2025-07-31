import tkinter as tk
from tkinter import messagebox
import copy

# --- Constants ---
PLAYER = 'X'
AI = 'O'
EMPTY = ' '

# --- Initialize the game board ---
board = [[EMPTY for _ in range(3)] for _ in range(3)]

# --- GUI setup ---
root = tk.Tk()
root.title("Tic-Tac-Toe with AI")

buttons = [[None for _ in range(3)] for _ in range(3)]

# --- Check for winner ---
def check_winner(b):
    for row in b:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]

    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col] != EMPTY:
            return b[0][col]

    if b[0][0] == b[1][1] == b[2][2] != EMPTY:
        return b[0][0]

    if b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return b[0][2]

    return None

# --- Check for full board ---
def is_full(b):
    for row in b:
        if EMPTY in row:
            return False
    return True

# --- Minimax Algorithm ---
def minimax(b, depth, is_maximizing):
    winner = check_winner(b)
    if winner == AI:
        return 1
    elif winner == PLAYER:
        return -1
    elif is_full(b):
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = AI
                    score = minimax(b, depth + 1, False)
                    b[i][j] = EMPTY
                    best = max(best, score)
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = PLAYER
                    score = minimax(b, depth + 1, True)
                    b[i][j] = EMPTY
                    best = min(best, score)
        return best

# --- AI Move ---
def ai_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, 0, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        i, j = move
        board[i][j] = AI
        buttons[i][j].config(text=AI, state=tk.DISABLED)
        check_game_over()

# --- Check game over ---
def check_game_over():
    winner = check_winner(board)
    if winner:
        messagebox.showinfo("Game Over", f"{winner} wins!")
        disable_all_buttons()
    elif is_full(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        disable_all_buttons()

# --- Disable all buttons ---
def disable_all_buttons():
    for row in buttons:
        for btn in row:
            btn.config(state=tk.DISABLED)

# --- On click by player ---
def on_click(i, j):
    if board[i][j] == EMPTY:
        board[i][j] = PLAYER
        buttons[i][j].config(text=PLAYER, state=tk.DISABLED)
        check_game_over()
        if not check_winner(board) and not is_full(board):
            root.after(300, ai_move)

# --- Reset game ---
def reset_game():
    global board
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=EMPTY, state=tk.NORMAL)

# --- Build GUI buttons ---
for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text=EMPTY, font=('Arial', 36), width=5, height=2,
                        command=lambda i=i, j=j: on_click(i, j))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

reset_btn = tk.Button(root, text="Reset Game", font=('Arial', 12), command=reset_game)
reset_btn.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()