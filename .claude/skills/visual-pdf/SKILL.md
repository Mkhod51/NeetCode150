---
name: visual-pdf
description: Create visually rich, print-ready PDFs from HTML and CSS using WeasyPrint. Use when the user wants an attractive, colourful PDF (a guide, handbook, report or booklet) with a cover page, callout boxes, cards, coloured badges, a table of contents with real page numbers and page footers, rather than a plain headings-and-text PDF.
---

# Visual PDF

Build good-looking PDFs by writing HTML and CSS, then rendering with WeasyPrint.
This gives full modern CSS (colours, gradients, flexbox, callout boxes, page
counters, a table of contents with real page numbers) which plain reportlab
does not. Use it whenever a document should look designed, not just typed.

## Setup (once)

WeasyPrint needs a Python environment and, on macOS, the Homebrew native
libraries (pango, cairo, harfbuzz). Create a virtualenv and install:

```
python3 -m venv .venv
./.venv/bin/python -m pip install weasyprint pymupdf
```

`pymupdf` is only for rasterising pages so you can visually check the result;
it is not needed for the PDF itself. Keep `.venv` out of git.

On macOS the render helper below sets `DYLD_FALLBACK_LIBRARY_PATH` to
`/opt/homebrew/lib` for you, so you do not need to export it by hand.

## How to build a visual PDF

1. Write a single self-contained HTML file. Put the CSS in one `<style>` block
   so the PDF is reproducible from one file. Use the component classes in
   `reference.css` (copy the ones you need into your `<style>`): `.cover`,
   `.callout` with `.tip` / `.warn` / `.note` / `.rule`, `.cardrow` + `.card`,
   `.badge` with `.easy` / `.med` / `.hard`, `.step`, `.toc`, `.codebox`.
2. Drive page structure with CSS paged media, not manual spacing:
   - `@page { size: letter; margin: ...; @bottom-center { content: counter(page); } }`
   - a named `@page cover { @bottom-center { content: none } }` for a
     footer-free cover, used by `.cover { page: cover }`.
   - `break-before: page` (or `page-break-before: always`) to start a section
     on a fresh page.
   - a table of contents whose links show the target page number with
     `a::after { content: target-counter(attr(href), page); }`.
3. Render and rasterise for review:

```
./.venv/bin/python .claude/skills/visual-pdf/render_pdf.py \
    input.html output.pdf --png /tmp/pdf-review
```

4. Open the PNGs (`Read` them) and check: cover, table-of-contents page numbers
   match, no text overflowing the page, no orphaned headings, callouts and
   cards render. Fix the HTML/CSS and re-render.

## Design guidance

- Pick one accent colour plus a small set of semantic colours (green = tip,
  amber = warning, blue = note, red = important). Reuse them; do not add a new
  colour per element.
- Colour emoji render, so a few (used as consistent anchors, for example one
  per callout type) are fine. Do not scatter them randomly.
- Keep body text one readable font. Use a monospace font only for code.
- Prefer short blocks, callouts and cards over long grey paragraphs. The point
  of this skill is that the reader can skim and find things.

Files in this skill:
- `render_pdf.py` — HTML to PDF via WeasyPrint (handles the macOS lib path),
  optional page-PNG export for review.
- `reference.css` — a component library to copy from.
