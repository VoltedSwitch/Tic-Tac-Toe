import time
from .user_interface_utility_functions import (
    clear_screen,
    hide_cursor,
    show_cursor,
    instant_input
)
from .colors import c
from structure.tic_tac_toe import TicTacToe
from structure.player import Player

class UserInterface:
    GO_BACK = "B"
    START_OVER = "O"

    def __init__(self):
        self.tic_tac_toe: TicTacToe = TicTacToe()

    def play_game(self) -> None:
        while True:
            if self.get_valid_versus_mode_selection() == "2":
                player1_symbol_or_back = self.before_starting_computer_versus_player_mode()
                if player1_symbol_or_back == self.GO_BACK:
                    continue
            else:
                player1_symbol_or_back = self.before_starting_player_versus_player_mode()
                if player1_symbol_or_back == self.GO_BACK:
                    continue
                
            self.tic_tac_toe.set_player_symbols(player1_symbol_or_back)
            while True:
                position = self.get_valid_position_from_active_player()
                self.tic_tac_toe.active_player_box_fill(position)

                if self.tic_tac_toe.some_player_won():
                    self.tic_tac_toe.set_winner(self.tic_tac_toe.get_active_player())
                    if self.after_game_over() == self.START_OVER:
                        break
                elif self.tic_tac_toe.is_board_full():
                    if self.after_game_over() == self.START_OVER:
                        break
                self.tic_tac_toe.set_turn_end_for_active_player()

    def after_game_over(self) -> None:
        print(self.tic_tac_toe.game_over_message())
        print()
        print(f"{self.tic_tac_toe.get_player_call(1).capitalize()} Symbol: {self.tic_tac_toe.player1.symbol}")
        print(f"{self.tic_tac_toe.get_player_call(2).capitalize()} Symbol: {self.tic_tac_toe.player2.symbol} ")
        print()
        self.display_board()
        print()
        again = instant_input("Play again? (Y/N): ").strip().upper()
        clear_screen()
        if again == "Y":
            self.tic_tac_toe.reset_game()
            return self.START_OVER
        else:
            print("Thanks for playing!")
            exit()

    def before_starting_computer_versus_player_mode(self) -> str:
        while True:
            mode = self.get_valid_mode_difficulty_selection_or_back()
            if mode == self.GO_BACK:
                return self.GO_BACK
            self.tic_tac_toe.turn_on_computer_versus_player_mode(mode)
            player1_symbol = self.get_valid_player_one_symbol_or_back()
            if player1_symbol == self.GO_BACK:
                continue
            return player1_symbol
            
    def before_starting_player_versus_player_mode(self) -> str:
        while True:
            player1_symbol = self.get_valid_player_one_symbol_or_back()
            if player1_symbol == self.GO_BACK:
                return self.GO_BACK
            return player1_symbol

    def get_valid_position_from_active_player(self) -> str:
        while True:
            self.display_board()
            print()

            player = self.tic_tac_toe.get_active_player_call()
            symbol = self.tic_tac_toe.get_active_player().symbol
            
            position_entry_statement = f"Enter a position, {player}, to place '{symbol}': "

            if self.tic_tac_toe.get_active_player().is_computer:
                hide_cursor()
                print(position_entry_statement)
                time.sleep(1)
                print("\nComputer is thinking...")
                time.sleep(2)
                show_cursor()
                position = self.tic_tac_toe.get_valid_computer_position()
            else:
                position = instant_input(position_entry_statement).strip()
            clear_screen()

            if self.tic_tac_toe.is_valid_box_position(position) and self.tic_tac_toe.is_box_empty(position):
                return position
            elif not self.tic_tac_toe.is_valid_box_position(position):
                print("Invalid Box Position!\n")
            else:
                print("Box Already Filled!\n")

    def get_valid_player_one_symbol_or_back(self) -> str:
        while True:
            self.display_board(disable_positions_chart_view=True)
            print()

            player = self.tic_tac_toe.get_active_player_call().capitalize()
            O = self.tic_tac_toe.VALID_ENTRY_OPTIONS[0]
            X = self.tic_tac_toe.VALID_ENTRY_OPTIONS[1]
            option = instant_input(f"{player} Select '{O}' or '{X}' to  continue or ({self.GO_BACK})ack: ").strip().upper()
            clear_screen()

            if option == self.GO_BACK:
                self.tic_tac_toe.reset_mode()
                return self.GO_BACK
            elif self.tic_tac_toe.is_valid_board_entry(option):
                return option
            print(f"Please Enter '{O}' OR '{X} OR B for Back'\n")

    def get_valid_mode_difficulty_selection_or_back(self) -> str:
        mode_difficulty = {
            "1": "easy",
            "2": "medium",
            "3": "hard"
        }
        while True:
            self.display_board(disable_positions_chart_view=True)
            print()

            mode_number = instant_input(f"Select An Option:\n1. Easy\n2. Medium\n3. Hard\nor ({self.GO_BACK})ack\n\n> ").strip().upper()
            clear_screen()

            if mode_number == self.GO_BACK:
                return self.GO_BACK
            elif mode_number in ("1", "2", "3"):
                return mode_difficulty[mode_number]
            print("Please Enter A Valid Mode Number OR B for Back!\n")

    def get_valid_versus_mode_selection(self) -> str:
        while True:
            self.display_board(disable_positions_chart_view=True)
            print()

            mode_number = instant_input("Select An Option:\n1. Player vs Player\n2. Player vs Computer\n\n> ").strip()
            clear_screen()

            if mode_number in ("1", "2"):
                return mode_number
            print("Please Enter A Valid Mode Number!\n")

    def display_board(self, disable_positions_chart_view:bool=False) -> None:
        if self.tic_tac_toe.is_computer_player_mode_on():
            print(f"Computer Mode Difficulty: {self.tic_tac_toe.get_computer_mode_difficulty().capitalize()}")
            print()
        b: dict[str, str] = self.tic_tac_toe.board
        print(f"{b['1']}|{b['2']}|{b['3']}")
        print("-----")
        print(f"{b['4']}|{b['5']}|{b['6']}")
        print("-----")
        print(f"{b['7']}|{b['8']}|{b['9']}")
        if not disable_positions_chart_view:
            print()
            print("Positions:")
            print("1|2|3")
            print("-----")
            print("4|5|6")
            print("-----")
            print("7|8|9")