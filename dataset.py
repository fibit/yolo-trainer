import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python dataset.py DatasetName", file=sys.stderr)
        return 1

    dataset_name = sys.argv[1]
    dataset_dir = Path("datasets") / dataset_name

    if dataset_dir.exists():
        print(f"Dataset already exists: {dataset_dir}", file=sys.stderr)
        return 1

    for split in ("train", "valid", "test"):
        for subdir in ("images", "labels"):
            (dataset_dir / split / subdir).mkdir(parents=True, exist_ok=True)

    (dataset_dir / "data.yaml").write_text(
        """train: train/images
val: valid/images
test: test/images

nc: 0
names: []
""",
        encoding="utf-8",
    )

    print(f"Created empty dataset: {dataset_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
