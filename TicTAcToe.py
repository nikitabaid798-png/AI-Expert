import random
from colorama import init, Fore, Style

init(autoreset=True)


def show_board(board):
    print()

    def format_cell(value):
        if value == 'X':
            return Fore.CYAN + value + Style.RESET_ALL
        elif value == 'O':
            return Fore.MAGENTA + value + Style.RESET_ALL
        return Fore.YELLOW + value + Style.RESET_ALL

    print(' ' + format_cell(board[0]) + ' | ' + format_cell(board[1]) + ' | ' + format_cell(board[2]))
    print(Fore.CYAN + '---+---+---' + Style.RESET_ALL)
    print(' ' + format_cell(board[3]) + ' | ' + format_cell(board[4]) + ' | ' + format_cell(board[5]))
    print(Fore.CYAN + '---+---+---' + Style.RESET_ALL)
    print(' ' + format_cell(board[6]) + ' | ' + format_cell(board[7]) + ' | ' + format_cell(board[8]))
    print()


def choose_symbols():
    choice = ""

    while choice not in ['X', 'O']:
        choice = input(
            Fore.GREEN + "Choose your symbol (X/O): " + Style.RESET_ALL
        ).upper()

    if choice == 'X':
        return 'X', 'O'
    return 'O', 'X'


def get_player_move(board, symbol):
    while True:
        try:
            position = int(input("Choose a position (1-9): "))

            if position < 1 or position > 9:
                print("Please choose a number from 1 to 9.")
                continue

            if not board[position - 1].isdigit():
                print("That position is already taken.")
                continue

            board[position - 1] = symbol
            break

        except ValueError:
            print("Please enter a valid number.")


def computer_move(board, computer_symbol, player_symbol):

    # First, try to win
    for position in range(9):
        if board[position].isdigit():
            test_board = board.copy()
            test_board[position] = computer_symbol

            if has_won(test_board, computer_symbol):
                board[position] = computer_symbol
                return

    # Next, try to block the player
    for position in range(9):
        if board[position].isdigit():
            test_board = board.copy()
            test_board[position] = player_symbol

            if has_won(test_board, player_symbol):
                board[position] = computer_symbol
                return

    # Otherwise, choose a random empty position
    empty_positions = [
        position for position in range(9)
        if board[position].isdigit()
    ]

    selected = random.choice(empty_positions)
    board[selected] = computer_symbol


def has_won(board, symbol):
    winning_lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for first, second, third in winning_lines:
        if board[first] == symbol and board[second] == symbol and board[third] == symbol:
            return True

    return False


def board_is_full(board):
    for position in board:
        if position.isdigit():
            return False

    return True


def start_game():
    print("Let's play Tic-Tac-Toe!")

    player_name = input(
        Fore.GREEN + "Enter your name: " + Style.RESET_ALL
    )

    while True:
        board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        player_symbol, computer_symbol = choose_symbols()
        current_turn = "player"
        game_running = True

        while game_running:
            show_board(board)

            if current_turn == "player":
                get_player_move(board, player_symbol)

                if has_won(board, player_symbol):
                    show_board(board)
                    print(
                        "Great job, " + player_name +
                        "! You won the game!"
                    )
                    game_running = False

                elif board_is_full(board):
                    show_board(board)
                    print("The game ended in a draw.")
                    break

                else:
                    current_turn = "computer"

            else:
                print("Computer is making a move...")
                computer_move(
                    board,
                    computer_symbol,
                    player_symbol
                )

                if has_won(board, computer_symbol):
                    show_board(board)
                    print("The computer won this round!")
                    game_running = False

                elif board_is_full(board):
                    show_board(board)
                    print("The game ended in a draw.")
                    break

                else:
                    current_turn = "player"

        again = input(
            "Would you like to play again? (yes/no): "
        ).lower()

        if again != "yes":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    start_game()