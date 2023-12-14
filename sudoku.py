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

        root.title("Sudoku com GPT")

        self.create_UI()

    def create_UI(self):
        self.puzzle_frame = tk.Frame(self.root)
        self.puzzle_frame.pack(padx=10, pady=10)
        self.draw_puzzle()

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=10)
        self.draw_buttons()

    def draw_puzzle(self):
        for i in range(9):
            for j in range(9):
                cell_value = self.sudoku.puzzle[i][j]
                if cell_value != 0:
                    label = tk.Label(self.puzzle_frame, text=str(cell_value), font=("Arial", 16), padx=20, pady=20, borderwidth=1, relief="solid")
                else:
                    label = tk.Label(self.puzzle_frame, text="", font=("Arial", 16), padx=26, pady=20, borderwidth=1, relief="solid", bg="lightgray")
                label.grid(row=i, column=j)

    def draw_buttons(self):
        resolve_button = tk.Button(self.buttons_frame, text="Resolver com GPT", command=self.resolve_button_listener)
        resolve_button.pack(pady=10)

        new_puzzle_button = tk.Button(self.buttons_frame, text="Novo Tabuleiro", command=self.new_puzzle_button_listener)
        new_puzzle_button.pack()

    def resolve_button_listener(self):
        pass

    def new_puzzle_button_listener(self):
        self.sudoku.refresh()
        self.draw_puzzle()

if __name__ == "__main__":
    sudoku = Sudoku()

    root = tk.Tk()
    sudoku_gui = SudokuGUI(root, sudoku)
    root.mainloop()