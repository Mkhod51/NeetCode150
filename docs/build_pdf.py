#!/usr/bin/env python3
"""Build docs/guide.pdf from docs/GUIDE.md.

A small, self-contained Markdown to PDF builder using reportlab. It produces a
print-ready handbook: a cover page, a table of contents with real page numbers
(two-pass build), footer page numbers, a clear heading hierarchy, monospace
code boxes and a fresh page for each of the 18 category primers.

Requires reportlab. Create an isolated environment and run it from the repo
root:

    python3 -m venv .venv
    ./.venv/bin/python -m pip install reportlab
    ./.venv/bin/python docs/build_pdf.py

The .venv folder is gitignored; only docs/guide.pdf and this script are
committed.
"""
import pathlib
import re

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Preformatted,
    Spacer, Table, TableStyle, NextPageTemplate,
)
from reportlab.platypus.tableofcontents import TableOfContents

# --------------------------------------------------------------------------- setup

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "docs" / "GUIDE.md"
OUT = REPO_ROOT / "docs" / "guide.pdf"

PAGE_W, PAGE_H = letter
MARGIN_X = 0.95 * inch
MARGIN_TOP = 0.95 * inch
MARGIN_BOTTOM = 1.0 * inch

INK = HexColor("#1b1b1b")
ACCENT = HexColor("#22506b")
SUBTLE = HexColor("#5a5a5a")
CODE_INK = HexColor("#20303a")
CODE_BG = HexColor("#f4f5f6")
CODE_BORDER = HexColor("#d9dde0")
RULE = HexColor("#c9ced2")

BODY = ParagraphStyle(
    "body", fontName="Times-Roman", fontSize=10.5, leading=15.5,
    textColor=INK, spaceAfter=7, alignment=0)
BULLET = ParagraphStyle(
    "bullet", parent=BODY, leftIndent=16, bulletIndent=4, spaceAfter=3)
H1 = ParagraphStyle(
    "h1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=ACCENT,
    spaceBefore=6, spaceAfter=10, keepWithNext=1)
H2 = ParagraphStyle(
    "h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=ACCENT,
    spaceBefore=4, spaceAfter=7, keepWithNext=1)
COVER_TITLE = ParagraphStyle(
    "coverTitle", fontName="Helvetica-Bold", fontSize=30, leading=36,
    textColor=ACCENT, alignment=TA_CENTER)
COVER_SUB = ParagraphStyle(
    "coverSub", fontName="Times-Italic", fontSize=13, leading=19,
    textColor=SUBTLE, alignment=TA_CENTER)
CODE = ParagraphStyle(
    "code", fontName="Courier", fontSize=8.6, leading=11.6, textColor=CODE_INK)
TOC_HEAD = ParagraphStyle(
    "tocHead", fontName="Helvetica-Bold", fontSize=15, leading=20,
    textColor=ACCENT, spaceAfter=12)

# --------------------------------------------------------------------------- markdown

def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text):
    """Convert a subset of inline Markdown to reportlab markup."""
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(
        r"`([^`]+)`",
        lambda m: '<font face="Courier" size="9">%s</font>' % m.group(1),
        text)
    return text


def parse_blocks(md):
    """Turn Markdown into a list of (kind, payload) blocks."""
    blocks = []
    para = []
    bullets = []
    in_code = False
    code = []

    def flush_para():
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()

    def flush_bullets():
        if bullets:
            blocks.append(("ul", list(bullets)))
            bullets.clear()

    for line in md.splitlines():
        if line.startswith("```"):
            if in_code:
                blocks.append(("code", "\n".join(code)))
                code = []
                in_code = False
            else:
                flush_para()
                flush_bullets()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if line.startswith("# "):
            flush_para(); flush_bullets(); blocks.append(("h1doc", line[2:].strip()))
        elif line.startswith("## "):
            flush_para(); flush_bullets(); blocks.append(("h1", line[3:].strip()))
        elif line.startswith("### "):
            flush_para(); flush_bullets(); blocks.append(("h2", line[4:].strip()))
        elif line.strip() == "---":
            flush_para(); flush_bullets()
        elif line.startswith("- "):
            flush_para(); bullets.append(line[2:].strip())
        elif line.strip() == "":
            flush_para(); flush_bullets()
        else:
            flush_bullets(); para.append(line.strip())
    flush_para(); flush_bullets()
    return blocks


