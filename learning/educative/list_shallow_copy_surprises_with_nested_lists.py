from __future__ import annotations

import copy


def main() -> None:
    nested = [[1, 2], [3, 4]]
    shallow = nested.copy()  # copies only the outer list

    print("Before:")
    print(f"  nested : {nested}")
    print(f"  shallow: {shallow}")
    print("Identity checks:")
    print(f"  nested is shallow        : {nested is shallow}")
    print(f"  nested[0] is shallow[0]  : {nested[0] is shallow[0]}")
    print(f"  nested[1] is shallow[1]  : {nested[1] is shallow[1]}")

    shallow[0].append(99)  # mutates the shared inner list

    print("\nAfter shallow[0].append(99):")
    print(f"  nested : {nested}")
    print(f"  shallow: {shallow}")

    deep = copy.deepcopy(nested)
    deep[0].append(100)

    print("\nDeep copy demo (deep[0].append(100)):")
    print(f"  nested: {nested}")
    print(f"  deep  : {deep}")
    print("Deep identity checks:")
    print(f"  nested[0] is deep[0]     : {nested[0] is deep[0]}")


if __name__ == "__main__":
    main()