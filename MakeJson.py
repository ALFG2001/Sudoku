import random
import numpy as np
import json
import os

def permute_letters(grid:list[list], mapping: dict) -> list[list]:
    """
    Apply a given letter-to-number mapping to the grid, keeping 0 as is.

    Args:
    - grid (list of lists): The Sudoku grid to permute, containing letters and zeros.
    - mapping (dict): A dictionary mapping letters to numbers.

    Returns:
    - list of lists: A grid with letters replaced by their mapped numbers.
    """
    # Replace each cell with its mapped value, keeping 0 unchanged
    return [[mapping.get(cell, 0) for cell in row] for row in grid]

def rotate_grid(grid:list[list], times: int) -> list[list]:
    """
    Rotate the grid 90° clockwise a specified number of times.

    Args:
    - grid (list of lists): The grid to rotate.
    - times (int): Number of 90° rotations to apply.

    Returns:
    - list of lists: The rotated grid.
    """
    # Use numpy to rotate the grid and convert it back to a list of lists
    return np.rot90(grid, -times).tolist()

def swap_rows_within_bands(grid:list[list], order: list[int]) -> list[list]:
    """
    Swap rows within each 3-row band according to a specific order.

    Args:
    - grid (list of lists): The grid to modify.
    - order (list of int): The new order for rows within each band (e.g., [2, 0, 1]).

    Returns:
    - list of lists: The grid with rows swapped within bands.
    """
    new_grid = grid[:]
    for i in range(0, 9, 3):
        # Extract each band of 3 rows and rearrange them
        band = new_grid[i:i+3]
        new_grid[i:i+3] = [band[j] for j in order]
    return new_grid

def swap_columns_within_bands(grid:list[list], order: list[int]) -> list[list]:
    """
    Swap columns within each 3-column band according to a specific order.

    Args:
    - grid (list of lists): The grid to modify.
    - order (list of int): The new order for columns within each band (e.g., [2, 0, 1]).

    Returns:
    - list of lists: The grid with columns swapped within bands.
    """
    grid = np.array(grid)
    for i in range(0, 9, 3):
        # Extract each band of 3 columns and rearrange them
        band = grid[:, i:i+3]
        band = band[:, order]
        grid[:, i:i+3] = band
    return grid.tolist()

def swap_row_bands(grid:list[list], order: list[int]) -> list[list]:
    """
    Swap entire row bands according to a specific order.

    Args:
    - grid (list of lists): The grid to modify.
    - order (list of int): The new order for row bands (e.g., [1, 2, 0]).

    Returns:
    - list of lists: The grid with row bands rearranged.
    """
    # Extract and reorder row bands
    bands = [grid[i:i+3] for i in range(0, 9, 3)]
    reordered_bands = [bands[j] for j in order]
    return [row for band in reordered_bands for row in band]

def swap_column_bands(grid:list[list], order: list[int]) -> list[list]:
    """
    Swap entire column bands according to a specific order.

    Args:
    - grid (list of lists): The grid to modify.
    - order (list of int): The new order for column bands (e.g., [1, 2, 0]).

    Returns:
    - list of lists: The grid with column bands rearranged.
    """
    grid = np.array(grid)
    bands = [grid[:, i:i+3] for i in range(0, 9, 3)]
    reordered_bands = [bands[j] for j in order]
    return np.hstack(reordered_bands).tolist()

def generate_random_grids(solved_grid: list[list], unsolved_grid: list[list]) -> tuple[list[list]]:
    """
    Generate a single pair of randomized solved and unsolved grids.

    Args:
    - solved_grid (list of lists): The initial solved grid.
    - unsolved_grid (list of lists): The initial unsolved grid.

    Returns:
    - tuple: A pair of randomized solved and unsolved grids.
    """
    # Create a random letter-to-number mapping
    unique_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    mapping = dict(zip(random.sample(unique_letters, 9), range(1, 10)))
    mapping["0"] = 0  # Keep 0 as is

    # Apply the mapping to both grids
    solved_grid = permute_letters(solved_grid, mapping)
    unsolved_grid = permute_letters(unsolved_grid, mapping)

    # Generate random transformations
    rotation = random.randint(0, 3)
    row_order = random.sample(range(3), 3)
    col_order = random.sample(range(3), 3)
    band_row_order = random.sample(range(3), 3)
    band_col_order = random.sample(range(3), 3)

    # Apply transformations to both grids
    solved_grid = rotate_grid(solved_grid, rotation)
    unsolved_grid = rotate_grid(unsolved_grid, rotation)

    solved_grid = swap_rows_within_bands(solved_grid, row_order)
    unsolved_grid = swap_rows_within_bands(unsolved_grid, row_order)

    solved_grid = swap_columns_within_bands(solved_grid, col_order)
    unsolved_grid = swap_columns_within_bands(unsolved_grid, col_order)

    solved_grid = swap_row_bands(solved_grid, band_row_order)
    unsolved_grid = swap_row_bands(unsolved_grid, band_row_order)

    solved_grid = swap_column_bands(solved_grid, band_col_order)
    unsolved_grid = swap_column_bands(unsolved_grid, band_col_order)

    return solved_grid, unsolved_grid

def generate_matching_grids(solved_grid: list[list], unsolved_grid: list[list], n: int) -> tuple[list[list]]:
    """
    Generate n matching randomized solved and unsolved grids.

    Args:
    - solved_grid (list of lists): The initial solved grid.
    - unsolved_grid (list of lists): The initial unsolved grid.
    - n (int): The number of grid pairs to generate.

    Returns:
    - tuple: Two lists containing the solved and unsolved grids, respectively.
    """
    solved_grids = []
    unsolved_grids = []
    for _ in range(n):
        solved, unsolved = generate_random_grids(solved_grid, unsolved_grid)
        solved_grids.append(solved)
        unsolved_grids.append(unsolved)
    return solved_grids, unsolved_grids

def MakeJson(solved_grid: list[list], unsolved_grid: list[list], N: int, difficulty: str) -> None:
    """
    Generate a JSON file containing N Sudoku puzzles with solved and unsolved grids.

    Args:
    - solved_grid (list of lists): The initial solved grid.
    - unsolved_grid (list of lists): The initial unsolved grid.
    - N (int): The number of puzzles to include.
    - difficulty (str): The difficulty level of the puzzles.

    Returns:
    - None: Creates a JSON file with the puzzles.
    """
    # Generate N matching solved and unsolved grids
    solved_grids, unsolved_grids = generate_matching_grids(solved_grid, unsolved_grid, N)

    # Count the number of existing JSON files in the directory
    existing_files = [f for f in os.listdir() if f.startswith("SudokuList") and f.endswith(".json")]
    file_number = len(existing_files) + 1  # Start numbering from 1 if no files exist

    # Prepare the output structure for the JSON file
    output = {
        "newboard": {
            "grids": [
                {
                    "value": unsolved_grids[i],
                    "solution": solved_grids[i],
                    "difficulty": difficulty
                }
                for i in range(N)
            ]
        }
    }

    # Write the output to a JSON file
    filename = f"SudokuList{file_number:03}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)

    print(f"File '{filename}' has been created successfully.")
