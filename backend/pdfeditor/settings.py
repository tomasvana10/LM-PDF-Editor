import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv


class PDFEditorSettings(TypedDict):
    LMS_HOST: str
    LMS_PORT: int
    API_HOST: str
    API_PORT: int


env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)


def get_settings() -> PDFEditorSettings:
    return PDFEditorSettings(
        LMS_HOST=os.environ["LMS_HOST"],
        LMS_PORT=int(os.environ["LMS_PORT"]),
        API_HOST=os.environ["API_HOST"],
        API_PORT=int(os.environ["API_PORT"]),
    )
