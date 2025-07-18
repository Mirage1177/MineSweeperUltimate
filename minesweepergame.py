import random
import sys

from numpy.ma.core import count
from numpy.ma.extras import stack


def inita_board(n , m, k):
    board = [[0] * (m + 2) for i in range(n + 2)]
    mines = set()
    while len(mines) < k:
        x = random.randint(1, n)
        y = random.randint(1, m)
        if (x, y) not in mines:
            mines.add((x, y))
            board[x][y] = '*'
    for i in range(1, n+1):
        for j in range(1, m+1):
            if board[i][j] != '*':
                count = 0
                for dx in (-1, 0, 1):
                    for dy in (-1, 0,1):
                        if dx != 0 or dy != 0:
                            if board[i+dx][j+dy] == '*':
                                count += 1
                board[i][j] = count
    return board, mines

def print_disp(n, m, showed, flagged, board):
    sys.stdout.write("   ")
    for j in range(1, m+1):
        sys.stdout.write(f" {j:2}")
    print()
    for i in range(1, n+1):
        sys.stdout.write(f"{i:2} ")
        for j in range(1, m+1):
            if (i, j) in flagged:
                sys.stdout.write(" F ")
            elif (i, j) not in showed:
                sys.stdout.write(" . ")
            elif board[i][j] == '*':
                sys.stdout.write(" * ")
            else:
                val = board[i][j]
                sys.stdout.write(f" {val if val != 0 else ' '} ")
        print()
    print()

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
                    nx, ny, = cx+dx, cy+dy
                    if 1 <= nx <= n and 1 <= ny <= m and (nx, ny) not in showed:
                        stack.append((nx, ny))

def play(n, m, k):
    board, mines = inita_board(n, m, k)
    showed = set()
    flagged = set()
    moves = 0

    while True:
        print_disp(n, m, showed, flagged, board)
        act = input("enter move ([r]eveal x y, [f]lag x y) : ").split()
        if len(act) != 3 or act[0] not in ('r', 'f'):
            print("wrong input. try again.")
            continue
        cmd, xs, ys = act
        try:
            x, y = int(xs), int(ys)
        except ValueError:
            print("Must be integers.")
            continue
        if not (1 <= x <= n and 1 <= y <= m):
            print("out of range.")
            continue

        if cmd == 'f':
            if (x, y) in showed:
                print("can't flag a revealed cell.")
            elif (x, y) in flagged:
                flagged.remove((x, y))
            else:
                flagged.add((x, y))
        else:
            if (x, y) in flagged:
                print("unflag before trying to reveal.")
                continue
            if (x, y) in mines:
                showed.update(mines)
                print_disp(n, m, showed, flagged, board)
                print("you hit a mine! BOOM!!! \n \t ...GAME OVER...")
                return
            fill(x, y, n, m, board, showed)

        moves +=1
        if len(showed) == n*m - k:
            showed.update(mines)
            print_disp(n, m, showed, flagged, board)
            print(f"congrats! you discovered the mines and cleared the board in {moves} moves.")
            return



def main():
    print("--- MineSweeper command line game ! ---")
    try:
        n = int(input("Rows: "))
        m = int(input("columns: "))
        k = int(input("Mines: "))
    except ValueError:
        print("please enter valid integers.")
        return
    if k >= n*m:
        print("the number of mines is bigger than the number of cells.")
        return
    play(n, m, k)

main()


