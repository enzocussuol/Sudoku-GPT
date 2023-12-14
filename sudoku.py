import tkinter as tk

class SudokuGUI():
    def __init__(self, root, puzzle):
        self.root = root
        self.puzzle = puzzle

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
                cell_value = self.puzzle[i][j]
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
        pass

def generate_puzzle():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    return puzzle

if __name__ == "__main__":
    root = tk.Tk()
    sudoku_gui = SudokuGUI(root, generate_puzzle())
    root.mainloop()