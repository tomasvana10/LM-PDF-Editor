from fastapi import FastAPI
import fitz
from pydantic import BaseModel
from os import path

from ..helpers import PDFHelper, HTMLHelper
from ..lm import LMClient

app = FastAPI()


class UpsertableArgs(BaseModel):
    src_file: str | None = None
    dest_file: str | None = None
    user_context: str
    model: str


@app.post("/api/pdf/upsert")
def upsert_pdf(args: UpsertableArgs):
    pdfh = PDFHelper()
    htmlh = HTMLHelper()
    lms = LMClient()

    original_html = ""
    if args.src_file:
        # `src_file` exists. This means the user is trying to edit an existing
        # PDF, so we will load it, convert it to HTML, and add it for context.
        try:
            original_html = pdfh.to_html(pdfh.read(args.src_file))
        except fitz.FileNotFoundError:
            pass

    # modify the html and convert it back to a pdf
    html = lms.process_html(args.user_context, original_html, args.model)
    pdf = htmlh.to_pdf(html)

    write_error = False

    try:
        if args.dest_file:
            pdfh.write(pdf, args.dest_file)
    except FileNotFoundError:
        write_error = True

    # if writing was successful, output the absolute path of the file that was written to
    # otherwise, output the datat that was written
    return {
        "value": path.abspath(args.dest_file)
        if args.dest_file and not write_error
        else pdf
    }


@app.get("/api/models/all")
def get_all_models():
    return LMClient().get_models()


@app.get("/api/models/active")
def get_active_models():
    return LMClient().get_models(only_active=True)
