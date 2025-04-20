import random
from .player import Player
from .structure_utility_functions import has_true_value


class TicTacToe:
    WINNING_COMBINATIONS: list[list[str]] = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["1", "4", "7"],
        ["2", "5", "8"],
        ["3", "6", "9"],
        ["1", "5", "9"],
        ["3", "5", "7"],
    ]
    VALID_ENTRY_OPTIONS: tuple = ("O", "X")
    EMPTY_BOX: str = " "

    def __init__(self) -> None:
        self.player1: Player = Player()
        self.player2: Player = Player()
        self.active_player = 1
        self.winner: int | None = None
        self.is_computer_player_mode: dict[str, bool] = {
            "easy": False,
            "medium": False,
            "hard": False,
        }
        self.board: dict[str, str] = {
            "1": " ",
            "2": " ",
            "3": " ",
            "4": " ",
            "5": " ",
            "6": " ",
            "7": " ",
            "8": " ",
            "9": " ",
        }

    # Setter Methods:

    def active_player_box_fill(self, position: str) -> None:
        self.board[position] = self.get_active_player().symbol

    def set_winner(self, player: Player) -> None:
        self.winner = 1 if player is self.player1 else 2

    def turn_on_computer_versus_player_mode(
        self, mode: str, player_number: int
    ) -> None:
        self.is_computer_player_mode[mode] = True
        self.get_player(player_number).is_computer = True

    def reset_game(self):
        self.reset_board()
        if self.is_computer_player_mode_on():
            self.reset_to_default_versus_mode()
        self.reset_player_symbols()
        self.active_player = 1
        self.winner = None

    def reset_to_default_versus_mode(self) -> None:
        for mode in self.is_computer_player_mode:
            if self.is_computer_player_mode[mode]:
                self.is_computer_player_mode[mode] = False
        self.get_computer_player().is_computer = False

    def reset_player_symbols(self) -> None:
        self.player1.symbol = None
        self.player2.symbol = None

    def reset_board(self) -> None:
        for position in self.board:
            self.board[position] = self.EMPTY_BOX

    def set_player_symbols(self, player1_symbol: str) -> None:
        VALID_ENTRY_OPTIONS_MAPPED = {
            v: self.VALID_ENTRY_OPTIONS[1 - i]
            for i, v in enumerate(self.VALID_ENTRY_OPTIONS)
        }
        self.player1.symbol = player1_symbol
        self.player2.symbol = VALID_ENTRY_OPTIONS_MAPPED[self.player1.symbol]

    def set_turn_end_for_active_player(self) -> None:
        self.active_player = 2 if self.active_player == 1 else 1

    # Getter methods:

    def get_computer_mode_difficulty(self) -> str | None:
        if self.is_computer_player_mode["easy"]:
            return "easy"
        elif self.is_computer_player_mode["medium"]:
            return "medium"
        elif self.is_computer_player_mode["hard"]:
            return "hard"
        return None

    def get_valid_computer_position(self) -> str | None:
        if self.is_computer_player_mode["easy"]:
            return self.get_easy_computer_position()
        elif self.is_computer_player_mode["medium"]:
            return self.get_medium_computer_position()
        elif self.is_computer_player_mode["hard"]:
            return self.get_hard_computer_position()
        return None

    def get_hard_computer_position(self) -> str:
        win_or_block_position = (
            self.computer_try_to_win() or self.computer_try_to_block()
        )
        middle_position = self.enter_middle_position()
        corner_position = self.computer_try_cornering()
        random_position = self.get_random_computer_position()

        if win_or_block_position:
            return win_or_block_position
        elif middle_position:
            return middle_position
        elif corner_position:
            return corner_position
        return random_position

    def get_medium_computer_position(self) -> str:
        win_or_block_position = (
            self.computer_try_to_win() or self.computer_try_to_block()
        )
        middle_position = self.enter_middle_position()
        random_position = self.get_random_computer_position()

        if random.randint(1, 100) <= 60 and win_or_block_position:
            return win_or_block_position
        elif random.randint(1, 100) <= 40 and middle_position:
            return middle_position
        return random_position

    def get_easy_computer_position(self) -> str:
        win_or_block_position = (
            self.computer_try_to_win() or self.computer_try_to_block()
        )
        random_position = self.get_random_computer_position()

        if random.randint(1, 100) <= 30 and win_or_block_position:
            return win_or_block_position
        return random_position

    def get_random_computer_position(self) -> str:
        while True:
            position = str(random.randint(1, len(self.board)))
            if self.is_box_empty(position):
                return position

    def enter_middle_position(self) -> str:
        MIDDLE_POSITION = "5"
        if self.is_box_empty(MIDDLE_POSITION):
            return MIDDLE_POSITION
        return None

    def computer_try_cornering(self) -> str | None:
        corners = ["1", "3", "7", "9"]
        available_corners = [pos for pos in corners if self.is_box_empty(pos)]
        symbol = self.get_computer_player().symbol

        # Check if computer already owns one corner
        owned_corners = [pos for pos in corners if self.board[pos] == symbol]

        # Try to take opposite corner if one is owned
        opposites = {"1": "9", "3": "7", "7": "3", "9": "1"}
        for pos in owned_corners:
            opposite = opposites[pos]
            if self.is_box_empty(opposite):
                return opposite

        # If no opposite corner is available, take any free corner
        if available_corners:
            return random.choice(available_corners)

        return None

    def computer_try_to_win(self) -> str | None:
        for combination in self.WINNING_COMBINATIONS:
            first, second, third = combination
            if self.board[first] == self.board[
                second
            ] == self.get_computer_player().symbol and self.is_box_empty(third):
                return third
            elif self.board[first] == self.board[
                third
            ] == self.get_computer_player().symbol and self.is_box_empty(second):
                return second
            elif self.board[second] == self.board[
                third
            ] == self.get_computer_player().symbol and self.is_box_empty(first):
                return first
        return None

    def computer_try_to_block(self) -> str | None:
        for combination in self.WINNING_COMBINATIONS:
            first, second, third = combination
            if self.board[first] == self.board[
                second
            ] == self.get_non_computer_player().symbol and self.is_box_empty(third):
                return third
            elif self.board[first] == self.board[
                third
            ] == self.get_non_computer_player().symbol and self.is_box_empty(second):
                return second
            elif self.board[second] == self.board[
                third
            ] == self.get_non_computer_player().symbol and self.is_box_empty(first):
                return first
        return None

    def get_computer_symbol_selection(self) -> str:
        return random.choice(self.VALID_ENTRY_OPTIONS)

    def get_computer_player(self) -> Player | None:
        for player in (self.player1, self.player2):
            if player.is_computer:
                return player
        return None

    def get_non_computer_player(self):
        for player in (self.player1, self.player2):
            if not player.is_computer:
                return player
        return None

    def get_player(self, player_number: int) -> Player | None:
        if player_number == 1:
            return self.player1
        elif player_number == 2:
            return self.player2
        return None

    def get_active_player_call(self) -> str:
        if self.active_player == 1:
            return "player 1" if not self.player1.is_computer else "computer"
        else:
            return "player 2" if not self.player2.is_computer else "computer"

    def get_player_call(self, player_number: int) -> str | None:
        if player_number == 1:
            return "player 1" if not self.player1.is_computer else "computer"
        elif player_number == 2:
            return "player 2" if not self.player2.is_computer else "computer"
        return None

    def get_winner_player_call(self) -> str:
        if self.winner == 1:
            return "player 1" if not self.player1.is_computer else "computer"
        elif self.winner == 2:
            return "player 2" if not self.player2.is_computer else "computer"
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
        return position.isdigit() and int(position) in range(1, len(self.board) + 1)

    def is_valid_board_entry(self, entry: str) -> bool:
        return entry in self.VALID_ENTRY_OPTIONS

    def is_computer_player_mode_on(self):
        return has_true_value(self.is_computer_player_mode)
