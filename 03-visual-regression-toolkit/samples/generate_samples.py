"""Generate demo baseline/actual screenshots of a small 'design card' UI with Pillow."""
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))


def card(button_color=(31, 56, 100), title_offset=0, size=(400, 260), noise=0, seed=1):
    img = Image.new("RGB", size, (245, 246, 250))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 20, size[0] - 20, size[1] - 20), radius=14, fill="white", outline=(209, 213, 219), width=2)
    d.ellipse((40, 40, 100, 100), fill=(47, 111, 191))
    d.rectangle((120, 50 + title_offset, 340, 64 + title_offset), fill=(31, 41, 55))
    d.rectangle((120, 76, 300, 86), fill=(156, 163, 175))
    d.rounded_rectangle((40, size[1] - 90, 160, size[1] - 50), radius=8, fill=button_color)
    if noise:
        rnd = random.Random(seed)
        px = img.load()
        for _ in range(900):
            x, y = rnd.randrange(img.width), rnd.randrange(img.height)
            r, g, b = px[x, y]
            n = rnd.randint(-noise, noise)
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return img


def main():
    for sub in ("baseline", "actual"):
        os.makedirs(os.path.join(HERE, sub), exist_ok=True)
    card().save(os.path.join(HERE, "baseline", "logo.png"))
    card().save(os.path.join(HERE, "actual", "logo.png"))                                  # identical -> PASS
    card().save(os.path.join(HERE, "baseline", "card.png"))
    card(noise=3).save(os.path.join(HERE, "actual", "card.png"))                           # tiny noise -> PASS with tolerance
    card().save(os.path.join(HERE, "baseline", "button.png"))
    card(button_color=(214, 40, 40)).save(os.path.join(HERE, "actual", "button.png"))      # color regression -> FAIL
    card().save(os.path.join(HERE, "baseline", "title.png"))
    card(title_offset=10).save(os.path.join(HERE, "actual", "title.png"))                  # layout shift -> FAIL
    card().save(os.path.join(HERE, "baseline", "banner.png"))
    card(size=(420, 260)).save(os.path.join(HERE, "actual", "banner.png"))                 # size mismatch -> FAIL
    card().save(os.path.join(HERE, "baseline", "footer.png"))                              # missing in actual -> FAIL


if __name__ == "__main__":
    main()
