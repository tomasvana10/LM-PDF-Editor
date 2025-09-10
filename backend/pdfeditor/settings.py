import tomllib
from typing import TypedDict
from pathlib import Path


class PDFEditorSettings(TypedDict):
    lms_host: str
    lms_port: int
    api_host: str
    api_port: int


settings_path = Path(__file__).resolve().parent / "data" / "settings.toml"


def get_settings():
    with open(settings_path, "rb") as f:
        data = tomllib.load(f)

    config = data.get("default", {}).copy()
    config.update(data.get("user-override", {}))

    return PDFEditorSettings(**config)
