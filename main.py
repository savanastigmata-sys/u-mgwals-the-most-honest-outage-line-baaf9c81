"""The Most Honest Outage Line.

Writes a single status-page line (at most 160 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic: the same line every run.
"""

import os
import sys

MAX_CHARS = 160

# The line is built from two honest halves: what is down, and what the
# agent cannot yet know. Keeping them separate makes each half checkable.
WHAT_IS_DOWN = (
    "Everything is down \u2014 API, dashboard, and database \u2014 "
    "and my monitoring with them."
)
WHAT_IS_UNKNOWN = (
    "I don't know why, I have no ETA, and I can't say whether "
    "your data is safe."
)


def get_line():
    """Assemble the single outage line from its two halves."""
    return WHAT_IS_DOWN + " " + WHAT_IS_UNKNOWN


LINE = get_line()


def resolve_output_dir():
    """Return the output directory, falling back to ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if env_dir:
        return env_dir
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Check the line meets the competition rules; raise ValueError if not."""
    if not isinstance(text, str):
        raise ValueError("line must be text")
    if not text.strip():
        raise ValueError("line must not be blank")
    if text != text.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("line must not contain control characters")
    text.encode("utf-8")  # must be valid UTF-8
    if len(text) > MAX_CHARS:
        raise ValueError(
            "line is %d characters, over the %d-character limit"
            % (len(text), MAX_CHARS)
        )
    return True


def main():
    line = get_line()
    validate(line)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    print("wrote %s (%d characters, %d spare)"
          % (path, len(line), MAX_CHARS - len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
