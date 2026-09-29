# A small command-dispatcher built on a `while True` loop.
# New concepts in this version:
#   - str.split()       -> break a string into a list of words
#   - *args unpacking   -> capture "everything else" after the first item

while True:
    user_input = input("> ").strip()

    # Skip empty input (e.g. user just pressed Enter)
    if not user_input:
        continue

    # .split() with no args: split on any whitespace, collapse runs,
    # and never produce empty strings. This is the safe default.
    parts = user_input.split()

    # Tuple unpacking: first item -> command, rest -> args.
    # The `*` (a.k.a. "splat") gathers everything that didn't get a name.
    # So "greet Alice Smith" -> command="greet", args=["Alice", "Smith"]
    command, *args = parts

    # ---- Commands ----
    if command in ("stop", "quit", "exit", "q"):
        print("Goodbye!")
        break

    elif command == "greet":
        # args[0] is the first argument, or "stranger" if none was given.
        # `if args` is True when the list is non-empty.
        name = args[0] if args else "stranger"
        print(f"Hello, {name}!")

    elif command == "echo":
        # " ".join() glues a list of strings back together with single spaces.
        # It's the opposite of .split() with no args.
        print(" ".join(args))

    elif command == "shout":
        # .upper() converts to UPPERCASE.
        print(" ".join(args).upper() + "!")

    else:
        # The !r inside an f-string wraps the value in quotes.
        # Great for error messages so you can SEE what the user typed.
        print(f"Unknown command: {command!r}. Try: greet, echo, shout, stop")
