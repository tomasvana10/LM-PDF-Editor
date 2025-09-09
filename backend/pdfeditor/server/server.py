from fastapi import FastAPI
from pydantic import BaseModel

from ..helpers import PDFHelper, HTMLHelper
from ..lm import LMClient

app = FastAPI()


class UpsertableArgs(BaseModel):
    src_file: str | None
    dest_file: str | None
    user_context: str
    model: str


@app.post("/api/pdf/upsert")
def upsert_pdf(args: UpsertableArgs):
    pdfh = PDFHelper()
    htmlh = HTMLHelper()
    lms = LMClient()

    original_html = ""
    if args.src_file:
        try:
            original_html = pdfh.to_html(pdfh.read(args.src_file))
        except FileNotFoundError:
            pass

    html = lms.ask_full(args.user_context, original_html, args.model)
    pdf = htmlh.to_pdf(html)

    if args.dest_file:
        pdfh.write(pdf, args.dest_file)

    return {"ctx": args.dest_file or pdf}


@app.get("/api/models/all")
def get_all_models():
    lms = LMClient()
    return lms.get_models()


@app.get("/api/models/active")
def get_active_models():
    lms = LMClient()
    return lms.get_models(only_active=True)
