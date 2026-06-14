#!/usr/bin/env python3
"""Thin runner for the falsification acceptance gate (the path SKILL.md / SPEC.md reference).

Equivalent to `kp-build falsify`. Scores a base agent's answer vs a KP-loaded agent's answer on
citation precision + spine recall and records the verdict in the package manifest.

    python eval/falsify.py <package_dir> --question "<area>" --base base.txt --kp kp.txt
"""
import sys
from kp_build.cli import main

if __name__ == "__main__":
    sys.exit(main(["falsify", *sys.argv[1:]]))
