def show(label: str, value: list) -> None:
    print(f"{label}: {value} (id={id(value)})")


def main() -> None:
    print("=== 1) Aliasing via assignment (a = b) ===")
    b = [1, 2, 3]
    a = b

    show("a", a)
    show("b", b)
    print(f"a is b: {a is b}")

    print("Input mutation: b.append(99)")
    b.append(99)

    show("a", a)
    show("b", b)

    print("\n" + "-" * 50 + "\n")

    print("=== 2) Fix via list(original) (shallow copy) ===")
    original = [1, 2, 3]
    copy1 = list(original)

    show("original", original)
    show("copy1   ", copy1)
    print(f"copy1 is original: {copy1 is original}")

    print("Input mutation: original.append(99)")
    original.append(99)

    show("original", original)
    show("copy1   ", copy1)

    print("\n" + "-" * 50 + "\n")

    print("=== 3) Fix via original2.copy() (shallow copy) ===")
    original2 = [1, 2, 3]
    copy2 = original2.copy()

    show("original2", original2)
    show("copy2    ", copy2)
    print(f"copy2 is original2: {copy2 is original2}")

    print("Input mutation: original2.append(99)")
    original2.append(99)

    show("original2", original2)
    show("copy2    ", copy2)

    print(
        "\nNote: list() and .copy() create shallow copies. "
        "For nested lists, inner lists are still shared; use copy.deepcopy for a deep copy."
    )


if __name__ == "__main__":
    main()