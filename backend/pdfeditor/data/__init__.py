from pathlib import Path


def read_data(file: str):
    with open(Path(__file__).resolve().parent / file, encoding="utf-8") as f:
        return f.read()
