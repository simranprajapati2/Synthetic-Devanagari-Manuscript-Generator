from pathlib import Path
from datasets import Dataset, DatasetDict, Image

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "output"

SCRIPTS = ["devanagari", "modi", "sharada"]


def load_split(script, split):
    split_dir = DATA_DIR / script / split

    if not split_dir.exists():
        return None

    image_files = sorted(split_dir.glob("*.png"))

    records = []

    for image_file in image_files:
        annotation_file = image_file.with_suffix(".md")

        if not annotation_file.exists():
            print(f"Warning: annotation missing for {image_file.name}")
            continue

        text = annotation_file.read_text(encoding="utf-8")

        # Ground truth section se actual text extract karo
        marker_start = "## Ground Truth Text"

        if marker_start in text:
            ground_truth = text.split(marker_start, 1)[1]

            if "## Generation Information" in ground_truth:
                ground_truth = ground_truth.split(
                    "## Generation Information", 1
                )[0]

            ground_truth = ground_truth.strip()
        else:
            ground_truth = ""

        records.append(
            {
                "image": str(image_file),
                "text": ground_truth,
                "script": script,
                "filename": image_file.name,
            }
        )

    return records


def build_script_dataset(script):
    print()
    print(f"Building dataset: {script}")
    print("--------------------------------")

    split_data = {}

    for split in ["train", "validation", "test"]:
        records = load_split(script, split)

        if records is None:
            print(f"{split}: folder not found")
            continue

        print(f"{split}: {len(records)} samples")

        split_data[split] = Dataset.from_list(records)

    if not split_data:
        return None

    dataset = DatasetDict(split_data)

    # Convert image path → actual image feature
    for split in dataset:
        dataset[split] = dataset[split].cast_column(
            "image",
            Image()
        )

    return dataset


def main():
    print("Synthetic Indic Manuscript Dataset Builder")
    print("==========================================")

    datasets = {}

    for script in SCRIPTS:
        dataset = build_script_dataset(script)

        if dataset is not None:
            datasets[script] = dataset

    print()
    print("Dataset summary")
    print("================")

    for script, dataset in datasets.items():
        print(f"\n{script}:")
        for split in dataset:
            print(f"  {split}: {len(dataset[split])}")

    print()
    print("Dataset building completed.")


if __name__ == "__main__":
    main()
