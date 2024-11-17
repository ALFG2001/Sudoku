def get_sudoku_input():
    """
    Prompts the user to enter both an unsolved and a solved Sudoku grid. 
    Accepts input in the form of a 2D array or a single string of digits.

    Returns:
    - list: A list containing two 9x9 Sudoku grids (unsolved and solved).
    """
    print("Enter both an unsolved Sudoku grid and a solved Sudoku grid.")
    print("For a 2D array, use the format: [[6, 4, 0, 0, 0, 2, 9, 1, 0], ...]")
    print("For a single string of digits, use the format: 647832915231594786958716243...")

    # Loop until a valid unsolved Sudoku grid is provided
    while True:
        unsolved_input = input("Enter the unsolved Sudoku grid: ").strip()
        unsolved_grid = process_sudoku_input(unsolved_input)
        if unsolved_grid:
            break  # Exit loop when valid input is received

    # Loop until a valid solved Sudoku grid is provided
    while True:
        solved_input = input("Enter the solved Sudoku grid: ").strip()
        solved_grid = process_sudoku_input(solved_input)
        if solved_grid:
            break  # Exit loop when valid input is received

    return [unsolved_grid, solved_grid]


def process_sudoku_input(grid_input):
    """
    Processes the user's input to validate and convert it into a 9x9 Sudoku grid.

    Args:
    - grid_input (str): The raw input provided by the user, either a 2D array or a string.

    Returns:
    - list or None: A 9x9 Sudoku grid as a list of lists if input is valid; None otherwise.
    """
    try:
        # Try to evaluate input as a Python expression (e.g., a 2D array)
        sudoku_grid = eval(grid_input)
        
        # Check if it's a valid 9x9 2D grid
        if isinstance(sudoku_grid, list) and len(sudoku_grid) == 9 and all(len(row) == 9 for row in sudoku_grid):
            return sudoku_grid
    except (SyntaxError, ValueError, NameError):
        pass  # Not a valid 2D array, continue to check for string input

    # Check if input is a valid string of 81 digits
    if grid_input.isdigit() and len(grid_input) == 81:
        # Convert string into a 9x9 grid
        return [list(map(int, grid_input[i:i+9])) for i in range(0, 81, 9)]
    else:
        # Invalid input format
        print("Invalid input format. Ensure you provide either a valid 2D array or a string with 81 digits.")


def get_amount():
    """
    Prompts the user to enter the number of puzzles to generate.

    Returns:
    - int: The number of puzzles requested by the user (positive integer).
    """
    while True:
        try:
            # Prompt the user for the number of puzzles
            amount = int(input("How many puzzles would you like to generate? "))
            if amount > 0:
                return amount  # Valid input, return the value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_difficulty():
    """
    Prompts the user to choose a difficulty level for the Sudoku puzzles.

    Returns:
    - str: The selected difficulty level ('Easy', 'Medium', 'Hard').
    """
    while True:
        # Prompt for difficulty level and normalize input to capitalized form
        difficulty = input("Enter the difficulty (Easy, Medium, Hard): ").capitalize()
        if difficulty in ['Easy', 'Medium', 'Hard']:
            return difficulty  # Return valid difficulty
        else:
            print("Invalid input. Please choose from 'Easy', 'Medium', or 'Hard'.")
