from PIL import Image, ImageDraw, ImageFont
import random


def load_font(font_path, size):
    return ImageFont.truetype(font_path, size)


def wrap_text(draw, text, font, max_width):
    words = text.split()

    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word

        bbox = draw.textbbox(
            (0, 0),
            test,
            font=font
        )

        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def render_block(
    image,
    text,
    font_path,
    x,
    y,
    max_width,
    font_size
):

    draw = ImageDraw.Draw(image)

    font = load_font(
        font_path,
        font_size
    )

    lines = wrap_text(
        draw,
        text,
        font,
        max_width
    )

    line_spacing = random.randint(
        int(font_size * 1.35),
        int(font_size * 1.65)
    )

    current_y = y

    for line in lines:

        # Natural baseline variation
        x_jitter = random.randint(-5, 5)
        y_jitter = random.randint(-3, 3)

        # Slight variation in ink darkness
        ink_value = random.randint(35, 70)

        ink = (
            ink_value,
            max(20, ink_value - 5),
            max(15, ink_value - 12)
        )

        draw.text(
            (
                x + x_jitter,
                current_y + y_jitter
            ),
            line,
            font=font,
            fill=ink
        )

        current_y += line_spacing

    return current_y


def render_manuscript(
    image,
    paragraphs,
    font_path,
    margin=180
):

    width, height = image.size

    writing_width = width - (2 * margin)

    current_y = margin

    # -------------------------
    # TITLE
    # -------------------------

    if paragraphs:

        title = paragraphs[0]

        title_size = random.randint(
            55,
            72
        )

        draw = ImageDraw.Draw(image)

        title_font = load_font(
            font_path,
            title_size
        )

        bbox = draw.textbbox(
            (0, 0),
            title,
            font=title_font
        )

        title_width = bbox[2] - bbox[0]

        title_x = (
            width - title_width
        ) // 2

        draw.text(
            (
                title_x + random.randint(-3, 3),
                current_y
            ),
            title,
            font=title_font,
            fill=(40, 32, 25)
        )

        current_y += (
            title_size + 80
        )

    # -------------------------
    # MAIN TEXT
    # -------------------------

    for paragraph in paragraphs[1:]:

        if current_y >= height - margin:
            break

        indentation = random.randint(
            0,
            70
        )

        x = margin + indentation

        block_width = (
            writing_width - indentation
        )

        font_size = random.randint(
            40,
            54
        )

        current_y = render_block(
            image=image,
            text=paragraph,
            font_path=font_path,
            x=x,
            y=current_y,
            max_width=block_width,
            font_size=font_size
        )

        # Irregular paragraph spacing
        current_y += random.randint(
            25,
            75
        )

        # -------------------------
        # SECTION MARKER
        # -------------------------

        if random.random() < 0.30:

            draw = ImageDraw.Draw(image)

            marker_x = width // 2
            marker_y = current_y

            radius = random.randint(
                4,
                9
            )

            draw.ellipse(
                (
                    marker_x - radius,
                    marker_y - radius,
                    marker_x + radius,
                    marker_y + radius
                ),
                fill=(65, 45, 30)
            )

            current_y += random.randint(
                25,
                50
            )

    return image