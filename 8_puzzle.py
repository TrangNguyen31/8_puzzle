import tkinter as tk
from tkinter import messagebox
import random
import heapq

class PuzzleState:
    def __init__(self, board, moves=0, previous=None):
        self.board = board
        self.moves = moves
        self.previous = previous

    def __lt__(self, other):
        return self.priority() < other.priority()

    def priority(self):
        return self.moves + self.manhattan()

    def manhattan(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                if value != 0:
                    target_x = (value - 1) // 3
                    target_y = (value - 1) % 3
                    distance += abs(i - target_x) + abs(j - target_y)
        return distance

    def neighbors(self):
        neighbors = []
        x, y = self.find_empty()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                neighbors.append(PuzzleState(new_board, self.moves + 1, self))
        return neighbors

    def find_empty(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_goal(self):
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.board == goal

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

def solve_8_puzzle(initial_board):
    initial_state = PuzzleState(initial_board)
    if initial_state.is_goal():
        return initial_state
    frontier = []
    heapq.heappush(frontier, initial_state)
    explored = set()
    while frontier:
        current_state = heapq.heappop(frontier)
        explored.add(tuple(map(tuple, current_state.board)))
        for neighbor in current_state.neighbors():
            if tuple(map(tuple, neighbor.board)) not in explored:
                if neighbor.is_goal():
                    return neighbor
                heapq.heappush(frontier, neighbor)
    return None

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")

        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0)

        self.board = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
        self.tiles = [[None for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.tiles[i][j] = tk.Button(self.frame, text=str(self.board[i][j]) if self.board[i][j] != 0 else "",
                                             width=4, height=2, font=('Helvetica', 24),
                                             command=lambda row=i, col=j: self.move_tile(row, col))
                self.tiles[i][j].grid(row=i, column=j)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, padx=10)

        self.new_puzzle_button = tk.Button(self.control_frame, text="New puzzle", command=self.new_puzzle)
        self.new_puzzle_button.grid(row=0, column=0, pady=5)

        self.random_button = tk.Button(self.control_frame, text="Random", command=self.random_puzzle)
        self.random_button.grid(row=1, column=0, pady=5)

        self.solve_button = tk.Button(self.control_frame, text="Solve", command=self.solve)
        self.solve_button.grid(row=2, column=0, pady=5)

        self.up_button = tk.Button(self.control_frame, text="UP", command=lambda: self.move('UP'))
        self.up_button.grid(row=3, column=0, pady=5)

        self.down_button = tk.Button(self.control_frame, text="DOWN", command=lambda: self.move('DOWN'))
        self.down_button.grid(row=4, column=0, pady=5)

        self.left_button = tk.Button(self.control_frame, text="LEFT", command=lambda: self.move('LEFT'))
        self.left_button.grid(row=5, column=0, pady=5)

        self.right_button = tk.Button(self.control_frame, text="RIGHT", command=lambda: self.move('RIGHT'))
        self.right_button.grid(row=6, column=0, pady=5)

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.tiles[i][j].config(text=str(self.board[i][j]) if self.board[i][j] != 0 else "")

    def move_tile(self, row, col):
        empty_row, empty_col = self.find_empty()
        if abs(row - empty_row) + abs(col - empty_col) == 1:
            self.board[empty_row][empty_col], self.board[row][col] = self.board[row][col], self.board[empty_row][empty_col]
            self.update_board()

    def find_empty(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def new_puzzle(self):
        self.board = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
        self.update_board()

    def random_puzzle(self):
        flattened_board = list(range(9))
        random.shuffle(flattened_board)
        self.board = [flattened_board[i * 3:(i + 1) * 3] for i in range(3)]
        self.update_board()

    def solve(self):
        solution = solve_8_puzzle(self.board)
        if solution:
            steps = []
            current = solution
            while current:
                steps.append(current)
                current = current.previous
            steps.reverse()
            for step in steps:
                self.board = step.board
                self.update_board()
                self.root.update()
                self.root.after(500)
        else:
            messagebox.showinfo("No Solution", "This puzzle cannot be solved")

    def move(self, direction):
        empty_row, empty_col = self.find_empty()
        if direction == 'UP' and empty_row < 2:
            self.board[empty_row][empty_col], self.board[empty_row + 1][empty_col] = self.board[empty_row + 1][empty_col], self.board[empty_row][empty_col]
        elif direction == 'DOWN' and empty_row > 0:
            self.board[empty_row][empty_col], self.board[empty_row - 1][empty_col] = self.board[empty_row - 1][empty_col], self.board[empty_row][empty_col]
        elif direction == 'LEFT' and empty_col < 2:
            self.board[empty_row][empty_col], self.board[empty_row][empty_col + 1] = self.board[empty_row][empty_col + 1], self.board[empty_row][empty_col]
        elif direction == 'RIGHT' and empty_col > 0:
            self.board[empty_row][empty_col], self.board[empty_row][empty_col - 1] = self.board[empty_row][empty_col - 1], self.board[empty_row][empty_col]
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
