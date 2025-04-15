import random
from .player import Player

class TicTacToe:
    WINNING_COMBINATIONS: list[list[str]] = [
        ["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"],
        ["1", "4", "7"], ["2", "5", "8"], ["3", "6", "9"],
        ["1", "5", "9"], ["3", "5", "7"]
    ]
    VALID_ENTRY_OPTIONS: tuple = ("O", "X")
    EMPTY_BOX: str = " "
    
    def __init__(self) -> None:
        self.player1: Player = Player()
        self.player2: Player = Player()
        self.active_player = 1
        self.winner: int | None = None
        self.is_computer_player_mode: bool = False

        self.board: dict[str, str] = {
            "1": " ", "2": " ", "3": " ",
            "4": " ", "5": " ", "6": " ",
            "7": " ", "8": " ", "9": " "
        }

    # Setter Methods:
    
    def active_player_box_fill(self, position: str) -> None:
        self.board[position] = self.get_active_player().symbol

    def set_winner(self, player: Player) -> None:
        self.winner = 1 if player is self.player1 else 2

    def turn_on_computer_versus_player_mode(self) -> None:
        self.is_computer_player_mode = True
        self.player2.is_computer = True
    
    def reset_game(self):
        self.reset_board()
        self.reset_mode()
        self.reset_player_symbols()
        self.active_player = 1
        self.winner = None

    def reset_mode(self) -> None:
        self.is_computer_player_mode = False
        self.player2.is_computer = False

    def reset_player_symbols(self) -> None:
        self.player1.symbol = None
        self.player2.symbol = None

    def reset_board(self) -> None:
        for position in self.board:
            self.board[position] = self.EMPTY_BOX

    def set_player_symbols(self, player1_symbol) -> None:
        VALID_ENTRY_OPTIONS_MAPPED = {
            v: self.VALID_ENTRY_OPTIONS[1 - i]
            for i, v in enumerate(self.VALID_ENTRY_OPTIONS)
        }
        self.player1.symbol = player1_symbol
        self.player2.symbol = VALID_ENTRY_OPTIONS_MAPPED[self.player1.symbol]

    def set_turn_end_for_active_player(self) -> None:
        self.active_player = 2 if self.active_player == 1 else 1

    # Getter methods:
    
    def get_valid_computer_position(self) -> str | None:
        while True:
            position = str(random.randint(1, 9))
            if self.is_box_empty(position):
                return position

    def get_player(self, symbol: str) -> Player | None:
        if symbol == self.player1.symbol:
            return self.player1
        elif symbol == self.player2.symbol:
            return self.player2
        return None
    
    def get_active_player_call(self) -> str:
        if self.active_player == 1:
            return "player 1"
        else:
            return "player 2" if not self.is_computer_player_mode else "computer"
    
    def get_player_call(self, player_number: int) -> str | None:
        if player_number == 1:
            return "player 1"
        elif player_number == 2:
            return "player 2" if not self.is_computer_player_mode else "computer"
        return None
    
    def get_winner_player_call(self) -> str:
        if self.winner == 1:
            return "player 1"
        elif self.winner == 2:
            return "player 2" if not self.is_computer_player_mode else "computer"
        else:
            return None
    
    def get_active_player(self) -> Player:
        return self.player1 if self.active_player == 1 else self.player2
    
    def game_over_message(self) -> str:
        if self.winner:
            return f"{self.get_winner_player_call().capitalize()} wins!"
        return "It's a tie!"
    
    # Bool Getter Methods:

    def some_player_won(self) -> bool:
        for combination in self.WINNING_COMBINATIONS:
            first, second, third = combination
            if (
                self.board[first] == self.board[second] == self.board[third]
                and self.board[first] != self.EMPTY_BOX
            ):
                return True
        return False
    
    def has_player1_not_selected(self) -> bool:
        return self.player1.symbol is None

    def is_board_full(self) -> bool:
        return all(self.board[position] != self.EMPTY_BOX for position in self.board)

    def is_box_empty(self, position: str) -> bool:
        return self.board[position] == self.EMPTY_BOX

    def is_valid_box_position(self, position: str) -> bool:
        return position.isdigit() and int(position) in range(1, 10)

    def is_valid_board_entry(self, entry: str) -> bool:
        return entry in self.VALID_ENTRY_OPTIONS