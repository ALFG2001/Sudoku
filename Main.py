from CreaJson import CreaJson
from MakeSingleExcel import MakeExcel
from MettiLettere import FromNumberToLetter
from GestioneInput import get_sudoku_input, get_amount, get_difficulty

def print_header():
    print("=" * 50)
    print("Welcome to the Sudoku Generator & Excel Exporter")
    print("=" * 50)

def print_menu():
    print("\nWhat would you like to do?")
    print("[1] Generate more Sudoku puzzles")
    print("[2] Generate the Excel file")

def main():
    print_header()

    while True:
        # Get the Sudoku grids
        sudoku_grids = get_sudoku_input()
        
        # Unpack the grids into unsolved and solved versions
        unsolved, solved = FromNumberToLetter(sudoku_grids)
        
        # Generate the JSON for the Sudoku grids
        CreaJson(solved, unsolved, get_amount(), get_difficulty())

        # Ask the user if they want to generate more puzzles or make the Excel file
        print_menu()
        
        user_choice = input("\nPlease enter your choice (1, or 2): ").strip()

        if user_choice == '1':
            print("\nGenerating new Sudoku puzzles...\n")
            continue  # If the user chooses to generate more puzzles, the loop will restart
        elif user_choice == '2':
            # Generate the Excel file
            print("\nGenerating the Excel file...\n")
            MakeExcel()
            print("\nExcel file generated successfully.\n")
            break  # Exit the loop after generating the Excel file
        else:
            print("\nInvalid input. Please enter 1, or 2.\n")

# Run the main program
main()
