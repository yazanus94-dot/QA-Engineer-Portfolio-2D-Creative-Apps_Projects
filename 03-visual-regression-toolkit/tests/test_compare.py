import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vrt import compare_images  # noqa: E402


def solid(color=(255, 255, 255, 255), size=(100, 50)):
    return Image.new("RGBA", size, color)


def with_block(base, box, color):
    im = base.copy()
    im.paste(Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), color), box[:2])
    return im


def test_identical_images_pass():
    r = compare_images(solid(), solid())
    assert r.passed and r.diff_pixels == 0 and r.bbox is None and r.diff_percent == 0


def test_any_difference_fails_with_zero_tolerance():
    r = compare_images(solid(), with_block(solid(), (10, 10, 12, 12), (0, 0, 0, 255)))
    assert not r.passed and r.diff_pixels == 4


def test_bounding_box_and_percent():
    r = compare_images(solid(), with_block(solid(), (10, 10, 20, 20), (0, 0, 0, 255)))
    assert r.bbox == (10, 10, 20, 20)
    assert r.diff_pixels == 100
    assert abs(r.diff_percent - 2.0) < 1e-9  # 100 of 5000


def test_channel_tolerance_absorbs_small_noise():
    noisy = with_block(solid(), (0, 0, 100, 50), (252, 253, 254, 255))
    assert not compare_images(solid(), noisy, channel_tolerance=0).passed
    assert compare_images(solid(), noisy, channel_tolerance=3).passed


def test_tolerance_boundary_is_exclusive_of_the_limit():
    off_by_5 = with_block(solid(), (0, 0, 100, 50), (250, 255, 255, 255))
    assert compare_images(solid(), off_by_5, channel_tolerance=5).passed
    assert not compare_images(solid(), off_by_5, channel_tolerance=4).passed


def test_max_diff_percent_threshold():
    changed = with_block(solid(), (0, 0, 10, 10), (0, 0, 0, 255))  # 2%
    assert compare_images(solid(), changed, max_diff_percent=2.0).passed
    assert not compare_images(solid(), changed, max_diff_percent=1.9).passed


def test_ignore_regions_are_excluded():
    changed = with_block(solid(), (0, 0, 10, 10), (0, 0, 0, 255))
    r = compare_images(solid(), changed, ignore_regions=[(0, 0, 10, 10)])
    assert r.passed and r.diff_pixels == 0


def test_alpha_channel_differences_are_detected():
    r = compare_images(solid((255, 255, 255, 255)), solid((255, 255, 255, 0)))
    assert not r.passed and r.max_channel_delta == 255


def test_size_mismatch_fails_without_crashing():
    r = compare_images(solid(size=(100, 50)), solid(size=(120, 50)))
    assert not r.passed and not r.same_size
    assert "size mismatch" in r.summary()


def test_diff_image_marks_changed_pixels_red():
    r = compare_images(solid(), with_block(solid(), (5, 5, 6, 6), (0, 0, 0, 255)))
    assert r.diff_image.getpixel((5, 5)) == (230, 30, 30)
    assert r.diff_image.getpixel((50, 25)) != (230, 30, 30)


def test_invalid_arguments_raise():
    for kwargs in ({"channel_tolerance": -1}, {"channel_tolerance": 256}, {"max_diff_percent": -0.1}):
        try:
            compare_images(solid(), solid(), **kwargs)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {kwargs}")


def test_accepts_file_paths():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p1, p2 = os.path.join(d, "a.png"), os.path.join(d, "b.png")
        solid().save(p1); solid().save(p2)
        assert compare_images(p1, p2).passed
