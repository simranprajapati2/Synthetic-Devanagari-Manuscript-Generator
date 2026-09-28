from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import random


def create_old_paper(width=1600, height=2200):
    """
    Creates a simple aged-paper manuscript background.
    """

    # Base paper color
    base = np.zeros((height, width, 3), dtype=np.uint8)

    base_color = np.array([218, 196, 155])

    # Random paper texture
    noise = np.random.normal(0, 9, (height, width, 1))

    image_array = base_color + noise
    image_array = np.clip(image_array, 0, 255)

    base[:, :, :] = image_array

    image = Image.fromarray(base.astype(np.uint8), "RGB")

    # -----------------------------
    # Add random stains
    # -----------------------------
    draw = ImageDraw.Draw(image, "RGBA")

    for _ in range(80):
        x = random.randint(0, width)
        y = random.randint(0, height)

        radius = random.randint(10, 70)

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius,
            ),
            fill=(90, 60, 30, random.randint(5, 20)),
        )

    # Slight blur makes stains natural
    image = image.filter(ImageFilter.GaussianBlur(1.2))

    # -----------------------------
    # Darker edges
    # -----------------------------
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    for i in range(30):
        alpha = int(1 + i * 0.8)

        overlay_draw.rectangle(
            (
                i,
                i,
                width - i,
                height - i,
            ),
            outline=(70, 45, 20, alpha),
            width=2,
        )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    )

    return image.convert("RGB")