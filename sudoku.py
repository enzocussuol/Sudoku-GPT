import tkinter as tk
import requests

class Sudoku():
    def __init__(self):
        self.refresh()

    def refresh(self):
        sudoku = requests.get("https://sudoku-api.vercel.app/api/dosuku").json()

        grid = sudoku["newboard"]["grids"][0]
        self.puzzle = grid["value"]
        self.solution = grid["solution"]
        self.difficulty = grid["difficulty"]

class SudokuGUI():
    def __init__(self, root, sudoku):
        self.root = root
        self.sudoku = sudoku

        self.init_UI()

    def init_UI(self):
        self.games_frame = tk.Frame(self.root)
        self.games_frame.pack()

        puzzle_frame = tk.Frame(self.games_frame)
        puzzle_frame.pack(side=tk.LEFT, pady=10, padx=10)
        self.draw_game(self.sudoku.puzzle, puzzle_frame)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=5)
        self.draw_buttons()

    def refresh_UI(self):
        self.games_frame.pack_forget()
        self.buttons_frame.pack_forget()

        self.init_UI()

    def draw_game(self, game, frame):
        for i in range(9):
            for j in range(9):
                cell_value = game[i][j]
                if cell_value != 0:
                    label = tk.Label(frame, text=str(cell_value), font=("Arial", 16), padx=20, pady=20, borderwidth=1, relief="solid")
                else:
                    label = tk.Label(frame, text="", font=("Arial", 16), padx=26, pady=20, borderwidth=1, relief="solid", bg="lightgray")
                label.grid(row=i, column=j)

    def draw_buttons(self):
        resolve_button = tk.Button(self.buttons_frame, text="Resolver com GPT", command=self.resolve_button_listener)
        resolve_button.pack(pady=10)

        new_puzzle_button = tk.Button(self.buttons_frame, text="Novo Tabuleiro", command=self.new_puzzle_button_listener)
        new_puzzle_button.pack()

    def resolve_button_listener(self):
        gpt_solution_frame = tk.Frame(self.games_frame)
        gpt_solution_frame.pack(side=tk.LEFT, pady=10, padx=10)
        self.draw_game(get_gpt_solution(self.sudoku.puzzle), gpt_solution_frame)

        solution_frame = tk.Frame(self.games_frame)
        solution_frame.pack(side=tk.LEFT, padx=10)
        self.draw_game(self.sudoku.solution, solution_frame)

    def new_puzzle_button_listener(self):
        self.sudoku.refresh()
        self.refresh_UI()

def get_gpt_solution(puzzle):
    # Por enquanto
    return puzzle

if __name__ == "__main__":
    sudoku = Sudoku()

    root = tk.Tk()
    root.title("Sudoku com GPT")

    sudoku_gui = SudokuGUI(root, sudoku)

    root.mainloop()