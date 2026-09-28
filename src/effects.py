from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random


def add_ink_variation(image):
    """
    Adds subtle blur and contrast variation.
    """

    if random.random() < 0.7:
        image = image.filter(
            ImageFilter.GaussianBlur(
                radius=random.uniform(0.1, 0.35)
            )
        )

    if random.random() < 0.5:
        contrast = ImageEnhance.Contrast(image)
        image = contrast.enhance(
            random.uniform(0.92, 1.08)
        )

    return image


def add_faded_areas(image):
    """
    Creates subtle faded regions on the manuscript.
    """

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    for _ in range(12):

        x = random.randint(0, width)
        y = random.randint(0, height)

        radius = random.randint(40, 160)

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(
                225,
                205,
                165,
                random.randint(8, 22)
            )
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(35)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")


def add_stains(image):
    """
    Adds random historical paper stains.
    """

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    for _ in range(random.randint(8, 18)):

        x = random.randint(0, width)
        y = random.randint(0, height)

        radius = random.randint(10, 80)

        alpha = random.randint(8, 25)

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(90, 55, 25, alpha)
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(12)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")


def add_creases(image):
    """
    Adds subtle page crease/fold marks.
    """

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    # Vertical creases
    for _ in range(random.randint(1, 3)):

        x = random.randint(
            100,
            width - 100
        )

        draw.line(
            (
                x,
                0,
                x + random.randint(-20, 20),
                height
            ),
            fill=(80, 60, 40, 20),
            width=random.randint(1, 3)
        )

    # Horizontal creases
    for _ in range(random.randint(1, 2)):

        y = random.randint(
            100,
            height - 100
        )

        draw.line(
            (
                0,
                y,
                width,
                y + random.randint(-15, 15)
            ),
            fill=(80, 60, 40, 15),
            width=2
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(1.5)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")


def add_edge_damage(image):
    """
    Creates subtle darkening and damage near page edges.
    """

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    # Top edge
    draw.rectangle(
        (0, 0, width, 35),
        fill=(60, 40, 20, 18)
    )

    # Bottom edge
    draw.rectangle(
        (0, height - 35, width, height),
        fill=(60, 40, 20, 22)
    )

    # Left edge
    draw.rectangle(
        (0, 0, 35, height),
        fill=(60, 40, 20, 18)
    )

    # Right edge
    draw.rectangle(
        (width - 35, 0, width, height),
        fill=(60, 40, 20, 18)
    )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(15)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")