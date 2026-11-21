#!/usr/bin/env python3
"""make.fun bounty entry: Sum up 21 November's world news in one image.

Writes one image to /output/entry.png. No network, no randomness:
the program copies the bundled entry.png byte-for-byte, so every run
produces identical output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    dst = "/output/entry.png"
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
