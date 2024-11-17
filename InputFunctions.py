def get_sudoku_input():
    print("Enter both an unsolved Sudoku grid and a solved Sudoku grid.")
    print("For a 2D array, use the format: [[6, 4, 0, 0, 0, 2, 9, 1, 0], ...]")
    print("For a single string of digits, use the format: 647832915231594786958716243419283657562947831873165492394671528126458379785329164")

    while True:
        # Get unsolved grid input
        unsolved_input = input("Enter the unsolved Sudoku grid: ").strip()
        unsolved_grid = process_sudoku_input(unsolved_input)
        if unsolved_grid:
            break
    
    while True:
        # Get solved grid input
        solved_input = input("Enter the solved Sudoku grid: ").strip()
        solved_grid = process_sudoku_input(solved_input)
        if solved_grid:
            break

    return [unsolved_grid, solved_grid]

def process_sudoku_input(grid_input):
    """Helper function to process either a 2D array or a string of digits."""
    try:
        # Try to evaluate as a 2D array
        sudoku_grid = eval(grid_input)
        
        # If it's a valid 2D list, check if it's a 9x9 grid
        if isinstance(sudoku_grid, list) and len(sudoku_grid) == 9 and all(len(row) == 9 for row in sudoku_grid):
            return sudoku_grid
    except (SyntaxError, ValueError, NameError):
        pass  # Not a valid 2D array, continue to check for string input

    # If it's a long string of digits, process it
    if grid_input.isdigit() and len(grid_input) == 81:  # Sudoku has 81 digits
        return [list(map(int, grid_input[i:i+9])) for i in range(0, 81, 9)]
    else:
        print("Invalid input format. Ensure you provide either a valid 2D array or a string with 81 digits.")

    
def get_amount():
    while True:
        try:
            # Ask for the number of puzzles to generate
            amount = int(input("How many puzzles would you like to generate? "))
            if amount > 0:
                return amount
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_difficulty():
    while True:
        # Ask for the difficulty level (Easy, Medium, Hard)
        difficulty = input("Enter the difficulty (Easy, Medium, Hard): ").capitalize()
        if difficulty in ['Easy', 'Medium', 'Hard']:
            return difficulty
        else:
            print("Invalid input. Please choose from 'Easy', 'Medium', or 'Hard'.")