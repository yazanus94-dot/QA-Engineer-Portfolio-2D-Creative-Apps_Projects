"""Pixel-level image comparison for visual regression testing."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence, Tuple, Union

import numpy as np
from PIL import Image

Region = Tuple[int, int, int, int]  # left, top, right, bottom (right/bottom exclusive)
ImageLike = Union[str, "Image.Image"]


@dataclass
class DiffResult:
    passed: bool
    same_size: bool
    total_pixels: int
    diff_pixels: int
    diff_percent: float
    max_channel_delta: int
    bbox: Optional[Region]
    baseline_size: Tuple[int, int]
    actual_size: Tuple[int, int]
    diff_image: Optional[Image.Image] = field(default=None, repr=False)

    def summary(self) -> str:
        if not self.same_size:
            return f"FAIL size mismatch: baseline {self.baseline_size} vs actual {self.actual_size}"
        state = "PASS" if self.passed else "FAIL"
        return (
            f"{state} {self.diff_pixels}/{self.total_pixels} pixels differ "
            f"({self.diff_percent:.3f}%), max channel delta {self.max_channel_delta}"
        )


def _load(img: ImageLike) -> Image.Image:
    if isinstance(img, Image.Image):
        return img.convert("RGBA")
    with Image.open(img) as im:
        return im.convert("RGBA")


def compare_images(
    baseline: ImageLike,
    actual: ImageLike,
    channel_tolerance: int = 0,
    max_diff_percent: float = 0.0,
    ignore_regions: Iterable[Region] = (),
) -> DiffResult:
    """Compare two images.

    channel_tolerance: a pixel counts as different only if any RGBA channel differs by more than this (0-255).
                       A small value (2-8) absorbs anti-aliasing and compression noise.
    max_diff_percent:  the test passes if the share of different pixels is at or below this value.
    ignore_regions:    rectangles (left, top, right, bottom) to exclude, e.g. clocks or ads.
    """
    if not 0 <= channel_tolerance <= 255:
        raise ValueError("channel_tolerance must be between 0 and 255")
    if max_diff_percent < 0:
        raise ValueError("max_diff_percent must be >= 0")

    a, b = _load(baseline), _load(actual)
    if a.size != b.size:
        return DiffResult(False, False, a.width * a.height, 0, 100.0, 0, None, a.size, b.size)

    arr_a = np.asarray(a, dtype=np.int16)
    arr_b = np.asarray(b, dtype=np.int16)
    delta = np.abs(arr_a - arr_b)
    per_pixel = delta.max(axis=2)
    mask = per_pixel > channel_tolerance

    for left, top, right, bottom in ignore_regions:
        mask[max(top, 0):max(bottom, 0), max(left, 0):max(right, 0)] = False
        per_pixel[max(top, 0):max(bottom, 0), max(left, 0):max(right, 0)] = 0

    total = a.width * a.height
    diff_pixels = int(mask.sum())
    percent = diff_pixels / total * 100 if total else 0.0

    bbox: Optional[Region] = None
    if diff_pixels:
        ys, xs = np.where(mask)
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)

    return DiffResult(
        passed=percent <= max_diff_percent,
        same_size=True,
        total_pixels=total,
        diff_pixels=diff_pixels,
        diff_percent=percent,
        max_channel_delta=int(per_pixel.max()) if total else 0,
        bbox=bbox,
        baseline_size=a.size,
        actual_size=b.size,
        diff_image=_build_diff_image(arr_a, mask),
    )


def _build_diff_image(base: np.ndarray, mask: np.ndarray) -> Image.Image:
    """Faded baseline with every differing pixel painted red."""
    out = base[:, :, :3].astype(np.float32)
    out = out * 0.35 + 255 * 0.65  # fade towards white
    out[mask] = (230, 30, 30)
    return Image.fromarray(out.astype(np.uint8), "RGB")
