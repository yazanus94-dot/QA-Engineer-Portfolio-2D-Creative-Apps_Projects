"""Compare every image in a baseline folder with the same-named image in an actual folder."""
from __future__ import annotations

import html
import os
from dataclasses import dataclass
from typing import List, Optional

from .compare import DiffResult, compare_images

IMAGE_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".webp")


@dataclass
class Entry:
    name: str
    status: str  # PASS, FAIL, MISSING_ACTUAL, NEW
    result: Optional[DiffResult] = None
    diff_file: Optional[str] = None


def _images(folder: str) -> List[str]:
    return sorted(f for f in os.listdir(folder) if f.lower().endswith(IMAGE_EXT))


def run_comparison(baseline_dir: str, actual_dir: str, out_dir: str, channel_tolerance: int = 0,
                   max_diff_percent: float = 0.0) -> List[Entry]:
    os.makedirs(out_dir, exist_ok=True)
    base, act = set(_images(baseline_dir)), set(_images(actual_dir))
    entries: List[Entry] = []
    for name in sorted(base | act):
        if name not in act:
            entries.append(Entry(name, "MISSING_ACTUAL"))
        elif name not in base:
            entries.append(Entry(name, "NEW"))
        else:
            res = compare_images(os.path.join(baseline_dir, name), os.path.join(actual_dir, name),
                                 channel_tolerance, max_diff_percent)
            diff_file = None
            if not res.passed and res.diff_image is not None:
                diff_file = f"diff_{os.path.splitext(name)[0]}.png"
                res.diff_image.save(os.path.join(out_dir, diff_file))
            entries.append(Entry(name, "PASS" if res.passed else "FAIL", res, diff_file))
    return entries


def has_failures(entries: List[Entry]) -> bool:
    return any(e.status in ("FAIL", "MISSING_ACTUAL") for e in entries)


def write_html_report(entries: List[Entry], out_path: str, baseline_dir: str, actual_dir: str) -> None:
    colors = {"PASS": "#15803d", "FAIL": "#b91c1c", "MISSING_ACTUAL": "#b91c1c", "NEW": "#b45309"}
    rows = []
    for e in entries:
        detail = html.escape(e.result.summary()) if e.result else {
            "MISSING_ACTUAL": "Screenshot missing from the actual run",
            "NEW": "No baseline yet: review and approve",
        }[e.status]
        imgs = ""
        if e.status == "FAIL" and e.diff_file:
            imgs = (f'<div class="imgs"><figure><figcaption>Baseline</figcaption><img src="{html.escape(os.path.relpath(os.path.join(baseline_dir, e.name), os.path.dirname(out_path)))}"></figure>'
                    f'<figure><figcaption>Actual</figcaption><img src="{html.escape(os.path.relpath(os.path.join(actual_dir, e.name), os.path.dirname(out_path)))}"></figure>'
                    f'<figure><figcaption>Diff</figcaption><img src="{html.escape(e.diff_file)}"></figure></div>')
        rows.append(f'<section><h3>{html.escape(e.name)} <span style="color:{colors[e.status]}">{e.status}</span></h3><p>{detail}</p>{imgs}</section>')
    passed = sum(e.status == "PASS" for e in entries)
    doc = f"""<!doctype html><meta charset="utf-8"><title>Visual regression report</title>
<style>body{{font:14px system-ui;margin:24px;color:#1f2937}}section{{border:1px solid #d1d5db;border-radius:8px;padding:8px 16px;margin:12px 0}}
.imgs{{display:flex;gap:12px;flex-wrap:wrap}}figure{{margin:0}}img{{max-width:300px;border:1px solid #d1d5db}}h1{{color:#1f3864}}</style>
<h1>Visual regression report</h1><p>{passed} of {len(entries)} passed.</p>{''.join(rows)}"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
