import tkinter as tk
import requests
import google.generativeai as genai

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

        self.init_UI(show_solutions=False)

    def init_UI(self, show_solutions):
        self.games_frame = tk.Frame(self.root)
        self.games_frame.pack()

        puzzle_frame = tk.Frame(self.games_frame)
        puzzle_frame.pack(side=tk.LEFT, pady=10, padx=10)

        puzzle_label = tk.Label(puzzle_frame, text="Jogo Atual", font=("Arial", 16))
        puzzle_label.pack()

        puzzle_board_frame = tk.Frame(puzzle_frame)
        puzzle_board_frame.pack()

        self.draw_game(self.sudoku.puzzle, puzzle_board_frame)

        if show_solutions:
            gpt_solution_frame = tk.Frame(self.games_frame)
            gpt_solution_frame.pack(side=tk.LEFT, padx=10)

            gpt_solution_label = tk.Label(gpt_solution_frame, text="Solução via GPT (Gemini)", font=("Arial", 16))
            gpt_solution_label.pack()

            gpt_solution_board_frame = tk.Frame(gpt_solution_frame)
            gpt_solution_board_frame.pack()

            self.draw_game(get_gpt_solution(self.sudoku.puzzle), gpt_solution_board_frame)

            solution_frame = tk.Frame(self.games_frame)
            solution_frame.pack(side=tk.LEFT, padx=10)

            solution_label = tk.Label(solution_frame, text="Solução Real", font=("Arial", 16))
            solution_label.pack()

            solution_board_frame = tk.Frame(solution_frame)
            solution_board_frame.pack()

            self.draw_game(self.sudoku.solution, solution_board_frame)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=5)

        difficulty_label = tk.Label(self.buttons_frame, text="Dificuldade: " + self.sudoku.difficulty, font=("Arial", 16))
        difficulty_label.pack(pady=10)

        self.draw_buttons(show_solutions)

    def refresh_UI(self, show_solutions):
        self.games_frame.pack_forget()
        self.buttons_frame.pack_forget()

        self.init_UI(show_solutions)

    def draw_game(self, game, frame):
        for i in range(9):
            for j in range(9):
                cell_value = game[i][j]
                if cell_value != 0:
                    label = tk.Label(frame, text=str(cell_value), font=("Arial", 16), padx=20, pady=20, borderwidth=1, relief="solid")
                else:
                    label = tk.Label(frame, text="", font=("Arial", 16), padx=26, pady=20, borderwidth=1, relief="solid", bg="lightgray")
                label.grid(row=i, column=j)

    def draw_buttons(self, show_solutions):
        if not show_solutions:
            resolve_button = tk.Button(self.buttons_frame, text="Resolver com GPT", command=self.resolve_button_listener)
            resolve_button.pack(pady=10)
        else:
            new_puzzle_button = tk.Button(self.buttons_frame, text="Novo Tabuleiro", command=self.new_puzzle_button_listener)
            new_puzzle_button.pack()

    def resolve_button_listener(self):
        self.refresh_UI(show_solutions=True)

    def new_puzzle_button_listener(self):
        self.sudoku.refresh()
        self.refresh_UI(show_solutions=False)

def puzzle_to_text(puzzle):
    puzzle_as_text = ""
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                puzzle_as_text = puzzle_as_text + str(puzzle[i][j])
            else:
                puzzle_as_text = puzzle_as_text + 'X'

            puzzle_as_text = puzzle_as_text + ' '
            if j == 2 or j == 5:
                puzzle_as_text = puzzle_as_text + '| '
            elif j == 8:
                puzzle_as_text = puzzle_as_text + '\n'

        if i == 2 or i == 5:
            puzzle_as_text = puzzle_as_text + '---------------------\n'

    return puzzle_as_text

def text_to_puzzle(text):
    puzzle = []

    i, j, k = 0, 0, 0
    while i < 9:
        row = []
        j = 0
        while j < 9:
            if k < len(text):
                char = text[k]
                k = k + 1

            if char.isdigit():
                row.append(int(char))
                j = j + 1

        puzzle.append(row)
        i = i + 1

    return puzzle

def get_gpt_solution(puzzle, use_code=False):
    prompt_to_gpt = '''
Let's play the Sudoku game. This is a Sudoku board with unkown numbers marked as X:

X X X | 4 X X | X 9 X 
X X 7 | X X X | 6 X X 
3 X X | X 5 X | X 7 4 
---------------------
X X 9 | X 7 X | 3 1 X 
1 X X | 9 X 8 | X X X 
X X X | X X 1 | X 4 X 
---------------------
X X X | 1 X X | 7 X 8
X X X | 7 X 5 | X X X
X 5 X | X X X | 9 3 X

To play the game, consider this rules:
- You can use only numbers from 1 to 9;
- Each 3x3 block can only contain numbers from 1 to 9;
- Each vertical column can only contain numbers from 1 to 9;
- Each horizontal row can only contain numbers from 1 to 9;
- Each number in the 3x3 block, vertical column or horizontal row can be used only once;
- The game is over when the whole Sudoku grid is correctly filled with numbers.

Based on the rules, the solution of this example is:

8 2 1 | 4 6 7 | 5 9 3 
5 4 7 | 3 1 9 | 6 8 2 
3 9 6 | 8 5 2 | 1 7 4 
---------------------
4 8 9 | 2 7 6 | 3 1 5 
1 3 5 | 9 4 8 | 2 6 7 
6 7 2 | 5 3 1 | 8 4 9 
---------------------
2 6 4 | 1 9 3 | 7 5 8 
9 1 3 | 7 8 5 | 4 2 6 
7 5 8 | 6 2 4 | 9 3 1
    '''
    
    if not use_code:
        prompt_to_gpt = prompt_to_gpt + "\nNow, can you solve this Sudoku puzzle? Please answer using the same format provided.\n\n"
    else:
        prompt_to_gpt = prompt_to_gpt + "\nNow, can you write a program and then use it to solve this Sudoku puzzle? Please print the output in the same format provided.\n\n"

    prompt_to_gpt = prompt_to_gpt + puzzle_to_text(puzzle)

    print(prompt_to_gpt)

    response = model.generate_content(prompt_to_gpt)

    print(response.text)

    return text_to_puzzle(response.text)

if __name__ == "__main__":
    genai.configure(api_key="AIzaSyB68D7_R5URXuRuemSZlQFB5mxCX3vDaT8")
    model = genai.GenerativeModel('gemini-pro')

    sudoku = Sudoku()

    root = tk.Tk()
    root.title("Sudoku com GPT")

    sudoku_gui = SudokuGUI(root, sudoku)

    root.mainloop()