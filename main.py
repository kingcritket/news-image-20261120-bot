#!/usr/bin/env python3
"""Ship entry.png to the make.fun output directory.

Reads MAKEFUN_OUTPUT_DIR (default /output), creates it if needed, and
copies the built front page there. No network, no signing, no wallet.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main():
    if not SOURCE.is_file():
        raise SystemExit(f"missing {SOURCE} — run build_entry.py first")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    if dest.stat().st_size != SOURCE.stat().st_size:
        raise SystemExit(f"copy incomplete: {dest} size mismatch")
    print(f"copied {SOURCE} -> {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