# --------------------------------------------------------------------------- document

class GuideDoc(BaseDocTemplate):
    """Doc template that feeds heading positions to the table of contents."""

    def afterFlowable(self, flowable):
        level = getattr(flowable, "_toc_level", None)
        if level is None:
            return
        text = flowable.getPlainText()
        key = getattr(flowable, "_key")
        self.canv.bookmarkPage(key)
        self.notify("TOCEntry", (level, text, self.page, key))
        self.canv.addOutlineEntry(text, key, level=level, closed=(level > 0))


_counter = [0]


def heading(text, level):
    style = H1 if level == 0 else H2
    para = Paragraph(inline(text), style)
    para._toc_level = level
    _counter[0] += 1
    key = "h%d_%d" % (level, _counter[0])
    para._key = key
    para._bookmarkKey = key
    return para


def code_block(text):
    inner = Preformatted(text, CODE)
    table = Table([[inner]], colWidths=[PAGE_W - 2 * MARGIN_X])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("BOX", (0, 0), (-1, -1), 0.6, CODE_BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    table.spaceBefore = 4
    table.spaceAfter = 9
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_X, MARGIN_BOTTOM - 14, PAGE_W - MARGIN_X, MARGIN_BOTTOM - 14)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(SUBTLE)
    canvas.drawCentredString(PAGE_W / 2, MARGIN_BOTTOM - 26, str(doc.page))
    canvas.drawString(MARGIN_X, MARGIN_BOTTOM - 26, "NeetCode 150 User Guide")
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PAGE_H - 0.55 * inch, PAGE_W, 0.55 * inch, stroke=0, fill=1)
    canvas.rect(0, 0, PAGE_W, 0.35 * inch, stroke=0, fill=1)
    canvas.restoreState()


def build():
    md = SRC.read_text(encoding="utf-8")
    blocks = parse_blocks(md)

    # Pull the cover title and one-line description off the front.
    title = "NeetCode 150 User Guide"
    subtitle = ""
    body_blocks = []
    seen_title = False
    for kind, payload in blocks:
        if kind == "h1doc" and not seen_title:
            title = payload
            seen_title = True
            continue
        if seen_title and not subtitle and kind == "p":
            subtitle = payload
            continue
        body_blocks.append((kind, payload))

    frame = Frame(
        MARGIN_X, MARGIN_BOTTOM, PAGE_W - 2 * MARGIN_X,
        PAGE_H - MARGIN_TOP - MARGIN_BOTTOM, id="main",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = GuideDoc(
        str(OUT), pagesize=letter, title=title,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=cover),
        PageTemplate(id="body", frames=[frame], onPage=footer),
    ])

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName="Helvetica-Bold", fontSize=10.5,
                       leading=17, textColor=INK),
        ParagraphStyle("toc1", fontName="Helvetica", fontSize=9.5,
                       leading=13.5, leftIndent=16, textColor=SUBTLE),
    ]

    story = []
    # Cover.
    story.append(Spacer(1, 2.7 * inch))
    story.append(Paragraph(esc(title), COVER_TITLE))
    story.append(Spacer(1, 0.35 * inch))
    if subtitle:
        story.append(Paragraph(esc(subtitle), COVER_SUB))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # Table of contents.
    story.append(Paragraph("Contents", TOC_HEAD))
    story.append(toc)
    story.append(PageBreak())

    # Body.
    in_primers = False
    primer_started = False
    for kind, payload in body_blocks:
        if kind == "h1":
            in_primers = payload.lower().startswith("8.")
            primer_started = False
            story.append(heading(payload, 0))
        elif kind == "h2":
            if in_primers:
                # Each category primer starts on a fresh page.
                story.append(PageBreak())
                primer_started = True
            story.append(heading(payload, 1))
        elif kind == "p":
            story.append(Paragraph(inline(payload), BODY))
        elif kind == "ul":
            for item in payload:
                story.append(Paragraph(inline(item), BULLET, bulletText="•"))
        elif kind == "code":
            story.append(code_block(payload))

    doc.multiBuild(story)
    print("Wrote", OUT.relative_to(REPO_ROOT))


if __name__ == "__main__":
    build()
