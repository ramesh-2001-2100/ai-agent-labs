"""Tiny examples demonstrating nested-list aliasing, deepcopy, and a rebuild alternative.

Run this file to see how shallow copies share inner lists, while deepcopy and
explicit rebuilding create independent inner lists.
"""

from __future__ import annotations

import copy


def demo_aliasing_and_shallow_copy() -> None:
    nested = [[1, 2], [3, 4]]
    shallow = nested.copy()  # copies only the outer list; inner lists are shared

    print("== Aliasing / shallow copy ==")
    print(f"Input nested:  {nested}")
    print(f"Input shallow: {shallow}")

    shallow[0].append(99)

    print("After: shallow[0].append(99)")
    print(f"Output nested:  {nested}  (changed: shared inner list)")
    print(f"Output shallow: {shallow}")
    print()


def demo_deepcopy_fix_and_tradeoff() -> None:
    nested = [[1, 2], [3, 4]]
    deep = copy.deepcopy(nested)

    print("== deepcopy fix (with trade-off) ==")
    print(f"Input nested: {nested}")
    print(f"Input deep:   {deep}")

    deep[0].append(99)

    print("After: deep[0].append(99)")
    print(f"Output nested: {nested}  (unchanged)")
    print(f"Output deep:   {deep}")
    print("Note: copy.deepcopy() copies the entire object graph; for large structures,")
    print("      this can cost more time and memory than a targeted rebuild.")
    print()


def demo_rebuild_alternative() -> None:
    nested = [[1, 2], [3, 4]]
    rebuilt = [inner.copy() for inner in nested]  # rebuild known structure

    print("== Rebuild alternative (structure-known) ==")
    print(f"Input nested:  {nested}")
    print(f"Input rebuilt: {rebuilt}")

    rebuilt[0].append(99)

    print("After: rebuilt[0].append(99)")
    print(f"Output nested:  {nested}  (unchanged)")
    print(f"Output rebuilt: {rebuilt}")
    print()


def main() -> None:
    demo_aliasing_and_shallow_copy()
    demo_deepcopy_fix_and_tradeoff()
    demo_rebuild_alternative()


if __name__ == "__main__":
    main()