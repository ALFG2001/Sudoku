import random
import numpy as np
import json
import os

def permute_letters(grid, mapping:dict):
    """Apply a given letter-to-number mapping to the grid, keeping 0 as is."""
    return [[mapping.get(cell, 0) for cell in row] for row in grid]

def rotate_grid(grid, times):
    """Rotate the grid 90° clockwise 'times' times."""
    return np.rot90(grid, -times).tolist()

def swap_rows_within_bands(grid, order):
    """Swap rows within each 3-row band according to a specific order."""
    new_grid = grid[:]
    for i in range(0, 9, 3):
        band = new_grid[i:i+3]
        new_grid[i:i+3] = [band[j] for j in order]
    return new_grid

def swap_columns_within_bands(grid, order):
    """Swap columns within each 3-column band according to a specific order."""
    grid = np.array(grid)
    for i in range(0, 9, 3):
        band = grid[:, i:i+3]
        band = band[:, order]
        grid[:, i:i+3] = band
    return grid.tolist()

def swap_row_bands(grid, order):
    """Swap entire row bands according to a specific order."""
    bands = [grid[i:i+3] for i in range(0, 9, 3)]
    reordered_bands = [bands[j] for j in order]
    return [row for band in reordered_bands for row in band]

def swap_column_bands(grid, order):
    """Swap entire column bands according to a specific order."""
    grid = np.array(grid)
    bands = [grid[:, i:i+3] for i in range(0, 9, 3)]
    reordered_bands = [bands[j] for j in order]
    return np.hstack(reordered_bands).tolist()

def generate_random_grids(solved_grid, unsolved_grid):
    """Generate a single pair of randomized grids."""
    # Step 1: Create a random letter-to-number mapping
    unique_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    mapping = dict(zip(random.sample(unique_letters, 9), range(1,10)))
    mapping["0"] = 0  # Keep 0 as is

    # Step 2: Apply the mapping to both grids
    solved_grid = permute_letters(solved_grid, mapping) 
    unsolved_grid = permute_letters(unsolved_grid, mapping)

    # Step 3: Generate random transformations
    rotation = random.randint(0, 3)
    row_order = random.sample(range(3), 3)
    col_order = random.sample(range(3), 3)
    band_row_order = random.sample(range(3), 3)
    band_col_order = random.sample(range(3), 3)

    # Step 4: Apply transformations to both grids
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

def generate_matching_grids(solved_grid, unsolved_grid, n=100):
    """Generate n matching permutations of solved and unsolved grids."""
    solved_grids = []
    unsolved_grids = []
    for _ in range(n):
        solved, unsolved = generate_random_grids(solved_grid, unsolved_grid)
        solved_grids.append(solved)
        unsolved_grids.append(unsolved)
    return solved_grids, unsolved_grids

def MakeJson(solved_grid, unsolved_grid, N, difficulty):
    # Generate and print 1 matching grid
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

    # Write the output to a JSON file with the correct filename
    filename = f"SudokuList{file_number:03}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)

    print(f"File '{filename}' has been created successfully.")
