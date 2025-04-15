from .user_interface_utility_functions import (
    clear_screen,
    hide_cursor,
    show_cursor
)
from .colors import c
from structure.tic_tac_toe import TicTacToe
from structure.player import Player

class UserInterface:
    def __init__(self):
        self.tic_tac_toe: TicTacToe = TicTacToe()

    def display_board(self, disable_positions_chart_view:bool=False) -> None:
        b: dict[str, str] = self.tic_tac_toe.board
        print(f"{b['1']}|{b['2']}|{b['3']}")
        print("-----")
        print(f"{b['4']}|{b['5']}|{b['6']}")
        print("-----")
        print(f"{b['7']}|{b['8']}|{b['9']}")
        print()
        if not disable_positions_chart_view:
            print("Positions:")
            print("1|2|3")
            print("-----")
            print("4|5|6")
            print("-----")
            print("7|8|9")

    def after_game_over(self) -> None:
        print(self.tic_tac_toe.game_over_message())
        print()
        self.display_board()
        print()
        again = input("Play again? (Y/N): ").strip().upper()
        clear_screen()
        if again == "Y":
            self.tic_tac_toe.reset_game()
            self.play_game()
        else:
            print("Thanks for playing!")
            exit()

    def get_valid_position_from_active_player(self) -> None:
        while True:
            self.display_board()
            print()

            player = self.tic_tac_toe.get_active_player_call()
            selection = self.tic_tac_toe.get_active_player_selection()
            position = input(f"Enter a position, {player}, to place '{selection}': ").strip()
            clear_screen()

            if self.tic_tac_toe.is_valid_box_position(position) and self.tic_tac_toe.is_box_empty(position):
                return position
            elif not self.tic_tac_toe.is_valid_box_position(position):
                print("Invalid Box Position!\n")
            else:
                print("Box Already Filled!\n")

    def get_valid_player_one_selection(self) -> None:
        while True:
            self.display_board(disable_positions_chart_view=True)
            print()

            player = self.tic_tac_toe.get_active_player_call().capitalize()
            O = self.tic_tac_toe.VALID_ENTRY_OPTIONS[0]
            X = self.tic_tac_toe.VALID_ENTRY_OPTIONS[1]
            option = input(f"{player} Select '{O}' or '{X}' to  continue: ").strip().upper()
            clear_screen()

            if self.tic_tac_toe.is_valid_board_entry(option):
                return option
            else:
                print(f"Please Enter '{O}' OR '{X}'\n")
            
    def play_game(self) -> None:
        player1_selection = self.get_valid_player_one_selection()
        self.tic_tac_toe.set_player_selections(player1_selection)

        while True:
            position = self.get_valid_position_from_active_player()
            self.tic_tac_toe.active_player_box_fill(position)

            if self.tic_tac_toe.some_player_won():
                self.tic_tac_toe.set_winner(self.tic_tac_toe.get_active_player())
                self.after_game_over()
            elif self.tic_tac_toe.is_board_full():
                self.after_game_over()
            else:
                self.tic_tac_toe.set_turn_end_for_active_player()
