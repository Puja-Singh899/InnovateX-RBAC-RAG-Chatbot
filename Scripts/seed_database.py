from pathlib import Path

from backend.indexer import index_document


DATA_DIR = Path("data")

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf"
}


def seed_database():
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            "data/ directory does not exist."
        )

    indexed_count = 0

    for department_dir in DATA_DIR.iterdir():

        if not department_dir.is_dir():
            continue

        department = department_dir.name.lower()

        for file_path in department_dir.iterdir():

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            print(
                f"Indexing: {file_path.name} "
                f"-> {department}"
            )

            result = index_document(
                file_path=str(file_path),
                department=department,
                source_name=file_path.name
            )

            print(
                f"  Chunks created: {result['chunks']}"
            )

            indexed_count += 1

    print(
        f"\nSuccessfully indexed {indexed_count} document(s)."
    )


if __name__ == "__main__":
    seed_database()