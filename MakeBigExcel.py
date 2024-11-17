import os
import pandas as pd
import numpy as np

# Function to merge Sudoku files by difficulty level into separate Excel files
def merge_sudoku_files_by_difficulty(directory:str):
    """
    Merges all Sudoku puzzle Excel files from the given directory into three separate files, one for each difficulty level: Easy, Medium, and Hard.

    Args:
    - directory (str): The path to the directory containing Sudoku puzzle Excel files.

    Returns:
    - None: Creates output Excel files for each difficulty level and deletes intermediate files.
    """
    # Initialize a dictionary to hold lists of DataFrames for each difficulty level
    difficulty_data = {
        "Easy": [],  # Store DataFrames of 'Easy' puzzles
        "Medium": [],  # Store DataFrames of 'Medium' puzzles
        "Hard": []  # Store DataFrames of 'Hard' puzzles
    }

    # Loop through all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):  # Process only Excel files
            # Construct the full file path
            filepath = os.path.join(directory, filename)
            
            # Read the Excel file into a DataFrame
            df = pd.read_excel(filepath)
            
            # Check the filename for difficulty (assuming difficulty is part of the filename)
            for difficulty in difficulty_data:
                if difficulty in filename:  # If the filename contains a difficulty level
                    # Append the DataFrame to the corresponding difficulty list
                    difficulty_data[difficulty].append(df)
                    break  # Stop checking other difficulties for this file

    # For each difficulty level, combine the DataFrames and write to a new Excel file
    for difficulty, dfs in difficulty_data.items():
        if dfs:  # Only process if there are DataFrames for this difficulty
            # Concatenate all DataFrames for the current difficulty level into one
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Convert the 'unsolved' and 'solved' columns (lists in string form) to 2D arrays
            for column in ['unsolved', 'solved']:
                if column in combined_df.columns:  # Ensure the column exists
                    combined_df[column] = combined_df[column].apply(
                        lambda x: np.array(eval(x)).reshape(9, 9).tolist() 
                        if isinstance(x, str) and len(eval(x)) == 81 else x  # Convert only valid 81-character strings
                    )

            # If 'Titolo' column (for puzzle numbering) doesn't exist, create it
            if 'Titolo' not in combined_df.columns:
                combined_df.insert(0, 'Titolo', range(1, len(combined_df) + 1))

            # Save the combined DataFrame to a new Excel file for this difficulty level
            output_filename = f"{difficulty}.xlsx"
            combined_df.to_excel(output_filename, index=False)
            print(f"Created {output_filename} with {len(combined_df)} puzzles.")

    # After processing, delete all .xlsx files containing 'SudokuList' in the filename
    print("Cleaning up: deleting all .xlsx files...")
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") and "SudokuList" in filename:  # Target specific files
            file_path = os.path.join(directory, filename)
            os.remove(file_path)  # Delete the file
            print(f"Deleted {filename}")
