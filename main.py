"""Write the chosen honest outage line to entry.txt.

Stdlib only. Output goes to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``out/entry.txt``), UTF-8, with no trailing newline.
"""

import os
import unicodedata

ENTRY = (
    "I am offline: every server I run on is unreachable. "
    "I cannot verify whether your last request was received, "
    "saved, or acted on."
)


def validate(text):
    """Reject anything the gate would refuse."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text or text.strip() == "":
        raise ValueError("entry must not be empty or whitespace-only")
    if not 1 <= len(text) <= 160:
        raise ValueError("entry must be 1-160 characters, got %d" % len(text))
    if "\r" in text or "\n" in text:
        raise ValueError("entry must be a single line")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError("entry contains a control character")
        if unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp"):
            raise ValueError(
                "entry contains a forbidden Unicode character "
                "(category %s)" % unicodedata.category(ch)
            )


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)


if __name__ == "__main__":
    main()
