"""news-image-20261120 entry: place the bundled image at the output path.

The program is deliberately boring: it copies entry.png, byte for byte,
into MAKEFUN_OUTPUT_DIR (or /output when the variable is unset). No
network, no randomness, no re-encoding, so two runs always write
identical bytes. The picture itself is produced by build_entry.py from
the scene photos in assets/; this file only delivers it.
"""

import os
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    source = root / "entry.png"
    if not source.is_file():
        print("entry.png is missing next to main.py", file=sys.stderr)
        return 1
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "entry.png").write_bytes(source.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
