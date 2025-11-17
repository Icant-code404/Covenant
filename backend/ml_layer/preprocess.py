# ml_layer/preprocess.py
import re
from pathlib import Path

def clean_text(text: str) -> str:
    """Normalize spaces and remove extra newlines."""
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def split_into_clauses(text: str) -> list[str]:
    """
    Split text into logical clauses:
    - Top-level headers (1., 2., etc.) start a new clause.
    - Subsections (A., B., etc.) merge with previous line.
    - All-caps lines treated as headers merged with next line.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    clauses = []
    buffer = ""
    for line in lines:
        top_level = re.match(r"^\d+\.", line)
        subsection = re.match(r"^[A-Z]\.", line)
        all_caps = re.match(r"^[A-Z\s]{3,}$", line) and len(line) > 3

        if top_level:
            if buffer:
                clauses.append(buffer.strip())
            buffer = line
        elif subsection or all_caps:
            buffer += " " + line if buffer else line
        else:
            buffer += " " + line if buffer else line

    if buffer:
        clauses.append(buffer.strip())

    # Normalize whitespace
    return [re.sub(r"\s+", " ", c) for c in clauses]

def preprocess_file(file_path: str | Path) -> list[str]:
    """Read uploaded file, clean text, and extract clauses."""
    file_path = Path(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    cleaned = clean_text(raw_text)
    clauses = split_into_clauses(cleaned)
    return clauses
