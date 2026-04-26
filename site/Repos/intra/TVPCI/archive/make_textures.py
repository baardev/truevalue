"""Create four labeled, colored placeholder PNG textures for the tetrahedron."""

from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(os.path.abspath(__file__))

FACES = {
    "bottom": (80,  160, 220),   # blue
    "front":  (220, 100,  80),   # red-orange
    "left":   (100, 200, 100),   # green
    "right":  (220, 180,  60),   # amber
}

SIZE = 512

for name, color in FACES.items():
    img = Image.new("RGB", (SIZE, SIZE), color)
    draw = ImageDraw.Draw(img)

    # Dark border
    draw.rectangle([4, 4, SIZE - 5, SIZE - 5], outline=(30, 30, 30), width=6)

    # Large centred label
    try:
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 96)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), name.upper(), font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((SIZE - tw) // 2, (SIZE - th) // 2), name.upper(),
              fill=(255, 255, 255), font=font)

    path = os.path.join(OUT, f"{name}.png")
    img.save(path)
    print(f"Saved {path}")
