import random
import os.path
import json

# This makes the random choices different each time
random.seed()

def draw_board(board):
    """Draws the current state of the board."""
    print("\n")
    print("+---+---+---+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Show cells with dividers
        print("+---+---+---+")  # Row border
    print("\n")

def welcome(board):
    """Displays the welcome message and initial board."""
    print("Welcome to the Noughts and Crosses Game!")
    print("You are X and computer is O")
    draw_board(board)

def initialise_board(board):
    """Initializes the board to all empty spaces."""
    # Make all spots on the board empty
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '
    return board

def get_player_move(board):
    """Gets a valid move from the player."""
    while True:
        try:
            # Ask player to pick a number
            move = int(input("Enter the cell number (1-9) to place X: "))
            
            # Make sure number is between 1-9
            if move < 1 or move > 9:
                print("Please choose a number between 1 and 9.")
                continue
                
            # Figure out which row and column that number is
            row = (move - 1) // 3  # Get the row (0, 1, or 2)
            col = (move - 1) % 3   # Get the column (0, 1, or 2)
            
            # Check if that spot is empty
            if board[row][col] == ' ':
                return row, col
            else:
                print("That cell is already taken. Try again.")
        except ValueError:
            print("Please enter a number.")

def choose_computer_move(board):
    """Chooses a random empty cell for the computer's move."""
    # Find all empty spots
    empty_cells = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                empty_cells.append((row, col))
    
    # Pick a random empty spot
    if empty_cells:
        return random.choice(empty_cells)
    return None, None

def check_for_win(board, mark):
    """Checks if the specified mark (X or O) has won the game."""
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == mark:
            return True
            
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == mark:
            return True
            
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == mark:
        return True
    if board[0][2] == board[1][1] == board[2][0] == mark:
        return True
        
    return False

def check_for_draw(board):
    """Checks if the board is full and it's a draw."""
    # Check if any spots are still empty
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                # Game still going if any spot is empty
                return False
    # If no empty spots, it's a draw
    return True

def play_game(board):
    """Plays one round of the game."""
    # Start with clean board
    initialise_board(board)
    draw_board(board)
    
    while True:
        # Player's turn
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)
        
        # Check if player won
        if check_for_win(board, 'X'):
            print("You win!")
            return 1  # Player gets a point
            
        # Check if it's a tie
        if check_for_draw(board):
            print("It's a draw!")
            return 0  # No points
        
        # Computer's turn
        print("Computer is thinking...")
        row, col = choose_computer_move(board)
        if row is not None:
            board[row][col] = 'O'
            print("Computer chose cell:")
            draw_board(board)
            
            # Check if computer won
            if check_for_win(board, 'O'):
                print("Computer wins!")
                return -1  # Player loses a point
                
            # Check if it's a tie
            if check_for_draw(board):
                print("It's a draw!")
                return 0  # No points

def menu():
    """Displays the menu and returns the player's choice."""
    print("\nMenu:")
    print("1 - Play the game")
    print("2 - Save your score")
    print("3 - Display leaderboard")
    print("q - Quit")
    
    while True:
        choice = input("Enter your choice: ").lower()
        if choice in ['1', '2', '3', 'q']:
            return choice
        print("Invalid choice. Please choose 1, 2, 3, or q.")

def load_scores():
    """Loads the scores from leaderboard.txt file."""
    leaders = {}
    if os.path.exists("leaderboard.txt"):
        with open("leaderboard.txt", "r") as file:
            try:
                leaders = json.load(file)
            except json.JSONDecodeError:
                leaders = {}  # Use empty dict if file has problems
    return leaders

def save_score(score):
    """Asks for the player's name and saves their score."""
    name = input("Enter your name: ")
    
    # Get existing scores
    leaders = load_scores()
    
    # Add new score to player's total
    leaders[name] = leaders.get(name, 0) + score
        
    # Save to file
    with open("leaderboard.txt", "w") as file:
        json.dump(leaders, file) 
    
    print("Score saved successfully!")

def display_leaderboard(leaders):
    """Displays the leaderboard in a sorted order."""
    print("\nLeaderboard:")
    
    # Sort by highest score first
    sorted_leaders = sorted(leaders.items(), key=lambda x: x[1], reverse=True)
    
    # Show each player and score
    for name, score in sorted_leaders:
        print(f"{name}: {score}")
    print("\n")

def main():
    # Start with numbered board to show positions
    board = [['1','2','3'],
             ['4','5','6'],
             ['7','8','9']]
             
    # Show welcome message
    welcome(board)
    
    # Track player's score
    total_score = 0
    
    # Main game loop
    while True:
        choice = menu()
        
        # Play a game
        if choice == '1':
            score = play_game(board)
            total_score += score
            print('Your current score is:', total_score)
            
        # Save score
        if choice == '2':
            save_score(total_score)
            
        # Show leaderboard
        if choice == '3':
            leader_board = load_scores() 
            display_leaderboard(leader_board)
            
        # Quit game
        if choice == 'q':
            print('Thank you for playing the "Unbeatable Noughts and Crosses" game.')
            print('Good bye')
            return

# Start the game when this file is run
if __name__ == '__main__':
    main()