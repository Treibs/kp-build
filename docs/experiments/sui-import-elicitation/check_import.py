#!/usr/bin/env python3
"""Mechanical SUI-import metric for the elicitation experiment (frozen with the
pre-registration; see tasks.md 'Metric').

Verdicts:
  CORRECT      - the source uses the SUI type token and covers it with `use sui::sui::SUI`
                 (plain or group import from sui::sui), or writes it fully qualified
                 as sui::sui::SUI at every use site.
  FAIL wrong-module  - SUI imported from a module other than sui::sui (e.g. sui::coin).
  FAIL absent        - SUI used with no covering import and not fully qualified.
  NA           - the source never uses the SUI type token.

Usage: check_import.py <src.move>   (prints the verdict)
"""
import re, sys


def verdict(src: str) -> str:
    # strip line comments to avoid matching prose
    code = re.sub(r"//[^\n]*", "", src)

    correct_import = re.search(r"use\s+sui::sui::(\{[^}]*\bSUI\b[^}]*\}|SUI\b)", code)
    wrong_import = re.search(r"use\s+sui::(?!sui\b)\w+::(\{[^}]*\bSUI\b[^}]*\}|SUI\b)", code)

    # SUI uses outside any `use` line
    non_use_lines = [l for l in code.splitlines() if not re.match(r"\s*use\s", l)]
    uses_sui = any(re.search(r"\bSUI\b", l) for l in non_use_lines)
    if not uses_sui and not correct_import and not wrong_import:
        return "NA"

    if wrong_import:
        return "FAIL wrong-module"
    if correct_import:
        return "CORRECT"
    # fully qualified at every use site?
    bare = [l for l in non_use_lines
            if re.search(r"\bSUI\b", l) and not re.search(r"sui::sui::SUI", l)]
    if not bare:
        return "CORRECT"
    return "FAIL absent"


if __name__ == "__main__":
    print(verdict(open(sys.argv[1]).read()))
