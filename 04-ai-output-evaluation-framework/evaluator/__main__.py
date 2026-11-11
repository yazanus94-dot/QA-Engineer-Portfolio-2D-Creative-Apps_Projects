import argparse
import sys

from .report import build_report


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="evaluator", description="Score model responses and write an evaluation report.")
    p.add_argument("data_dir", nargs="?", default="data")
    p.add_argument("--out", help="write the Markdown report to this file")
    args = p.parse_args(argv)
    report = build_report(args.data_dir)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
