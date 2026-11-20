#!/usr/bin/env python3
"""Deliver entry.png to the make.fun output directory.

The competition harness runs this file; all it has to do is place the
pre-built front page where the harness looks for it. The destination
comes from the MAKEFUN_OUTPUT_DIR environment variable and defaults to
/output. The copy is verified by size before success is reported.
Nothing here touches the network, a wallet or any credential.
"""

import os
import shutil
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
FRONT_PAGE = REPO_DIR / "entry.png"
DEFAULT_OUT = "/output"


def deliver():
    if not FRONT_PAGE.is_file():
        raise SystemExit(
            "missing {} — run build_entry.py first".format(FRONT_PAGE)
        )
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT))
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / "entry.png"
    shutil.copyfile(FRONT_PAGE, destination)
    if destination.stat().st_size != FRONT_PAGE.stat().st_size:
        raise SystemExit(
            "copy incomplete: {} size mismatch".format(destination)
        )
    print("copied {} -> {} ({} bytes)".format(
        FRONT_PAGE, destination, destination.stat().st_size))


if __name__ == "__main__":
    deliver()
