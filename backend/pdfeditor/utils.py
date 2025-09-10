from pathlib import Path


def find_unique_filepath(path: Path) -> Path:
    if not path.exists():
        return path

    stem, suffix = path.stem, path.suffix
    counter = 1
    while True:
        new_path = path.with_name(f"{stem} ({counter}){suffix}")
        if not new_path.exists():
            return new_path
        counter += 1
