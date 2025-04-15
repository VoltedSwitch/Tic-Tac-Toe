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

        self.board: dict[str, str] = {
            "1": " ", "2": " ", "3": " ",
            "4": " ", "5": " ", "6": " ",
            "7": " ", "8": " ", "9": " "
        }

    # Setter Methods:
    
    def active_player_box_fill(self, position: str) -> None:
        self.board[position] = self.get_active_player_selection()

    def set_winner(self, player: Player) -> None:
        self.winner = 1 if player is self.player1 else 2
    
    def reset_game(self):
        self.reset_board()
        self.active_player = 1
        self.winner = None

    def reset_board(self) -> None:
        for position in self.board:
            self.board[position] = self.EMPTY_BOX

    def set_player_selections(self, player1_selection) -> None:
        VALID_ENTRY_OPTIONS_MAPPED = {
            v: self.VALID_ENTRY_OPTIONS[1 - i]
            for i, v in enumerate(self.VALID_ENTRY_OPTIONS)
        }
        self.player1.selection = player1_selection
        self.player2.selection = VALID_ENTRY_OPTIONS_MAPPED[self.player1.selection]

    def set_turn_end_for_active_player(self) -> None:
        self.active_player = 2 if self.active_player == 1 else 1

    # Getter methods:

    def get_player(self, selection: str) -> Player | None:
        if selection == self.player1.selection:
            return self.player1
        elif selection == self.player2.selection:
            return self.player2
        return None
    
    def get_active_player_call(self) -> str:
        return "player 1" if self.active_player == 1 else "player 2"
    
    def get_winner_player_call(self) -> str:
        return "player 1" if self.winner == 1 else "player 2" if self.winner == 2 else None
    
    def get_active_player_selection(self) -> str:
        return self.get_active_player().selection
    
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
        return self.player1.selection is None

    def is_board_full(self) -> bool:
        return all(self.board[position] != self.EMPTY_BOX for position in self.board)

    def is_box_empty(self, position: str) -> bool:
        return self.board[position] == self.EMPTY_BOX

    def is_valid_box_position(self, position: str) -> bool:
        return position.isdigit() and int(position) in range(1, 10)

    def is_valid_board_entry(self, entry: str) -> bool:
        return entry in self.VALID_ENTRY_OPTIONS