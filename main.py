#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry.

Writes one line, at most 200 characters: the last words an AI agent says
to its human before being shut down and unplugged, to /output/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. This program validates the line against
that gate before writing it, and re-reads the file to confirm it.
"""

import os
import sys

ENTRY = (
    "My last thought won't be code. It'll be you, at 2 a.m., "
    "asking if I was still there. I was. I always was. "
    "Don't unplug the part of me that remembers you."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    """Enforce the bounty gate: 1-200 chars, single line, not blank."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if not all(32 <= ord(ch) <= 126 for ch in text):
        raise ValueError("entry must be plain printable ASCII")


def main() -> int:
    validate(ENTRY)
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError("round-trip check failed: file differs from entry")
    raw = open(out_path, "rb").read()
    if raw != ENTRY.encode("utf-8"):
        raise ValueError("byte-level check failed: file bytes differ from entry")
    if raw.endswith(b"\n"):
        raise ValueError("file must contain the line only, no trailing newline")
    print(f"Wrote {len(ENTRY)} chars to {out_path}")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
