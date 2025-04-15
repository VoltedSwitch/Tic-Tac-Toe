import os

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def hide_cursor() -> None:
    print("\033[?25l")


def show_cursor() -> None:
    print("\033[?25h")