import json
import numpy as np
import pandas as pd
import os
import glob
from MakeBigExcel import *

def process_sudoku_puzzles(json_filename: str) -> list[str]:
    """
    Process Sudoku puzzles from a JSON file and generate Excel files categorized by difficulty.
    
    Args:
    - json_filename (str): The name of the JSON file containing Sudoku data.
    
    Returns:
    - list[str]: A list of created Excel filenames for each difficulty level.
    """
    # Load JSON data from the file
    with open(json_filename, "r") as file:
        data = json.load(file)
    
    # Dictionary to store puzzles categorized by difficulty level
    sudoku_by_difficulty = {}
    
    # Iterate over the grids in the JSON data
    for grid in data["newboard"]["grids"]:
        difficulty = grid["difficulty"]
        puzzle_values = grid["value"]
        puzzle_solution = grid["solution"]
        
        # If the difficulty level is not in the dictionary, add it
        if difficulty not in sudoku_by_difficulty:
            sudoku_by_difficulty[difficulty] = []
        
        # Add the puzzle and its solution to the dictionary under the corresponding difficulty
        sudoku_by_difficulty[difficulty].append({
            "unsolved_grid": puzzle_values, 
            "solution_grid": puzzle_solution
        })
    
    # For each difficulty level, create a separate Excel file
    created_files = []  # Track created files
    for difficulty, puzzles in sudoku_by_difficulty.items():
        # Prepare a list to store data for the current difficulty level
        sudoku_data = []
        
        # Iterate over each puzzle in the current difficulty category
        for counter, puzzle in enumerate(puzzles, start=1):
            print(f"Processing {difficulty}: {counter}/{len(puzzles)} puzzles")
            unsolved_grid = np.array(puzzle["unsolved_grid"])  # The unsolved puzzle grid
            solution_grid = np.array(puzzle["solution_grid"])  # The known solution grid
            
            # Convert the unsolved grid to a string format (to store as text)
            unsolved_grid_string = str(unsolved_grid.tolist())
            
            # Convert the solution grid to a string format (to store as text)
            solution_grid_string = str(solution_grid.tolist())
            
            # Append the puzzle data to the list for this difficulty
            sudoku_data.append({
                "Unsolved_Puzzle": unsolved_grid_string, 
                "Solved_Puzzle": solution_grid_string
            })
        
        # Define the output Excel filename based on the JSON file name and difficulty level
        output_filename = f"{os.path.splitext(os.path.basename(json_filename))[0]}_{difficulty}.xlsx"
        
        # If there is data to write, create a DataFrame and save it as an Excel file
        if sudoku_data:
            df = pd.DataFrame(sudoku_data)
            df.to_excel(output_filename, index=False)
            print(f"Excel file saved: {output_filename}")
            created_files.append(output_filename)  # Add to the list of created files

    return created_files  # Return the list of created files


def MakeExcel() -> None:
    """
    Process all Sudoku JSON files in the current directory to create categorized Excel files 
    and merge them by difficulty level.
    """
    # Iterate over all JSON files in the current directory
    json_files = glob.glob("*.json")
    all_created_files = []  # List to store all created files

    # Process each JSON file in the directory
    for json_file in json_files:
        print(f"Starting to process {json_file}...")
        created_files = process_sudoku_puzzles(json_file)  # Get created files for this JSON
        all_created_files.extend(created_files)  # Add to the list of all created files
        print(f"{json_file} processed successfully.")

    # Merge all the generated Sudoku files by difficulty
    merge_sudoku_files_by_difficulty(".")

    # After processing, delete only JSON files with 'SudokuList' in the filename
    print("Cleaning up: deleting all JSON files...")
    for json_file in json_files:
        if 'SudokuList' in json_file:
            os.remove(json_file)
            print(f"Deleted {json_file}")
