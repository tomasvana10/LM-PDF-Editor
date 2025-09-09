from typing import final, override

import fitz

from .helper import Helper


@final
class PDFHelper(Helper[bytes, fitz.Document]):
    _styles = """
body { line-height: 1.4; margin:0; padding:0; font-family: Arial, sans-serif; }
p { margin:0; }
.sup { vertical-align: super; font-size: smaller; }
.sub { vertical-align: sub; font-size: smaller; }
"""

    @override
    def write(self, data: bytes, dest: str) -> None:
        if not dest.endswith(".pdf"):
            raise ValueError("Destination file must end with '.pdf'")
        with open(dest, "xb") as f:
            f.write(data)

    @override
    def read(self, src: str) -> fitz.Document:
        return fitz.open(src)

    def to_html(self, data: fitz.Document) -> str:
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
        html = [
            "<html><head><style>" + self.__class__._styles + "</style></head><body>",
        ]

        for page in data:
            blocks = page.get_text("dict")["blocks"] # pyright: ignore[reportAttributeAccessIssue]
            for block in blocks:
                if block["type"] == 0:  # text block
                    for line in block["lines"]:
                        line_html = ""
                        for span in line["spans"]:
                            text = (
                                span["text"]
                                .replace("&", "&amp;")
                                .replace("<", "&lt;")
                                .replace(">", "&gt;")
                            )
                            font = span["font"]
                            size = span["size"]
                            color_int = span.get("color", 0)
                            color_hex = f"#{color_int:06X}"
                            flags = span.get("flags", 0)

                            # Bold / Italic / Underline / Strikeout
                            if "bold" in font.lower():
                                text = f"<b>{text}</b>"
                            if "italic" in font.lower() or "oblique" in font.lower():
                                text = f"<i>{text}</i>"
                            if flags & 1:  # underline
                                text = f"<u>{text}</u>"
                            if flags & 2:  # strikeout
                                text = f"<s>{text}</s>"

                            # Superscript / Subscript heuristic
                            if (
                                span.get("origin", (0, 0))[1] < 0
                            ):  # slightly above baseline
                                text = f'<span class="sup">{text}</span>'
                            elif (
                                span.get("origin", (0, 0))[1] > 0
                            ):  # slightly below baseline
                                text = f'<span class="sub">{text}</span>'

                            line_html += f'<span style="font-family:{font}; font-size:{size}pt; color:{color_hex}">{text}</span>'

                        html.append(f"<p>{line_html}</p>")

        html.append("</body></html>")

        return "".join(html)
