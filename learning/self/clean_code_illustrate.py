from collections.abc import Iterable


def double_even_numbers(numbers: Iterable[int]) -> list[int]:
    """Return twice each even number in the input."""
    return [number * 2 for number in numbers if number % 2 == 0]


def get_number_list_from_user() -> list[int]:
    """Get a list of integers from the user."""
    try:
        text = input("Enter integers separated by spaces: ")
        return [int(number) for number in text.split()]
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return []


def get_number_tuple_from_user() -> tuple[int, ...]:
    """Get a tuple of integers from the user."""
    try:
        text = input("Enter integers separated by spaces: ")
        return tuple(int(number) for number in text.split())
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return ()


def main() -> None:
    numbers_list = get_number_list_from_user()
    print(double_even_numbers(numbers_list))
    numbers_tuple = get_number_tuple_from_user()
    print(double_even_numbers(numbers_tuple))


if __name__ == "__main__":
    main()


