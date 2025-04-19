import os
import sys
import termios
import tty
import select


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def hide_cursor() -> None:
    print("\033[?25l")


def show_cursor() -> None:
    print("\033[?25h")


def instant_input(
    prompt: str | None = None,
    timeout: int | float | None = None,
    special_keys: dict[str, str] | None = None,
) -> str:
    """
    Reads a single character from standard input without waiting for the Enter key.
    If a timeout is specified, it will return "no key pressed" if no key is pressed within the timeout period.
    If special_keys is provided, it will map certain key combinations to specific strings.
    """

    if prompt:
        print(prompt, end="", flush=True)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)

        if timeout:
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if not rlist:
                return "no key pressed"

        key_pressed = sys.stdin.read(1)  # Read one character

        # Handle escape sequences for arrow keys
        if key_pressed == "\x1b":
            key_pressed += sys.stdin.read(2)  # Read the next two bytes

        # Use the provided special_keys dictionary, or default to None
        if special_keys is None:
            return key_pressed  # Return raw keypress if no special keys are set
        else:
            return special_keys.get(
                key_pressed, key_pressed
            )  # Apply mapping if provided

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
