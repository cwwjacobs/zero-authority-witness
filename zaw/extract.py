"""
Zero Authority Witness — Text extraction

Supports:
- .html / .htm via stdlib html.parser (scripts and styles are stripped)
- .txt, .md, .json (treated as text for the base proof; structured extraction can be added later)
No authority is granted or implied during extraction.
"""

from __future__ import annotations

import html.parser
from pathlib import Path
from typing import List


class TextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: List[str] = []
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() == "script":
            self.in_script = True
        if tag.lower() == "style":
            self.in_style = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script":
            self.in_script = False
        if tag.lower() == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if not self.in_script and not self.in_style:
            text = data.strip()
            if text:
                self.parts.append(text)

    def handle_comment(self, data: str) -> None:
        text = data.strip()
        if text:
            self.parts.append(text)


def extract_text(source_text: str, source_suffix: str) -> str:
    suffix = source_suffix.lower()
    if suffix in {".html", ".htm"}:
        parser = TextExtractor()
        parser.feed(source_text)
        return "\n".join(parser.parts)
    # For .json, .md, .txt and everything else we return the raw text for the base proof.
    # Structured JSON extraction can be layered on top without changing this contract.
    return source_text


def write_extracted(run_dir: Path, extracted_text: str) -> Path:
    p = run_dir / "extracted_text.txt"
    p.write_text(extracted_text, encoding="utf-8")
    return p
