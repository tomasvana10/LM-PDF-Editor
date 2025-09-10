from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator, FilePath
from typing import ClassVar
from pathlib import Path
from io import BytesIO

from ..helpers import PDFHelper, HTMLHelper
from ..lm import LMClient
from ..utils import find_unique_filepath

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UpsertArgs(BaseModel):
    src_file: FilePath | None = None
    dest_file: Path | None = None
    overwrite: bool = False
    user_context: str
    model: str

    _extension: ClassVar[str] = ""

    @field_validator("src_file", "dest_file", mode="after")
    def check_files(cls, value: FilePath | Path | None) -> Path | None:
        if value is None:
            return value
        if value.suffix != cls._extension:
            raise ValueError(f"File '{value}' must have '{cls._extension}' extension")
        return value


class PDFUpsertArgs(UpsertArgs):
    _extension: ClassVar[str] = ".pdf"


class HTMLUpsertArgs(UpsertArgs):
    _extension: ClassVar[str] = ".html"


@app.post("/api/pdf")
def upsert_pdf(args: PDFUpsertArgs):
    pdfh = PDFHelper()
    htmlh = HTMLHelper()
    lms = LMClient()

    og_html = pdfh.to_html(pdfh.read(str(args.src_file))) if args.src_file else ""
    html = lms.process_html(args.user_context, og_html, args.model)
    pdf = htmlh.to_pdf(html)

    headers = {"Content-Disposition": "inline; filename=preview.pdf"}

    if args.dest_file:
        pdfh.write(
            pdf,
            str(
                find_unique_filepath(args.dest_file)
                if not args.overwrite
                else str(args.dest_file)
            ),
        )
        return FileResponse(
            path=args.dest_file,
            media_type="application/pdf",
            filename=args.dest_file.name,
            headers=headers,
        )

    return StreamingResponse(
        BytesIO(pdf),
        headers=headers,
        media_type="application/pdf",
    )


@app.post("/api/html")
def upsert_html(args: HTMLUpsertArgs):
    htmlh = HTMLHelper()
    lms = LMClient()

    og_html = htmlh.read(str(args.src_file)) if args.src_file else ""
    html = lms.process_html(args.user_context, og_html, args.model)

    headers = {"Content-Disposition": "inline; filename=preview.pdf"}

    if args.dest_file:
        htmlh.write(
            html,
            str(
                find_unique_filepath(args.dest_file)
                if not args.overwrite
                else str(args.dest_file)
            ),
        )
        return FileResponse(
            path=args.dest_file,
            media_type="text/html",
            filename=args.dest_file.name,
            headers=headers,
        )

    return Response(
        content=html,
        headers=headers,
        media_type="text/html",
    )


@app.get("/api/models/all")
def get_all_models():
    return LMClient().get_models()


@app.get("/api/models/active")
def get_active_models():
    return LMClient().get_models(only_active=True)
