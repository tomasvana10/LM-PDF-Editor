from typing import Annotated
from fastapi import FastAPI, Form, Response, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO

from ..helpers import PDFHelper, HTMLHelper
from ..lm import LMClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/pdf")
async def edit_pdf(
    user_context: Annotated[str, Form()],
    model: Annotated[str, Form()],
    existing_file: UploadFile | None = None,
):
    lms = LMClient()
    pdfh = PDFHelper()

    existing_html = (
        pdfh.to_html(pdfh.read(await existing_file.read())) if existing_file else ""
    )
    html = lms.process_html(user_context, existing_html, model)
    pdf = HTMLHelper().to_pdf(html)

    headers = {"Content-Disposition": "inline; filename=output.pdf"}

    return StreamingResponse(
        BytesIO(pdf),
        headers=headers,
        media_type="application/pdf",
    )


@app.post("/api/html")
async def edit_html(
    user_context: Annotated[str, Form()],
    model: Annotated[str, Form()],
    existing_file: UploadFile | None = None,
):
    lms = LMClient()

    existing_html = (
        (await existing_file.read()).decode("utf-8") if existing_file else ""
    )
    html = lms.process_html(user_context, existing_html, model)

    headers = {"Content-Disposition": "inline; filename=output.html"}

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
