from typing import final, override
import subprocess
import shutil

from .fs_base import FSBase


wkhtmltopdf = shutil.which("wkhtmltopdf")
if wkhtmltopdf is None:
    raise FileNotFoundError("wkhtmltopdf was not installed properly")


@final
class HTMLHelper(FSBase[str, str]):
    @override
    def write(self, data: str, dest: str) -> None:
        if not dest.endswith(".html"):
            raise ValueError("Destination file must end with '.html'")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(data)

    @override
    def read(self, src: str) -> str:
        with open(src, "r", encoding="utf-8") as f:
            return f.read()

    def to_pdf(self, data: str) -> bytes:
        cmd: list[str] = [
            wkhtmltopdf,  # pyright: ignore[reportAssignmentType]
            "--enable-local-file-access",
            "--disable-smart-shrinking",
            "--encoding",
            "UTF-8",
            "-",
            "-",
        ]

        result = subprocess.run(
            cmd,
            input=data.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return result.stdout
