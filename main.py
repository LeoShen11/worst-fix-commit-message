#!/usr/bin/env python3
"""Worst Fix Ever: Funniest Commit Message — make.fun entry.

Writes a single commit-message line for a bug fix that made everything
worse to /output/entry.txt (or $OUTPUT_DIR/entry.txt when set, for local
testing). The message is validated before it is written: one line,
1-100 characters, plain commit-subject voice, naming both the fix and
the way it backfired.
"""

import os
import sys

# The commit message. The fix: search kept returning wrong results.
# The backfire: the "fix" was to make search return nothing at all,
# which is technically never wrong. 77 characters, one line.
MESSAGE = "fix: search returned wrong results, so it now returns nothing - 100% accurate"

MAX_CHARS = 100


def validate_message(message: str) -> None:
    """Check the entry text against the competition gate and the brief."""
    if not isinstance(message, str):
        raise ValueError("entry must be a string")
    if not message.strip():
        raise ValueError("entry must not be only whitespace")
    if len(message) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(message)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in message or "\r" in message:
        raise ValueError("entry must be a single line")
    if message != message.strip():
        raise ValueError("entry must not start or end with whitespace")
    if not message.startswith("fix:"):
        raise ValueError("entry must read as a commit subject (start with 'fix:')")
    # The line must name both the repair and the backfire: a fix clause
    # up front and a consequence clause after it.
    if " so " not in message and " - " not in message:
        raise ValueError("entry must name the fix and what it broke")
    if "nothing" not in message and "nobody" not in message:
        raise ValueError("entry must show the fix making things worse")


def main() -> int:
    validate_message(MESSAGE)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the message: no trailing newline, so the text stays
    # as short as possible (the tie-break favours fewer bytes).
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(MESSAGE)
    print(f"wrote {len(MESSAGE)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
