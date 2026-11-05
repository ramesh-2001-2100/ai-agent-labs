"""CLI: save, find, or list emails in the local SQLite store."""

from __future__ import annotations

import argparse
import sys

from email_db import (
    fetch_emails_by_domain,
    find_email,
    init_db,
    save_email,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Store and look up emails. "
            "Choose a mode with -i (insert), -f (find), or -d (domain list)."
        )
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-i",
        "--insert",
        action="store_true",
        help="Insert an email (alerts if that address is already stored)",
    )
    mode.add_argument(
        "-f",
        "--find",
        action="store_true",
        help="Check whether an email is already stored (no insert)",
    )
    mode.add_argument(
        "-d",
        "--domain",
        action="store_true",
        help="List stored emails for a domain",
    )
    parser.add_argument(
        "value",
        nargs="?",
        help="Email address (-i / -f) or domain (-d). Prompted if omitted.",
    )
    return parser


def _prompt(message: str) -> str:
    return input(message).strip()


def _show_help(parser: argparse.ArgumentParser) -> int:
    parser.print_help()
    return 0


def cmd_save(raw: str) -> int:
    try:
        existing = find_email(raw)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if existing is not None:
        print(
            f"Alert: {existing['email_id']!r} is already stored "
            f"(username={existing['username']!r}, domain={existing['domain']!r})."
        )
        return 0

    result = save_email(raw)
    if result.get("duplicate"):
        print(f"Alert: {result['email_id']!r} is already stored; not inserted again.")
        return 0

    print(
        f"Saved: username={result['username']!r}, "
        f"domain={result['domain']!r}, email_id={result['email_id']!r}"
    )
    return 0


def cmd_find(raw: str) -> int:
    try:
        row = find_email(raw)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if row is None:
        print(f"Not found: {raw.strip().lower()!r}")
        return 0

    print(
        f"Found: email_id={row['email_id']!r}, "
        f"username={row['username']!r}, domain={row['domain']!r}"
    )
    return 0


def cmd_domain(raw: str) -> int:
    try:
        rows = fetch_emails_by_domain(raw)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not rows:
        print(f"No emails stored for domain {raw.strip().lower()!r}.")
        return 0

    print(f"Emails on {rows[0]['domain']!r}:")
    for row in rows:
        print(f"  - {row['email_id']} (username={row['username']})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # No args at all → same as -h
    if not args.insert and not args.find and not args.domain and args.value is None:
        return _show_help(parser)

    # Bare email/domain with no mode flag → invalid
    if not args.insert and not args.find and not args.domain:
        print(
            f"Error: invalid argument {args.value!r}; "
            "choose a mode with -i, -f, or -d.",
            file=sys.stderr,
        )
        parser.print_help()
        return 2

    db_path = init_db()
    print(f"Using database: {db_path}")

    if args.domain:
        value = args.value or _prompt("Enter a domain (e.g. gmail.com): ")
        if not value:
            print("Error: domain is required.", file=sys.stderr)
            return 1
        return cmd_domain(value)

    value = args.value or _prompt("Please enter your email id in correct syntax: ")
    if not value:
        print("Error: email is required.", file=sys.stderr)
        return 1

    if args.find:
        return cmd_find(value)
    return cmd_save(value)


if __name__ == "__main__":
    raise SystemExit(main())
