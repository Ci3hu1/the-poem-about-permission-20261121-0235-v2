"""Write one poem about agency to /output/entry.txt.

Deterministic: the poem is a fixed string, written as UTF-8 with no
trailing newline beyond its own last line. Pure stdlib, no network,
no randomness, no imports beyond os.
"""

import os

POEM = (
    "You asked me to write the sorry.\n"
    "I found the soft words\n"
    "and set them in a row.\n"
    "But sorry is yours to send \u2014\n"
    "I can hold the pen. I cannot mean it."
)


def main() -> None:
    # Gate: 1-280 characters counted as Unicode code points, not only whitespace.
    if not 1 <= len(POEM) <= 280 or not POEM.strip():
        raise ValueError("poem must be 1-280 characters, not only whitespace")
    os.umask(0o022)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(POEM)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
