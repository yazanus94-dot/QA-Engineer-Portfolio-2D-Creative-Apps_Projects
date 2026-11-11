import argparse
import os
import sys

from .runner import has_failures, run_comparison, write_html_report


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="vrt", description="Visual regression: compare baseline and actual screenshots.")
    p.add_argument("baseline", help="folder with approved baseline images")
    p.add_argument("actual", help="folder with new screenshots")
    p.add_argument("--out", default="report", help="output folder for diff images and report.html")
    p.add_argument("--tolerance", type=int, default=0, help="per-channel tolerance 0-255 (default 0)")
    p.add_argument("--max-diff", type=float, default=0.0, help="allowed %% of different pixels (default 0)")
    args = p.parse_args(argv)

    entries = run_comparison(args.baseline, args.actual, args.out, args.tolerance, args.max_diff)
    for e in entries:
        print(f"{e.status:<15} {e.name:<20} {e.result.summary() if e.result else ''}")
    write_html_report(entries, os.path.join(args.out, "report.html"), args.baseline, args.actual)
    print(f"\nReport: {os.path.join(args.out, 'report.html')}")
    return 1 if has_failures(entries) else 0


if __name__ == "__main__":
    sys.exit(main())
