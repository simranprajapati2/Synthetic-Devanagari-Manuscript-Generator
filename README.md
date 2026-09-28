# Synthetic Devanagari Manuscript Generator

A Python-based project for generating synthetic **Devanagari manuscript-style images** with realistic paper aging, ink variation, stains, fading, and other document effects.

The generated dataset contains manuscript images along with their **ground-truth text annotations**, making it useful for OCR and document-image research.

## Features

- Devanagari script generation
- Synthetic aged-paper backgrounds
- Ink variation and fading
- Paper stains and creases
- Edge-aging effects
- Ground-truth text annotations
- Train / Validation / Test split
- Hugging Face dataset support

## Project Structure

```text
synthetic-indic-manuscript/
│
├── generate.py
├── dataset_builder.py
├── upload_dataset.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   └── devanagari.txt
│   └── output/
│       └── devanagari/
│           ├── train/
│           ├── validation/
│           └── test/
│
├── fonts/
│   └── NotoSansDevanagari-Regular.ttf
│
└── src/
    ├── background.py
    ├── renderer.py
    └── effects.py
Requirements
Python 3.10+
Pillow
NumPy
Datasets
Hugging Face Hub
PyYAML
tqdm
Installation
python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Generate Dataset

Add unique Devanagari text samples to:

data/raw/devanagari.txt

Then run:

python generate.py

The generator creates:

Train       → 85%
Validation  → 10%
Test        → 5%

Each image has a corresponding .md file containing its ground-truth text.

Build Dataset
python dataset_builder.py
Upload to Hugging Face

Login first:

hf auth login

Then:

python upload_dataset.py
Dataset

The dataset contains:

image
text
script
filename

Example:

image    → manuscript_0001.png
text     → Devanagari ground-truth text
script   → devanagari
filename → manuscript_0001.png
Applications

This dataset can be used for:

Devanagari OCR
Document image analysis
Computer vision
Synthetic data generation
Indic script recognition
Current Scope

The current version supports Devanagari only. The architecture can be extended to other Indic scripts in the future.