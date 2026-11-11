import os
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from vrt.runner import has_failures, run_comparison  # noqa: E402


def make(folder, name, color, size=(40, 40)):
    Image.new("RGB", size, color).save(os.path.join(folder, name))


def setup(d):
    b, a = os.path.join(d, "b"), os.path.join(d, "a")
    os.makedirs(b); os.makedirs(a)
    return b, a


def test_statuses_for_pass_fail_missing_and_new():
    with tempfile.TemporaryDirectory() as d:
        b, a = setup(d)
        make(b, "same.png", "white"); make(a, "same.png", "white")
        make(b, "changed.png", "white"); make(a, "changed.png", "black")
        make(b, "gone.png", "white")
        make(a, "fresh.png", "white")
        out = os.path.join(d, "out")
        status = {e.name: e.status for e in run_comparison(b, a, out)}
        assert status == {"same.png": "PASS", "changed.png": "FAIL", "gone.png": "MISSING_ACTUAL", "fresh.png": "NEW"}
        assert os.path.exists(os.path.join(out, "diff_changed.png"))


def test_new_images_alone_do_not_fail_the_run():
    with tempfile.TemporaryDirectory() as d:
        b, a = setup(d)
        make(a, "fresh.png", "white")
        assert not has_failures(run_comparison(b, a, os.path.join(d, "out")))


def test_cli_exit_codes_and_report():
    with tempfile.TemporaryDirectory() as d:
        b, a = setup(d)
        make(b, "x.png", "white"); make(a, "x.png", "white")
        out = os.path.join(d, "out")
        ok = subprocess.run([sys.executable, "-m", "vrt", b, a, "--out", out], cwd=ROOT, capture_output=True, text=True)
        assert ok.returncode == 0 and os.path.exists(os.path.join(out, "report.html"))
        make(a, "x.png", "black")
        bad = subprocess.run([sys.executable, "-m", "vrt", b, a, "--out", out], cwd=ROOT, capture_output=True, text=True)
        assert bad.returncode == 1 and "FAIL" in bad.stdout
