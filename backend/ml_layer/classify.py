# ml_layer/classify.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pathlib import Path
from typing import List

# ---- CONFIG ----
MODEL_DIR = Path(__file__).parent / "models" / "inlegalbert_finetuned"
MAX_TOKEN_LEN = 512  # BERT max input length

def load_model():
    """Load tokenizer and fine-tuned model locally."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR, local_files_only=True)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return classifier, tokenizer

def chunk_clause(clause: str, tokenizer) -> List[str]:
    """Split long clauses into chunks for BERT."""
    tokens = tokenizer(clause, truncation=False, add_special_tokens=False)["input_ids"]
    if len(tokens) <= MAX_TOKEN_LEN:
        return [clause]
    chunks = []
    for i in range(0, len(tokens), MAX_TOKEN_LEN):
        chunk_tokens = tokens[i:i+MAX_TOKEN_LEN]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
    return chunks

def classify_clauses(clauses: List[str]) -> list[dict]:
    """Classify each clause (or chunk if too long)."""
    classifier, tokenizer = load_model()
    results = []

    for clause in clauses:
        clause_chunks = chunk_clause(clause, tokenizer)
        chunk_preds = []

        for chunk in clause_chunks:
            pred = classifier(chunk)[0]  # dict with label & score
            chunk_preds.append(pred)

        # Take chunk with highest score as representative
        best_pred = max(chunk_preds, key=lambda x: x["score"])
        results.append({
            "clause": clause,
            "label": best_pred["label"],
            "score": best_pred["score"]
        })

    return results

if __name__ == "__main__":
    # Quick local test
    from preprocess import preprocess_file
    sample_file = Path(__file__).parent / "sample_contract.txt"
    clauses = preprocess_file(sample_file)
    print(f"Total clauses extracted: {len(clauses)}")

    classified = classify_clauses(clauses)
    for c in classified:
        print(f"\nClause: {c['clause']}\nPredicted: {c['label']} ({c['score']:.2f})")
