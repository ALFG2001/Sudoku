def flatten_sudoku_grid_to_string(sudoku_grid: list[list[int]]) -> str:
    """
    Flattens a 2D Sudoku grid into a single string by concatenating the values row by row.
    
    Args:
    - sudoku_grid (list[list[int]]): A 2D list representing a Sudoku grid.
    
    Returns:
    - str: A string representing the Sudoku grid with values from all rows concatenated.
    """
    # Flatten the 2D grid by iterating through each cell row by row and converting values to a single string
    return ''.join(str(cell) for row in sudoku_grid for cell in row)


def digit_to_sudoku_letter(digit: str) -> str:
    """
    Converts a digit (1-9) to a corresponding letter (A-I) for Sudoku.
    
    Args:
    - digit (str): A string representing a number from 1 to 9.
    
    Returns:
    - str: A letter corresponding to the input digit, or the original input if not in the range 1-9.
    """
    # Define a mapping from digits (1-9) to letters (A-I)
    digit_to_letter_map = {
        "1": "A", "2": "B", "3": "C", "4": "D", "5": "E",
        "6": "F", "7": "G", "8": "H", "9": "I"
    }
    # Return the corresponding letter or the digit itself if not mapped
    return digit_to_letter_map.get(digit, digit)


def FromNumberToLetter(sudoku_grids: list[list[list[int]] | str]) -> list[list[list[str]]]:
    """
    Converts Sudoku grids (in numeric format) to grids with corresponding letters (A-I).
    
    Args:
    - sudoku_grids (list[list[list[int]] | str]): A list of Sudoku grids, where each grid can be a 2D list of numbers or a flattened string of numbers.
    
    Returns:
    - list[list[list[str]]]: A list of converted Sudoku grids where numbers (1-9) are replaced by letters (A-I).
    """
    # List to store Sudoku grids after converting numbers to letters
    sudoku_grid_with_letters = []

    # Process each Sudoku grid in the input list
    for grid in sudoku_grids:
        # Convert 2D grid to a flattened string if the grid is in list format
        if isinstance(grid, list):
            flattened_sudoku_string = flatten_sudoku_grid_to_string(grid)
        else:
            # Use the string as-is if already flattened
            flattened_sudoku_string = grid

        # Split the flattened string into rows of 9 characters (Sudoku rows)
        sudoku_rows = [flattened_sudoku_string[i:i+9] for i in range(0, len(flattened_sudoku_string), 9)]

        # Convert each row from a string to a list of characters (representing cells)
        sudoku_rows_list = [list(row) for row in sudoku_rows]

        # Map each digit in the grid to its corresponding letter (A-I)
        lista = [
            [digit_to_sudoku_letter(cell) for cell in row]
            for row in sudoku_rows_list
        ]

        # Append the transformed grid to the output list
        sudoku_grid_with_letters.append(lista)

    # Return the list of grids with letters instead of digits
    return sudoku_grid_with_letters
