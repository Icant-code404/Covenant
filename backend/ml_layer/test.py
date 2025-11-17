# test_contract_classification.py
from preprocess import clean_text, split_into_clauses
from classify import classify_clauses
import os

# Path to sample contract
current_dir = os.path.dirname(__file__)
txt_path = os.path.join(current_dir, "sample_contract.txt")

with open(txt_path, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Preprocess
cleaned_text = clean_text(raw_text)
clauses = split_into_clauses(cleaned_text)
print(f"Total clauses extracted: {len(clauses)}")

# Classify
classified_clauses = classify_clauses(clauses)

# Print results
for i, c in enumerate(classified_clauses, 1):
    print(f"Clause {i}: {c['clause']}")
    print(f"  → Predicted Type: {c['label']} (Score: {c['score']:.2f})\n")
