#!/usr/bin/env python3
"""Entry point for the 21 November 2026 world-news front page.

Copies the pre-drawn ``entry.png`` sitting next to this file into the
output directory named by the ``MAKEFUN_OUTPUT_DIR`` environment variable
(``/output`` when the variable is unset). The copy is checked with a
SHA-256 comparison so a truncated or altered write is caught loudly
instead of being graded silently.

Python 3.13, standard library only.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
DEFAULT_OUT = "/output"


def sha256_of(path):
    """Return the hex SHA-256 digest of the file at ``path``."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
        return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)

    shutil.copyfile(source, target)

    before = sha256_of(source)
    after = sha256_of(target)
    if before != after:
        print(f"error: copied {target} does not match {source}",
              file=sys.stderr)
        print(f"  source sha256: {before}", file=sys.stderr)
        print(f"  target sha256: {after}", file=sys.stderr)
        return 1

    size = os.path.getsize(target)
    print(f"entry ready: {target} — {size} bytes, "
          f"sha256 {before[:16]}...", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
