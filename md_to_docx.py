#!/usr/bin/env python3
"""
Simple Markdown to DOCX converter focused on legal/professional docs.

Usage:
    python md_to_docx.py --input markdown/marco_legal_formateado.md --output output/marco_legal_formateado.docx
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from docx import Document


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
NUMBER_RE = re.compile(r"^\s*\d+[\.)]\s+(.*)$")


def convert_md_to_docx(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    doc = Document()

    for raw_line in lines:
        line = raw_line.rstrip()

        if not line.strip():
            doc.add_paragraph("")
            continue

        if line.strip() == "---":
            # Skip markdown horizontal rules
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = min(len(heading_match.group(1)), 4)
            title = heading_match.group(2).strip()
            doc.add_heading(title, level=level)
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            doc.add_paragraph(bullet_match.group(1).strip(), style="List Bullet")
            continue

        number_match = NUMBER_RE.match(line)
        if number_match:
            doc.add_paragraph(number_match.group(1).strip(), style="List Number")
            continue

        # Plain paragraph
        doc.add_paragraph(line)

    doc.save(str(output_path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown file to DOCX")
    parser.add_argument(
        "--input",
        "-i",
        default="markdown/marco_legal_formateado.md",
        help="Input .md file",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output/marco_legal_formateado.docx",
        help="Output .docx file",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    if input_path.suffix.lower() != ".md":
        raise SystemExit("Input must be a .md file")

    if output_path.suffix.lower() != ".docx":
        raise SystemExit("Output must be a .docx file")

    convert_md_to_docx(input_path, output_path)
    print(f"OK: Generated {output_path}")


if __name__ == "__main__":
    main()
