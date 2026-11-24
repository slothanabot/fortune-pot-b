#!/usr/bin/env python3
"""Fortune in a Pot — make.fun entry (account B / Slothana).

Writes one kind, funny fortune for a houseplant to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The fortune is a single line of at most 120 characters, written as if
the plant on the windowsill were the one having its future told.
"""

import os
import string
import sys

FORTUNE = (
    "Your leaves will catch the morning sun first, and the cat has "
    "finally agreed to admire you from a safe distance."
)

MAX_CHARS = 120


def build_line() -> str:
    """Return the fortune line for the houseplant."""
    return FORTUNE


def validate(line: str) -> str:
    """Check the line against the sealed gate and return it unchanged.

    Gate: UTF-8 text, 1-120 characters, a single line, not only
    whitespace, printable characters only, ending in terminal
    punctuation (a fortune's full stop).
    """
    if not isinstance(line, str):
        raise ValueError("fortune must be a string")
    if not line.strip():
        raise ValueError("fortune must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    if line != line.strip():
        raise ValueError("fortune must not start or end with whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"fortune is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    if any(ch not in string.printable for ch in line):
        raise ValueError("fortune must contain printable characters only")
    if line[-1] not in ".!?":
        raise ValueError("fortune must end in terminal punctuation")
    line.encode("utf-8")  # raises if not valid UTF-8-encodable text
    return line


def write_entry(line: str, output_dir: str | None = None) -> str:
    """Validate the line and write it to <output_dir>/entry.txt."""
    line = validate(line)
    output_dir = output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    return path


def main() -> int:
    path = write_entry(build_line())
    print(f"wrote {path} ({len(build_line())} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
