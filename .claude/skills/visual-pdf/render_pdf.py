#!/usr/bin/env python3
"""Render an HTML file to PDF with WeasyPrint (part of the visual-pdf skill).

On macOS the Homebrew native libraries (pango, cairo, harfbuzz) are not on the
default loader path, so WeasyPrint fails to import. This script fixes that
automatically: it sets DYLD_FALLBACK_LIBRARY_PATH and re-execs itself once so
the dynamic loader picks the libraries up. You can therefore just run:

    ./.venv/bin/python render_pdf.py input.html output.pdf [--png OUTDIR]

Requires weasyprint (and pymupdf only if you pass --png for page previews).
"""
import os
import sys


def _ensure_native_libs():
    """On macOS, put Homebrew's lib dir on the loader path and re-exec once."""
    if sys.platform != "darwin":
        return
    candidates = ["/opt/homebrew/lib", "/usr/local/lib"]
    libdir = next((d for d in candidates if os.path.isdir(d)), None)
    if not libdir:
        return
    current = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if libdir in current.split(":"):
        return  # already set: do not re-exec again
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(
        p for p in (current, libdir) if p)
    os.execv(sys.executable, [sys.executable] + sys.argv)


_ensure_native_libs()

import argparse  # noqa: E402
import pathlib  # noqa: E402

from weasyprint import HTML  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render an HTML file to a PDF with WeasyPrint.")
    parser.add_argument("html", help="input HTML file")
    parser.add_argument("pdf", help="output PDF file")
    parser.add_argument("--png", help="also write page PNGs to this directory")
    parser.add_argument("--dpi", type=int, default=110,
                        help="DPI for the PNG previews (default 110)")
    args = parser.parse_args(argv)

    src = pathlib.Path(args.html).resolve()
    HTML(str(src)).write_pdf(args.pdf)
    print("Wrote", args.pdf)

    if args.png:
        import fitz  # pymupdf, only needed for previews
        out = pathlib.Path(args.png)
        out.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(args.pdf)
        for i in range(doc.page_count):
            doc[i].get_pixmap(dpi=args.dpi).save(str(out / ("page%02d.png" % (i + 1))))
        print("Rendered %d page PNG(s) to %s" % (doc.page_count, out))


if __name__ == "__main__":
    main()
