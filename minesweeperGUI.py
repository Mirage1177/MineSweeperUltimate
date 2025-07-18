import random
import tkinter as tk
from tkinter import messagebox

def inita_board(n, m, k):
    board = [[0] * (m + 2) for _ in range(n + 2)]
    mines = set()
    while len(mines) < k:
        x = random.randint(1, n)
        y = random.randint(1, m)
        if (x, y) not in mines:
            mines.add((x, y))
            board[x][y] = '*'
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if board[i][j] != '*':
                count = 0
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx != 0 or dy != 0:
                            if board[i + dx][j + dy] == '*':
                                count += 1
                board[i][j] = count
    return board, mines

def fill(x, y, n, m, board, showed):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in showed:
            continue
        showed.add((cx, cy))
        if board[cx][cy] == 0:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = cx + dx, cy + dy
                    if 1 <= nx <= n and 1 <= ny <= m and (nx, ny) not in showed:
                        stack.append((nx, ny))

class MinesweeperGUI:
    def __init__(self, master, n, m, k):
        self.master = master
        self.master.title("MineSweeper")
        self.n = n
        self.m = m
        self.k = k
        self.board, self.mines = inita_board(n, m, k)
        self.showed = set()
        self.flagged = set()
        self.moves = 0
        self.game_over = False

        self.buttons = {}
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack()

        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                button = tk.Button(self.grid_frame, width=3, height=1,
                                   command=lambda r=i, c=j: self.on_left_click(r, c))
                button.bind("<Button-3>", lambda event, r=i, c=j: self.on_right_click(r, c))
                button.grid(row=i, column=j)
                self.buttons[(i, j)] = button

        self.restart_button = tk.Button(self.master, text="New Game", command=self.restart_game)
        self.restart_button.pack(pady=10)

    def update_display(self):
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                btn = self.buttons[(i, j)]
                btn.config(state=tk.NORMAL)
                if (i, j) in self.flagged:
                    btn.config(text="F", bg="orange")
                elif (i, j) not in self.showed:
                    btn.config(text="", bg="lightgray")
                elif self.board[i][j] == '*':
                    btn.config(text="*", bg="red")
                else:
                    val = self.board[i][j]
                    btn.config(text=str(val) if val != 0 else "", bg="lightgreen", fg=self.get_number_color(val))
                    if val == 0:
                        btn.config(relief=tk.SUNKEN)
        if self.game_over:
            for btn in self.buttons.values():
                btn.config(state=tk.DISABLED)

    def get_number_color(self, val):
        colors = {
            1: "blue", 2: "green", 3: "red", 4: "purple",
            5: "maroon", 6: "turquoise", 7: "black", 8: "gray"
        }
        return colors.get(val, "black")

    def on_left_click(self, r, c):
        if self.game_over or (r, c) in self.showed:
            return
        if (r, c) in self.flagged:
            messagebox.showinfo("MineSweeper", "Unflag before trying to reveal.")
            return
        if (r, c) in self.mines:
            self.showed.update(self.mines)
            self.update_display()
            messagebox.showinfo("MineSweeper", "You hit a mine! BOOM!!!\n\t...GAME OVER...")
            self.game_over = True
            return
        fill(r, c, self.n, self.m, self.board, self.showed)
        self.moves += 1
        self.update_display()
        self.check_win()

    def on_right_click(self, r, c):
        if self.game_over or (r, c) in self.showed:
            messagebox.showinfo("MineSweeper", "Cannot flag a revealed cell.")
            return
        if (r, c) in self.flagged:
            self.flagged.remove((r, c))
        else:
            if len(self.flagged) >= self.k:
                messagebox.showinfo("MineSweeper", "You have placed all your flags.")
                return
            self.flagged.add((r, c))
        self.update_display()

    def check_win(self):
        if len(self.showed) == self.n * self.m - self.k:
            self.showed.update(self.mines)
            self.update_display()
            messagebox.showinfo("MineSweeper", f"🎉 You cleared the board in {self.moves} moves!")
            self.game_over = True

    def restart_game(self):
        self.master.destroy()
        launch_setup_window()

def launch_setup_window():
    root = tk.Tk()

    def start_game():
        try:
            n = int(rows_entry.get())
            m = int(cols_entry.get())
            k = int(mines_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return
        if k >= n * m:
            messagebox.showerror("Error", "Too many mines.")
            return
        setup_window.destroy()
        game_root = tk.Tk()
        MinesweeperGUI(game_root, n, m, k)
        game_root.mainloop()

    setup_window = tk.Toplevel(root)
    setup_window.title("Setup MineSweeper")

    tk.Label(setup_window, text="Rows:").grid(row=0, column=0)
    rows_entry = tk.Entry(setup_window)
    rows_entry.grid(row=0, column=1)
    rows_entry.insert(0, "10")

    tk.Label(setup_window, text="Columns:").grid(row=1, column=0)
    cols_entry = tk.Entry(setup_window)
    cols_entry.grid(row=1, column=1)
    cols_entry.insert(0, "10")

    tk.Label(setup_window, text="Mines:").grid(row=2, column=0)
    mines_entry = tk.Entry(setup_window)
    mines_entry.grid(row=2, column=1)
    mines_entry.insert(0, "15")

    start_button = tk.Button(setup_window, text="Start Game", command=start_game)
    start_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.withdraw()
    setup_window.mainloop()

if __name__ == "__main__":
    launch_setup_window()
