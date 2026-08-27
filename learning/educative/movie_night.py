ELIGIBLE_MOVIEGOING_AGE = 13


def get_age() -> int | None:
    """Read the user's age. Return an int, or None if the input is not a valid integer."""
    try:
        return int(input("Please enter your age: "))
    except ValueError:
        return None


def decide_message(user_age: int) -> str:
    """Return the message for a given age. Does not print."""
    if user_age < 0:
        return "Age cannot be negative. Please enter a number that is 0 or greater."
    if user_age < ELIGIBLE_MOVIEGOING_AGE:
        return "You are too young to watch this movie."
    return "Enjoy the movie!"


def show_message(message: str) -> None:
    """Output the message to the user."""
    print(message)


def main() -> None:
    user_age = get_age()
    if user_age is None:
        show_message("Please enter a valid age.")
        return
    message = decide_message(user_age)
    show_message(message)


if __name__ == "__main__":
    main()