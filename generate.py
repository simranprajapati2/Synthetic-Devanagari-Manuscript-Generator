from pathlib import Path
import random

from src.background import create_old_paper
from src.renderer import render_manuscript
from src.effects import (
    add_ink_variation,
    add_faded_areas,
    add_stains,
    add_creases,
    add_edge_damage
)


BASE_DIR = Path(__file__).resolve().parent

# ==============================
# SCRIPT CONFIGURATION
# ==============================

SCRIPT = "devanagari"

SCRIPT_CONFIG = {
    "devanagari": {
        "text": BASE_DIR / "data" / "raw" / "devanagari.txt",
        "font": BASE_DIR / "fonts" / "NotoSansDevanagari-Regular.ttf",
    },

    "modi": {
        "text": BASE_DIR / "data" / "raw" / "modi.txt",
        "font": BASE_DIR / "fonts" / "NotoSansModi-Regular.ttf",
    },

    "sharada": {
        "text": BASE_DIR / "data" / "raw" / "sharada.txt",
        "font": BASE_DIR / "fonts" / "NotoSansSharada-Regular.ttf",
    },
}


if SCRIPT not in SCRIPT_CONFIG:
    raise ValueError(
        f"Unknown script: {SCRIPT}"
    )


CONFIG = SCRIPT_CONFIG[SCRIPT]

TEXT_FILE = CONFIG["text"]
FONT_FILE = CONFIG["font"]

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "output"
    / SCRIPT
)


# ==============================
# IMAGE SETTINGS
# ==============================

WIDTH = 1600
HEIGHT = 2200

MARGIN = 180

NUM_IMAGES = 100


# ==============================
# LOAD TEXT
# ==============================

def load_paragraphs():

    text = TEXT_FILE.read_text(
        encoding="utf-8"
    )

    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
        and not p.startswith("#")
    ]

    return paragraphs


# ==============================
# CREATE ANNOTATION
# ==============================

def create_annotation(
    image_name,
    paragraphs
):

    ground_truth = "\n\n".join(
        paragraphs
    )

    annotation = f"""# Synthetic Manuscript Annotation

## Image Information

- **Filename:** `{image_name}`
- **Script:** {SCRIPT.title()}
- **Language:** Sanskrit / Indic
- **Width:** {WIDTH}px
- **Height:** {HEIGHT}px

## Ground Truth Text

{ground_truth}

## Generation Information

- Background: Aged handmade paper
- Ink variation: Enabled
- Fading effect: Enabled
- Manuscript layout: Enabled
- Paper stains: Enabled
- Paper creases: Enabled
- Edge aging: Enabled
- Synthetic image: Yes
"""

    return annotation


# ==============================
# GENERATE ONE IMAGE
# ==============================

def generate_one(
    paragraphs,
    index
):

    # Create manuscript paper
    image = create_old_paper(
        WIDTH,
        HEIGHT
    )

    # Render manuscript text
    image = render_manuscript(
        image=image,
        paragraphs=paragraphs,
        font_path=str(FONT_FILE),
        margin=MARGIN
    )

    # Apply visual effects
    image = add_ink_variation(image)

    image = add_faded_areas(image)

    image = add_stains(image)

    image = add_creases(image)

    image = add_edge_damage(image)

    # Image filename
    image_name = (
        f"manuscript_{index:04d}.png"
    )

    output_file = (
        OUTPUT_DIR / image_name
    )

    image.save(output_file)

    # Annotation filename
    annotation_file = (
        OUTPUT_DIR
        / f"manuscript_{index:04d}.md"
    )

    annotation = create_annotation(
        image_name,
        paragraphs
    )

    annotation_file.write_text(
        annotation,
        encoding="utf-8"
    )

    return (
        output_file,
        annotation_file
    )


# ==============================
# DATASET SPLIT
# ==============================

def create_dataset_split():

    print()
    print("Creating dataset split...")
    print("--------------------------------")

    files = list(
        OUTPUT_DIR.glob("*.png")
    )

    if not files:
        print("No PNG files found.")
        return

    random.shuffle(files)

    total = len(files)

    train_count = int(
        total * 0.85
    )

    validation_count = int(
        total * 0.10
    )

    train_files = files[
        :train_count
    ]

    validation_files = files[
        train_count:
        train_count + validation_count
    ]

    test_files = files[
        train_count + validation_count:
    ]

    splits = {
        "train": train_files,
        "validation": validation_files,
        "test": test_files
    }

    for split_name, split_files in splits.items():

        split_dir = (
            OUTPUT_DIR / split_name
        )

        split_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for image_file in split_files:

            md_file = (
                image_file.with_suffix(".md")
            )

            # Move image
            image_file.rename(
                split_dir
                / image_file.name
            )

            # Move annotation
            if md_file.exists():

                md_file.rename(
                    split_dir
                    / md_file.name
                )

        print(
            f"{split_name}: "
            f"{len(split_files)} images"
        )


# ==============================
# MAIN
# ==============================

def main():

    print(
        "Synthetic Manuscript Generator"
    )

    print(
        "--------------------------------"
    )

    print(
        f"Script: {SCRIPT}"
    )

    print(
        f"Target images: {NUM_IMAGES}"
    )

    print()

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Check text file
    if not TEXT_FILE.exists():

        raise FileNotFoundError(
            f"Text file not found: "
            f"{TEXT_FILE}"
        )

    # Check font
    if not FONT_FILE.exists():

        raise FileNotFoundError(
            f"Font not found: "
            f"{FONT_FILE}"
        )

    # Load text
    paragraphs = load_paragraphs()

    if not paragraphs:

        raise ValueError(
            f"No text found in "
            f"{TEXT_FILE.name}"
        )

    print(
        f"Loaded {len(paragraphs)} "
        f"text samples."
    )

    print()

    # Generate images
    for i in range(NUM_IMAGES):

        image_file, annotation_file = (
            generate_one(
                paragraphs,
                i + 1
            )
        )

        print(
            f"[{i + 1}/{NUM_IMAGES}] "
            f"{image_file.name} + "
            f"{annotation_file.name}"
        )

    # Create train/validation/test
    create_dataset_split()

    print()
    print(
        "================================"
    )

    print(
        "Generation completed!"
    )

    print(
        f"Output folder: {OUTPUT_DIR}"
    )

    print(
        "================================"
    )


# ==============================
# PROGRAM ENTRY POINT
# ==============================

if __name__ == "__main__":
    main()