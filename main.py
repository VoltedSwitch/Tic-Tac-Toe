from ui.user_interface import UserInterface
from ui.user_interface_utility_functions import clear_screen

def main():
    ui = UserInterface()
    ui.play_game()


if __name__ == "__main__":
    clear_screen()
    main()