import os
import re

# Path to sample contract
current_dir = os.path.dirname(__file__)
txt_path = os.path.join(current_dir, "sample_contract.txt")

# Read the file
with open(txt_path, "r", encoding="utf-8") as f:
    raw_text = f.read()


def clean_text(text):
    """Basic cleaning: normalize spaces, remove extra newlines."""
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = text.strip()
    return text

def split_into_clauses(text):
    """
    Split text into logical clauses:
    - Top-level headers (1., 2., etc.) are merged with their content.
    - Subsections (A., B., etc.) are merged with following lines.
    - All-caps lines are treated as headers but merged with next line if normal text.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    clauses = []
    buffer = ""
    for i, line in enumerate(lines):
        # Detect line type
        top_level = re.match(r"^\d+\.", line)
        subsection = re.match(r"^[A-Z]\.", line)
        all_caps = re.match(r"^[A-Z\s]{3,}$", line) and len(line) > 3

        # Decide if we should start a new clause
        if top_level:
            if buffer:
                clauses.append(buffer.strip())
            buffer = line  # start new clause buffer
        elif subsection or all_caps:
            if buffer:
                buffer += " " + line
            else:
                buffer = line
        else:
            # Normal text, merge into buffer
            if buffer:
                buffer += " " + line
            else:
                buffer = line

    if buffer:
        clauses.append(buffer.strip())

    # Normalize internal whitespace
    clauses = [re.sub(r"\s+", " ", c) for c in clauses]
    return clauses

# Run preprocessing
cleaned_text = clean_text(raw_text)
clauses = split_into_clauses(cleaned_text)

# Print first 10 clauses
for i, c in enumerate(clauses[:10]):
    print(f"Clause {i+1}: {c}\n")
print(f"Total clauses extracted: {len(clauses)}")   