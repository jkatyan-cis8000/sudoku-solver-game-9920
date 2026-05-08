#!/usr/bin/env python3
"""
Classic Sudoku Puzzle Game

A 9x9 grid where each row, column, and 3x3 subgrid must contain digits 1-9 exactly once.
Features:
- Pre-populated puzzle with valid clues
- Player input for empty cells
- Mistake detection
- Win condition confirmation
"""

import os
import json

# Difficulty levels - number of empty cells
DIFFICULTY = {
    'easy': 30,
    'medium': 40,
    'hard': 50
}

class SudokuGame:
    def __init__(self):
        """Initialize the Sudoku game with a valid puzzle."""
        self.board = [[0] * 9 for _ in range(9)]
        self.solution = [[0] * 9 for _ in range(9)]
        self.initial_board = [[0] * 9 for _ in range(9)]
        self.player_moves = {}
        self.generate_solved_puzzle()
        self.create_playable_puzzle(difficulty='medium')
    
    def generate_solved_puzzle(self):
        """Generate a valid completed Sudoku puzzle."""
        self._fill_diagonal()
        self._solve_backtrack(self.board)
        # Copy solution for validation
        for i in range(9):
            for j in range(9):
                self.solution[i][j] = self.board[i][j]
    
    def _fill_diagonal(self):
        """Fill the 3 diagonal 3x3 boxes with valid numbers."""
        for i in range(0, 9, 3):
            self._fill_box(i, i)
    
    def _fill_box(self, row, col):
        """Fill a 3x3 box with numbers 1-9 in random order."""
        numbers = list(range(1, 10))
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = numbers[i * 3 + j]
    
    def _is_safe(self, row, col, num):
        """Check if placing num at (row, col) is valid."""
        # Check row
        for x in range(9):
            if self.board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if self.board[x][col] == num:
                return False
        
        # Check 3x3 subgrid
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def _find_empty(self):
        """Find an empty cell (value 0)."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def _solve_backtrack(self, board):
        """Solve the puzzle using backtracking."""
        empty = self._find_empty_pos(board)
        if not empty:
            return True
        
        row, col = empty
        
        for num in range(1, 10):
            if self._is_safe_pos(board, row, col, num):
                board[row][col] = num
                
                if self._solve_backtrack(board):
                    return True
                
                board[row][col] = 0
        
        return False
    
    def _find_empty_pos(self, board):
        """Find an empty cell in the given board."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def _is_safe_pos(self, board, row, col, num):
        """Check if placing num at (row, col) is valid for given board."""
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 subgrid
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def create_playable_puzzle(self, difficulty='medium'):
        """Create a playable puzzle by removing cells from the solved board."""
        attempts = DIFFICULTY[difficulty]
        
        while attempts > 0:
            i = attempts % 9
            j = attempts // 9
            attempts -= 1
            
            if self.board[i][j] != 0:
                self.board[i][j] = 0
        
        # Copy initial state
        for i in range(9):
            for j in range(9):
                self.initial_board[i][j] = self.board[i][j]
    
    def display_board(self):
        """Display the current board state."""
        print("\n" + "=" * 21)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            
            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                
                cell = self.board[i][j]
                if cell == 0:
                    row_str += ". "
                else:
                    row_str += f"{cell} "
            
            print(row_str)
        print("=" * 21 + "\n")
    
    def get_cell_location(self):
        """Get valid cell location from player."""
        while True:
            try:
                pos = input("Enter position (row col, e.g., '1 2') or 'quit' to exit: ").strip()
                if pos.lower() == 'quit':
                    return None
                
                parts = pos.split()
                if len(parts) != 2:
                    print("Invalid format. Use: row col (e.g., '1 2')")
                    continue
                
                row, col = int(parts[0]) - 1, int(parts[1]) - 1
                
                if not (0 <= row < 9 and 0 <= col < 9):
                    print("Position out of range. Use rows 1-9, columns 1-9.")
                    continue
                
                if self.initial_board[row][col] != 0:
                    print("Cannot modify pre-filled cells. Choose an empty cell.")
                    continue
                
                return (row, col)
            except ValueError:
                print("Invalid input. Enter two numbers separated by space.")
    
    def get_value(self):
        """Get valid value (1-9) from player."""
        while True:
            try:
                val = input("Enter value (1-9): ").strip()
                if val.lower() == 'quit':
                    return None
                
                val = int(val)
                if not 1 <= val <= 9:
                    print("Value must be between 1 and 9.")
                    continue
                
                return val
            except ValueError:
                print("Invalid input. Enter a number between 1 and 9.")
    
    def make_move(self, row, col, value):
        """Make a move by placing value at (row, col)."""
        self.board[row][col] = value
        self.player_moves[(row, col)] = value
        return self._check_cell(row, col, value)
    
    def _check_cell(self, row, col, value):
        """Check if a specific cell is correct."""
        return value == self.solution[row][col]
    
    def check_board(self):
        """Check if the entire board is correct and complete."""
        # Check if board is full
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        
        # Check if all cells match solution
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        
        return True
    
    def validate_move(self, row, col, value):
        """Validate a move against Sudoku rules."""
        # Temporarily place the value
        original = self.board[row][col]
        self.board[row][col] = value
        
        # Check row
        for c in range(9):
            if c != col and self.board[row][c] == value:
                self.board[row][col] = original
                return False, "Duplicate in row"
        
        # Check column
        for r in range(9):
            if r != row and self.board[r][col] == value:
                self.board[row][col] = original
                return False, "Duplicate in column"
        
        # Check 3x3 subgrid
        start_row, start_col = row - row % 3, col - col % 3
        for r in range(3):
            for c in range(3):
                curr_r, curr_c = start_row + r, start_col + c
                if (curr_r != row or curr_c != col) and self.board[curr_r][curr_c] == value:
                    self.board[row][col] = original
                    return False, "Duplicate in 3x3 subgrid"
        
        self.board[row][col] = original
        return True, ""
    
    def reset_game(self):
        """Reset the game to initial state."""
        for i in range(9):
            for j in range(9):
                self.board[i][j] = self.initial_board[i][j]
        self.player_moves = {}
    
    def save_game(self, filename='sudoku_save.json'):
        """Save current game state to file."""
        state = {
            'board': self.board,
            'player_moves': {f"{k[0]},{k[1]}": v for k, v in self.player_moves.items()},
            'solution': self.solution
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
        print(f"Game saved to {filename}")
    
    def load_game(self, filename='sudoku_save.json'):
        """Load game state from file."""
        if not os.path.exists(filename):
            print(f"Save file {filename} not found.")
            return False
        
        with open(filename, 'r') as f:
            state = json.load(f)
        
        self.board = state['board']
        self.solution = state['solution']
        self.player_moves = {(int(k.split(',')[0]), int(k.split(',')[1])): v 
                            for k, v in state['player_moves'].items()}
        return True
    
    def print_help(self):
        """Print help information."""
        print("\n=== Sudoku Game Help ===")
        print("Rules:")
        print("  - Fill the 9x9 grid so each row, column, and 3x3 box contains 1-9")
        print("  - Numbers cannot repeat in any row, column, or 3x3 box")
        print("Commands:")
        print("  - Enter 'save' to save the current game")
        print("  - Enter 'quit' to exit the game")
        print("  - Enter 'help' to see this help message")
        print("Playing:")
        print("  - Enter position as: row col (e.g., '3 5' for row 3, column 5)")
        print("  - Enter value as: 1-9")
        print("  - Use 'reset' to restart the current puzzle")
        print("========================\n")


def main():
    """Main game loop."""
    print("\n" + "=" * 50)
    print("       WELCOME TO SUDOKU PUZZLE GAME")
    print("=" * 50)
    
    game = SudokuGame()
    game.print_help()
    
    while True:
        game.display_board()
        
        command = input("Enter position (row col), 'save', 'quit', 'reset', or 'help': ").strip()
        
        if command.lower() == 'quit':
            print("\nThanks for playing! Goodbye!")
            break
        
        elif command.lower() == 'help':
            game.print_help()
            continue
        
        elif command.lower() == 'save':
            game.save_game()
            continue
        
        elif command.lower() == 'reset':
            game.reset_game()
            print("Game reset to initial state.")
            continue
        
        # Try to parse position
        parts = command.split()
        if len(parts) != 2:
            print("Invalid input. Use format: row col (e.g., '3 5')")
            continue
        
        try:
            row, col = int(parts[0]) - 1, int(parts[1]) - 1
            
            if not (0 <= row < 9 and 0 <= col < 9):
                print("Position out of range. Use rows 1-9, columns 1-9.")
                continue
            
            if game.initial_board[row][col] != 0:
                print("Cannot modify pre-filled cells. Choose an empty cell.")
                continue
            
            # Get value
            value = input("Enter value (1-9): ").strip()
            
            if value.lower() == 'quit':
                print("\nThanks for playing! Goodbye!")
                break
            elif value.lower() == 'save':
                game.save_game()
                continue
            elif value.lower() == 'help':
                game.print_help()
                continue
            
            value = int(value)
            if not 1 <= value <= 9:
                print("Value must be between 1 and 9.")
                continue
            
            # Check for duplicates before placing
            valid, error_msg = game.validate_move(row, col, value)
            if not valid:
                print(f"Invalid move: {error_msg}")
                continue
            
            # Make the move
            game.make_move(row, col, value)
            
            # Check if solved
            if game.check_board():
                game.display_board()
                print("\n" + "=" * 50)
                print("   CONGRATULATIONS! YOU SOLVED THE PUZZLE!")
                print("=" * 50)
                print("\nWould you like to play again? (yes/no): ")
                play_again = input().strip().lower()
                if play_again in ['yes', 'y']:
                    game = SudokuGame()
                    game.print_help()
                else:
                    print("\nThanks for playing! Goodbye!")
                    break
        
        except ValueError:
            print("Invalid input. Enter two numbers separated by space.")


if __name__ == "__main__":
    main()
