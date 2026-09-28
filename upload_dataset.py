from pathlib import Path
from datasets import Dataset, DatasetDict, Image
from huggingface_hub import HfApi

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "output"

# YAHAN APNA HUGGING FACE USERNAME LIKHO
HF_USERNAME = "simranprajapa"

REPO_NAME = f"{HF_USERNAME}/synthetic-indic-manuscripts"


def load_split(script, split):
    split_dir = DATA_DIR / script / split

    if not split_dir.exists():
        return None

    records = []

    for image_file in sorted(split_dir.glob("*.png")):
        md_file = image_file.with_suffix(".md")

        if not md_file.exists():
            continue

        annotation = md_file.read_text(encoding="utf-8")

        marker = "## Ground Truth Text"

        if marker in annotation:
            text = annotation.split(marker, 1)[1]

            if "## Generation Information" in text:
                text = text.split(
                    "## Generation Information",
                    1
                )[0]

            text = text.strip()
        else:
            text = ""

        records.append({
            "image": str(image_file),
            "text": text,
            "script": script,
            "filename": image_file.name
        })

    if not records:
        return None

    dataset = Dataset.from_list(records)

    dataset = dataset.cast_column(
        "image",
        Image()
    )

    return dataset


def build_dataset(script):
    splits = {}

    for split in ["train", "validation", "test"]:
        dataset = load_split(script, split)

        if dataset is not None:
            splits[split] = dataset
            print(f"{script} / {split}: {len(dataset)}")

    if not splits:
        return None

    return DatasetDict(splits)


def main():

    print("Building Hugging Face dataset")
    print("================================")

    datasets = {}

    # Currently available
    devanagari = build_dataset("devanagari")

    if devanagari:
        datasets["devanagari"] = devanagari

    if not datasets:
        raise RuntimeError(
            "No dataset found. Run generate.py first."
        )

    # Create Hugging Face repository
    api = HfApi()

    api.create_repo(
        repo_id=REPO_NAME,
        repo_type="dataset",
        exist_ok=True,
        private=False
    )

    print()
    print(f"Uploading to: {REPO_NAME}")
    print()

    # Upload Devanagari configuration
    datasets["devanagari"].push_to_hub(
        REPO_NAME,
        config_name="devanagari"
    )

    print()
    print("================================")
    print("Upload completed!")
    print(f"https://huggingface.co/datasets/{REPO_NAME}")
    print("================================")


if __name__ == "__main__":
    main()