"""umbral-lint — conformance checker for Umbral repos."""
from __future__ import annotations

import argparse
import pathlib
import sys

from . import checks, context, report

VERSION = "1.1.0"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="umbral-lint",
        description="Check a repo against the Umbral design system.",
        epilog="Rule text: https://github.com/umbralmx/umbral-style-guide/blob/main/rules/rules.yaml",
    )
    p.add_argument("path", nargs="?", default=".", type=pathlib.Path,
                   help="file or directory to check (default: .)")
    p.add_argument("--format", choices=sorted(report.FORMATS), default="human")
    p.add_argument("--rules", type=pathlib.Path, help="path to rules.json")
    p.add_argument("--tokens", type=pathlib.Path, help="path to tokens.json")
    p.add_argument("--select", metavar="IDS",
                   help="comma-separated check ids to run (default: all)")
    p.add_argument("--ignore", metavar="IDS", help="comma-separated check ids to skip")
    p.add_argument("--max-severity", choices=["error", "warning", "info"], default="error",
                   help="lowest severity that causes a non-zero exit (default: error)")
    p.add_argument("--list-checks", action="store_true",
                   help="list the checks this build implements, and exit")
    p.add_argument("--version", action="version", version=f"umbral-lint {VERSION}")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.list_checks:
        print(f"umbral-lint {VERSION} implements {len(checks.IMPLEMENTED)} checks:\n")
        for cid, what in sorted(checks.IMPLEMENTED.items()):
            print(f"  {cid:<24} {what}")
        print("\nRules whose check is `review` are judgement calls and are not "
              "checked here.\nSee guide/CHECKLIST.md for the human list.")
        return 0

    root = args.path.resolve()
    if not root.exists():
        print(f"umbral-lint: {args.path} does not exist", file=sys.stderr)
        return 2

    ctx = context.load(root, args.rules, args.tokens)
    checks.run_all(ctx)

    findings = ctx.findings
    if args.select:
        keep = {s.strip() for s in args.select.split(",")}
        findings = [f for f in findings if f.check in keep]
    if args.ignore:
        drop = {s.strip() for s in args.ignore.split(",")}
        findings = [f for f in findings if f.check not in drop]

    checked = sum(1 for _ in ctx.files())
    sys.stdout.write(report.FORMATS[args.format](findings, root, checked))

    threshold = report.ORDER[args.max_severity]
    return 1 if any(report.ORDER.get(f.severity, 3) <= threshold for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
